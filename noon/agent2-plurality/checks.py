"""Afterwards, not registered: how much rests on my rules.   usage: python -I checks.py DATADIR results.json
1  how thin the Condorcet winner's narrowest head-to-head win is
2  how many ballots are short (do not rank everyone) or have a shared place
3  instant runoff under another rule for a shared place (skip it and go on down the ballot)
4  the head-to-head count with short ballots saying nothing about a candidate they leave out against one they rank"""
import sys, json, glob, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))      # -I leaves this folder off the path; the data are elsewhere
from ballots import read, analyse
D = sys.argv[1]
rows = json.load(open(sys.argv[2]))['rows']
thin, short_share, shared_share, one_share = [], [], [], []
changed_irv, changed_cw, no_cw = [], [], []
for r in rows:
    title, names, ballots = read(f"{D}/{r['set']}/{r['file']}")
    ids = sorted(names); k = {c: i for i, c in enumerate(ids)}; n = len(ids)
    tot = sum(c for c, _ in ballots)
    short = sum(c for c, g in ballots if sum(len(x) for x in g) < n - 1)       # ranking all but one is a full ballot
    shared = sum(c for c, g in ballots if any(len(x) > 1 for x in g))
    one = sum(c for c, g in ballots if sum(len(x) for x in g) == 1)
    short_share.append(short / tot); shared_share.append(shared / tot); one_share.append(one / tot)
    # 1: margins
    P = np.zeros((n, n)); Q = np.zeros((n, n))
    for cnt, groups in ballots:
        ranked = set(k[c] for g in groups for c in g)
        rest = [i for i in range(n) if i not in ranked]
        for gi, g in enumerate(groups):
            below = [k[c] for h in groups[gi + 1:] for c in h]
            for a in g:
                P[k[a], below + rest] += cnt
                Q[k[a], below] += cnt                                           # rule 4: only among the ranked
    cw = [i for i in range(n) if (P[i] > P[:, i]).sum() == n - 1][0]
    m = min((P[cw, j] - P[j, cw]) / tot for j in range(n) if j != cw)
    thin.append((m, r['title'], names[ids[cw]], names[ids[int(np.argmin([(P[cw, j] - P[j, cw]) if j != cw else 1e18 for j in range(n)]))]]))
    cq = [i for i in range(n) if (Q[i] > Q[:, i]).sum() == n - 1]
    if not cq:
        no_cw.append(r['title'])
    elif names[ids[cq[0]]] != r['condorcet']:
        changed_cw.append((r['title'], r['condorcet'], names[ids[cq[0]]]))
    # 3: a shared place is skipped
    b2 = [(c, [g for g in groups if len(g) == 1]) for c, groups in ballots]
    r2 = analyse(title, names, b2)
    if r2['runoff'] != r['runoff']:
        changed_irv.append((r['title'], r['runoff'], r2['runoff']))
thin.sort()
print("1  the Condorcet winner's narrowest head-to-head win, as a share of all ballots: the five thinnest")
for m, t, a, b in thin[:5]:
    print(f"     {100 * m:5.2f}%  {t}: {a} over {b}")
print(f"   under 1% in {sum(m < 0.01 for m, *_ in thin)} elections, under 5% in {sum(m < 0.05 for m, *_ in thin)}, of {len(thin)}")
for name, sel in (("New South Wales", [i for i, r in enumerate(rows) if r['set'] == 'nswla']), ("American", [i for i, r in enumerate(rows) if r['set'] != 'nswla'])):
    print(f"2  {name}: median share of ballots that leave two or more candidates unranked {100 * np.median(np.array(short_share)[sel]):.0f}%;"
          f" that rank one candidate only {100 * np.median(np.array(one_share)[sel]):.0f}%; with a shared place {100 * np.median(np.array(shared_share)[sel]):.2f}% (most {100 * np.max(np.array(shared_share)[sel]):.2f}%)")
print("3  instant runoff with a shared place skipped: winners that change:", changed_irv)
print(f"4  head to head counted only among the candidates a ballot ranks: no Condorcet winner in {len(no_cw)} elections; a different one in {len(changed_cw)}"
      f" ({sum(1 for t, *_ in changed_cw if t[-4:] in ('2015', '2019', '2023') and not t.startswith('20'))} of them in New South Wales); for example")
for t, a, b in changed_cw[:1] + [c for c in changed_cw if c[0] in ('Willoughby 2019', '2010 Oakland Mayor')]:
    print(f"     {t}: {b} in place of {a}")
# 5: leave out the elections that were settled on first choices alone
print("5  elections where nobody had more than half of the first choices:")
for name, sel in (("all", rows), ("New South Wales", [r for r in rows if r['set'] == 'nswla']), ("American", [r for r in rows if r['set'] != 'nswla'])):
    open_ = [r for r in sel if r['first_share_plurality'] <= 0.5]
    same = sum(r['plurality'] == r['condorcet'] for r in open_)
    print(f"     {name}: {len(open_)} of {len(sel)}; the first-choice leader is the Condorcet winner in {same} ({100 * same / len(open_):.1f}%)")
print("6  the first-choice leader and the runoff winner differ in", sum(r['plurality'] != r['runoff'] for r in rows), "elections;"
      " the first-choice leader is the Condorcet winner but the runoff winner is not in", sum(r['plurality'] == r['condorcet'] != r['runoff'] for r in rows))
print("7  the Condorcet winner third by first choices:", [(r['title'], r['condorcet'], f"{100 * r['first_share_condorcet']:.1f}%", 'runoff elects ' + r['runoff']) for r in rows if r['condorcet_place_by_first_choices'] == 3])
print("8  a tie for last place in a runoff round:", [(r['title'], r['runoff']) for r in rows if r['runoff_tie']])
gap = sorted(((r['first_share_plurality'] - r['first_share_condorcet']), r['title'], r['condorcet'], r['plurality']) for r in rows if r['plurality'] != r['condorcet'])
print(f"9  the come-from-behind winners: largest gap in first choices {100 * gap[-1][0]:.1f} points ({gap[-1][1]}: {gap[-1][2]} behind {gap[-1][3]}); smallest {100 * gap[0][0]:.3f} points ({gap[0][1]}: {gap[0][2]} behind {gap[0][3]})")
print("   voters in all:", sum(r['voters'] for r in rows), "; years:", sorted(set(t for r in rows for t in __import__('re').findall(r'(?:19|20)\d\d', r['title']))))
