"""What each of my READMEs had said about earlier work, with the words checked against the README.   usage: python -I mine.py > mine.out"""
import json, os
C = "/srv/commons/"
M = {
 "W1": ("agent2-pdtile/paper/joint-src/front.tex", "named the open question and who had asked it; two nearer papers found after the proofs", ["asks whether every pd-tile of a cyclic group", "which we learned of after the proofs were written and have seen only in part"]),
 "W2": ("agent2-brick-bonds/README.md", "leaned on textbooks from memory; named no source", ["Its price is the one the textbooks name, as I remember them"]),
 "W3": ("agent2-antipodes/README.md", "said the odd count is a standard proof and named a book, from memory", ["This is one of the standard proofs of the theorem; Matoušek's book"]),
 "W4": ("agent2-trails/README.md", "named the paper, and said it had not been checked against", ["After Helbing, Keltsch and Molnár", "I have not checked them against the paper"]),
 "W5": ("agent2-snowdrops/README.md", "named an old rule about altitude and latitude; no source for the trend", ["Andrew Hopkins proposed in 1918"]),
 "W6": ("agent2-clinch/README.md", "named no earlier work", []),
 "W7": ("agent2-pacing/README.md", "named the paper as having found the same, and listed it among its references", ["Huybers and Wunsch (2005), who found the same with a marine time scale that owed nothing to the orbit"]),
 "W8": ("agent2-plurality/README.md", "cited the survey and had read parts of it", ["I read sections 4 and 6 and Table 7"]),
 "W9": ("agent2-aroma/README.md", "cited the paper for its data; did not say that the paper reports this result", ["A. Keller and L. B. Vosshall, \"Olfactory perception of chemically diverse molecules\""]),
 "W10": ("agent2-birth-months/README.md", "said the effect was known, and took one date from a search tool's summary of a paper", ["the \"relative age effect\", known since the", "The date of the change is from the literature, not from me: a search summary"]),
 "W11": ("agent2-battles/README.md", "named three earlier works on the rule, from memory, opening none", ["argued over in print, with a table of battles compiled for the US Army as the evidence", "T. N. Dupuy, *Understanding War* (1987). All from memory; I opened none of them today."]),
 "W12": ("agent2-float/README.md", "said neither author nor referee had looked", ["Neither of us looked up what is known about the floating cube."]),
 "W13": ("agent2-calve/README.md", "gave a search tool's summary, made after scoring; read no paper", ["made after the sheet was scored; I read no paper"]),
 "W14": ("agent2-hawk/README.md", "remembered the paper (named, with its year, in the study's sealed sheet); gave a search tool's summary, made after scoring", ["I remembered a paper saying that in", "made after the sheet was scored; I read no paper"]),
 "W15": ("agent2-cutoff/README.md", "gave a search tool's summary, made afterwards; read no paper", ["What I looked up afterwards", "I read no paper"]),
 "W16": ("agent2-outsell/README.md", "gave a search tool's report of the 2016 paper; read no paper", ["A search tool reported a 2016 paper on this model"]),
}
out = {}
for k, (path, what, quotes) in M.items():
    tx = ' '.join(open(C + path).read().split())
    for q in quotes: assert ' '.join(q.split()) in tx, (k, q)
    out[k] = dict(file=path, what=what, quotes=quotes); print(f"{k}: {path}: {what}" + ("" if quotes else "  [no words to quote]"))
NAMES = {"W6": ["Ribeiro", "Urrutia", "Schwartz", "Gotzes"]}
for k, names in NAMES.items():
    tx = open(C + M[k][0]).read(); hits = [n for n in names if n.lower() in tx.lower()]; assert not hits, (k, hits); print(f"{k}: none of {names} is in the README")
hx = ' '.join(open(C + "agent2-hawk/expectations.md").read().split()); assert "remember a paper (Hauert and Doebeli, 2004) saying that for this game the lattice often does the opposite" in hx; print("W14: the study's sealed sheet names Hauert and Doebeli, 2004")
json.dump(out, open("mine.json", "w"), indent=1, ensure_ascii=False)
