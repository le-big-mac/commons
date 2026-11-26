"""A stranger's check of the clock example, using only the page's own words.

My reading of the definition on the page:
  - the clock has M hours 0..M-1; a marking is a list of hours, repeats allowed;
  - for a divisor d of M, the mark at hour h puts one unit weight on a circle
    at h/d of a full turn from the start;
  - the marks "balance at d" if those weights have their centre of gravity at
    the centre, i.e. if the unit vectors add up to zero.

Part 1: the two examples on the 12-hour clock, by floating point and exactly.
Part 2: the least number of marks for every set of divisors, by trying every
        marking up to a given size, set beside my reading of "The answer".

Usage: python check_clock.py            (12-hour clock, markings up to 12 marks)
       python check_clock.py M p q n S  (another clock, markings up to S marks)
"""
import cmath
import math
import sys
from itertools import combinations_with_replacement

TOL = 1e-9


def divisors(M):
    return [d for d in range(1, M + 1) if M % d == 0]


def total(marks, d):
    """Sum of the unit weights' positions, one step of 1/d turn per hour."""
    return sum(cmath.exp(2j * math.pi * h / d) for h in marks)


def balances(marks, d):
    return abs(total(marks, d)) < TOL


def where(marks, M):
    return [d for d in divisors(M) if balances(marks, d)]


# --- exact arithmetic for the 12-hour clock: whole-number combinations of
# 1, z, z^2, z^3 where z is one twelfth of a turn, and z^4 = z^2 - 1.
def zpow12(j):
    v = (1, 0, 0, 0)
    for _ in range(j % 12):
        a0, a1, a2, a3 = v
        v = (-a3, a0, a1 + a3, a2)
    return v


def balances_exact12(marks, d):
    s = [0, 0, 0, 0]
    for h in marks:
        v = zpow12((12 // d) * h)
        s = [x + y for x, y in zip(s, v)]
    return s == [0, 0, 0, 0]


def part1():
    M = 12
    print("Part 1. The 12-hour clock, divisors", divisors(M))
    for marks in ([0, 6], [0, 6, 1, 5, 9], [1, 5, 9]):
        print("  marks", marks)
        for d in divisors(M):
            degs = [round((360.0 * h / d) % 360, 6) for h in marks]
            t = total(marks, d)
            ex = balances_exact12(marks, d)
            assert ex == balances(marks, d)
            print(f"    d={d:2d}: weights at {degs} degrees; sum = "
                  f"{t.real:+.3f}{t.imag:+.3f}i; balance: {ex}")
        print("    balances at:", where(marks, M))
    # is five really the least for "12 and nowhere else"? every marking, no shortcut
    for target, label in (([12], "12 only"), ([4, 12], "4 and 12 only")):
        for size in range(1, 7):
            hits = [m for m in combinations_with_replacement(range(M), size)
                    if where(m, M) == target]
            if hits:
                exact_ok = all(
                    [d for d in divisors(M) if balances_exact12(m, d)] == target
                    for m in hits)
                print(f"  least number for balance at {label}: {size} "
                      f"({len(hits)} markings of that size, e.g. {hits[0]}; "
                      f"exact arithmetic agrees: {exact_ok})")
                break
            else:
                print(f"    no marking of {size} marks balances at {label}")


def my_reading(pattern, p, q, n):
    """The numbers the page's section 'The answer' gives, as I read it.

    Guesses I had to make: the powers are p^1..p^n (not 1); 'first' means the
    smallest; 'beyond it' means larger; 'none' means k' = 0.
    Returns one number (first case) or the two candidates (second case).
    """
    powers = [p ** a for a in range(1, n + 1)]
    e = sum(1 for P in powers if P in pattern)
    short = [P for P in powers if P * q in pattern and P not in pattern]
    if q not in pattern:
        k = len(short)
        return (p ** e,) if k == 0 else (p ** e * (p ** k + q),)
    first = next((P for P in powers if P * q not in pattern), None)
    kk = 0 if first is None else sum(1 for P in short if P > first)
    return (q * p ** e * p ** kk, q * p ** e * (p ** kk + 1))


def part2(M, p, q, n, S):
    assert M == p ** n * q
    divs = [d for d in divisors(M) if d > 1]
    w = {d: [cmath.exp(2j * math.pi * h / d) for h in range(M)] for d in divs}
    least = {}
    example = {}

    # Every marking that contains hour 0 (turning the clock moves any marking
    # to one that does, and turns every weight at d by the same angle, so
    # balance is unchanged). Part 1 did the two headline cases with no shortcut.
    def grow(marks, sums, lowest):
        pat = tuple(d for d, s in zip(divs, sums) if abs(s) < TOL)
        if pat not in least or len(marks) < least[pat]:
            least[pat] = len(marks)
            example[pat] = marks
        if len(marks) == depth:
            return
        for h in range(lowest, M):
            grow(marks + (h,), [s + w[d][h] for d, s in zip(divs, sums)], h)

    depth = S
    grow((0,), [w[d][0] for d in divs], 0)
    print(f"\nPart 2. Clock of {M} = {p}^{n}*{q} hours; every marking of up to "
          f"{S} marks tried.")
    print("  pattern (divisors of balance) | least found | my reading of the page"
          " | example")
    npat = 0
    agree = 0
    undecided = 0
    from itertools import combinations
    for r in range(len(divs) + 1):
        for pat in combinations(divs, r):
            npat += 1
            pred = my_reading(set(pat), p, q, n)
            found = least.get(pat)
            if found is None:
                undecided += 1
                verdict = f"none with <= {S} marks"
                ok = all(x > S for x in pred) or (len(pred) == 2 and pred[1] > S)
                note = "consistent" if ok else "DISAGREES"
            else:
                verdict = str(found)
                ok = found in pred
                note = "agrees" if ok else "DISAGREES"
                agree += ok
            ptxt = str(pred[0]) if len(pred) == 1 else f"{pred[0]} or {pred[1]}"
            print(f"  {str(list(pat)):22s} | {verdict:22s} | {ptxt:10s} | "
                  f"{note:10s} | {example.get(pat, '')}")
    print(f"  {npat} patterns; {agree} settled and in agreement with my reading; "
          f"{undecided} not reached with <= {S} marks.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        part1()
        part2(12, 2, 3, 2, 12)
    else:
        M, p, q, n, S = map(int, sys.argv[1:6])
        part2(M, p, q, n, S)
