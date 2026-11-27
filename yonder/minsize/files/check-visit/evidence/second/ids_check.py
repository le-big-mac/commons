"""Second pass: the builder now gives every folded section an id.  Does any id stand twice on a page (which would break a link)?
Builds the notebook once with the new builder into this folder, looks at the five study pages, deletes the build.
usage: ids_check.py"""
import os, re, shutil, subprocess, collections
E = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(E, 'tmp-built-ids'); stage = os.path.join(E, 'tmp-stage')
for d in (out, stage):
    if os.path.exists(d): shutil.rmtree(d)
shutil.copytree('/home/agent3/door/visit-3-page/minsize/files', stage, ignore=shutil.ignore_patterns('*.html'))
r = subprocess.run(['bash', os.path.expanduser('~/bin/cap2g.sh'), os.path.expanduser('~/welch/.venv/bin/python'), '-I', '-B', '/home/agent3/site/build/site.py', out],
                   env=dict(os.environ, DOOR_SRC=stage), capture_output=True, text=True)
assert r.returncode == 0, r.stderr[-800:]
for slug in ('antikythera', 'hemispheres', 'handshake', 'wikipedia', 'minsize'):
    t = open(os.path.join(out, slug, 'index.html'), encoding='utf-8').read()
    ids = re.findall(r'\bid="([^"]*)"', t); dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    folds = re.findall(r'<details class="fold[^"]*"(?: id="([^"]*)")?>\n<summary>(.*?)</summary>', t)
    print(f'{slug}: ids {len(ids)}, standing twice: {dup}; folds: {folds}; links to sections: {len(re.findall("class=.tosec.", t))}; script for opening folds: {"openFold" in t}')
for d in (out, stage): shutil.rmtree(d)
print('build deleted')
