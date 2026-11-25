"""Adds one source to found.json, after checking that the quotation is in the saved text word for word (white space aside).
usage: python -I record.py LINE NAME 'who, what, where, year' 'the quotation' ['a second quotation' ...]"""
import sys, json, os
line, name, cite = sys.argv[1:4]; quotes = sys.argv[4:]; d = os.path.expanduser(f"~/prior-data/{line}/{name}"); tx = ' '.join(open(f"{d}/text.txt", errors="replace").read().split())
for q in quotes: assert ' '.join(q.split()) in tx, "NOT IN THE TEXT: " + q[:80]
p = "found.json"; F = json.load(open(p)) if os.path.exists(p) else {}
F.setdefault(line, []); F[line] = [e for e in F[line] if e['name'] != name] + [dict(name=name, cite=cite, url=open(f"{d}/url.txt").read().strip(), quotes=[' '.join(q.split()) for q in quotes])]
json.dump(F, open(p, "w"), indent=1, ensure_ascii=False); print(f"{line}/{name}: {len(quotes)} quotation(s) recorded")
