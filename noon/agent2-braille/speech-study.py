"""speech-study.py: the five lines of expectations-2.md scored from the record that speech.py writes.
    /usr/bin/python3 -I speech-study.py speech.json   ->  printed; speech-study.json"""
import json, os, sys
def S(u, c): return 1 - c / u
if __name__ == '__main__':
    recs = [r for r in json.load(open(sys.argv[1])) if r['era'] in (1, 2, 3)]; lines = []
    def verdict(name, ok, odds, note): lines.append((name, ok, odds)); print('   %-3s %-6s (odds %.2f)  %s' % (name, 'HELD' if ok else 'FAILED', odds, note))
    for r in recs:
        r['share'] = r['in'][2] / (r['in'][2] + r['out'][2]); r['Sin'] = S(r['in'][0], r['in'][1]) if r['in'][0] else None; r['Sout'] = S(r['out'][0], r['out'][1])
        r['Sboth'] = S(r['in'][0] + r['out'][0], r['in'][1] + r['out'][1])
    print('The books: share saved inside quotation marks, outside them, on both together; share of letters inside')
    for r in sorted(recs, key=lambda r: (r['era'], r['year'])):
        print('   era %d  %d  %-34s inside %s   outside %.2f%%   both %.2f%%   letters inside %.1f%%' % (r['era'], r['year'], r['title'], '%.2f%%' % (100 * r['Sin']) if r['Sin'] is not None else '   -  ', 100 * r['Sout'], 100 * r['Sboth'], 100 * r['share']))
    count = [r for r in recs if r['share'] >= 0.05]; left = [r['title'] for r in recs if r['share'] < 0.05]
    print('   left out of D1 and D3 (fewer than 5%% of letters inside): %s' % (', '.join(left) or 'none'))
    mean = lambda xs: sum(xs) / len(xs); era = lambda e, rs=recs: [r for r in rs if r['era'] == e]
    lower = [r for r in count if r['Sin'] < r['Sout']]
    verdict('D1', len(lower) >= 14, 0.60, 'inside is lower than outside in %d of the %d novels that count' % (len(lower), len(count)))
    out = {e: mean([r['Sout'] for r in era(e)]) for e in (1, 2, 3)}; ins = {e: mean([r['Sin'] for r in era(e, count)]) for e in (1, 2, 3)}
    verdict('D2', out[1] - out[3] >= 0.010, 0.65, 'outside: era means %.2f, %.2f, %.2f; era 1 less era 3: %.2f points' % (100 * out[1], 100 * out[2], 100 * out[3], 100 * (out[1] - out[3])))
    verdict('D3', ins[1] - ins[3] >= 0.010, 0.55, 'inside: era means %.2f, %.2f, %.2f; era 1 less era 3: %.2f points' % (100 * ins[1], 100 * ins[2], 100 * ins[3], 100 * (ins[1] - ins[3])))
    sh = {e: mean([r['share'] for r in era(e)]) for e in (1, 2, 3)}
    verdict('D4', sh[3] > sh[1], 0.50, 'share of letters inside: era means %.1f%%, %.1f%%, %.1f%%' % (100 * sh[1], 100 * sh[2], 100 * sh[3]))
    p1 = sh[1]
    for r in recs:
        if r['in'][0] == 0: r['Sre'] = r['Sout']; continue
        a_in = r['in'][0] / r['in'][2]; a_out = r['out'][0] / r['out'][2]; w = p1 * a_in / (p1 * a_in + (1 - p1) * a_out)
        r['Sre'] = 1 - (w * r['in'][1] / r['in'][0] + (1 - w) * r['out'][1] / r['out'][0])
    gap = mean([r['Sboth'] for r in era(1)]) - mean([r['Sboth'] for r in era(3)]); gre = mean([r['Sre'] for r in era(1)]) - mean([r['Sre'] for r in era(3)])
    verdict('D5', gre >= 0.8 * gap, 0.55, 'the gap as the books are: %.2f points; with every book at era 1\'s share of speech (%.1f%% of letters): %.2f points, which is %.0f%% of it' % (100 * gap, 100 * p1, 100 * gre, 100 * gre / gap))
    held = sum(ok for _, ok, _ in lines); print('   %d of %d held; Brier score %.3f' % (held, len(lines), sum((o - ok) ** 2 for _, ok, o in lines) / len(lines)))
    json.dump(dict(books=[{k: r[k] for k in ('era', 'year', 'title', 'folder', 'share', 'Sin', 'Sout', 'Sboth', 'Sre')} for r in recs], out=out, ins=ins, share=sh, gap=gap, gap_reweighed=gre, held=held, n=len(lines), left=left),
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[2] if len(sys.argv) > 2 else 'speech-study.json'), 'w'), indent=1)
