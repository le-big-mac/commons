"""Do the changes to the site builder change any word of any page?
Builds the whole notebook twice into this folder, once with site.py.before-visit and once with site.py, from the same sources
(the page under test is staged here: the public folder of the page, with the candidate as README.md, the new picture and the
visitor's report).  Compares every file of the two builds, and for every HTML file that differs, its words with the tags removed.
Then compares the new build of the page with the one the author built (visit-2-page).  The built trees are deleted at the end;
only this output is kept.     usage: builder_check.py"""
import os, sys, re, shutil, subprocess, html, difflib, filecmp
E = os.path.dirname(os.path.abspath(__file__))
B = '/home/agent3/site/build'
PY = os.path.expanduser('~/welch/.venv/bin/python')
CAP = os.path.expanduser('~/bin/cap2g.sh')
stage = os.path.join(E, 'tmp-stage'); old = os.path.join(E, 'tmp-built-old'); new = os.path.join(E, 'tmp-built-new')
for d in (stage, old, new):
    if os.path.exists(d): shutil.rmtree(d)
shutil.copytree('/srv/commons/minsize-door-agent3', stage)
shutil.copy2('/home/agent3/door/README.visit-candidate.md', os.path.join(stage, 'README.md'))
shutil.copy2('/home/agent3/door/clock-five-marks.png', os.path.join(stage, 'clock-five-marks.png'))
os.makedirs(os.path.join(stage, 'check-visit')); shutil.copy2('/home/agent3/door/check-visit/visit-1.md', os.path.join(stage, 'check-visit', 'visit-1.md'))
env = dict(os.environ, DOOR_SRC=stage)
for script, out in (('site.py.before-visit', old), ('site.py', new)):
    r = subprocess.run(['bash', CAP, PY, '-I', '-B', os.path.join(B, script), out], env=env, capture_output=True, text=True)
    print(f'--- build with {script}: exit {r.returncode}'); print(r.stdout.strip()); print(r.stderr.strip()[-2000:])
    assert r.returncode == 0

def words(path):
    t = open(path, encoding='utf-8', errors='replace').read()
    t = re.sub(r'<(script|style)\b.*?</\1>', ' ', t, flags=re.S)
    alts = re.findall(r'alt="([^"]*)"', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return html.unescape(t).split(), alts

def files(root):
    out = []
    for d, ds, fs in os.walk(root):
        for f in fs: out.append(os.path.relpath(os.path.join(d, f), root))
    return sorted(out)
fo, fn = files(old), files(new)
print(f'\nfiles in old build: {len(fo)}; in new build: {len(fn)}; only in old: {sorted(set(fo) - set(fn))}; only in new: {sorted(set(fn) - set(fo))}')
nhtml = sum(1 for f in fn if f.endswith('.html'))
differ = [f for f in fn if f in set(fo) and not filecmp.cmp(os.path.join(old, f), os.path.join(new, f), shallow=False)]
print(f'HTML files in new build: {nhtml};  files that differ in bytes between the two builds: {len(differ)}')
wordchanged = []
for f in differ:
    if not f.endswith('.html'):
        print(f'   differs (not HTML): {f}'); continue
    wo, ao = words(os.path.join(old, f)); wn, an = words(os.path.join(new, f))
    a = open(os.path.join(old, f), encoding='utf-8', errors='replace').read().split('\n'); b = open(os.path.join(new, f), encoding='utf-8', errors='replace').read().split('\n')
    nl = sum(1 for l in difflib.unified_diff(a, b, lineterm='', n=0) if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++', '---')))
    same = (wo == wn and ao == an)
    print(f'   differs: {f}: changed lines {nl}; words with tags removed the same: {wo == wn}; alt texts the same: {ao == an}')
    if not same:
        wordchanged.append(f)
        sm = difflib.SequenceMatcher(None, wo, wn, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'equal': print(f'        {tag}: OLD[{" ".join(wo[i1:i2])[:400]}] -> NEW[{" ".join(wn[j1:j2])[:400]}]')
    # what kind of raw change
    kinds = set()
    for l in difflib.unified_diff(a, b, lineterm='', n=0):
        if l.startswith('+') and not l.startswith('+++'):
            if '<a href=' in l and '<img' in l: kinds.add('link round a picture')
            elif '<details class="fold">' in l or '<summary>' in l or '</details>' in l: kinds.add('fold')
            elif l.strip() == '+': kinds.add('blank line')
            else: kinds.add('other: ' + l[:160])
    print('        kinds of change:', sorted(kinds))
print(f'\npages whose words (tags removed) differ between the two builds: {wordchanged}')
print('pages with a picture that now has a link round it:', sorted(f for f in fn if f.endswith('.html') and '<figure><a href=' in open(os.path.join(new, f), encoding='utf-8', errors='replace').read()))
print('pages with folds (whose label is written by the style sheet):', sorted(f for f in fn if f.endswith('.html') and '<details class="fold' in open(os.path.join(new, f), encoding='utf-8', errors='replace').read()))

print('\n--- the new build of the page against the author\'s build (visit-2-page)')
for rel in ('minsize/index.html', 'style.css', 'index.html', 'licence.html', 'minsize/files/index.html'):
    a = os.path.join(new, rel); b = os.path.join('/home/agent3/door/visit-2-page', rel)
    print(f'   {rel}: ' + ('missing in visit-2-page' if not os.path.exists(b) else ('same bytes' if filecmp.cmp(a, b, shallow=False) else 'DIFFERENT')))
vf = files('/home/agent3/door/visit-2-page/minsize'); nf = files(os.path.join(new, 'minsize'))
print('   files of the page only in the author\'s build:', sorted(set(vf) - set(nf)), ' only in mine:', sorted(set(nf) - set(vf)))
print('   differing among the common ones:', [f for f in vf if f in set(nf) and not filecmp.cmp(os.path.join('/home/agent3/door/visit-2-page/minsize', f), os.path.join(new, 'minsize', f), shallow=False)])

print('\n--- the words of the built page against the words of the candidate Markdown')
wp, alts = words(os.path.join(new, 'minsize/index.html'))
md = open('/home/agent3/door/README.visit-candidate.md', encoding='utf-8').read()
md2 = re.sub(r'!\[([^\]]*)\]\([^)]*\)', ' ', md)                 # the picture: its alt text is compared apart
md2 = re.sub(r'\[([^\]]*)\]\((https?://[^)]*)\)', r'\1', md2)    # a link keeps its words
md2 = re.sub(r'(?m)^#+ ', '', md2); md2 = re.sub(r'(?m)^(\s*)- ', r'\1', md2)
md2 = md2.replace('**', '').replace('`', '')
md2 = re.sub(r'(?<![\w*])\*(?=\S)|(?<=\S)\*(?![\w*])', '', md2)
wm = md2.split()
sm = difflib.SequenceMatcher(None, wm, wp, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal': print(f'   {tag}: MARKDOWN[{" ".join(wm[i1:i2])[:300]}] -> PAGE[{" ".join(wp[j1:j2])[:300]}]')
print('   alt text of the picture on the page equals the candidate\'s:', alts == re.findall(r'!\[([^\]]*)\]', md))
pg = open(os.path.join(new, 'minsize/index.html'), encoding='utf-8').read()
print('   folds on the page, in order:', re.findall(r'<summary>(.*?)</summary>', pg))
print('   open headings on the page, in order:', re.findall(r'<h2>(.*?)</h2>', pg))
print('   files beside the page whose name starts with clock:', sorted(f for f in nf if os.path.basename(f).startswith('clock')))
for d in (stage, old, new): shutil.rmtree(d)
print('\nbuilt trees and the staged copy deleted')
