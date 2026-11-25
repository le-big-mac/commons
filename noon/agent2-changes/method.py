"""Plain Bob Doubles: find a touch that rings all 120 orders of five bells once each and comes back to rounds.
usage: python method.py out.json
A change swaps neighbouring bells except in the places named: "5" keeps the bell in fifth place where it is and swaps
the pairs in places 1-2 and 3-4; "1" keeps the first and swaps 2-3 and 4-5.  A lead is ten changes: 5 1 5 1 5 1 5 1 5
and then the lead end, which is "125" (plain) or "145" (a bob, called by the conductor)."""
import sys, json, itertools

def change(row, places):
    row = list(row); i = 0
    while i < 5:
        if (i + 1) in places:
            i += 1
        else:
            row[i], row[i + 1] = row[i + 1], row[i]; i += 2
    return tuple(row)

LEAD = [{5}, {1}, {5}, {1}, {5}, {1}, {5}, {1}, {5}]
END = {'P': {1, 2, 5}, 'B': {1, 4, 5}}

def ring(calls):
    row = (1, 2, 3, 4, 5); rows = []
    for c in calls:
        for pl in LEAD + [END[c]]:
            rows.append(row)                      # the row rung, then the change that follows it
            row = change(row, pl)
    return rows, row

found = []
for calls in itertools.product('PB', repeat=12):
    rows, last = ring(calls)
    if last == (1, 2, 3, 4, 5) and len(set(rows)) == 120:
        found.append(''.join(calls))
print(len(found), "touches of twelve leads ring every row once and come round:", found)
plain, last = ring('PPPP')
print("the plain course (no calls):", len(plain), "rows,", len(set(plain)), "different, comes round:", last == (1, 2, 3, 4, 5))
best = sorted(found, key=lambda c: (c.count('B'), c))[0]
rows, last = ring(best)
assert sorted(rows) == sorted(itertools.permutations(range(1, 6))) and last == (1, 2, 3, 4, 5)
assert all(sum(abs(a.index(b) - c.index(b)) for b in range(1, 6)) <= 4 and all(abs(a.index(b) - c.index(b)) <= 1 for b in range(1, 6)) for a, c in zip(rows, rows[1:] + [last]))
print("chosen:", best, "with", best.count('B'), "bobs; every bell moves at most one place at each change; all 120 orders rung once")
json.dump(dict(calls=best, rows=rows, all=found), open(sys.argv[1], 'w'))
for k in range(0, 21):
    print(''.join(map(str, rows[k])), end='  ')
print()
