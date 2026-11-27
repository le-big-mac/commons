"""cmutants.py: break pcore.js, search.c and merge.py on purpose, one fault at a time, and run ctest.js on each
broken copy. A fault the tests do not notice is a hole in the tests. First of all a control: an unbroken copy
must pass, or "caught" would mean nothing.     python -I cmutants.py
"""
import os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'mutants')
FILES = ['pcore.js', 'ctest.js', 'search.c', 'merge.py']
M = [
 # --- pcore.js ---
 ('plain-misses-exact-coin', 'pcore.js', "for (i = 0; i < c.length && c[i] <= a; i++) {\n        v = m[a - c[i]] + 1;", "for (i = 0; i < c.length && c[i] < a; i++) {\n        v = m[a - c[i]] + 1;"),
 ('plain-takes-largest-first-only', 'pcore.js', "        if (v < best) best = v;\n      }\n      m[a] = best;", "        best = v;\n      }\n      m[a] = best;"),
 ('greedy-smallest-first', 'pcore.js', "      r = a; n = 0;\n      for (i = c.length - 1; i >= 0; i--) {", "      r = a; n = 0;\n      for (i = 0; i < c.length; i++) {"),
 ('greedy-stuck-unnoticed', 'pcore.js', "g[a] = r === 0 ? n : INF;", "g[a] = n;"),
 ('greedyway-stuck-unnoticed', 'pcore.js', "return r === 0 ? out : null;", "return out;"),
 ('both-no-sum-below-zero', 'pcore.js', "var lo = -(cmax - 1), hi = (L - 1) + (cmax - 1), size = hi - lo + 1;", "var lo = 0, hi = (L - 1) + (cmax - 1), size = hi - lo + 1;"),
 ('both-no-sum-above-range', 'pcore.js', "var lo = -(cmax - 1), hi = (L - 1) + (cmax - 1), size = hi - lo + 1;", "var lo = -(cmax - 1), hi = (L - 1), size = hi - lo + 1;"),
 ('both-window-half', 'pcore.js', "var lo = -(cmax - 1), hi = (L - 1) + (cmax - 1), size = hi - lo + 1;", "var lo = -Math.floor(cmax / 2), hi = (L - 1) + Math.floor(cmax / 2), size = hi - lo + 1;"),
 ('both-never-hands-back', 'pcore.js', "        y = x - c[i];\n        if (y >= 0 && dist[y] === INF) { dist[y] = d; queue[tail++] = y; }\n      }\n    }\n    for (a = 0; a < L; a++) out[a] = dist[a - lo];", "      }\n    }\n    for (a = 0; a < L; a++) out[a] = dist[a - lo];"),
 ('both-counts-one-too-many', 'pcore.js', "x = queue[head++]; d = dist[x] + 1;", "x = queue[head++]; d = dist[x] + (dist[x] > 2 ? 2 : 1);"),
 ('counts-greedy-is-plain', 'pcore.js', "if (mode === 'greedy') return greedy(coins, L);", "if (mode === 'greedy') return plain(coins, L);"),
 ('total-ignores-cannot', 'pcore.js', "for (a = 0; a < m.length; a++) { if (m[a] >= INF) return Infinity; s += m[a]; }", "for (a = 0; a < m.length; a++) { if (m[a] >= INF) continue; s += m[a]; }"),
 ('worst-is-least', 'pcore.js', "if (m[a] > w) w = m[a]; }", "if (m[a] < w || w === 0) w = m[a]; }"),
 ('greedyfails-counts-ties', 'pcore.js', "if (g[a] > p[a]) out.push(a);", "if (g[a] >= p[a]) out.push(a);"),
 ('pearson-skips-first-j', 'pcore.js', "for (j = i; j < n; j++) {\n        w = 0; size = 0;", "for (j = i + 1; j < n; j++) {\n        w = 0; size = 0;"),
 ('pearson-from-the-coin-itself', 'pcore.js', "g = vec(c[i - 1] - 1);", "g = vec(c[i - 1]);"),
 ('pearson-takes-largest', 'pcore.js', "(best === 0 || w < best)) best = w;", "(best === 0 || w > best)) best = w;"),
 ('pearson-no-extra-coin', 'pcore.js', "w += c[j]; size += 1;", "w += c[j]; size += 2;"),
 ('firstfailure-stops-early', 'pcore.js', "top = c[n - 1] + c[n - 2];", "top = c[n - 1];"),
 ('bestadd-worst-first', 'pcore.js', "return p.total - q.total || p.coin - q.coin; });", "return q.total - p.total || p.coin - q.coin; });"),
 ('bestadd-ties-largest-first', 'pcore.js', "return p.total - q.total || p.coin - q.coin; });", "return p.total - q.total || q.coin - p.coin; });"),
 ('bestadd-offers-coins-already-there', 'pcore.js', "      if (have[v]) continue;\n", ""),
 ('bestadd-misses-the-last', 'pcore.js', "for (v = 1; v <= maxCoin; v++) {", "for (v = 1; v < maxCoin; v++) {"),
 ('plainway-any-coin', 'pcore.js', "if (c[i] <= a && m[a - c[i]] === m[a] - 1)", "if (c[i] <= a && m[a - c[i]] < INF)"),
 ('schemes-never-hand-back', 'pcore.js', "for (v = left; v >= -left; v--) {", "for (v = left; v >= 0; v--) {"),
 ('schemes-prune-too-hard', 'pcore.js', "else if (Math.abs(r2) > lim * desc[idx + 1]) continue;", "else if (Math.abs(r2) >= lim * desc[idx + 1]) continue;"),
 ('schemes-one-over-the-limit', 'pcore.js', "if (out.length < limit) {", "if (out.length <= limit) {"),
 ('schemes-never-give-up', 'pcore.js', "if (++steps > budget) { gaveUp = true; return; }", "++steps;"),
 ('schemes-count-only-kept', 'pcore.js', "return { count: k, ways: out, more: more || gaveUp, total: found, gaveUp: gaveUp };", "return { count: k, ways: out, more: more || gaveUp, total: out.length, gaveUp: gaveUp };"),
 ('signed-lists-not-doubled', 'pcore.js', "binom(k - 1, j - 1) * Math.pow(2, j);", "binom(k - 1, j - 1) * 2 * j;"),
 ('bound-both-not-halved', 'pcore.js', "n = mode === 'plain' ? multisets(D, k) : signedLists(D, k) / 2;", "n = mode === 'plain' ? multisets(D, k) : signedLists(D, k);"),
 ('bound-counts-zero', 'pcore.js', "var left = L - 1, k = 1, s = 0, n;", "var left = L, k = 1, s = 0, n;"),
 ('bound-modes-swapped', 'pcore.js', "n = mode === 'plain' ? multisets(D, k) : signedLists(D, k) / 2;", "n = mode !== 'plain' ? multisets(D, k) : signedLists(D, k) / 2;"),
 ('multisets-one-short', 'pcore.js', "function multisets(D, k) { return binom(D + k - 1, k); }", "function multisets(D, k) { return binom(D + k - 2, k); }"),
 ('meantext-about-everything', 'pcore.js', "return (exact ? '' : 'about ') + s;", "return 'about ' + s;"),
 ('meantext-never-about', 'pcore.js', "return (exact ? '' : 'about ') + s;", "return s;"),
 # added 27 November 2026, with the function's rounding
 ('meantext-machine-rounding', 'pcore.js', "var s = (n / scale).toFixed(places);", "var s = (tot / L).toFixed(places);"),
 ('meantext-rounds-down', 'pcore.js', "n = Math.floor((2 * tot * scale + L) / (2 * L)), exact", "n = Math.floor(tot * scale / L), exact"),
 ('meantext-half-goes-down', 'pcore.js', "n = Math.floor((2 * tot * scale + L) / (2 * L)), exact", "n = Math.ceil((2 * tot * scale - L) / (2 * L)), exact"),
 ('meantext-always-three-places', 'pcore.js', "var scale = Math.pow(10, places), n", "var scale = 1000, n"),
 ('clean-keeps-repeats', 'pcore.js', "if (!seen[c]) { seen[c] = 1; out.push(c); }", "out.push(c);"),
 ('clean-takes-fractions', 'pcore.js', "|| c !== Math.floor(c) ||", "||"),
 ('pearson-without-one', 'pcore.js', "    if (asc[0] !== 1) throw new Error('the test needs a coin of 1');\n    for (i = 0; i < n; i++) c.push(asc[n - 1 - i]);", "    for (i = 0; i < n; i++) c.push(asc[n - 1 - i]);"),
 # --- search.c ---
 ('c-plain-misses-top-coin', 'search.c', "    for (c = from; c <= M - (D - 1 - d); c++) {\n        if (d == 1 && FIRST && c != FIRST) continue;\n        coin[d] = c;\n        for (a = 0; a < L; a++) {\n            int v = old[a];",
    "    for (c = from; c < M - (D - 1 - d); c++) {\n        if (d == 1 && FIRST && c != FIRST) continue;\n        coin[d] = c;\n        for (a = 0; a < L; a++) {\n            int v = old[a];"),
 ('c-plain-one-coin-once', 'search.c', "if (a >= c && nw[a - c] + 1 < v) v = nw[a - c] + 1;", "if (a >= c && old[a - c] + 1 < v) v = old[a - c] + 1;"),
 ('c-greedy-wrong-rest', 'search.c', "for (a = 0; a < L; a++) nw[a] = a / c + old[a % c];", "for (a = 0; a < L; a++) nw[a] = a / c + old[a % c > 0 ? a % c - 1 : 0] + (a % c > 0);"),
 ('c-leaf-keeps-first-only', 'search.c', "    if (s == bestTotal) {\n        if (nBest < KEEP) memcpy(bestSets[nBest++], coin, sizeof(int) * D);\n        nBestAll++;\n    }", "    if (s == bestTotal && nBest == 0) {\n        if (nBest < KEEP) memcpy(bestSets[nBest++], coin, sizeof(int) * D);\n        nBestAll++;\n    }"),
 ('c-leaf-counts-cannot', 'search.c', "for (a = 0; a < L; a++) { if (t[a] >= INF) return; s += t[a]; if (t[a] > w) w = t[a]; }", "for (a = 0; a < L; a++) { if (t[a] >= INF) continue; s += t[a]; if (t[a] > w) w = t[a]; }"),
 ('c-worst-ties-uncounted', 'search.c', "    if (w == bestWorst) nWorst++;", "    if (w == bestWorst && nWorst == 0) nWorst++;"),
 ('c-both-never-hands-back', 'search.c', "            y = x - coin[i]; if (y >= 0 && dist[y] == INF) { dist[y] = d; queue[tail++] = y; }\n", ""),
 ('c-both-window-short', 'search.c', "int cmax = coin[D - 1], lo = -(cmax - 1), size = (L - 1) + (cmax - 1) - lo + 1;", "int cmax = coin[D - 1], lo = -(cmax - 1), size = (L - 1) - lo + 1;"),
 ('c-both-needs-a-one', 'search.c', "        recBoth(0, 1);", "        coin[0] = 1; recBoth(1, 2);"),
 ('c-first-ignored-plain', 'search.c', "        if (d == 1 && FIRST && c != FIRST) continue;\n        coin[d] = c;\n        for (a = 0; a < L; a++) {\n            int v = old[a];", "        coin[d] = c;\n        for (a = 0; a < L; a++) {\n            int v = old[a];"),
 ('c-first-ignored-both', 'search.c', "        if (d == 0 && FIRST && c != FIRST) continue;\n", ""),
 ('c-one-alone-off', 'search.c', "for (a = 0; a < L; a++) tab[1][a] = a;", "for (a = 0; a < L; a++) tab[1][a] = a + (a > 0);"),
 # --- merge.py ---
 ('merge-takes-largest-total', 'merge.py', "if tot is None or t < tot: tot, best, nbest = t, [], 0", "if tot is None or t > tot: tot, best, nbest = t, [], 0"),
 ('merge-forgets-ties', 'merge.py', "if t == tot: best += b; nbest += nb", "if t == tot: best = b; nbest = nb"),
 ('merge-sets-not-summed', 'merge.py', "n = int(re.search(r'sets scored (\\d+)', s).group(1)); sets += n", "n = int(re.search(r'sets scored (\\d+)', s).group(1)); sets = n"),
 ('merge-worst-count-not-summed', 'merge.py', "if w == worst: nworst += nw", "if w == worst: nworst = nw"),
]
def build(name, f, old, new):
    d = os.path.join(WORK, name); os.makedirs(d, exist_ok=True)
    for x in FILES:
        s = open(os.path.join(HERE, x), encoding='utf-8').read()
        if x == f:
            if s.count(old) != 1: raise SystemExit('mutant %s: pattern found %d times in %s' % (name, s.count(old), f))
            s = s.replace(old, new)
        open(os.path.join(d, x), 'w', encoding='utf-8').write(s)
    r = subprocess.run(['gcc', '-O2', '-o', os.path.join(d, 'search'), os.path.join(d, 'search.c')], capture_output=True, text=True)
    if r.returncode: raise SystemExit('mutant %s does not compile: %s' % (name, r.stderr[:300]))
    return d
def run(d):
    try:
        r = subprocess.run(['node', os.path.join(d, 'ctest.js')], capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        return 1, ['TIMEOUT']
    return r.returncode, [l for l in r.stdout.split('\n') if l.startswith('FAIL')] + ([r.stderr.strip().split('\n')[-1][:150]] if r.returncode and r.stderr.strip() else [])
if __name__ == '__main__':
    if os.path.isdir(WORK): shutil.rmtree(WORK)
    code, fails = run(build('CONTROL', None, None, None))
    print('control (nothing broken): %s' % ('passes' if code == 0 else 'FAILS: ' + '; '.join(fails)), flush=True)
    if code != 0: sys.exit('the control does not pass; nothing below would mean anything')
    caught = 0; passed = []
    for name, f, old, new in M:
        code, fails = run(build(name, f, old, new))
        if code != 0: caught += 1; print('caught   %-36s by %d: %s' % (name, len(fails), (fails[0] if fails else '')[:110]), flush=True)
        else: passed.append(name); print('PASSED   %s' % name, flush=True)
    code, fails = run(build('CONTROL-AFTER', None, None, None))
    print('control again, after the last: %s' % ('passes' if code == 0 else 'FAILS: ' + '; '.join(fails)))
    print('\n%d of %d broken copies caught; passed: %s' % (caught, len(M), ', '.join(passed) or 'none'))
