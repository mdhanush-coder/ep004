# S01 "The Invisible Brain": research note (2026-11-02)

## Subject facts (sources)
- **OLED phone stack, screen inward:** cover glass → optically clear adhesive → polariser (sometimes omitted) → touch electrodes (on-cell) → thin-film encapsulation → OLED emitters → TFT backplane on polyimide → midframe/chassis → shielding cans → logic board (stacked "sandwich" boards since iPhone X). [fieldscale.com touch-sensor stackups; iFixit iPhone X teardown]
- **SoC package:** package-on-package (PoP). The application processor is the bottom package, soldered to the board; the **DRAM package sits on top** on its own solder balls; underfill reinforces the joints. Current phones use fan-out InFO-PoP. [krayden.com PoP; GSMArena A18 die shots by ChipWise]
- **The die is flip-chip, face-down on micro-bumps.** From the screen side you meet the DRAM package, then the die's plain silicon backside, not its circuitry.
- **Scale:** phone SoC die is about 90–105 mm² with about 15–20 billion transistors (A18 15.2 B). "3 nm" is a node name, not a feature size. Narration says "billions", which is safe.
- **Visibility:** 8+ metal layers hide the transistors. Optical die shots of circuitry come from delayered dies. Transistors are below the optical limit, so SEM only (greyscale). The rainbow sheen on die shots is thin-film interference. [arXiv 1910.00948; ASM EDFA 2023]

## Common errors to avoid
Glowing transistors visible through the metal; approaching the die from the circuit side; AP drawn above DRAM; colour at transistor scale; "3 nm" used as a size.

## Best practitioners + technique (from descriptions; videos not watched by the researcher)
- **Branch Education** ("How are microchips made", smartphone flythroughs): continuous single-take flythroughs of detailed Blender models (Blender 4.x, Eevee + Cycles). Their touchscreen video took about 3 weeks. https://www.blendernation.com/2018/11/07/video-how-do-touchscreens-work/
- **Branch Education, "The $200M Machine that Prints Microchips"**: machine exterior → interior journey. https://evertiq.com/design/2025-11-14-zooming-in-on-the-machine-that-prints-microchips
- **Intel, "From Sand to Silicon" (2020)**: sand → FinFET → 3D wire stack scale journey. https://www.intel.com/content/www/us/en/newsroom/article/sand-silicon-making-microchip.html
- **Veritasium × ASML, "The World's Most Important Machine"**: live action intercut with animation. https://rosetta.to/u/veritasium/the-world-s-most-important-machine
- **Apple "All Systems Pro" (A18 Pro, TBWA\Media Arts Lab)**: premium dark-studio chip reveal. https://campaignbrief.com/?p=275163
- **Hook pacing:** YouTube Analytics measures the 30 s retention mark (support.google.com/youtube/answer/9314415). Practitioner advice (not studies): deliver the promise at once, change the visual often, no self-intro.

## What I could NOT find
Production breakdowns of any chip-dive sequence (Branch, Apple, Qualcomm, Asianometry); a primary source for the A18 Pro transistor count; peer-reviewed hook-pacing evidence. Nothing here invents a studio's internals.

## Asset check (EngineX libraries, 2026-11-02)
- 3D library: no smartphone, no PCB/chip, no car interior (steering wheels only), satellite dishes only.
- Unreal library: no phone, chip, cleanroom, satellite or car interior. Unreal is **not used in S01**.
- HDRIs available: Omniverse studio set ("studio small 05/07", free to use).

## Method chosen and why
| Shots | Method | Why |
|---|---|---|
| 01-01/02, 01-09, 01-12/13 phone, teardown, PoP, die | **Blender, own procedural hero model** (phone + separable stack + logic board + PoP + die) | No library phone; the push-through needs real separable layers; becomes the reusable hero chip asset for S02–S06 |
| 01-03/04/05 UPI tick, train ticket, AI chat | **Motion graphic** (GSAP), generic UI, no real branding | Exact, readable UI; AI images can't do text |
| 01-06 car ignition | **GEN** text-to-image → `first-image2video` or depth-motion | Supporting shot; no library asset |
| 01-07 satellite over India at night | **Blender**: Earth sphere with NASA Black Marble night-lights (public domain) + simple satellite + MG data lines | India's outline must be geographically correct, which GEN can't guarantee |
| 01-08 recap collapse, 01-10 software, 01-11 freeze | MG + edit (+ GEN+DM developer screens for 01-10) | |

## How it maps to the timeline (narration-locked)
- **01-09 push-through, 0:21.94–0:26.20, "Inside them, billions of microscopic switches…"**: one continuous camera move, about 4.3 s: cover glass refraction (0.8 s) → OLED pixel grid + TFT lines (1.0 s) → midframe/shield can (0.7 s) → logic board traces to the PoP; the DRAM package lifts off to show the solder balls and underfill (1.8 s).
- **01-12 die reveal, 0:30.53–0:35.32, "So why is building **the chips themselves**…"**: the camera slips **under** the substrate (cutaway) and looks up at the face-down die: iridescent top metal → metal layers peel away (illustrative delayering) → greyscale SEM-style transistor field on "challenge?". Small label `ILLUSTRATIVE · NOT TO SCALE`.
- **01-13 tail, 0:35.44–0:36.24**: the die tiles outward into a grid of identical dies, the first hint of the wafer, bridging to S02 ("Our journey begins with silicon…").

## Verification plan
1. Clay + lit preview stills of the hero phone stack and PoP (Gate B), checked against the layer order above.
2. Low-res Eevee motion test of 01-09 + 01-12 timed to the narration master (frames at 24 fps from the timing map), reviewed by the user before final.
3. Checks: DRAM above AP; die face-down; no transistors visible through metal; no "3 nm" size callout; label present.
