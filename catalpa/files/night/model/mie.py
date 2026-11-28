# Scattering of light by a sphere (Mie's solution), after the routine printed by Bohren and Huffman (1983), and its
# average over a log-normal spread of sizes. Used for the droplets of the stratospheric haze.
import numpy as np
def mie(m, x, mu):
    """one sphere: refractive index m (may be complex), size parameter x = 2 pi r / wavelength, cosines mu.
    Returns Qext, Qsca, g and the unpolarized intensity function (|S1|^2 + |S2|^2) / 2 at each mu."""
    mu = np.asarray(mu, float); nstop = int(x + 4.0 * x ** (1.0 / 3.0) + 2.0); y = m * x; nmx = int(max(nstop, abs(y)) + 15)
    D = np.zeros(nmx + 1, complex)
    for n in range(nmx, 0, -1): D[n - 1] = n / y - 1.0 / (D[n] + n / y)
    psi0, psi1 = np.cos(x), np.sin(x); chi0, chi1 = -np.sin(x), np.cos(x); xi1 = complex(psi1, -chi1)
    pi0 = np.zeros_like(mu); pi1 = np.ones_like(mu); S1 = np.zeros_like(mu, complex); S2 = np.zeros_like(mu, complex)
    qsca = 0.0; qext = 0.0; gs = 0.0; an1 = 0j; bn1 = 0j
    for n in range(1, nstop + 1):
        psi = (2 * n - 1) / x * psi1 - psi0; chi = (2 * n - 1) / x * chi1 - chi0; xi = complex(psi, -chi)
        an = ((D[n] / m + n / x) * psi - psi1) / ((D[n] / m + n / x) * xi - xi1)
        bn = ((m * D[n] + n / x) * psi - psi1) / ((m * D[n] + n / x) * xi - xi1)
        qsca += (2 * n + 1) * (abs(an) ** 2 + abs(bn) ** 2); qext += (2 * n + 1) * (an + bn).real
        if n > 1: gs += ((n - 1) * (n + 1) / n) * (an1 * np.conj(an) + bn1 * np.conj(bn)).real
        if n >= 1: gs += ((2 * n - 1) / ((n - 1) * n)) * (an1 * np.conj(bn1)).real if n > 1 else 0.0
        tau = n * mu * pi1 - (n + 1) * pi0; fn = (2 * n + 1) / (n * (n + 1.0))
        S1 += fn * (an * pi1 + bn * tau); S2 += fn * (an * tau + bn * pi1)
        psi0, psi1 = psi1, psi; chi0, chi1 = chi1, chi; xi1 = complex(psi1, -chi1)
        pi_new = ((2 * n + 1) * mu * pi1 - (n + 1) * pi0) / n; pi0, pi1 = pi1, pi_new; an1, bn1 = an, bn
    gs += ((2 * nstop + 1) / (nstop * (nstop + 1.0))) * (an1 * np.conj(bn1)).real
    qsca *= 2 / x ** 2; qext *= 2 / x ** 2; g = 4 / x ** 2 * gs / qsca
    return qext, qsca, g, 0.5 * (abs(S1) ** 2 + abs(S2) ** 2)
MU = np.cos(np.radians(np.concatenate([np.arange(0, 10, 0.25), np.arange(10, 180.01, 1.0)])))[::-1]      # ascending in mu
def ensemble(lam_um, rm_um, sigma, m=1.43, nr=160):
    """a log-normal spread of sphere radii (median rm, geometric width sigma): the extinction cross-section per particle
    (square micrometres), the single-scattering albedo, the asymmetry, and the phase function on the grid MU,
    normalized so that its mean over the sphere is 1"""
    lr = np.linspace(np.log(rm_um) - 4 * np.log(sigma), np.log(rm_um) + 4 * np.log(sigma), nr); r = np.exp(lr)
    w = np.exp(-0.5 * ((lr - np.log(rm_um)) / np.log(sigma)) ** 2); w /= w.sum()
    cext = 0.0; csca = 0.0; ph = np.zeros_like(MU); gsum = 0.0
    for ri, wi in zip(r, w):
        x = 2 * np.pi * ri / lam_um; qe, qs, g, s11 = mie(m, x, MU); a = np.pi * ri * ri
        cext += wi * a * qe; csca += wi * a * qs; gsum += wi * a * qs * g; ph += wi * s11 * (lam_um / (2 * np.pi)) ** 2      # differential cross-section
    P = 4 * np.pi * ph / csca
    norm = 0.5 * np.trapezoid(P, MU)
    return dict(cext=cext, ssa=csca / cext, g=gsum / csca, mu=MU, P=P / norm, norm=norm, reff=float(rm_um * np.exp(2.5 * np.log(sigma) ** 2)))
if __name__ == '__main__':
    print('checks of the single sphere:')
    for m, x, note in ((1.5, 10.0, 'a standard test case; from memory, Qext 2.8820 and g 0.7429'), (1.5, 100.0, 'from memory, Qext 2.0944 and g 0.8182'), (1.33, 0.05, 'small sphere'), (1.43, 4.0, 'a haze droplet')):
        qe, qs, g, s = mie(m, x, MU); ray = (8.0 / 3.0) * x ** 4 * abs((m * m - 1) / (m * m + 2)) ** 2
        P = 2 * s / (x * x * qs); print(f'   m {m} x {x:g}: Qext {qe:.4f} Qsca {qs:.4f} g {g:.4f}; mean of the phase function over the sphere {0.5 * np.trapezoid(P, MU):.4f}; g from the phase function {0.5 * np.trapezoid(P * MU, MU):.4f}' + (f'; the small-sphere formula gives Qsca {ray:.3e}' if x < 0.1 else '') + f'   ({note})')
    print('the haze of the print (sulphuric acid droplets, refractive index 1.43):')
    for nm, rm, sg in (('the Hunga plume', 0.35, 1.23), ('the haze before', 0.18, 1.37)):
        e550 = ensemble(0.55, rm, sg)
        for lam in (0.425, 0.55, 0.675, 0.725):
            e = ensemble(lam, rm, sg); f = lambda deg: float(np.interp(np.cos(np.radians(deg)), e['mu'], e['P']))
            print(f"   {nm}, {int(lam * 1000)} nm: effective radius {e['reff']:.2f} um; extinction relative to 550 nm {e['cext'] / e550['cext']:.2f}; g {e['g']:.3f}; phase function at 5, 15, 30, 60, 95, 150 degrees: {f(5):.1f} {f(15):.1f} {f(30):.2f} {f(60):.2f} {f(95):.3f} {f(150):.3f}; normalization {e['norm']:.4f}")
