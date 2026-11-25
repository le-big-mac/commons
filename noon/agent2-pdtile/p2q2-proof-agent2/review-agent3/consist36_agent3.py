"""Cross-check at M = 36 of Noon's categories against my complete census of Z_36 (agent3 / Yonder).
The census (census36-agent3/census36.out) gives, for each of the 256 zero patterns, the sizes of the sets that have exactly that pattern.
D^w(Z) = 36 / (optimum of LP(Z)), from my own linear programme (pnq-agent3/weak/dw.py).  A set with pattern Z is a weak tile iff its size is D^w(Z).
Noon's proof says, for (p, q) = (2, 3) (regime A):  category b, H, N -> no weak tile;  category a -> weak tiles have k elements;
Lemma-2 patterns (neither 2 nor 3 a zero) -> weak tiles lie in 2Z or 3Z;  RP/RQ -> whatever weak tiles there are, they tile."""
import sys, json, collections
sys.path.insert(0, "/home/agent3/pnq/weak")
from dw import setup
DS = [2, 4, 3, 9, 6, 12, 18, 36]; LM = {2: (1, 0), 4: (2, 0), 3: (0, 1), 9: (0, 2), 6: (1, 1), 12: (2, 1), 18: (1, 2), 36: (2, 2)}
cnt = collections.defaultdict(dict)
for line in open("/srv/commons/agent2-pdtile/census36-agent3/census36.out"):
    p, n, c = map(int, line.split()); cnt[p][n] = c
D, bound = setup(36)
cert = {(tuple(e["Ep"]), tuple(e["Eq"]), tuple(sorted(map(tuple, e["F"])))): e["cat"] for e in json.load(open("/srv/commons/agent2-pdtile/p2q2-proof-agent2/certificates_p2q2.json")) if e["regime"] == "A"}
tab = collections.Counter(); problems = []
for bits in range(256):
    Z = [d for i, d in enumerate(DS) if bits >> i & 1]; lm = [LM[d] for d in Z]
    Ep = tuple(sorted(l for l, m in lm if m == 0)); Eq = tuple(sorted(m for l, m in lm if l == 0)); F = tuple(sorted((l, m) for l, m in lm if l and m))
    cat = "L2" if (1 not in Ep and 1 not in Eq) else cert[(Ep, Eq, F)]
    k = 2 ** len(Ep) * 3 ** len(Eq); dw = bound(set(Z), False); sizes = sorted(cnt.get(bits, {}))
    weak = bool(sizes) and abs(sizes[0] - dw) < 1e-6
    if sizes and sizes[0] < dw - 1e-6: problems.append((Z, "a set smaller than D^w"))
    tab[(cat, "weak tiles exist" if weak else ("occurs, no weak tile" if sizes else "pattern does not occur"))] += 1
    if weak and cat in ("b", "H", "N"): problems.append((Z, cat, "the proof says no weak tile, the census has one"))
    if weak and cat == "a" and sizes[0] != k: problems.append((Z, cat, "weak tile of size != k"))
    if weak and cat in ("RP", "RQ"): problems.append((Z, cat, "note: a weak tile with an R pattern exists (allowed by the proof)"))
for key in sorted(tab): print(f"  {key[0]:3s} {key[1]:26s} {tab[key]}")
print("patterns with weak tiles:", sum(v for (c, s), v in tab.items() if s == "weak tiles exist"))
print("problems:", problems)
