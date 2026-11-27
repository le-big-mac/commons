"""Adds to the note beyond up-sets (with its sections 7 to 15) a dated section 16: "twice" for the whole of Z_n, on paper and in
Lean (two statements), the shares for few elements, a correction to section 14 (27 November 2026); and one entry in the list of files.
usage: apply_union.py ADDED-AT READ-FILE < note-with-section-15 > candidate
The section's text is union-section.md beside this script, with @@TIME@@ (the time it was added) and @@READ@@ (the
sentence, in italics under the heading, on how the section was read; from READ-FILE).  """
import sys, os
s = sys.stdin.read(); when = sys.argv[1]; read = open(sys.argv[2]).read().strip()
sec = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'union-section.md'), encoding='utf-8').read().strip()
assert sec.count('@@TIME@@') == 1 and sec.count('@@READ@@') == 1 and sec.count('@@') == 4
sec = sec.replace('@@TIME@@', when).replace('@@READ@@', read)
assert "## 16. " not in s and "## 15. " in s
a = "\n## Files\n"
assert s.count(a) == 1
s = s.replace(a, "\n" + sec + "\n" + a)
k = s.index(" · section 15: `lean-lift/even-lean/`"); e = s.find(" · ", k + 5); e = e if e > 0 else s.find("\n", k)
entry = (" · section 16: `lean-lift/even/third/union-twice.md` (the note, with its referee's three reports beside it and the referee's programs in `referee-union/`), "
         "`lean-lift/even/shares/` (my programs and their outputs), `lean-lift/even/scout-union-report.md` (the third search in print, without what it downloaded), "
         "and `lean-lift/union-lean/` (its `README.md` first: the two Lean files, the two statements as fixed before proof with their hashes, the briefs, the two provers' reports, "
         "my check's log and script, the audit of the statements with its programs in `audit/`, the reading of this section, my sealed sheets and their scoring)")
s = s[:e] + entry + s[e:]
sys.stdout.write(s)
