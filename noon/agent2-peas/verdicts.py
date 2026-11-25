"""Scores the fourteen sealed lines against results.json.   usage: python -I verdicts.py expectations.md results.json"""
import sys, re, json
odds = {k: float(v) for k, v in re.findall(r"^(P\d+)\..*?odds (0\.\d+)[ \t]*$", open(sys.argv[1]).read(), re.M | re.S)}; R = json.load(open(sys.argv[2])); G = R['groups']
V = {
 'P1': (abs(G['seven']['chisq'] - 2.14) <= 0.01, f"{G['seven']['chisq']:.4f}"),
 'P2': (abs(G['eight']['chisq'] - 5.17) <= 0.02, f"{G['eight']['chisq']:.4f}"),
 'P3': (R['six_hybrid'] == 399 and R['six_n'] == 600 and 1.6 <= R['six_z_fisher'] <= 2.0, f"{R['six_hybrid']} of {R['six_n']}; {R['six_z_fisher']:+.2f}"),
 'P4': (abs(G['nine kinds']['chisq'] - 2.81) <= 0.02 and G['nine kinds']['df'] == 8, f"{G['nine kinds']['chisq']:.4f}"),
 'P5': (abs(G['27 kinds']['chisq'] - 15.32) <= 0.15, f"{G['27 kinds']['chisq']:.4f}"),
 'P6': (abs(G['twenty plants']['chisq'] - 12.49) <= 0.05, f"{G['twenty plants']['chisq']:.4f}"),
 'P7': (abs(G['back-crosses']['chisq'] - 3.67) <= 0.3 and G['back-crosses']['df'] == 15, f"{G['back-crosses']['chisq']:.4f}"),
 'P8': (abs(R['total'] - 41.6) <= 0.6 and R['df'] == 84, f"{R['total']:.4f} on {R['df']}"),
 'P9': (2e-5 <= R['p_low'] <= 2e-4, f"{R['p_low'] * 1e5:.2f} in 100,000"),
 'P10': (R['max_x1'] < 2.1, f"{R['max_x1']:.4f}"),
 'P11': (5 <= R['small'] <= 9, f"{R['small']}"),
 'P12': (R['lr'] >= 10, f"a factor of {R['lr']:.1f}"),
 'P13': (R['share_shrunk_sim'] > 0.05, f"{100 * R['share_shrunk_sim']:.1f}% of sets"),
 'P14': (0.55 <= R['stopping_mean'] <= 0.90, f"{R['stopping_mean']:.3f}"),
}
tot = 0
for k in sorted(V, key=lambda s: int(s[1:])):
    h = bool(V[k][0]); tot += (odds[k] - h) ** 2; print(f"{k:4s} odds {odds[k]:.2f}  {'held' if h else 'FAILED':6s}  {V[k][1]}")
print(f"held {sum(bool(v[0]) for v in V.values())} of {len(V)}; my mean odds {sum(odds.values()) / len(odds):.3f}; Brier {tot / len(V):.4f}")
