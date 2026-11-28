"""Second look: replay the generators of the structured runs (same seeds, no counting of signings) to state exactly
which moduli and which sizes m the runs covered."""
import math, random
from collections import Counter
import tests as TS
import tests2 as T2
from eng import factor

NS = [3, 9, 27, 81, 243, 5, 25, 125, 7, 49, 15, 45, 75, 135, 225, 21, 63, 105, 315, 35, 33, 165, 1155, 11, 13]
for seed in (101, 102):
    rng = random.Random(seed); done = 0; mod = Counter(); ms_ = []
    while done < 4000:
        n = rng.choice(NS); ms = TS.rand_multiset(rng, n)
        if not ms: continue
        g = math.prod(h + 1 for h in ms.values())
        if g > 40000 or sum(ms.values()) > 60 or g * n > 6000000: continue
        done += 1; mod[n] += 1; ms_.append(sum(ms.values()))
    print(f"rand seed {seed}: {done} multisets on {len(mod)} of the {len(NS)} moduli; fewest on Z_{min(mod, key=mod.get)} ({min(mod.values())}); m from {min(ms_)} to {max(ms_)}; odd m >= 17: {sum(1 for x in ms_ if x % 2 and x >= 17)}; by modulus: {dict(sorted(mod.items()))}")
NS2 = [15, 21, 35, 45, 75, 135, 225, 63, 147, 315, 105, 165, 495, 675, 525, 1155]
for seed in (201, 202):
    rng = random.Random(seed); done = 0; mod = Counter(); ms_ = []
    while done < 3000:
        n = rng.choice(NS2); ms = T2.gon_multiset(rng, n)
        if not ms: continue
        gsz = math.prod(h + 1 for h in ms.values())
        if gsz > 70000 or gsz * n > 12000000 or sum(ms.values()) > 60: continue
        done += 1; mod[n] += 1; ms_.append(sum(ms.values()))
    print(f"gon seed {seed}: {done} multisets on {len(mod)} of the {len(NS2)} moduli; fewest on Z_{min(mod, key=mod.get)} ({min(mod.values())}); m from {min(ms_)} to {max(ms_)}; odd m >= 17: {sum(1 for x in ms_ if x % 2 and x >= 17)}; by modulus: {dict(sorted(mod.items()))}")
