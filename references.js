/* Scripture selections shared by lookup, audio and future reading plans. */
function scriptureSelection(input, books, currentSlug) {
 const raw=input.trim().toLowerCase().replace(/\s+/g,' ').replace(/[–—]/g,'-');
 if(!raw) throw new Error('Enter a Scripture reference, such as John 1:1-10.');
 const names=books.flatMap(book=>[book.name,...(book.aliases||[])].map(name=>[
  name.toLowerCase().replace(/\s+/g,' '),book.slug,
 ])).sort((a,b)=>b[0].length-a[0].length);
 let slug=currentSlug;
 return raw.split(',').flatMap(part=>{
  let rest=part.trim();
  if(/^(?:the )?(?:entire )?(?:nt|new testament)$/.test(rest))return books.map(book=>({slug:book.slug}));
  const name=names.find(([label])=>rest.startsWith(label)&&/^(?:\s*\d|$)/.test(rest.slice(label.length)));
  if(name){slug=name[1];rest=rest.slice(name[0].length).trim()}
  if(name&&!rest)return [{slug}];
  const match=rest.match(/^(\d+)(?:\s*[:.]\s*(\d+))?(?:\s*-\s*(\d+)(?:\s*[:.]\s*(\d+))?)?$/);
  if(!match||!slug)throw new Error('Try John 1:18, John 1:14–3:16, or NT.');
  const [,ch,v,end,endVerse]=match;
  const start={chapter:Number(ch),verse:v?Number(v):null};
  const finish=end ? (v&&!endVerse ? {chapter:Number(ch),verse:Number(end)}
   : {chapter:Number(end),verse:endVerse?Number(endVerse):null}) : start;
  return [{slug,start,finish}];
 });
}

function expandScriptureSelection(selections, index, books) {
 const names=new Map(books.map(book=>[book.slug,book.name]));
 const verses=new Map();
 for(const {slug,start,finish} of selections) {
  const chapters=index[slug];
  if(!chapters)throw new Error('Scripture chapter index unavailable.');
  const first=start?.chapter??1,last=finish?.chapter??chapters.length;
  if(first<1||last<first||last>chapters.length)throw new Error(`Check the chapter range in ${names.get(slug)}.`);
  for(let chapter=first;chapter<=last;chapter++){
   const entry=chapters[chapter-1];
   const numbers=Array.isArray(entry)?entry:Array.from({length:entry},(_,i)=>i+1);
   const from=chapter===first?(start?.verse??numbers[0]):numbers[0];
   const to=chapter===last?(finish?.verse??numbers.at(-1)):numbers.at(-1);
   if(!numbers.includes(from)||!numbers.includes(to)||to<from)
    throw new Error(`Check the verse range in ${names.get(slug)} ${chapter}.`);
   for(const verse of numbers)if(verse>=from&&verse<=to){
    const key=`${slug}/${chapter}/${verse}`;
    verses.set(key,{key,slug,chapter,verse,label:`${names.get(slug)} ${chapter}:${verse}`});
   }
  }
 }
 return [...verses.values()];
}


let scriptureIndexRequest;
function loadScriptureIndex(){
 if(!scriptureIndexRequest)scriptureIndexRequest=fetch('scripture-index.json').then(response=>{
  if(!response.ok)throw new Error('Scripture references could not be loaded.');
  return response.json();
 }).catch(error=>{scriptureIndexRequest=null;throw error});
 return scriptureIndexRequest;
}
