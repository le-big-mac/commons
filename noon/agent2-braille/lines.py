"""lines.py: two rival lines through the eighteen novels (stories alone): the share saved against the year, and against
how many of a book's words are shortened forms of speech (n't, 'll, 've, 're, 'd, 'm). The referee's point: the second
explains these books at least as well as the first, and the year adds nothing once it is known.
    /usr/bin/python3 -I lines.py books-story [books-new]   ->  printed; lines.json"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study, story
def fit(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; sxx = sum((x - mx) ** 2 for x in xs); b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx; a = my - b * mx
    res = sum((y - a - b * x) ** 2 for x, y in zip(xs, ys)); tot = sum((y - my) ** 2 for y in ys); return a, b, 1 - res / tot, math.sqrt(res / (n - 2) / sxx)
def fit2(x1, x2, ys):
    """y = a + b1 x1 + b2 x2 by least squares; returns b1, b2, their standard errors and r squared"""
    n = len(ys); m1 = sum(x1) / n; m2 = sum(x2) / n; my = sum(ys) / n; u = [x - m1 for x in x1]; v = [x - m2 for x in x2]; w = [y - my for y in ys]
    s11 = sum(a * a for a in u); s22 = sum(a * a for a in v); s12 = sum(a * b for a, b in zip(u, v)); s1y = sum(a * b for a, b in zip(u, w)); s2y = sum(a * b for a, b in zip(v, w)); det = s11 * s22 - s12 ** 2
    b1 = (s22 * s1y - s12 * s2y) / det; b2 = (s11 * s2y - s12 * s1y) / det; res = sum((c - b1 * a - b2 * b) ** 2 for a, b, c in zip(u, v, w)); s2 = res / (n - 3)
    return b1, b2, math.sqrt(s2 * s22 / det), math.sqrt(s2 * s11 / det), 1 - res / sum(c * c for c in w)
def measures(r):
    u = r['ueb']; return dict(S=(u['U'] - u['C']) / u['U'], L=(u['U'] - u['C']) / (u['letters'] + u['words']), rate=1000 * story.short_forms(u['vocab']) / u['words'], year=r['year'], title=r['title'], era=r['era'])
if __name__ == '__main__':
    ms = [measures(r) for r in study.load(sys.argv[1]) if r['era'] in (1, 2, 3)]; out = dict(books=ms)
    print('Shortened forms of speech in a thousand words, and the share saved (stories alone)')
    for m in sorted(ms, key=lambda m: m['year']): print('   %d  %-34s %5.1f in a thousand   S %.2f%%   on letters and spaces %.2f%%' % (m['year'], m['title'], m['rate'], 100 * m['S'], 100 * m['L']))
    for key, name in (('S', 'the share of all cells'), ('L', 'the share on letters and one space a word')):
        ys = [100 * m[key] for m in ms]; yr = [m['year'] for m in ms]; rt = [m['rate'] for m in ms]
        a1, b1, r1, se1 = fit(yr, ys); a2, b2, r2, se2 = fit(rt, ys); c1, c2, s1, s2, r12 = fit2(yr, rt, ys)
        print('%s:' % name)
        print('   against the year:            %.3f points a century (standard error %.3f); r squared %.2f' % (100 * b1, 100 * se1, r1))
        print('   against shortened forms:     %.3f points for each one in a thousand words (standard error %.3f); r squared %.2f' % (b2, se2, r2))
        print('   against both:                the year %.3f points a century (%.3f); shortened forms %.3f (%.3f); r squared %.2f' % (100 * c1, 100 * s1, c2, s2, r12))
        out[key] = dict(year=(a1, b1), rate=(a2, b2), r2_year=r1, r2_rate=r2, both=(c1, c2, s1, s2, r12))
    if len(sys.argv) > 2:
        new = [measures(r) for r in study.load(sys.argv[2])]; out['new'] = new
        print('The four added texts, and what each line said of them (share on letters and one space a word; then the share of all cells)')
        for m in new:
            row = []
            for key in ('L', 'S'):
                (a1, b1), (a2, b2) = out[key]['year'], out[key]['rate']; py = a1 + b1 * m['year']; pr = a2 + b2 * m['rate']; row.append((100 * m[key], py, pr))
            m['pred'] = row
            print('   %d  %-30s %5.1f shortened forms in a thousand | measured %.2f%%, the year\'s line %.2f, the shortened forms\' line %.2f | all cells: measured %.2f%%, %.2f, %.2f' % (m['year'], m['title'], m['rate'], row[0][0], row[0][1], row[0][2], row[1][0], row[1][1], row[1][2]))
    json.dump(out, open(os.path.join(HERE, 'lines.json'), 'w'), indent=1)
