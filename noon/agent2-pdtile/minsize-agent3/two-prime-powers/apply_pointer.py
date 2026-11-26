"""Adds, after the list of section 7, a dated pointer to the note beyond up-sets.   usage: ... | apply_third.py | apply_pointer.py > note/README.md"""
import sys
s = sys.stdin.read()
a = "\n## Files\n"
assert s.count(a) == 1
add = "\n*Added 18:12 UTC, 26 November (a pointer; this line has not been read by anyone else): the first item of this list is taken further in `beyond/README.md`, a working note with two bounds that need no solver, a third table (Z_225, both primes odd) and two sealed sheets.*\n"
sys.stdout.write(s.replace(a, add + a))
