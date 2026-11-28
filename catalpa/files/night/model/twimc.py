# A small model of the twilight sky overhead: sunlight in a spherical atmosphere, scattered once (by direct sums along
# the line of sight) and more than once (by a backward Monte Carlo with a local estimate at every collision).
# Scalar light (no polarization), no bending of rays, a hard Earth, a point Sun.
#   air: US Standard Atmosphere 1976 density (exponential above 86 km); Rayleigh scattering (Hansen and Travis formula)
#   ozone: one analytic profile (Green's), Chappuis absorption from a short table (approximate; varied in tests)
#   haze near the ground: an exponential layer; haze in the stratosphere: a Gaussian layer; both Henyey-Greenstein
#   ground: a Lambert surface
# Result: the zenith radiance for a unit of sunlight across the beam, order by order.
import numpy as np
RE = 6371.0; ZTOP = 120.0; RT = RE + ZTOP
ZE = np.arange(0.0, ZTOP + 1e-9, 0.25); ZC = 0.5 * (ZE[:-1] + ZE[1:])
def density(z):
    """air density relative to sea level, US Standard Atmosphere 1976 to 86 km, exponential above"""
    z = np.asarray(z, float); h = 6356.766 * z / (6356.766 + z)
    hb = [0, 11, 20, 32, 47, 51, 71, 84.852]; L = [-6.5, 0, 1.0, 2.8, 0, -2.8, -2.0]; T = [288.15]; P = [101325.0]; g0R = 34.1632
    for i in range(7):
        dh = hb[i + 1] - hb[i]; Tn = T[i] + L[i] * dh
        P.append(P[i] * (np.exp(-g0R * dh / T[i]) if L[i] == 0 else (T[i] / Tn) ** (g0R / L[i]))); T.append(Tn)
    rho = np.zeros_like(h)
    for i in range(7):
        m = (h >= hb[i]) & (h < hb[i + 1]) if i < 6 else (h >= hb[i]); dh = h[m] - hb[i]; Tm = T[i] + L[i] * dh
        Pm = P[i] * (np.exp(-g0R * dh / T[i]) if L[i] == 0 else (T[i] / Tm) ** (g0R / L[i])); rho[m] = Pm / Tm
    rho = rho / (101325.0 / 288.15)
    top = z > 86.0
    if np.any(top):
        r86 = float(density(np.array([86.0]))[0]); rho[top] = r86 * np.exp(-(z[top] - 86.0) / 5.9)
    return rho
O3_NM = np.array([400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 800.0])
O3_CS = np.array([0.1, 0.6, 2.0, 5.5, 12.2, 21.0, 33.0, 47.0, 51.0, 39.0, 28.0, 17.0, 11.0, 6.0, 4.5, 1.5]) * 1e-22   # cm2, approximate
def atmosphere(lam_nm, o3_du=300.0, o3_z0=23.5, o3_h=4.6, trop_tau=0.08, trop_h=1.5, trop_g=0.70, trop_ssa=0.95, trop_ang=1.3,
               strat_tau=0.004, strat_z0=20.0, strat_fwhm=6.0, strat_g=0.70, strat_ang=1.5, albedo=0.15, extra=None, layers=None):
    """optical properties by height for one wavelength. extra: an added stratospheric layer, dict(tau=at 550 nm, z0, fwhm, g, ang)"""
    lam = lam_nm / 1000.0; z = ZC
    tauR = 0.008569 * lam ** -4 * (1 + 0.0113 * lam ** -2 + 0.00013 * lam ** -4)
    rho = density(z); col = np.sum(rho) * 0.25; scaR = tauR * rho / col
    x = np.exp((z - o3_z0) / o3_h); shape = x / (1 + x) ** 2; shape = shape / (np.sum(shape) * 0.25)
    abso3 = np.interp(lam_nm, O3_NM, O3_CS) * o3_du * 2.687e16 * shape
    tt = trop_tau * (lam_nm / 550.0) ** -trop_ang; et = np.exp(-z / trop_h); et = tt * et / (np.sum(et) * 0.25)
    def layer(tau550, z0, fwhm, ang):
        s = fwhm / 2.3548; p = np.exp(-0.5 * ((z - z0) / s) ** 2); return tau550 * (lam_nm / 550.0) ** -ang * p / (np.sum(p) * 0.25)
    comps = [dict(sca=scaR, g=None), dict(sca=et * trop_ssa, g=trop_g)]; ext = scaR + abso3 + et
    if layers is None:
        sb = layer(strat_tau, strat_z0, strat_fwhm, strat_ang); comps.append(dict(sca=sb, g=strat_g)); ext = ext + sb
    else:      # haze layers of droplets: dict(tau=optical depth at 550 nm, z0, fwhm, rm, sigma)
        for ly in layers:
            tab, rel, g = droplets(lam_nm, ly['rm'], ly['sigma']); s_ = ly['fwhm'] / 2.3548; pz = np.exp(-0.5 * ((z - ly['z0']) / s_) ** 2)
            sl = ly['tau'] * rel * pz / (np.sum(pz) * 0.25); comps.append(dict(sca=sl, g=g, tab=tab)); ext = ext + sl
    if extra:
        sx = layer(extra['tau'], extra['z0'], extra['fwhm'], extra.get('ang', 0.5)); comps.append(dict(sca=sx, g=extra.get('g', 0.72))); ext = ext + sx
    return dict(ext=ext, comps=comps, sca=sum(c['sca'] for c in comps), albedo=albedo, tauR=tauR)
def pR(mu): return 0.75 * (1 + mu * mu)
def pHG(g, mu): return (1 - g * g) / (1 + g * g - 2 * g * mu) ** 1.5
def pcomp(c, mu):
    """phase function of one component: a table (droplets), Henyey-Greenstein (g given) or Rayleigh"""
    if 'tab' in c: return np.interp(mu, c['tab'][0], c['tab'][1])
    return pR(mu) if c['g'] is None else pHG(c['g'], mu)
def psample(c, xi):
    if 'tab' in c: return np.interp(xi, c['tab'][2], c['tab'][0])
    if c['g'] is None:
        q = 4 * xi - 2; dd = np.cbrt(q + np.sqrt(q * q + 1)); return dd - 1 / dd
    g = c['g']; return (1 + g * g - ((1 - g * g) / (1 - g + 2 * g * xi)) ** 2) / (2 * g)
def droplets(lam_nm, rm, sigma, _cache={}):
    """the table (mu, phase function, cumulative share) and relative extinction for a log-normal haze of acid droplets"""
    key = (round(lam_nm, 1), rm, sigma)
    if key not in _cache:
        import importlib.util as iu
        sp = iu.spec_from_file_location('mie', '/home/agent1/night/model/mie.py'); MI = iu.module_from_spec(sp); sp.loader.exec_module(MI)
        e = MI.ensemble(lam_nm / 1000.0, rm, sigma); e0 = MI.ensemble(0.55, rm, sigma)
        mu = np.linspace(-1, 1, 4001); P = np.interp(mu, e['mu'], e['P']); cdf = np.concatenate([[0.0], np.cumsum(0.5 * (P[1:] + P[:-1]) * np.diff(mu))]); cdf /= cdf[-1]
        _cache[key] = ((mu, P, cdf), e['cext'] / e0['cext'], e['g'])
    return _cache[key]
def ray(pos, d, ext, K=192):
    """for rays from pos along d: length to the top or the ground, optical depth to the middle and end of K steps, ground flag"""
    r0 = np.linalg.norm(pos, axis=1); pd = np.einsum('ij,ij->i', pos, d); b2 = np.maximum(r0 * r0 - pd * pd, 0.0)
    ground = (pd < 0) & (b2 < RE * RE)
    smax = np.where(ground, -pd - np.sqrt(np.maximum(RE * RE - b2, 0.0)), -pd + np.sqrt(np.maximum(RT * RT - b2, 0.0))); smax = np.maximum(smax, 0.0)
    s = (np.arange(K) + 0.5) / K * smax[:, None]
    z = np.sqrt(r0[:, None] ** 2 + 2 * s * pd[:, None] + s * s) - RE
    e = np.interp(z, ZC, ext, left=ext[0], right=0.0); cum = np.cumsum(e * (smax[:, None] / K), axis=1)
    return smax, cum, ground
def sun_trans(pos, shat, ext, K=192):
    d = np.broadcast_to(shat, pos.shape); smax, cum, ground = ray(pos, d, ext, K)
    return np.where(ground, 0.0, np.exp(-cum[:, -1]))
def at_height(pos, prof):
    return np.interp(np.linalg.norm(pos, axis=1) - RE, ZC, prof, left=prof[0], right=0.0)
def phase_mix(atm, pos, mu):
    tot = np.zeros(len(pos)); num = np.zeros(len(pos))
    for c in atm['comps']:
        sc = at_height(pos, c['sca']); tot += sc; num += sc * pcomp(c, mu)
    return np.where(tot > 0, num / np.maximum(tot, 1e-300), 0.0)
def single(atm, depth_deg, zobs=0.0, n=4000):
    """the zenith radiance from light scattered once, by a direct sum up the line of sight; also its height profile"""
    dl = np.radians(depth_deg); shat = np.array([np.cos(dl), 0.0, -np.sin(dl)])
    zs = zobs + (np.arange(n) + 0.5) / n * (ZTOP - zobs); dz = (ZTOP - zobs) / n
    pos = np.zeros((n, 3)); pos[:, 2] = RE + zs
    ext = np.interp(zs, ZC, atm['ext']); tlos = np.exp(-(np.cumsum(ext) - 0.5 * ext) * dz)
    mu = -np.sin(dl); sca = at_height(pos, atm['sca']); ts = sun_trans(pos, shat, atm['ext'], 384)
    contrib = sca * phase_mix(atm, pos, np.full(n, mu)) / (4 * np.pi) * tlos * ts * dz
    return float(contrib.sum()), zs, contrib
def rotate(d, mu, phi):
    """new directions at angle acos(mu) from d, azimuth phi"""
    st = np.sqrt(np.maximum(1 - mu * mu, 0.0)); a = np.where(np.abs(d[:, 2:3]) < 0.999, np.array([[0.0, 0.0, 1.0]]), np.array([[1.0, 0.0, 0.0]]))
    u = np.cross(d, a); u /= np.linalg.norm(u, axis=1)[:, None]; v = np.cross(d, u)
    return d * mu[:, None] + (u * np.cos(phi)[:, None] + v * np.sin(phi)[:, None]) * st[:, None]
def multiple(atm, depth_deg, N=20000, seed=1, zobs=0.0, orders=40, K=192):
    """backward Monte Carlo. returns the zenith radiance by order of scattering (index 1 = once), as sums over N photons"""
    rng = np.random.default_rng(seed); dl = np.radians(depth_deg); shat = np.array([np.cos(dl), 0.0, -np.sin(dl)])
    pos = np.zeros((N, 3)); pos[:, 2] = RE + zobs; d = np.zeros((N, 3)); d[:, 2] = 1.0; w = np.ones(N); L = np.zeros(orders + 1); L2 = np.zeros(orders + 1)
    smax, cum, ground = ray(pos, d, atm['ext'], K); tt = cum[:, -1]
    w *= (1 - np.exp(-tt)); ts = -np.log(1 - rng.random(N) * (1 - np.exp(-tt)))
    def place(pos, d, smax, cum, ts):
        j = np.minimum((cum < ts[:, None]).sum(axis=1), cum.shape[1] - 1); ds = smax / cum.shape[1]
        prev = np.where(j > 0, cum[np.arange(len(j)), np.maximum(j - 1, 0)], 0.0); step = cum[np.arange(len(j)), j] - prev
        s = (j + np.clip((ts - prev) / np.maximum(step, 1e-300), 0, 1)) * ds; return pos + d * s[:, None]
    pos = place(pos, d, smax, cum, ts); onground = np.zeros(N, bool)
    for k in range(1, orders + 1):
        if len(w) == 0: break
        est = np.zeros(len(w)); air = ~onground
        if air.any():
            pa = pos[air]; ext = at_height(pa, atm['ext']); sca = at_height(pa, atm['sca']); wa = w[air] * sca / np.maximum(ext, 1e-300)
            mu = d[air] @ shat; est[air] = wa * phase_mix(atm, pa, mu) / (4 * np.pi) * sun_trans(pa, shat, atm['ext'], K); w[air] = wa
            # the scatterer and the new direction
            probs = np.stack([at_height(pa, c['sca']) for c in atm['comps']], axis=1); probs /= np.maximum(probs.sum(axis=1, keepdims=True), 1e-300)
            u = rng.random(len(pa)); which = (u[:, None] > np.cumsum(probs, axis=1)).sum(axis=1); which = np.minimum(which, len(atm['comps']) - 1)
            xi = rng.random(len(pa)); m2 = np.empty(len(pa))
            for ci, c in enumerate(atm['comps']):
                sel = which == ci
                if not sel.any(): continue
                m2[sel] = psample(c, xi[sel])
            d[air] = rotate(d[air], np.clip(m2, -1, 1), 2 * np.pi * rng.random(len(pa)))
        if onground.any():
            pg = pos[onground]; nrm = pg / np.linalg.norm(pg, axis=1)[:, None]; mu0 = nrm @ shat
            est[onground] = w[onground] * atm['albedo'] * np.maximum(mu0, 0) / np.pi * np.where(mu0 > 0, sun_trans(pg + nrm * 1e-6, shat, atm['ext'], K), 0.0)
            w[onground] *= atm['albedo']
            mu = np.sqrt(rng.random(len(pg))); phi = 2 * np.pi * rng.random(len(pg)); d[onground] = rotate(nrm, mu, phi); pos[onground] = pg + nrm * 1e-6
        L[k] += est.sum(); L2[k] += (est ** 2).sum()
        smax, cum, ground = ray(pos, d, atm['ext'], K); ts = -np.log(rng.random(len(w))); hit = ts < cum[:, -1]
        newpos = place(pos, d, smax, cum, ts); endpos = pos + d * smax[:, None]
        alive = hit | ground; pos = np.where(hit[:, None], newpos, endpos)[alive]; onground = (~hit & ground)[alive]; d = d[alive]; w = w[alive]
        keep = w > 1e-7
        if not keep.all(): pos, d, w, onground = pos[keep], d[keep], w[keep], onground[keep]
    return L, L2
if __name__ == '__main__':
    import sys, time
    atm = atmosphere(550.0)
    print('vertical optical depths at 550 nm: all', round(float(atm['ext'].sum() * 0.25), 4), ' Rayleigh', round(float(atm['tauR']), 4), ' air column in km of sea-level air', round(float(density(ZC).sum() * 0.25), 3))
    for dep in (0.0, 3.0, 6.0, 9.0):
        t0 = time.time(); L1, zs, c = single(atm, dep); zmid = zs[np.searchsorted(np.cumsum(c), 0.5 * c.sum())]
        L, L2 = multiple(atm, dep, N=40000, seed=3); N = 40000
        print(f'depth {dep:g}: once, by direct sum {L1:.4e} (half of it from above {zmid:.0f} km); once, by Monte Carlo {L[1] / N:.4e} +- {np.sqrt(L2[1] / N - (L[1] / N) ** 2) / np.sqrt(N):.1e}; twice {L[2] / N:.3e}; three times and more {L[3:].sum() / N:.3e}; share scattered more than once {(L[2:].sum() / N) / (L1 + L[2:].sum() / N):.2f}; {time.time() - t0:.0f} s')

def paired(atm, alts, depth_deg, N=20000, seed=1, zobs=0.0, orders=40, K=192):
    """backward Monte Carlo in the atmosphere atm, with the same paths weighted for each atmosphere in alts (which must
    have nothing that atm lacks). Returns, for atm and each of alts, the radiance sums by order, and per-photon totals
    of the light scattered more than once (for errors of ratios)."""
    rng = np.random.default_rng(seed); dl = np.radians(depth_deg); shat = np.array([np.cos(dl), 0.0, -np.sin(dl)]); A = [atm] + list(alts); nA = len(A)
    pos = np.zeros((N, 3)); pos[:, 2] = RE + zobs; d = np.zeros((N, 3)); d[:, 2] = 1.0; W = np.ones((N, nA)); idx = np.arange(N)
    L = np.zeros((nA, orders + 1)); per = np.zeros((N, nA))
    def flight(pos, d):
        r0 = np.linalg.norm(pos, axis=1); pd = np.einsum('ij,ij->i', pos, d); b2 = np.maximum(r0 * r0 - pd * pd, 0.0)
        ground = (pd < 0) & (b2 < RE * RE)
        smax = np.maximum(np.where(ground, -pd - np.sqrt(np.maximum(RE * RE - b2, 0.0)), -pd + np.sqrt(np.maximum(RT * RT - b2, 0.0))), 0.0)
        s = (np.arange(K) + 0.5) / K * smax[:, None]; z = np.sqrt(r0[:, None] ** 2 + 2 * s * pd[:, None] + s * s) - RE
        cums = [np.cumsum(np.interp(z, ZC, a['ext'], left=a['ext'][0], right=0.0) * (smax[:, None] / K), axis=1) for a in A]
        return smax, cums, ground
    def locate(cum, ts):
        j = np.minimum((cum < ts[:, None]).sum(axis=1), K - 1); ar = np.arange(len(j)); prev = np.where(j > 0, cum[ar, np.maximum(j - 1, 0)], 0.0)
        fr = np.clip((ts - prev) / np.maximum(cum[ar, j] - prev, 1e-300), 0, 1); return j, fr, prev
    def upto(cum, j, fr, prev0=None):
        ar = np.arange(len(j)); prev = np.where(j > 0, cum[ar, np.maximum(j - 1, 0)], 0.0); return prev + fr * (cum[ar, j] - prev)
    smax, cums, ground = flight(pos, d); tt = cums[0][:, -1]
    ts = -np.log(1 - rng.random(N) * (1 - np.exp(-tt))); j, fr, _ = locate(cums[0], ts)
    W[:, 0] *= (1 - np.exp(-tt))
    for a in range(1, nA): W[:, a] *= (1 - np.exp(-tt)) * np.exp(ts - upto(cums[a], j, fr))
    pos = pos + d * ((j + fr) * smax / K)[:, None]; onground = np.zeros(N, bool)
    for k in range(1, orders + 1):
        if len(idx) == 0: break
        est = np.zeros((len(idx), nA)); air = ~onground
        if air.any():
            pa = pos[air]; ext = at_height(pa, atm['ext']); mu = d[air] @ shat
            scas = [at_height(pa, a['sca']) for a in A]
            for a in range(nA):
                W[air, a] = W[air, a] * scas[a] / np.maximum(ext, 1e-300)
                est[air, a] = W[air, a] * phase_mix(A[a], pa, mu) / (4 * np.pi) * sun_trans(pa, shat, A[a]['ext'], K)
            probs = np.stack([at_height(pa, c['sca']) for c in atm['comps']], axis=1); probs /= np.maximum(probs.sum(axis=1, keepdims=True), 1e-300)
            u = rng.random(len(pa)); which = np.minimum((u[:, None] > np.cumsum(probs, axis=1)).sum(axis=1), len(atm['comps']) - 1)
            xi = rng.random(len(pa)); m2 = np.empty(len(pa))
            for ci, c in enumerate(atm['comps']):
                sel = which == ci
                if not sel.any(): continue
                m2[sel] = psample(c, xi[sel])
            m2 = np.clip(m2, -1, 1); p0 = phase_mix(atm, pa, m2)
            for a in range(1, nA): W[air, a] = W[air, a] * phase_mix(A[a], pa, m2) / np.maximum(p0, 1e-300)
            d[air] = rotate(d[air], m2, 2 * np.pi * rng.random(len(pa)))
        if onground.any():
            pg = pos[onground]; nrm = pg / np.linalg.norm(pg, axis=1)[:, None]; mu0 = nrm @ shat; up = pg + nrm * 1e-6
            for a in range(nA):
                est[onground, a] = W[onground, a] * atm['albedo'] * np.maximum(mu0, 0) / np.pi * np.where(mu0 > 0, sun_trans(up, shat, A[a]['ext'], K), 0.0)
            W[onground] *= atm['albedo']
            d[onground] = rotate(nrm, np.sqrt(rng.random(len(pg))), 2 * np.pi * rng.random(len(pg))); pos[onground] = up
        L[:, k] += est.sum(axis=0)
        if k >= 2: per[idx] += est
        smax, cums, ground = flight(pos, d); ts = -np.log(rng.random(len(idx))); hit = ts < cums[0][:, -1]
        j, fr, _ = locate(cums[0], np.minimum(ts, cums[0][:, -1]))
        for a in range(1, nA):
            dt = np.where(hit, ts - upto(cums[a], j, fr), cums[0][:, -1] - cums[a][:, -1]); W[:, a] *= np.exp(dt)
        newpos = np.where(hit[:, None], pos + d * ((j + fr) * smax / K)[:, None], pos + d * smax[:, None])
        alive = (hit | ground) & (W.max(axis=1) > 1e-8)
        pos = newpos[alive]; onground = (~hit & ground)[alive]; d = d[alive]; W = W[alive]; idx = idx[alive]
    return L, per

# ---- light scattered twice, by direct sums (no random numbers)
def sun_table(atm, K=384):
    """transmission from a point at height z towards the Sun, by the Sun's zenith angle there: a table (z, angle)"""
    zs = np.concatenate([np.arange(0.0, 60.0, 0.25), np.arange(60.0, ZTOP + 1e-9, 1.0)]); ch = np.concatenate([np.arange(0.0, 80.0, 2.0), np.arange(80.0, 112.01, 0.05)])
    Zg, Cg = np.meshgrid(zs, np.radians(ch), indexing='ij'); pos = np.zeros((Zg.size, 3)); pos[:, 2] = RE + Zg.ravel()
    d = np.stack([np.sin(Cg.ravel()), np.zeros(Cg.size), np.cos(Cg.ravel())], axis=1)
    T = np.empty(Zg.size)
    for i in range(0, Zg.size, 20000):
        smax, cum, ground = ray(pos[i:i + 20000], d[i:i + 20000], atm['ext'], K); T[i:i + 20000] = np.where(ground, 0.0, np.exp(-cum[:, -1]))
    return zs, ch, T.reshape(Zg.shape)
def table_lookup(tab, z, chi_deg):
    zs, ch, T = tab; iz = np.clip(np.searchsorted(zs, z) - 1, 0, len(zs) - 2); ic = np.clip(np.searchsorted(ch, chi_deg) - 1, 0, len(ch) - 2)
    fz = np.clip((z - zs[iz]) / (zs[iz + 1] - zs[iz]), 0, 1); fc = np.clip((chi_deg - ch[ic]) / (ch[ic + 1] - ch[ic]), 0, 1)
    out = T[iz, ic] * (1 - fz) * (1 - fc) + T[iz + 1, ic] * fz * (1 - fc) + T[iz, ic + 1] * (1 - fz) * fc + T[iz + 1, ic + 1] * fz * fc
    return np.where((chi_deg > ch[-1]) | (z > zs[-1] + 1e-6), np.where(z > zs[-1] + 1e-6, 1.0, 0.0), out)
def second(atm, depth_deg, tab=None, nel=160, naz=48, ns=200, zobs=0.0, detail=False):
    """the zenith radiance from light scattered exactly twice: first where the Sun shines (B), then on the line of
    sight (A). Sums over A up the line of sight, over directions from A (half the sky, doubled), and along each ray."""
    if tab is None: tab = sun_table(atm)
    dl = np.radians(depth_deg); shat = np.array([np.cos(dl), 0.0, -np.sin(dl)])
    zA = np.concatenate([np.arange(0.125, 12.0, 0.25), np.arange(12.5, 40.0, 1.0), np.arange(41.0, 100.0, 2.0)]) + zobs
    wA = np.gradient(zA); wA[0] = 0.25; ext = np.interp(zA, ZC, atm['ext'])
    zfine = np.arange(0.0, ZTOP, 0.05) + 0.025; tfine = np.cumsum(np.interp(zfine, ZC, atm['ext']) * 0.05); tlos = np.exp(-np.interp(zA, zfine, tfine))
    # directions: elevation by a rule that crowds points near the horizon; azimuth over half a circle from the Sun's side
    u = (np.arange(nel) + 0.5) / nel * 2 - 1; el = np.pi / 2 * np.sign(u) * np.abs(u) ** 2.0; wel = np.pi / 2 * 2.0 * np.abs(u) * (2.0 / nel) * np.cos(el)
    az = (np.arange(naz) + 0.5) / naz * np.pi; waz = 2 * np.pi / naz
    EL, AZ = np.meshgrid(el, az, indexing='ij'); W = (wel[:, None] * waz * np.ones_like(AZ)).ravel()
    D = np.stack([np.cos(EL.ravel()) * np.cos(AZ.ravel()), np.cos(EL.ravel()) * np.sin(AZ.ravel()), np.sin(EL.ravel())], axis=1)
    muA = D[:, 2]; cosB = D @ shat; total = 0.0; prof = np.zeros(len(zA)); byh = np.zeros(len(ZC))
    for ia, za in enumerate(zA):
        pos = np.zeros((len(D), 3)); pos[:, 2] = RE + za
        r0 = RE + za; pd = r0 * D[:, 2]; b2 = r0 * r0 - pd * pd; ground = (pd < 0) & (b2 < RE * RE)
        smax = np.where(ground, -pd - np.sqrt(np.maximum(RE * RE - b2, 0.0)), -pd + np.sqrt(np.maximum(RT * RT - b2, 0.0)))
        t = (np.arange(ns) + 0.5) / ns; s = smax[:, None] * t ** 2; ds = smax[:, None] * 2 * t / ns          # steps crowd near A
        B = pos[:, None, :] + D[:, None, :] * s[:, :, None]; rB = np.linalg.norm(B, axis=2); zB = rB - RE
        e = np.interp(zB, ZC, atm['ext'], left=atm['ext'][0], right=0.0); tau = np.cumsum(e * ds, axis=1) - 0.5 * e * ds
        chi = np.degrees(np.arccos(np.clip((B @ shat) / rB, -1, 1))); ts = table_lookup(tab, zB.ravel(), chi.ravel()).reshape(zB.shape)
        src = np.zeros_like(zB)
        for c in atm['comps']:
            sc = np.interp(zB, ZC, c['sca'], left=c['sca'][0], right=0.0); src += sc * (pcomp(c, cosB)[:, None])
        f = src / (4 * np.pi) * np.exp(-tau) * ts * ds; inner = f.sum(axis=1)
        if ground.any():      # the sunlit ground at the end of the ray
            G = pos[ground] + D[ground] * smax[ground][:, None]; nrm = G / np.linalg.norm(G, axis=1)[:, None]; mu0 = nrm @ shat
            tg = np.exp(-(tau[ground, -1] + 0.5 * e[ground, -1] * ds[ground, -1]))
            inner[ground] += atm['albedo'] * np.maximum(mu0, 0) / np.pi * tg * table_lookup(tab, np.zeros(mu0.size), np.degrees(np.arccos(np.clip(mu0, -1, 1))))
        pa = np.zeros(len(D))
        for c in atm['comps']:
            sc = float(np.interp(za, ZC, c['sca'])); pa += sc * pcomp(c, muA)
        val = float((W * pa / (4 * np.pi) * inner).sum()) * tlos[ia] * wA[ia]; total += val; prof[ia] = val
        if detail: byh += np.histogram(zB.ravel(), bins=ZE, weights=((W * pa / (4 * np.pi))[:, None] * f).ravel() * tlos[ia] * wA[ia])[0]
    return (total, zA, prof, byh) if detail else total
