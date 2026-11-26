"""Second reader: how much of the comparisons the section leans on is beyond chance (thirty runs a cell), and the handshake in the
first reader's own run.   usage: python -I -B stats.py"""
import sys, json
from scipy.stats import fisher_exact, beta
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical
def cp(k, n, a=0.05):
    return (0.0 if k == 0 else beta.ppf(a / 2, k, n - k + 1), 1.0 if k == n else beta.ppf(1 - a / 2, k + 1, n - k))
def fe(k1, n1, k2, n2): return fisher_exact([[k1, n1 - k1], [k2, n2 - k2]])[1]
print('Exact 95% intervals for a count of 30:')
for k in (0, 1, 9, 20, 11, 7, 18, 19, 22, 5): lo, hi = cp(k, 30); print(f'   {k:2d} of 30: {30 * lo:4.1f} to {30 * hi:4.1f} runs of 30  ({lo:.0%} to {hi:.0%})')
print('Fisher exact, two-sided:')
for name, a in [('1% all-defect: 1 (sealed, string mutation) against 18 (after, the study\'s mutation)', (1, 30, 18, 30)),
                ('1% all-defect: 1 (sealed) against the first reader\'s 16', (1, 30, 16, 30)),
                ('2% all-defect: 9 (sealed) against his 19', (9, 30, 19, 30)),
                ('4% all-defect: 20 (sealed) against his 22', (20, 30, 22, 30)),
                ('2% all-defect: 9 (sealed) against 18 (after)', (9, 30, 18, 30)),
                ('4% all-defect: 20 (sealed) against 30 (after)', (20, 30, 30, 30)),
                ('0% all-defect: 0 (sealed) against 5 (after)', (0, 30, 5, 30)),
                ('sealed, all-defect 1% against 2%: 1 against 9', (1, 30, 9, 30)),
                ('sealed, all-defect 2% against 4%: 9 against 20', (9, 30, 20, 30)),
                ('handshake-led at 1%: 11 (sealed) against 0 at 0%', (11, 30, 0, 30)),
                ('handshake-led at 1%: 11 (sealed) against 7 at 2%', (11, 30, 7, 30)),
                ('handshake-led at 1%: 11 (sealed) against 1 at 4%', (11, 30, 1, 30)),
                ('handshake-led at 1%: 11 (sealed) against 5 (after)', (11, 30, 5, 30)),
                ('2%: handshake 7 against all-defect 9, as two counts of 30', (7, 30, 9, 30))]:
    print(f'   p = {fe(*a):.2g}   {name}')
T = ([1, 1, 0], [[0, 1], [0, 2], [2, 0]]); HS = {repr(canonical(FSM(st, *T))): st for st in (0, 1, 2)}
for f in ('elitist.json',):
    R = json.load(open('/home/agent3/welch-prior/corner/check-scripts/' + f))
    print('the first reader\'s own run (' + f + '), runs led by the handshake at any of its three entry states:')
    for pm in (1.0, 0.64):
        print(f'   newcomers mutated with chance {pm}: ' + ', '.join(f'{e:.0%}: {sum(x["top"] in HS for x in R if x["e"] == e and x["p_mut"] == pm)} of {sum(1 for x in R if x["e"] == e and x["p_mut"] == pm)}' for e in (0.0, 0.01, 0.02, 0.04)))
R = json.load(open('/home/agent3/welch-prior/corner/elite_after.json'))
print('elite_after.json, handshake at any entry: ' + ', '.join(f'{e:.0%}: {sum(x["top"] in HS for x in R if x["rate"] == e)}' for e in (0.0, 0.01, 0.02, 0.04)))

# with the second batch of the sealed design (replay.py, variant text, fresh seeds) and the side runs
import os
D = '/home/agent3/welch-prior/corner/check-2-scripts/'
def cnt(name, key='top_is_alld'):
    R = json.load(open(D + name)); return [sum(x[key] for x in R if x['rate'] == r) for r in (0.0, 0.01, 0.02, 0.04)]
if os.path.exists(D + 'replay_text_fresh.json'):
    a, b = cnt('replay_text_same.json'), cnt('replay_text_fresh.json'); ha, hb = cnt('replay_text_same.json', 'top_is_handshake'), cnt('replay_text_fresh.json', 'top_is_handshake')
    print('\nthe sealed design twice (sealed seeds, fresh seeds): all-defect', a, b, '; handshake at an entry state', ha, hb)
    print(f'   the two batches against each other, all-defect: p = ' + ', '.join(f'{fe(x, 30, y, 30):.2g}' for x, y in zip(a, b)))
    print(f'   both batches together against his: 2%: {a[2] + b[2]} of 60 against 19 of 30, p = {fe(a[2] + b[2], 60, 19, 30):.2g}; 4%: {a[3] + b[3]} of 60 against 22 of 30, p = {fe(a[3] + b[3], 60, 22, 30):.2g}')
    print(f'   both batches together against the study\'s mutation at 1%: {a[1] + b[1]} of 60 against 18 of 30, p = {fe(a[1] + b[1], 60, 18, 30):.2g}')
    lo, hi = cp(ha[1] + hb[1], 60); print(f'   handshake-led at 1%, both batches: {ha[1] + hb[1]} of 60, 95% interval {lo:.0%} to {hi:.0%}; at 2%: {ha[2] + hb[2]} of 60')
    for name, label in (('replay_ties_fresh.json', 'ties broken at random'), ('replay_played_fresh.json', 'matches played out once'), ('replay_exact200_fresh.json', 'exactly 200 rounds, exact'),
                        ('replay_h2h_fresh.json', 'winner of the pair\'s game'), ('replay_one_fresh.json', 'exactly one element'), ('replay_rate8_fresh.json', '8% an element'), ('replay_rate12_fresh.json', '12% an element')):
        if not os.path.exists(D + name): continue
        c = cnt(name)
        print(f'   {label}: all-defect {c}; against the sealed design\'s two batches together, p at 1%, 2%, 4% = ' + ', '.join(f'{fe(c[k], 30, a[k] + b[k], 60):.2g}' for k in (1, 2, 3))
              + f'; against his 19 and 22: p = {fe(c[2], 30, 19, 30):.2g}, {fe(c[3], 30, 22, 30):.2g}')

# exact payoffs against matches played out, all the string-mutation batches of replay.py together
EXACT = ('replay_text_same.json', 'replay_text_fresh.json', 'replay_one_fresh.json', 'replay_rate8_fresh.json', 'replay_rate12_fresh.json', 'replay_ties_fresh.json',
         'replay_h2h_fresh.json', 'replay_exact200_fresh.json', 'replay_norm_fresh.json')
ONCE = ('replay_played_fresh.json', 'replay_playednorm_fresh.json', 'replay_playedh2h_fresh.json', 'replay_playedone_fresh.json', 'replay_playedall_fresh.json')
if all(os.path.exists(D + f) for f in EXACT + ONCE):
    E = [cnt(f) for f in EXACT]; O = [cnt(f) for f in ONCE]
    print('\nall-defect commonest, by batch, exact payoffs:', E); print('all-defect commonest, by batch, matches played out once:', O)
    for k, r in ((2, '2%'), (3, '4%')):
        e = sum(x[k] for x in E); o = sum(x[k] for x in O)
        print(f'   {r}: exact {e} of {30 * len(E)} (batches from {min(x[k] for x in E)} to {max(x[k] for x in E)}); played out once {o} of {30 * len(O)} (batches from {min(x[k] for x in O)} to {max(x[k] for x in O)}); '
              f'exact against played p = {fe(e, 30 * len(E), o, 30 * len(O)):.2g}; his {(19, 22)[k - 2]} of 30 against exact p = {fe((19, 22)[k - 2], 30, e, 30 * len(E)):.2g}, against played p = {fe((19, 22)[k - 2], 30, o, 30 * len(O)):.2g}')
    P = lambda f, k: [sum(x['payoff'] for x in json.load(open(D + f)) if x['rate'] == r) / 30 for r in (0.0, 0.01, 0.02, 0.04)][k]
    for k, r in ((0, '0%'), (1, '1%'), (2, '2%'), (3, '4%')):
        print(f'   mean payoff at {r}: exact batches {min(P(f, k) for f in EXACT):.2f} to {max(P(f, k) for f in EXACT):.2f}; played out once {min(P(f, k) for f in ONCE):.2f} to {max(P(f, k) for f in ONCE):.2f}')
    Cq = lambda f: [sum(x['coop'] for x in json.load(open(D + f)) if x['rate'] == r) / 30 for r in (0.0, 0.01, 0.02, 0.04)]
    print('   cooperation falls at each step of the error rate in every batch:', all(c[0] > c[1] > c[2] > c[3] for c in map(Cq, EXACT + ONCE + ('replay_played5_fresh.json', 'replay_study_same.json'))))
    H = [cnt(f, 'top_is_handshake') for f in EXACT + ONCE + ('replay_played5_fresh.json',)]
    print('   handshake at an entry state, by batch, at 1%:', [h[1] for h in H], '; at 2%:', [h[2] for h in H])

# the second batches of two variants (second_batch.py)
if os.path.exists(D + 'second_ties.json') and os.path.exists(D + 'second_played.json'):
    t1, t2, p1, p2 = cnt('replay_ties_fresh.json'), cnt('second_ties.json'), cnt('replay_played_fresh.json'), cnt('second_played.json')
    a, b = cnt('replay_text_same.json'), cnt('replay_text_fresh.json')
    others = [cnt(f) for f in EXACT if f != 'replay_ties_fresh.json']
    print('\nties broken at random, two batches:', t1, t2, '; matches played out once, two batches:', p1, p2)
    e2 = sum(x[2] for x in others)
    print(f'   ties at 2%: {t1[2] + t2[2]} of 60 against the sealed design\'s {a[2] + b[2]} of 60, p = {fe(t1[2] + t2[2], 60, a[2] + b[2], 60):.2g}; against all eight batches with exact payoffs and the listed-first rule, {e2} of {30 * len(others)} (batches {sorted(x[2] for x in others)}), p = {fe(t1[2] + t2[2], 60, e2, 30 * len(others)):.2g}')
    print(f'   ties at 4%: {t1[3] + t2[3]} of 60 against {a[3] + b[3]} of 60, p = {fe(t1[3] + t2[3], 60, a[3] + b[3], 60):.2g}')
    print(f'   played out once at 4%: {p1[3] + p2[3]} of 60 against the sealed design\'s {a[3] + b[3]} of 60, p = {fe(p1[3] + p2[3], 60, a[3] + b[3], 60):.2g}; against his 22 of 30, p = {fe(p1[3] + p2[3], 60, 22, 30):.2g}')
    print(f'   played out once at 2%: {p1[2] + p2[2]} of 60 against the sealed design\'s {a[2] + b[2]} of 60, p = {fe(p1[2] + p2[2], 60, a[2] + b[2], 60):.2g}; against his 19 of 30, p = {fe(p1[2] + p2[2], 60, 19, 30):.2g}')
    O6 = [cnt(f) for f in ONCE] + [p2]; E9 = [cnt(f) for f in EXACT] + [t2]
    print(f'   all batches played out once, 4%: {sorted(x[3] for x in O6)} = {sum(x[3] for x in O6)} of {30 * len(O6)}; all batches with exact payoffs, 4%: {sorted(x[3] for x in E9)} = {sum(x[3] for x in E9)} of {30 * len(E9)}; p = {fe(sum(x[3] for x in O6), 30 * len(O6), sum(x[3] for x in E9), 30 * len(E9)):.2g}')
    print(f'   all batches, 2%: played out once {sorted(x[2] for x in O6)}; exact {sorted(x[2] for x in E9)}; five times a pair {cnt("replay_played5_fresh.json")[2]}')
    allb = EXACT + ONCE + ('replay_played5_fresh.json', 'second_ties.json', 'second_played.json')
    print('   batches of the string scheme in all:', len(allb), '; all-defect at 2% from', min(cnt(f)[2] for f in allb), 'to', max(cnt(f)[2] for f in allb), '; at 1% from', min(cnt(f)[1] for f in allb), 'to', max(cnt(f)[1] for f in allb), '; at 0%:', sorted(set(cnt(f)[0] for f in allb)))
    print('   handshake at an entry state at 1%, all batches:', sorted(cnt(f, 'top_is_handshake')[1] for f in allb))
    print('   cooperation falls at each step in every batch:', all(c[0] > c[1] > c[2] > c[3] for c in map(Cq, allb)))
    P2 = lambda f: [sum(x['payoff'] for x in json.load(open(D + f)) if x['rate'] == r) / 30 for r in (0.0, 0.01, 0.02, 0.04)]
    print('   mean payoff at 4%: played out once', sorted(round(P2(f)[3], 2) for f in ONCE + ('second_played.json',)), '; exact', sorted(round(P2(f)[3], 2) for f in EXACT + ('second_ties.json',)))
    print('   last generation only: same or fewer all-defect runs than over the last 100, every batch and rate:', all(lk <= tk for f in allb for key in ('last_plural_is_alld', 'last_best_is_alld') for lk, tk in zip(cnt(f, key), cnt(f))))
