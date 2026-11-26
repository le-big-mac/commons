"""After the release: how long do the bells stay more evenly spread than chance?
usage: python -I release.py step.json step.npz > release.out      (numpy)
Added 26 November 2026. A reader pointed out that the evenness is a passing thing. After the coupling is switched off at
185 s each bell turns freely, so its phase is known for all later time: theta_j(185) + omega_j (t - 185). The piece ends at 232 s."""
import sys, json, math
sys.dont_write_bytecode = True
import numpy as np

def main(pj, pz):
    d = json.load(open(pj)); om = np.array(d['omega']); N = d['N']; t3 = d['t3']; tend = d['tend']
    ph = np.load(pz)['phases']
    th0 = ph[int(round(t3 * 30))]                      # phases are saved 30 times a second
    rr = np.array(d['r']); tt = np.arange(len(rr)) * d['r_dt']
    def r_at(t):                                       # t: seconds after the release (array)
        return np.abs(np.exp(1j * (th0[None, :] + om[None, :] * t[:, None])).mean(1))
    # check against the piece's own record of r while it lasts
    m = (tt > t3 + 0.5) & (tt < tend)
    print(f"{N} bells. Free turning from the phases at {t3:.0f} s against the piece's own record of r from {t3 + 0.5:.1f} to {tend:.0f} s: largest difference {np.abs(r_at(tt[m] - t3) - rr[m]).max():.4f}")
    chance = math.sqrt(math.pi / (4 * N))
    print(f"chance level for {N} bells with unrelated phases: mean r = {chance:.3f}")
    t = np.arange(0, 20000, 0.05)
    r = r_at(t)
    print("seconds after the release   mean r")
    for lo, hi in ((0, 5), (5, 15), (15, 47), (47, 100), (100, 200), (200, 400), (400, 1000), (1000, 5000), (5000, 20000)):
        k = (t >= lo) & (t < hi)
        print(f"  {lo:6d} to {hi:6d}        {r[k].mean():.3f}" + ("   (the piece ends at 47)" if hi == 47 else ""))
    k = t >= 15
    first = t[k][np.argmax(r[k] > chance)]
    big = t[k][np.argmax(r[k])]
    print(f"first moment after 15 s when r is above the chance level: {first:.0f} s after the release; largest r after 15 s: {r[k].max():.2f} at {big:.0f} s")
    dw = np.abs(np.diff(np.sort(om)))
    print(f"the bells' tempos are {dw.min():.4f} to {dw.max():.4f} rad/s apart from their neighbours; 2 pi over the smallest gap is {2 * math.pi / dw.min():.0f} s")
    # the same bells with phases scattered at random and then left to turn: what a chance start looks like in the same windows
    rng = np.random.default_rng(1)
    tr = np.arange(15, 47, 0.05)
    means = [np.abs(np.exp(1j * (rng.uniform(0, 2 * math.pi, N)[None, :] + om[None, :] * tr[:, None])).mean(1)).mean() for _ in range(2000)]
    means = np.array(means)
    print(f"2,000 random scatterings of the same bells, mean r over the same 15 to 47 s: median {np.median(means):.3f}, lowest {means.min():.3f}; share below the piece's {r[(t >= 15) & (t < 47)].mean():.3f}: {np.mean(means < r[(t >= 15) & (t < 47)].mean()):.4f}")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
