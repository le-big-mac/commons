"""Two statements the write-up gives as counts over whole-degree turtles, searched more widely: over EVERY first turn,
whole-degree or not, for laps up to a stated length.
usage: python -I clause.py > clause.out      (numpy; one thread; a few minutes)

A. "Standing on its start, facing as it began, the turtle is about to make its first turn again."
   If the turtle stands on its start facing as it began after n steps, then n ANGLE + INC n(n-1)/2 is a whole number of
   turns, so ANGLE is one of n values (m - p n(n-1)/(2q))/n of a turn, m = 0 .. n-1.  For each lap length q up to QA,
   each p, each n up to NQ laps that is NOT a multiple of q, and each m, the n steps are added up: are they ever nought?
B. "A turtle that marches away never stands on its starting point again."
   The marching turtles with a lap of q are exactly ANGLE = (m - p(q-1)/2)/q of a turn, m = 0 .. q-1.  For each q up to QB,
   each p and each m, the turtle is walked for sqrt(q) + 2 laps (after that it is further than a lap's length away).

Places are in floating point; anything nearer nought than 1e-9 would be printed, with its numbers, to be tried exactly."""
import math, sys
import numpy as np

QA, NQ, QB = 48, 4, 150

if __name__ == '__main__':
    # ---- A
    cases = 0; hits = []; nearest = (9.0, None)
    for q in range(1, QA + 1):
        for p in range(0 if q == 1 else 1, q):
            if math.gcd(p, q) != 1: continue
            for n in range(2, NQ * q + 1):
                if n % q == 0: continue
                k = np.arange(n); m = np.arange(n)[:, None]
                # ANGLE in turns for each m: (m - p n(n-1)/(2q)) / n ; heading before step k: k a + p k(k-1)/(2q)
                a = (m - p * n * (n - 1) / (2.0 * q)) / n
                h = k[None, :] * a + (p * k * (k - 1) % (2 * q))[None, :] / (2.0 * q)
                z = np.abs(np.exp(2j * np.pi * h).sum(axis=1)); cases += n
                j = int(z.argmin())
                if z[j] < 1e-9: hits.append((q, p, n, j, float(z[j])))
                if z[j] < nearest[0]: nearest = (float(z[j]), (q, p, n, j))
    print(f"A. laps of 1 to {QA} steps, every amount p/q of a turn, every number of steps n up to {NQ} laps that is not a whole number of laps, and each of the n first turns that would leave the turtle facing as it began: {cases} cases")
    print(f"   on its starting point (to 1e-9) in {len(hits)} of them" + (": " + "; ".join(f"q {q} p {p} n {n} m {m} ({d:.1e})" for q, p, n, m, d in hits[:12]) if hits else ""))
    print(f"   the nearest miss: {nearest[0]:.6f} of a step (q {nearest[1][0]}, p {nearest[1][1]}, n {nearest[1][2]}, m {nearest[1][3]})")
    # the control: the same sum where n IS a whole number of laps must find the turtles that are then home
    chits = ccases = 0
    for q in range(1, 13):
        for p in range(0 if q == 1 else 1, q):
            if math.gcd(p, q) != 1: continue
            for n in range(q, NQ * q + 1, q):
                k = np.arange(n); m = np.arange(n)[:, None]; a = (m - p * n * (n - 1) / (2.0 * q)) / n
                h = k[None, :] * a + (p * k * (k - 1) % (2 * q))[None, :] / (2.0 * q)
                z = np.abs(np.exp(2j * np.pi * h).sum(axis=1)); ccases += n; chits += int((z < 1e-9).sum())
    print(f"   control, the same sum with n a whole number of laps (laps of 1 to 12): on its starting point in {chits} of {ccases} cases")
    sys.stdout.flush()
    # ---- C: can a lap end on its starting point for a first turn that is not the amount added?  (The referee's count, made again.)
    # With x = e(ANGLE), one lap's displacement is the polynomial sum_k e(p k(k-1)/(2q)) x^k; its roots of modulus 1 are the first turns wanted.
    found = []; others = 0
    for q in range(2, 41):
        for p in range(1, q):
            if math.gcd(p, q) != 1: continue
            k = np.arange(q); coef = np.exp(2j * np.pi * ((p * k * (k - 1)) % (2 * q)) / (2.0 * q))
            for x in np.roots(coef[::-1]):
                if abs(abs(x) - 1) < 1e-7:
                    a = (np.angle(x) / (2 * np.pi)) % 1.0; is_inc = min(abs(a - p / q), 1 - abs(a - p / q)) < 1e-7
                    found.append((q, p, a)); others += not (is_inc and q % 2 == 0)
    print(f"C. laps of 2 to 40 steps, every amount p/q, any first turn at all: a lap ends on its starting point for {len(found)} first turns; of these, {others} are something other than first turn = amount added with a lap of even length")
    print(f"   pairs p/q with an even lap, q from 2 to 40: {sum(1 for q in range(2, 41, 2) for p in range(1, q) if math.gcd(p, q) == 1)}")
    sys.stdout.flush()
    # ---- B
    cases = 0; back = []; nearest = (9.0, None)
    for q in range(1, QB + 1):
        laps = int(math.sqrt(q)) + 2; n = q * laps; k = np.arange(n)
        for p in range(0 if q == 1 else 1, q):
            if math.gcd(p, q) != 1: continue
            m = np.arange(q)[:, None]
            e = (k[None, :] * (2 * m - p * (q - 1)) + p * k * (k - 1)[None, :]) % (2 * q)       # headings in (2q)-ths of a turn, exact
            z = np.abs(np.cumsum(np.exp(2j * np.pi * e / (2.0 * q)), axis=1)); cases += q
            d = z.min(axis=1); j = int(d.argmin())
            for mm in np.nonzero(d < 1e-9)[0]: back.append((q, p, int(mm)))
            if d[j] < nearest[0]: nearest = (float(d[j]), (q, p, j, int(z[j].argmin()) + 1))
    print(f"B. laps of 1 to {QB} steps, every amount p/q of a turn, and every first turn that makes the turtle march away: {cases} turtles, each walked for sqrt(q) + 2 laps")
    print(f"   on its starting point again (to 1e-9) at some step: {len(back)}" + (": " + "; ".join(f"q {q} p {p} m {m}" for q, p, m in back[:12]) if back else ""))
    print(f"   the nearest any comes: {nearest[0]:.6f} of a step (q {nearest[1][0]}, p {nearest[1][1]}, m {nearest[1][2]}, at step {nearest[1][3]})")
    # the control: the same walk for turtles whose lap turns half a turn and whose first turn is the amount added must find them back on the start
    cback = ccases = 0
    for q in range(2, 41, 2):
        n = q * 3; k = np.arange(n)
        for p in range(1, q):
            if math.gcd(p, q) != 1: continue
            e = (2 * p * k + p * k * (k - 1)) % (2 * q)                    # ANGLE = INC: heading before step k is p k(k+1)/(2q) of a turn
            z = np.abs(np.cumsum(np.exp(2j * np.pi * e / (2.0 * q)))); ccases += 1; cback += bool(z.min() < 1e-9)
    print(f"   control, the same walk for first turn = amount added and a lap of even length (laps of 2 to 40): on its starting point again in {cback} of {ccases}")
