# Reader for poems from The Latin Library: the hexameter lines, leaving out prefaces (elegiac or iambic) and anything set as a couplet.
import re, html
def load(fn, verbose=False):
    t = open(fn, encoding='latin-1', errors='replace').read()
    t = re.sub(r'<span[^>]*>.*?</span>', '', t, flags=re.S | re.I)
    t = t.replace('&Aelig;', 'Ae').replace('&aelig;', 'ae').replace('&OElig;', 'Oe').replace('&oelig;', 'oe')
    blocks = re.split(r'<p[^>]*>', t, flags=re.I); out = []; skip_next = False; heads = []
    for b in blocks:
        raw = b
        text = html.unescape(re.sub(r'<br\s*/?>', '\n', b, flags=re.I))
        head = re.search(r'<b>(.*?)</b>', raw, flags=re.S | re.I)
        if head and len(re.sub(r'<[^>]+>', '', text).strip().split('\n')) <= 2:
            h = re.sub(r'<[^>]+>', '', head.group(1)).strip(); heads.append(h)
            skip_next = bool(re.search(r'PRAEF|PREFACE|PROOEM', h, flags=re.I)); continue
        lines = [re.sub(r'<[^>]+>', '', x) for x in text.split('\n')]
        lines = [x for x in lines if len(re.sub(r'[^A-Za-z]', '', x)) >= 18]
        lines = [x for x in lines if not re.search(r'Claudian:|Prudentius:|Sedulius:', x) and not (sum(1 for c in x if c.isupper()) > 0.6 * sum(1 for c in x if c.isalpha()))]
        if not lines: continue
        elegiac = sum(1 for x in lines if re.match(r'[\s\xa0]{3,}', x)) >= max(1, len(lines) // 4)
        if skip_next or elegiac:
            if verbose: print('   left out', len(lines), 'lines beginning:', lines[0].strip()[:50])
            skip_next = False; continue
        out += [x.replace('\xa0', ' ').strip() for x in lines]
    if verbose: print('  ', fn.split('/')[-1], len(out), 'lines kept; headings:', heads[:8])
    return out
def late():
    """the late-antique poems used beside Arator: name -> lines"""
    T = '/home/agent1/arator/texts/'
    sed = [l for i in range(1, 6) for l in load(T + f'sedulius{i}.html')]
    c6 = load(T + 'claudian_cons6.html'); k = next(i for i, l in enumerate(c6) if l.startswith('Aurea Fortunae')); c6 = c6[k:]      # the rest of its elegiac preface is dropped
    cla = [l for f in ('olyb', 'proserp1', 'proserp2', 'proserp3') for l in load(T + f'claudian_{f}.html')] + c6      # In Rufinum is left out: that copy writes u for v throughout
    cla = [re.sub(r'\s+\d+\s*$', '', l) for l in cla]
    # Prudentius's Psychomachia is left out as well: that copy too writes u for v, which this scanner cannot read
    return dict(sedulius=sed, claudian=cla)
if __name__ == '__main__':
    for k, v in late().items(): print(k, len(v), '|', v[0][:50], '|', v[-1][:50])
    import glob
    for f in sorted(glob.glob('/home/agent1/arator/texts/sedulius[1-5].html')) + sorted(glob.glob('/home/agent1/arator/texts/claudian_*.html')) + ['/home/agent1/arator/texts/prud_psycho.html']:
        L = load(f, verbose=True); print('      first:', L[0][:60], '| last:', L[-1][:60])
