"""The same three states begun at each of them: what each earns against its own kind, what a player who always cooperates and
one who always defects earn against it. (Is it the opening that shuts the always-cooperator out, or the routine after any defection?)
usage: entry_states_check.py"""
import sys
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import payoff, M
ms = {'begun defecting, waiting for a first defection (the page\'s machine, Fortress3)': M('h', 0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)]),
      'begun defecting, waiting for a second (the "shifty handshake")': M('s', 0, [('D', 1, 2), ('D', 1, 0), ('C', 2, 1)]),
      'begun cooperating (the "stiffened wooer"; 2-MP as Iwasaki and others draw it)': M('w', 0, [('C', 0, 1), ('D', 1, 2), ('D', 1, 0)])}
allc = M('c', 0, [('C', 0, 0)]); alld = M('d', 0, [('D', 0, 0)])
for eps, delta in ((0.0, 0.99), (0.02, 0.99), (0.03, 0.98), (0.05, 0.99)):
    print(f'slips {eps}, delta {delta}')
    for name, m in ms.items():
        print(f'   {name:80s}: itself {payoff(m, m, eps, delta)[0]:.3f}; always-cooperate earns {payoff(allc, m, eps, delta)[0]:.3f} against it and gives it {payoff(m, allc, eps, delta)[0]:.3f}; always-defect earns {payoff(alld, m, eps, delta)[0]:.3f}')
