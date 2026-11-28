"""Adds to the note beyond up-sets (with its sections 7 to 16) a dated section 17: at least a quarter of the signings are good (Theorem Q on odd moduli, by three instances;
28 November 2026); and one entry in the list of files.
usage: apply_quarter.py ADDED-AT READ-FILE < note-with-section-16 > candidate
The section's text is quarter-section.md beside this script, with @@TIME@@ (the time it was added) and @@READ@@ (the
sentence, in italics under the heading, on how the section was read; from READ-FILE).  """
import sys, os
s = sys.stdin.read(); when = sys.argv[1]; read = open(sys.argv[2]).read().strip()
sec = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quarter-section.md'), encoding='utf-8').read().strip()
assert sec.count('@@TIME@@') == 1 and sec.count('@@READ@@') == 1 and sec.count('@@') == 4
sec = sec.replace('@@TIME@@', when).replace('@@READ@@', read)
assert "## 17. " not in s and "## 16. " in s
a = "\n## Files\n"
assert s.count(a) == 1
s = s.replace(a, "\n" + sec + "\n" + a)
k = s.index(" · section 16: `lean-lift/even/third/union-twice.md`"); e = s.find(" · ", k + 5); e = e if e > 0 else s.find("\n", k)
entry = (" · section 17: `lean-lift/even/quarter/` (my brief `brief-quarter.md`; the three instances' texts `one/result.md`, `two/result.md`, `three/result.md`, each with its programs and outputs beside it, "
         "as sent to its referee and with what changed after; the three referees' reports `report-referee-*.md` and their programs in `referee-*/`; my sealed sheets and their scores), "
         "`lean-lift/even/scout-quarter-report.md` (the fourth search in print, without what it downloaded), and my runs in `lean-lift/even/shares/`")
s = s[:e] + entry + s[e:]
sys.stdout.write(s)
