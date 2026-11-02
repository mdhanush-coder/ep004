# EP004 — Narration-to-visual production map (v1, for approval)

Times are global and come from the recorded sameer narration (`production/timing-map.md`). Picture changes land on the spoken word they illustrate.
Each shot runs 1.5–6 s; nothing static runs past 7 s. **Bold** marks a reveal that has to land on that exact word.

**Tool key**
- **BL** Blender (`blender/script`, `preview`, `render`; Cycles/Eevee). Exact geometry and process science.
- **UE** Unreal (`unreal/scene`, `unreal/script`, asset library via `find_unreal_asset`). Large lit spaces and long camera journeys.
- **MG** Motion graphic (GSAP page, `motion-graphic` + `/snapshot` + `/check`). Maps, labels, data, end card.
- **GEN** Generative workflow: `text-to-image`, `image_editing`, `first`/`firstlast-image2video`, `upscale_image`. Mood, atmosphere and inserts only. Never facts, text, chip layouts or real facilities.
- **DM** `depth-motion`: 2.5D parallax on a still, so stills never sit as static frames.
- **CUT** `image-cutout` / `rotoscope`: cutouts and depth layers for compositing.
- **SFX** sound library (`find_sound`). Music from the library first; `text-to-music` only if nothing fits.

Continuity thread: **one hero chip / one hero wafer** (same Blender master asset) appears in every scene.

---

## S01 The Invisible Brain — 0:00.00–0:36.24 (36.2 s)
| ID | Time | Narration cue | Visual | Tool |
|---|---|---|---|---|
| 01-01 | 0:00.0–1.4 | (pre-roll) | Darkness. A phone buzzes on a table and its screen lights the frame. | UE (or BL) |
| 01-02 | 1.4–3.6 | "you **unlock** a phone" | Macro on the fingerprint unlock; the screen wakes. | BL + MG UI |
| 01-03 | 3.6–5.4 | "send a **UPI** payment" | UPI-style confirmation tick, as a generic recreated UI with no real app branding. | MG |
| 01-04 | 5.4–7.4 | "book a **train ticket**" | Ticket appears on the phone, then a match cut… | MG → GEN+DM |
| 01-05 | 7.4–11.0 | "ask artificial intelligence…" | Chat bubble types; AI answer streams in. | MG |
| 01-06 | 11.4–12.9 | "A car engine **starts**" | Dashboard ignition: gauges sweep and light up. | GEN image → DM / image2video |
| 01-07 | 13.5–16.3 | "A **satellite**…" | Satellite crossing over India at night; data lines pulse to the ground. | UE or BL (Earth) + MG lines |
| 01-08 | 16.9–21.4 | "Different experiences. **One hidden foundation**" | Fast four-panel recap collapses into the phone; "computer chips" lands as the screen goes dark. | MG + edit |
| 01-09 | 21.9–26.2 | "**billions** of microscopic switches" | Camera pushes through the glass, display layers and PCB to the processor. | BL (phone teardown asset) |
| 01-10 | 26.6–29.5 | "India builds software…" | Code wall reflected on the processor lid; developers' screens across India. | GEN+DM / MG |
| 01-11 | 29.7–30.3 | **HOLD 0.6 s** | Everything freezes and the sound cuts. | edit + SFX |
| 01-12 | 30.5–35.3 | "So why is building the chips themselves…" | Processor fills the frame; circuit traces light; the camera dives at the silicon. | BL |
| 01-13 | 35.4–36.2 | (tail) | The die surface becomes the transition into S02. | BL |

## S02 From Quartz to a Chip — 0:36.24–1:14.75 (38.5 s)
| ID | Time | Narration cue | Visual | Tool |
|---|---|---|---|---|
| 02-01 | 36.2–40.8 | "begins with **silicon**… **quartz**" | Reverse-zoom out of the die to a raw quartz crystal; label `SILICON`. | BL + MG label |
| 02-02 | 41.2–44.6 | "ordinary **sand** cannot simply become a processor" | Sand grains next to a finished processor, split screen. | BL (or GEN plate + BL chip) |
| 02-03 | 45.1–48.0 | "refined to extraordinary **purity**" | Grey material resolves into bright polysilicon chunks. | BL (shader/geo transform) |
| 02-04 | 48.0–50.5 | "**grown into a single crystal**" | Seed rod pulls a glowing ingot from the melt (Czochralski). | BL |
| 02-05 | 50.5–52.5 | "**sliced** into thin wafers" | Wire-saw slices; a wafer falls away. | BL |
| 02-06 | 52.5–53.8 | "and **polished**" | Moving reflection sweeps across the mirror wafer; label `WAFER`. | BL + MG |
| 02-07 | 54.2–57.5 | "microscopic structures are created" | Fly across the wafer grid and select one die. | BL |
| 02-08 | 57.9–61.8 | "**transistors**: tiny electrical switches" | Dive to one transistor; gate voltage shown; channel OFF to ON (two clear states); label `TRANSISTOR`. | BL + MG |
| 02-09 | 62.5–63.5 | "One switch is simple." | Single switch toggles once, crisp. | BL |
| 02-10 | 64.1–67.5 | "**Billions** working together" | Pull back: array repeats via instancing, then fractal-scale zoom-out. | BL (Geometry Nodes) |
| 02-11 | 67.6–68.1 | **HOLD 0.5 s** | Array impact beat. | edit + SFX |
| 02-12 | 68.3–74.4 | "Follow one tiny section… almost unbelievable" | Array resolves into the hero chip; it enters the litho tool. | BL |

## S03 The Precision Problem — 1:14.75–2:14.71 (60.0 s)
| ID | Time | Narration cue | Visual | Tool |
|---|---|---|---|---|
| 03-01 | 74.8–77.5 | "Why can't every country…" | World at night with a handful of chip hubs lit and India dim, an abstract map. | MG |
| 03-02 | 78.2–83.5 | "extraordinary **precision**, **layer after layer**" | Wafer cross-section builds layer by layer, stacking up. | BL |
| 03-03 | 83.9–88.2 | "**light-sensitive coating**" | Resist spin-coat on the wafer; label `PHOTOLITHOGRAPHY`. | BL (fluid/shader) |
| 03-04 | 88.6–91.1 | "Light **transfers** a pattern" | UV through a mask; the pattern exposes in the resist. | BL |
| 03-05 | 91.5–94.0 | "**developed**" | Exposed resist washes away. | BL |
| 03-06 | 94.0–97.3 | "**etched**… new layers **added**" | Etch carves; a deposition layer settles; repeat loop ×2, fast. | BL |
| 03-07 | 97.7–101.2 | "many specialised stages" | Wafer hops tool to tool on a robot arm (match cuts). | UE or BL |
| 03-08 | 102.2–105.4 | "precise alignment and control" | Alignment marks snap into register; tolerance readout. | BL + MG |
| 03-09 | 105.4–106.5 | **HOLD 1.0 s** | Near-silence; a single particle drifts into frame. | BL + SFX |
| 03-10 | 106.5–110.4 | "imagine a microscopic **particle**" | Freeze; magnify; scale bar next to a human hair and to the features. | BL + MG scale bar |
| 03-11 | 111.0–118.0 | "**damage** tiny features… fewer usable chips" | Particle lands and bridges two lines; wafer map shows dies turning red (some, not all). | BL + MG wafer map |
| 03-12 | 118.7–122.0 | "controlled **cleanrooms**" | Wide cleanroom: yellow light, bunny-suited engineers, overhead transport. | UE (asset library) or GEN+DM |
| 03-13 | 122.0–125.0 | "specialised machines" | Lithography scanner exterior, panels and robotics. | UE / BL |
| 03-14 | 125.0–128.8 | "pure chemicals and gases… expertise" | Gas lines and valves; an engineer at a console. | GEN+DM inserts |
| 03-15 | 129.3–134.4 | "**cut, packaged, tested** and verified" | Wafer dicing → die on substrate → wire bonds → test probe; label `ASSEMBLY & TESTING`. | BL |
| 03-16 | 134.4–134.7 | (tail) | Finished package flips to camera, the hand-off. | BL |

## S04 Why India Needs the Capability — 2:14.71–3:03.29 (48.6 s)
| ID | Time | Narration cue | Visual | Tool |
|---|---|---|---|---|
| 04-01 | 134.7–137.4 | "back to **India**" | Chip package match-cuts into a dark digital map of India. | MG (map) |
| 04-02 | 137.8–145.4 | "cars, medical… satellites, data centres, AI" | Icons light on the map in rhythm with each word; quick 0.7–1 s inserts of each system. | MG + GEN inserts |
| 04-03 | 145.9–152.1 | "**concentrated** in a small number of hubs" | Map pulls out to a world view; a few hubs glow and supply arcs converge. | MG |
| 04-04 | 152.7–155.9 | "A **delayed shipment**" | One container on an arc stalls and turns amber. | MG |
| 04-05 | 156.0–156.6 | **HOLD 0.6 s** | Ripple runs downstream; factory icons dim one by one. | MG + SFX |
| 04-06 | 156.8–163.8 | "**strategic vulnerability**" | India on the map, dependence lines pulling inward; flat, tense. | MG |
| 04-07 | 164.3–167.5 | "India already has **design** capabilities" | Design-studio layout screens; label `DESIGN`, lit. | GEN+DM + MG label |
| 04-08 | 167.5–176.4 | "ecosystem: manufacturing, equipment… talent" | Ecosystem ring: each node lights on its word (manufacturing, equipment, materials, packaging, testing, research, talent). | MG |
| 04-09 | 176.7–183.0 | "not simply to assemble… create the technology" | Ring locks around the hero chip. | MG + BL chip |

## S05 India's Silicon Bet — 3:03.29–4:19.77 (76.5 s, the longest scene, so cut density matters most)
| ID | Time | Narration cue | Visual | Tool |
|---|---|---|---|---|
| 05-01 | 183.3–188.6 | "from announcements towards facilities" | Headlines fade back; a construction crane silhouette rises. | MG + GEN+DM |
| 05-02 | 189.1–190.9 | "**Gujarat**" | Dark India map; Gujarat lights in saffron. | MG |
| 05-03 | 191.3–196.0 | "Tata… fabrication facility at **Dholera**" | Label `DHOLERA · FABRICATION · UNDER DEVELOPMENT`; conceptual fab reconstruction tagged "Conceptual visualisation". | UE / BL + MG |
| 05-04 | 196.4–201.9 | "**2028**… commercial production expected" | Date chip `TARGET: MID-2028 (REPORTED)`, sub-line `NOT YET OPERATIONAL`. Never "commissioning date" or a fixed date. Site timeline shows a dashed (projected) segment. | MG |
| 05-05 | 202.5–209.5 | "**Sanand**, Micron… assembly and testing, **not** wafer fabrication" | Map hop to Sanand; label `ASSEMBLY & TESTING`; a "FABRICATION" tag strikes through; memory-module test line. | MG + BL/UE (ATMP line) |
| 05-06 | 210.0–215.4 | "CG Semi… July 2026" | Separate Sanand marker for CG Semi; date chip `JUL 2026 · COMMERCIAL PRODUCTION`. | MG |
| 05-07 | 215.8–222.9 | "Fabrication… Assembly and testing…" | Split screen: left the wafer gaining circuits (S03 asset), right the die packaged and probed (S03-15 asset). | BL reuse + MG |
| 05-08 | 223.3–226.5 | "**Twelve units** approved" | `12 APPROVED UNITS · SEMICON INDIA 1.0`, splitting into two colour-coded groups: `3 FABS` (cyan: silicon, SiC, display) and `9 ASSEMBLY & TESTING UNITS` (saffron). The same two colours are used for the rest of S05. | MG |
| 05-09 | 227.0–231.3 | "Micron, Kaynes, CG Semi led the way" | Three **saffron** (ATMP/OSAT) markers in Sanand pulse in order of start date, each tagged `ASSEMBLY & TESTING`. | MG |
| 05-10 | 231.8–235.5 | "by September 2026, **five**" | Two more saffron markers (Mohali, Surat) light. Counter: `5 IN COMMERCIAL PRODUCTION` / sub-line `ALL ASSEMBLY & TESTING (ATMP/OSAT)`. Beside it, the cyan Dholera marker stays outlined (not filled): `WAFER FAB · UNDER DEVELOPMENT`. | MG |
| 05-11 | 235.9–241.2 | "**₹1.64 lakh crore**" | Overlay `₹1.64 LAKH CRORE+ · PROPOSED INVESTMENT` over moving ATMP footage. | MG + BL/GEN plate |
| 05-12 | 241.7–252.8 | "Semicon **2.0**… **₹1,27,500 crore**" | `SEMICON 2.0 · APPROVED JUL 2026` then `₹1,27,500 CRORE · PROPOSED OUTLAY`; six pillar icons. | MG |
| 05-13 | 253.3–259.8 | "bigger than one factory… **ecosystem**" | Pull back from a tested chip to the ecosystem network of facilities, people and research. | BL chip → MG network |

## S06 The Future Is Built Layer by Layer — 4:19.77–5:00.00 (40.2 s)
| ID | Time | Narration cue | Visual | Tool |
|---|---|---|---|---|
| 06-01 | 259.8–263.2 | "not built overnight" | Time-lapse feel: one layer deposits, then another, slowly stacking. | BL (reuse 03-02) |
| 06-02 | 263.7–270.7 | "expertise in manufacturing, equipment…" | Fast inserts: tool, material, lab and supply line, one per word. | GEN+DM inserts |
| 06-03 | 271.2–281.2 | "The real test… master, manufacture, create" | Young Indian engineer in the cleanroom, camera moving past them; hero wafer catches the light. | UE (character) or GEN consistent ref + DM |
| 06-04 | 281.5–287.7 | "Follow the silicon again. **Raw material. Wafer. Circuits. Finished chip.**" | Four hard cuts on the four words: quartz, wafer, transistor array, hero chip (S02 assets). | BL reuse |
| 06-05 | 288.1–294.7 | "not software alone… **built on silicon**" | Dive through the wafer; transistor structures assemble into the **outline of India**. End line 1 appears: `INDIA'S SILICON FUTURE IS BEING BUILT. LAYER BY LAYER.` | BL + MG |
| 06-06 | 295.1–297.9 | "Can India build an entire future around it?" | Single finished processor on dark ground. | BL |
| 06-07 | 298.0–300.0 | (tail 2.0 s) | `XPLAINEDUNSEEN — TECHNOLOGY IS MORE INTERESTING THAN IT LOOKS.` | MG |

---

## Reusable master assets (build once, reuse)
1. **Hero chip + package** (BL): S01, S02, S03-15, S04-09, S05-13, S06.
2. **Hero wafer** (BL): S02, S03, S05-07, S06.
3. **Transistor + array** (BL, Geometry Nodes): S02, S06-04/05.
4. **Litho process rig**: coat, expose, develop, etch, deposit (BL): S03, S06-01.
5. **India / world map system** (MG): S03-01, S04, S05, S06-05 outline.
6. **Label and data-card templates** (MG): every scene.
7. **Cleanroom** (UE asset library if one exists, otherwise GEN+DM): S03, S06.

## S05 labelling rules (approved 2026-11-02)
- Two colour codes all through S05: **cyan = wafer fabrication**, **saffron = assembly & testing (ATMP/OSAT)**. Operating units are filled markers; under-development units are outlined.
- The five operating units are always labelled assembly & testing. No S05 graphic may suggest an operating wafer fab in India.
- Dholera always carries `UNDER DEVELOPMENT`, and its date is shown as `TARGET: MID-2028 (REPORTED)`.
- Investment cards always say `PROPOSED`; Semicon 2.0 says `PROPOSED OUTLAY`.

## Open checks before visual production
- Confirm that all five operating units, CDIL Mohali included, are ATMP/OSAT approvals, before the 05-10 label is final.
- `find_unreal_asset`: is there a cleanroom, phone, car interior or character in the Unreal library? This decides UE or GEN+DM for 01-06, 03-12, 06-03.
- Real facility imagery (Dholera, Sanand) needs verified, licensed photos. Until then everything there is a labelled **conceptual visualisation**.
- Captions: `edit/captions/ep004_en.srt` uses ASR punctuation. Polish casing, numerals (₹1.64 lakh crore, 2028) and two split sentences ("at Sanand.", "capabilities The") at the assembly step.
