# EP004 motion-graphics label pages: plays a silent scene video as the base layer and animates tags on the spoken words.
# usage: python ep004_mg_labels.py  -> writes mg/s03_labels.html and mg/s04_labels.html next to this file's project (EP004/production/mg/)
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'production', 'mg'); os.makedirs(OUT, exist_ok=True)

def page(video, dur, items, cid):
    # item: dict(text, t0, t1 [scene-relative s], kind 'tag'|'stage'|'note', kicker?, idx?)
    els = []; js = []
    for i, it in enumerate(items):
        k = it.get('kind', 'tag'); kick = it.get('kicker', '')
        els.append(f'<div class="lab {k}" id="l{i}"><div class="bar"></div><div class="body">' + (f'<div class="kick">{kick}</div>' if kick else '') + f'<div class="txt">{it["text"]}</div></div></div>')
        t0, t1 = it['t0'], it['t1']
        js.append(f"tl.fromTo('#l{i}', {{y: 22, opacity: 0, clipPath: 'inset(0 100% 0 0)'}}, {{y: 0, opacity: 1, clipPath: 'inset(0 0% 0 0)', duration: 0.32, ease: 'power3.out'}}, {t0:.3f});"
                  f"tl.to('#l{i}', {{opacity: 0, y: -10, duration: 0.22, ease: 'power2.in'}}, {max(t0 + 0.4, t1 - 0.22):.3f});")
    css = '''body{margin:0;background:transparent}#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:#000}
video{position:absolute;left:0;top:0;width:1920px;height:1080px;transform:scale(1.07);transform-origin:50% 50%}
.lab{position:absolute;display:flex;opacity:0;font-family:"Studio Grotesk","Inter",sans-serif;color:#fff;
 background:linear-gradient(90deg,rgba(7,11,17,.86),rgba(7,11,17,.62));backdrop-filter:blur(6px);border-radius:4px;box-shadow:0 8px 30px rgba(0,0,0,.45)}
.lab .bar{width:6px;background:#4fd8ff;border-radius:3px 0 0 3px;box-shadow:0 0 18px #4fd8ff99}
.lab .body{padding:16px 30px 16px 24px}.lab .kick{font-size:17px;letter-spacing:.28em;color:#4fd8ff;font-weight:600;margin-bottom:6px}
.lab .txt{font-weight:650;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap}
.tag{left:96px;bottom:112px}.tag .txt{font-size:34px}
.stage{left:96px;bottom:112px}.stage .txt{font-size:52px;letter-spacing:.1em}
.note{right:96px;top:72px}.note .txt{font-size:20px;letter-spacing:.2em;color:#cfe9f4}.note .bar{background:#ffb347;box-shadow:0 0 14px #ffb34788}.note .body{padding:10px 20px 10px 16px}'''
    return f'''<!doctype html><html><head><meta charset="utf-8"><script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><style>{css}</style></head><body>
<div id="root" data-composition-id="{cid}" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080" data-fps="24">
<video src="assets/{video}" data-start="0" data-duration="{dur}" muted playsinline></video>
{chr(10).join(els)}
</div><script>const tl = gsap.timeline({{paused: true}});
{chr(10).join(js)}
window.__timelines = {{{cid}: tl}};</script></body></html>'''

S3 = 74.75; S4 = 134.75
def r(t, base): return round(t - base, 3)
s3 = [
 dict(text='ILLUSTRATIVE MAP', t0=0.3, t1=3.3, kind='note'),
 dict(text='PHOTOLITHOGRAPHY', kicker='PROCESS', t0=r(84.11, S3), t1=r(86.9, S3), kind='stage'),
 dict(text='1 · COAT', t0=r(86.99, S3), t1=r(88.5, S3), kind='tag') if False else dict(text='COAT', kicker='STEP 1', t0=r(86.99, S3) + 0.5, t1=r(88.55, S3), kind='tag'),
 dict(text='EXPOSE', kicker='STEP 2', t0=r(88.91, S3), t1=r(91.4, S3), kind='tag'),
 dict(text='DEVELOP', kicker='STEP 3', t0=r(92.58, S3), t1=r(94.1, S3), kind='tag'),
 dict(text='ETCH', kicker='STEP 4', t0=r(95.26, S3), t1=r(96.0, S3), kind='tag'),
 dict(text='ADD LAYERS', kicker='STEP 5', t0=r(96.28, S3), t1=r(97.6, S3), kind='tag'),
 dict(text='ALIGNMENT & CONTROL', t0=r(103.7, S3), t1=r(106.3, S3), kind='tag'),
 dict(text='CONTAMINATION', t0=r(112.5, S3), t1=r(115.2, S3), kind='tag'),
 dict(text='FEWER USABLE CHIPS', t0=r(115.9, S3), t1=r(118.5, S3), kind='tag'),
 dict(text='CLEANROOMS', t0=r(121.56, S3), t1=r(123.4, S3), kind='tag'),
 dict(text='SPECIALISED MACHINES', t0=r(123.55, S3), t1=r(125.1, S3), kind='tag'),
 dict(text='PURE CHEMICALS & GASES', t0=r(125.2, S3), t1=r(127.1, S3), kind='tag'),
 dict(text='TECHNICAL EXPERTISE', t0=r(127.37, S3), t1=r(129.2, S3), kind='tag'),
 dict(text='ASSEMBLY & TESTING', kicker='AFTER FABRICATION', t0=r(129.3, S3), t1=r(134.7, S3), kind='stage'),
]
eco = [('MANUFACTURING', 171.22), ('EQUIPMENT', 172.16), ('MATERIALS', 172.99), ('PACKAGING', 173.85), ('TESTING', 174.51), ('RESEARCH', 175.17), ('TALENT', 175.83)]
s4 = [dict(text='ILLUSTRATIVE MAP', t0=0.3, t1=5.2, kind='note'),
      dict(text='CARS', t0=r(140.15, S4), t1=r(140.73, S4)), dict(text='MEDICAL EQUIPMENT', t0=r(140.73, S4), t1=r(141.66, S4)),
      dict(text='COMMUNICATION NETWORKS', t0=r(141.66, S4), t1=r(142.80, S4)), dict(text='DEFENCE SYSTEMS', t0=r(142.80, S4), t1=r(143.64, S4)),
      dict(text='SATELLITES', t0=r(143.64, S4), t1=r(144.22, S4)), dict(text='DATA CENTRES', t0=r(144.22, S4), t1=r(145.0, S4)), dict(text='AI', t0=r(145.0, S4), t1=r(145.9, S4)),
      dict(text='ILLUSTRATIVE MAP', t0=r(146.2, S4), t1=r(151.8, S4), kind='note'),
      dict(text='DESIGN', kicker='CAPABILITY', t0=r(166.40, S4), t1=r(168.0, S4), kind='stage')]
for i, (w, t) in enumerate(eco):
    t1 = eco[i + 1][1] if i + 1 < len(eco) else 176.7
    s4.append(dict(text=w, kicker=f'ECOSYSTEM  {i + 1:02d} / 07', t0=r(t, S4), t1=r(t1, S4) - 0.02, kind='stage'))
s4.append(dict(text='ILLUSTRATIVE MAP', t0=r(156.9, S4), t1=r(163.5, S4), kind='note'))
open(os.path.join(OUT, 's03_labels.html'), 'w', encoding='utf8').write(page('concat.mp4', 60.0, s3, 's03'))
open(os.path.join(OUT, 's04_labels.html'), 'w', encoding='utf8').write(page('concat.mp4', 48.8125, s4, 's04'))
print('ok')
