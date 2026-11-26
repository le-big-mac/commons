# How often does the scanner give the reference's pattern?  Texts: the reference's own words with the length marks stripped, j turned to i, and (to imitate an edition that
# begins every line with a capital) the first word's capital treated as unreliable.
import sys, glob, collections; sys.path.insert(0, '/home/agent1/arator')
import scan, gold
def run(files, rounds=4, lex=None, learn=True, label=''):
    G = []
    for f in files: G += gold.load(f)
    lines = [g['text'] for g in G]
    if learn: lex, scans = scan.learn(lines, rounds=rounds, lex=lex, verbose=True)
    else: scans = [scan.scan_line(t, lex) for t in lines]
    n = sum(1 for g in G if g['pat']); got = right = 0; how = collections.Counter(); conf = cright = 0; wrong = []
    for g, sc in zip(G, scans):
        if not g['pat']: continue
        if sc is None or sc['pat'] is None: how['fail'] += 1; continue
        got += 1; ok = sc['pat'] == g['pat']; right += ok; how[sc['how'].split(':')[0] + ('' if ok else ' WRONG')] += 1
        if sc['how'] == 'plain' and (sc['n_ok'] == 1 or sc['margin'] >= 2.5): conf += 1; cright += ok
        if not ok: wrong.append((g, sc))
    print(f'{label}: {len(G)} lines, {n} with a regular reference pattern; scanned {got} ({100 * got / n:.1f}%); same pattern as the reference {right} = {100 * right / n:.2f}% of all, {100 * right / got:.2f}% of those scanned; confident lines {conf}, right {100 * cright / max(conf, 1):.2f}%')
    print('   ', dict(how))
    return lex, G, scans, wrong
if __name__ == '__main__':
    files = [f'/home/agent1/arator/gold/aen{b}.html' for b in range(1, 13)]
    lex, G, scans, wrong = run(files, label='Aeneid, learning from its own lines')
