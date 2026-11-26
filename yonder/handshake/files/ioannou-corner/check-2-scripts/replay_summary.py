"""Second reader: summarise the replays and side runs of replay.py.   usage: python -I -B replay_summary.py"""
import sys, json, os
import numpy as np
D = '/home/agent3/welch-prior/corner/check-2-scripts/'; C = '/home/agent3/welch-prior/corner/'
RATES = (0.0, 0.01, 0.02, 0.04)
def load(name):
    p = D + name
    return json.load(open(p)) if os.path.exists(p) else None

# 1. the replays with the sealed seeds must give the sealed files
for mine, theirs in (('replay_text_same.json', 'elite_run.json'), ('replay_study_same.json', 'elite_after.json')):
    a, b = load(mine), json.load(open(C + theirs))
    if a is None: print(mine, 'not there yet'); continue
    same = all(all(x[k] == y[k] for k in y) for x, y in zip(a, b)) and len(a) == len(b)
    print(f'{mine} against {theirs}: every field of the {len(b)} runs reproduced: {same}')

LABEL = {'replay_text_same.json': 'elite.py replayed with its own seeds (the sealed run)',
         'replay_text_fresh.json': 'elite.py, fresh seeds (a second batch of the sealed design)',
         'replay_study_same.json': 'elite_after.py replayed with its own seeds (the study\'s mutation)',
         'replay_one_fresh.json': 'exactly one element of 25 switched in every newcomer (Figure 3 by its letter)',
         'replay_rate8_fresh.json': 'each element changed at 8% (footnote 7)',
         'replay_rate12_fresh.json': 'each element changed at 12% (footnote 7)',
         'replay_ties_fresh.json': 'exact ties at the cut broken at random',
         'replay_h2h_fresh.json': 'better of a pair = winner of the game between the two',
         'replay_exact200_fresh.json': 'exact payoffs over exactly 200 rounds',
         'replay_played_fresh.json': 'matches played out once, 200 rounds, errors drawn',
         'replay_played5_fresh.json': 'matches played out five times a pair and averaged (Miller 1996 did this)',
         'replay_norm_fresh.json': 'pairs drawn by Miller\'s normalised score, exact payoffs',
         'replay_playednorm_fresh.json': 'played out once, pairs drawn by Miller\'s normalised score',
         'replay_playedh2h_fresh.json': 'played out once, newcomer copies the winner of the pair\'s one match (Figure 3 by its letter)',
         'replay_playedone_fresh.json': 'played out once, exactly one element switched in every newcomer',
         'replay_playedall_fresh.json': 'played out once, normalised draw, winner of the pair\'s match, exactly one element switched'}
GEN = (1, 10, 25, 50, 100, 200, 300, 400, 450, 500)
for name, label in LABEL.items():
    R = load(name)
    if R is None: continue
    print(f'\n== {label}  [{name}]')
    print('   error: all-defect commonest over the last 100 generations | most often the largest group in the last 100 | largest group in the last generation | top scorer of the last generation'
          ' || handshake at an entry state | handshake after a prefix too || mean payoff (standard error) | cooperation || newcomers: string unchanged | machine unchanged || generations with an exact tie at the cut between different machines')
    for r in RATES:
        c = [x for x in R if x['rate'] == r]; n = len(c); pay = np.array([x['payoff'] for x in c])
        nn = sum(x['newcomers'] for x in c)
        print(f'   {r:.0%}: {sum(x["top_is_alld"] for x in c):2d} | {sum(x["plural_is_alld"] for x in c):2d} | {sum(x["last_plural_is_alld"] for x in c):2d} | {sum(x["last_best_is_alld"] for x in c):2d}'
              f' || {sum(x["top_is_handshake"] for x in c):2d} | {sum(x["top_handshake_cored"] for x in c):2d} || {pay.mean():.2f} ({pay.std(ddof=1) / n ** .5:.2f}) | {np.mean([x["coop"] for x in c]):.0%}'
              f' || {sum(x["same_string"] for x in c) / nn:.0%} | {sum(x["same_machine"] for x in c) / nn:.0%} || {sum(x["tie_cut"] for x in c) / (n * 500):.0%}   (of {n})')
    print('   mean payoff a round by generation (mean of 30 runs; generations ' + ', '.join(map(str, GEN)) + '; then the mean over 401 to 500):')
    for r in RATES:
        cur = np.array([x['curve'] for x in R if x['rate'] == r]).mean(0)
        print(f'   {r:.0%}: ' + '  '.join(f'{cur[g - 1]:.2f}' for g in GEN) + f'   | {cur[400:].mean():.2f}')

print('\n== all batches in brief: all-defect commonest of 30 at 0, 1, 2, 4% | handshake at an entry state | mean payoff | cooperation')
for name, label in LABEL.items():
    R = load(name)
    if R is None: continue
    cells = [[x for x in R if x['rate'] == r] for r in RATES]
    print('   ' + ', '.join(f'{sum(x["top_is_alld"] for x in c):2d}' for c in cells) + ' | ' + ', '.join(f'{sum(x["top_is_handshake"] for x in c):2d}' for c in cells)
          + ' | ' + ', '.join(f'{np.mean([x["payoff"] for x in c]):.2f}' for c in cells) + ' | ' + ', '.join(f'{np.mean([x["coop"] for x in c]):.0%}' for c in cells) + '   ' + label)
print('   his paper:  -,  -, 19, 22 | not said | 2.80, 2.52, 1.89, 1.45 (Figure 4 averaged over generations 400 to 500, as measured by read_fig4.py) | not given')
