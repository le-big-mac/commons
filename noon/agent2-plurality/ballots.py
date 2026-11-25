"""Plurality, instant runoff and the Condorcet winner in real ranked-ballot elections (PrefLib files).
usage: python -I ballots.py DATADIR out.json

Rules (fixed in expectations.md): a ballot puts every candidate it ranks above every one it leaves out, and says
nothing between those it leaves out or between candidates it ties.  X beats Y if more ballots put X above Y than
Y above X.  The Condorcet winner beats every other candidate.  Plurality: most ballots with that candidate alone
in first place.  Instant runoff: the candidate with fewest current first places drops out; a ballot whose
highest remaining place is empty or shared is set aside; until someone has more than half of the ballots still
counting.
"""
import sys, os, re, glob, json
import numpy as np

MULTI_SEAT = ("Aspen City Council 2009", "Minneapolis Park and Recreation", "Minneapolis Board of Estimate")


def read(path):
    names, ballots, title = {}, [], ''
    for line in open(path, encoding='utf-8', errors='replace'):
        line = line.strip()
        if line.startswith('# TITLE:'):
            title = line[8:].strip()
        m = re.match(r"# ALTERNATIVE NAME (\d+): (.*)", line)
        if m:
            names[int(m.group(1))] = m.group(2).strip()
        if not line or line.startswith('#'):
            continue
        count, rest = line.split(':', 1)
        groups = []
        for tok in re.findall(r"\{[^}]*\}|[^,{}]+", rest):
            tok = tok.strip()
            if not tok:
                continue
            groups.append(tuple(int(x) for x in tok.strip('{}').split(',') if x.strip()))
        ballots.append((int(count), groups))
    return title, names, ballots


def analyse(title, names, ballots):
    ids = sorted(names)
    k = {c: i for i, c in enumerate(ids)}
    n = len(ids)
    P = np.zeros((n, n))                                                # P[a, b]: ballots that put a above b
    first = np.zeros(n)
    for cnt, groups in ballots:
        ranked = [k[c] for g in groups for c in g]
        rest = [i for i in range(n) if i not in set(ranked)]
        for gi, g in enumerate(groups):
            below = [k[c] for h in groups[gi + 1:] for c in h] + rest
            for a in g:
                P[k[a], below] += cnt
        if groups and len(groups[0]) == 1:
            first[k[groups[0][0]]] += cnt
    beats = P > P.T
    cw = [i for i in range(n) if beats[i].sum() == n - 1]
    cw = cw[0] if cw else None
    order = np.argsort(-first)
    plur = int(order[0])
    plur_tie = bool(first[order[0]] == first[order[1]])
    # instant runoff
    alive = set(range(n))
    rounds, tie_break = 0, False
    while True:
        tally = np.zeros(n)
        for cnt, groups in ballots:
            for g in groups:
                live = [k[c] for c in g if k[c] in alive]
                if live:
                    if len(live) == 1:
                        tally[live[0]] += cnt
                    break                                               # a shared highest place sets the ballot aside
        total = tally.sum()
        rounds += 1
        best = max(alive, key=lambda i: tally[i])
        if tally[best] * 2 > total or len(alive) == 1:
            irv = best
            break
        low = min(tally[i] for i in alive)
        lows = [i for i in alive if tally[i] == low]
        if len(lows) > 1:
            tie_break = True
            lows = [min(lows, key=lambda i: (first[i], -i))]            # a tie for last: the one with fewer first choices at the start goes
        alive.discard(lows[0])
    rank_by_first = {int(c): r for r, c in enumerate(order)}
    return dict(title=title, candidates=n, voters=int(sum(c for c, _ in ballots)), condorcet=names[ids[cw]] if cw is not None else None,
                plurality=names[ids[plur]], runoff=names[ids[irv]], plurality_tie=plur_tie, runoff_tie=tie_break, rounds=rounds,
                condorcet_place_by_first_choices=(rank_by_first[cw] + 1) if cw is not None else None,
                first_share_plurality=float(first[plur] / max(first.sum(), 1)), first_share_condorcet=float(first[cw] / max(first.sum(), 1)) if cw is not None else None,
                smith=None if cw is not None else smith_set(beats, names, ids))


def smith_set(beats, names, ids):
    """the smallest group of candidates each of whom beats or ties everyone outside it"""
    n = len(ids)
    wins = sorted(range(n), key=lambda i: -beats[i].sum())
    for m in range(1, n + 1):
        S = set(wins[:m])
        if all(not beats[j, i] for i in S for j in range(n) if j not in S) and all(beats[i, j] or not beats[j, i] for i in S for j in range(n) if j not in S):
            return [names[ids[i]] for i in S]
    return None


if __name__ == '__main__':
    D, OUT = sys.argv[1], sys.argv[2]
    rows, skipped = [], []
    for d in sorted(os.listdir(D)):
        files = sorted(glob.glob(f"{D}/{d}/*.soi") + glob.glob(f"{D}/{d}/*.toi"))
        for f in files:
            title, names, ballots = read(f)
            if any(title.startswith(m) or m in title for m in MULTI_SEAT):
                skipped.append((os.path.basename(f), title, 'more than one seat'))
                continue
            if len(names) < 3:
                skipped.append((os.path.basename(f), title, 'fewer than three candidates'))
                continue
            r = analyse(title, names, ballots)
            r['set'] = d
            r['file'] = os.path.basename(f)
            rows.append(r)
    json.dump(dict(rows=rows, skipped=skipped), open(OUT, 'w'), indent=1)
    print(f"elections analysed: {len(rows)}; left out: {len(skipped)}:", [(s[1], s[2]) for s in skipped])
    b = next(r for r in rows if r['title'] == '2009 Burlington Mayoral Election')
    print(f"V1  Burlington 2009: Condorcet winner {b['condorcet']}; plurality winner {b['plurality']}; instant runoff elects {b['runoff']}")
    for name, sel in (("all", rows), ("New South Wales", [r for r in rows if r['set'] == 'nswla']), ("American", [r for r in rows if r['set'] != 'nswla'])):
        n = len(sel)
        has = [r for r in sel if r['condorcet'] is not None]
        pl = [r for r in has if r['plurality'] == r['condorcet']]
        ir = [r for r in has if r['runoff'] == r['condorcet']]
        dis = [r for r in has if r['plurality'] != r['condorcet']]
        fixed = [r for r in dis if r['runoff'] == r['condorcet']]
        print(f"{name}: {n} elections")
        print(f"   V2  with a Condorcet winner: {len(has)} ({100 * len(has) / n:.1f}%)")
        print(f"   V3  plurality winner is the Condorcet winner: {len(pl)} of {len(has)} ({100 * len(pl) / len(has):.1f}%)")
        print(f"   V4  instant runoff elects the Condorcet winner: {len(ir)} of {len(has)} ({100 * len(ir) / len(has):.1f}%); fails in {len(has) - len(ir)}")
        print(f"   V5  where plurality and Condorcet differ ({len(dis)}): instant runoff elects the Condorcet winner in {len(fixed)}" + (f" ({100 * len(fixed) / len(dis):.0f}%)" if dis else ""))
    print("no Condorcet winner:")
    for r in rows:
        if r['condorcet'] is None:
            print(f"   {r['title']}: the candidates who beat all others but not each other: {r['smith']}; plurality {r['plurality']}; runoff {r['runoff']}")
    print("instant runoff did not elect the Condorcet winner:")
    for r in rows:
        if r['condorcet'] is not None and r['runoff'] != r['condorcet']:
            print(f"   {r['title']}: Condorcet {r['condorcet']} (place {r['condorcet_place_by_first_choices']} by first choices, {100 * r['first_share_condorcet']:.1f}%); runoff elects {r['runoff']}; plurality {r['plurality']}")
    places = [r['condorcet_place_by_first_choices'] for r in rows if r['condorcet'] is not None and r['plurality'] != r['condorcet']]
    print("where plurality and Condorcet differ, the Condorcet winner's place by first choices:", {p: places.count(p) for p in sorted(set(places))})
    print("ties met: plurality", sum(r['plurality_tie'] for r in rows), "; in a runoff elimination", sum(r['runoff_tie'] for r in rows))
    print("candidates per election: median", int(np.median([r['candidates'] for r in rows])), "; voters: median", int(np.median([r['voters'] for r in rows])))
