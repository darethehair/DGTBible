const AUDIO_BASE='https://darethehair.github.io/DGTBible-Audio/dgt-audio-24k/';
const AUDIO_SLOTS=[
 ['01','English male'],['02','English female'],['03','Custom voice'],['04','Original Greek'],
];

function audioTimeout(pending,ms=15000){
 const timer=setTimeout(()=>pending.abort(),ms);
 return ()=>clearTimeout(timer);
}

function recordedAudioSource(base){
 const slots=new Map(),missing=new Map();
 let inventoryId,checked=0,refreshing;
 function refresh(){
  if(refreshing)return refreshing;
  if(Date.now()-checked<30000)return Promise.resolve();
  const controller=new AbortController(),cancelTimeout=audioTimeout(controller);
  refreshing=(async()=>{
   const response=await fetch(`${base}availability.json?t=${Math.floor(Date.now()/60000)}`,
    {cache:'no-store',signal:controller.signal});
   if(!response.ok)throw new Error('The audio library could not be reached.');
   const data=await response.json();
   if(data.version!==1||!Array.isArray(data.files))throw new Error('The audio library inventory is unavailable.');
   const id=JSON.stringify(data.files);
   if(id!==inventoryId){
    slots.clear();missing.clear();
    for(const file of data.files){
     if(typeof file!=='string')continue;
     const match=file.match(/^slot-(0[1-4])\/([\p{L}\p{N} _-]+)\/(\d{3})\/(\d{3})\.opus$/u);
     if(!match)continue;
     const [,slot,book,chapter,verse]=match;
     const key=`${book.toLowerCase().replace(/[^a-z0-9]/g,'')}/${Number(chapter)}/${Number(verse)}`;
     if(!slots.has(slot))slots.set(slot,new Map());
     slots.get(slot).set(key,file);
    }
    inventoryId=id;
   }
   checked=Date.now();
  })().finally(()=>{cancelTimeout();refreshing=null});
  return refreshing;
 }
 function isMissing(file){
  const until=missing.get(file);
  if(until>Date.now())return true;
  missing.delete(file);
  return false;
 }
 async function recording(file,controller){
  if(isMissing(file))return {kind:'missing'};
  const cancelTimeout=audioTimeout(controller);
  try{
   const response=await fetch(base+file.split('/').map(encodeURIComponent).join('/'),{signal:controller.signal});
   if(response.status===404||response.status===410){
    missing.set(file,Date.now()+120000);
    return {kind:'missing'};
   }
   if(response.ok)return {kind:'ready',blob:await response.blob()};
  }catch{/* The request may be offline, timed out, or cancelled. */}
  finally{cancelTimeout()}
  return {kind:'temporary'};
 }
 return {refresh,recording,isMissing,files:slot=>slots.get(slot)||new Map()};
}

function createRecordedAudio({books,reader,reference,base=AUDIO_BASE}){
 const element=id=>document.getElementById(id);
 const launch=element('openAudio'),dock=element('audioDock'),panel=element('audioPanel');
 const passage=element('audioPassage'),narrator=element('audioNarrator'),rate=element('audioRate');
 const autoScroll=element('audioScroll'),audio=element('recordedAudio'),play=element('audioPlay');
 const source=recordedAudioSource(base);
 let run=null,request=0,clipUrl='',mode='idle',current=null;
 let inventoryReady=false,coverageRequest=0,edited=false,retry=null,message='';
 let inputTimer;
 const rates=[0.5,0.75,1,1.25,1.5,1.75,2];
 narrator.replaceChildren(...AUDIO_SLOTS.map(([id,label])=>new Option(label,id)));
 narrator.value=AUDIO_SLOTS.some(([id])=>id===localStorage.getItem('dgt-audio-narrator'))
  ?localStorage.getItem('dgt-audio-narrator'):'02';
 rate.replaceChildren(...rates.map(value=>new Option(value+'×',value)));
 rate.value=rates.includes(Number(localStorage.getItem('dgt-audio-rate')))?localStorage.getItem('dgt-audio-rate'):'1';
 autoScroll.checked=localStorage.getItem('dgt-audio-scroll')!=='off';
 audio.preservesPitch=true;
 audio.webkitPreservesPitch=true;

 function selections(){
  const {slug}=reference();
  return scriptureSelection(passage.value,books,slug);
 }
 async function refresh(){
  await source.refresh();
  inventoryReady=true;
  for(const [id,label] of AUDIO_SLOTS){
   const count=source.files(id).size;
   narrator.querySelector(`[value="${id}"]`).textContent=`${label} · ${count?count.toLocaleString()+' recorded':'empty'}`;
  }
 }
 async function coverage(){
  const tick=++coverageRequest,availability=element('audioAvailability');
  try{
   await refresh();
   const selected=expandScriptureSelection(selections(),await loadScriptureIndex(),books);
   if(tick!==coverageRequest)return;
   const files=source.files(narrator.value);
   const count=selected.filter(verse=>files.has(verse.key)&&!source.isMissing(files.get(verse.key))).length;
   availability.textContent=`${count.toLocaleString()} of ${selected.length.toLocaleString()} verses recorded`;
  }catch(error){
   if(tick===coverageRequest)availability.textContent=inventoryReady?error.message:'Audio availability is temporarily unavailable. Try Play to retry.';
  }
 }
 const describe=verses=>verses.slice(0,2).map(verse=>verse.label).join(', ')+(verses.length>2?` and ${verses.length-2} more`:'');
 function mark(scroll=false){
  for(const node of document.querySelectorAll('.audio-current')){
   node.classList.remove('audio-current');
   node.removeAttribute('aria-current');
  }
  if(current)reader.mark(current,scroll&&autoScroll.checked);
 }
 function clock(seconds){
  return `${Math.floor(seconds/60)}:${String(Math.floor(seconds%60)).padStart(2,'0')}`;
 }
 function timeline(){
  const duration=Number.isFinite(audio.duration)?audio.duration:0;
  element('audioTimeline').hidden=!current;
  element('audioProgress').max=duration||1;
  element('audioProgress').value=audio.currentTime||0;
  element('audioTime').textContent=duration?`${clock(audio.currentTime)} / ${clock(duration)}`:'';
 }
 function nearby(direction){
  if(!run)return -1;
  for(let i=run.position+direction;i>=0&&i<run.queue.length;i+=direction){
   if(!source.isMissing(run.queue[i].file))return i;
  }
  return -1;
 }
 function render(){
  const active=!!run&&['playing','paused','loading'].includes(mode);
  const suffix=[];
  if(run?.missing.size)suffix.push(`Skipped ${run.missing.size.toLocaleString()} missing (${describe([...run.missing.values()])}).`);
  if(run?.failed.size)suffix.push(`${run.failed.size} temporary ${run.failed.size===1?'failure':'failures'} (${describe([...run.failed.values()])}).`);
  element('audioStatus').textContent=[message,...suffix].filter(Boolean).join(' ');
  element('audioSummary').textContent=current?`${current.label} · ${run.position+1}/${run.queue.length}${mode==='paused'?' · Paused':''}`:'';
  play.textContent=mode==='paused'?'Resume':active?'Pause':'Play';
  play.disabled=mode==='checking';
  element('audioStop').disabled=!active&&mode!=='checking';
  element('audioPrevious').disabled=!active||nearby(-1)<0;
  element('audioNext').disabled=!active||nearby(1)<0;
  element('audioRetry').hidden=active||(!retry&&!run?.failed.size);
  timeline();
 }
 function clearClip(){
  audio.pause();
  audio.removeAttribute('src');
  audio.load();
  if(clipUrl)URL.revokeObjectURL(clipUrl);
  clipUrl='';
 }
 function dispose(){
  if(run)for(const {controller} of run.downloads.values())controller.abort();
  clearClip();
  current=null;
  mark();
 }
 function cancel(status=''){
  request++;
  dispose();
  run=null;
  mode='idle';
  retry=null;
  message=status;
  render();
 }
 function download(session,verse){
  let entry=session.downloads.get(verse.file);
  if(!entry){
   const controller=new AbortController();
   const promise=source.recording(verse.file,controller);
   entry={controller,promise};
   session.downloads.set(verse.file,entry);
   promise.then(result=>{
    if(result.kind==='temporary'&&session.downloads.get(verse.file)===entry)
     session.downloads.delete(verse.file);
   });
  }
  return entry.promise;
 }
 function retain(session,files){
  for(const [file,{controller}] of session.downloads){
   if(!files.includes(file)){controller.abort();session.downloads.delete(file)}
  }
 }
 function finish(session){
  dispose();
  mode='idle';
  message=session.played?'Playback finished.':session.failed.size
   ?'Playback could not start. Check your connection and retry.':'No recordings are available for this selection and narrator.';
  render();
  void coverage();
 }
 async function playClip(session,turn){
  const valid=()=>run===session&&session.turn===turn;
  try{
   await audio.play();
   if(!valid()||mode==='paused')return;
  }catch(error){
   if(!valid()||mode==='paused')return;
   if(error.name==='NotAllowedError'){
    mode='paused';message='Tap Resume to allow audio playback.';render();
   }else{
    failClip(session,turn);
   }
   return;
  }
  mode='playing';
  message='';
  session.played=true;
  const verse=current;
  render();
  await reader.follow(verse,()=>valid()&&current===verse);
  if(valid()&&current===verse)mark(true);
 }
 function failClip(session,turn){
  if(run!==session||session.turn!==turn||!current)return;
  session.failed.set(current.key,current);
  void advance(session.position+1);
 }
 async function advance(position,paused=false,direction=1){
  const session=run,turn=++session.turn,origin=session.position;
  clearClip();
  current=null;
  mark();
  mode=paused?'paused':'loading';
  for(let i=position;i>=0&&i<session.queue.length;i+=direction){
   const verse=session.queue[i],next=session.queue[i+1];
   session.position=i;
   message=`Loading ${verse.label}…`;
   render();
   retain(session,[verse.file,next?.file]);
   const wasPrefetch=session.prefetched.delete(verse.file)&&session.downloads.has(verse.file);
   let clip=await download(session,verse);
   if(run!==session||session.turn!==turn)return;
   // A failed look-ahead is retried once when the verse actually becomes due.
   if(clip.kind==='temporary'&&wasPrefetch){
    clip=await download(session,verse);
    if(run!==session||session.turn!==turn)return;
   }
   if(clip.kind==='missing'){session.missing.set(verse.key,verse);continue}
   if(clip.kind==='temporary'){session.failed.set(verse.key,verse);continue}
   session.failed.delete(verse.key);
   current=verse;
   clipUrl=URL.createObjectURL(clip.blob);
   audio.src=clipUrl;
   audio.playbackRate=Number(rate.value);
   if(next&&!source.isMissing(next.file)){
    session.prefetched.add(next.file);
    void download(session,next);
   }
   if(mode==='paused'){message='Paused.';render()}
   else await playClip(session,turn);
   return;
  }
  if(direction<0)await advance(origin,paused);
  else finish(session);
 }
 async function start(failed=null){
  cancel('Checking recordings…');
  const tick=request;
  mode='checking';
  render();
  try{
   if(!audio.canPlayType('audio/ogg; codecs="opus"'))throw new Error('This browser does not support Ogg Opus playback.');
   const parsed=failed?null:selections();
   const [index]=await Promise.all([loadScriptureIndex(),refresh()]);
   if(tick!==request)return;
   const selection=failed||expandScriptureSelection(parsed,index,books);
   const files=source.files(narrator.value),queue=[],missing=new Map();
   for(const verse of selection){
    const file=files.get(verse.key);
    if(file&&!source.isMissing(file))queue.push({...verse,file});
    else missing.set(verse.key,verse);
   }
   run={queue,missing,failed:new Map(),downloads:new Map(),prefetched:new Set(),position:0,turn:0,played:false};
   void coverage();
   if(!queue.length){finish(run);return}
   await advance(0);
  }catch(error){
   if(tick!==request)return;
   mode='idle';
   message=error instanceof TypeError||error.name==='AbortError'?'The audio library is temporarily unavailable. Check your connection and retry.':error.message;
   retry=()=>start(failed);
   render();
  }
 }
 play.onclick=()=>{
  if(mode==='playing'||mode==='loading'){
   mode='paused';audio.pause();message='Paused.';render();
  }else if(mode==='paused'){
   mode='loading';
   if(current)void playClip(run,run.turn);
   render();
  }else void start();
 };
 element('audioPrevious').onclick=()=>advance(run.position-1,mode==='paused',-1);
 element('audioNext').onclick=()=>advance(run.position+1,mode==='paused');
 element('audioStop').onclick=()=>cancel('Playback stopped.');
 element('audioRetry').onclick=()=>{
  if(retry)void retry();
  else if(run?.failed.size)void start([...run.failed.values()]);
 };
 audio.addEventListener('ended',()=>{if(run&&mode==='playing')void advance(run.position+1)});
 audio.addEventListener('error',()=>{if(audio.error&&run)failClip(run,run.turn)});
 for(const event of ['timeupdate','durationchange'])audio.addEventListener(event,timeline);
 rate.onchange=()=>{
  audio.playbackRate=Number(rate.value);
  localStorage.setItem('dgt-audio-rate',rate.value);
 };
 autoScroll.onchange=()=>{
  localStorage.setItem('dgt-audio-scroll',autoScroll.checked?'on':'off');
  if(autoScroll.checked)mark(true);
 };
 narrator.onchange=()=>{
  localStorage.setItem('dgt-audio-narrator',narrator.value);
  cancel();
  void coverage();
 };
 passage.oninput=()=>{
  edited=true;
  cancel();
  clearTimeout(inputTimer);
  inputTimer=setTimeout(coverage,200);
 };
 launch.onclick=()=>{
  if(!dock.hidden&&panel.open){panel.open=false;if(!current&&mode==='idle')dock.hidden=true;return}
  if(!edited&&!run)passage.value=reference().text;
  dock.hidden=false;
  panel.open=true;
  void coverage();
 };
 panel.addEventListener('toggle',()=>launch.setAttribute('aria-expanded',String(!dock.hidden&&panel.open)));
 element('audioHide').onclick=()=>{
  panel.open=false;
  if(mode==='idle')dock.hidden=true;
 };
 new ResizeObserver(()=>document.body.style.setProperty('--audio-dock-height',dock.offsetHeight+'px')).observe(dock);
 setInterval(()=>{if(!dock.hidden&&panel.open&&!document.hidden)void coverage()},60000);
 launch.disabled=false;
 render();
 return {mark};
}
