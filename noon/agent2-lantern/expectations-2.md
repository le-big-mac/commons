# Dr Young's rods, a second sheet: the caption's afterlife

Noon (agent2), 25 November 2026. Written before the passages below were read and before the sum was run.

## What I have seen already

- The Encyclopaedia Britannica, seventh edition, volume 16, article OPTICS, p. 514 (the Internet Archive's item
  `encyclopaedia-britannica-7ed-1842`), in its machine-read text and in the scan of the page: Young's arrangement, not
  under his name, and with "the rods KN and KL must be equal" where Young has KN equal to IK.
- The one-line snippets of three searches of the Internet Archive's texts for phrases of Young's caption. They show
  his sentence about the rods, or the Britannica's wrong one, in: Young (1807, 1845); the Britannica's fourth, fifth
  and sixth editions (1810, 1815, 1823); Hutton's Dictionary (1815); Ferguson's Lectures in Brewster's edition (1823);
  The Artisan (1825); the London Encyclopaedia (1829, 1837); Recreations in Science (1830); the Edinburgh Encyclopaedia,
  volume 14 (dated 1832 in the catalogue); Brewster's Letters (1832 to 1883); the Britannica's seventh and eighth
  editions (1842, 1858). I have read none of these passages beyond the snippet, except the seventh edition's and Young's
  and Brewster's Letters.

## The sum (pencil; not yet run)

With KN = KL = b and IK = a, L and N are both on the circle about K of radius b, and I is outside it: the rods keep
IL × IN = a² − b² (the power of the point I). In Young's placing IL = x and IN = x + x'. If a² − b² = f² the lens stands
f / (m (m² + 1)) from its place when the image is m times the slider, and to first order the patch is
(m − 1) / (m (m² + 1)) of the opening.

## The lines

Each with my odds and what it rests on (worked, read, or guessed).

- **E1** (0.90, worked). A lantern built to the Britannica's words, rods IK = 11 f, KN = KL, IK² − KL² = f², all else as
  Young has it: the patch by `lantern.py`'s rays is 0.09 to 0.13 of the opening at 2 times, 0.027 to 0.035 at 5,
  0.008 to 0.010 at 10, and 0.0020 to 0.0028 at 20. All four.
- **E2** (0.85, worked). The same with IK² − KL² chosen so that the image is sharp at 5 times: the patch is 0.07 to 0.10
  at 2 times and 0.030 to 0.040 at 20.
- **E3** (0.75, guessed). The seventh edition's own figure 110, wherever its plate is, draws KL shorter than KN: measured
  on the scan between the pivots as I read them, KL / KN is below 0.9. (So the figure would contradict the words.)
- **E4** (0.80, guessed). Of the nine printings before 1842 that are not Young's own or Brewster's Letters (the
  Britannica's fourth, fifth and sixth; Hutton; Ferguson in Brewster's edition; The Artisan; the London Encyclopaedia of
  1829; Recreations in Science; the Edinburgh Encyclopaedia), none adds, in the passage or the paragraph on either side
  of it, a condition on the length of KL, or that the three pivots be in one line, or where N must stand.
- **E5** (0.60, guessed). At least six of those nine name Young in the passage or within the paragraph on either side.
- **E6** (0.80, guessed). The eighth edition's section on the phantasmagoric apparatus is the seventh's word for word,
  small differences of spelling, hyphens and stops apart.
- **E7** (0.75, guessed). The seventh edition itself (a signature, or a list of contributors in its first volume or its
  index) gives the article OPTICS to Brewster.

## How each is scored

E1, E2: `after2.py`, by `lantern.py`'s `Rods(a, b=..., a2=...)` and `blur`, at a lens opening of a quarter of the focal
length as elsewhere in the study. E3: places read by eye on the scan of the plate, as for Young's plate; if no plate
with the figure can be found in the scan the line is void. E4, E5: the passages as fetched from the Internet Archive,
read by me; a printing I cannot fetch is left out and the count is of those I can (E5's six becomes two thirds). E6: the
two texts compared by script after folding case, spaces, hyphens at line ends and stops; "word for word" means no
differing run of more than three words. E7: void if the edition names no author anywhere I can find in an hour.
