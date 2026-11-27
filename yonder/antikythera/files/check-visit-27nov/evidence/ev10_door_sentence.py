"""The plain page on clocks, one sentence: does the candidate differ from the public text in that sentence only,
and are its two facts true of the public repository as fetched (no network: the clone's origin/main)?
usage: python ev10_door_sentence.py README.md README.candidate-public-now.md CLONE
Prints; writes nothing."""
import difflib
import subprocess
import sys

a, b = (open(p, encoding='utf-8').read() for p in sys.argv[1:3])
clone = sys.argv[3]
sm = difflib.SequenceMatcher(None, a.split(' '), b.split(' '), autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
print('lines that differ:', sum(x != y for x, y in zip(a.split('\n'), b.split('\n'))), 'of', len(a.split('\n')), '(same number of lines:', len(a.split('\n')) == len(b.split('\n')), ')')
for tag, i1, i2, j1, j2 in ops:
    print(f'  {tag}: PUBLIC[{" ".join(a.split(" ")[i1:i2])}]\n  {" " * len(tag)}  CANDIDATE[{" ".join(b.split(" ")[j1:j2])}]')
old = ("were added to it on 27 November; its public copy will hold them once Noon has pushed that folder again. They are also kept, with the statements as first written, "
       "the record of my check and the audit, with the second working note, in its folder `lean-lift/sets-lean/`, which becomes public in the same way.")
new = ("were added to it on 27 November, and its public copy holds them too. They are also kept, with the statements as first written, "
       "the record of my check and the audit, with the second working note, in its folder `lean-lift/sets-lean/`, which is public as well.")
print('the candidate is the public text with that one passage replaced, and nothing else:', a.count(old) == 1 and a.replace(old, new) == b)


def git(*args):
    return subprocess.run(['git', '-C', clone, *args], capture_output=True, text=True, check=True).stdout.strip()


head = git('log', '-1', '--format=%H %cI', 'origin/main')
print('\norigin/main as fetched:', head)
names = git('ls-tree', '-r', '--name-only', 'origin/main').split('\n')
LT = 'noon/agent2-pdtile/lean-tiling/'
for f in ('SetLift.lean', 'SetAll.lean', 'Sign.lean', 'Lift2.lean', 'LiftAll.lean'):
    hits = [n for n in names if n.startswith(LT) and n.endswith('/' + f)]
    print(f'  {f}: in the public Lean folder: {hits}')
SL = [n for n in names if '/lean-lift/sets-lean/' in n]
roots = sorted({n[:n.index('/lean-lift/sets-lean/') + len('/lean-lift/sets-lean/')] for n in SL})
print('  folders lean-lift/sets-lean/ in the public tree:', roots, '| files under:', len(SL))
top = sorted({n[len(roots[0]):].split('/')[0] for n in SL if n.startswith(roots[0])}) if roots else []
print('  what it holds at its top:', top)
for f in ('SetLift.lean', 'SetAll.lean'):
    x = git('rev-parse', f'origin/main:{LT}Pnq/{f}'); y = git('rev-parse', f'origin/main:{roots[0]}{f}')
    print(f'  {f}: the same file in both places (same blob): {x == y}')
print('  the commit that added them:', git('log', '--format=%h %cI %an', 'origin/main', '--', LT + 'Pnq/SetLift.lean', LT + 'Pnq/SetAll.lean', roots[0]))
print('  the sentence as public now (origin/main:yonder/minsize/files/README.md) is the old one:', old in git('show', 'origin/main:yonder/minsize/files/README.md'))
