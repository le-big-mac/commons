"""Replay a strategy printed by lag.c against every code, with a feedback function written here. Nothing of lag.c's search is used.
usage: python -I verify.py n k d Q mode strategy.out
A strategy line is "S t answers:guess": at guess number t, having seen those answers (to guesses 1 .. t-1-d, "-" if none), send that guess."""
import sys, itertools
n, k, d, Q, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
book = {}
for line in open(sys.argv[6]):
    if line.startswith("S "):
        _, t, rest = line.split(); hist, guess = rest.split(":"); key = (int(t), "" if hist == "-" else hist)
        assert key not in book or book[key] == guess, f"two guesses for {key}"; book[key] = guess
def answer(g, s):
    b = sum(x == y for x, y in zip(g, s)); return f"{b}{sum(min(g.count(c), s.count(c)) for c in set(g)) - b}"
codes = ["".join(p) for p in itertools.product("123456"[:k], repeat=n)]; seen = {}; longest = 0; lost = []; used = set()
for s in codes:
    sent = []
    for t in range(1, Q + 1):
        known = ",".join(answer(g, s) for g in sent[:max(0, t - 1 - d)])
        if f"{n}0" in known.split(",") and mode == "W": break            # the codebreaker has been told the code was sent
        if (t, known) not in book: break                                 # the strategy needs no more guesses here
        used.add((t, known)); sent.append(book[(t, known)])
    longest = max(longest, len(sent))
    if mode == "W":
        if s not in sent: lost.append(s)
    else:
        sig = (tuple(sent), tuple(answer(g, s) for g in sent))           # everything the codebreaker ends up knowing
        if sig in seen: lost.append((s, seen[sig]))
        seen[sig] = s
print(f"{n} pegs, {k} colours, lag {d}, {Q} guesses, question {mode}: {len(book)} lines in the strategy, {len(used)} used; {len(codes)} codes replayed; most guesses sent {longest}; "
      + ("every code " + ("is sent" if mode == "W" else "is told apart from every other") if not lost else f"FAILS for {len(lost)}: {lost[:5]}"))
sys.exit(1 if lost or longest > Q else 0)
