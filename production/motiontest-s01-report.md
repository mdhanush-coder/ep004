# S01 low-res motion test: report (2026-11-02)

**Preview:** `renders/previews/s01/motiontest_v2/S01_motiontest_v2_narrated.mp4`: 640×360, 24 fps, 244 frames, 10.17 s, narration under it (AAC mono).
Per-shot clips beside it (`S01_A_pushthrough_…`, `S01_B_dive_…`, `S01_C_wafer_…`) and 10-per-second frame sheets (`frames_*.jpg`). v1 is in `motiontest_v1/` (kept for comparison).
Studio file: `blender/master-assets/ep004_s01_camera_v011.blend` = v010 + `blender/scripts/ep004_s01_patch_v011.py` (in-place patch; camera keys, shot ranges and narration timing unchanged).

**How judged:** I cannot play video. Findings come from frame sheets sampled every 0.1 s plus measured luminance (0–255) and frame-to-frame change per sample. Your own playback is the final judge.

**Preview structure:** shot A (21.94–26.19 s) → B (30.33–35.33 s) → C (35.33–36.25 s), narration windows cut to match. The unbuilt 26.2–30.3 s section (software shot, freeze beat) is not in the preview, so the sentence "India builds software…" is skipped there.

| Question | v1 | v2 (patched) |
|---|---|---|
| Camera speed / continuity | No jump cuts; B starts on A's last pose; C starts on B's. A: fast opening swoop (≤ 2.3 cm/frame), a near-static macro ~0.8 s, ~1 s settle at the end. B: gentle (≤ 0.12 cm/frame). C: fast eased pull-back (≤ 7.4 cm/frame). | unchanged (camera not touched) |
| Layer fades | **Pop:** screen layers wash out to ~150 then collapse to ~15 in ≈ 0.2 s | Smoother: 109 → 40 over ≈ 0.5 s. A **brief dark dip to ~9 remains** (~0.1 s, t ≈ 1.9 s). Screen layers still read as a beige wash. |
| Transistor lattice | Bright grey (≈ 125) flash after ~2.3 s of near-black (≈ 12) | Fades in with the peel (12 → 136 over ~3 s, no flash); contact blocks added. Reads as a repeating chip layout, still flat and stylised, not obviously transistors. Label as illustrative. |
| Wafer hand-off | Continuous | Continuous: lattice → metal layers slide back → identical dies → wafer disc. Wafer appears only in the last ≈ 0.25 s; colours muddy. |

## Remaining problems
1. A, ~0.8–1.6 s: OLED macro is a beige wash; the RGB sub-pixels show only at the bottom edge (glancing camera angle, camera locked).
2. A, final ~1 s: nearly static, DRAM drifts out of the top of frame.
3. B, first ~1.7 s: die underside still dim (luminance 12–20): metal reflects the black world.
4. B: copper layers read as flat orange sheets.
5. C: wafer arrives late and in muddy pastel/olive.
6. Not in the preview: freeze beat (edit hold), `ILLUSTRATIVE · NOT TO SCALE` label, S02 hand-off.

No full-quality render has been started.
