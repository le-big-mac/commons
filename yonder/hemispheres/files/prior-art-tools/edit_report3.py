"""usage: python -I edit_report3.py REPORT.md   -- third list of exact replacements, each must match once."""
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
R = [
("10. \"Sources\".\n    Old: `the population map is Bill Rankin's, as described at brilliantmaps.com/human-hemisphere`\n    New: `the population maps are Bill Rankin's \"Human Hemisphere\" and \"Your Hemisphere\" (2015), radicalcartography.net/human-hemisphere.html and radicalcartography.net/your-hemisphere.html, which I first knew from the description at brilliantmaps.com/human-hemisphere`",
 "10. \"Sources\" (in the README the address is in code marks, left out here).\n    Old text: the population map is Bill Rankin's, as described at brilliantmaps.com/human-hemisphere\n    New text: the population maps are Bill Rankin's \"Human Hemisphere\" and \"Your Hemisphere\" (2015), radicalcartography.net/human-hemisphere.html and radicalcartography.net/your-hemisphere.html, which I first knew from the description at brilliantmaps.com/human-hemisphere"),
("`places.py`, `edit_report.py`, `edit_report2.py`, `check_old_texts.py`);",
 "`places.py`, `check_old_texts.py`, and three `edit_report` scripts that record the corrections I made to this report while checking it);"),
]
for old, new in R:
    n = s.count(old)
    if n != 1:
        print("NOT APPLIED (matches: %d): %s" % (n, old[:70]))
        continue
    s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
print("done")
