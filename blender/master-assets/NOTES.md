# EP004 hero phone asset: notes

Research: `production/research/s01-invisible-brain.md` (layer order, PoP, face-down die, honesty rules).

## Files
- Build scripts (versioned, each builds the whole asset): `blender/scripts/ep004_hero_phone_v001.py` … `v005.py`. **Current: v005.**
- Asset: `blender/master-assets/ep004_hero_phone_v005.blend` (earlier versions kept beside it).
- Preview stills: `renders/previews/s01/hero_phone_contact_v00N.png`, `die_underside_v00N.png`. 640×360, Cycles, 32 spp, so a **look-development check only, not a render deliverable**.
- Run it: upload the script, then `blender/script` with `exec(open(list(inputs.values())[0]).read())`. It builds in about 4 s.

## What it contains (1 unit = 1 cm, phone screen-up, +Z toward the viewer)
Collections: `01_DISPLAY_STACK` (cover glass, touch, OLED, TFT), `02_HERO_PHONE` (back glass, frame, midframe, battery), `03_LOGIC_BOARD` (board, 130+ SMD parts, shield can), `04_POP_SOC` (AP balls, substrate, die micro-bumps, **face-down die**, mould, DRAM balls, DRAM package), `04_LIGHTING`, `05_CAMERAS`.
Every layer is keyed on Z: frame 1 assembled, frame 50 exploded. Screen emission and touch grid are keyed too (dark at rest, lit when exploded).

## Gate B: against the research
| Check | Result |
|---|---|
| Layer order glass → touch → OLED → TFT → midframe → can → DRAM → AP → die → board | ✅ |
| DRAM package above the AP, with its own ball array (not stacked wrongly) | ✅ |
| Die is face-down: circuit side toward the board, silicon backside toward the screen | ✅ (material index on faces with normal −Z) |
| Shield can open underneath, like a real lid | ✅ (v005) |
| Transistors not visible through the metal | ✅ No transistor geometry in S01 yet |
| Die underside reads: bump array, iridescent metal | ✅ readable, iridescence **subtle** |
| "3 nm" used as a size | ✅ Not used |

## Known issues (not blocking a motion test, to fix before final)
1. The OLED layer reads **beige** at distance because the 120/cm sub-pixel stripes average out. Needs a closer-up look test, or a coarser stripe for the wide shots.
2. Passives are plain boxes, and the board is dark and quiet. The close-ups need more incidental detail (pads, a connector, labels with no real brands).
3. The AP substrate and DRAM package are almost the same dark slab. Give the DRAM a visible marking-free texture and a different tone so the two packages separate on screen.
4. Thin-film iridescence works (supported on this Blender build) but is faint at 32 spp. Re-check at a higher sample count.
5. ~~No camera animation yet~~: done, see the S01 camera section below.
6. The die circuit face is a stylised pattern. The `ILLUSTRATIVE · NOT TO SCALE` label is needed on screen (motion graphics).

## Verification still to do
A timed low-res **motion** test of shots A/B/C (only contact sheets exist so far), then user review before any final render.

---
# S01 camera moves (2026-11-02): `ep004_s01_camera_v010.blend` (build: `blender/scripts/ep004_s01_camera_v010.py`)
One file, three shots, bound to cameras with timeline markers. 24 fps, frames locked to the approved narration (`production/timing-map.md`, word times in `edit/captions/ep004_words_master.json`).

| Shot | Frames | Narration time | Camera | Words → picture |
|---|---|---|---|---|
| **A** 01-09 push-through | 001–102 | 21.94–26.20 s | `CAM_S01_A_pushthrough`, 40 mm | "Inside them" glass lifts · **"billions"** (23.14) OLED sub-pixel macro · "microscopic" TFT, midframe window · **"switches"** (24.66) board → PoP · "process information" DRAM lifts off, balls and die visible |
| **B** 01-12 chip dive | 201–320 | 30.33–35.32 s | `CAM_S01_B_dive`, 50 mm | f201 = f102 pose (freeze beat 29.73–30.33 holds f201 in the edit) · "So why" board/substrate drop away · **"building"** (31.64) die face from below · **"chips"** (32.30) metal layers peel M6→M1 · "such a" transistor field exposed · **"challenge?"** (34.86–35.32) field fills the frame |
| **C** 01-13 tail | 401–422 | 35.32–36.24 s | `CAM_S01_C_wafer`, 50→28 mm | metal layers slide back, identical dies tile outward, camera pulls back to a wafer disc; hand-off to S02 (quartz / silicon) |

## Verified
- Camera path: subject centred (x = 0.5) at every probe frame in B and C. Camera step ≤ 2.3 cm/frame in A, ≤ 0.12 in B, ≤ 7.4 in C (the deliberate fast pull-back).
- Contact sheets (8 frames per shot, 480×270, 24 spp): `renders/previews/s01/sheet_{A_pushthrough,B_dive,C_wafer}_v010.png`. **No video has been rendered.**
- Bugs found by inspection and fixed on the way: box-built parts lost their base height (DRAM/shield/battery), the mould compound covered the die, metal layers + transistor field were built at the world origin, the wafer disc sat in front of the die, coaxial light glare.

## Known gaps (preview quality, not final)
1. Transistor field is a flat greyscale lattice: reads as "repeating pattern" but has no SEM depth/shading yet.
2. Copper wiring layers in the peel (f255–f280) are dark; need more light or a brighter copper.
3. Wafer-tile colours are pastel; the hero die's texture scale differs slightly from its neighbours.
4. Layers dissolve (alpha) as the camera crosses them rather than being cut through; check that on motion.
5. Needs on-screen `ILLUSTRATIVE · NOT TO SCALE` (motion graphics), and the freeze beat is an edit hold, not rendered.
6. The wafer shot should hand off to S02's quartz opening; S02 not built.

## v011 patch (motion test round 1)
In-place patch of v010 (`blender/scripts/ep004_s01_patch_v011.py`): layer dissolves 3→8 frames + exposure dip over the screen layers (A); stronger, softer under-light and brighter copper layers, transistor field fades in with contacts and stronger relief (B). Camera keys, shot ranges and narration timing unchanged. Results and remaining problems: `production/motiontest-s01-report.md`.
