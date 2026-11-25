"""Referee's audit of the author's files (read only). Usage: python audit.py /home/agent2/onset"""
import sys, re, json, math
import numpy as np
from scipy import integrate as sint, optimize as sopt
from scipy.stats import spearmanr
from scipy.special import wofz

D = sys.argv[1]
J = lambda f: json.load(open(f"{D}/{f}"))
rng = np.random.default_rng(7)
SIG = math.sqrt(math.pi / 8)
g = lambda w: np.exp(-w * w / (2 * SIG * SIG)) / (SIG * math.sqrt(2 * math.pi))


def th_gauss(K):
    if K <= 1: return 0.0
    F = lambda r: K * sint.quad(lambda x: np.cos(x) ** 2 * g(K * r * np.sin(x)), -np.pi / 2, np.pi / 2)[0] - 1
    return sopt.brentq(F, 1e-7, 1.0)


def th_uniform(K):
    if K <= 1: return 0.0
    gam = np.pi / 4
    G = lambda r: (lambda a: (a * np.sqrt(1 - a * a) + np.arcsin(a)) / (2 * a) - r)(gam / (K * r))
    return sopt.brentq(G, gam / K + 1e-12, 1.0)


th_lor = lambda K: math.sqrt(1 - 1 / K) if K > 1 else 0.0
TH = dict(lorentz=th_lor, gauss=th_gauss, uniform=th_uniform)

print("=== 1. scorecard and Brier scores")
text = open(f"{D}/expectations.md").read()
mine = {m.group(1): float(m.group(2)) for m in re.finditer(r"^(O\d+)\.[\s\S]*?odds (0\.\d+)\s*$", text, re.M)}
ids = [f"O{i}" for i in range(1, 11)]
verd = J("results.json")["verdicts"]
y = np.array([1.0 if verd[i] else 0.0 for i in ids])
me = np.array([mine[i] for i in ids])
F = np.array([[J(f"forecast/f{k}.json")[i] for i in ids] for k in (1, 2, 3)])
med = np.median(F, axis=0)
B = lambda p, yy=y: float(((p - yy) ** 2).mean())
print("mine", me, "median", med)
print(f"Brier: mine {B(me):.4f}; median {B(med):.4f}; each {[round(B(f),4) for f in F]}; mean-of-three odds {B(F.mean(0)):.4f}; flat 0.90 {B(np.full(10,.9)):.4f}; flat at their mean {med.mean():.3f}: {B(np.full(10,med.mean())):.4f}; flat at my mean {me.mean():.3f}: {B(np.full(10,me.mean())):.4f}")
print(f"share of the forecasters' score that is O7 alone: {((med-y)**2)[6]/((med-y)**2).sum():.2f}; of mine: {((me-y)**2)[6]/((me-y)**2).sum():.2f}")
d = (me - y) ** 2 - (med - y) ** 2
bs = [d[rng.integers(0, 10, 10)].mean() for _ in range(20000)]
print(f"difference {d.mean():+.4f}; bootstrap 95%: {np.percentile(bs,2.5):+.3f} to {np.percentile(bs,97.5):+.3f}; share of resamples where the forecasters win: {np.mean(np.array(bs)>0):.2f}")
dm, dt_ = np.abs(me - y), np.abs(med - y)
print(f"closer: mine {int((dm<dt_-1e-9).sum())}, theirs {int((dt_<dm-1e-9).sum())}, equal {int((abs(dm-dt_)<=1e-9).sum())}")
print("if exactly one more line had failed (flip one held line): mine / theirs / who wins")
for j, i in enumerate(ids):
    if y[j] == 1:
        y2 = y.copy(); y2[j] = 0
        print(f"   {i}: {B(me,y2):.4f} / {B(med,y2):.4f}  -> {'forecasters' if B(med,y2)<B(me,y2) else 'author'}")
y2 = y.copy(); y2[6] = 1
print(f"if O7 had held (ten of ten): mine {B(me,y2):.4f} / theirs {B(med,y2):.4f}")
sh = np.minimum(me + (med.mean() - me.mean()), 0.99)
print(f"my odds shifted up by {med.mean()-me.mean():.3f} (capped at 0.99) would score {B(sh):.4f}; rank correlation of my odds with outcome vs theirs: n/a with one failure; my lowest odds on {ids[int(np.argmin(me))]}, their lowest on {ids[int(np.argmin(med))]}")
print("lines on which each forecaster was above/equal/below me:", [(int((f > me).sum()), int((f == me).sum()), int((f < me).sum())) for f in F])

print("\n=== 2. the sheet: points, sweep, rise")
S = J("sheet.json")
for p in S["points"]:
    th = TH[p["shape"]](p["K"])
    extra = f"  N<r^2> = {p['N']*p['r2']:.4f}" if p["K"] == 0.5 else ""
    print(f"   {p['shape']:8s} {p['kind']:8s} N={p['N']} K={p['K']}: r = {p['r']:.5f} (sd {p['sd']:.5f}, {p['runs']} runs)  theory {th:.5f}  gap {p['r']-th:+.5f}{extra}")
up = [s for s in S["sweep"] if s["leg"] == "up"]; down = [s for s in S["sweep"] if s["leg"] == "down"]
dd = {s["K"]: s["r"] for s in down}
print("   sweep K, up, down:")
for s in up:
    print(f"      {s['K']:.2f}  {s['r']:.4f}  {dd.get(s['K'], float('nan')):.4f}")
for q in S["rise"]:
    print(f"   rise K={q['K']}: target {q['target']:.4f}; times sorted: {sorted(q['times'])}")
t12 = np.array([q for q in S["rise"] if q["K"] == 1.2][0]["times"]); t20 = np.array([q for q in S["rise"] if q["K"] == 2.0][0]["times"])
rat = [np.median(t12[rng.integers(0, 20, 20)]) / np.median(t20[rng.integers(0, 20, 20)]) for _ in range(20000)]
print(f"   O9 ratio of medians {np.median(t12)/np.median(t20):.3f}; bootstrap 95% {np.percentile(rat,2.5):.2f} to {np.percentile(rat,97.5):.2f}; share of resamples below 3: {np.mean(np.array(rat)<3):.3f}")
ks = np.array([1.02, 1.05, 1.10])
print(f"   O10: slope from the many-oscillator values themselves: {np.polyfit(np.log(ks-1), np.log([th_gauss(k) for k in ks]), 1)[0]:.4f}")

print("\n=== 3. sizes at K = 1")
for name in ("random", "regular"):
    rows = J(f"sizes-{name}.json")["sizes"]
    N = np.array([q["N"] for q in rows], float); r = np.array([q["r"] for q in rows]); each = [np.array(q["each"]) for q in rows]
    sl = np.polyfit(np.log(N), np.log(r), 1)[0]
    bsl = []
    for _ in range(5000):
        rb = [e[rng.integers(0, len(e), len(e))].mean() for e in each]
        bsl.append(np.polyfit(np.log(N), np.log(rb), 1)[0])
    bsl = np.array(bsl)
    sem = np.array([e.std(ddof=1) / math.sqrt(len(e)) for e in each])
    w = r / sem  # weights for log r
    cw = np.polyfit(np.log(N), np.log(r), 1, w=w)
    chi2 = (((np.log(r) - np.polyval(cw, np.log(N))) * w) ** 2).sum()
    print(f"   {name}: slope {sl:.4f}; bootstrap over runs: sd {bsl.std():.4f}, 95% {np.percentile(bsl,2.5):.3f} to {np.percentile(bsl,97.5):.3f}; share inside the sealed range: "
          f"{np.mean((bsl>=-0.26)&(bsl<=-0.14)) if name=='random' else np.mean((bsl>=-0.46)&(bsl<=-0.30)):.3f}")
    print(f"      weighted fit slope {cw[0]:.4f}, chi2 = {chi2:.1f} on 6 d.o.f.")
    print("      local slopes between neighbours: " + " ".join(f"{np.log(r[i+1]/r[i])/np.log(2):+.2f}" for i in range(7)))
    for lab, sel in (("first four (100-800)", slice(0, 4)), ("last four (1600-12800)", slice(4, 8)), ("six sizes 100-3200", slice(0, 6)), ("six sizes 400-12800", slice(2, 8))):
        b = [np.polyfit(np.log(N[sel]), np.log([e[rng.integers(0, len(e), len(e))].mean() for e in each[sel]]), 1)[0] for _ in range(2000)]
        print(f"      slope over {lab}: {np.polyfit(np.log(N[sel]), np.log(r[sel]), 1)[0]:+.3f} +- {np.std(b):.3f}")
    for q, e in zip(rows, each):
        print(f"      N={q['N']:6d} runs={len(e):4d} mean {e.mean():.4f} se {e.std(ddof=1)/math.sqrt(len(e)):.4f} median {np.median(e):.4f} min {e.min():.4f} max {e.max():.4f}; share of runs below 0.08: {np.mean(e<0.08):.2f}; below 0.055: {np.mean(e<0.055):.2f}")

print("\n=== 4. curves: gap between simulated and the limit, by region")
C = J("curves.json")["curves"]
for shn in ("lorentz", "gauss", "uniform"):
    pts = [p for p in C if p["shape"] == shn]
    gaps = [(p["K"], p["r"], TH[shn](p["K"])) for p in pts]
    for lab, cond in (("K < 1", lambda K: K < 1), ("K = 1", lambda K: K == 1), ("1 < K < 1.1", lambda K: 1 < K < 1.1), ("K >= 1.1", lambda K: K >= 1.1)):
        sel = [(K, r, t) for K, r, t in gaps if cond(K)]
        if not sel: continue
        mx = max(sel, key=lambda x: abs(x[1] - x[2]))
        nd = sum(round(r, 3) != round(t, 3) for K, r, t in sel)
        print(f"   {shn:8s} {lab:12s}: {len(sel):2d} points; largest gap {abs(mx[1]-mx[2]):.4f} at K={mx[0]} (sim {mx[1]:.4f}, limit {mx[2]:.4f}); points that differ when both are rounded to 3 places: {nd}")
print(f"   runs per point: {set(p['runs'] for p in C)}, kinds: {set(p['kind'] for p in C)}, N: {set(p['N'] for p in C)}")

print("\n=== 5. plateau: windows against 1/sqrt(1/r0^2 + (t - t0)/2)")
PL = J("plateau.json")
def wmean(r0, t0, a, b):
    t = np.linspace(a, b, 2001); return float(np.mean(1 / np.sqrt(1 / r0 ** 2 + (t - t0) / 2)))
print(f"   bare formula sqrt(2/t): 300-600 {wmean(1e9,0,300,600):.4f}; 600-1200 {wmean(1e9,0,600,1200):.4f}; 1200-2400 {wmean(1e9,0,1200,2400):.4f}")
for q in PL:
    if q["K"] == 1.0 and q["kind"] == "regular" and q["dt"] == 0.05:
        w = {(a, b): v for a, b, v in q["windows"]}
        # take r0 as the largest early window, t0 its midpoint
        (a0, b0), r0 = max(((k, v) for k, v in w.items() if k[1] <= 300), key=lambda kv: kv[1]); t0 = (a0 + b0) / 2
        line = f"   N={q['N']:6d}: peak window {a0}-{b0} r0={r0:.4f}; "
        for k in ((300, 600), (600, 1200), (1200, 2400)):
            if k in w: line += f"{k[0]}-{k[1]}: seen {w[k]:.4f}, formula {wmean(r0, t0, *k):.4f}; "
        print(line)
print("   peak window value against N^(-1/4): " + "; ".join(f"N={q['N']}: {max(v for a,b,v in q['windows'] if b<=300):.4f} x N^0.25 = {max(v for a,b,v in q['windows'] if b<=300)*q['N']**0.25:.2f}" for q in PL if q['K']==1.0 and q['kind']=='regular' and q['dt']==0.05))

print("\n=== 6. below the onset: linear-response value for a smooth Gaussian, N<r^2> = int g(w)/|eps(w)|^2 dw")
eps = lambda w, K: 1 - (K / 2) * math.sqrt(math.pi / 2) / SIG * wofz(w / (SIG * math.sqrt(2)))
for K in (0.0, 0.25, 0.5, 0.75, 0.9):
    val = sint.quad(lambda w: g(w) / abs(eps(w, K)) ** 2, -12, 12, limit=400)[0]
    print(f"   K={K}: {val:.3f}   (1/(1-K) = {1/(1-K):.3f})")
# the same formula for the Lorentzian, as a check that it returns 1/(1-K)
gl = lambda w: (0.5 / np.pi) / (w * w + 0.25)
epl = lambda w, K: 1 - (K / 2) / (0.5 - 1j * w)
print(f"   check, Lorentzian K=0.5: {sint.quad(lambda w: gl(w)/abs(epl(w,0.5))**2, -np.inf, np.inf)[0]:.4f} (should be 2)")

print("\n=== 7. the piece, from step.json")
P = J("step.json")
st = np.array(P["strikes"]); t = st[:, 0]; bell = st[:, 1].astype(int); pit = st[:, 2]
r = np.array(P["r"]); tr = np.arange(len(r)) * P["r_dt"]; om = np.array(P["omega"])
t1, t2, t3, tend = P["t1"], P["t2"], P["t3"], P["tend"]
print(f"   N={P['N']}, strikes {len(st)}, r_dt={P['r_dt']}, t1,t2,t3,tend = {t1},{t2},{t3},{tend}; periods {2*np.pi/om.max():.2f}-{2*np.pi/om.min():.2f}; Kc at t={t1+(t2-t1)/P['kmax']:.1f}")
print(f"   faster bells lower in pitch? spearman(omega, pitch by bell) = {spearmanr(om, np.array(P['pitch']))[0]:.3f}")
def rolls(a, z, gap=1.0):
    k = np.nonzero((t >= a) & (t < z))[0]; G = [[k[0]]]
    for i in k[1:]:
        (G.append([i]) if t[i] - t[G[-1][-1]] > gap else G[-1].append(i))
    return G
for lab, a, z in (("whole hold 150-185", t2, t3), ("author's window 152-183", t2 + 2, t3 - 2)):
    G = rolls(a, z); full = [gq for gq in G if len(gq) == P["N"] and len(set(bell[gq])) == P["N"]]
    wd = [t[gq[-1]] - t[gq[0]] for gq in full]; rho = [spearmanr(t[gq], pit[gq])[0] for gq in full]; rhob = [spearmanr(t[gq], -om[bell[gq]])[0] for gq in full]
    gp = np.diff([t[gq].mean() for gq in full])
    print(f"   {lab}: groups {len(G)} (sizes {[len(gq) for gq in G]}), complete {len(full)}; width {np.mean(wd):.3f} ({min(wd):.3f}-{max(wd):.3f}); spacing {gp.mean():.3f}; spearman time~pitch {np.mean(rho):.4f} (min {min(rho):.4f}); time~(-omega) {np.mean(rhob):.4f}")
gq = rolls(t2 + 2, t3 - 2)[1]
print("   one roll, bells in order of striking:", list(bell[gq]), "(bell 0 is the fastest)")
for lab, a, z in (("no coupling 0-35", 0, t1), ("hold 150-185", t2, t3), ("release+15 to end", t3 + 15, tend), ("release+5 to +15", t3 + 5, t3 + 15), ("release+30 to end", t3 + 30, tend)):
    k = (tr >= a) & (tr < z); print(f"   r {lab}: mean {r[k].mean():.3f}, min {r[k].min():.3f}, max {r[k].max():.3f}")
print(f"   chance level sqrt(pi/(4N)) = {math.sqrt(math.pi/96):.3f}; rms 1/sqrt(N) = {1/math.sqrt(24):.3f}")
i1 = np.argmax(r > 0.5); print(f"   r first above 0.5 at {tr[i1]:.2f} s: coupling {(tr[i1]-t1)/(t2-t1)*P['kmax']:.3f} x critical; r at K=1.0x: {r[np.argmin(abs(tr-(t1+(t2-t1)/3)))]:.3f}; at 1.5x: {r[np.argmin(abs(tr-(t1+(t2-t1)/2)))]:.3f}")
aft = tr[(tr > t3) & (r < 0.5)][0]; print(f"   after release r<0.5 at {aft:.2f} s ({aft-t3:.2f} s after)")
# what a fan of evenly spaced tempos gives after release with no dynamics at all: phases at release + omega*tau
tau = np.arange(15, tend - t3, 0.05)
# and what random phases give with these 24 tempos: time-average r over a 32 s stretch, many draws
sim = []
for _ in range(2000):
    ph = rng.uniform(0, 2 * np.pi, 24)
    sim.append(np.abs(np.exp(1j * (ph[None, :] + om[None, :] * tau[:, None])).mean(axis=1)).mean())
sim = np.array(sim)
print(f"   random phases, these 24 tempos, r averaged over a stretch of {tau[-1]-tau[0]:.0f} s: mean {sim.mean():.3f}, 2.5%-97.5%: {np.percentile(sim,2.5):.3f}-{np.percentile(sim,97.5):.3f}; share of draws at or below 0.04: {np.mean(sim<=0.04):.4f}")
tau0 = np.arange(0, t1, 0.05); sim0 = []
for _ in range(2000):
    ph = rng.uniform(0, 2 * np.pi, 24); sim0.append(np.abs(np.exp(1j * (ph[None, :] + om[None, :] * tau0[:, None])).mean(axis=1)).mean())
print(f"   random phases, r averaged over the first 35 s: mean {np.mean(sim0):.3f}, 2.5%-97.5%: {np.percentile(sim0,2.5):.3f}-{np.percentile(sim0,97.5):.3f}")
# lead of fast bells in the locked state: theory theta_i - psi = asin((om_i - W0)/(K r))
K3 = P["kc"] * P["kmax"]; W0 = 2 * np.pi / P["period"]
lead = np.arcsin((om - W0) / (K3 * 0.98)); print(f"   locked-state theory at 3 x critical: phase lead from {lead.min():+.3f} to {lead.max():+.3f} rad = spread in time {(lead.max()-lead.min())/W0:.3f} s (the README's roll: 0.52 s)")
