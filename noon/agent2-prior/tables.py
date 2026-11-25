"""The audit's table, from the record files.   usage: python -I tables.py > tables.out      (final.json, if present, holds the referee's classes)"""
import json, os, re
F = json.load(open("found.json")); M = json.load(open("mine.json")); C = json.load(open("classes.json")); S = json.load(open("searches.json")); R = json.load(open("final.json")) if os.path.exists("final.json") else {}
NAME = {"W1": "weak tiles of cyclic groups", "W2": "brick bonds", "W3": "opposite points with the same weather", "W4": "desire paths", "W5": "snowdrops", "W6": "when a league is settled", "W7": "what paces the ice ages", "W8": "ranked-ballot elections",
        "W9": "what makes a smell foul", "W10": "born just after the line", "W11": "do numbers decide battles", "W12": "which way up a cube floats", "W13": "which blocks of ice roll over", "W14": "hawks and doves with neighbours", "W15": "the arXiv's daily boundary", "W16": "how chancy is outselling"}
SHORT = {"kadirfan": "Kadir and Fan 2026 (the case pq)", "klms": "Kiss and others 2024", "kmms2": "Kiss and others 2026", "dbwiki": "a building-trade wiki", "multiplicity": "Abdelgalil 2025", "difftop": "lecture notes", "helbing97pdf": "Helbing, Keltsch and Molnár 1997",
         "uba": "Germany's environment agency", "jochner": "Jochner and Menzel 2015", "ribeiropdf": "Ribeiro and Urrutia 2003", "gotzes": "Gotzes and Hoppmann-Baum 2020", "huybers05": "Huybers and Wunsch 2005", "graham23pdf": "Graham-Squire and McCune 2023",
         "keller16": "Keller and Vosshall 2016", "musch99": "Musch and Hay 1999", "dupuy243": "the Dupuy Institute 2019", "anderson22": "Anderson and others 2022", "physicstoday19": "Physics Today 2019", "kantor98": "a university's physics question page", "burton12": "Burton and others 2012",
         "hauert04": "Hauert and Doebeli 2004", "haque09": "Haque and Ginsparg 2009", "jiang16": "Jiang and others 2016", "cam": "Kattuman and Lewis 2007"}
short = lambda e: SHORT[e['name']]
print("AUDIT-ROWS")
for k in sorted(F, key=lambda s: int(s[1:])):
    srcs = "; ".join(short(e) for e in F[k]); print(f"| {k} | {NAME[k]} | {M[k]['what']} | {srcs} | {S[k]} | {C[k]} | {R.get(k, '')} |")
print("COUNTS")
for who, D in (("mine", C), ("referee", R)):
    if D: print(f"{who}: found {sum(v == 'found' for v in D.values())}; found in part {sum(v == 'found in part' for v in D.values())}; not found {sum(v == 'not found' for v in D.values())}")
print(f"searches {sum(S.values())}; sources quoted {sum(len(v) for v in F.values())}; quotations {sum(len(e['quotes']) for v in F.values() for e in v)}")
Q = json.load(open("queries.json")); print(f"the searches' own record: {len(Q)} searches from {Q[0]['time'][11:]} to {Q[-1]['time'][11:]} UTC")
