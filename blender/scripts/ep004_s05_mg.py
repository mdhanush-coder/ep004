# EP004 S05 "India's Silicon Bet" as one motion-graphics page (183.5625-259.8 s). Writes production/mg/s05/index.html (+ assets copied by the caller).
import os
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'production', 'mg', 's05'); os.makedirs(OUT, exist_ok=True)
B = 183.5625; DUR = round(259.8 - B, 3)
def R(t): return round(t - B, 3)
els = []; js = []; n = [0]
def fade(i, t0, t1, y=18):
    js.append(f"tl.fromTo('#{i}',{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:0.35,ease:'power3.out'}},{R(t0)});tl.to('#{i}',{{opacity:0,duration:0.25,ease:'power2.in'}},{R(t1) - 0.25});")
def blk(kick, text, t0, t1, cls='', style=''):
    n[0] += 1; i = f'b{n[0]}'
    els.append(f'<div class="blk {cls}" id="{i}" style="{style}">' + (f'<div class="kick">{kick}</div>' if kick else '') + f'<div class="txt">{text}</div></div>'); fade(i, t0, t1); return i
def bg(i, img, t0, t1, dim=0.55):
    els.append(f'<div class="bg" id="{i}" style="background-image:url(assets/{img});--dim:{dim}"></div>')
    js.append(f"tl.fromTo('#{i}',{{opacity:0,scale:1.0}},{{opacity:1,duration:0.6,ease:'power2.out'}},{R(t0)});tl.to('#{i}',{{scale:1.07,duration:{R(t1) - R(t0):.3f},ease:'none'}},{R(t0)});tl.to('#{i}',{{opacity:0,duration:0.4}},{R(t1) - 0.4});")
def card(i, img, t0, t1, tag, x, y, w=620, h=349):
    els.append(f'<div class="card" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div class="img" style="background-image:url(assets/{img})"></div><div class="ctag">{tag}</div></div>'); fade(i, t0, t1)
def mapshow(t0, t1):
    js.append(f"tl.fromTo('#mapl',{{opacity:0}},{{opacity:1,duration:0.6}},{R(t0)});tl.to('#mapl',{{opacity:0,duration:0.4}},{R(t1) - 0.4});")
def marker(i, t0, t1, color='saf'):
    js.append(f"tl.fromTo('#{i}',{{opacity:0,scale:0.2}},{{opacity:1,scale:1,duration:0.45,ease:'back.out(2)'}},{R(t0)});" + (f"tl.to('#{i}',{{opacity:0,duration:0.3}},{R(t1) - 0.3});" if t1 else ''))

# --- A: announcements -> facilities -> production
bg('bgcrane', 'crane.jpg', 183.56, 189.1, 0.45)
blk('INDIA’S SILICON BET', 'FROM ANNOUNCEMENTS TO FACILITIES', 183.98, 189.0, 'big', 'left:110px;top:430px')
# --- B..F map story
mapshow(189.1, 215.75); js.append(f"tl.to('#guj',{{fill:'#b8641d',stroke:'#ffb347',duration:0.9,ease:'power2.out'}},{R(189.1)});tl.to('#guj',{{fill:'#3a2a1b',stroke:'#7a5a3a',duration:0.6}},{R(196.4)});")
blk('MAJOR FOCUS', 'GUJARAT', 189.1, 191.25, 'big', 'left:110px;top:660px')
card('cardD', 'dholera.jpg', 191.29, 202.4, 'CONCEPTUAL VISUALISATION', 110, 90)
marker('mDholera', 195.35, 215.7, 'cy'); js.append(f"tl.fromTo('#mDholera .ring',{{attr:{{r:14}},opacity:1}},{{attr:{{r:40}},opacity:0,duration:1.2,repeat:6,ease:'power1.out'}},{R(195.35)});")
blk('TATA ELECTRONICS', 'DEVELOPING A FABRICATION FACILITY', 191.29, 196.3, 'mid', 'left:110px;top:520px')
blk('DHOLERA · FABRICATION · UNDER DEVELOPMENT', 'TARGET: MID-2028 (REPORTED)', 196.39, 202.4, 'chip', 'left:110px;top:520px')
blk('', 'NOT YET OPERATIONAL', 199.82, 202.4, 'sub', 'left:110px;top:690px')
marker('mSanand', 202.54, 231.7); js.append(f"tl.fromTo('#mSanand .ring',{{attr:{{r:14}},opacity:1}},{{attr:{{r:40}},opacity:0,duration:1.2,repeat:20,ease:'power1.out'}},{R(202.54)});")
blk('SANAND', 'MICRON', 203.9, 209.9, 'mid', 'left:110px;top:430px')
blk('', 'ASSEMBLY & TESTING', 206.15, 209.9, 'chip saf', 'left:110px;top:590px')
blk('', '<s>WAFER FABRICATION</s>', 208.0, 209.9, 'sub dim', 'left:110px;top:740px')
blk('SANAND', 'CG SEMI', 209.97, 215.7, 'mid', 'left:110px;top:430px')
blk('', 'JUL 2026 · COMMERCIAL PRODUCTION', 213.55, 215.7, 'chip saf', 'left:110px;top:590px')
# --- G: split screen
els.append('<div class="split" id="spl"><div class="half l" style="background-image:url(assets/layers.jpg)"></div><div class="half r" style="background-image:url(assets/probe.jpg)"></div><div class="divider"></div></div>')
js.append(f"tl.fromTo('#spl',{{opacity:0}},{{opacity:1,duration:0.5}},{R(215.75)});tl.to('#spl',{{opacity:0,duration:0.35}},{R(223.2) - 0.35});")
blk('FABRICATION', 'CREATES CIRCUITS ON WAFERS', 215.75, 223.2, 'mid', 'left:110px;top:800px;width:700px')
blk('ASSEMBLY & TESTING', 'FINISHED, VERIFIED PRODUCTS', 219.26, 223.2, 'mid saf', 'left:1010px;top:800px;width:800px')
# --- H: twelve units
blk('SEMICON INDIA 1.0 · FIRST PHASE', '12 APPROVED UNITS', 223.32, 226.9, 'huge', 'left:110px;top:300px')
blk('', '3 FABS', 225.75, 226.9, 'chip', 'left:110px;top:760px')
blk('', '9 ASSEMBLY & TESTING UNITS', 225.75, 226.9, 'chip saf', 'left:110px;top:880px')
# --- I,J: map again
mapshow(226.95, 235.8)
marker('mMicron', 226.95, 235.7); marker('mKaynes', 227.65, 235.7); marker('mCG', 228.75, 235.7)
for _i, _t in (('mMicron', 226.95), ('mKaynes', 227.65), ('mCG', 228.75)):
    js.append(f"tl.fromTo('#ld_{_i}',{{strokeOpacity:0}},{{strokeOpacity:0.75,duration:0.4}},{R(_t)});tl.to('#ld_{_i}',{{strokeOpacity:0,duration:0.3}},{R(235.4)});")
blk('', 'MICRON', 226.95, 231.7, 'mid saf', 'left:110px;top:380px'); blk('', 'KAYNES', 227.65, 231.7, 'mid saf', 'left:110px;top:500px'); blk('', 'CG SEMI', 228.75, 231.7, 'mid saf', 'left:110px;top:620px')
blk('', 'LED THE WAY INTO COMMERCIAL PRODUCTION', 230.0, 231.7, 'sub', 'left:110px;top:760px')
marker('mMohali', 232.09, 235.7); marker('mSurat', 233.09, 235.7)
blk('SEPTEMBER 2026', '5 IN COMMERCIAL PRODUCTION', 234.25, 235.8, 'huge', 'left:110px;top:330px')
blk('', 'ALL ASSEMBLY & TESTING (ATMP/OSAT)', 234.64, 235.8, 'sub saf', 'left:110px;top:800px')
# --- K: investment
bg('bgatmp', 'atmp.jpg', 235.88, 241.7, 0.6)
blk('CUMULATIVE PROPOSED INVESTMENT', '₹1.64 LAKH CRORE+', 236.6, 241.7, 'huge', 'left:110px;top:440px')
# --- L: Semicon 2.0
bg('bgring', 'hero_ring.jpg', 241.74, 253.3, 0.7)
blk('APPROVED JULY 2026', 'SEMICON 2.0', 242.59, 253.3, 'huge', 'left:110px;top:330px')
blk('PROPOSED OUTLAY', '₹1,27,500 CRORE', 247.55, 253.3, 'huge saf', 'left:110px;top:620px')
# --- M: ecosystem
bg('bgring2', 'hero_ring.jpg', 253.3, 259.8, 0.5)
blk('', 'BIGGER THAN ONE FACTORY', 253.72, 256.9, 'big', 'left:110px;top:470px')
blk('', 'BUILD THE ECOSYSTEM BEHIND THE CHIP', 256.95, 259.8, 'big', 'left:110px;top:470px')

css = '''body{margin:0;background:#000}#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:radial-gradient(ellipse at 70% 40%,#0c1a26,#05080c 70%);font-family:"Studio Grotesk","Inter",sans-serif;color:#fff}
.bg{position:absolute;inset:0;background-size:cover;background-position:center;opacity:0}.bg:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(4,7,11,.92),rgba(4,7,11,.35) 70%,rgba(4,7,11,.1));opacity:1}
.blk{position:absolute;opacity:0;max-width:800px}.huge{max-width:860px}.kick{font-size:22px;letter-spacing:.3em;color:#4fd8ff;font-weight:600;margin-bottom:12px}.saf .kick,.saf.chip,.saf .txt{color:#ffb347}
.txt{font-weight:700;letter-spacing:.06em;line-height:1.08;text-transform:uppercase}.big .txt{font-size:76px}.mid .txt{font-size:58px}.huge .txt{font-size:104px}.sub .txt{font-size:34px;letter-spacing:.16em;color:#cfe3ee}
.chip .txt{display:inline-block;font-size:42px;padding:14px 26px;border-left:6px solid #4fd8ff;background:rgba(8,14,20,.8)}.chip.saf .txt{border-left-color:#ffb347}.dim .txt{color:#7f97a6}
.card{position:absolute;opacity:0;border:2px solid #1f3a4c;border-radius:6px;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,.6)}.card .img{position:absolute;inset:0;background-size:cover;background-position:center}.card .ctag{position:absolute;left:0;bottom:0;padding:8px 16px;font-size:18px;letter-spacing:.2em;background:rgba(8,12,18,.85);color:#ffb347;font-weight:600}
#mapl{position:absolute;inset:0;opacity:0}.state{fill:#10202c;stroke:#2c566f;stroke-width:1.1}.pin circle{transform-box:fill-box;transform-origin:50% 50%}.pin{opacity:0;transform-box:fill-box;transform-origin:50% 50%}
.lead{stroke:#ffb347;stroke-width:2;stroke-opacity:.0}.pin.gj circle{display:none}.pin.gj{opacity:0}.pin.gj .halo{display:inline;fill:#ff9a3c;fill-opacity:.28}.pin .dot{fill:#ffb347}.pin.cy .dot{fill:#4fd8ff}.pin .ring{fill:none;stroke:#ffb347;stroke-width:3}.pin.cy .ring{stroke:#4fd8ff}
.split{position:absolute;inset:0;opacity:0}.half{position:absolute;top:0;bottom:0;width:50%;background-size:cover;background-position:center}.half.l{left:0}.half.r{right:0}.divider{position:absolute;left:959px;top:0;bottom:0;width:2px;background:#4fd8ff}
.split:after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(4,7,11,.85),rgba(4,7,11,0) 45%)}'''
pins = ''.join(f'<g id="pos_{i}"><g class="pin {c}" id="{i}"><circle class="halo" r="70" style="display:none"/><circle class="ring" r="14"/><circle class="dot" r="9"/></g></g>' for i, c in (('mDholera', 'cy'), ('mSanand', ''), ('mMicron', ''), ('mKaynes', ''), ('mCG', ''), ('mMohali', ''), ('mSurat', '')))
leads = ''.join(f'<line id="ld_{i}" class="lead"/>' for i in ('mMicron', 'mKaynes', 'mCG'))
script = '''window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady['map'] = (async () => {
  const topo = await (await fetch('hf-assets/maps/india-detailed.json')).json(); const key = Object.keys(topo.objects)[0];
  const fc = topojson.feature(topo, topo.objects.states); const ctry = topojson.feature(topo, topo.objects.country); const proj = d3.geoMercator().fitExtent([[900, 70], [1820, 1010]], ctry); const path = d3.geoPath(proj);
  const g = document.getElementById('states');
  fc.features.forEach(f => { const p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', path(f)); p.setAttribute('class', 'state');
    if (f.id === 'gujarat' || (f.properties && f.properties.id === 'gujarat')) { document.getElementById('guj').setAttribute('d', path(f)); return; } g.appendChild(p); });
  const put = (id, lon, lat, dx = 0, dy = 0) => { const [x, y] = proj([lon, lat]); document.getElementById('pos_' + id).setAttribute('transform', `translate(${x + dx},${y + dy})`); };
  put('mDholera', 72.02, 22.25); put('mSanand', 72.38, 22.99); put('mMicron', 72.38, 22.99, -46, -30); put('mKaynes', 72.38, 22.99, 0, -52); put('mCG', 72.38, 22.99, 46, -30);
  const lead = (id, dx, dy) => { const [x, y] = proj([72.38, 22.99]); const l = document.getElementById('ld_' + id); l.setAttribute('x1', x); l.setAttribute('y1', y); l.setAttribute('x2', x + dx); l.setAttribute('y2', y + dy); };
  lead('mMicron', -46, -30); lead('mKaynes', 0, -52); lead('mCG', 46, -30);
  put('mMohali', 76.72, 30.70); put('mSurat', 72.83, 21.17);
})();'''
html = f'''<!doctype html><html><head><meta charset="utf-8"><script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><style>{css}</style></head><body>
<div id="root" data-composition-id="s05" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080" data-fps="24">
<svg id="mapl" width="1920" height="1080" viewBox="0 0 1920 1080"><g id="states"></g><path id="guj" class="state"/>{leads}{pins}</svg>
{chr(10).join(els)}
</div><script>{script}
const tl = gsap.timeline({{paused: true}});
{chr(10).join(js)}
window.__timelines = {{s05: tl}};</script></body></html>'''
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(html); print('ok', DUR)
