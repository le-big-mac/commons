"""Compare the hand-written finite-state machines in the Axelrod library's finite_state_machines.py
(read as TEXT, never imported or executed) with the machines of the welch study.
usage: axelrod_compare.py PATH_TO_finite_state_machines.py
The Axelrod machines are Mealy machines: (state, opponent's last action, next state, next action), plus an
initial state and an initial action.  They are converted to Moore machines (action attached to the state),
minimised with the study's own canonical(), and compared by canonical key."""
import sys, re, itertools
import numpy as np
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical, M

text = open(sys.argv[1], encoding='utf-8', errors='replace').read()
classes = re.split(r'\nclass ', text)[1:]

def moore(transitions, init_state, init_action):
    """Moore states are (mealy state, action being played)."""
    tr = {(s, a): (ns, na) for s, a, ns, na in transitions}
    start = (init_state, init_action)
    order = [start]; idx = {start: 0}
    for st in order:
        for a in 'CD':
            nxt = tr[(st[0], a)]
            if nxt not in idx:
                idx[nxt] = len(order); order.append(nxt)
    play = [0 if st[1] == 'C' else 1 for st in order]
    nx = [[idx[tr[(st[0], 'C')]], idx[tr[(st[0], 'D')]]] for st in order]
    return canonical(FSM(0, play, nx))

lib = {}
for c in classes:
    name = re.match(r'(\w+)', c).group(1)
    m = re.search(r'transitions\s*=\s*\((.*?)\n\s*\)\n', c, re.S)
    if not m: continue
    tups = re.findall(r'\(\s*(\d+)\s*,\s*([CD])\s*,\s*(\d+)\s*,\s*([CD])\s*\)', m.group(1))
    if not tups: continue
    ini = re.search(r'initial_state\s*=\s*(\d+)\s*,\s*initial_action\s*=\s*([CD])', c, re.S)
    if not ini: continue
    try:
        lib[name] = moore([(int(s), a, int(ns), na) for s, a, ns, na in tups], int(ini.group(1)), ini.group(2))
    except KeyError as e:
        print('could not convert', name, e)

mine = {
 'handshake':        M('handshake', 0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)]),
 'shifty handshake': M('shifty handshake', 0, [('D', 1, 2), ('D', 1, 0), ('C', 2, 1)]),
 'stiffened wooer':  M('stiffened wooer', 0, [('C', 0, 1), ('D', 1, 2), ('D', 1, 0)]),
 'Tat for Tit (2 states)': M('tat for tit', 0, [('D', 0, 1), ('C', 1, 0)]),
 'handshake with three defecting states': M('h4', 0, [('D', 0, 1), ('D', 0, 2), ('D', 0, 3), ('C', 3, 0)]),
 'four-state wooer with one free pass': M('w4', 0, [('C', 0, 1), ('C', 1, 2), ('D', 2, 3), ('D', 2, 1)]),
 'handshake, unconditional first step (Schlag b*, u=2)': M('hb', 0, [('D', 1, 1), ('D', 0, 2), ('C', 2, 0)]),
}
print('Axelrod machines parsed:', len(lib))
for k, v in lib.items():
    print(f'  {k:22s} {v!r}')
print()
for mk, mv in mine.items():
    ck = canonical(mv).key()
    hits = [k for k, v in lib.items() if v.key() == ck]
    print(f'{mk:55s} {canonical(mv)!r}\n      identical Axelrod machines: {hits if hits else "none"}')
