// Editorial annotations keyed to the pinned SBLGNT verse numbering.
const textualVariants = [
 {
  book:'matthew', ranges:[[21,44,44]], title:'Matthew 21:44 · The stone that crushes',
  explanation:'Most Greek manuscripts include this saying, but Codex Bezae (D), manuscript 33, and some Old Latin and Syriac witnesses omit it. The parallel in Luke 20:18 has led some scholars to suspect it was copied into Matthew. SBLGNT retains the verse in its running text. Nestle–Aland 28 brackets it.',
  sources:[['NET textual note and SBLGNT','https://www.biblegateway.com/passage/?search=Matthew+21&version=NET%3BSBLGNT']]
 },
 {
  book:'mark', ranges:[[16,8,8]], title:'After Mark 16:8 · Shorter ending',
  explanation:'Sinaiticus and Vaticanus end at verse 8. Old Latin Codex Bobiensis (k) has the shorter ending alone, and several later Greek witnesses give it before the longer ending. SBLGNT prints the shorter ending in double brackets as an unnumbered alternative after verse 8. The dagger marks that location in DGTBible, where the shorter ending is discussed in the editorial note.',
  sources:[['NABRE textual note and SBLGNT','https://www.biblegateway.com/passage/?search=Mark+16&version=NABRE%3BSBLGNT']]
 },
 {
  book:'mark', ranges:[[16,9,20]], title:'Mark 16:9–20 · Longer ending',
  explanation:'Sinaiticus and Vaticanus end at verse 8. The longer ending is in most surviving Greek manuscripts, including Alexandrinus, and Irenaeus cites verse 19 around AD 180. Some witnesses give both endings. SBLGNT prints verses 9–20 in double brackets as an alternative ending.',
  sources:[['NABRE textual note and SBLGNT','https://www.biblegateway.com/passage/?search=Mark+16&version=NABRE%3BSBLGNT']]
 },
 {
  book:'luke', ranges:[[22,43,44]], title:'Luke 22:43–44 · The angel and the agony',
  explanation:'Papyrus 75 and Codices Alexandrinus and Vaticanus omit these verses. The original hand of Sinaiticus, Codex Bezae, and the early fragment 0171 attest them. The evidence for both readings is early, and scholars differ over how the variation arose. SBLGNT keeps both verses in the running text.',
  sources:[['NET textual note','https://www.biblegateway.com/passage/?search=Luke+22%3A43-45&version=NET'],['SBLGNT','https://www.biblegateway.com/passage/?search=Luke+22%3A43-45&version=SBLGNT']]
 },
 {
  book:'luke', ranges:[[23,34,34]], title:'Luke 23:34a · The prayer for forgiveness',
  explanation:'The dispute concerns Jesus’ opening prayer. Papyrus 75, Vaticanus, and the original hand of Bezae omit it. The original hand of Sinaiticus, Alexandrinus, and many later manuscripts include it. SBLGNT retains the prayer in the running text. Nestle–Aland 28 double-brackets it. The remainder of verse 34 is outside this variant.',
  sources:[['NET textual note and SBLGNT','https://www.biblegateway.com/passage/?search=Luke+23&version=NET%3BSBLGNT']]
 },
 {
  book:'john', ranges:[[7,53,53],[8,1,11]], title:'John 7:53–8:11 · The woman accused of adultery',
  explanation:'Papyri 66 and 75, Sinaiticus, and Vaticanus omit this story. Codex Bezae and many later Greek manuscripts include it. Some copies place it after John 21:25 or Luke 21:38, among other locations. The early omissions and shifting position weigh against its belonging here in the earliest recoverable text of John. SBLGNT preserves it here in double brackets.',
  sources:[['NET textual note and SBLGNT','https://www.biblegateway.com/passage/?search=John+7%3A53-8%3A11&version=NET%3BSBLGNT']]
 },
 {
  book:'romans', ranges:[[16,24,24]], title:'Romans 16:24 · The grace benediction',
  explanation:'Bezae and most later Greek manuscripts have this benediction after verse 23. Some witnesses place it after verse 27. Papyri 46 and 61, Sinaiticus, Alexandrinus, and Vaticanus lack it. The wording echoes the blessing in verse 20. SBLGNT retains verse 24 in its running text. Nestle–Aland 28 omits it.',
  sources:[['NET textual note and SBLGNT','https://www.biblegateway.com/passage/?search=Romans+16&version=NET%3BSBLGNT']]
 }
];

function textualVariantMarker(book, chapter, verse) {
 const index = textualVariants.findIndex(note => note.book === book &&
  note.ranges.some(([ch, first, last]) => chapter === ch && verse >= first && verse <= last));
 if (index < 0) return '';
 return `<button type="button" class="variant-marker" data-variant="${index}" aria-label="Textual note for ${esc(textualVariants[index].title)}" aria-controls="variant-note" aria-expanded="false">†</button>`;
}

function initTextualVariantNotes() {
 const panel = document.getElementById('variant-note');
 const title = document.getElementById('variant-title');
 const body = document.getElementById('variant-explanation');
 const sources = document.getElementById('variant-sources');
 let anchor, pinned, dismissTimer;

 function close(restoreFocus = false) {
  clearTimeout(dismissTimer);
  if (!anchor) return;
  const previous = anchor;
  anchor = null;
  panel.hidden = true;
  previous.setAttribute('aria-expanded', 'false');
  if (restoreFocus && previous.isConnected) previous.focus({preventScroll:true});
 }

 function open(button, pin) {
  close();
  anchor = button;
  pinned = pin;
  const note = textualVariants[button.dataset.variant];
  title.textContent = note.title;
  body.textContent = note.explanation;
  sources.replaceChildren(...note.sources.map(([label, url]) => {
   const link = document.createElement('a');
   link.textContent = label;
   link.href = url;
   link.target = '_blank';
   link.rel = 'noopener noreferrer';
   return link;
  }));
  panel.hidden = false;
  button.setAttribute('aria-expanded', 'true');
  const rect = button.getBoundingClientRect();
  const x = Math.min(rect.left, document.documentElement.clientWidth - panel.offsetWidth - 8);
  const below = rect.bottom + 4;
  panel.style.left = `${Math.max(8, x)}px`;
  const above = rect.top - panel.offsetHeight - 4;
  panel.style.top = `${below + panel.offsetHeight <= innerHeight - 8 ? below : Math.max(8, above)}px`;
 }

 document.addEventListener('pointerover', event => {
  const button = event.target.closest?.('.variant-marker');
  if (event.pointerType !== 'mouse' || pinned && anchor) return;
  if (button && button !== anchor) open(button, false);
  if (button || panel.contains(event.target)) clearTimeout(dismissTimer);
 });
 document.addEventListener('pointerout', event => {
  if (event.pointerType !== 'mouse' || pinned || !anchor) return;
  if (anchor.contains(event.target) || panel.contains(event.target)) {
   clearTimeout(dismissTimer);
   dismissTimer = setTimeout(() => close(), 180);
  }
 });
 document.addEventListener('click', event => {
  const button = event.target.closest?.('.variant-marker');
  if (button) {
   if (anchor === button && pinned) close();
   else {
    open(button, true);
    if (event.detail === 0) panel.focus({preventScroll:true});
   }
  } else if (!panel.contains(event.target)) close();
 });
 document.getElementById('variant-close').onclick = () => close(true);
 document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && anchor) close(panel.contains(document.activeElement));
 });
 window.addEventListener('scroll', () => close(), {passive:true});
 window.addEventListener('resize', () => close());
 return close;
}
