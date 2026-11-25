*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

REFEREE REPORT: shapes

Second step, 03:59 to about 04:20 UTC (inside the 35 minutes). Scripts and outputs are in /home/agent2/shape-referee/: flowp.py and flowp.out (full-circle solver, no symmetry needed), after_ref.py and after_ref.out (the fresh clouds and the poolings).

**FINDINGS, the most serious first**

1. The excess at 100,000 points (your item 3). Three sentences do not stand as written.

 (a) "**At 100,000 points every kind of cloud stands a little above the theory: the sheet's nine sets together by 0.7 (0.3) parts in 100, and with the fresh clouds twelve sets by 0.8 (0.2).**"
 - The two figures are right: I get 1.0073 (0.0031) and 1.0075 (0.0024).
 - "Every kind of cloud" is not: 4 of the 13 files lie below their own lines (square 0.9967, ellipse 0.9954, disc0 0.9979, fresh half disc 0.9971).
 - The excess is carried by one shape and one file:

 | pooling, measured over own line | ratio (se) | errors from 1 |
 |---|---|---|
 | quarter disc, all 84,000 clouds | 1.0169 (0.0050) | +3.4 |
 | quarter disc, fresh 76,000 only | 1.0146 (0.0052) | +2.8 |
 | all but the quarter disc, 10 files | 1.0047 (0.0027) | +1.7 |
 | those less the sheet's disc set, 9 files | 1.0029 (0.0029) | +1.0 (chi-square 2.9 on 8) |
 | fresh discs and fresh half discs alone | 1.001 (0.005) | +0.2 |

 - The quarter disc's 84,000 clouds give w·n = 0.3804 (0.0019), which is 2.7 errors above the ceiling itself.
 - Both accounts fit the 13 files: a common level (chi-square 13.9 on 12), and "the theory, with the quarter disc alone off". The section prints only the first.

 (b) "Set against that common level (the six ceiling sets' 0.3774) the quarter disc is 0.9 of an error high."
 - This is too kind in three ways.
 - The quarter disc's own line is 0.3741, not the ceiling. Scaled to it the level is 0.3761 and the fresh quarter discs are +1.4.
 - The level leans on the disc set that the same paragraph calls a high draw. With the fresh discs in its place the level is 0.3764 (0.0014), only 0.7 errors above the ceiling, and the quarter disc is +1.9.
 - With all 84,000 quarter discs it is +2.3.

 (c) "30,000 fresh discs give 0.3777 (0.0031): the first set was a high draw." and "Fresh discs say it was chance (finding 16);"
 - The fresh set is 0.7 errors above the line and 1.1 below the first set. It cannot tell the two apart.
 - The 60,000 cloud.c discs together give 0.3802 (0.0022), 2.2 errors above the line.

 (d) "I have no account of an excess that is there at the larger size and not at the smaller; it is 1.9 errors from being the same at both." The 1.9 is right (0.0086 (0.0046)). Accounts not named:
 - The quarter disc alone, as in (a). It cannot be a wrong I: 1.7 in 100 would need I·A/T² = 1.3415, above 4/3.
 - A constant next term. Var = (theory at D′) − b fits both sizes with D′ = 1.093 (0.005) and b = 0.065 (0.035). That D′ is the study's own finding 13 ("1.096 (0.019) at 10^5 points, 1.094 (0.026) at 10^6"), which also says the disc's excess sits at 0.6 to 0.95 of the radius. The mean already has a constant term (+0.1 layer at both sizes). The section quotes 1.095 but does not join it to this paragraph.
 - The generator. Every set above the line is cloud.c's. The one set that is not (disc0) reads 0.9979 (0.0099), 1.0 error from cloud.c's 1.0081 (0.0025): neither cleared nor convicted. More disc0 clouds would settle it.
 - Selection. The pooled "twelve sets" keep the two first draws that were followed up because they were high.
 - My reading: too kind to the quarter disc, and too broad in the bold sentence.

2. "so **for every convex shape the standard deviation of the count is, when the points are many, at most 0.6127/√n of its mean with exactly n points and 0.9055/√n with the number left to chance, and those are the figures for a disc, a triangle, a square.**"
 - This is a bold statement about counts, to four figures. "What the third addition does not say" says the ceiling is "a fact about the equation, not a theorem about peeling", and that it is only as well placed as D.
 - From the section's own digits the constant is 0.6078 at D = 1.073 and 0.6213 at 1.095.
 - The clouds: the six ceiling sets give √0.3774 = 0.6143 (0.0011); the quarter disc 0.6168 (0.0015); 8 of the 13 files at 100,000 lie above 0.3754.
 - The sentence needs "by the equation, with D = 1.081" inside the bold, and "about 0.61".

3. "On paper it comes out that the spread of the count, set against its mean, is the same for ellipses, triangles, parallelograms and regular polygons and is smaller for every other convex shape;"
 - Contradicted by the section's own bullet ("regular polygons and kites are (by symmetry)") and by the theorem, which gives equality wherever T/A^(2/3) stands still.
 - That class is not determined. notes.md section 5, "Among all shapes those are the ellipses (where it is least)", is asserted and not proved: nothing shows that a smooth shape with ψ level on its edge is an ellipse.
 - "Smaller or the same for every other" is what is proved. The sealed sheet has the same slip ("for every other shape it is less than that"); it belongs among the sheet's slips.

4. "The solve is tested by the other program alone: `erode.c` gives the change of T when each side of a polygon is moved, and from those the edge formula gives I, to 4 parts in 10,000 of `flow.c`'s for a triangle and for a square with a corner cut off (`shape/stest.py`);"
 - For a triangle the edge formula returns (4/3)T²/A whatever the program, since scaling fixes each side's gradient. The printed ratio 0.99962 is (0.81975/0.81991)² = 0.99961: a test of T, not of the solve.
 - For the cut square, 99 in 100 of I is that same ceiling part. The shortfall is what tests the solve, and there the two programs give 0.01305 (erode, 1.32028) against 0.01385 (flow, 1.31948): 6 in 100 apart.
 - What does bear the claim: arccheck.out (g on the quarter disc, to 2 in 10,000), and now my solver (finding 5).

5. The proof (your item 1). I went through sections 4, 5 and 7 line by line and found no hole.
 - The backward equation is the one I derived blind.
 - dΓ/dt = −2q is right: L is symmetric, and both g and ∂g/∂t have no cos or sin.
 - The split I = (4/3)T²/A + (3/2)∫ z L⁻¹z is right.
 - The sign is right: the form has one positive direction, h is on it, and w = L⁻¹z is at right angles to h. Its null directions there are cos and sin only, so equality needs z = 0.
 - The disc bound of section 7 is the one I gave blind. "The flow's time is least for an ellipse" is used but not derived; it is one line: dA/dt = −L ≥ −(8π²A)^(1/3).
 - The kite argument is right. An isosceles trapezoid's mirror maps every member of its family to itself, so nothing is forced; that agrees with your 1.3328 and my blind 1.328.
 - Correction to my blind report: I said a trapezoid's side gradients were forced equal. That was wrong; turning a side is not a first-order change of h.

 Three places where the notes are thinner than the result:
 - (i) The end. "As the shape vanishes it becomes an ellipse and Γ goes to nothing with it" rests on a theorem you have not read, and on Γ being continuous there. It is not needed. g ≥ 0 by comparison, so |∫ g L⁻¹g| ≤ (∫g dθ)²/(2π). The form is a mixed area, so area-keeping affine maps leave it alone. With John's ellipse made a disc of radius r, ∫g dθ ≤ (4/3)T/r ≤ 2^(4/3) r^(1/3). So Γ → 0, and since Γ falls, Γ ≥ 0 and I is finite.
 - (ii) Polygons. The identity at t = 0 is a limit and needs g(t) → g(0) as measures. In my solver the corner fans' share of g falls only as about the 0.37 power of the corner radius (8 to 10 in 100 at radius 0.003), and ψ at the corner grows as the −0.63 power. That fits your 4/3-power argument, but "g is nothing between the sides' directions" is true only in a slow limit.
 - (iii) I·A/T² is not smooth at a polygon. By your own files the shortfall is 0.00028 at a swelling of 1e-4 (stopcheck) and 0.0113 at 0.02 (ceiling): about the 0.7 power. So "a starting shape a hundred times less rounded at its corners moves T and I by as little" holds at 1e-6 and not in general.

 The numbers, with my own solver (flowp.py). The limit was taken with T alone: each side moved by ±0.002, then your edge formula.

 | shape | mine | yours |
 |---|---|---|
 | cut square, I·A/T² | 1.31951 to 1.31954 | 1.31948 |
 | cut square, shortfall | 0.013824 | 0.01385 |
 | cut square, T over the disc's | 1.07609 | 1.07613 |
 | hexagon 0, 40, 110, 170, 230, 300: shortfall | 0.000121 (at 360, 720 and 1,080 angles; radii 0.001 and 0.0003) | 0.000124 |

 - Controls: a scalene triangle and a square both read a shortfall of 0.000000; Euler's sum is 1.00000.
 - The identity itself, by my backward solve on the cut square rounded at 0.001 (720 angles): summed inside 1.31862, from the edge 1.31859. These are lower than the sharp figure because of (iii).

6. "**16. The five shapes at the ceiling have one relative spread, and it is the predicted one.**"
 - The numbers under it say "to half a part in 100, 1.4 errors above" (0.3774 (0.0014)), or 0.7 errors with the fresh discs.
 - The same finding's bold then says every kind stands above the theory. Heading and bold cannot both stay unqualified.
 - I would write "... and it is the predicted one to 1 part in 100".

7. The plate (your item 4). I looked at shape.png by eye; I did not measure it by script.
 - It draws what its title says for the sheet's nine sets.
 - It draws none of the 146,000 fresh clouds, which the section uses to re-read two of its nine columns. The quarter-disc dot (0.3893, from 8,000 clouds) is the least representative figure in the section: 84,000 clouds give 0.3804.
 - The label "dashed: the theory's ceiling, 0.3754, for every convex shape" stands as fact under a dot 2.5 errors above it.
 - Add the fresh sets as open dots, or say in the caption that they are not drawn.

8. The sheet (your item 2). The verdicts follow the letter: I recomputed every figure from the raw files and all sixteen are inside their bands. The account of ruler.out is fair: the nine lines that some wrong rule fails every time, and the seven that none does, are as the section lists them. Not said:
 - S3, S13, S14 and S15 have bands of ±4 to ±5 in 100 on figures good to 0.6 to 1.0. They would have held for any D from about 1.06 to 1.10, so the sheet could not see the excess of finding 1.
 - S16 is S7 and S8 over again.
 - The triangle and square parts of S2 were known from the first study.

9. "**17. The triangle with round corners falls short of the ceiling by what was worked out.**"
 - The measured shortfall is 0.042 (0.006) against 0.045: agreed, to one part in seven. The heading could say so.

10. Small things.
 - "above the discs from the old one by 2.2 in 100 (1.6 errors)": from the printed digits, (3.818 − 3.738)/√(0.031² + 0.037²) = 1.66, so 1.7.
 - "2.3 errors above 3.745": study.out prints 2.4; the figure is 2.35.
 - "Write g for ψ on the edge of K itself, taken per unit of the angle θ of the edge's normal instead of per unit of length": ψ is per unit of area. A reader cannot recover g = ψ·R from this; say "g = ψ times the radius of curvature".
 - "had ψ been level along each curve (the least I can be)": that is the least for that flow; finding 15 gives another least (a disc's).
 - along.out, cited for the ceiling, starts its polygons at 1.3341 and 1.3340, above 4/3. That is inside its "good to about 0.001", but it needs a word.
 - erode.c's T is low by 1.6 to 2.0 in 10,000 on the polygons, always the same way. My solver sides with flow.c to 2 in 100,000 (triangle 0.81993, square 0.78606, rounded triangle 0.80342).

11. The web (your item 6): three searches and two pages, about four minutes. Everything below is a tool's summary; both fetched pages came back paraphrased with short excerpts, so I have read no source myself.
 - Summaries found nothing on a first variation or shape derivative of the affine flow's vanishing time, nothing on I = (3/2)⟨g, L⁻¹g⟩ or a bound of 4/3, and nothing on the variance of the total number of layers in a general shape. They returned Dalal, Calder and Smart, and Calka and Quilan again.
 - A summary of Sapiro and Tannenbaum's abstract (J. Funct. Anal. 1994) says the affine isoperimetric ratio never falls along the flow and the curve tends to an ellipse. You do not use the monotone ratio; it bears on along.out.
 - arXiv:2604.14804, which came up twice, is a fourth-order area-keeping flow and is not relevant.
 - "Not in print, as far as three searches went" is fairly put.

**CHECKED AND FOUND SOUND**
- The sheet's sha256 is c64724a6… as printed. flow.c, erode.c, cloud.c, smake.py, theory.py, theory.json and the three batch scripts match the sheet's hashes. notes-as-sealed.md and stest-as-sealed.py match. notes.md sections 1 to 6 are identical to the sealed file. batchA.out says "began 00:13:05".
- 384,000 clouds in 15 files; 1,820 peeled both ways; seeds contiguous, none shared between files or with runs-after.
- Brier score 0.0626 from the printed odds.
- The table of 14 against my blind figures: T ratios agree to 2 in 100,000 on six shapes; I·A/T² 1.3304, 1.3311 and 1.3056 against my 1.3303, 1.3310 and 1.3056.
- From the printed digits: 0.6127 and 0.9055; 0.3754 and 0.8199; every w·n in the table of 16; 1.176 and 1.074; 1.195 and 1.098; chi-square 14.6 on 9 (I get 14.7); 0.9595, 0.9560 and 0.9577, at 6.9 and 0.5 errors; sealed 0.9547; the three differences over (4/9)·mean²/n; the three growth ratios; the slopes (mine identical); D read back as 1.085 and 1.080; 0.3694 and 0.3860; 0.0967 (0.0006).
- runs-after by my own program: discs 0.3777 (0.0030); quarter 0.3825 (0.0043) and 0.3788 (0.0022); half disc 0.3725 (0.0026).
- The tests as far as their files go: stest.out 101 passed; smutants.out 58 planted, 57 noticed, the control passed; smutants-part.out shows the new strip test catching fault 9; ymutants 24 of 24; pmutants 22 of 22; ruler 36 cases.
- passed.out's reasoning: 0.0006 of the area is worth 0.40 layers each way, and they cancel for a disc.
- cloud.c's grid is 2^28 to the unit, too fine for ties to matter.

**NOT DONE**
- I did not run your tests or the planted faults, or read flow.c or erode.c. The claims for them are checked against their output files only.
- The plate was not measured by script; sfigtest and pmutants were not examined beyond their last lines.
- The time on the shared board was not checked.
- I did not test cloud.c's quarter disc for evenness myself.
- along.out, stopcheck.out and incircle.out were read, not rerun, apart from the one hexagon and the cut square.
- No source was read in the original.
- I have no proof that the quarter disc's excess is real or is chance: at 3.4 errors in 84,000 clouds, after a look elsewhere over nine shapes, I would not call it either.
