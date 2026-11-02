# EP004 — Factual research notes

Basis: `documetary_skill.md` (production brief built from the *Animated Semiconductor Documentary* PDF; the PDF itself is **not** in the project).
Each claim was cross-checked on 2026-11-02 by a web check. Source links are in `research/sources.md` (numbers in [brackets]).

## Claim status

| # | Claim in narration / on screen | Status | Evidence | Used as |
|---|---|---|---|---|
| C1 | Tata Electronics is developing a fab at Dholera, Gujarat | ✅ Verified | Partner PSMC; nodes 28–110 nm; starts on 90/55 nm [1][2] | Narration S05, label "UNDER DEVELOPMENT" |
| C2 | Dholera commercial production expected mid-2028 | ⚠️ Reported, not a company-announced date | Bloomberg via TrendForce: "delayed to mid-2028"; the minister says mid-2028 [1][2] | Narration says "expected", not "scheduled" |
| C3 | Micron Sanand = assembly and testing (ATMP), not wafer fab | ✅ Verified | Packages DRAM/NAND wafers from Micron's global fabs; inaugurated 28 Feb 2026 [3][4] | S05 |
| C4 | CG Semi Sanand OSAT began commercial production July 2026 | ✅ Verified | Announced 4 Jul 2026; JV of CG Power, Renesas and Stars [5][6] | S05 |
| C5 | 12 units approved under Semicon India 1.0 | ✅ Verified | 1 silicon fab, 1 SiC fab, 1 display fab, 9 packaging units; 12th approved 5 May 2026 [7][8] | S05 overlay |
| C6 | "3 in commercial production: Micron, Kaynes, CG Semi" (**brief**) | ❌ Out of date | ISM site: **5** units in commercial production. CDIL (Mohali) and Suchi Semicon (Surat) started 17 Sep 2026 [8][9]. Kaynes Sanand OSAT started 31 Mar 2026 [10] | **Narration corrected**: "Micron, Kaynes and CG Semi led the way… by September 2026, five units had started" |
| C7 | ₹1.64 lakh crore+ cumulative **proposed** investment | ✅ Verified | "cumulative investment of over Rs.1.64 Lakh Crore" [7] | Always said as "proposed" |
| C8 | Semicon 2.0 approved July 2026, outlay ₹1,27,500 crore | ✅ Verified | Cabinet, 15 Jul 2026; six pillars [7][11] | "proposed outlay" (government outlay, not private investment) |
| C9 | India already has chip-design capability | ✅ Verified | About 20% of the global semiconductor design workforce (MeitY), mostly in multinational design centres [12] | S04. Do **not** imply India owns 20% of designs |
| C10 | Quartz contains silicon (as SiO₂); refined; single-crystal ingot; sliced; polished | ✅ Textbook | Czochralski growth; metallurgical-grade → polysilicon → ingot | S02 |
| C11 | Photolithography: coat → expose through pattern → develop → etch → new layers | ✅ Textbook | Fabs also repeat deposition, doping, CMP and cleans | S03 |
| C12 | A particle can damage features and reduce yield | ✅ Textbook | Shown as *some* dies lost, never "destroys the wafer" | S03 |

## Wording guardrails (from the brief plus the fact check)
- All three named Sanand units are **packaging and test (ATMP/OSAT)**. India has **no commercial wafer fab yet**, so never say "India now makes chips" without that qualifier.
- Tata Dholera is **under development**. Never show it as operating; any reconstruction is labelled conceptual.
- Investment figures are **proposed / outlay**, not spent.
- If nodes are ever mentioned: Dholera starts at **90 nm / 55 nm**, not 28 nm.

## Decisions (user, 2026-11-02)
- C6 approved: use **five** units in commercial production, always shown as assembly & testing (ATMP/OSAT), visibly separate from wafer fabrication.
- C2: keep the Dholera qualifier. Mid-2028 is a **reported target**, never a confirmed Tata commissioning date.
- Scene 05 stays at about 76 s.

## Still needs verification / a decision
0. **Whether CDIL Mohali's approved unit is ATMP/OSAT.** Suchi (Surat), Micron, Kaynes and CG Semi are confirmed OSAT/ATMP. CDIL makes discrete devices; confirm its unit type on the ISM approved-units list before the "all assembly & testing" label is locked.
1. **The source PDF** is missing from the project. The brief's "3 units" figure is dated 2 Nov 2026 but contradicts the ISM site. The narration follows the ISM site. If the PDF must be the only basis, use the alternative take (old wording).
2. **Mid-2028 for Dholera** is press-reported (Bloomberg) and repeated by the minister. Tata has published no date. The current wording ("expected") is safe.
3. **Primary pages could not be opened directly** (PIB and PMIndia returned HTTP 403). Their quotes come from search snippets of those official pages; ISM was opened directly. Re-open the PIB release (PRID 2311220) before publishing.
4. **Facility imagery**: licensed or verified photos of Dholera, Micron, Kaynes and CG Semi are not sourced yet.
