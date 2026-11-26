"""usage: python -I edit_report2.py REPORT.md   -- second list of exact replacements, each must match once."""
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
R = [
("which the README gives as its own (28.6° N, 100.5° E), was published by Rudy Arthur in 2023–24 (28.375° N, 100.625° E).",
 "which the README reports with no credit for the place (28.6° N, 100.5° E), was published by Rudy Arthur in 2023–24 (28.375° N, 100.625° E)."),
("On Rankin's \"Your Hemisphere\" map a thin, unlabelled contour (the 92% line, by his text) encloses a band running north-east from the south-east of France through Germany to southern Sweden and Finland.",
 "On Rankin's \"Your Hemisphere\" map a thin, unlabelled contour (I take it for the 92% line, from his text and the spacing of the lines) encloses a band running north-east from the south-east of France through Germany to southern Sweden and Finland, as I read the picture."),
("I read the abstract on the University of Amsterdam's repository; it maps \"broad-scale woodpecker species richness\" worldwide from ranges.",
 "I read the abstract on the University of Amsterdam's repository; it relates \"broad-scale woodpecker species richness\" across the world to tree cover and climate."),
("Annales Zoologici Fennici 43 (2006) 86–95.** Not obtained",
 "Annales Zoologici Fennici 43 (2006), from page 86.** Not obtained"),
("**How the study differs.** The published maps count species per place from range maps.",
 "**How the study differs.** The published work counts species per place (from range maps, as I understand it; I read only an abstract)."),
("I did not find the remark made in biogeography, about woodpeckers or about any hemisphere of species; one search, and the papers it returned on the Malay Archipelago do not make it.",
 "I did not find the remark made in biogeography, about woodpeckers or about any hemisphere of species: one search, whose summary reported no source that makes it."),
("and treats the centre as a correction of the one it remembered from Danny Quah.",
 "and sets it against the centre it remembered from Danny Quah, 770 km away."),
("**Wrong, or more than the tables show.** Old text, then new text.",
 "**Wrong, or more than the tables show.** Old text, then new text. The README's lines are wrapped; an old text is given here with a space where the README has a line end."),
]
for old, new in R:
    n = s.count(old)
    if n != 1:
        print("NOT APPLIED (matches: %d): %s" % (n, old[:70]))
        continue
    s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
print("done")
