# EP004 — Narration review package (awaiting human listening approval)

**Open `review/narration_review.html` in a browser.** It plays the real files from disk; nothing is uploaded. It has:
- the full 5:00 master, with a clickable scene, hold and splice bar;
- a live word-highlighted transcript (click any word to jump there);
- a 19-point listening checklist with OK/Fix and a note per item. "Copy review notes" turns your verdicts into text to paste back to me.

## Files under review (approved assets; nothing is regenerated or overwritten)
| File | Length |
|---|---|
| `assets/audio/narration/ep004_narration_master.wav` | 300.000 s |
| `assets/audio/narration/ep004_s01_sameer.wav` … `ep004_s06_sameer.wav` | 33.64 / 37.41 / 58.36 / 47.48 / 76.08 / 38.01 s |

## What machine QA already established
| Check | Result |
|---|---|
| Every word against the script (ASR) | All six match. ASR spellings like "Canes" and "Macron" are transcription, not speech |
| Runtime | 300.000 s exactly |
| Peak level | −1.0 dBFS on every scene (no clipping) |
| Speech loudness by scene | −17.1 to −18.5 dBFS RMS (within 1.4 dB) |
| S05 splice seams (12.673 s, 18.703 s in the scene file) | −90 dBFS: cut inside digital silence, so no click is possible |
| Spliced line vs neighbours | −16.4 dBFS vs −17.2 before and −19.6 after (normal line-to-line variation, but **listen**) |

## What only a human can judge (the checklist targets these)
- Voice quality, naturalness and emotional build across all five minutes.
- Pronunciation: U-P-I, Dholera, Sanand, Kaynes, Semicon, lakh/crore figures.
- **Splice at 3:16.2–3:22.2** (master time): same tone and room on both sides?
- A **0.7 s pause after "At Sanand,"** (3:22.5) inside one sentence: natural or awkward?
- Sentence break at 2:44 ("capabilities. The challenge…"): ASR heard no break.
- Whether the 0.6–1.0 s picture-only holds feel intentional.

## If something fails
Fixes are line-level: re-voice only the failing line in sameer and splice it into the silence gap, as was done in S05. Every approved line stays untouched, and the timing map is rebuilt with `edit/build_timeline.py`. Nothing is replaced without your sign-off.

## Approval gate
- [ ] Narration master approved by user → then Scene 01 starts from the actual timestamps in `production/timing-map.md`.
