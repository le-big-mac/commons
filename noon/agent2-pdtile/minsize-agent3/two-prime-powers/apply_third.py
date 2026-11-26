"""The referee's third, short reading applied: reads the text that apply_second.py writes (stdin) and the third report as saved
(note/referee-3.md), makes each change in the referee's words, and writes the note (stdout).
usage: make_note2.py READ-FILE LEAN-FILE | apply_second.py | apply_third.py > note/README.md"""
import sys
s = sys.stdin.read()
t = open('note/referee-3.md').read(); r = t[t.index('## Report (the referee)'):]
Q = [l[2:] for l in r.split('\n') if l.startswith('> ')]
assert len(Q) == 2 and Q[0].startswith('(for one pattern of Z_36 and 68 of Z_100 the only programme') and Q[1].startswith('the size has to be a multiple of 2^a·5^b')
def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:90]); s = s.replace(old, new)
def between(a, b):
    i = r.index(a) + len(a); return r[i:r.index(b, i)]
# must 1
rep("(for one pattern of Z_36 and 68 of Z_100 on the word of the solver HiGHS alone, whose proofs that nothing smaller exists are in floating point)", Q[0])
# must 2
m2 = between('Replacement for "For one of them, {2, 5, 50},": "', '".'); assert m2 == 'For one more of the sixteen, {2, 5, 50},'
rep("For one of them, {2, 5, 50},", m2)
# must 3
rep("the size having to be a multiple of the prime powers that the pattern forces: no smaller admissible size has a multiset for {2, 4, 5, 100} (60), {2, 4, 5, 50, 100} (100) or {2, 5, 50, 100} (70) (`referee/second/out/sizes-*.jsonl`)", Q[1])
# must 4
m4 = between('which is 1 in most of these rows. Replacement: "', '"\n'); assert m4.startswith('In each of these 55 rows, in both tables, the multiset on file has exactly the size of that lower bound') and m4.endswith('on no solver.')
rep("In each of these 55 rows, in both tables, the multiset on file has exactly that size, so there the least size rests on the theorem and that multiset and on no solver.", m4)
# suggestion 5
s5a = between('which settles four more of Z_100 outside the tables. Write "', '", and after'); assert s5a == 'has been decided by a programme of the tables for 256 and 240'
s5b = between('after "25 minutes a pattern." add: "', '"\n'); assert s5b == 'Four more of Z_100 are settled outside the tables (section 4).'
rep("the least size is now known for 256 and 240", "the least size " + s5a)
rep("when I gave it 25 minutes a pattern.", "when I gave it 25 minutes a pattern. " + s5b)
# suggestion 6
s6 = between('After "rests on HiGHS alone" you may add: "', '". Source'); assert s6.startswith('(one size at a time') and s6.endswith('330 seconds)')
rep("rests on HiGHS alone.", "rests on HiGHS alone " + s6 + ".")
rep("`referee-2.md` (its second reading, of the changed text), `referee/`", "`referee-2.md` (its second reading, of the changed text), `referee-3.md` (its third, of the lines changed after the second; `changes-after-second.md` lists them), `referee/`")
sys.stdout.write(s)
