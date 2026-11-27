# Referee's second look: how many of the random draws of thmu.py (seeds 1, 2, 3; the numbers of draws are those
# of thmu.out) are different families, and how many systems of values they have.  Regenerates the draws with the
# same seeds; the checks themselves are not run again.
import collections
import thmu
seen = set()
by_systems = collections.Counter()
empty = 0
def record(k, pos, systems, T):
    global empty
    T.fam += 1
    key = (k, tuple(g for g, _ in systems),
           tuple(sorted((pos[i],) + tuple(v[i] for _, v in systems) for i in range(len(pos)))))
    seen.add(key)
    by_systems[len(systems)] += 1
    if not pos:
        empty += 1
thmu.check = record
total = 0
for seed, count in ((1, 60962), (2, 63351), (3, 49159)):
    thmu.rand_runs(seed, count, 10 ** 6)
    total += count
print("random draws", total, "; different families (same k, same groups in the same order, same multiset of elements):", len(seen))
print("draws by number of systems of values:", dict(sorted(by_systems.items())), "; draws with the empty family:", empty)
