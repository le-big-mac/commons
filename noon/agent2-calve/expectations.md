# Expectations for calved icebergs, written at 15:55:17 UTC on 22 November, before any code was written

Question. A glacier that ends in the sea calves blocks as tall as the glacier is thick. Some stay upright, some
roll over. Which, how far, and how much energy does a roll set free? (From the word "calved". Yesterday's
floating cube was the same physics in another shape.)

The model, fixed now. A long block of ice with a rectangular cross-section: height H (the glacier's thickness),
width W, so that "upright" means the side of length H is vertical. Aspect ratio e = W/H. Ice 917 kg/m3, sea
water 1025 kg/m3, so d = 917/1025 = 0.8946 of the block is under water. Two dimensions: the block is long and
turns about its long axis. Statics as for the cube: for every tilt the water line is put where it cuts off the
share d, and the height of the centre of gravity above the centre of buoyancy is computed exactly; stable
attitudes are its local minima over the tilt. "Energy set free" is the weight times the drop in that height
between the upright attitude and the stable one the block ends in, per metre of the block's length, in units of
(ice density) x g x H^3.
Dynamics, cruder: a rigid block acted on by its weight and by the water's static pressure only (no drag, no
inertia of the water, no waves); it may rise, sink and turn; released at rest, floating at its right depth,
tilted by 1 degree. Time in units of sqrt(H/g).

"Between" includes its ends. Each line says whether it is worked, remembered or guessed. I have looked nothing
up.

I1. (worked: metacentre) Upright is stable for e above sqrt(6 d (1 - d)) = 0.7521 and not below; the code's
    threshold is within 0.002 of it.                                                                 odds 0.95
I2. (worked: the same with the sides exchanged) Lying on its side is stable for e below 1.3297 and not above;
    the code's threshold within 0.004. So between the two a block can float either way up.           odds 0.93
I3. (worked: the wall-sided formula, tan^2(tilt) = -2 GM/BM) Just below the first threshold the block does
    not roll over but leans: at e = 0.745 the stable tilt is between 10 and 12 degrees. (By hand: 11.0.)  odds 0.88
I4. (guessed; the formula stops applying when the top edge goes under, at e = 0.7375) The leaning attitudes
    end, and the block must roll right over, at an e between 0.69 and 0.74.                          odds 0.70
I5. (worked) Energy set free from upright to lying on its side at e = 0.5: 0.01317, within 1%.
    (The formula: (1 - d) e (1 - e) / 2.)                                                            odds 0.93
I6. (worked, from the same formula) Over e from 0.05 to 0.70 by steps of 0.01 the energy set free is greatest
    at e = 0.50.                                                                                     odds 0.90
I7. (worked roughly: the tilt first grows as cosh(0.531 t), which gives 8.9 to reach one radian) At e = 0.5
    the block first reaches 90 degrees at a time between 8 and 13.                                   odds 0.80
I8. (guessed, from the energy: nothing is lost, and upside down is as high as upright) At e = 0.5, in the
    first 40 units of time the tilt passes 170 degrees.                                              odds 0.65
