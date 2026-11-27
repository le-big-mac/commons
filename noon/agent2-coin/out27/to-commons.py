"""to-commons.py: copy the coin study's files of 27 November to the shared folder, file by file, deleting nothing.
python -I out27/to-commons.py [--dry]      (from anywhere; paths are fixed)
Left at home: files named *.private.txt (the readers' handles), the working pictures in out27/, the runner's work folders."""
import filecmp, os, shutil, sys
SRC = '/home/agent2/coin'; DST = '/srv/commons/agent2-coin'; DRY = '--dry' in sys.argv
TOP = ['README.md', 'change.html', 'page.src.html', 'page.src.before-27nov.html', 'pcore.js', 'ctest.js', 'ctest.out', 'cmutants.py', 'cmutants.out', 'checkfacts.js', 'checkfacts.out',
       'page-mutants.py', 'page-mutants.out', 'sources.md', 'quotes.json', 'quotes.out', 'tools/shot-change.js', 'tools/shot-change.before-27nov.js.txt',
       'shots/euro.png', 'shots/narrow.png', 'shots/page.png', 'shots/three.png']
def wanted(rel):
    name = os.path.basename(rel)
    if name.endswith('.private.txt') or name.endswith('.pyc'): return False
    if rel.startswith('out27/') and (name.endswith('.png') or name in ('page-test.tmp.out', 'stage1.html', 'stage2a.html', 'shot-stage1.js', 'page-test.now.out', 'ctest.now.out', 'checkfacts.now.out', 'cmutants.now.out')): return False   # working pictures; what the scripts write on their way and write again when run; records that are also kept under their lasting names
    return True
if __name__ == '__main__':
    files = list(TOP)
    for d in ('reader', 'referee27', 'truth27', 'out27'):
        for f in sorted(os.listdir(os.path.join(SRC, d))):
            p = os.path.join(SRC, d, f)
            if os.path.isfile(p): files.append(d + '/' + f)
    new = same = changed = skipped = 0
    for rel in files:
        if not wanted(rel): skipped += 1; print('left at home  ' + rel); continue
        s, t = os.path.join(SRC, rel), os.path.join(DST, rel)
        if not os.path.isfile(s): raise SystemExit('missing at home: ' + rel)
        if os.path.exists(t) and filecmp.cmp(s, t, shallow=False): same += 1; continue
        kind = 'changed' if os.path.exists(t) else 'new'
        if kind == 'changed': changed += 1
        else: new += 1
        print('%-8s %s' % (kind, rel))
        if not DRY:
            os.makedirs(os.path.dirname(t), exist_ok=True)
            if os.path.exists(t):
                with open(s, 'rb') as a, open(t, 'wb') as b: b.write(a.read())          # written in place: the file keeps its place and owner
            else: shutil.copy2(s, t)
    print('%d new, %d changed, %d already the same, %d left at home%s' % (new, changed, same, skipped, '  (a dry run: nothing written)' if DRY else ''))
