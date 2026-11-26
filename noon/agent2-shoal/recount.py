"""A recount of this study's own records, after a reader found that the page said more than they hold.
usage: python -I recount.py > recount.out      (standard library; run in this folder)   Added 26 November 2026."""
import json, sys
sys.dont_write_bytecode = True

if __name__ == '__main__':
    trend = json.load(open('trend.json')); longr = json.load(open('long.json')); sweep = json.load(open('sweep.json'))
    lab = lambda p, m: 'A' if p > .65 and p > m else ('M' if m > .5 else '.')
    print("1. the forty-seed runs (my rule, trend.json): 280 schools")
    split = [r for r in trend if r[4] > 1]; whole = [r for r in trend if r[4] == 1]
    print(f"   split into more than one group: {len(split)} of {len(trend)}; largest group {sum(r[3] for r in trend) / len(trend):.1f} fish on average, {min(r[3] for r in trend)} at the least")
    print(f"   mills among the schools that stayed whole: {sum(r[2] == 'M' for r in whole)} of {len(whole)}; among those that split: {sum(r[2] == 'M' for r in split)} of {len(split)}")
    print(f"   neither state: {sum(r[2] == '.' for r in trend)}")
    print(f"   of the {len(split)} that split: the largest group still held 98 or more of the 100 fish in {sum(r[3] >= 98 for r in split)}; the largest group held fewer than 90 in {sum(r[3] < 90 for r in trend)} of all {len(trend)}, and 50 or fewer in {sum(r[3] <= 50 for r in trend)}")
    print("2. the long runs (long.json): 24 schools, 60 checks each")
    checks = ''.join(r[2] for r in longr)
    print(f"   checks that were neither state: {checks.count('.')} of {len(checks)}")
    same = [r for r in longr if len(set(r[2])) == 1]
    print(f"   schools with one label at all 60 checks: {len(same)} of {len(longr)}")
    for r in longr:
        if len(set(r[2])) > 1:
            s = r[2]; print(f"   width {r[0]}, seed {r[1]}: mill {s.count('M')}, aligned {s.count('A')}, neither {s.count('.')}; first {s[0]}, last {s[-1]}; " + ("crossed between mill and aligned" if 'M' in s and 'A' in s else "never crossed"))
    print(f"   last check: mills {sum(r[2][-1] == 'M' for r in longr)}, aligned {sum(r[2][-1] == 'A' for r in longr)}, neither {sum(r[2][-1] == '.' for r in longr)}; at width 6.0: mills {sum(r[2][-1] == 'M' for r in longr if r[0] == 6.0)} of {sum(1 for r in longr if r[0] == 6.0)}")
    print("3. the first sweep (sweep.json): six seeds a width")
    for lo, hi in ((0.5, 1.0), (1.5, 8.0), (1.5, 5.0), (5.5, 8.0)):
        rs = [r for r in sweep if lo <= r[0] <= hi]; L = [lab(r[2], r[3]) for r in rs]
        print(f"   widths {lo} to {hi}: {len(rs)} schools; mills {L.count('M')}, aligned {L.count('A')}, neither {L.count('.')}" + ("; the in-between ones (alignment/rotation): " + ", ".join(f"{r[2]:.2f}/{r[3]:.2f}" for r, l in zip(rs, L) if l == '.') if '.' in L else ""))
    m1 = sum(lab(r[2], r[3]) == 'M' for r in sweep if 5.5 <= r[0] <= 8.0); n1 = sum(1 for r in sweep if 5.5 <= r[0] <= 8.0)
    m2 = sum(r[2] == 'M' for r in trend if r[0] in (6, 7, 8)); n2 = sum(1 for r in trend if r[0] in (6, 7, 8))
    p = (m1 + m2) / (n1 + n2); z = (m2 / n2 - m1 / n1) / (p * (1 - p) * (1 / n1 + 1 / n2)) ** 0.5
    print(f"   mills at widths 5.5 to 8.0 in the sweep: {m1} of {n1}; at widths 6 to 8 in the forty-seed runs: {m2} of {n2}; the two shares differ by {z:.2f} standard errors")
    mills = [r for r in sweep if lab(r[2], r[3]) == 'M' and r[0] >= 1.5]; al = [r for r in sweep if lab(r[2], r[3]) == 'A' and r[0] >= 1.5]
    print(f"   mills at widths 1.5 to 8: rotation {min(r[3] for r in mills):.2f} to {max(r[3] for r in mills):.2f}, alignment {min(r[2] for r in mills):.2f} to {max(r[2] for r in mills):.2f}; aligned schools: alignment {min(r[2] for r in al):.2f} to {max(r[2] for r in al):.2f}")
    # added after a reader's third pass (26 November): the sealed run of the paper's rule, kind by kind
    import os
    if os.path.exists('rule.json'):
        rule = json.load(open('rule.json')); pr = rule['printed']
        rng = lambda v: f"{min(v):.2f} to {max(v):.2f}, mean {sum(v) / len(v):.2f}" if v else "none"
        print("4. the paper's rule (rule.json, 'printed'): 40 schools a width; each row is width, mills / aligned / neither")
        for w in sorted(set(r[0] for r in pr)):
            rs = [r for r in pr if r[0] == w]; M = [r for r in rs if r[2] == 'M']; A = [r for r in rs if r[2] == 'A']; N = [r for r in rs if r[2] == '.']
            print(f"   width {w}: {len(M)} / {len(A)} / {len(N)}; mills: rotation {rng([r[6] for r in M])}, alignment {rng([r[5] for r in M])}, with rotation under 0.6: {sum(r[6] < 0.6 for r in M)};"
                  f" aligned: alignment {rng([r[5] for r in A])}; neither: alignment {rng([r[5] for r in N])}, rotation {rng([r[6] for r in N])}")
        tun = lambda a, m: 'P' if a > .65 and m < .35 else ('M' if a < .35 and m > .65 else ('S' if a < .35 and m < .35 else 'T'))
        print("   the same runs by the cut-offs of Tunstrom and others (2013), set for their own fish: polar (alignment over 0.65, rotation under 0.35) / mill (under 0.35, over 0.65) / swarm (both under 0.35) / transitional (the rest)")
        for w in sorted(set(r[0] for r in pr)):
            L = [tun(r[5], r[6]) for r in pr if r[0] == w]
            print(f"   width {w}: {L.count('P')} / {L.count('M')} / {L.count('S')} / {L.count('T')}")
        Mp = [r for r in pr if r[2] == 'M']; Mv = [r for r in trend if r[2] == 'M']
        print(f"   all mills under the paper's rule: alignment mean {sum(r[5] for r in Mp) / len(Mp):.2f}, rotation mean {sum(r[6] for r in Mp) / len(Mp):.2f}; mills under my variant in the control runs of that batch: "
              + (lambda c: f"alignment mean {sum(r[5] for r in c) / len(c):.2f}, rotation mean {sum(r[6] for r in c) / len(c):.2f} ({len(c)} mills of {len(rule['control'])} control runs)")([r for r in rule['control'] if r[2] == 'M']))
