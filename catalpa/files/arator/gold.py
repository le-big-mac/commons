# Reader for the reference scansion (hypotactic.com): each line as plain words and as the pattern of its first five feet.
import re, html
def load(fn):
    t = open(fn, encoding='utf-8', errors='replace').read(); out = []
    for m in re.finditer(r'<div class="line[^"]*"[^>]*>(.*?)</div>', t, flags=re.S):
        words = []; q = []; flags = set(); nel = 0
        for w in re.finditer(r'<span class="word[^"]*">(.*?)</span></span>', m.group(1), flags=re.S):
            syl = re.findall(r'<span class="syll ([^"]*)">([^<]*)', w.group(1) + '</span>')
            words.append(''.join(html.unescape(s) for c, s in syl))
            for c, s in syl:
                c = c.split(); flags.update(c[1:])
                if c[0] == 'elided': nel += 1; continue
                q.append('L' if c[0] == 'long' else 'S' if c[0] == 'short' else '?')
        pat = ''; i = 0; ok = True
        for f in range(5):
            if i < len(q) and q[i] == 'L' and i + 2 < len(q) and q[i + 1] == 'S' and q[i + 2] == 'S': pat += 'D'; i += 3
            elif i + 1 < len(q) and q[i] == 'L' and q[i + 1] == 'L': pat += 'S'; i += 2
            else: ok = False; break
        if ok and len(q) - i != 2: ok = False
        out.append(dict(text=' '.join(words), pat=pat if ok else None, flags=flags, nel=nel))
    return out
