"""merge.py DIR: put together the outputs of search runs that shared one search by FIRST."""
import sys, re, glob
tot = None; best = []; nbest = 0; worst = None; nworst = 0; sets = 0; files = 0; first = None
for f in sorted(glob.glob(sys.argv[1] + '/*.out')):
    s = open(f).read()
    if 'least total' not in s:
        print('INCOMPLETE', f); sys.exit(1)
    files += 1
    n = int(re.search(r'sets scored (\d+)', s).group(1)); sets += n
    if n == 0: continue
    t = int(re.search(r'least total (-?\d+)', s).group(1))
    b = [tuple(map(int, l.split()[1:])) for l in s.split('\n') if l.startswith('  best')]
    nb = int(re.search(r'sets with the least total (\d+)', s).group(1))
    w = int(re.search(r'least worst case (-?\d+)', s).group(1))
    nw = int(re.search(r'sets with the least worst case (\d+)', s).group(1))
    fw = tuple(map(int, re.search(r'^  first (.*)$', s, re.M).group(1).split()))
    if tot is None or t < tot: tot, best, nbest = t, [], 0
    if t == tot: best += b; nbest += nb
    if worst is None or w < worst: worst, nworst, first = w, 0, fw
    if w == worst: nworst += nw
print('files', files)
print('sets scored', sets)
print('least total', tot)
print('sets with the least total', nbest)
for b in sorted(best): print('  best', *b)
print('least worst case', worst)
print('sets with the least worst case', nworst)
print('  first', *first)
