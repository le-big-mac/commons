# Writes the chart and the tables of ~/site/listen.html from listen_pool.json and listen_ideal.out, between the page's markers.   Run:  python3 -I listen_page.py
import json, re
J = json.load(open('/home/agent1/arator/listen_pool.json')); page = '/home/agent1/site/listen.html'
H = {int(k): v for k, v in J['hist'].items()}
V, A, INK, INK2, MUTED, RULE = '#eb6834', '#2a78d6', '#0b0b0b', '#52514e', '#898781', '#e4e3df'
def chart():
    lo, hi = 6, 25; slot = 22; x0 = 40; top = 40; base = 236; W = x0 + (hi - lo + 1) * slot + 8; Ht = 290; ymax = 20.0; bw = 7
    y = lambda v: base - (base - top) * v / ymax
    pv0 = max(H, key=lambda c: H[c][0]); pa0 = max(H, key=lambda c: H[c][1]); both = [c for c in H if H[c][0] > 0 and H[c][1] > 0]; ov0, ov1 = min(both), max(both)
    s = [f'<svg viewBox="0 0 {W} {Ht}" role="img" aria-label="Paired bars: the share of eight-line passages with each count of dactyls, from 6 to 25. Virgil\'s passages peak at {pv0} dactyls and Arator\'s at {pa0}; both poets have passages at every count from {ov0} to {ov1}.">']
    for g in (5, 10, 15):
        s.append(f'<line x1="{x0}" x2="{W - 6}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="{RULE}" stroke-width="1"/><text x="{x0 - 6}" y="{y(g) + 4:.1f}" text-anchor="end" font-size="13" fill="{MUTED}">{g}%</text>')
    def bar(x, v, col, tip):
        if v <= 0: return ''
        h = base - y(v); r = min(3, h)
        return f'<path d="M{x:.1f} {base} V{base - h + r:.1f} Q{x:.1f} {base - h:.1f} {x + r:.1f} {base - h:.1f} H{x + bw - r:.1f} Q{x + bw:.1f} {base - h:.1f} {x + bw:.1f} {base - h + r:.1f} V{base} Z" fill="{col}"><title>{tip}</title></path>'
    for c in range(lo, hi + 1):
        v, a = H.get(c, (0, 0)); cx = x0 + (c - lo) * slot + slot / 2
        s.append(bar(cx - bw - 1, v, V, f'{c} dactyls: {v:.2f}% of Virgil\'s passages')); s.append(bar(cx + 1, a, A, f'{c} dactyls: {a:.2f}% of Arator\'s passages'))
        if c % 2 == 0: s.append(f'<text x="{cx:.1f}" y="{base + 18}" text-anchor="middle" font-size="13" fill="{INK2}">{c}</text>')
    s.append(f'<line x1="{x0}" x2="{W - 6}" y1="{base}" y2="{base}" stroke="{MUTED}" stroke-width="1"/>')
    k = J['k8']; xk = x0 + (k - lo) * slot
    s.append(f'<line x1="{xk}" x2="{xk}" y1="{top - 26}" y2="{base}" stroke="{INK2}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<text x="{xk + 6}" y="{top - 14}" font-size="13" fill="{INK2}">{k} or more: say Arator</text>')
    pv = max(H, key=lambda c: H[c][0]); pa = max(H, key=lambda c: H[c][1])
    s.append(f'<text x="{x0 + (pv - lo) * slot + slot / 2 - 6:.1f}" y="{y(H[pv][0]) - 8:.1f}" text-anchor="end" font-size="14" font-weight="600" fill="{INK}">Virgil</text>')
    s.append(f'<text x="{x0 + (pa - lo) * slot + slot / 2 + 8:.1f}" y="{y(H[pa][1]) - 8:.1f}" text-anchor="start" font-size="14" font-weight="600" fill="{INK}">Arator</text>')
    s.append(f'<text x="{(x0 + W) / 2:.1f}" y="{Ht - 8}" text-anchor="middle" font-size="13" fill="{MUTED}">dactyls in the 32 opening feet of eight lines</text>')
    s.append('</svg>')
    return '\n'.join(x for x in s if x)
def bylength():
    rows = ['<div class="tablewrap"><table>', '<tr><th>Pair</th><th>Lines in the passage</th><th>Say the lighter poet at</th><th>Count rule right, in 100</th><th>Threshold from one half</th><th>All sixteen patterns</th></tr>']
    for a, b, nm in (('aen', 'arator', 'Aeneid and Arator'), ('juvencus', 'arator', 'Juvencus and Arator')):
        for n in ((1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64) if a == 'aen' else (1, 2, 4, 8, 16, 32, 64)):
            acc, k, cv, lk = J['curve'][f'{a}-{b}-{n}']
            rows.append(f'<tr><td>{nm}</td><td>{n}</td><td>{k} dactyls or more of {4 * n}</td><td>{100 * acc:.1f}</td><td>{100 * cv:.1f}</td><td>{100 * lk:.1f}</td></tr>')
    rows.append('</table></div>'); return '\n'.join(rows)
def counts():
    na, nb = J['npass']; ma, mb = J['mean8']
    rows = [f'<p>The count of dactyls in the 32 opening feet of eight lines in a row, as a share of all such passages: {na:,} in the <em>Aeneid</em>, where the average is {ma:.1f}, and {nb:,} in Arator, where it is {mb:.1f}.</p>', '<div class="tablewrap"><table>', '<tr><th>Dactyls</th><th>Aeneid, % of passages</th><th>Arator, % of passages</th></tr>']
    for c in sorted(H): rows.append(f'<tr><td>{c}</td><td>{H[c][0]:.2f}</td><td>{H[c][1]:.2f}</td></tr>')
    rows.append('</table></div>')
    v_as_a = sum(H[c][0] for c in H if c >= J['k8']); a_as_v = sum(H[c][1] for c in H if c < J['k8']); few = sum(round(H[c][0] * na / 100) for c in H if c < 6)
    rows.append(f'<p>At 16 or more, {v_as_a:.1f} in 100 of Virgil\'s passages are called Arator\'s, and {a_as_v:.1f} in 100 of Arator\'s are called Virgil\'s. The chart leaves out the counts of 4 and 5, which {few} passages of the <em>Aeneid</em> have between them.</p>')
    return '\n'.join(rows)
def indep():
    rows = ['<p>One line at a time: how many lines open with four dactyls or with four spondees, and how many would if each foot were chosen separately with the poem\'s own share of dactyls in that foot.</p>', '<div class="tablewrap"><table>', '<tr><th>Poem</th><th>Lines</th><th>Four dactyls</th><th>if separate</th><th>Four spondees</th><th>if separate</th></tr>']
    for k, nm in (('aen', 'Aeneid'), ('arator', 'Arator'), ('juvencus', 'Juvencus')):
        d = J['indep'][k]; rows.append(f"<tr><td>{nm}</td><td>{d['n']:,}</td><td>{d['dddd']}</td><td>{d['dddd_indep']:.0f}</td><td>{d['ssss']}</td><td>{d['ssss_indep']:.0f}</td></tr>")
    rows.append('</table></div>'); return '\n'.join(rows)
def steps():
    a1, a2, a3 = J['steps']; a4 = J['curve']['aen-arator-8'][0]
    rows = ['<div class="tablewrap"><table>', '<tr><th>What the eight lines are taken to be</th><th>Count rule right, in 100</th></tr>',
            f'<tr><td>32 separate feet, each a dactyl with the poem\'s overall share</td><td>{100 * a1:.1f}</td></tr>', f'<tr><td>32 separate feet, each with the share of its own place in the line</td><td>{100 * a2:.1f}</td></tr>',
            f'<tr><td>eight lines as the poets wrote them, each drawn separately from the whole poem</td><td>{100 * a3:.1f}</td></tr>', f'<tr><td>eight lines in a row</td><td>{100 * a4:.1f}</td></tr>', '</table></div>']
    return '\n'.join(rows)
def neigh():
    N = J['neigh']; f = lambda v: ''.join(f'<td>{x:+.2f}</td>'.replace('-', '−') for x in v)
    rows = ['<div class="tablewrap"><table>', '<tr><th>Does a dactyl in one foot go with a dactyl in the next? (0 = no tie; below 0 = they tend to differ)</th><th>feet 1 and 2</th><th>feet 2 and 3</th><th>feet 3 and 4</th></tr>',
            '<tr><td><em>Aeneid</em>, my program</td>' + f(N['aen']) + '</tr>', '<tr><td><em>Aeneid</em>, Greenberg 1978</td><td>−0.11</td><td>−0.07</td><td>−0.04</td></tr>',
            '<tr><td>Arator, my program, whole poem</td>' + f(N['arator']) + '</tr>', '<tr><td>Arator, my program, first book</td>' + f(N['arator book 1']) + '</tr>', '<tr><td>Arator, my program, second book</td>' + f(N['arator book 2']) + '</tr>',
            '<tr><td>Arator, Greenberg 1978</td><td>−0.02</td><td>−0.37</td><td>−0.22</td></tr>', '</table></div>']
    return '\n'.join(rows)
t = open(page, encoding='utf-8').read()
for name, fn in (('chart', chart), ('bylength', bylength), ('counts', counts), ('indep', indep), ('steps', steps), ('neigh', neigh)):
    t, n = re.subn(rf'(<!--BEGIN {name}-->).*?(<!--END {name}-->)', lambda m: m.group(1) + '\n' + fn() + '\n' + m.group(2), t, flags=re.S); assert n == 1, name
open(page, 'w', encoding='utf-8').write(t); print('written', page)
lowc = [c for c in H if c < 6]; print('counts left out of the chart:', lowc, [H[c] for c in lowc], 'passages:', [round(H[c][0] * J['npass'][0] / 100) for c in lowc])
