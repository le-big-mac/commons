"""Compare two JSON files number by number, ignoring keys named 'seconds'.   usage: python compare.py LABEL new.json published.json"""
import sys, json, math
def walk(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k == 'seconds': continue
            if k not in a or k not in b: out.append((path + '/' + k, 'missing')); continue
            walk(a[k], b[k], path + '/' + k, out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): out.append((path, f'lengths {len(a)} and {len(b)}')); return
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, f'{path}[{i}]', out)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        if a != b:
            rel = abs(a - b) / max(abs(a), abs(b), 1e-300); out.append((path, f'{a!r} against {b!r} (relative {rel:.1e})'))
    elif a != b: out.append((path, f'{a!r} against {b!r}'))
a, b = json.load(open(sys.argv[2])), json.load(open(sys.argv[3])); out = []; walk(a, b, '', out)
worst = max((float(x[1].split('relative ')[1].rstrip(')')) for x in out if 'relative' in x[1]), default=0.0)
print(f"{sys.argv[1]}: " + ("identical, number for number" if not out else f"{len(out)} differences; largest relative difference {worst:.1e}; first: {out[0]}"), flush=True)
