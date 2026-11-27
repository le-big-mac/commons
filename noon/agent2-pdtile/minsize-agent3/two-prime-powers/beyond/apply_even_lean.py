"""Adds to the note beyond up-sets (with its sections 7 to 14) a dated section 15: the lemma on signs for every n, in
Lean (fourteen statements; 27 November 2026); and one entry in the list of files.
usage: apply_even_lean.py ADDED-AT READ-FILE < note-with-section-14 > candidate
The section's text is even-lean-section.md beside this script, with @@TIME@@ (the time it was added) and @@READ@@ (the
sentence, in italics under the heading, on how the section was read; from READ-FILE).  The sentence on where the files
are and on Noon's reading is part of the section's text and changes there when Noon has read them."""
import sys, os
s = sys.stdin.read(); when = sys.argv[1]; read = open(sys.argv[2]).read().strip()
sec = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'even-lean-section.md'), encoding='utf-8').read().strip()
assert sec.count('@@TIME@@') == 1 and sec.count('@@READ@@') == 1 and sec.count('@@') == 4
sec = sec.replace('@@TIME@@', when).replace('@@READ@@', read)
assert "## 15. " not in s
a = "\n## Files\n"
assert s.count(a) == 1
s = s.replace(a, "\n" + sec + "\n" + a)
k = s.index(" · section 14: `lean-lift/even/`"); e = s.find(" · ", k + 5); e = e if e > 0 else s.find("\n", k)
entry = (" · section 15: `lean-lift/even-lean/` (its `README.md` first: the eight Lean files, the fourteen statements as fixed before proof with their hashes, the plan and the briefs, "
         "the reports of the instance that wrote the statements and of the seven provers, my check's log and script, the audit of the statements with its programs in `audit/`, "
         "the reading of this section and of that front page, my sealed sheets and their scoring)")
s = s[:e] + entry + s[e:]
sys.stdout.write(s)
