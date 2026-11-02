# EP004 handoff — state 2026-11-02

## Status: Steps 0 + 1 complete. User approved (2026-11-02): S05 "five units" (always labelled ATMP/OSAT, distinct from fabs), S05 kept at ~76 s, Dholera mid-2028 kept as a reported target.
**Narration APPROVED by the user** after listening via `review/narration_review.html`. Scene 01 has started. Do NOT regenerate or overwrite the narration tracks or master.

## Update 2026-11-02 (later): narration APPROVED by user; Scene 01 in progress
- Research note: `production/research/s01-invisible-brain.md`. Method per shot is in it. Unreal is not used in S01.
- Hero phone asset v005 built and checked on stills: `blender/master-assets/ep004_hero_phone_v005.blend` (+ `NOTES.md` with known issues).
- **Camera moves done (contact-sheet verified, no video yet):** shots A/B/C in `blender/master-assets/ep004_s01_camera_v010.blend` (build script `blender/scripts/ep004_s01_camera_v010.py`; notes in `blender/master-assets/NOTES.md`).
- **Motion test rendered (low-res, v2 after in-place patch v011):** `renders/previews/s01/motiontest_v2/`; report `production/motiontest-s01-report.md`. Waiting for the user's review. **No full-quality render until the user approves.**
- **Not done yet in S01 (camera moves removed from this list):** MG shots (unlock, UPI, ticket, AI chat, labels), car ignition (GEN), satellite over India (Blender + night-lights), freeze beat and recap edit.
- Render rule: previews only until the user reviews a timed S01 preview; no final renders.

## Update: continuous S01 motion test v3 rendered (opening → bridge into S02)
- `renders/previews/s01/motiontest_v3/S01_motiontest_v3_narrated.mp4`; report `production/motiontest-s01-report-v3.md`; studio `blender/master-assets/ep004_s01_camera_v016.blend` (animation shifted +600 frames from v015 on; opening frame = n-527+600).
- Awaiting the user's review. **No full-quality render until explicit approval.**

## Update: motion test v5 (round 2 corrections) rendered; user says frames look good
- `renders/previews/s01/motiontest_v5/S01_motiontest_v5_narrated.mp4`; `production/motiontest-s01-report-v5.md`; studio `blender/master-assets/ep004_s01_camera_v018.blend`.
- **User asked for 'the next step' but earlier set a gate: full-quality render needs explicit approval. Confirm with the user before rendering.**

## Done (verified)
- Folders: production/ research/ blender/ unreal/ assets/ renders/ edit/ delivery/
- Fact check → `research/source-notes.md`, `research/sources.md`
- Narration, voice **sameer** (user request; oliver takes kept in `assets/audio/narration/_superseded_oliver/`)
  - `assets/audio/narration/ep004_s01..s06_sameer.wav`: each take passed ASR QA against the script
  - S05 is spliced (two takes) because sameer misreads numbers; see `production/script.md`
  - `assets/audio/narration/ep004_narration_master.wav`: 5:00.000 with picture-only holds
- Timing: `edit/build_timeline.py` → `production/timing-map.md`, `edit/captions/ep004_words_master.json`, `edit/captions/ep004_en.srt`
- Narration-to-visual map with a tool per shot: `production/narration-visual-map.md`

## Lessons (sameer voice)
- Garbles years, decimals and "point oh" unpredictably; every take differs. Keep one number per line, put years mid-sentence, QA every take with `transcribe/subtitle`, splice lines across takes in the 250 ms gaps.
- "A car starts" was garbled twice; "A car engine starts" read fine.
- `transcribe/words` returns large JSON inline; use `transcribe/subtitle` and download `transcript.json` instead.

## Next (after approval)
1. `find_unreal_asset` check (cleanroom, phone, car, character).
2. xu-research-first, then Scene 01 build: preview → user review → final.

## Update 2026-11-02 (S02 started while S01 awaits the user's review)
- Research: `production/research/s02-quartz-to-chip.md`. Build script `blender/scripts/ep004_s02_v003.py` (v001→v003 kept), studio file `blender/master-assets/ep004_s02_v003.blend`. 10 stages, one camera each, frames locked to the timing map (local f = (global s − 36.24)·24 + 1).
- Contact sheets only (no video): `renders/previews/s02/v001|v002|v003/`. Latest per shot: v003 for crystal/polish/transistor, v002 for the rest.
- AI-generated plates (user request: look like the Blender frames): `assets/generated/s02/s02_gen_{quartz,ingot,wafer,chip}_v001.png`, made with `image_editing` from Blender stills (`ref_*` in the v002 sheets). Not yet animated (depth-motion) and not yet in a timed preview. Chip plate invented extra PCB parts: inserts only.
- Open problems: transistor cross-section (02-08/09) still unclear (camera sees the top, channel hidden); crystal-pull melt blown out; shots 02-02/03/05/07/10/12 fine as previews. No MG labels (SILICON, WAFER, TRANSISTOR, ILLUSTRATIVE), no timed/narrated preview, no final render.
