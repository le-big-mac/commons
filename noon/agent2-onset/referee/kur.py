"""Referee's own Kuramoto simulation (blind step). Mean-field form, RK4, dt = 0.05."""
import numpy as np
from scipy.special import ndtri

DT = 0.05
SIG = np.sqrt(np.pi / 8.0)


def freqs(shape, kind, N, R, rng):
    """Return (R, N) array of natural frequencies."""
    if kind == "regular":
        p = (np.arange(1, N + 1) - 0.5) / N
        p = np.broadcast_to(p, (R, N))
    else:
        p = rng.random((R, N))
    if shape == "lorentz":
        return 0.5 * np.tan(np.pi * (p - 0.5))
    if shape == "gauss":
        return SIG * ndtri(p)
    if shape == "uniform":
        return -np.pi / 4 + (np.pi / 2) * p
    raise ValueError(shape)


def integrate(omega, theta, K, nsteps, dt=DT):
    """RK4. omega, theta: (R, N). Returns (theta_final, r) with r of shape (R, nsteps+1):
    r[:, n] is r at time n*dt."""
    R, N = theta.shape
    rec = np.empty((R, nsteps + 1))
    c = np.empty_like(theta)
    s = np.empty_like(theta)
    th = np.empty_like(theta)

    def f(x):
        np.cos(x, out=c)
        np.sin(x, out=s)
        C = c.mean(axis=1, keepdims=True)
        S = s.mean(axis=1, keepdims=True)
        return omega + K * (S * c - C * s), C, S

    for n in range(nsteps):
        k1, C, S = f(theta)
        rec[:, n] = np.hypot(C[:, 0], S[:, 0])
        np.multiply(k1, dt / 2, out=th); th += theta
        k2, _, _ = f(th)
        np.multiply(k2, dt / 2, out=th); th += theta
        k3, _, _ = f(th)
        np.multiply(k3, dt, out=th); th += theta
        k4, _, _ = f(th)
        theta = theta + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    np.cos(theta, out=c); np.sin(theta, out=s)
    rec[:, nsteps] = np.hypot(c.mean(axis=1), s.mean(axis=1))
    return theta, rec


def runs(shape, kind, N, K, T, R, rng, chunk_elems=24000):
    """R independent runs from uniform random phases; returns r(t) array (R, nsteps+1)."""
    nsteps = int(round(T / DT))
    out = []
    per = max(1, chunk_elems // N)
    done = 0
    while done < R:
        m = min(per, R - done)
        om = freqs(shape, kind, N, m, rng)
        th0 = rng.random((m, N)) * 2 * np.pi
        _, rec = integrate(om, th0, K, nsteps)
        out.append(rec)
        done += m
    return np.concatenate(out, axis=0)


def measured(rec):
    """mean of r over the second half of the run, per run."""
    n = rec.shape[1] - 1
    return rec[:, n // 2:].mean(axis=1)
