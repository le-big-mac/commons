"""puck.py: a hand that only chases, by the equation and by simulation.
The ring's offset from the dot, r, obeys  r'(t) = -k R(a) r(t - tau):  the hand moves toward where it saw the dot lie from
the ring a time tau ago, k times the distance a second, and the pointer turns that movement by the angle a.
  no delay:   |r| = |r0| exp(-k t cos a);  the ring swings round the dot at k sin a;  the path is |r0| / cos a  (for a under a quarter turn)
  with delay: steady exactly when  k tau < pi/2 - |a|
  in steps (a share g of the distance at each step, no delay): steady exactly when  0 < g < 2 cos a;
     each step leaves r = sqrt(1 - 2 g cos a + g g) of the distance, and the path is g / (1 - r) times the distance closed
    python3 -I puck.py     prints a small table"""
import cmath, math
def ratio(deg):
    c = math.cos(math.radians(deg)); return 1 / c if c > 1e-12 else math.inf
def limit_delay(deg, k):
    """the longest delay, in seconds, at which a chaser of gain k is still steady under a turn of deg (nought or less: never)"""
    return (math.pi / 2 - abs(math.radians(deg))) / k
def limit_step(deg):
    return 2 * math.cos(math.radians(deg))
def step_ratio(deg, g):
    r = math.sqrt(1 - 2 * g * math.cos(math.radians(deg)) + g * g); return g / (1 - r) if r < 1 else math.inf
def step_run(deg, g, n=100000, stop=1e-9):
    """the stepped hand run: returns (last distance, path length over distance closed)"""
    rot = cmath.exp(1j * math.radians(deg)); e = complex(1.0); length = 0.0
    for _ in range(n):
        step = -g * rot * e; e += step; length += abs(step)
        if abs(e) < stop or abs(e) > 1e9: break
    return abs(e), length / (1 - abs(e))
def simulate(deg, k=1.0, tau=0.0, T=40.0, dt=1e-3, r0=1.0):
    """the equation stepped forward; returns (last distance, path length, largest distance met, time for the distance to fall to r0/e or None)"""
    rot = cmath.exp(1j * math.radians(deg)); n = int(round(tau / dt)); hist = [complex(r0)] * (n + 1); r = complex(r0); length = 0.0; big = abs(r); t_e = None
    for i in range(int(round(T / dt))):
        seen = hist[0]; step = -k * rot * seen * dt; r += step; length += abs(step); hist.append(r); hist.pop(0); big = max(big, abs(r))
        if t_e is None and abs(r) <= r0 / math.e: t_e = (i + 1) * dt
        if abs(r) > 1e6: break
    return abs(r), length, big, t_e
if __name__ == '__main__':
    print('turn   path over straight line   steady with a delay up to (a hand closing 5 times a second)')
    for a in (0, 15, 30, 45, 60, 75, 85, 90):
        print('%3d    %-24s  %s' % (a, '%.2f' % ratio(a) if a < 90 else 'circles for ever', '%.2f s' % limit_delay(a, 5) if a < 90 else 'never'))
