"""Second reader: the course of the mean payoff over the 500 generations in the sealed design (the sealed batch and a fresh batch
from replay.py), set beside the values read off Ioannou's Figure 4 by read_fig4.py.   usage: python -I -B curve_compare.py"""
import json, os
import numpy as np
D = '/home/agent3/welch-prior/corner/check-2-scripts/'
HIS = {50: (2.73, 2.00, 1.71, 1.34), 100: (2.78, 2.13, 1.70, 1.34), 150: (2.78, 2.17, 1.85, 1.35), 200: (2.73, 2.22, 1.91, 1.36), 300: (2.74, 2.33, 1.86, 1.42),
       400: (2.76, 2.46, 1.85, 1.49), 450: (2.80, 2.53, 1.89, 1.43), 490: (2.85, 2.54, 1.91, 1.45)}       # from read_fig4.out
RATES = (0.0, 0.01, 0.02, 0.04)
R = json.load(open(D + 'replay_text_same.json')) + json.load(open(D + 'replay_text_fresh.json'))
for extra in ('replay_played_fresh.json',):
    pass
def table(R, label):
    print(label)
    print('   generation | ' + ' | '.join(f'{r:.0%}: mine (s.e.), his, difference in s.e. of mine' for r in RATES))
    for G, his in HIS.items():
        out = []
        for r, h in zip(RATES, his):
            c = np.array([x['curve'] for x in R if x['rate'] == r]); w = c[:, max(0, G - 11):G + 10].mean(1)      # each run averaged over 21 generations about G
            se = w.std(ddof=1) / len(w) ** .5
            out.append(f'{w.mean():.2f} ({se:.2f}), {h:.2f}, {(w.mean() - h) / se:+.1f}')
        print(f'   {G:10d} | ' + ' | '.join(out))
table(R, f'sealed batch and a fresh batch of elite.py together ({len(R) // 4} runs a rate), each run averaged over 21 generations about the one named:')
p = D + 'replay_played_fresh.json'
if os.path.exists(p): table(json.load(open(p)), 'matches played out once over 200 rounds (30 runs a rate):')
