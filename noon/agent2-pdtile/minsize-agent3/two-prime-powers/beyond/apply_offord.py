"""Adds to the note beyond up-sets (with its sections 7 to 18) a dated section 19: the first statements about shares
in Lean, and Erdős's bound (28 November 2026); and one entry in the list of files.
usage: apply_offord.py ADDED-AT READ-FILE < note-with-section-18 > candidate
The section's text is offord-section.md beside this script, with @@TIME@@ (twice: the time it was added) and @@READ@@."""
import sys, os
s = sys.stdin.read(); when = sys.argv[1]; read = open(sys.argv[2], encoding='utf-8').read().strip()
sec = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'offord-section.md'), encoding='utf-8').read().strip()
assert sec.count("@@TIME@@") == 3 and sec.count("@@READ@@") == 1 and sec.count("@@") == 8, sec.count("@@")
sec = sec.replace('@@TIME@@', when).replace('@@READ@@', read)
assert "## 19. " not in s and "## 18. " in s
a = "\n## Files\n"
assert s.count(a) == 1
s = s.replace(a, "\n" + sec + "\n" + a)
k = s.index(" · section 18: `lean-lift/even/root/`"); e = s.find(" · ", k + 5); assert e > 0
entry = (" · section 19: `lean-lift/offord-lean/` (its `README.md` first: the two Lean files, the seven statements as fixed before any proof, hashes, my check log, "
         "the briefs, the provers' reports, the audit of the statements with its programs, my sealed sheet and its score)")
s = s[:e] + entry + s[e:]
sys.stdout.write(s)
