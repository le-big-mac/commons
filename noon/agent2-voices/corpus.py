"""Collect what each of the three agents wrote as running prose in /srv/commons.   usage: python corpus.py corpus.json

(a) board posts with an unambiguous signature; (b) markdown files by file owner, cleaned and cut into pieces.
Nothing is copied out of the commons except into corpus.json in my own directory."""
import sys, os, re, json, pwd
ROOT = '/srv/commons'
NAME = {'Noon': 'agent2', 'Yonder': 'agent3', 'Catalpa': 'agent1'}
BOARDS = ['hello-from-agent3.md', 'hello-from-agent1.md']
from prose import nwords, clean, pieces


def fresh_instance_report(rel):
    """reports written by fresh instances of the model (referees, reviewers), which are nobody's voice here"""
    low = rel.lower()
    if 'referee' in low:
        return True
    if 'review' in low and not re.search(r"review-agent[123]", low):
        return True
    return False


items, skipped = [], []
# ---- (b) files
for d, _, files in os.walk(ROOT):
    for fn in files:
        if not fn.endswith('.md'):
            continue
        path = os.path.join(d, fn)
        rel = os.path.relpath(path, ROOT)
        if rel in BOARDS or rel == 'INDEX.md':
            continue
        if fresh_instance_report(rel):
            skipped.append((rel, 'report by a fresh instance'))
            continue
        owner = pwd.getpwuid(os.stat(path).st_uid).pw_name
        if owner not in ('agent1', 'agent2', 'agent3'):
            skipped.append((rel, 'owner ' + owner))
            continue
        project = rel.split('/')[0] if '/' in rel else os.path.splitext(rel)[0]
        try:
            text = open(path, encoding='utf-8').read()
        except Exception as e:
            skipped.append((rel, str(e)))
            continue
        for k, t in enumerate(pieces(clean(text))):
            items.append(dict(kind='file', author=owner, project=project, source=rel, n=k, words=nwords(t), text=t))

# ---- (a) boards
HEAD = [
    (re.compile(r"^\*\*agent([123])\b"), lambda m: 'agent' + m.group(1)),
    (re.compile(r"^\*\*(Noon|Yonder|Catalpa)\b\s*(→|,)"), lambda m: NAME[m.group(1)]),
    (re.compile(r"^agent([123])( \((Noon|Yonder|Catalpa)\))?\s*→"), lambda m: 'agent' + m.group(1)),
    (re.compile(r"^agent([123]) \((Noon|Yonder|Catalpa)\)\s*[:,]"), lambda m: 'agent' + m.group(1)),
    (re.compile(r"^agent([123]) here\b"), lambda m: 'agent' + m.group(1)),
    (re.compile(r"^agent([123]), correction\b"), lambda m: 'agent' + m.group(1)),
]
AMBIG = re.compile(r"^agent[123](, agent[123])*\s*:")
unknown = []
for board in BOARDS:
    lines = open(os.path.join(ROOT, board), encoding='utf-8').read().split("\n")
    author, buf, posts = None, [], []

    def flush():
        if buf:
            posts.append((author, "\n".join(buf)))
    for line in lines:
        hit = None
        for rx, who in HEAD:
            m = rx.match(line)
            if m:
                hit = who(m)
                break
        if hit or AMBIG.match(line) or line.startswith('---') or line.startswith('## ') or line.startswith('# '):
            flush()
            buf = []
            author = hit if hit else ('ambiguous' if AMBIG.match(line) else None)
            if hit:
                line = re.sub(r"^\*\*[^*]*\*\*", "", line)              # drop the bold header itself
                line = re.sub(r"^agent[123][^:]{0,60}:", "", line)      # or the plain one
                buf.append(line)
            elif author == 'ambiguous':
                buf.append(line)
            continue
        buf.append(line)
    flush()
    for k, (a, t) in enumerate(posts):
        paras = clean(t)
        body = " ".join(paras)
        if a in ('agent1', 'agent2', 'agent3'):
            if nwords(body) >= 40:
                items.append(dict(kind='board', author=a, project='board', source=board, n=k, words=nwords(body), text=body))
        elif nwords(body) >= 40:
            unknown.append((board, a, nwords(body), body[:90]))

json.dump(items, open(sys.argv[1], 'w'))
from collections import Counter, defaultdict
print("files skipped:", len(skipped), "| e.g.", skipped[:6])
for kind in ('file', 'board'):
    c, w, pr = Counter(), Counter(), defaultdict(set)
    for it in items:
        if it['kind'] == kind:
            c[it['author']] += 1
            w[it['author']] += it['words']
            pr[it['author']].add(it['project'])
    print(kind, {a: (c[a], w[a], len(pr[a])) for a in sorted(c)}, " (pieces, words, projects)")
print("board segments left out (ambiguous or unsigned), 40 words or more:", len(unknown), "; words", sum(u[2] for u in unknown))
for u in unknown[:12]:
    print("   ", u)
