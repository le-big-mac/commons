# Referee, after reading: (a) the table of W from the four numbers, (b) my own replay of Noon's scheme files under the lag rule,
# (c) the "117 states of knowledge" sentence, (d) the Brier line.
import itertools, sys
from collections import Counter, defaultdict
N = 1296; m = {0: 1296, 1: 1282, 2: 1177, 3: 703, 4: 24, 5: 0}     # my own values (blind.out)
early = {0: 5, 1: 7, 2: 8, 3: 9}                                   # first sheet, not rechecked here
def W(d):
    if d < 4: return early[d]
    return min([N] + [d + 1 + j for j in m if j <= d + 1 and m[j] <= d + 1 - j])
runs = []; d = 0
while d <= 1400:
    off = W(d) - d if W(d) < N else None; e = d
    while e < 1400 and ((W(e + 1) - (e + 1) if W(e + 1) < N else None) == off): e += 1
    runs.append((d, e, off)); d = e + 1
print("W by lag from m = 1282, 1177, 703, 24, 0:", runs)
print("lags where W does not rise:", [d for d in range(1, 1300) if W(d) == W(d - 1)][:8], " W(1293), W(1294), W(1295) =", W(1293), W(1294), W(1295))
print("W(5) =", W(5), " W(26), W(27) =", W(26), W(27), " W(704), W(705) =", W(704), W(705), " W(1177), W(1178) =", W(1177), W(1178), " W(1281), W(1282) =", W(1281), W(1282))
codes = ["".join(p) for p in itertools.product("123456", repeat=4)]
def ans(g, s):
    b = sum(x == y for x, y in zip(g, s)); cg, cs = Counter(g), Counter(s)
    return "%d%d" % (b, sum(min(cg[c], cs[c]) for c in "123456") - b)
for j, d in ((5, 4), (4, 27), (3, 705), (2, 1178), (1, 1282)):
    book = {}
    for line in open(f"/home/agent2/post/out/scheme-j{j}-d{d}.out"):
        if line.startswith("S "):
            _, t, rest = line.split(); h, g = rest.split(":"); book[(int(t), () if h == "-" else tuple(h.split(",")))] = g
    T = d + 1 + j; lost = 0; nostate = 0; qs = [book[(t, ())] for t in range(1, j + 1)]; latest = 0
    row = {q: {s: ans(q, s) for s in codes} for q in set(book.values())}
    for s in codes:
        sent = []
        for t in range(1, T + 1):
            known = tuple(row[g][s] for g in sent[:max(0, t - 1 - d)])     # the lag rule: answers to letters 1 .. t-1-d only
            if (t, known) not in book: nostate += 1; break                 # no letter for this state (only legitimate if the code is already sent)
            sent.append(book[(t, known)])
        if s not in sent: lost += 1
        else: latest = max(latest, sent.index(s) + 1)
    print(f"scheme j={j} lag {d}: questions {' '.join(qs)}; {T} letters; codes never sent: {lost}; codes for which the book ran out of letters: {nostate}; latest letter at which a code is first sent: {latest}")
# two questions: states of knowledge and names
for qs in (("1234", "6632"), ("1234", "1355")):
    rest = [c for c in codes if c not in qs]
    l1 = defaultdict(list); l2 = defaultdict(list)
    for c in rest: l1[ans(qs[0], c)].append(c); l2[(ans(qs[0], c), ans(qs[1], c))].append(c)
    print(qs, "level-1 classes", len(l1), "level-2 classes", len(l2), "together", len(l1) + len(l2), "codes named", len(rest) - 1177,
          "level-1 classes all of whose sub-classes are single codes:", sum(all(len(v) == 1 for k, v in l2.items() if k[0] == a) for a in l1))
odds = [0.45, 0.75, 0.70, 0.70, 0.90, 0.80]; held = [0, 0, 1, 0, 1, 1]
print("Brier", sum((o - h) ** 2 for o, h in zip(odds, held)) / 6, "mean odds", sum(odds) / 6)
