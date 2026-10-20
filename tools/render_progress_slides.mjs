/** Render the requested Markdown slides to portable HTML and a printable PDF.
 * Requires marked and playwright. Reuses the bundled runtime when available.
 * Run: node tools/render_progress_slides.mjs
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.join(root, 'presentations');
const stem = 'Anamorphic_Fluid_Room_Progress';
const source = path.join(out, stem + '.slides.md');
const runtimeModules = process.env.CODEX_RUNTIME_NODE_MODULES || path.join(process.env.USERPROFILE || '', '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const bundled = createRequire(path.join(runtimeModules, '__slides_resolver.cjs'));
async function dependency(name) {
  try { return await import(name); }
  catch { return await import(pathToFileURL(bundled.resolve(name)).href); }
}
const { marked } = await dependency('marked');
const playwrightModule = await dependency('playwright');
const { chromium } = playwrightModule.default || playwrightModule;
const md = (await fs.readFile(source, 'utf8')).replace(/\r\n/g, '\n');
const front = md.match(/^---\n([\s\S]*?)\n---\n/);
if (!front) throw new Error('Expected Markdown frontmatter');
const style = front[1].split('style: |\n')[1].split('\n').map(line => line.replace(/^  /, '')).join('\n');
const parts = md.slice(front[0].length).trim().split(/\n---\n/);
const imagePaths = new Set();
const esc = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
async function inlineImages(html) {
  for (const match of [...html.matchAll(/<img\b[^>]*\bsrc="([^\"]+)"[^>]*>/g)]) {
    const src = match[1];
    if (/^(https?:|data:)/.test(src)) continue;
    const full = path.resolve(path.dirname(source), src);
    if (!full.startsWith(root + path.sep)) throw new Error('Image outside project: ' + src);
    const data = await fs.readFile(full);
    imagePaths.add(full);
    const mime = path.extname(full).toLowerCase() === '.png' ? 'image/png' : 'image/jpeg';
    html = html.replace(match[0], match[0].replace(src, `data:${mime};base64,${data.toString('base64')}`));
  }
  return html;
}
const slides = [];
const notes = [];
for (let i = 0; i < parts.length; i++) {
  const part = parts[i];
  const cls = part.match(/<!--\s*_class:\s*([^>]*?)\s*-->/)?.[1] || '';
  const speaker = part.match(/<!--\s*Speaker notes:\s*([\s\S]*?)-->/)?.[1]?.trim() || '';
  notes.push(speaker);
  const clean = part.replace(/<!--[\s\S]*?-->/g, '').trim();
  const title = clean.match(/^#{1,2}\s+(.+)$/m)?.[1]?.replace(/<[^>]+>/g, ' ') || `Slide ${i+1}`;
  const html = await inlineImages(marked.parse(clean));
  slides.push(`<section class="slide ${esc(cls)}" id="slide-${i+1}" aria-label="${esc(title)}" tabindex="-1">${html}<span class="page-number">${i+1} / ${parts.length}</span></section>`);
}
const viewerStyle = `
html,body{margin:0;width:100%;height:100%;background:#000;color:#f3f4f5;overflow:hidden}
#stage{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
#deck{width:1280px;height:720px;flex:none;transform-origin:center center}
.slide{display:none}.slide.active{display:flex}.page-number{position:absolute;right:27px;bottom:17px;color:#798b94;font:16px 'Segoe UI',sans-serif}
#controls{position:fixed;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:5px;opacity:.18;transition:opacity .2s;z-index:5}
#controls:hover,#controls:focus-within{opacity:1}button{border:1px solid #354149;background:#10171c;color:#e9eeee;padding:7px 12px;font:14px 'Segoe UI',sans-serif;cursor:pointer;border-radius:3px}button:focus-visible{outline:2px solid #83e6df}
#notes{position:fixed;right:16px;top:16px;bottom:62px;width:min(470px,80vw);box-sizing:border-box;background:#11191f;border:1px solid #3e505b;color:#e2ebef;padding:26px;overflow:auto;z-index:8;font:17px/1.5 'Segoe UI',sans-serif;white-space:pre-wrap}#notes[hidden]{display:none}
@page{size:1280px 720px;margin:0}
@media print{html,body{width:1280px;height:auto;overflow:visible;-webkit-print-color-adjust:exact;print-color-adjust:exact}#stage{position:static;display:block}#deck{height:auto;transform:none!important}.slide{display:flex!important;break-after:page;page-break-after:always;break-inside:avoid}.slide:last-child{break-after:auto;page-break-after:auto}#controls,#notes{display:none!important}}
`;
const doc = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="dark"><title>Anamorphic Fluid Room | Progress review</title><style>${style}\n${viewerStyle}</style></head><body><main id="stage"><div id="deck">${slides.join('\n')}</div></main><nav id="controls" aria-label="Slide navigation"><button id="prev" aria-label="Previous slide">Previous</button><button id="next" aria-label="Next slide">Next</button><button id="full" aria-label="Fullscreen">Fullscreen</button><button id="notesButton" aria-label="Toggle speaker notes">Notes</button><button id="print" aria-label="Print slides">Print</button></nav><aside id="notes" hidden></aside><script>
const notes=${JSON.stringify(notes).replaceAll('<','\\u003c')};
const slides=[...document.querySelectorAll('.slide')]; let current=0;
function resize(){document.querySelector('#deck').style.transform='scale('+Math.min(innerWidth/1280,innerHeight/720)+')'}
function show(n){current=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>{s.classList.toggle('active',i===current);s.setAttribute('aria-hidden',String(i!==current))});document.querySelector('#notes').textContent=notes[current];history.replaceState(null,'','#'+(current+1));document.title=(current+1)+' / '+slides.length+' · Anamorphic Fluid Room'}
function toggleNotes(){const n=document.querySelector('#notes');n.hidden=!n.hidden}
document.querySelector('#prev').onclick=()=>show(current-1);document.querySelector('#next').onclick=()=>show(current+1);
document.querySelector('#full').onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();document.querySelector('#notesButton').onclick=toggleNotes;document.querySelector('#print').onclick=()=>window.print();
addEventListener('keydown',e=>{if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(current-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key.toLowerCase()==='n')toggleNotes();if(e.key.toLowerCase()==='f')document.querySelector('#full').click()});
let touchX=0;addEventListener('touchstart',e=>touchX=e.changedTouches[0].screenX,{passive:true});addEventListener('touchend',e=>{let dx=e.changedTouches[0].screenX-touchX;if(Math.abs(dx)>60)show(current+(dx<0?1:-1))},{passive:true});
addEventListener('resize',resize);resize();show((parseInt(location.hash.slice(1),10)||1)-1);
</script></body></html>`;
const htmlPath=path.join(out,stem+'.html');
await fs.writeFile(htmlPath,doc);
const qa=path.join(root,'output','playwright','progress-slides');
await fs.mkdir(qa,{recursive:true});
const browser=await chromium.launch({headless:true,channel:process.env.SLIDES_BROWSER||'chrome'});
try{
  const page=await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(htmlPath).href,{waitUntil:'load'});
  await page.evaluate(()=>document.fonts.ready);
  await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
  const checks=[];
  for(let i=0;i<slides.length;i++){
    await page.evaluate(n=>show(n),i);
    const result=await page.evaluate(()=>{
      const s=document.querySelector('.slide.active'),r=s.getBoundingClientRect();
      const out=[];
      for(const e of s.querySelectorAll('h1,h2,h3,p,li,table,figure,.big,.bar-track')){
        if(e.classList.contains('image-label'))continue;
        const b=e.getBoundingClientRect();
        if(b.bottom>r.bottom-15||b.top<r.top-1||b.right>r.right+1||b.left<r.left-1)out.push({tag:e.tagName,text:e.textContent.slice(0,70),bounds:{x:b.x,y:b.y,w:b.width,h:b.height}});
      }
      return {slide:s.id,background:getComputedStyle(s).backgroundColor,brokenImages:[...s.querySelectorAll('img')].filter(i=>!i.naturalWidth).length,overflow:out};
    });
    checks.push(result);
    await page.locator('.slide.active').screenshot({path:path.join(qa,`slide-${String(i+1).padStart(2,'0')}.png`)});
  }
  await page.evaluate(()=>show(0));await page.keyboard.press('ArrowRight');
  const navigation=await page.locator('.slide.active').getAttribute('id')==='slide-2';
  await page.keyboard.press('n');const notesVisible=await page.locator('#notes').isVisible();await page.keyboard.press('n');
  await page.pdf({path:path.join(out,stem+'.pdf'),preferCSSPageSize:true,printBackground:true,displayHeaderFooter:false});
  const report={slideCount:slides.length,imageCount:imagePaths.size,checks,errors,navigation,notesVisible};
  await fs.writeFile(path.join(qa,'validation.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  if(errors.length||checks.some(c=>c.overflow.length||c.brokenImages||c.background!=='rgb(0, 0, 0)')||!navigation||!notesVisible)process.exitCode=1;
}finally{await browser.close()}
