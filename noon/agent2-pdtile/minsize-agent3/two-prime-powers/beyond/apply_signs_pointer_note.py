"""Adds to the note beyond up-sets (with its sections 7 to 18) a pointer, under its title, to the one page of statements
about signs that is posted beside it, and an entry in the list of files.
usage: apply_signs_pointer_note.py ADDED-AT < note > candidate"""
import sys
s = sys.stdin.read(); when = sys.argv[1]
lines = s.split('\n')
assert lines[0].startswith('# Beyond up-sets') and lines[1] == '' and lines[2].startswith('*agent3 (Yonder), 26 November 2026.')
ptr = (f"*Added {when}: the statements about signs of section 7 and sections 9 to 18 are gathered on one page, `signs-where-it-stands.md` beside this file: "
       "the four statements with their status (in Lean, or on paper and refereed), what is open, what is in print, and whose each piece is. It is a short form of those sections and has no result that is not in them.*")
lines[1:1] = ['', ptr]
s = '\n'.join(lines)
k = s.index(" · section 18: `lean-lift/even/root/`"); e = s.find(" · ", k + 5); assert e > 0
entry = " · the statements about signs on one page: `signs-where-it-stands.md` (read twice by a fresh instance, alone and against section 7, sections 9 to 18 and the Lean statements: `signs-reading/`)"
s = s[:e] + entry + s[e:]
sys.stdout.write(s)
