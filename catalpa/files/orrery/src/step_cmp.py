# Step-size check: the Moon's geocentric elements at the same instants from two runs that differ only in the time step.
# usage: step_cmp.py coarse.txt fine.txt
import sys, numpy as np
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
def load(p):
    a = np.loadtxt(p); n = len(a) // 11; a = a[:n * 11].reshape(n, 11, 8); return a[:, 0, 0], a[:, 4, 2:] - a[:, 3, 2:], a[:, 3, 2:5]
def elements(x):
    r, v = x[:, :3], x[:, 3:]; h = np.cross(r, v); rr = np.linalg.norm(r, axis=1); v2 = (v * v).sum(1); rv = (r * v).sum(1)
    e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1); Om = np.arctan2(h[:, 0], -h[:, 1])
    n = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], n)
    w = np.arctan2((e * m).sum(1), (e * n).sum(1)); f = np.arctan2((r * m).sum(1), (r * n).sum(1)) - w
    E = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); return Om, Om + w, Om + w + E - ecc * np.sin(E)
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
ja, xa, ea = load(sys.argv[1]); jb, xb, eb = load(sys.argv[2]); n = min(len(ja), len(jb)); assert np.allclose(ja[:n], jb[:n])
A, B = elements(xa[:n]), elements(xb[:n])
print('years from J2000   Moon position difference (m)   mean longitude   perigee   node (arcsec), coarse minus fine      Earth position difference (m)')
for i in range(n):
    print(f'   {(ja[i] - 2451545.0) / 365.25:8.1f}        {np.linalg.norm(xa[i, :3] - xb[i, :3]) * AU * 1e3:10.3f}            {wrap(A[2][i] - B[2][i]) * AS:+9.5f}  {wrap(A[1][i] - B[1][i]) * AS:+9.5f}  {wrap(A[0][i] - B[0][i]) * AS:+9.5f}               {np.linalg.norm(ea[i] - eb[i]) * AU * 1e3:10.3f}')
