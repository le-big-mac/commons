"""When is a matter truly settled in a football league?   (Noon = agent2, 21 November 2026)

usage: python -I clinch.py test                 brute-force check of the integer programmes on tiny leagues
       python -I clinch.py run DATADIR out.json [nproc]

A league state = points so far + the fixtures still to play (3 for a win, 1 for a draw).  Five matters, each for
a team t, each with the papers' simple count and an exact answer:
  out      t cannot finish level with or above everyone                       (simple: t's largest total < the leader's points now)
  doomed   t cannot finish with at most 16 teams above it                      (simple: 17 teams already have more than t's largest total)
  safe     t is certain to have at most 16 teams level with or above it        (simple: at most 16 others can still reach t's points now)
  top4     t is certain to have at most 3 teams level with or above it         (simple: at most 3 others can still reach t's points now)
  title    t is certain to finish above everyone                              (simple: nobody can still reach t's points now)
Ties count against the team in the "certain" matters and for it in the "cannot" ones, so goal difference never enters.
Exact: for "cannot", let t win everything left and ask whether the other results can be arranged to keep enough
teams at or below t's total; for "certain", let t lose everything left and ask whether enough teams can reach t.
"""
import sys, csv, json, datetime, itertools
import numpy as np
from ortools.sat.python import cp_model

MATTERS = ['out', 'doomed', 'safe', 'top4', 'title']


def simple(matter, t, pts, left, above=None):
    """left[u] = games u still has to play.  above = (for doomed/safe) the number of teams allowed above: 16; top4: 3."""
    n = len(pts)
    mx = [pts[u] + 3 * left[u] for u in range(n)]
    others = [u for u in range(n) if u != t]
    if matter == 'out':
        return mx[t] < max(pts[u] for u in others)
    if matter == 'doomed':
        return sum(pts[u] > mx[t] for u in others) > above
    if matter in ('safe', 'top4'):
        return sum(mx[u] >= pts[t] for u in others) <= above
    if matter == 'title':
        return all(mx[u] < pts[t] for u in others)


def exact(matter, t, pts, fixtures, above=None, limit=600.0, workers=4):
    """fixtures: list of (home, away) still to play.  Returns True if the matter is settled.

    The programme is shrunk first by results that can never hurt (each is a dominance argument, and the whole is
    checked against brute force in self_test):
    "cannot" matters (t wins everything): a team that cannot pass t's total even by winning everything is harmless;
       games between two harmless teams are dropped, and a harmless team beats any other team it meets.
    "certain" matters (t loses everything): a team that cannot reach t even by winning everything is hopeless, a
       team already level with t is home; a team still in between beats every hopeless or home team it meets, and
       games not involving such a team are dropped.  This is repeated until nothing changes."""
    n = len(pts)
    left = [0] * n
    for h, a in fixtures:
        left[h] += 1
        left[a] += 1
    if simple(matter, t, pts, left, above):
        return True
    cannot = matter in ('out', 'doomed')
    base = list(pts)
    rest = []
    for h, a in fixtures:
        if t in (h, a):
            o = a if h == t else h
            if cannot:
                base[t] += 3
            else:
                base[o] += 3
        else:
            rest.append((h, a))
    others = [u for u in range(n) if u != t]
    target = base[t]
    if cannot:
        togo = [sum(u in f for f in rest) for u in range(n)]
        harmless = {u for u in others if base[u] + 3 * togo[u] <= target}
        live = [f for f in rest if f[0] not in harmless and f[1] not in harmless]     # only games between two teams that could pass t
        teams = sorted({u for f in live for u in f})
        fixed_above = sum(1 for u in others if base[u] > target)                       # already past t for good
        if matter == 'out':
            if fixed_above:
                return True
            if all(base[u] + sum(u in f for f in live) <= target for u in teams):      # all draws is a way out
                return False
        else:
            if fixed_above > above:
                return True
            if sum(1 for u in others if u not in harmless) <= above:                   # even if every such team passes t, t is not doomed
                return False
        m = cp_model.CpModel()
        gain = {u: [] for u in teams}
        for h, a in live:
            x = [m.NewBoolVar('') for _ in range(3)]
            m.AddExactlyOne(x)
            gain[h].append(3 * x[0] + x[1])
            gain[a].append(3 * x[2] + x[1])
        if matter == 'out':
            for u in teams:
                m.Add(base[u] + sum(gain[u]) <= target)
        else:
            b = {}
            for u in others:
                if u in harmless:
                    continue
                if u in gain and base[u] <= target:
                    b[u] = m.NewBoolVar('')                                            # 1: u is allowed to finish above t
                    room = target - base[u]
                    m.Add(sum(gain[u]) <= room + (3 * len(gain[u]) - room) * b[u])     # the tightest such bound
                elif base[u] > target:
                    b[u] = 1
                # a team outside `teams` with base <= target plays only harmless teams from now on, loses to them, and stays below
            m.Add(sum(b.values()) <= above)
    else:
        need = 1 if matter == 'title' else above + 1
        while True:
            togo = [sum(u in f for f in rest) for u in range(n)]
            home = {u for u in others if base[u] >= target}
            hopeless = {u for u in others if base[u] + 3 * togo[u] < target}
            between = [u for u in others if u not in home and u not in hopeless]
            changed = False
            keep = []
            for h, a in rest:
                hb, ab = h in between, a in between
                if hb and ab:
                    keep.append((h, a))
                elif hb:
                    base[h] += 3
                    changed = True
                elif ab:
                    base[a] += 3
                    changed = True
            rest = keep
            if not changed:
                break
        if len(home) >= need:
            return False
        if len(home) + len(between) < need:
            return True
        m = cp_model.CpModel()
        gain = {u: [] for u in between}
        for h, a in rest:
            x = [m.NewBoolVar('') for _ in range(3)]
            m.AddExactlyOne(x)
            gain[h].append(3 * x[0] + x[1])
            gain[a].append(3 * x[2] + x[1])
        c = []
        for u in between:
            cu = m.NewBoolVar('')
            m.Add(sum(gain[u]) >= (target - base[u]) * cu)              # linear, so that the solver's bound sees the points that are available
            c.append(cu)
        m.Add(sum(c) >= need - len(home))
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = limit
    sol.parameters.num_workers = workers
    st = sol.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return False                                                    # a way out (or a way down) exists: not settled
    if st == cp_model.INFEASIBLE:
        return True
    raise RuntimeError(f"solver gave no answer: {sol.StatusName(st)} ({matter}, team {t}, {len(fixtures)} fixtures left)")


def brute(matter, t, pts, fixtures, above=None):
    n = len(pts)
    for outcome in itertools.product(range(3), repeat=len(fixtures)):
        p = list(pts)
        for (h, a), o in zip(fixtures, outcome):
            if o == 0:
                p[h] += 3
            elif o == 1:
                p[h] += 1
                p[a] += 1
            else:
                p[a] += 3
        others = [u for u in range(n) if u != t]
        if matter == 'out' and all(p[u] <= p[t] for u in others):
            return False
        if matter == 'doomed' and sum(p[u] > p[t] for u in others) <= above:
            return False
        if matter in ('safe', 'top4') and sum(p[u] >= p[t] for u in others) > above:
            return False
        if matter == 'title' and any(p[u] >= p[t] for u in others):
            return False
    return True


def self_test(trials=400, seed=5):
    rng = np.random.default_rng(seed)
    n = 5
    allfix = [(h, a) for h in range(n) for a in range(n) if h != a]     # a double round robin of five teams: 20 games
    agree = differ = settled_exact_not_simple = 0
    for _ in range(trials):
        order = rng.permutation(len(allfix))
        played = int(rng.integers(9, 18))
        pts = [0] * n
        for k in order[:played]:
            h, a = allfix[k]
            o = int(rng.choice(3, p=[0.45, 0.25, 0.30]))
            if o == 0:
                pts[h] += 3
            elif o == 1:
                pts[h] += 1
                pts[a] += 1
            else:
                pts[a] += 3
        fixtures = [allfix[k] for k in order[played:]]
        left = [sum(t in f for f in fixtures) for t in range(n)]
        for t in range(n):
            for matter, above in (('out', None), ('doomed', 2), ('safe', 2), ('top4', 1), ('title', None)):
                e, b = exact(matter, t, pts, fixtures, above), brute(matter, t, pts, fixtures, above)
                if e == b:
                    agree += 1
                else:
                    differ += 1
                if b and not simple(matter, t, pts, left, above):
                    settled_exact_not_simple += 1
                assert not (simple(matter, t, pts, left, above) and not b), "the simple count claimed something false"
    print(f"tiny leagues: {agree + differ} questions; integer programme and brute force agree on {agree}, differ on {differ};"
          f" settled in truth but not by the simple count: {settled_exact_not_simple}")
    assert differ == 0


def load(path):
    rows = []
    with open(path, encoding='latin-1', newline='') as f:
        for r in csv.DictReader(f):
            if not r.get('HomeTeam') or not r.get('FTHG'):
                continue
            d = r['Date'].strip()
            fmt = '%d/%m/%Y' if len(d.split('/')[-1]) == 4 else '%d/%m/%y'
            rows.append((datetime.datetime.strptime(d, fmt).date(), r['HomeTeam'].strip(), r['AwayTeam'].strip(), int(r['FTHG']), int(r['FTAG'])))
    rows.sort(key=lambda x: x[0])
    teams = sorted({r[1] for r in rows})
    assert len(rows) == 380 and len(teams) == 20, (path, len(rows), len(teams))
    return rows, teams


def season(path):
    rows, teams = load(path)
    idx = {t: i for i, t in enumerate(teams)}
    dates = sorted({r[0] for r in rows})
    # state k = after the k-th match day (k = 0: before the season)
    pts = [[0] * 20]
    played = [0]
    for d in dates:
        p = list(pts[-1])
        n = 0
        for dd, h, a, gh, ga in rows:
            if dd == d:
                n += 1
                if gh > ga:
                    p[idx[h]] += 3
                elif gh == ga:
                    p[idx[h]] += 1
                    p[idx[a]] += 1
                else:
                    p[idx[a]] += 3
        pts.append(p)
        played.append(played[-1] + n)
    fixtures_after = [[(idx[h], idx[a]) for dd, h, a, _, _ in rows if k == 0 or dd > dates[k - 1]] for k in range(len(dates) + 1)]
    left_after = [[sum(t in f for f in fx) for t in range(20)] for fx in fixtures_after]
    K = len(dates)
    out = []
    for t in range(20):
        for matter, above in (('out', None), ('doomed', 16), ('safe', 16), ('top4', 3), ('title', None)):
            def first(fn):
                if not fn(K):
                    return None
                lo, hi = 0, K                                           # settled at hi; find the first settled state
                while lo < hi:
                    mid = (lo + hi) // 2
                    if fn(mid):
                        hi = mid
                    else:
                        lo = mid + 1
                return lo
            ks = first(lambda k: simple(matter, t, pts[k], left_after[k], above))
            try:
                ke = first(lambda k: exact(matter, t, pts[k], fixtures_after[k], above))
            except RuntimeError as err:                                 # the solver ran out of time on one state: say so, and leave this one out
                out.append(dict(team=teams[t], matter=matter, undetermined=str(err), simple=str(dates[ks - 1]) if ks else None))
                continue
            if ke is None:
                assert ks is None
                continue
            assert ks is not None and ke <= ks
            out.append(dict(team=teams[t], matter=matter, exact=str(dates[ke - 1]) if ke else 'before the season', simple=str(dates[ks - 1]),
                            lead_rounds=(played[ks] - played[ke]) / 10.0, lead_days=(dates[ks - 1] - dates[ke - 1]).days if ke else None,
                            games_left_exact=left_after[ke][t], final_points=pts[K][t]))
    final = sorted(range(20), key=lambda u: -pts[K][u])
    return dict(file=path.split('/')[-1], champion=teams[final[0]], table=[(teams[u], pts[K][u]) for u in final], results=out)


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        self_test()
    else:
        from multiprocessing import Pool
        d, outp = sys.argv[2], sys.argv[3]
        files = [f"{d}/E0-{s}.csv" for s in ('1415', '1516', '1617', '1718', '1819', '1920', '2021', '2122', '2223', '2324')]
        with Pool(int(sys.argv[4]) if len(sys.argv) > 4 else 10) as pool:
            res = pool.map(season, files)
        json.dump(res, open(outp, 'w'), indent=1)
        for matter in MATTERS:
            und = [r for s in res for r in s['results'] if r['matter'] == matter and 'undetermined' in r]
            if und:
                print(f"{matter:7s}: NOT DETERMINED for {len(und)} team-seasons (solver out of time): {[(r['team'], r['simple']) for r in und]}")
            rr = [r for s in res for r in s['results'] if r['matter'] == matter and 'undetermined' not in r]
            lead = np.array([r['lead_rounds'] for r in rr])
            print(f"{matter:7s}: settled for {len(rr)} team-seasons; exact earlier than simple in {int((lead > 0).sum())} ({100 * (lead > 0).mean():.0f}%);"
                  f" mean lead {lead.mean():.2f} rounds; largest {lead.max():.1f}")
            for r in sorted(rr, key=lambda r: -r['lead_rounds'])[:3]:
                s = next(s for s in res if any(r is q for q in s['results']))
                print(f"      {s['file'][3:7]} {r['team']:16s} exact {r['exact']}, simple {r['simple']}: {r['lead_rounds']:.1f} rounds, {r['lead_days']} days")
