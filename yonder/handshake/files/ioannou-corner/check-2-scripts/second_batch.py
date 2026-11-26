"""Second reader: a second batch of one of replay.py's variants on other seeds, to see whether a difference found once comes again.
usage: python -I -B second_batch.py VARIANT OUT.json [PROCESSES]"""
import sys, json, time
from multiprocessing import Pool
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner/check-2-scripts')
import replay, elite
if __name__ == '__main__':
    variant, out = sys.argv[1], sys.argv[2]; procs = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    base = 9000000 + 100000 * replay.VARIANTS.index(variant) + 50000          # replay.py's seeds for the variant, moved on by 50,000
    J = [(variant, r, base + 1000 * k + s, 500) for k, r in enumerate(elite.RATES) for s in range(30)]; t = time.time()
    with Pool(procs) as p: res = p.map(replay.run, J, chunksize=1)
    json.dump(res, open(out, 'w')); print(variant, 'second batch:', len(res), 'runs in', round(time.time() - t), 's')
    for r in elite.RATES:
        c = [x for x in res if x['rate'] == r]
        print(f'   {r:.0%}: all-defect commonest in {sum(x["top_is_alld"] for x in c)} of {len(c)}; handshake at an entry state {sum(x["top_is_handshake"] for x in c)}; '
              f'mean payoff {sum(x["payoff"] for x in c) / len(c):.2f}; cooperation {sum(x["coop"] for x in c) / len(c):.0%}')
