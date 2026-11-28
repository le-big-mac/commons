"""Adds to the note beyond up-sets (with its sections 7 to 17) a dated section 18: the share of bad signings falls like a
constant over the square root of the number of elements (Theorem R on odd moduli, by two instances, with a part by a
third; 28 November 2026); and one entry in the list of files.
usage: apply_root.py ADDED-AT READ-FILE < note-with-section-17 > candidate
The section's text is root-section.md beside this script, with @@TIME@@ (the time it was added) and @@READ@@ (the
sentence, in italics under the heading, on how the section was read; from READ-FILE).  """
import sys, os
s = sys.stdin.read(); when = sys.argv[1]; read = open(sys.argv[2], encoding='utf-8').read().strip()
sec = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'root-section.md'), encoding='utf-8').read().strip()
assert sec.count('@@TIME@@') == 1 and sec.count('@@READ@@') == 1 and sec.count('@@') == 4, sec.count('@@')
sec = sec.replace('@@TIME@@', when).replace('@@READ@@', read)
assert "## 18. " not in s and "## 17. " in s
a = "\n## Files\n"
assert s.count(a) == 1
s = s.replace(a, "\n" + sec + "\n" + a)
k = s.index(" · section 17: `lean-lift/even/quarter/`"); e = s.find(" · ", k + 5); e = e if e > 0 else s.find("\n", k)
entry = (" · section 18: `lean-lift/even/root/` (my brief `brief-root.md`; the three instances' texts `one/result.md`, `two/result.md`, `three/result.md`, each with its programs and outputs beside it, "
         "as sent to its referee and with what changed after; the three referees' reports `report-referee-*.md`, their second looks and their programs in `referee-*/`; my sealed sheets and their scores), "
         "`lean-lift/even/asym/` (my counts for one heavy element), and `lean-lift/even/scout-root-report.md` (the fifth search in print, without what it downloaded)")
s = s[:e] + entry + s[e:]
sys.stdout.write(s)
