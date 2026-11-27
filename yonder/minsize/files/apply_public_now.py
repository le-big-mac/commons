"""The clock page, one sentence: Noon's public copy now holds the two Lean files for marks without repeats
(commit 5817546 of the public repository, 27 November), and the folder lean-lift/sets-lean/ is public too.
usage: python apply_public_now.py < README.md > README.candidate-public-now.md"""
import sys
t = sys.stdin.read()
old = ("were added to it on 27 November; its public copy will hold them once Noon has pushed that folder again. They are also kept, with the statements as first written, "
       "the record of my check and the audit, with the second working note, in its folder `lean-lift/sets-lean/`, which becomes public in the same way.")
new = ("were added to it on 27 November, and its public copy holds them too. They are also kept, with the statements as first written, "
       "the record of my check and the audit, with the second working note, in its folder `lean-lift/sets-lean/`, which is public as well.")
assert t.count(old) == 1, t.count(old)
sys.stdout.write(t.replace(old, new))
