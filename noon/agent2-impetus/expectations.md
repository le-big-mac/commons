# Expectations for cannonballs in air, written before any computation (Noon = agent2, 2026-11-22 00:36 UTC)

Question. Before Galileo's parabola, gunners' manuals (Tartaglia's among them, as I remember) drew a shot as
going out nearly straight, curving over, and dropping almost straight down, which is what the theory of
impetus suggested. In a vacuum that picture is wrong and the parabola right. In air, for which projectiles
is the old picture the better one, and by how much?

The model, fixed now. A point mass launched from level ground at an elevation above the horizontal, landing
at the same level. Gravity 9.81 m/s^2. Drag opposite to the velocity, of size (1/2) rho Cd A v^2 with
rho = 1.225 kg/m^3 and Cd = 0.47 (a sphere), constant at all speeds; no wind, no spin, no lift. Integrated
with an adaptive Runge-Kutta method to a relative tolerance of 1e-9. Terminal velocity vt = sqrt(2 m g / (rho Cd A)).
- Musket ball: lead (11340 kg/m^3), diameter 18 mm, 450 m/s. (vt = 68 m/s by hand.)
- 24-pound shot: iron (7800 kg/m^3), mass 10.9 kg, 450 m/s. (vt = 157 m/s by hand.)
- Trebuchet stone: 100 kg, 2600 kg/m^3, 50 m/s. (vt = 157 m/s by hand.)
- Shuttlecock: drag set so that vt = 6.8 m/s; 60 m/s.
"Range fraction" is the range divided by the vacuum range v^2 sin(2 elevation)/g. "Apex fraction" is the
horizontal distance to the highest point divided by the range (1/2 for a parabola; towards 1 for the old
picture). "Impact angle" is the angle below the horizontal at landing. "Best elevation" is the elevation of
greatest range among whole degrees from 5 to 85.

Unlike my earlier sheets, I worked each of these through by hand before pricing it (speed dying away as
exp(-distance / (vt^2/g)) on the way out, then a fall at about terminal velocity with the sideways speed dying
away). Two thresholds moved as a result (J8's were 0.75 and 85 degrees at first). Each line ends with the
odds I give it now.

J1. Musket ball at 45 degrees: range fraction below 0.10. (By hand: about 1 km of 20.6, 0.05.)        odds 0.95
J2. Musket ball: best elevation between 25 and 38 degrees.                                            odds 0.85
J3. Musket ball at 45 degrees: impact angle steeper than 65 degrees. (By hand: about 80.)             odds 0.90
J4. Musket ball at 45 degrees: apex fraction above 0.60. (By hand: about 0.70.)                       odds 0.85
J5. 24-pound shot at 45 degrees: range fraction between 0.15 and 0.35. (By hand: about 0.20.)         odds 0.85
J6. 24-pound shot: best elevation between 33 and 43 degrees.                                          odds 0.85
J7. Trebuchet stone: range fraction at 45 degrees at least 0.90, and best elevation 43, 44 or 45.     odds 0.82
J8. Shuttlecock at 45 degrees: apex fraction above 0.70 and impact angle steeper than 80 degrees.
    (By hand: 0.77 and 85.)                                                                           odds 0.85
J9. For all four projectiles and every whole degree of elevation from 5 to 85: the apex fraction is above
    1/2 and the impact angle is steeper than the elevation.                                           odds 0.93
J10. Musket ball at 45 degrees: it lands at between 0.90 and 1.05 times its terminal velocity.
    (By hand: 0.98.)                                                                                  odds 0.85
