"""Build the EP004 5:00 narration timeline from the six approved scene takes.

Inserts the picture-only beats (pre-roll, mid-scene holds, tails), then writes:
  assets/audio/narration/ep004_narration_master.wav   - full 5:00 narration bed
  edit/captions/ep004_words_master.json               - every word on the global timeline
  edit/captions/ep004_en.srt                          - English captions (global timing)
  production/timing-map.md                            - scene boundaries + line timing
Run from the EP004 folder: python -X utf8 edit/build_timeline.py
"""
import array, json, re, wave

RUNTIME = 300.0
NARR = 'assets/audio/narration/ep004_s0{}_sameer.wav'
WORDS = 'edit/captions/s0{}.raw.json'

# Picture-only beats in seconds: pre-roll, holds inserted before/after a word, tail.
# ("before", word) inserts the hold in the silence before the last match of that word;
# ("after", word) in the silence after the first match.
SCENES = [
    dict(n=1, title='The Invisible Brain', pre=1.2, tail=0.8,
         holds=[('before', 'So', 0.6, 'freeze beat: activity stops, sound drops')]),
    dict(n=2, title='From Quartz to a Chip', pre=0.3, tail=0.3,
         holds=[('after', 'computing.', 0.5, 'transistor-array impact reveal')]),
    dict(n=3, title='The Precision Problem', pre=0.3, tail=0.3,
         holds=[('before', 'Now', 1.0, 'particle freeze, near-silence')]),
    dict(n=4, title='Why India Needs the Capability', pre=0.3, tail=0.2,
         holds=[('after', 'away.', 0.6, 'delayed shipment ripples downstream')]),
    dict(n=5, title="India's Silicon Bet", pre=0.2, tail=0.2, holds=[]),
    dict(n=6, title='The Future Is Built Layer by Layer', pre=0.2, tail=2.02,
         holds=[]),
]

# ASR spellings -> script spellings (captions only; the audio is correct)
FIX = {'Canes': 'Kaynes', 'Keynes': 'Kaynes', 'Macron': 'Micron', "Macron's": "Micron's",
       'Dolera': 'Dholera', 'Bholera': 'Dholera', 'Sanant': 'Sanand', 'Semican': 'Semicon',
       'defense': 'defence', 'centers': 'centres', 'specialized': 'specialised'}


def read_wav(path):
    w = wave.open(path)
    return array.array('h', w.readframes(w.getnframes())), w.getframerate()


def words_of(n):
    out = []
    for w in json.load(open(WORDS.format(n), encoding='utf8'))['word_segments']:
        if 'start' in w:
            core = w['word'].strip(',.?:;')
            fixed = FIX.get(core, core)
            out.append(dict(word=w['word'].replace(core, fixed), start=w['start'], end=w['end']))
    return out


def hold_point(words, where, target):
    idx = [i for i, w in enumerate(words) if w['word'].strip(',') == target]
    i = idx[-1] if where == 'before' else idx[0]
    if where == 'before':
        return (words[i - 1]['end'] + words[i]['start']) / 2
    return (words[i]['end'] + words[i + 1]['start']) / 2


def ts(t):
    cs = round(t * 100)
    return f'{cs // 6000}:{cs // 100 % 60:02}.{cs % 100:02}'


def srt_ts(t):
    ms = round(t * 1000)
    return f'{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}'


master, sr, gwords, scenes_out, cursor = array.array('h'), None, [], [], 0.0
for sc in SCENES:
    audio, sr = read_wav(NARR.format(sc['n']))
    words = words_of(sc['n'])
    cuts = sorted((hold_point(words, w, t), d, why) for w, t, d, why in sc['holds'])
    start = cursor
    master.extend([0] * int(sc['pre'] * sr)); cursor += sc['pre']
    src_pos, shift, events = 0.0, cursor, []
    for at, dur, why in cuts:
        master.extend(audio[int(src_pos * sr):int(at * sr)])
        events.append((shift + at, dur, why))
        master.extend([0] * int(dur * sr))
        for w in words:
            if src_pos <= w['start'] < at:
                gwords.append(dict(scene=sc['n'], word=w['word'], start=round(w['start'] + shift, 3), end=round(w['end'] + shift, 3)))
        shift += dur; src_pos = at
    master.extend(audio[int(src_pos * sr):])
    for w in words:
        if w['start'] >= src_pos:
            gwords.append(dict(scene=sc['n'], word=w['word'], start=round(w['start'] + shift, 3), end=round(w['end'] + shift, 3)))
    cursor = shift + len(audio) / sr + sc['tail']
    master.extend([0] * int(sc['tail'] * sr))
    # keep sample count in step with the float cursor
    want = int(round(cursor * sr)); master.extend([0] * max(0, want - len(master))); del master[want:]
    scenes_out.append(dict(sc, start=start, end=cursor, events=events, vo=len(audio) / sr))

assert abs(cursor - RUNTIME) < 0.01, f'runtime {cursor:.3f}s, not {RUNTIME}'
master.extend([0] * max(0, int(RUNTIME * sr) - len(master)))

w = wave.open('assets/audio/narration/ep004_narration_master.wav', 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(master.tobytes()); w.close()
json.dump(gwords, open('edit/captions/ep004_words_master.json', 'w', encoding='utf8'), indent=0, ensure_ascii=False)

# Captions: break at sentence ends or 42 characters, never across scenes
cues, cur = [], []
for w in gwords:
    width = len(' '.join(x['word'] for x in cur + [w]))
    # a sentence's last word may run to 50 characters rather than sit alone on a cue
    if cur and (cur[-1]['scene'] != w['scene'] or width > (50 if re.search(r'[.?!]$', w['word']) else 42)):
        cues.append(cur); cur = []
    cur.append(w)
    if re.search(r'[.?!]$', w['word']):
        cues.append(cur); cur = []
if cur:
    cues.append(cur)
with open('edit/captions/ep004_en.srt', 'w', encoding='utf8') as f:
    for i, c in enumerate(cues, 1):
        f.write(f"{i}\n{srt_ts(c[0]['start'])} --> {srt_ts(c[-1]['end'])}\n{' '.join(x['word'] for x in c)}\n\n")

# Timing map: scenes, sentences, holds
lines = ['# EP004 timing map (generated by edit/build_timeline.py — do not hand-edit)', '',
         f'Runtime **{ts(cursor)}** · narration {sum(s["vo"] for s in scenes_out):.2f} s · '
         f'picture-only {cursor - sum(s["vo"] for s in scenes_out):.2f} s · {len(gwords)} words', '',
         '| Scene | Start | End | Length | VO | Picture-only |', '|---|---|---|---|---|---|']
for s in scenes_out:
    lines.append(f"| S0{s['n']} {s['title']} | {ts(s['start'])} | {ts(s['end'])} | {s['end'] - s['start']:.2f} s | "
                 f"{s['vo']:.2f} s | {s['end'] - s['start'] - s['vo']:.2f} s |")
for s in scenes_out:
    lines += ['', f"## S0{s['n']} {s['title']}  ({ts(s['start'])}–{ts(s['end'])})", '',
              f"- {ts(s['start'])} picture-only pre-roll {s['pre']:.2f} s"]
    sent, items = [], []
    for w in (x for x in gwords if x['scene'] == s['n']):
        sent.append(w)
        if re.search(r'[.?!]$', w['word']):
            items.append((sent[0]['start'], f"- {ts(sent[0]['start'])}–{ts(sent[-1]['end'])} {' '.join(x['word'] for x in sent)}")); sent = []
    items += [(t, f'- {ts(t)} **HOLD {d:.2f} s** — {why}') for t, d, why in s['events']]
    lines += [x for _, x in sorted(items)]
    lines.append(f"- {ts(s['end'] - s['tail'])} picture-only tail {s['tail']:.2f} s")
open('production/timing-map.md', 'w', encoding='utf8').write('\n'.join(lines) + '\n')
print('\n'.join(lines[:12]))
print(f'cues {len(cues)}  master {len(master) / sr:.3f}s')
