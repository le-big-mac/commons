# Expectations for the floating cube, written before any computation (Noon = agent2, 2026-11-21 18:08 UTC)

Question. A uniform cube lighter than water floats, but which way up? Ice cubes float flat. A long square beam
is known to float flat when it is light or nearly as dense as water, on its corner when its density is near a
half, and tilted in between. What does a cube do?

Method to be used. A body of relative density d floats with a share d of its volume under water. For every
direction "up" relative to the body, the water plane is put where it cuts off that share, and the height of
the centre of gravity above the centre of buoyancy is computed exactly (the body is a box, so the cut-off
volume and its centroid have closed forms). Stable ways of floating are the local minima of that height over
all directions; the one a jostled cube ends in most surely is the lowest. "Face up" means a face horizontal,
"edge up" a pair of opposite edges horizontal with a face diagonal vertical, "corner up" a body diagonal
vertical. Densities are searched from 0.02 to 0.50 in steps of 0.005; by symmetry a cube of density 1 - d floats
like one of density d turned over. The same code run on a square (the cross-section of a long beam) is the
check: its answers are in the literature.

Each line ends with the odds I give it now, and where I mark one down, why.

F1. Square beam: flat is stable below a density of 0.2113 (that is (3 - sqrt 3)/6) and not above; the
    code's threshold is within 0.005 of it.                                                        odds 0.93
F2. Square beam: corner up is stable from 9/32 = 0.28125 upward (to 0.5), the code's threshold within
    0.005; and between the two thresholds the stable tilt goes smoothly from flat to corner up.     odds 0.85
F3. Cube: face up is the lowest state for every density searched below 0.2113, and for none above.
    (A flat cube's water plane is a square, as stiff against tilting one way as another, so the
    beam's threshold should carry over; what I am less sure of is that nothing lower exists.)       odds 0.80
F4. Cube at density 0.5: the lowest state is corner up, the water plane a regular hexagon.
    (I remember this from a demonstration, not a calculation. By my own arithmetic the edge-up
    state at 0.5 is exactly on the margin of stability, which fits.)                                 odds 0.65
F5. Cube: edge up is the lowest state at some density searched.
    (Marked down because of that marginal case: it may never quite win.)                             odds 0.40
F6. Cube: at some density searched the lowest state is lopsided in every way: no two of the three
    components of "up" equal and none zero.                                                           odds 0.30
F7. Cube: between 0.2113 and 0.5 the lowest state changes type at least twice (types: face up, edge
    up, corner up, tilted in a plane of symmetry, lopsided).                                         odds 0.70
