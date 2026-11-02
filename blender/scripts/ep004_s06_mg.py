# EP004 S06 "The Future Is Built Layer by Layer" + end card as one motion-graphics page (259.8-300.0 s).
# Media (clips) come from the bucket via `media`; stills are in production/mg/s06/assets.
import os, random
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'production', 'mg', 's06'); os.makedirs(OUT, exist_ok=True)
B = 259.8; DUR = round(300.0 - B, 3)
def R(t): return round(t - B, 3)
els = []; js = []; n = [0]
def show(i, t0, t1, fade=0.0):
    js.append(f"tl.set('#{i}',{{opacity:1}},{R(t0)});" if fade == 0 else f"tl.fromTo('#{i}',{{opacity:0}},{{opacity:1,duration:{fade}}},{R(t0)});")
    js.append(f"tl.set('#{i}',{{opacity:0}},{R(t1)});")
def still(i, img, t0, t1, z0=1.0, z1=1.08, dim=0.35, fade=0.0):
    els.append(f'<div class="bg" id="{i}" style="background-image:url(assets/{img});--dim:{dim}"></div>')
    show(i, t0, t1, fade); js.append(f"tl.fromTo('#{i}',{{scale:{z0}}},{{scale:{z1},duration:{R(t1) - R(t0):.3f},ease:'none'}},{R(t0)});")
def clip(i, name, t0, t1):
    els.append(f'<video class="clip" id="{i}" src="assets/{name}" data-start="{R(t0)}" data-duration="{R(t1) - R(t0):.3f}" muted playsinline></video>'); show(i, t0, t1)
def blk(kick, text, t0, t1, cls='tag'):
    n[0] += 1; i = f'b{n[0]}'
    els.append(f'<div class="blk {cls}" id="{i}">' + (f'<div class="kick">{kick}</div>' if kick else '') + f'<div class="txt">{text}</div></div>')
    js.append(f"tl.fromTo('#{i}',{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.3,ease:'power3.out'}},{R(t0)});tl.to('#{i}',{{opacity:0,duration:0.2}},{R(t1) - 0.2});")
# A: layers
still('sA', 'layers.jpg', 259.8, 263.66, 1.0, 1.1); blk('', 'NOT BUILT OVERNIGHT', 261.92, 263.66, 'stage')
# B: one insert per word
ins = [('sB1', 'engineer.jpg', 263.66, 265.70, 'EXPERTISE', 264.72), ('sB2', 'scanner.jpg', 265.70, 267.44, 'ADVANCED MANUFACTURING', 265.70), ('sB3', 'robot.jpg', 267.44, 268.00, 'EQUIPMENT', 267.44),
       ('sB4', 'spincoat.jpg', 268.00, 268.86, 'MATERIALS', 268.00), ('sB5', 'design.jpg', 268.86, 269.67, 'RESEARCH', 268.86), ('sB6', 'world_hubs.jpg', 269.67, 271.19, 'GLOBAL SUPPLY CHAINS', 269.67)]
for i, img, t0, t1, txt, tt in ins:
    still(i, img, t0, t1, 1.0, 1.06); blk('', txt, tt, t1, 'tag')
# C: the engineer
still('sC', 'engineer2.jpg', 271.19, 281.49, 1.0, 1.12, 0.5)
blk('THE REAL TEST', 'NOT HOW MANY FACTORIES ARE ANNOUNCED', 272.47, 275.0, 'stage')
blk('WHAT THE COUNTRY CAN', 'MASTER', 276.17, 277.4, 'stage'); blk('', 'MANUFACTURE RELIABLY', 277.41, 279.7, 'stage'); blk('', 'CREATE FOR ITSELF', 279.77, 281.49, 'stage')
# D: follow the silicon (dark)
els.append('<div class="bg dark" id="sD"></div>'); show('sD', 281.49, 283.17)
blk('', 'FOLLOW THE SILICON', 281.81, 283.17, 'huge')
# E: four hard cuts
clip('vQ', 'S01FQ1080_14_Q_5600-5708.mp4', 283.17, 284.59); blk('', 'RAW MATERIAL', 283.39, 284.59, 'stage')
clip('vW', 'S02FQ1080_P06_polish_20306-20321.mp4', 284.59, 285.15); blk('', 'WAFER', 284.59, 285.15, 'stage')
clip('vL', 'S02FQ1080_P10_lattice_20561-20666.mp4', 285.15, 286.98); blk('', 'MICROSCOPIC CIRCUITS', 285.15, 286.98, 'stage')
still('sE', 'hero_ring.jpg', 286.98, 288.08, 1.0, 1.05); blk('', 'FINISHED CHIP', 287.0, 288.08, 'stage')
# F: dive + India assembles from dots
clip('vF', 'S02FQ1080_P07_fly_20322-20415.mp4', 288.08, 291.8)
els.append('<div class="bg dark" id="sF"></div>'); show('sF', 291.8, 295.1)
blk('', 'NOT BY SOFTWARE ALONE', 290.26, 292.7, 'stage'); blk('', 'BUILT ON SILICON', 293.69, 295.1, 'stage')
# G: finished processor + end line 1
still('sG', 'ai.jpg', 295.1, 298.0, 1.0, 1.07, 0.55)
blk('', 'INDIA’S SILICON FUTURE IS BEING BUILT.<br>LAYER BY LAYER.', 295.6, 298.0, 'end')
# H: end card
els.append('<div class="bg dark" id="sH"></div>'); js.append(f"tl.fromTo('#sH',{{opacity:0}},{{opacity:1,duration:0.35}},{R(298.0)});")
els.append('<div class="blk card" id="cardH"><div class="brand">XPLAINEDUNSEEN</div><div class="tagl">TECHNOLOGY IS MORE INTERESTING THAN IT LOOKS.</div></div>')
js.append(f"tl.fromTo('#cardH',{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.6,ease:'power3.out'}},{R(298.15)});tl.to('#cardH',{{opacity:0,duration:0.35}},{DUR - 0.35});tl.to('#sH',{{opacity:0,duration:0.35}},{DUR - 0.35});")
# India outline assembled from dots (positions computed in the page, the dots exist from the start)
random.seed(6); N = 1500
dots = ''.join(f'<circle class="dt" id="d{i}" r="3" cx="{random.uniform(200, 1720):.0f}" cy="{random.uniform(80, 1000):.0f}"/>' for i in range(N))
js.append(f"tl.fromTo('.dt',{{opacity:0}},{{opacity:1,duration:0.4,stagger:0.001}},{R(291.2)});"
          f"tl.to('.dt',{{attr:{{cx:(i,el)=>+el.dataset.tx,cy:(i,el)=>+el.dataset.ty}},duration:1.9,ease:'power3.inOut',stagger:{{each:0.0012,from:'random'}},immediateRender:false}},{R(291.8)});"
          f"tl.to('.dt',{{opacity:0,duration:0.3}},{R(295.0)});")
css = '''body{margin:0;background:#000}#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:#05080c;font-family:"Studio Grotesk","Inter",sans-serif;color:#fff}
.bg{position:absolute;inset:0;background-size:cover;background-position:center;opacity:0}.bg:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(4,7,11,.9),rgba(4,7,11,.25) 75%,rgba(4,7,11,.05))}.bg.dark{background:radial-gradient(ellipse at 50% 45%,#0c1a26,#05080c 70%)}.bg.dark:after{display:none}
.clip{position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover;opacity:0;transform:scale(1.07)}
.blk{position:absolute;opacity:0;left:110px;max-width:1000px}.kick{font-size:22px;letter-spacing:.3em;color:#4fd8ff;font-weight:600;margin-bottom:12px}
.txt{font-weight:700;letter-spacing:.06em;line-height:1.1;text-transform:uppercase}.tag{bottom:120px}.tag .txt{font-size:38px;padding:14px 26px;border-left:6px solid #4fd8ff;background:rgba(8,14,20,.82);display:inline-block}
.stage{bottom:120px}.stage .txt{font-size:56px}.huge{top:430px}.huge .txt{font-size:112px}.end{top:420px;max-width:1500px}.end .txt{font-size:72px;line-height:1.15}
.card{left:0;right:0;top:400px;text-align:center;max-width:none}.brand{font-size:104px;font-weight:700;letter-spacing:.32em;padding-left:.32em}.tagl{margin-top:26px;font-size:30px;letter-spacing:.24em;color:#4fd8ff;font-weight:600}
.dt{fill:#4fd8ff;opacity:0}#dots{position:absolute;inset:0}'''
script = '''window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady['india'] = (async () => {
  const topo = await (await fetch('hf-assets/maps/india-detailed.json')).json(); const ctry = topojson.feature(topo, topo.objects.country);
  const proj = d3.geoMercator().fitExtent([[560, 90], [1360, 990]], ctry); const d = d3.geoPath(proj)(ctry.features ? ctry.features[0] : ctry);
  const p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', d); const L = p.getTotalLength();
  document.querySelectorAll('.dt').forEach((c, i) => { const pt = p.getPointAtLength(L * i / document.querySelectorAll('.dt').length); c.dataset.tx = pt.x; c.dataset.ty = pt.y; });
})();'''
html = f'''<!doctype html><html><head><meta charset="utf-8"><script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><style>{css}</style></head><body>
<div id="root" data-composition-id="s06" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080" data-fps="24">
{chr(10).join(els)}
<svg id="dots" width="1920" height="1080" viewBox="0 0 1920 1080">{dots}</svg>
</div><script>{script}
const tl = gsap.timeline({{paused: true}});
{chr(10).join(js)}
window.__timelines = {{s06: tl}};</script></body></html>'''
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(html); print('ok', DUR)
