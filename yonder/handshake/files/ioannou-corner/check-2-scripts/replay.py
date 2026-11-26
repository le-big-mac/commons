"""Second reader: a replay of elite.py with things counted that elite.py does not record, and side runs that change one thing at a time.
Not sealed. Checked by nobody.

Variants (each the scheme as elite.py has it unless said):
  text      elite.py itself, draw for draw (with elite.py's seeds it must reproduce elite_run.json), each of 25 elements changed at 4%
  study     elite_after.py itself, draw for draw (the first reader's kind of mutation: the study's mutate() on the minimised machine)
  one       the letter of the paper's Figure 3: every newcomer has exactly one of its 25 elements switched
  rate8     each element changed at 8% (the paper's footnote 7: two elements a string on average)
  rate12    each element changed at 12% (footnote 7: three elements a string)
  ties      the twenty best chosen with exact ties broken at random (scores rounded to 8 places), not in favour of those already kept
  h2h       "the winner of the pair's match" read as the one that did better in the game between the two, not the one with the higher total
  exact200  exact expected payoffs over exactly 200 rounds, not over a game that ends at random after 200 on average
  played    payoffs played out once, 200 rounds a match, with the errors drawn (as the paper has it), each pair once and each machine its twin
  norm      the pairs drawn with chances in proportion to the normalised score of Miller (1996, footnote 7), whose algorithm the paper
            says it follows: (score - mean) / s.d. + 2, cut off at 0; not in proportion to the raw score
  played5   as played, but five matches a pair and the mean taken (Miller 1996, footnote 6, did this when there were errors)
  playednorm   played and norm together
  playedh2h    played and h2h together: Figure 3 by its letter, the newcomer copies the winner of the one match the pair played
  playedone    played, with exactly one element switched in every newcomer
  playedall    played, Miller's normalised draw, the winner of the pair's match, and exactly one element switched: every other reading at once

usage: python -I -B replay.py VARIANT OUT.json [same|fresh] [PROCESSES]"""
import sys, json, time
from collections import Counter
from multiprocessing import Pool
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner'); sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical, PAY
from evolve import mutate
from corner import payoff2, open_loop, ALLD
import elite

S = 8
T3 = ([1, 1, 0], [[0, 1], [0, 2], [2, 0]])
HSKEYS = {canonical(FSM(st, *T3)).key() for st in (0, 1, 2)}

def handshake_cored(m):
    """True if, whatever is read, the machine sooner or later sits for good in the three states of the handshake."""
    inside = [canonical(FSM(s, m.play, m.nxt)).key() in HSKEYS for s in range(m.n)]
    if not any(inside): return False
    reach = list(inside); changed = True                    # states from which the handshake's states can be reached
    while changed:
        changed = False
        for s in range(m.n):
            if not reach[s] and (reach[int(m.nxt[s, 0])] or reach[int(m.nxt[s, 1])]): reach[s] = True; changed = True
    return all(reach)

def mutate_rate(st, rng, q):                                 # elite.mutate_string with q for 0.04, same order of draws
    play, nxt, start = st[0].copy(), st[1].copy(), st[2]
    for i in range(S):
        if rng.random() < q: play[i] ^= 1
        for a in (0, 1):
            if rng.random() < q: nxt[i, a] = (nxt[i, a] + rng.integers(1, S)) % S
    if rng.random() < q: start = int((start + rng.integers(1, S)) % S)
    return [play, nxt, start]

def mutate_one(st, rng):                                     # exactly one of the 25 elements switched to another value
    play, nxt, start = st[0].copy(), st[1].copy(), st[2]
    k = int(rng.integers(25))
    if k < 8: play[k] ^= 1
    elif k < 24: i, a = divmod(k - 8, 2); nxt[i, a] = (nxt[i, a] + rng.integers(1, S)) % S
    else: start = int((start + rng.integers(1, S)) % S)
    return [play, nxt, start]

def chain(a, b, e):
    """Transition matrix over joint states and one-round payoffs and cooperation, errors of both kinds at rate e. My own writing."""
    na, nb = a.n, b.n; N = na * nb
    P = np.zeros((N, N)); ua = np.zeros(N); ub = np.zeros(N); ca = np.zeros(N); cb = np.zeros(N)
    for i in range(na):
        for j in range(nb):
            s = i * nb + j
            for x in (0, 1):                                 # a's move as it comes out
                px = 1 - e if x == a.play[i] else e
                for y in (0, 1):
                    py = 1 - e if y == b.play[j] else e
                    w = px * py
                    if w == 0: continue
                    ua[s] += w * PAY[x, y]; ub[s] += w * PAY[y, x]; ca[s] += w * (x == 0); cb[s] += w * (y == 0)
                    for ra, pra in ((y, 1 - e), (1 - y, e)):          # what a reads of b's move
                        for rb, prb in ((x, 1 - e), (1 - x, e)):      # what b reads of a's move
                            if pra * prb == 0: continue
                            P[s, int(a.nxt[i, ra]) * nb + int(b.nxt[j, rb])] += w * pra * prb
    return P, ua, ub, ca, cb

def payoff_fixed(a, b, e, T=200):
    """Exact expected payoff a round and cooperation over exactly T rounds."""
    P, ua, ub, ca, cb = chain(a, b, e)
    v = np.zeros(len(ua)); v[a.start * b.n + b.start] = 1.0; occ = np.zeros(len(ua))
    for _ in range(T): occ += v; v = v @ P
    occ /= T
    return occ @ ua, occ @ ub, occ @ ca, occ @ cb

IA, IB = np.triu_indices(30)                                 # 465 matches: every pair once, and each machine against its twin
OFF = IA != IB
def played(pop, e, rng, T=200):
    """Matches played out move by move, 200 rounds each, errors drawn. Returns, for every machine and every opponent, the payoff it
    took in their one match and its cooperative moves. In the twin match the machine takes the payoff of one of the two copies."""
    play = np.array([s[0] for s in pop]); nxt = np.array([s[1] for s in pop]); start = np.array([s[2] for s in pop])
    M = len(IA); sa = start[IA]; sb = start[IB]; ua = np.zeros(M); ub = np.zeros(M); ca = np.zeros(M); cb = np.zeros(M)
    for _ in range(T):
        r = rng.random((4, M)) < e
        xa = play[IA, sa] ^ r[0]; xb = play[IB, sb] ^ r[1]
        ua += PAY[xa, xb]; ub += PAY[xb, xa]; ca += xa == 0; cb += xb == 0
        sa, sb = nxt[IA, sa, xb ^ r[2]], nxt[IB, sb, xa ^ r[3]]
    U = np.zeros((30, 30)); C = np.zeros((30, 30))            # U[i, j]: what i got in all T rounds of its match with j (whole numbers, so sums are exact)
    U[IA, IB] = ua; U[IB[OFF], IA[OFF]] = ub[OFF]; C[IA, IB] = ca; C[IB[OFF], IA[OFF]] = cb[OFF]
    return U, C

def run(args):
    variant, rate, seed, gens = args
    rng = np.random.default_rng(seed)
    if variant == 'study':
        pop = None; can = [elite.canon(elite.rand_string(rng)) for _ in range(30)]
    else:
        pop = [elite.rand_string(rng) for _ in range(30)]; can = [elite.canon(s) for s in pop]
    cache = {}
    def pay(a, b):
        k = (a.key(), b.key()); v = cache.get(k)
        if v is None:
            if variant == 'exact200': ua, ub, ca, cb = payoff_fixed(a, b, rate)
            else: ua, ub, ca, cb = payoff2(a, b, rate, rate, 0.995)
            cache[k] = v = (ua, ca); cache[(b.key(), a.key())] = (ub, cb)
        return v
    occ, pay_tail, coop_tail = Counter(), [], []; kept = {}; curve = []; plural = Counter()
    n_new = same_string = same_machine = tie_cut = 0
    for g in range(gens):
        if variant in PLAYED:
            k = 5 if variant == 'played5' else 1
            UC = [played(pop, rate, rng) for _ in range(k)]; U = sum(x[0] for x in UC); score = U.sum(1) / (200 * k); coop = sum(x[1] for x in UC).sum(1) / (200 * k)
        else:
            score = np.zeros(30); coop = np.zeros(30)
            for i in range(30):
                for j in range(30):
                    u, c = pay(can[i], can[j]); score[i] += u; coop[i] += c
        curve.append(float(score.mean() / 30))
        if g >= gens - 100:
            pay_tail.append(float(score.mean() / 30)); coop_tail.append(float(coop.mean() / 30))
            for m in can: occ[m.key()] += 1; kept[m.key()] = m
            plural[Counter(m.key() for m in can).most_common(1)[0][0]] += 1
        if variant == 'ties':
            s = np.round(score, 8); order = rng.permutation(30); order = order[np.argsort(-s[order], kind='stable')]
        else: order = np.argsort(-score, kind='stable')
        best = [int(i) for i in order[:20]]
        i20, i21 = int(order[19]), int(order[20])
        if abs(score[i20] - score[i21]) < 1e-9 and can[i20].key() != can[i21].key(): tie_cut += 1
        if g == gens - 1:
            last_best = can[int(order[0])]; last_plural = kept[Counter(m.key() for m in can).most_common(1)[0][0]]
            last_alld = sum(m.key() == ALLD.key() for m in can)
        if variant in ('norm', 'playednorm', 'playedall'):
            sd = score.std(ddof=1); z = np.maximum((score - score.mean()) / sd + 2, 0) if sd > 0 else np.ones(30); p = z / z.sum()
        else: p = score / score.sum()
        new = []; newcan = []
        for _ in range(10):
            a, b = rng.choice(30, 2, p=p)
            if variant == 'h2h' and can[a].key() != can[b].key() and pay(can[a], can[b])[0] != pay(can[b], can[a])[0]:
                w = a if pay(can[a], can[b])[0] > pay(can[b], can[a])[0] else b
            elif variant in ('playedh2h', 'playedall') and a != b and U[a, b] != U[b, a]: w = a if U[a, b] > U[b, a] else b
            else: w = a if score[a] >= score[b] else b
            if variant == 'study':
                c = canonical(mutate(can[w], rng)); newcan.append(c)
            else:
                if variant in ('one', 'playedone', 'playedall'): child = mutate_one(pop[w], rng)
                elif variant == 'rate8': child = mutate_rate(pop[w], rng, 0.08)
                elif variant == 'rate12': child = mutate_rate(pop[w], rng, 0.12)
                else: child = elite.mutate_string(pop[w], rng)
                same_string += bool((child[0] == pop[w][0]).all() and (child[1] == pop[w][1]).all() and child[2] == pop[w][2])
                new.append(child); c = elite.canon(child); newcan.append(c)
            n_new += 1; same_machine += c.key() == can[w].key()
        if pop is not None: pop = [pop[i] for i in best] + new
        can = [can[i] for i in best] + newcan
        if g % 25 == 24:
            live = {m.key() for m in can}; cache = {k: v for k, v in cache.items() if k[0] in live and k[1] in live}
    topk, topc = occ.most_common(1)[0]; top = kept[topk]; pk = plural.most_common(1)[0][0]
    return dict(variant=variant, rate=rate, seed=seed, gens=gens, top=repr(top), top_is_alld=bool(topk == ALLD.key()), top_open_loop=bool(open_loop(top)),
                top_share=topc / sum(occ.values()), alld_share=occ.get(ALLD.key(), 0) / sum(occ.values()), payoff=float(np.mean(pay_tail)), coop=float(np.mean(coop_tail)),
                top_is_handshake=bool(topk in HSKEYS), top_handshake_cored=bool(handshake_cored(top)),
                plural_is_alld=bool(pk == ALLD.key()), last_plural_is_alld=bool(last_plural.key() == ALLD.key()), last_best_is_alld=bool(last_best.key() == ALLD.key()),
                last_alld=int(last_alld), last_plural=repr(last_plural), last_best=repr(last_best),
                newcomers=n_new, same_string=int(same_string), same_machine=int(same_machine), tie_cut=int(tie_cut), curve=[round(x, 4) for x in curve])

VARIANTS = ('text', 'study', 'one', 'rate8', 'rate12', 'ties', 'h2h', 'exact200', 'played', 'norm', 'played5', 'playednorm', 'playedh2h', 'playedone', 'playedall')
PLAYED = ('played', 'played5', 'playednorm', 'playedh2h', 'playedone', 'playedall')
if __name__ == '__main__':
    variant, out = sys.argv[1], sys.argv[2]; which = sys.argv[3] if len(sys.argv) > 3 else 'fresh'; procs = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    if variant == 'selftest':
        rng = np.random.default_rng(3); worst = 0; worstf = 0
        for _ in range(60):
            a, b = elite.canon(elite.rand_string(rng)), elite.canon(elite.rand_string(rng)); e = float(rng.choice([0.0, 0.01, 0.02, 0.04]))
            P, ua, ub, ca, cb = chain(a, b, e); e0 = np.zeros(len(ua)); e0[a.start * b.n + b.start] = 1
            o = 0.005 * np.linalg.solve((np.eye(len(ua)) - 0.995 * P).T, e0)
            worst = max(worst, max(abs(x - y) for x, y in zip((o @ ua, o @ ub, o @ ca, o @ cb), payoff2(a, b, e, e, 0.995))))
        print('my own chain, solved for a game that ends at random, against payoff2 on 60 random pairs: largest difference', worst)
        for e in (0.0, 0.02):                                # played-out scores against exact 200-round scores, one random population
            pop = [elite.rand_string(rng) for _ in range(30)]; can = [elite.canon(s) for s in pop]
            ex = np.array([sum(payoff_fixed(can[i], can[j], e)[0] for j in range(30)) for i in range(30)])
            sim = np.mean([played(pop, e, rng)[0].sum(1) / 200 for _ in range(200)], 0); one = played(pop, e, rng)[0].sum(1) / 200
            print(f'error {e}: played-out scores averaged over 200 tournaments against exact 200-round scores, 30 machines: largest difference {abs(sim - ex).max():.4f} '
                  f'(a single tournament: largest difference {abs(one - ex).max():.3f}; scores run from {ex.min():.1f} to {ex.max():.1f})')
        sys.exit()
    assert variant in VARIANTS
    if which == 'same':   base = {'text': 7000000, 'study': 8000000}[variant]             # the seeds of elite.py and of elite_after.py
    else:                 base = 9000000 + 100000 * VARIANTS.index(variant)
    J = [(variant, r, base + 1000 * k + s, 500) for k, r in enumerate(elite.RATES) for s in range(30)]; t = time.time()
    with Pool(procs) as p: res = p.map(run, J, chunksize=1)
    json.dump(res, open(out, 'w')); print(variant, which, len(res), 'runs in', round(time.time() - t), 's')
