# S01 continuous low-res motion test v3 (2026-11-02)

**Preview:** `renders/previews/s01/motiontest_v3/S01_motiontest_v3_narrated.mp4`: 640×360, 24 fps, 979 frames, 40.79 s, AAC mono, audio and picture the same length (probed).
Studio: `blender/master-assets/ep004_s01_camera_v016.blend` (chain v011→v012 corrections→v013/v014 new shots→v015 time-shift +600→v016 fixes). Scripts: `blender/scripts/ep004_s01_patch_v012.py`, `…opening_phone_v1.py`, `…opening_sets_v3.py`, `…patch_v016.py`, `…preview_render_v5.py`.
Narration: slice 0–40.79 s of the approved master, untouched (offset 0). Picture cuts sit on the spoken words; boundaries are rounded to whole frames (≤ 0.02 s).
**I cannot play video.** Everything below was judged from sheets sampled from the encoded file (0.1 s / 0.11 s steps) and measured luminance. The user's playback is the final judge.

## Timeline (all in one continuous file)
0–21.94 s opening (O1 lock/buzz, O2 fingerprint unlock, O3 payment, O4 ticket, O5 AI chat, O6 dashboard, O7 satellite over India, O8 recap → chip → dark phone) · 21.94–26.19 push-through · 26.2–29.73 software shot (code wall + world map) · 29.73–30.33 freeze beat (static pose, 14 frames) · 30.33–35.33 chip dive · 35.33–36.25 wafer tail · 36.25–40.79 Scene 02 bridge (quartz, `SILICON`).
Opening, software and bridge shots are **preview-grade** (generic UI, no real brands, schematic map from Natural Earth public-domain data), not final art.

## Corrections made
- OLED macro: distinct R/G/B pixels, low glare (key lights dipped while among the glossy layers), moving brightness wave, steeper macro camera (keys 27, 40).
- DRAM framing: end key (102) pulled back so both packages and balls stay in frame; chip dive still starts on that exact pose.
- Chip dive: lit underside (world lighting that renders black to camera + softer under-light), 5 copper interconnect layers with scaled line pitch/bump/bevel, real 3D fin/gate/contact lattice, `ILLUSTRATIVE · NOT TO SCALE` label (camera-only visibility, no ghost reflections).
- Wafer tail: wafer visible by about frame 410 of its shot (was the last 0.2 s), identical dies, motion blur on the pull-back; colours less pastel.
- Continuity: table fades during the first frames of A so the opening→A cut no longer drops 42→4; dashboard no longer black before ignition.

## Measured on the final file
No clipping (0.036 % of pixels > 250). No frame-to-frame flicker flagged beyond intended hard cuts. Hard cuts at the cue words: 2.5, 4.0, 6.25, 8.1, 11.3, 13.4, 16.85 s etc.

## Remaining issues
1. 30.8–31.2 s: ≈ 0.4 s near-black beat as the board drops away before the die underside lights.
2. 23.5 s: screen layer fades quickly (113 → 39 in 0.11 s).
3. 37.1 s (bridge): brief bright facet glint (62 → 130 → 55); bridge framing crops the crystal bases and the last ~2 s is nearly static.
4. Wafer: colour now a flat mauve/olive disc with visible die grid, still not rich; wafer light-grey lattice.
5. Dashboard is dim (luminance 14–28) before ignition; ticket card flashes bright (≈ 147) during the recap.
6. Freeze beat is a rendered static pose; the true edit hold is still to be done in assembly.
7. Opening/software/bridge shots are placeholders in fidelity.
Not started: full-quality render (waiting for approval).
