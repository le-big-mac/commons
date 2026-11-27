"""Adds to the note beyond up-sets (with its sections 7 to 13) a dated section 14: the lemma on signs for every n, with
its exceptional pairs (27 November 2026); and one entry in the list of files.
usage: apply_even.py ADDED-AT READ-FILE < note-with-section-13 > candidate
The section's text is even-section.md beside this script, with @@TIME@@ (the time it was added) and @@READ@@ (the
sentence, in italics under the heading, on how the section was read; from READ-FILE)."""
import sys, os
s = sys.stdin.read(); when = sys.argv[1]; read = open(sys.argv[2]).read().strip()
sec = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'even-section.md'), encoding='utf-8').read().strip()
assert sec.count('@@TIME@@') == 1 and sec.count('@@READ@@') == 1
sec = sec.replace('@@TIME@@', when).replace('@@READ@@', read)
a = "\n## Files\n"
assert s.count(a) == 1
s = s.replace(a, "\n" + sec + "\n" + a)
k = s.index(" · section 13: `lean-lift/four-lean/`"); e = s.find(" · ", k + 5); e = e if e > 0 else s.find("\n", k)
entry = (" · section 14: `lean-lift/even/` (its `README.md` first: a table of what is where, in the order in which things happened; the proof is `third/theorem-twice.md`; "
         "the two instances' results `even-result.md` and `even-result-2.md`, each with its referee's reports and the programs of both; my lemma `third/lemma-rho.md` with its referee's reports; "
         "the two searches in print, without what they downloaded; my searches `explore.py` and `confirm.py` with their outputs; the sealed sheets and their scores)")
s = s[:e] + entry + s[e:]
sys.stdout.write(s)
