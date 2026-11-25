"""third.py: the six lines of expectations-3.md scored from the four added texts' records and the lines fitted beforehand.
    /usr/bin/python3 -I third.py books-new lines-as-sealed.json   ->  printed; third.json"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study, lines
if __name__ == '__main__':
    new = {r['folder']: lines.measures(r) for r in study.load(sys.argv[1])}; fitted = json.load(open(sys.argv[2])); out = []; MID = 24.27
    def verdict(name, ok, odds, note): out.append((name, bool(ok), odds)); print('   %-3s %-6s (odds %.2f)  %s' % (name, 'HELD' if ok else 'FAILED', odds, note))
    print('The four texts (stories alone)')
    near = {'L': 0, 'S': 0}; rows = {}
    for f, m in new.items():
        row = {}
        for key in ('L', 'S'):
            (a1, b1), (a2, b2) = fitted[key]['year'], fitted[key]['rate']; y = 100 * m[key]; py = a1 + b1 * m['year']; pr = a2 + b2 * m['rate']; row[key] = (y, py, pr); near[key] += abs(y - pr) < abs(y - py)
        rows[f] = row
        print('   %d  %-30s %5.1f shortened forms in a thousand words | L %.2f%% (the year\'s line %.2f, the shortened forms\' line %.2f) | S %.2f%% (%.2f, %.2f)' % (m['year'], m['title'], m['rate'], row['L'][0], row['L'][1], row['L'][2], row['S'][0], row['S'][1], row['S'][2]))
    L = lambda f: rows[f]['L'][0]
    verdict('T1', L('twain-huck-finn-1884') < MID, 0.75, 'Huckleberry Finn %.2f%%, the midpoint %.2f%%' % (L('twain-huck-finn-1884'), MID))
    verdict('T2', L('jerome-three-men-1889') < MID, 0.50, 'Three Men in a Boat %.2f%%' % L('jerome-three-men-1889'))
    verdict('T3', L('hoover-zen-culture-1977') > MID, 0.60, 'Zen Culture %.2f%%' % L('hoover-zen-culture-1977'))
    verdict('T4', L('hoover-zen-experience-1980') > MID, 0.60, 'The Zen Experience %.2f%%' % L('hoover-zen-experience-1980'))
    verdict('T5', near['L'] >= 3, 0.60, 'on L, the shortened forms\' line is the nearer for %d of the four' % near['L'])
    verdict('T6', near['S'] >= 3, 0.55, 'on S, for %d of the four' % near['S'])
    held = sum(ok for _, ok, _ in out); print('   %d of %d held; Brier score %.3f' % (held, len(out), sum((o - ok) ** 2 for _, ok, o in out) / len(out)))
    json.dump(dict(rows=rows, books=list(new.values()), held=held, n=len(out), verdicts=out), open(os.path.join(HERE, 'third.json'), 'w'), indent=1)
