from math import comb
runs = {2: range(1, 41), 4: range(5, 23), 6: range(5, 25), 12: range(9, 12)}
tot = 0
for n, ms in runs.items():
    s = sum(comb(m - 1 + n - 1, n - 1) for m in ms)
    print("clock of", n, "hours, marks", ms[0], "to", ms[-1], ":", s, "markings")
    tot += s
print("total", tot)
