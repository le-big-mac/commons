"""Dr Young's rods: the caption's afterlife. Finds, in each fetched text, the passage that carries Young's arrangement
and writes it out with the paragraphs on either side, for reading.
    python -I afterlife.py ~/lantern-data/afterlife OUTDIR
"""
import os, re, sys

KEY = re.compile(r'lowers\s+the\s+point|twice\s+the\s+focal\s+length', re.I)

def passages(path, before=45, after=45):
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    hits = [i for i, l in enumerate(lines) if KEY.search(l)]
    out = []; start = None
    for i in hits:                                      # merge hits that are near one another
        if start is None: start, end = i, i
        elif i - end <= 60: end = i
        else: out.append((start, end)); start, end = i, i
    if start is not None: out.append((start, end))
    return [(max(0, a - before), min(len(lines), b + after + 1), lines) for a, b in out]

if __name__ == '__main__':
    root, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name, 'text.txt')
        if not os.path.exists(p): continue
        ps = passages(p)
        with open(os.path.join(outdir, name + '.txt'), 'w', encoding='utf-8') as f:
            for a, b, lines in ps:
                f.write(f'===== {name}: lines {a + 1} to {b} of the fetched text =====\n')
                f.write('\n'.join(l for l in lines[a:b] if l.strip()) + '\n')
        print(name, [(a + 1, b) for a, b, _ in ps])
