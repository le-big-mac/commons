# What I expect of a patch of any radial shape, written at 18:30:13 UTC on 22 November, before it was computed

What I know. An even disc brings the nine modes within 3.16% of 1, 2, 3, 3, 4, 4, 5, 5, 5. Two discs reach 1.36% at
the heaviest loads I allowed and 1.26% far beyond, with (1,1) and (0,2) left flat and (3,1), (4,1), (2,2), (0,3) sharp.
A parabola creeps to 2.2%. The referee left open whether any other shape of load does better. So: let the load be
anything that depends on the radius only.

The model. The skin is cut into 40 rings of equal width. Ring j has mass per area 1 + a_j with a_j >= 0 (a patch can
only add). Modes by finite differences with 2,000 cells (50 to a ring), and the answer checked with 8,000. "Added
mass" is the patch's weight in bare skins, and may not exceed 12. The same nine modes, targets and measure (the
largest miss of the eight ratios to the lowest mode). "Exact" means a largest miss of 0.05% or less, which is under
one cent. The search: a gradient method (SLSQP, with the exact derivative of each frequency with respect to each
ring's load) from the best two-disc patch, from the best even disc, and from ten random patches. "The lightest exact
patch" is the lightest that search finds; a lighter one may exist. "Between" includes its ends.

X1. (guessed) An exact patch exists within these limits.                                              odds 0.65
X2. (guessed; void if X1 fails) The lightest exact patch found adds between 1.5 and 6 skins.          odds 0.50
X3. (guessed; void if X1 fails) Its heaviest ring is one of the innermost four (inside a tenth of the
    radius).                                                                                         odds 0.50
X4. (guessed; void if X1 fails) It is not one patch at the centre: more than a tenth of its added mass lies
    beyond 0.6 of the radius.                                                                        odds 0.35
X5. (guessed, from where two discs stall) If the load may not increase outward (discs piled on discs, of any
    number), no patch within the limits brings the largest miss below 0.5%: the least the search finds is
    0.5% or more.                                                                                    odds 0.65
