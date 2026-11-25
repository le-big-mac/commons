"""The second ruler: lag.c against lag-plain.c (the same program with every shortcut taken out) on boards too large for slow.py.
Both start from no opening at all, so no symmetry is used either.   usage: python -I ruler2.py > ruler2.out"""
import subprocess, time
def run(prog, args, limit):
    try: out = subprocess.run([prog] + [str(a) for a in args] + ["-q"], input="\n", capture_output=True, text=True, timeout=limit).stdout
    except subprocess.TimeoutExpired: return None
    return "yes" if out.startswith("yes") else "no"
agree = total = slow = 0
for (n, k, Qmax) in ((3, 3, 5), (2, 5, 5), (2, 6, 5), (3, 4, 4), (4, 3, 4), (3, 5, 4), (4, 4, 4)):
    for mode in "KW":
        for d in range(0, 4):
            line = []
            for Q in range(1, Qmax + 1):
                a = run("./lag-plain", [n, k, d, Q, mode], 90)
                if a is None: slow += 1; line.append(f"Q={Q} plain too slow"); continue
                b = run("./lag-final", [n, k, d, Q, mode], 600); total += 1; agree += a == b; line.append(f"Q={Q} {a}/{b}" + ("" if a == b else " DIFFER"))
            print(f"{n} pegs {k} colours ({k ** n} codes), {mode}, lag {d}: " + "  ".join(line), flush=True)
print(f"\n{agree} of {total} cases agree (lag-plain / lag); {slow} cases left out because the plain program took more than 90 seconds")
