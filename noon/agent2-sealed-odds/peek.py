"""Bounded look at why a forecaster priced one line as it did: prints at most LIMIT characters around each of the last few mentions of a
label in the forecaster's own text (never the whole transcript).   usage: python peek.py TRANSCRIPT LABEL [LIMIT]"""
import sys, json, re
lab = sys.argv[2]; lim = int(sys.argv[3]) if len(sys.argv) > 3 else 500
texts = []
def walk(o):
    if isinstance(o, dict):
        if o.get('type') in ('text', 'thinking'):
            t = o.get('text') or o.get('thinking') or ''
            if isinstance(t, str): texts.append((o['type'], t))
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
for line in open(sys.argv[1], encoding='utf-8', errors='replace'):
    try: walk(json.loads(line))
    except Exception: pass
kinds = {}
for k, t in texts: kinds[k] = kinds.get(k, 0) + len(t)
print("characters of the forecaster's own text by kind:", kinds)
hits = [(k, t, m.start()) for k, t in texts for m in re.finditer(r"\b" + re.escape(lab) + r"\b", t)]
print(len(hits), "mentions of", lab)
for k, t, i in hits[-3:]:
    print(f"--- ({k}) ...{' '.join(t[max(0, i - 60): i + lim].split())}...")
