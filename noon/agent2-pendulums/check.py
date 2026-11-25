"""What the piece does, checked from its list of strikes.   usage: python check.py pendula.json"""
import sys, json
import numpy as np
J = json.load(open(sys.argv[1])); S = J['strikes']; T = J['T']; N = J['N']; M = J['M']
t = np.array([s[0] for s in S]); k = np.array([s[1] for s in S])
print(f"{N} voices, {len(S)} strikes; voice k sounds every {T:.0f}/({M} + k) seconds: from {T / M:.2f} s (lowest) to {T / (M + N - 1):.2f} s (highest)")
for name, at in (("start", 0), ("T/4", T / 4), ("T/3", T / 3), ("T/2", T / 2), ("2T/3", 2 * T / 3), ("3T/4", 3 * T / 4), ("T", T)):
    print(f"{name:5s} t = {at:6.1f} s: voices sounding within 0.02 s: {sorted(k[abs(t - at) < 0.02].tolist())}")
print("the largest group sounding within 0.03 s, in each twelve seconds:")
for a in range(0, int(T), 12):
    n, x = max(((abs(t - x) < 0.03).sum(), x) for x in t[(t >= a) & (t < a + 12)]); print(f"   {a:3d} to {a + 12:3d} s: {((t >= a) & (t < a + 12)).sum()} strikes; {n} together at {x:.1f} s")
back = all(any(abs((T - a) - b) < 1e-4 and ka == kb for b, kb in zip(t, k)) for a, ka in zip(t, k))
print(f"a palindrome (for every strike at t there is one by the same voice at {T:.0f} - t): {back}")
