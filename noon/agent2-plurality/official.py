"""Do my recounted winners in New South Wales match the members who sat?   usage: python -I official.py results.json MEMBERSDIR
MEMBERSDIR holds the raw text of Wikipedia's three lists "Members of the New South Wales Legislative Assembly, 2015-2019",
"2019-2023" and "2023-2027" (members-2015.wiki and so on).  A list also names members who came in at by-elections, so
a match means: my winner is one of the people who sat for that seat in that parliament."""
import sys, re, json, collections
rows = [r for r in json.load(open(sys.argv[1]))['rows'] if r['set'] == 'nswla']
norm = lambda s: re.sub(r"[^a-z]", "", s.lower().replace("’", "").replace("'", ""))
total = ok = 0
for year in ("2015", "2019", "2023"):
    text = open(f"{sys.argv[2]}/members-{year}.wiki", encoding='utf-8').read()
    seats = collections.defaultdict(list)
    for block in text.split("|-"):
        m = re.search(r"\{\{sortname\|([^|}]*)\|([^|}]*)", block)
        e = re.search(r"\[\[Electoral district of ([^|\]]*)", block)
        if m and e:
            seats[norm(re.sub(r"\(.*?\)", "", e.group(1)))].append((m.group(1).strip(), m.group(2).strip()))
    mine = [r for r in rows if r['title'].endswith(year)]
    several = sum(len(v) > 1 for v in seats.values())
    print(f"{year}: {len(mine)} elections recounted; the list has {len(seats)} seats, {several} of them with more than one member in the term")
    for r in mine:
        seat = norm(r['title'][:-4])
        total += 1
        got = norm(r['runoff'])
        hit = [p for p in seats.get(seat, []) if norm(p[1]) in got and norm(p[0].split()[0]) in got]
        if hit:
            ok += 1
        else:
            print(f"   NO MATCH  {r['title']}: I elect {r['runoff']}; the list has {seats.get(seat)}")
print(f"my winner is a member who sat for the seat in that parliament: {ok} of {total}")
