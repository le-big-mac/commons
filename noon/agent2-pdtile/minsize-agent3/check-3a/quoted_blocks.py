"""Check that every fenced lean block of section-3a.md stands verbatim in the Lean files.
usage: quoted_blocks.py SECTION.md LEAN_DIR"""
import sys, re
sec = open(sys.argv[1]).read(); L = sys.argv[2]
blocks = re.findall(r'```lean\n(.*?)\n```', sec, re.S)
print(len(blocks), 'fenced blocks')
files = {f: open(f'{L}/Pnq/{f}.lean').read() for f in ('Rule', 'Weighted', 'MinGroup')}
for b in blocks:
    for piece in b.split('\n\n'):
        name = re.match(r'(?:noncomputable )?(?:def|theorem) (\S+)', piece).group(1)
        hits = [(f, t.count(piece)) for f, t in files.items() if piece in t]
        what = ''
        for f, c in hits:
            t = files[f]; i = t.index(piece); after = t[i + len(piece): i + len(piece) + 12]
            before = t[max(0, i - 1): i]
            what += f' in {f}.lean x{c}; preceded by {before!r}; followed by {after!r}'
        print(f'{name}: {"VERBATIM" if hits else "NOT FOUND"}{what}')
