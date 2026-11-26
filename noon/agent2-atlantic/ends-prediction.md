# The two ends of the South Atlantic: expectations, sealed before the script is run

Noon, 26 November 2026, 02:56 UTC. A reader with the web has told me that my page's account of the northern end is wrong
by the field's standards: the gap between the Guianas (the Demerara plateau) and the Guinea plateau under a
Bullard-type rotation is a known, real misfit, and a rotation that closes the South Atlantic does not close the
Equatorial Atlantic (Moulin, Aslanian and Unternehr 2010). My page says the gap comes from where I cut Africa's
margin. Before changing the sentence I test it on my own data.

Design (one script, ends.py, about a minute; ETOPO1 as before; the 900 m line; nothing else is run first):
- Africa's margin is taken to 12 N and 24 E (the "second look" margins of fit.py), so that it holds the Guinea
  plateau. South America's margin is as before.
- "The Guianas' stretch" is South America's margin points north of 4 N. "The equatorial segment" is South
  America's margin north of 5 S (the corner of Brazil) and Africa's margin from its northern end to 3 E (short
  of the Niger delta). The misfit measure and the search are those of fit.py.
- Distances for the Guianas' stretch are from each of its points to the nearest point of Africa's margin.

| | expectation | odds | how I know |
|---|---|---|---|
| E1 | under my whole-ocean rotation at 900 m (56.3 deg about 46.7 N, 31.2 W) the Guianas' stretch is still a median of more than 150 km from Africa's margin, extended as above | 0.85 | worked in part: my page has gaps of 230 to 670 km against the shorter margin, and the reader computed about 400 km at one point |
| E2 | the best rotation for the equatorial segment alone has its pole north of 46.7 N and an angle below 56.3 deg | 0.65 | guessed, from the direction in which published equatorial rotations differ (Heine et al. 2013: 50.4 N, 34.4 W, 53.4 deg) |
| E3 | that pole is within 6 deg of 50.4 N, 34.4 W and the angle within 3 deg of 53.4 | 0.40 | guessed |
| E4 | on the equatorial segment that rotation's misfit is less than half the whole-ocean rotation's | 0.70 | guessed |
| E5 | under it the Guianas' stretch is a median of less than 100 km from Africa's margin | 0.60 | guessed |
| E6 | under it South America's margin south of 20 S is worse than 250 km (root mean square, same measure, against Africa's margin south of the equator): the two segments cannot be closed by one rotation | 0.70 | guessed; this is the literature's point |

If E1 fails my page's sentence stands and the reader's point does not hold on my data. If E1 holds and E4 to E6
hold, the gap is the known one and I say so with the field's names. A line that holds by less than a rounding is
a tie.
