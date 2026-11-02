# S01 continuous low-res motion test v5 (2026-11-02): corrections round 2

**Preview:** `renders/previews/s01/motiontest_v5/S01_motiontest_v5_narrated.mp4`: 640×360, 24 fps, 979 frames, 40.79 s, AAC mono (audio and picture identical length, probed).
Studio: `blender/master-assets/ep004_s01_camera_v018.blend` (patches `blender/scripts/ep004_s01_patch_v017.py`, `…_v018.py`; render script `…preview_render_v7.py`).
Judged from sheets sampled from the encoded file and measured luminance; I cannot play video. Narration = approved master slice 0–40.79 s, unchanged. No approved camera path, shot duration or narration timing changed.

| Request | Result (measured on the encoded file) |
|---|---|
| 1 Chip-dive dark beat | Fixed. First 3.2 s of the dive hold luminance 41–72 (was dipping to 4). Cause was an edge-on black slab on black after the board dropped; fixed with a lighter mould compound, a faint backdrop and a grazing fill light only during the drop. Darkest sample in the whole preview 13.7; no stretch < 10 for > 0.2 s. |
| 2 OLED fade (23.5 s) | Improved, not eliminated: pixels dim slowly (emission ramp) and the layer dissolves only when dim; lights return sooner. The drop is now a 0.5 s ramp (121 → 18) and recovers to 78 as the board comes into view. Still a visible dip through the dark layers. |
| 3 Wafer | Dark gunmetal silicon with bright silver die lanes and rim, sheen across the disc, clear grid of identical dies. No longer mauve/olive. |
| 4 Freeze beat | True hold: the push-through's own final frame (scene frame 702) rendered 14 times with the noise seed locked, no camera move. Consecutive sampled frames differ by ≈ 0.5/255 (encode noise). |
| 5 Scene 02 bridge | Flash fixed (luminance ramps 16 → 41 and stays, was 62 → 130 → 55); crystal bases and floor reflection inside the frame; subtle camera drift through the last ~1.6 s. |

## Remaining
- OLED dip described above; hard cuts of the opening (planned) and the bright ticket flash during the recap.
- Wafer hue is gunmetal rather than rich blue-violet.
- Quartz label overlaps the crystal bases slightly.
- Opening, software shot and bridge remain preview-grade placeholders.
- Backdrop during the board drop is a visible dark slate (deliberate).
Full-quality render NOT started.
