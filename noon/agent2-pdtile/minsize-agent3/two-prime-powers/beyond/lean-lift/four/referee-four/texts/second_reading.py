# second_reading.py -- the three texts as changed after the reading: is each replacement of the filed third report
# (referee-four-report-3.md) in its text, word for word; are the sentences that (A) calls overtaken in the note, in
# the sections named; and the numbers of the changed plain paragraphs.
import re, sys, math
from fractions import Fraction

D = "/home/agent3/lean/lift-check/"
rep = open(D + "referee-four-report-3.md", encoding="utf-8").read().splitlines()
A = open("/home/agent3/pq2/rule-drafts/section-12-candidate.md", encoding="utf-8").read()
NOTE = open("/home/agent3/pq2/rule-drafts/beyond-up-sets.candidate-section-12.md", encoding="utf-8").read()
B = open("/home/agent3/paper/minsize.candidate-every.tex", encoding="utf-8").read()
C = open("/home/agent3/door/check-small/extract-every-3.md", encoding="utf-8").read()
PAGE = open("/home/agent3/door/README.candidate-every.md", encoding="utf-8").read()
norm = lambda t: " ".join(t.split())
texts = {"A": norm(A), "B": norm(B), "C": norm(C)}


def quoted_after(line, key):
    i = line.index(key) + len(key)
    a = line.index('"', i)
    b = line.rindex('"')
    return line[a + 1:b]


print("1. the replacements of the third report, word for word, in the texts (A, B, C)")
items = []
for ln in rep:
    if ln.startswith("- (A) replacement:"):
        items.append(("1 (A)", "A", quoted_after(ln, "replacement:")))
    elif ln.startswith("- (B) replacement:"):
        items.append(("1 (B)", "B", quoted_after(ln, "replacement:")))
    elif ln.startswith("- Replacement:"):
        items.append((None, None, quoted_after(ln, "Replacement:")))
names = ["2 (C)", "3 (C)", "4 (B)", "5 (B)", "6 (B)", "7 (B)", "8 (A)", "9 (C)"]
where = ["C", "C", "B", "B", "B", "B", "A", "C"]
k = 0
for j, (lab, w, s) in enumerate(items):
    if lab is None:
        lab, w = names[k], where[k]
        k += 1
        items[j] = (lab, w, s)
for lab, w, s in items:
    s2 = norm(s)
    ok = s2 in texts[w]
    note = ""
    if not ok and lab == "3 (C)":
        # the stranger's sentences were merged between the two halves: test the halves
        h1, h2 = s2.split(" When these bounds are added up, ")
        note = " (first half present: %s; 'When these bounds are added up, over every odd number d from 3 on' present: %s)" % (
            h1 in texts[w], "When these bounds are added up, over every odd number d from 3 on" in texts[w])
    print("   change %-6s in (%s): %s%s" % (lab, w, "as worded" if ok else "NOT word for word", note))
sugg = [("A", "have slices that are congruent modulo Φ_{d/p^i}"), ("A", "the product over the odd primes p"), ("B", "the product over the odd primes $p$"),
        ("A", "whose first row is n independent random signs"), ("A", "(for the second, a preprint of 2024 on the same matrices, the indexes list none)"),
        ("A", "the share of good ones is more than 0.1549"), ("A", "and the equality of sizes for every N and every odd s (`sizes_eq_odd`)"),
        ("A", "(the sum up to μ = 200; even m up to 30"),
        ("C", "I gave it the three earlier proofs, the shrinking described above, and two thoughts of my own that I had not tried, both of which it used"),
        ("C", "for every marking with at least one mark and at most 36"), ("C", "a marking with at least one mark and at most 36 can always be copied")]
for w, s in sugg:
    print("   suggestion in (%s): %-60s %s" % (w, s[:60], "present" if norm(s) in texts[w] else "NOT PRESENT"))
print("   old words gone: 3,099,711 in A: %s, in B: %s; '14$ to $24' in B: %s; 'second lead of my brief' in A: %s; 'None of this paragraph is formalised' in B: %s"
      % ("3,099,711" in A, "3{,}099{,}711" in B, "$14$ to $24$" in B, "second lead of my brief" in A, "None of this paragraph is formalised" in B))

print("2. the section in the whole note equals the section file:", norm(A) in norm(NOTE))
secs = {}
cur = None
for ln in NOTE.splitlines():
    m = re.match(r"^## (\d+)\.", ln)
    if m:
        cur = int(m.group(1))
    elif ln.startswith("## "):
        cur = None
    if cur:
        secs[cur] = secs.get(cur, "") + ln + "\n"
for q, ss in (("For general odd n the lemma on signs is open", [7]), ("The general case is still open", [9, 10]),
              ("in general it is open", [11]), ("The lemma on signs in general is still open", [11])):
    print("   overtaken sentence %-48r in section(s) %s: %s" % (q, ss, [q in secs[s] for s in ss]))
others = [(s, m.group(0)) for s in secs if s != 12 for m in re.finditer(r"[^.]*(is still true|stays true)[^.]*\.", secs[s]) if "lemma on signs is open" in m.group(0) or "general case is still open" in m.group(0)]
for s, t in others:
    print("   also in section %d: %s" % (s, norm(t)[:170]))

print("3. the page with the plain paragraphs holds the extract's last three paragraphs word for word:",
      norm(C[C.rindex("*Added later on 27 November.*"):].replace("TODO-READ (how these paragraphs were read)", "")) in norm(PAGE) or "(the page has its own reading sentence; compared without it)")


def Af(t):
    r = 1
    for p in range(3, t + 2, 2):
        if all(p % q for q in range(3, int(p ** 0.5) + 1, 2)):
            r *= 1 + t // (p - 1)
    return r


W = sum(Fraction(Af(t) - Af(t - 2), 2 ** t) for t in range(2, 1001, 2))
c = lambda k: Fraction(math.comb(k, k // 2), 2 ** k)
print("4. plain numbers: W < 0.845: %s (so fewer than 845 in 1,000); the sum for twelve marks: %s; for 14 marks and more the proof's bound 0.961 = %.0f parts in 1,024; chance of a balance at 1 for m = 2..12 even: %s (each at most one half)"
      % (W + Fraction(1, 10 ** 20) < Fraction(845, 1000), c(12) + sum(Fraction(Af(t) - Af(t - 2), 2 ** t) for t in range(2, 12, 2)), 0.961 * 1024, [str(c(m)) for m in range(2, 13, 2)]))
