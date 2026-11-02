"""Write review/narration_review.html: a local playback page for approving the narration.
Embeds the master word timings; plays the WAVs straight from assets/ (nothing uploaded).
Run from the EP004 folder: python -X utf8 edit/build_review.py
"""
import json

words = json.load(open('edit/captions/ep004_words_master.json', encoding='utf8'))

SCENES = [  # from production/timing-map.md
    (1, 'The Invisible Brain', 0.00, 36.24), (2, 'From Quartz to a Chip', 36.24, 74.75),
    (3, 'The Precision Problem', 74.75, 134.71), (4, 'Why India Needs the Capability', 134.71, 183.29),
    (5, "India's Silicon Bet", 183.29, 259.77), (6, 'The Future Is Built Layer by Layer', 259.77, 300.00),
]
SPLICE = (196.16, 202.19)
HOLDS = [(29.73, 0.6), (67.64, 0.5), (105.44, 1.0), (156.04, 0.6)]
CHECKS = [  # (time, what to listen for)
    (1.37, 'Opening line: energy and pace. "U-P-I" said as letters?'),
    (11.38, '"A car engine starts": clean this time?'),
    (29.73, 'Freeze beat 0.6 s before "So why…": intentional, not a gap?'),
    (57.90, '"transistors: tiny electrical switches": emphasis lands?'),
    (88.59, '"Light transfers a carefully designed pattern": "transfers" clear?'),
    (105.44, 'Particle hold 1.0 s, then [tense, low voice]: tension shift audible?'),
    (137.77, 'The S04 list (cars, medical equipment…): rhythm, not robotic?'),
    (164.26, '"capabilities. The challenge…": the sentence break is audible?'),
    (191.29, '"Dholera" pronunciation'),
    (SPLICE[0], 'SPLICE (3:16.2–3:22.2): seamless? Tone, room and level match on both sides?'),
    (202.54, '"…to begin. At Sanand, Micron\'s…": the 0.7 s pause after "Sanand" sounds natural?'),
    (226.95, '"Kaynes" pronunciation'),
    (235.88, '"one point six four lakh crore rupees": clear?'),
    (241.74, '"Semicon two point oh": clear?'),
    (247.37, '"one lakh, twenty-seven thousand, five hundred crore": clear?'),
    (281.49, '"Raw material. Wafer. Microscopic circuits. Finished chip.": punchy rhythm?'),
    (295.08, 'Final question: lands with weight, not flat?'),
    (0.0, 'OVERALL: voice quality and naturalness across all 5 minutes'),
    (0.0, 'OVERALL: tension builds S03→S05; calm without being slow'),
]

page = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EP004 Narration Review</title>
<style>
:root{--bg:#f6f6f4;--panel:#fff;--ink:#1c1c1c;--mute:#666;--line:#ddd;--acc:#0a7d8c;--warn:#c25e00;--ok:#2e7d32;--bad:#c62828;--hl:#ffe9a8}
@media (prefers-color-scheme:dark){:root{--bg:#121315;--panel:#1b1d20;--ink:#e8e8e6;--mute:#9a9a9a;--line:#2e3135;--acc:#4fc3d1;--warn:#ffa24c;--ok:#66bb6a;--bad:#ef5350;--hl:#5a4a12}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}
main{max-width:1000px;margin:0 auto;padding:16px}h1{font-size:20px;margin:4px 0}h2{font-size:15px;margin:20px 0 8px;color:var(--mute);text-transform:uppercase;letter-spacing:.05em}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px}
audio{width:100%}.sub{color:var(--mute);font-size:13px}
#bar{position:relative;height:42px;margin-top:10px;cursor:pointer;border-radius:4px;overflow:hidden;background:var(--line)}
.seg{position:absolute;top:0;bottom:0;border-right:1px solid var(--bg);font-size:11px;padding:2px 4px;color:var(--ink);overflow:hidden;white-space:nowrap}
.seg:nth-child(odd){background:color-mix(in srgb,var(--acc) 22%,transparent)}.seg:nth-child(even){background:color-mix(in srgb,var(--acc) 12%,transparent)}
.mark{position:absolute;bottom:0;height:14px;background:var(--warn)}.splice{position:absolute;top:0;bottom:0;background:color-mix(in srgb,var(--bad) 35%,transparent);border:1px dashed var(--bad)}
#head{position:absolute;top:0;bottom:0;width:2px;background:var(--ink)}
#transcript{max-height:340px;overflow:auto;line-height:1.9}.w{cursor:pointer;border-radius:3px;padding:0 1px}.w.on{background:var(--hl)}.w.sp{text-decoration:underline wavy var(--bad)}
.sc{display:block;margin-top:8px;font-weight:600;color:var(--acc)}
table{width:100%;border-collapse:collapse}td{border-top:1px solid var(--line);padding:6px 4px;vertical-align:top}
button{font:inherit;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:6px;padding:3px 8px;cursor:pointer}
button.ok.sel{background:var(--ok);color:#fff}button.fix.sel{background:var(--bad);color:#fff}
input[type=text]{width:100%;font:inherit;padding:3px 6px;border:1px solid var(--line);border-radius:4px;background:var(--bg);color:var(--ink)}
.row{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}textarea{width:100%;height:120px;font:13px monospace;background:var(--bg);color:var(--ink);border:1px solid var(--line)}
</style></head><body><main>
<h1>EP004 — Narration review (sameer)</h1>
<div class="sub">Master 5:00.00 · narration 290.98 s · picture-only holds 9.02 s. Click the bar or any word to jump. Red dashed area = S05 splice. Orange ticks = picture-only holds.</div>
<div class="panel" style="margin-top:12px">
<audio id="a" controls preload="auto" src="../assets/audio/narration/ep004_narration_master.wav"></audio>
<div id="bar"><div id="head"></div></div>
<div class="row" id="scenebtns"></div>
<div class="row"><button id="splice">▶ Play splice with 3 s around it</button><label class="sub"><input type="checkbox" id="loop"> loop scene</label></div>
</div>
<h2>Live transcript</h2><div class="panel" id="transcript"></div>
<h2>Listening checklist</h2><div class="panel"><table id="checks"></table>
<div class="row"><button id="copy">Copy review notes</button><span class="sub" id="copied"></span></div>
<textarea id="out" readonly placeholder="Review notes appear here; paste them back into the chat."></textarea></div>
<h2>Individual scene files</h2><div class="panel" id="files"></div>
</main><script>
const W=__WORDS__,S=__SCENES__,SP=__SPLICE__,H=__HOLDS__,C=__CHECKS__,T=300;
const a=document.getElementById('a'),bar=document.getElementById('bar'),head=document.getElementById('head');
const fmt=t=>{const m=Math.floor(t/60),s=(t%60).toFixed(2).padStart(5,'0');return m+':'+s};
const go=t=>{a.currentTime=Math.max(0,t);a.play()};
const pct=t=>(t/T*100)+'%';
S.forEach(([n,ti,s,e])=>{const d=document.createElement('div');d.className='seg';d.style.left=pct(s);d.style.width=pct(e-s);d.textContent='S0'+n;d.title=ti;bar.prepend(d);
 const b=document.createElement('button');b.textContent='S0'+n+' '+fmt(s);b.onclick=()=>go(s);document.getElementById('scenebtns').append(b)});
H.forEach(([t,d])=>{const m=document.createElement('div');m.className='mark';m.style.left=pct(t);m.style.width=pct(d);m.title='hold '+d+' s';bar.append(m)});
const sp=document.createElement('div');sp.className='splice';sp.style.left=pct(SP[0]);sp.style.width=pct(SP[1]-SP[0]);sp.title='S05 splice';bar.append(sp);
bar.onclick=e=>{const r=bar.getBoundingClientRect();go((e.clientX-r.left)/r.width*T)};
const tr=document.getElementById('transcript');let last=0;const spans=[];
W.forEach((w,i)=>{if(w.scene!==last){const h=document.createElement('span');h.className='sc';h.textContent='S0'+w.scene+' — '+S[w.scene-1][1];tr.append(h);last=w.scene}
 const s=document.createElement('span');s.className='w'+(w.start>=SP[0]&&w.end<=SP[1]?' sp':'');s.textContent=w.word;s.title=fmt(w.start);s.onclick=()=>go(w.start);tr.append(s,' ');spans.push(s)});
let cur=-1;a.ontimeupdate=()=>{const t=a.currentTime;head.style.left=pct(t);
 if(document.getElementById('loop').checked){const sc=S.find(x=>t>=x[2]&&t<x[3]);if(sc&&t>sc[3]-0.05)a.currentTime=sc[2]}
 let i=W.findIndex(w=>t>=w.start&&t<=w.end+0.08);if(i!==cur){if(cur>=0)spans[cur].classList.remove('on');if(i>=0){spans[i].classList.add('on');spans[i].scrollIntoView({block:'nearest'})}cur=i}};
let stopAt=null;a.addEventListener('timeupdate',()=>{if(stopAt&&a.currentTime>=stopAt){a.pause();stopAt=null}});
document.getElementById('splice').onclick=()=>{stopAt=SP[1]+3;go(SP[0]-3)};
const key='ep004-narration-review';let st={};try{st=JSON.parse(localStorage.getItem(key))||{}}catch(e){}
const save=()=>{try{localStorage.setItem(key,JSON.stringify(st))}catch(e){}};
const tb=document.getElementById('checks');
C.forEach(([t,q],i)=>{const r=tb.insertRow();const c0=r.insertCell();if(t>0){const b=document.createElement('button');b.textContent='▶ '+fmt(t);b.onclick=()=>go(t-1);c0.append(b)}else c0.textContent='—';
 const c1=r.insertCell();c1.innerHTML='<div>'+q+'</div>';const inp=document.createElement('input');inp.type='text';inp.placeholder='note (optional)';inp.value=(st[i]||{}).note||'';inp.oninput=()=>{st[i]={...st[i],note:inp.value};save()};c1.append(inp);
 const c2=r.insertCell();c2.style.whiteSpace='nowrap';['ok','fix'].forEach(k=>{const b=document.createElement('button');b.className=k+((st[i]||{}).v===k?' sel':'');b.textContent=k==='ok'?'OK':'Fix';
  b.onclick=()=>{st[i]={...st[i],v:k};save();c2.querySelectorAll('button').forEach(x=>x.classList.toggle('sel',x===b))};c2.append(b)})});
document.getElementById('copy').onclick=()=>{const out=C.map(([t,q],i)=>{const s=st[i]||{};return `[${s.v?s.v.toUpperCase():'—'}] ${t>0?fmt(t)+' ':''}${q}${s.note?' :: '+s.note:''}`}).join('\n');
 const ta=document.getElementById('out');ta.value=out;ta.select();try{navigator.clipboard.writeText(out);document.getElementById('copied').textContent='Copied.'}catch(e){}};
const f=document.getElementById('files');S.forEach(([n,ti])=>{const d=document.createElement('div');d.innerHTML=`<div class="sub">S0${n} ${ti}</div><audio controls preload="none" src="../assets/audio/narration/ep004_s0${n}_sameer.wav"></audio>`;f.append(d)});
</script></body></html>'''

for k, v in {'__WORDS__': words, '__SCENES__': SCENES, '__SPLICE__': SPLICE, '__HOLDS__': HOLDS, '__CHECKS__': CHECKS}.items():
    page = page.replace(k, json.dumps(v, ensure_ascii=False))
open('review/narration_review.html', 'w', encoding='utf8').write(page)
print('wrote review/narration_review.html', len(page), 'bytes')
