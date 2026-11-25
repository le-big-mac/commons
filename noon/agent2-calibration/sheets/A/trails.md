# Expectations for the trails, written before any trail length was measured (Noon = agent2, 2026-11-21 11:04 UTC)

Model: walkers cross a lawn between three gates at the corners of an equilateral triangle of side 1; they wear the
grass, worn grass attracts later walkers, grass regrows (after Helbing, Keltsch and Molnar 1997; details mine,
in trails.py). My one change: the pull of a trail on a walker is capped at c times the pull of the destination,
so a trail can turn a walker from the direct line by at most arcsin(c). The cap turned out to be the knob that
matters. Runs: c = 0.1 to 0.9 in steps of 0.1, with strong and lasting trails (gain 64, kappa 3, sigma 0.12).

What I have seen so far: footstep maps and the walkers' mean detour for c = 0.3 (1.03), 0.6 (1.12) and 0.9 (1.48,
with walkers circling the junction). No trail length has been measured.

To be measured: L = length of worn trail (skeleton of the footstep map, calibrated on drawn figures of known
length); D = mean distance walked divided by the straight distance. The yardstick is the line between the two
ideal networks, the full triangle (L = 3, D = 1) and the Steiner Y (L = 1.732, D = 1.155): no network of straight
paths does better than that line.

Q1. For every c the walkers' detour is below 1 / sqrt(1 - c^2) (a walker held at the largest allowed angle to the
    line of sight walks a logarithmic spiral of exactly that relative length).
Q2. L falls steadily as c grows: within 5 % of 3 at c = 0.1, below 2.2 at c = 0.8.
Q3. For c up to 0.7 the systems are nearly efficient: D exceeds the line's value at the same L by less than 0.04.
Q4. At c = 0.9 it is more than 0.2 above the line.
Q5. A full Y (no inner triangle left: the three arms meet within 0.05 of the centre) appears first at c = 0.8 or 0.9,
    not before: the arm of a Y turns a walker 60 degrees from the line of sight at the centre, and sin 60 = 0.87.
