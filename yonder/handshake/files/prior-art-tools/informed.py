"""The best reply to the handshake by an opponent who CAN see its own slips (and so always knows the machine's state), against
the study's bound for one who cannot. A three-state decision problem solved by value iteration.
usage: informed.py"""
import sys
import numpy as np
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import payoff, M, PAY
HAND = M('handshake', 0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)])
DELTA = 0.99
for eps in (0.01, 0.05, 0.10):
    play = HAND.play; nxt = HAND.nxt                       # play: 0 = C, 1 = D; nxt[s][what it saw]
    V = np.zeros(3)
    for _ in range(20000):
        Q = np.zeros((3, 2))
        for s in range(3):
            for a in (0, 1):
                for x, px in ((a, 1 - eps), (1 - a, eps)):                      # the opponent's move as it comes out
                    for y, py in ((play[s], 1 - eps), (1 - play[s], eps)):      # the machine's move as it comes out
                        Q[s, a] += px * py * ((1 - DELTA) * PAY[x, y] + DELTA * V[nxt[s][x]])
        Vn = Q.max(1)
        if np.abs(Vn - V).max() < 1e-13: break
        V = Vn
    self_ = payoff(HAND, HAND, eps, DELTA)[0]
    print(f'noise {eps}: handshake against itself {self_:.4f}; an opponent who sees its own slips can earn {V[0]:.4f} (gain {V[0] - self_:+.4f}); its intended moves by the machine\'s state: {["CD"[a] for a in Q.argmax(1)]}')
