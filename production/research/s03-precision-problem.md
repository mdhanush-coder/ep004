# S03 "The Precision Problem": research note (2026-11-02)

## Research (date)

### Subject facts
- **Photolithography precision**: At the 45nm node, critical dimension uniformity (CDU) specifications call for 2nm or better (NIST, ITRS research)
- **Overlay requirements**: Level-to-layer registration accuracy requirements are less than 4nm repeatability for 100nm generation devices (NIST Overlay Metrology)
- **Particle contamination**: ISO 14644-1:2015 classifies cleanrooms by particle concentration (0.1µm to 5µm threshold sizes). Class 3 cleanroom: only 1,000 particles ≥0.1µm per cubic foot (halbleiter.org PDF)
- **Cleanroom operation**: Laminar airflow from ceiling through floor, positive pressure to prevent outside contamination, HEPA/ULPA filtration (halbleiter.org PDF)
- **Process steps**: coat (photoresist spin), expose (UV through mask), develop (solvent removes exposed areas), etch (material removal), deposit (layer addition), repeated 20-30+ times for modern chips (multiple sources)
- **Equipment**: Wafer transport via robotic arms, lithography scanners (multi-million dollar equipment), metrology tools for alignment verification

### Best practitioners + technique
1. **TED-Ed "How are microchips made?" (Kozmonot Animation Studio)**
   - URL: https://ed.ted.com/lessons/how-are-microchips-made-george-zaidan-and-sajan-saini
   - Technique: Stylized 2D/3D hybrid animation, clean flat design with abstract representations of microscopic processes
   - Storytelling: Uses analogies (cake layers) to explain complexity, shows scale transitions with visual comparisons
   - Timing: Explains one lithography layer with clear step-by-step visual, emphasizes precision without getting bogged in technical detail

2. **Silicon Run I & LITE**
   - URL: https://siliconrun.com/our-films/silicon-run-1 and https://siliconrun.com/our-films/silicon-run-lite/
   - Technique: Live industrial footage combined with microscopic filming, animation, graphics, and special effects
   - Storytelling: Shows real equipment and cleanrooms alongside animated process sequences
   - Camera: Macro shots of wafers, wide shots of cleanroom floors, cross-sectional views

3. **"How are Microchips Made?" YouTube (various creators)**
   - URL: https://www.youtube.com/watch?v=dX9CGRZwD-w
   - Technique: Scale transitions (mitochondria → dust → hair → transistor), split screen between microscopic and macroscopic views
   - Storytelling: Flips between "nanoscopic process" and "fab floor operation" to give complete picture
   - Visuals: 3D cross-sections of layers, size comparison bars, animated process diagrams

4. **Virtual Lab: Photolithography**
   - URL: https://www.wecanfigurethisout.org/VL/Photolith.htm
   - Technique: Interactive step-by-step visualization of coat → expose → develop → etch sequence
   - Storytelling: Click-through interface that lets user explore each step at their own pace

### What I could NOT find
- Specific camera techniques or lighting setups used by Silicon Run or Kozmonot for their cleanroom footage
- Detailed breakdown of how the scale transitions are technically executed in the YouTube videos
- Whether Kozmonot uses Blender, Unreal, or other 3D tools for their semiconductor animations
- Real cleanroom footage licensing terms for the specific Indian facilities (Dholera, Sanand)

### Method chosen and why
**Current approach (from S03_preview_v1.py):** Generated CGI stills as plates with 2.5D camera moves (depth-motion style). This is a valid approach for documentary animation where real footage is unavailable or licensing is prohibitive.

**Recommended refinement for S03:**
1. **Microscopic sequences (layers, spin, UV, develop, particle)**: Keep the plate-based approach but enhance with:
   - More accurate layer cross-sections showing realistic thickness ratios (oxide ~1-2µm, resist ~0.5-1µm)
   - Better material distinction (photoresist = colored/translucent, oxide = grey, metal = copper color)
   - Scale indicators that are clear but not distracting (show relationship to transistor size, not human hair)

2. **Macroscopic sequences (cleanroom, robot, scanner, gas, engineer)**:
   - If Unreal asset library has cleanroom assets, use Unreal for more spatial depth and realistic lighting
   - If not, enhance the generated plates with better depth-of-field and atmospheric lighting to feel more like real footage
   - Consider using GEN+DM with more diverse source imagery if current plates feel too uniform

3. **Particle contamination shot**: The single-particle visualization needs to be technically accurate:
   - Show particle size relative to feature size (e.g., 0.5µm particle bridging 50nm lines)
   - Use scale bar clearly indicating both dimensions
   - Animation should show the particle drifting slowly, then sudden freeze on impact

4. **Labels**: "PHOTOLITHOGRAPHY" and "ASSEMBLY & TESTING" are good additions. Add "ILLUSTRATIVE · NOT TO SCALE" for any microscopic cross-sections.

### How it maps to this shot
S03 has 16 shots covering:
- 03-01: World map with chip hubs (MG)
- 03-02: Layer-by-layer wafer cross-section (BL - can enhance realism)
- 03-03 to 03-06: Photolithography sequence (coat, expose, develop, etch) (BL - plate-based, refine materials)
- 03-07: Robot arm wafer transport (UE if asset exists, else BL/GEN)
- 03-08: Alignment marks and tolerance (BL + MG)
- 03-09 to 03-11: Particle contamination sequence (BL + MG scale bar - needs accuracy focus)
- 03-12 to 03-14: Cleanroom, equipment, expertise (UE if assets, else GEN+DM with variety)
- 03-15 to 03-16: Cut, package, test, verify (BL - reusing S02 assets)

### Verification plan
1. Review generated plates for technical accuracy:
   - Are layer thicknesses plausible relative to each other?
   - Is the particle-to-feature size ratio realistic (0.5µm vs 50nm)?
   - Do alignment marks look like actual lithography alignment marks (crosses, boxes)?

2. Check scale indicators:
   - Verify scale bar measurements match what they represent
   - Ensure "ILLUSTRATIVE" labels are present where appropriate

3. Test motion graphics:
   - Ensure labels fade in on the correct spoken word (per timing map)
   - Check that MG elements don't obscure the technical explanation

4. Preview review checklist:
   - Does the viewer understand why precision matters after the particle shot?
   - Is the transition from microscopic to macroscopic clear?
   - Do the cleanroom shots feel like real spaces, not generic rooms?
