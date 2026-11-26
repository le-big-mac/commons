"""The delays in days as well as rounds.   Added 26 November 2026, after a reader's check.
usage: python -I days.py results.json [E0-1920.csv] > days.out        (standard library)
For each of the five matters: how many cases were settled (a case is one club, one season, one matter), in how
many the exact answer came first, and those cases' delays in days and in rounds of matches (a round is ten
league matches).  With the 2019-20 match file named as well: the longest stretch of that season without a match."""
import json, sys, csv, datetime, statistics

if __name__ == '__main__':
    seasons = json.load(open(sys.argv[1]))
    rows = [dict(r, season=s['file'][3:7]) for s in seasons for r in s['results']]
    four = [r for r in rows if r['matter'] in ('title', 'out', 'top4', 'doomed')]
    late = sorted((r for r in four if r['exact'] < r['simple']), key=lambda r: r['lead_days'])
    print(f"the four matters people ask about: {len(four)} cases, the exact answer first in {len(late)}; without the {sum(r['matter'] == 'title' for r in four)} titles, which cannot be late: {len(late)} of {sum(r['matter'] != 'title' for r in four)}")
    for m in ('title', 'out', 'top4', 'doomed', 'safe'):
        t = [r for r in rows if r['matter'] == m]; l = [r for r in t if r['exact'] < r['simple']]
        print(f"   {m}: {len(l)} of {len(t)}")
    print("   their delays in days: " + ", ".join(str(r['lead_days']) for r in late) + "; in rounds: " + ", ".join(f"{r['lead_rounds']:.1f}" for r in late))
    print(f"   the longest: {late[-1]['season']} {late[-1]['team']} ({late[-1]['matter']}), {late[-1]['lead_days']} days, {late[-1]['lead_rounds']:.1f} rounds")
    safe = sorted((r for r in rows if r['matter'] == 'safe' and r['exact'] < r['simple']), key=lambda r: r['lead_days'])
    print(f"safe from relegation: the exact answer first in {len(safe)}; delays from {safe[0]['lead_days']} to {safe[-1]['lead_days']} days, median {statistics.median(r['lead_days'] for r in safe):g}")
    for r in safe[-4:][::-1]:
        print(f"   {r['season']} {r['team']}: exact {r['exact']}, simple {r['simple']}: {r['lead_days']} days, {r['lead_rounds']:.1f} rounds")
    by_rounds = max(safe, key=lambda r: r['lead_rounds'])
    print(f"   the longest in rounds: {by_rounds['season']} {by_rounds['team']}, {by_rounds['lead_rounds']:.1f} rounds, {by_rounds['lead_days']} days")
    if len(sys.argv) > 2:
        def day(t):
            for fmt in ('%d/%m/%Y', '%d/%m/%y'):
                try: return datetime.datetime.strptime(t, fmt).date()
                except ValueError: pass
        ds = sorted(day(r['Date']) for r in csv.DictReader(open(sys.argv[2], encoding='latin-1', newline='')) if r.get('Date'))
        gap, a, b = max(((y - x).days, x, y) for x, y in zip(ds, ds[1:]))
        print(f"2019-20, {len(ds)} matches: the longest stretch without one is {gap} days, from {a} to {b}")
