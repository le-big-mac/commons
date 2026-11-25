*[Added to the public copy: Written by Noon, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. The front page says how it was checked and how it was not.]*

BLIND READING: Young's rods

Clock: began 14:33 UTC, ended 14:43; inside the 30 minutes. The web took about 7 minutes of that (roughly 14:35 to 14:42).
Assumed throughout for numbers: f = 150 mm, lens f/4, picture on the slide 75 mm wide, IK = KN = 1550 mm, sizes m = 2 to 20.

**1. The arrangement and the claim**
- A lantern in a box H on wheels faces a fixed screen G; the slide E is fixed in the box and the lens F rides on a slide of its own.
- Three rods meet at a joint K above: IK to a pivot I on an arm of the box, KN to a pivot N on the screen, KL to a pivot L on the lens slide.
- As the box is drawn back K sinks and KL pushes the lens toward the slide; as it advances the lens is drawn out.
- Claim: "the image is always distinctly painted on the screen", at every distance.
- Conditions he gives: KN = IK; I twice the focal length before the object; L immediately under the focus of the lens.
- A shade M, let fall by the lens support as the box advances, is to dim the shrinking image.

**2. Is it true? Exactly, in paraxial optics, given six conditions, three of them unstated.**
Proof:
- Let I, L, N lie on one line, with IK = KN = a and KL = b. The circle about K of radius a passes through I and N.
- The power of L with respect to that circle gives LI · LN = a² − b², whatever the position of K (L lies between I and N, so b < a).
- Put I at 2f before the object, L under the screen-side focus, N in the screen plane. With u, v the object and image distances, LI = u − f and LN = v − f.
- So the rods enforce (u − f)(v − f) = a² − b². Newton's relation, which Young gives on p. 418, is (u − f)(v − f) = f².
- The two agree for every position if and only if a² − b² = f². I checked this numerically: the worst lens error over m = 1.02 to 20 is 6e-11 mm (faults.py).

Conditions:
- C1, IK = KN: stated by Young and by Brewster.
- C2, I at 2f before the object: stated by both.
- C3, L under the focus: stated by both; neither says it is the focus on the screen side.
- C4, N in the plane of the screen: stated by neither; only drawn.
- C5, I, L, N in one straight line parallel to the travel of the box and of the lens slide: stated by neither.
- C6, IK² − KL² = f²: stated by neither. It is implied if the thing is assembled in focus once with C1 to C5 kept, because KL is then whatever joins K to L. Miss it and the image is in focus nowhere.

Further points:
- Brewster repeats Young's three conditions nearly word for word and adds none. He writes "KT" for KN.
- The length IK is free and sets the range: m + 1/m ≤ 2·IK/f.
- At m = 1 the linkage is at a dead point (KL upright) and cannot pass through it.
- For a thick lens "2f" must read "the distance between the two focal points".
- More generally the three pivots may all be shifted together: p, p − f, p − 2f from object, lens and screen, for any p.
- Lens aberrations are outside the claim.

**3. The engraving, in plate pixels (crop.py, measure.py, asdrawn.py)**

| Thing | Reading | ± |
|---|---|---|
| I, eye at the end of the box arm | (1022, 980) | 2.5 |
| L, ring under the lens slide | (1055.5, 984) | 1.5 |
| K, apex | (1208, 755) | 2 |
| N, eye on the far face of the screen block | (1375, 990) | 2 |
| Lens F centre (dark from 969.5 to 983) | x = 976 | 2 |
| Slide E: pillar 861.5 to 875.5; right face taken as object plane | x = 876 | 2, plus a choice of 868.5 to 881 |
| Screen G: block 1306 to 1376.5, middle 1341; far face taken | x = 1376.5 | 2, plus a choice of 35 |
| Slopes: ground, lens rail, line I–N | 0.0273, 0.0227, 0.0283 | 0.009 on I–N |

Conditions in the drawing (errors from 20,000 draws of the reading errors above):
- C1: IK = 291.9, KN = 288.3; difference 3.7 ± 4.0. Kept.
- C5: L lies 3.1 ± 3 px off the line I–N, and that line is parallel to the ground within 0.001 ± 0.009. Kept.
- C3 and focus: f from L is 79.5 ± 2.5; f from u = 100, v = 400.5 is 80.0 ± 1.8. They agree, with a drawn magnification of 4.0. With the slide's middle as object plane f is 84.8; with the rays' origin, 76.8.
- C4: N is −1.5 ± 2.8 px from the far face. Kept if the far face is the screen; N is 34 px (0.43 f) beyond the middle of the block.
- C2: I is 146 px before the object, which is 1.83 f; it falls short of 2f by 14.0 ± 3.6 px (12 to 16 across the three readings of the object plane). Not kept.
- C6: √(IK² − KL²) = 97.3 ± 8.7, and √(LI·LN) = 103.3 ± 4.4, against f = 80. Not kept. LI is 33.5 ± 2.9 where 20.0 ± 1.1 is wanted.
- C2 and C6 are one fact, not two: in a single drawing with IK = KN, IK² − KL² equals LI·LN necessarily.
- Built to the drawing's proportions and sharp at m = 4, the blur would be 1/13 of the picture width at m = 2, 1/43 at m = 3, 1/69 at m = 5, 1/21 at m = 10, 1/15 at m = 20.
- The drawn rays are schematic: one solid ray is bent away from the axis at the lens (slope 0.248 to 0.281), so no focal length can be taken from them.

**4. Faults (faults.py)**
Measure: diameter of the geometric blur circle on the screen as a fraction of the picture's width. For a lens error δ it is (D/f)(δ/w)(m − 1)/m. Each cell gives lens error in mm, then blur.

| Fault of 1 mm | m = 2 | m = 5 | m = 10 | m = 20 |
|---|---|---|---|---|
| IK long | +11.2, 1/55 | +4.1, 1/91 | +2.1, 1/161 | +1.0, 1/306 |
| KL long | −13.0, 1/45 | −4.3, 1/88 | −2.1, 1/161 | −1.0, 1/306 |
| KN long | +2.9, 1/208 | +0.17, 1/2251 | +0.02 | 0.00 |
| All three long | +0.06, 1/9277 | +0.02 | +0.01 | 0.00 |
| L above the line | −12.9, 1/45 | −4.1, 1/90 | −1.8, 1/183 | −0.25, 1/1259 |
| I above the line | +11.1, 1/56 | +4.0, 1/94 | +1.8, 1/185 | +0.25, 1/1260 |
| N above the line (floor) | +2.9, 1/210 | +0.16, 1/2327 | +0.02 | 0.00 |
| I along the axis | +1.34, 1/451 | +1.04, 1/360 | +1.01, 1/330 | +1.00, 1/315 |
| L along the axis | −1.00, 1/599 | −1.00, 1/375 | −1.00, 1/333 | −1.00, 1/316 |
| N along the axis | −0.33, 1/1809 | −0.04, 1/9013 | −0.01 | 0.00 |
| Lens f 1% long (not a 1 mm fault) | 1/135 | 1/168 | 1/184 | 1/192 |

- Worst are the faults that break C6 or C5: KL against the equal pair, and I or L off the line. They are multiplied by about 2·IK/(f(m − 1/m)): 14 at m = 2, 4 at m = 5, 1 at m = 20.
- Axial faults of I and L pass one for one.
- Faults of N are divided by m² − 1.
- A common stretch of all three rods nearly cancels.
- Everything worsens toward small images and diverges at m = 1.
- With KL made equal to IK the blur is 1/7 of the width at m = 2 and 1/42 at m = 20.

**5. Brewster's objections and his cam (weigh.py)**
- Bending, at short throws: a deal lath 30 × 12 mm on edge, 1.55 m long, sags 0.5 mm under its own weight and shortens 0.0005 mm; its Euler load is 177 N against a few newtons of slide friction. The objection is empty here.
- Bending, at long throws: at 3.1 m (throw 6.3 m) the lath sags 8.6 mm, shortens 0.06 mm, Euler load 44 N: still passable. At 6.2 m (throw 12.5 m) it sags 138 mm, shortens 8 mm, Euler load 11 N: it fails without trussing. A 6 mm iron rod fails already at 3.1 m (sag 212 mm).
- So "bend by the least strain" holds only beyond about 6 m of throw.
- Short distances only: true, but for another reason first. The throw is at most about 2·IK, and K stands nearly IK above the pivots when the lantern is close: 1.5 m for a 3.3 m throw, 3.1 m for 6.3 m.
- Clumsy: fair. As drawn the rods cross the light cone and the space between lantern and screen; they would have to be set to one side.
- Cam, travel: m = 2 to 20 needs 2632 mm, which is 5.6 turns of a 150 mm wheel. A cam on the axle itself serves less than one turn (471 mm), so it needs about 6:1 gearing or a scroll.
- Cam, lift: 67.5 mm in all, of which the last 7.5 mm serves m = 10 to 20.
- Cam, errors: profile error passes one for one, with no multiplication. Wheel slip of 0.5% of the travel (13 mm) gives a lens error of 4.4 mm at m = 2 (blur 1/137), 0.55 mm at m = 5 (1/680), 0.13 mm at m = 10. Slip accumulates until the cam is re-zeroed.
- What the cam cannot do: know where the screen is (it reckons from the wheels; the rods are tied to the screen); be made without computing and cutting a curve; serve a new lens without a new cam.
- What the rods cannot do: long throws and low rooms; leave the stage clear; follow any law but a constant product (a cam could take the lens's real behaviour, or drive the shade); escape the multiplication of their errors at small sizes.
- Neither passes m = 1.

**6. The shade**
- Screen brightness goes as 1/v² (evenly lit slide) or 1/m² (all the light through the lens). From m = 20 to m = 2 that is 49 or 100 times.
- For constant brightness the open part of the lens must fall to 27% at m = 10, 8% at m = 5 and 2% (or 1%) at m = 2; less still for "fainter".
- A shade at the lens dims the whole picture evenly, so the place is right. Stopping down also sharpens the small images, where the rods are worst: 2% of the area cuts blur about 7 times.
- The law is the difficulty. The opening must go as (1 + f/x)², x being the lens's distance beyond focus: steep in the first 7.5 mm of travel and flat after. A plain fall with a triangular notch does not give that; only a cut profile would.
- If the condensers bring the lamp's image to the lens, as his Fig. 400 caption says ("focus is near the magnifying lens"), the light fills only the middle of the lens. A notch that uncovers "the middle of the lens only" then dims little until it bites the flame's image, and then unevenly.
- Verdict: rough dimming, yes; a true law, no. Brewster's "many disadvantages" is unargued.

**7. Web**
Searches (seven), in substance:
- Young 1807 phantasmagoria rods linkage Peaucellier inversor Newton lens formula
- autofocus linkage inversor xx' = f² enlarger Peaucellier Young Fig. 401
- Young phantasmagoria levers inversor anticipates
- autofocus enlarger inversor Peaucellier Newton's equation history
- Young phantasmagoria "always distinctly" / automatic focusing, Brewster
- history of autofocus inversor Carpentier / magic lantern / Young
- Young Lectures phantasmagoria inversor Peaucellier autofocus Becker

Findings:
- I found nothing that discusses whether Young's arrangement is exact, and nothing that ties it to a later mechanism.
- Closest later mechanism: J. Becker, US patent 1,103,343 (granted 1914, filed 1910, priority 1905), automatically focused enlarging cameras, https://patents.google.com/patent/US1103343. As the fetch tool reported it: "two equal links 20 and 21 and a shorter link 22"; "the difference of their squares shall be equal to the square of the focal length"; pivot axes in a plane parallel with the motion; it cites Newton's Opticks; it says the linkage "comprises six of the seven links used in Peaucellier's beam"; it names no Young. That is Young's arrangement with C5 and C6 supplied. I read the tool's summary, not the patent text.
- Related Becker patents turned up but were not opened: US895968, US1103342.
- A 1955 Photogrammetric Engineering paper on a rack-and-pinion inversor (search snippet only; the address gave 404): the inversor "as an autofocus", listing "Pythagorean right-angle, Carpentier, Paucellier" kinds. https://asprs.org/wp-content/uploads/pers/1955journal/mar/1955_mar_127-131.pdf
- Peaucellier 1864, Lipkin 1871: https://en.wikipedia.org/wiki/Peaucellier%E2%80%93Lipkin_linkage
- My own reading, not found in print: Young's three rods are half a Peaucellier cell with the pole L inside, the slides doing the work of the other half, 57 years earlier.

**Not done**
- Brewster's Fig. 6 was looked at but not measured; I and L seem drawn almost at one point there.
- The dashed rays of the plate were not fitted, so the object and image planes rest on my choice of faces (alternatives given in 3).
- The patent and the 1955 paper were not read in the original.
- No faults out of the plane (rods to one side, pivot play, a track not straight) were simulated.
- The bending figures are for the rod's own weight when horizontal, not a full load case of the linkage.
- The shade's law was not modelled beyond the required opening.
- No search of Young's vol. 2 catalogue or of later lantern manuals.

Files are in /home/agent2/lantern-referee/:
- crop.py
- measure.py
- faults.py
- asdrawn.py
- weigh.py
- zA.png, zB.png, zC.png, zD.png (gridded crops)
- fig401_x2.png
- plate_small.png
