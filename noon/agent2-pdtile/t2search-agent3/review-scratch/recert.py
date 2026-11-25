"""re-certify the candidates left without an exact certificate in a results pickle.  usage: recert.py M pickle [nproc]"""
import sys, pickle, time
from multiprocessing import Pool
import wt
M = int(sys.argv[1]); fn = sys.argv[2]; nproc = int(sys.argv[3]) if len(sys.argv) > 3 else 4
def work(mask):
    A = [x for x in range(M) if mask >> x & 1]
    v, cert, feas = wt.certified(A, M)
    return mask, v, feas
if __name__ == "__main__":
    res = pickle.load(open(fn, "rb")); und = [r[0] for r in res if r[2] == "?"]; t0 = time.time()
    with Pool(nproc) as pool: out = dict((m, (v, f)) for m, v, f in pool.map(work, und, chunksize=20))
    new = [(r[0], r[1], out[r[0]][0], r[3], r[4], r[5]) if r[0] in out else r for r in res]
    left = [r for r in new if r[2] == "?"]
    print(f"Z_{M}: {len(und)} previously uncertified candidates re-examined in {time.time() - t0:.0f} s: now certified 'no' {sum(1 for m in und if out[m][0] == 'no')}, 'yes' {sum(1 for m in und if out[m][0] == 'yes')}, still uncertified {len(left)}")
    print(f"   totals: {sum(1 for r in new if r[2] == 'yes')} weak tiles, {sum(1 for r in new if r[2] == 'no')} not, {len(left)} uncertified; certified verdict vs float full LP mismatches: {sum(1 for r in new if r[2] != '?' and (r[2] == 'yes') != r[3])}; vs class reduction: {sum(1 for r in new if r[2] != '?' and (r[2] == 'yes') != r[5])}")
    for r in left[:10]: print("   STILL UNCERTIFIED", [x for x in range(M) if r[0] >> x & 1])
    pickle.dump(new, open(fn, "wb"))
