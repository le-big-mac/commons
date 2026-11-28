"""to-commons.py: copy the gasket page's remake of 27 and 28 November to the shared folder, file by file, deleting nothing.
python -I out27/to-commons.py [--dry]      (from anywhere; paths are fixed)
Left at home: the page as built for the readers (out27/built-preview/: it is the public page itself once that is up, and
reader27/gasket-as-visited-7.html.txt is a copy), working scripts and drafts, records kept twice, Python's own files."""
import filecmp, os, shutil, sys
SRC = '/home/agent2/gasket'; DST = '/srv/commons/agent2-gasket'; DRY = '--dry' in sys.argv
TOP = ['README.md', 'gasket.html', 'page.src.html', 'page-mutants.py', 'page-mutants.out', 'page-test.out', 'checkfacts.py', 'checkfacts.out', 'tools/shot-gasket.js', 'tools/pinned-words.json'] + \
      ['shots/' + x for x in ['chart.png', 'gasket-0_0_1_1.png', 'gasket-contact.png', 'gasket-deep.png', 'gasket-inside-lit.png', 'gasket-m1_2_2_3.png', 'gasket-m23_48_49_52.png', 'gasket-m2_3_6_7.png', 'gasket-m3_4_12_13.png', 'gasket-m3_5_8_8.png', 'gasket-m4_5_20_21.png', 'gasket-squares.png', 'page.png']]
LEFT = {'out27/stage1.html', 'out27/page-mutants.new.py', 'out27/first-pass.out', 'out27/page-test.stage9.under-load.out', 'out27/page-mutants.last-whole-run.kept.out', 'out27/first-screen.js', 'out27/try-phone.js'}
def wanted(rel):
    name = os.path.basename(rel)
    if name.endswith('.private.txt') or name.endswith('.pyc') or '/__pycache__/' in '/' + rel or rel.startswith('out27/built-preview/'): return False
    return rel not in LEFT
if __name__ == '__main__':
    files = list(TOP)
    for d in ('reader27', 'referee27', 'truth27', 'out27'):
        for root, dirs, names in os.walk(os.path.join(SRC, d)):
            dirs.sort()
            for f in sorted(names): files.append(os.path.relpath(os.path.join(root, f), SRC))
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
