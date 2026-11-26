"""Three small checks for the prior-art report (reads the welch study's ipd.py; writes nothing).
 1. The study's three cooperative machines are one transition table (Iwasaki et al.'s 2-MP, Fig. 9) entered at
    its three states.
 2. Where the study's noise sits in Iwasaki et al.'s monitoring parameters (p, q, s).
 3. Best reply to each machine by an opponent who DOES see its own realised move (so knows the machine's
    state exactly): a three-state Markov decision problem, solved by value iteration.  Compare with the
    README's bound for an opponent who does not see its own slips.
usage: checks.py"""
import sys
import numpy as np
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical, payoff, M, PAY

# 1. 2-MP as drawn in Iwasaki et al. Fig. 9: R plays C (g: stay, b: P1); P1 plays D (g: stay, b: P2); P2 plays D (g: P1, b: R)
R, P1, P2 = 0, 1, 2
play = [0, 1, 1]; nxt = [[R, P1], [P1, P2], [P1, R]]
mine = {'stiffened wooer': M('w', 0, [('C', 0, 1), ('D', 1, 2), ('D', 1, 0)]),
        'handshake':       M('h', 0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)]),
        'shifty handshake': M('s', 0, [('D', 1, 2), ('D', 1, 0), ('C', 2, 1)])}
print('1. 2-MP entered at each of its states, against the study\'s machines')
for start, nm in ((R, 'R'), (P1, 'P1'), (P2, 'P2')):
    k = canonical(FSM(start, play, nxt)).key()
    print(f'   2-MP started in {nm}: identical to', [n for n, m in mine.items() if canonical(m).key() == k])
# 3-MP started in P1 against the four-state Fortress4 shape
k3 = canonical(FSM(1, [0, 1, 1, 1], [[0, 1], [1, 2], [1, 3], [1, 0]])).key()
print('   3-MP started in P1 identical to 0:D[0,1] 1:D[0,2] 2:D[0,3] 3:C[3,0]:',
      k3 == canonical(M('f4', 0, [('D', 0, 1), ('D', 0, 2), ('D', 0, 3), ('C', 3, 0)])).key())

print('\n2. independent flips at rate e, as Iwasaki et al. monitoring parameters: p=(1-e)^2 both right, q=e(1-e) exactly one wrong (each way), s=e^2')
for e in (0.01, 0.05, 0.10):
    print(f'   e={e}: p={(1-e)**2:.4f} q={e*(1-e):.4f} s={e*e:.4f}')

print('\n3. best reply when the opponent sees its own realised move (knows the machine state), continuation 0.99')
delta = 0.99
for e in (0.01, 0.05, 0.10):
    for n, m in mine.items():
        px = np.array([[1 - e, e], [e, 1 - e]])                       # P(realised x | intended a)
        py = np.where(m.play[:, None] == np.arange(2), 1 - e, e)       # P(machine's realised y | its state)
        V = np.zeros(m.n)
        for _ in range(200000):
            Q = np.zeros((2, m.n))
            for a in (0, 1):
                for s in range(m.n):
                    Q[a, s] = sum(px[a, x] * py[s, y] * ((1 - delta) * PAY[x, y] + delta * V[m.nxt[s, x]])
                                  for x in (0, 1) for y in (0, 1))
            Vn = Q.max(0)
            if np.abs(Vn - V).max() < 1e-13: V = Vn; break
            V = Vn
        self_ = payoff(m, m, e, delta)[0]
        pol = ''.join('CD'[i] for i in Q.argmax(0))
        print(f'   e={e} {n:17s} against itself {self_:.4f}; informed best reply {V[m.start]:.4f} (gain {V[m.start]-self_:+.4f}); '
              f'its intended move in machine states 0,1,2: {pol}')

print('\n4. Tat for Tit and Pavlov are one table (Iwasaki et al.\'s 1-MP); and the 2R > T+P boundary with payoffs 5, 3, 1, 0')
pav_R = canonical(FSM(0, [0, 1], [[0, 1], [1, 0]])); pav_P = canonical(FSM(1, [0, 1], [[0, 1], [1, 0]]))
tft2 = canonical(M('Tat for Tit', 0, [('D', 0, 1), ('C', 1, 0)])); wsls = canonical(M('Pavlov', 0, [('C', 0, 1), ('D', 1, 0)]))
print('   1-MP entered at its defecting state is Tat for Tit:', pav_P.key() == tft2.key(),
      '; entered at its cooperating state is the study\'s WSLS/Pavlov:', pav_R.key() == wsls.key())
alld = M('all-defect', 0, [('D', 0, 0)])
for e in (0.0, 0.05):
    for nm, m in (('Pavlov', wsls), ('Tat for Tit', tft2)):
        print(f'   noise {e}: {nm} against itself {payoff(m, m, e, delta)[0]:.4f}; all-defect against it {payoff(alld, m, e, delta)[0]:.4f}')
