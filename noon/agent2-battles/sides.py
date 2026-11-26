"""What else differs between the world-war rows and the rest of the table?   Added 26 November 2026; rewritten the same day.
usage: python -I sides.py DATADIR > sides.out        (numpy; the CDB90 files that battles.py reads)
After a reader's report, and then after the reader's check of my first use of it. The page's headline was that the
side with more men won 71% of the world-war rows and 51% of the rest, "and all of that is the two world wars".
1. Who attacks. In the world-war rows the attacker is nearly always the bigger side. How much of the gap in the two
   percentages is that? Three reckonings, which do not agree, and the agreement beyond chance in each half.
2. The compilers' judgement of leadership (column leada: above 0 the attacker better led, 0 neither, below 0 the
   defender; the values run from -2 to 3 and the documentation says only "attacker's relative leadership advantage").
   The marks were given by people who knew who won.
3. The size of the engagement.
4. Rows of one war are not independent: whole labels resampled, and each label left out in turn. A label is the
   table's column `war`; in the world-war rows the labels are campaigns, and the same armies recur across them."""
import sys, csv
sys.dont_write_bytecode = True
import numpy as np

def load(D):
    T = {r['isqno']: r for r in csv.DictReader(open(f"{D}/battles.csv", encoding='utf-8'))}
    S = {}
    for r in csv.DictReader(open(f"{D}/belligerents.csv", encoding='utf-8')): S[(r['isqno'], r['attacker'])] = r
    num = lambda s: float(s) if s not in ('', None) else float('nan')
    rows = []
    for q, t in T.items():
        a, d = S[(q, '1')], S[(q, '0')]
        rows.append(dict(q=q, war=t['war'], win=(int(t['wina']) if t['wina'] != '' else None), sa=num(a['str']), sd=num(d['str']),
                         lead=(int(t['leada']) if t['leada'] != '' else None), ww='WORLD WAR' in t['war'].upper()))
    return rows

def auc(sel):
    won = np.array([r['sa'] / r['sd'] for r in sel if r['win'] == 1]); lost = np.array([r['sa'] / r['sd'] for r in sel if r['win'] == -1])
    if len(won) == 0 or len(lost) == 0: return float('nan')
    return float(((won[:, None] > lost[None, :]).sum() + 0.5 * (won[:, None] == lost[None, :]).sum()) / (len(won) * len(lost)))

def bigger(sel):
    k = sum((r['sa'] > r['sd']) == (r['win'] == 1) for r in sel); return k, len(sel)

def pct(k, n): return f"{k} of {n} = {100 * k / n:.1f}%" if n else "none"
share = lambda s: (lambda kn: kn[0] / kn[1] if kn[1] else float('nan'))(bigger(s))

def rates(s):
    """share of rows where the attacker is the bigger side; attackers' win rate when bigger, when smaller, overall"""
    large = [r for r in s if r['sa'] > r['sd']]; small = [r for r in s if r['sa'] < r['sd']]
    w = lambda t: sum(r['win'] == 1 for r in t) / len(t)
    return len(large) / len(s), w(large), w(small), w(s)

def boot(sel, f, rng, draws=2000):
    wars = sorted(set(r['war'] for r in sel)); by = {w: [r for r in sel if r['war'] == w] for w in wars}; out = []
    for _ in range(draws):
        pick = rng.choice(len(wars), len(wars)); v = f([r for i in pick for r in by[wars[i]]])
        if np.isfinite(v): out.append(v)
    return np.percentile(out, 2.5), np.percentile(out, 97.5)

def leave_one(sel, f):
    wars = sorted(set(r['war'] for r in sel)); v = [f([r for r in sel if r['war'] != w]) for w in wars]
    return min(v), max(v)

if __name__ == '__main__':
    rows = load(sys.argv[1]); rng = np.random.default_rng(2611)
    ok = lambda r: np.isfinite(r['sa']) and np.isfinite(r['sd']) and r['sa'] > 0 and r['sd'] > 0
    dec = [r for r in rows if r['win'] in (1, -1) and ok(r) and r['sa'] != r['sd']]
    W = [r for r in dec if r['ww']]; O = [r for r in dec if not r['ww']]; G = (("world-war rows", W), ("all other rows", O))
    print(f"{len(dec)} decisive battles with unequal strengths")
    print("1. who attacks")
    for name, s in G:
        k, n = bigger(s); pb, wl, ws, wa = rates(s); indep = pb * wa + (1 - pb) * (1 - wa)
        print(f"   {name}: the bigger side won {pct(k, n)}; the attacker was the bigger side in {100 * pb:.1f}%; attackers won {100 * wa:.1f}% ({100 * wl:.1f}% with more men, {100 * ws:.1f}% with fewer);"
              f" ranking by force ratio {auc(s):.2f}; if an attacker's chance owed nothing to numbers the bigger side would win {100 * indep:.1f}%; agreement beyond that chance {(k / n - indep) / (1 - indep):+.2f}")
    (pbw, wlw, wsw, waw), (pbo, wlo, wso, wao) = rates(W), rates(O); gap = share(W) - share(O)
    A = share(W) - (pbo * wlw + (1 - pbo) * (1 - wsw))            # world-war rates kept, the others' mix of who attacks
    B = (pbw * wlo + (1 - pbw) * (1 - wso)) - share(O)            # the others' rates kept, the world wars' mix
    wall = sum(r['win'] == 1 for r in dec) / len(dec)
    C = (pbw * wall + (1 - pbw) * (1 - wall)) - (pbo * wall + (1 - pbo) * (1 - wall))     # one attackers' rate for all, each half's mix
    Dd = (pbw * waw + (1 - pbw) * (1 - waw)) - (pbo * wao + (1 - pbo) * (1 - wao))        # each half's own attackers' rate
    print(f"   the gap between the two shares is {100 * gap:.1f} points. Of it, who attacks accounts for: {100 * A / gap:.0f}% with the world wars' own win rates kept and the others' mix of attackers;"
          f" {100 * B / gap:.0f}% the other way about; {100 * C / gap:.0f}% with one attackers' win rate for the whole table; {100 * Dd / gap:.0f}% with each half's own")
    print("2. the compilers' leadership marks")
    for name, s in G:
        coded = [r for r in s if r['lead'] is not None]; marked = [r for r in coded if r['lead'] != 0]
        print(f"   {name}: one side marked as better led in {pct(len(marked), len(coded))} of the rows with a mark")
        for lab, t in (('attacker better led', [r for r in coded if r['lead'] > 0]), ('neither', [r for r in coded if r['lead'] == 0]), ('defender better led', [r for r in coded if r['lead'] < 0])):
            k, n = bigger(t)
            print(f"      {lab}: {len(t)} rows; the bigger side won {pct(k, n)}; attackers won {pct(sum(r['win'] == 1 for r in t), len(t))}; ranking by force ratio {auc(t):.2f}")
        up = [r for r in s if (r['sa'] > r['sd']) != (r['win'] == 1)]; ex = [r for r in s if (r['sa'] > r['sd']) == (r['win'] == 1)]
        winner_marked = lambda t: sum(r['lead'] is not None and r['lead'] * r['win'] > 0 for r in t)
        print(f"      the winner is the side marked as better led in {pct(winner_marked(up), len(up))} of the battles the smaller side won, and in {pct(winner_marked(ex), len(ex))} of those the bigger side won")
    print("3. the size of the engagement (the two sides' men together)")
    tot = np.array([r['sa'] + r['sd'] for r in dec]); cuts = np.percentile(tot, [25, 50, 75])
    for name, s in G:
        parts = []
        for lo, hi in zip([0, *cuts], [*cuts, np.inf]):
            t = [r for r in s if lo <= r['sa'] + r['sd'] < hi]; k, n = bigger(t); parts.append(f"{k}/{n}" + (f" ({100 * k / n:.0f}%)" if n else ""))
        print(f"   {name}, by quarter of all battles' size (cuts at {', '.join(f'{c:,.0f}' for c in cuts)} men): " + ", ".join(parts))
    print("4. dependence: whole labels resampled 2,000 times (95% intervals), and each label left out in turn (least to most)")
    for name, s in G:
        lo, hi = boot(s, share, rng); a, b = leave_one(s, share)
        big = max(set(r['war'] for r in s), key=lambda w: sum(r['war'] == w for r in s))
        print(f"   {name}: the bigger side's share {100 * lo:.0f} to {100 * hi:.0f}% resampled; {100 * a:.0f} to {100 * b:.0f}% leaving one out; {len(set(r['war'] for r in s))} labels, the largest {big.title()} with {sum(r['war'] == big for r in s)} rows")
        z = [r for r in s if r['lead'] == 0]
        lo, hi = boot(z, share, rng); a, b = leave_one(z, share)
        big = max(set(r['war'] for r in z), key=lambda w: sum(r['war'] == w for r in z))
        print(f"      rows with neither side marked: {100 * lo:.0f} to {100 * hi:.0f}% resampled; {100 * a:.0f} to {100 * b:.0f}% leaving one out; {len(set(r['war'] for r in z))} labels, the largest {big.title()} with {sum(r['war'] == big for r in z)} of {len(z)} rows")
    three = [r for r in rows if r['win'] in (1, -1, 0) and ok(r) and r['sa'] / r['sd'] >= 3]
    print(f"5. attackers at three to one or more, draws counted as not won: {pct(sum(r['win'] == 1 for r in three), len(three))}")
