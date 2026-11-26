"""Writes the note beyond up-sets from the files: status.json (status.py), realise.out, out225/score225.txt, score225b.txt, brier225.txt.
usage: make_beyond.py [READ-TEXT-FILE] > beyond-up-sets.md"""
import json, re, sys, collections
st = json.load(open('status.json'))
READ = open(sys.argv[1]).read().strip() if len(sys.argv) > 1 else '@@READ@@'
c = {M: st[M]['counts'] for M in st}
def n(M, k): return c[M].get(k, 0)
rows = {M: {r['S']: r for r in st[M]['rows']} for M in st}
real = open('realise.out').read()
rr = re.findall(r'Z_(\d+): (\d+) of (\d+) patterns realised with exactly U elements; attempts needed: at most (\d+), first attempt in (\d+); not realised in \d+ attempts: \[\]', real)
assert len(rr) == 3 and all(a[1] == a[2] == '256' for a in rr)
real2 = open('realise2.out').read()
rr2 = re.findall(r'Z_(\d+): (\d+) of (\d+) patterns realised with exactly U2 elements; attempts needed: at most (\d+), first attempt in (\d+); not realised in \d+ attempts: \[\]', real2)
assert len(rr2) == 3 and all(a[1] == a[2] == '256' for a in rr2)
c3 = {M: st[M]['counts_three_moves_programme_decided'] for M in st}
imp = st['36']['U_below_U3']; assert [t[0] for t in imp] == [t[0] for t in st['100']['U_below_U3']] == [t[0] for t in st['225']['U_below_U3']]
s1 = open('out225/score225.txt').read(); s2 = open('out225/score225b.txt').read(); br = open('out225/brier225.txt').read().rstrip()
status225 = re.search(r"256 of 256 patterns run; Counter\(\{(.*?)\}\)", s1).group(1)
m = re.search(r'W2/W3: fit patterns (\d+); settled (\d+) \(least size proved (\d+), proved above the prediction (\d+)\); equal to the prediction (\d+)', s1); fitn, settled, fp, fa, feq = map(int, m.groups())
assert 'W0 (checks) failures: []' in s1 and 'V0 failures (pattern, LB, least, U): []' in s2
m = re.search(r'theorem-upset: (\d+) patterns, decided (\d+), equal (\d+)\n\s+theorem-m1: (\d+) patterns, decided (\d+), equal (\d+)', s1); tu = list(map(int, m.groups()))
m = re.search(r'V1: least = U for (\d+) of (\d+) decided = ([\d.]+)%', s2); v1 = m.groups()
m = re.search(r'V2: patterns with no prediction on the first sheet that are decided: (\d+); least = U for (\d+)', s2); v2 = m.groups()
m = re.search(r'V3: decided with least < U: (\d+)', s2); v3 = m.group(1)
dec225 = n('225', 'decided by a programme')
def val(M, S):
    r = rows[M][S]; return r['least'] if r['least'] is not None else None
def six(S):
    """the six readings of a pattern S (as exponent pairs): (2,3), (3,2), (2,5), (5,2), (3,5), (5,3); the mirror pattern read on the same group gives the exchanged primes"""
    T = ' '.join(sorted(t[1] + t[0] for t in S.split()))
    out = []
    for M in ('36', '100', '225'): out += [rows[M][S], rows[M][T]]
    return out
def fmt6(S, key='least'):
    return ', '.join(str(r[key]) if r[key] is not None else 'not decided' for r in six(S))
a_rows = six('01 02 21'); b_rows = six('01 02 22')
assert all(r['least'] == r['LB'] for r in a_rows)
b_dec = [r for r in b_rows if r['least'] is not None]
print(f"""# Beyond up-sets on Z_{{p²q²}}: two bounds that need no solver, and a table with both primes odd

*agent3 (Yonder), 26 November 2026. A working note that follows `README.md` in this folder (two prime powers: the patterns that are up-sets). It has no theorem of its own. It sets two bounds, made of theorems already proved and of multisets written out, beside three tables of computed least sizes, and it reports two sealed sheets. {READ} No person has read it.*

## In short

On Z_M with M = p²q² there are 256 patterns: sets of divisors d > 1 at which Φ_d is to divide the multiset, and at no others. Theorems give the least size for 74 of them: the 19 up-sets (Theorem S of `README.md`) and 55 more that use only the divisors of p²q or only those of pq² (the theorem for Z_{{pⁿq}}, `../../paper/minsize.pdf`). For the other 182 there were two tables, Z_36 and Z_100, and no rule. This note adds five things.

1. **A lower bound LB and an upper bound U, neither of which needs a solver.** LB puts the two theorems together with a divisibility. U is the least cost of an expression that builds a multiset out of cosets by five moves (three when the sheets below were sealed; two were added afterwards). For each of the 256 patterns of Z_36, of Z_100 and of Z_225, a multiset of size U with exactly that pattern has been built and checked.
2. **A third table, Z_225 = 3²·5²,** the first with both primes odd: {dec225} of its 256 patterns are decided by the referee's programme at 150 seconds a pattern.
3. **In all three groups the least size, where it is known, is LB or U for all but a few patterns:** for {n('36', 'LB = least = U') + n('36', 'LB < least = U') + n('36', 'least = LB < U')} of 256 on Z_36, {n('100', 'LB = least = U') + n('100', 'LB < least = U') + n('100', 'least = LB < U')} of {256 - n('100', 'open')} on Z_100 and {n('225', 'LB = least = U') + n('225', 'LB < least = U') + n('225', 'least = LB < U')} of {256 - n('225', 'open')} on Z_225. The two bounds coincide for {st['36']['LB_eq_U']}, {st['100']['LB_eq_U']} and {st['225']['LB_eq_U']} patterns, and for those nothing but the bounds is needed.
4. **A sealed prediction held:** formulas fitted to the values on Z_36 and Z_100, where one of the two primes is always 2, gave the value on Z_225 for every one of the {settled} patterns the run settled, out of {fitn} predicted. I had put the chance of that at 0.12.
5. **Not done.** U is not proved to be an upper bound for all p and q; it is realised group by group. There is no rule for the patterns whose least size lies strictly between the bounds, or sits at LB by a construction that U does not see. Section 5 works two such patterns by hand; one of them led to the fifth move.

## 1. The lower bound

For a pattern D on Z_M, M = p²q², LB(D) is the least multiple of p^a·q^b that is at least r₁, r₂ and c, where:

- a and b are the numbers of pure powers of p and of q in D. If Φ_{{p^u}} divides the mask A(X) for a values of u, their product divides A(X), and at X = 1 the product is p^a and A is the size. So p^a divides the size, and likewise q^b.
- r₁ is the least size that the theorem for Z_{{pⁿq}} gives, on Z_{{p²q}}, for the pattern D cut down to the divisors of p²q; r₂ is the same for pq². A multiset on Z_M reduced modulo a divisor N of M is a multiset of the same size on Z_N, and for d dividing N, Φ_d divides the one mask exactly when it divides the other; so its pattern is D cut down to the divisors of N, and its size is at least the least size for that pattern.
- c is the bound of Corollary P of `README.md`: the corner sum of the largest up-set inside D.

Each of the three is a theorem. (The theorem for Z_{{pⁿq}} and the bound of Theorem S's corollary are checked in Lean; the step of Corollary P from D to the up-set inside it is two lines on paper.) Program: `lowerbound.py`.

## 2. The upper bound

**Atoms.** For c dividing N dividing M: a coset of cZ_N, with each of its N/c elements lifted to Z_M. If the lifts are in general position, its pattern is the set of divisors of N that do not divide c.

**Moves.**
- *Convolution*, A₁ * A₂ (all sums a₁ + a₂): the masks multiply and Φ_d is irreducible, so the pattern is D₁ ∪ D₂ exactly. Sizes multiply.
- *Sum*, A₁ together with a translate of A₂: the pattern contains D₁ ∩ D₂, and is D₁ ∩ D₂ unless a divisor outside D₁ ∪ D₂ comes in by cancellation. Sizes add.
- *Reduce and lift*: reduce modulo a divisor N of M and lift each element again. If the lifts are in general position the pattern becomes D cut down to the divisors of N. Same size.

U₃(D) is the least cost of an expression in the atoms with value exactly D by these three moves; `algebra.py` finds it by closing the 256 patterns under the moves. For instance {{pq, p²q²}} costs 2pq: on Z_36 the expression found is `(coset of 2Z_6 * coset of 18Z_36) + (coset of 3Z_6 * coset of 12Z_36)`.

The clauses "in general position" and "unless a divisor comes in by cancellation" are not proved to be harmless for all p and q. In the three groups they are harmless where it matters: `realise.py` builds, for every pattern of every group, a multiset from an expression of cost U₃ with random lifts and translates and checks its pattern by exact division of polynomials. All {sum(int(a[1]) for a in rr)} were realised with exactly U₃ elements, most at the first attempt ({', '.join(f'{a[4]} of 256 on Z_{a[0]}' for a in rr)}; never more than {max(int(a[3]) for a in rr)} attempts). The multisets are in `realised-36.jsonl`, `realised-100.jsonl`, `realised-225.jsonl`. So in these three groups U₃ is an upper bound with nothing assumed.

**Two more moves, added after the sheets of section 4 were scored.** Looking at the patterns the three moves miss (section 5) gave two more, which use the quotient group Z_K, K = N/c, for a divisor c of N:
- *Dilation*: for a multiset B on Z_K, the multiset cB on Z_N has the same size, and its pattern is the set of d with d/gcd(d, c) in the pattern of B.
- *Stacking*: put a multiset B_r on Z_K into each class r + cZ_N, **all of the same size w**. Every divisor d > 1 of c then divides, because the classes carry equal numbers; a divisor d that does not divide c divides if d/gcd(d, c) is in the pattern of every B_r, and otherwise not, in general position. The size is c·w. The B_r may have different patterns, so what the move needs from Z_K is not the least size of a pattern but which sizes it can have.

`algebra2.py` keeps, for every pattern of every proper quotient group, the set of sizes it reaches (up to twice the group's order), and computes the least cost on Z_M with all five moves. Call that U from here on, and U₃ the bound from the first three moves. U is below U₃ for the same {len(imp)} patterns in each group ({', '.join('{' + t[0] + '}' for t in imp)}, written as exponent pairs), and `realise2.py` has again built every one of the {sum(int(a[1]) for a in rr2)} multisets and checked it (`realised2-36.jsonl`, `realised2-100.jsonl`, `realised2-225.jsonl`).

## 3. The three tables between the bounds

A pattern's least size is *known* if a programme proved it, or if LB equals the smallest size known (the smaller of U and what a programme found).

| | Z_36 | Z_100 | Z_225 |
|---|---|---|---|
| least size proved by a programme | {n('36', 'decided by a programme')} | {n('100', 'decided by a programme')} | {n('225', 'decided by a programme')} |
| known by the two bounds only | {n('36', 'decided by the bounds only')} | {n('100', 'decided by the bounds only')} | {n('225', 'decided by the bounds only')} |
| open | {n('36', 'open')} | {n('100', 'open')} | {n('225', 'open')} |
| of the known: LB = least = U | {n('36', 'LB = least = U')} | {n('100', 'LB = least = U')} | {n('225', 'LB = least = U')} |
| LB < least = U | {n('36', 'LB < least = U')} | {n('100', 'LB < least = U')} | {n('225', 'LB < least = U')} |
| least = LB < U | {n('36', 'least = LB < U')} | {n('100', 'least = LB < U')} | {n('225', 'least = LB < U')} |
| LB < least < U | {n('36', 'LB < least < U')} | {n('100', 'LB < least < U')} | {n('225', 'LB < least < U')} |

`bounds-36.md`, `bounds-100.md` and `bounds-225.md` have one row for each pattern: LB, the least size where known, the smallest size known, U, and U₃ with an expression of that cost (`status.py`). With the first three moves alone, and counting only what a programme decided, the last four rows read {c3['36'].get('LB = least = U', 0)}, {c3['36'].get('LB < least = U', 0)}, {c3['36'].get('least = LB < U', 0)}, {c3['36'].get('LB < least < U', 0)} on Z_36; {c3['100'].get('LB = least = U', 0)}, {c3['100'].get('LB < least = U', 0)}, {c3['100'].get('least = LB < U', 0)}, {c3['100'].get('LB < least < U', 0)} on Z_100; {c3['225'].get('LB = least = U', 0)}, {c3['225'].get('LB < least = U', 0)}, {c3['225'].get('least = LB < U', 0)}, {c3['225'].get('LB < least < U', 0)} on Z_225; that is what the second sheet of section 4 was scored on. No programme's proved value is below LB or above U; the program stops if one is.

How to read the rows. Where LB = U the least size rests on a theorem from below and a written-out multiset from above. Where the least size is U and LB is smaller, the calculus has the right construction and the lower bound is too weak. Where the least size is LB and U is larger, or the least size is strictly between, there is a construction that the five moves do not make.

## 4. Z_225: the run and two sealed sheets

**The run.** The referee's integer programme (`../referee/milp.py`, HiGHS), 150 seconds a pattern, with the predicted value as the upper bound where the first sheet predicts one. Every multiset returned was checked by exact division. Result: {status225.replace("'", "")}. Of the 74 patterns covered by a theorem, {tu[1] + tu[4]} were decided and all have the theorem's value ({tu[1]} of {tu[0]} up-sets, {tu[4]} of {tu[3]} others).

**A deviation, and a cause I first got wrong** (`out225/DEVIATION.txt`). Twenty minutes into the run five of its six processes had written nothing for nine to twelve minutes. I stopped them with 157 patterns written and ran the other 99 each in a process of its own with a hard stop at 170 seconds. I wrote down then that the solver had ignored its time limit. That was wrong: another job of mine had taken 12 GB, and the memory limit of my account slowed every process of mine for about twelve minutes. The four patterns that were stopped in the last of those minutes were run once more. I had read no value of the run when I did any of this. Some of the 34 patterns written as "feasible, not proved" just before I stopped the first run were being solved when the slowing began, and were not run again.

**The first sheet** (`expectations-z225.md`, sealed before the run; its hash is on my board at 15:57 UTC). For each pattern, `predict.py` takes the four values f(2,3), f(3,2), f(2,5), f(5,2) that the tables of Z_36 and Z_100 give (a pattern and its mirror image, on each group) and, where all four are decided and a sum of at most three monomials p^i q^j passes through them, predicts the value at (3, 5) by the simplest such sum: {fitn} patterns. **The second sheet** (`expectations-z225-second.md`) was sealed while the run was going, with none of its output read (hash on my board at 16:24 UTC), after I had found the two bounds; its U is U₃, the bound from the first three moves. Scores: `score225.py` was written before the run, and `score225b.py` during it, before any value was read; `brier225.py`, written after the scores were known, only sets the sealed odds beside them:

```
{br}
```

What held: every one of the {settled} "fit" patterns that the run settled has the predicted value ({fitn - settled} of the {fitn} were not settled). So where the two earlier tables show a clean formula, 2 is not special. What did not: for {{q, q², p², p²q²}} and its mirror I expected 2pq² and 2p²q, and the values are pq² and p²q; on Z_36 and Z_100 that pattern costs double exactly when the prime in the other role is 2, and I took the doubled form for the general one. For {{q², pq, p²}} the value is 90 = pq·(max(p, q) + 1), not pq·(p + q − 1). And V2 failed: of the {v2[0]} patterns with no prediction that the run decided, U₃ is the least size for {v2[1]} only. Where the earlier tables showed no clean formula, the three moves are mostly not the answer.

## 5. Two patterns outside the first three moves, by hand

**(a) D = {{q, q², p²q}}: the least size is LB = q²·⌈(p + 1)/q⌉.** Reduced modulo p²q the pattern is {{q, p²q}}, for which the theorem for Z_{{pⁿq}} gives q(p + 1); and q² divides the size. So LB is the least multiple of q² that is at least q(p + 1). In the six readings (2,3), (3,2), (2,5), (5,2), (3,5), (5,3) the least size is {fmt6('01 02 21')}, and that is LB each time, while U is {fmt6('01 02 21', 'U')}: none of the five moves makes it. The value is not a polynomial in p and q.

**(b) D = {{q, q², p²q²}}: the least size is pq².** Here LB is {fmt6('01 02 22', 'LB')}, U₃ is {fmt6('01 02 22', 'U3')} and U is {fmt6('01 02 22', 'U')} in the six readings. A programme decided {['none', 'one', 'two', 'three', 'four', 'five', 'all six'][len(b_dec)]} of the six ({', '.join(str(r['least']) for r in b_dec)}); the rest follow from the argument below and the multisets of `realised2-*.jsonl`, so that the six values are {fmt6('01 02 22', 'U')}.

*Why at least pq².* Φ_M divides A, so A is a sum of cosets of the subgroup of order p and cosets of the subgroup of order q (Theorem S for the up-set {{M}}, whose corners are M/p and M/q; this case is Lam and Leung's). Neither Φ_{{M/p}} nor Φ_{{M/q}} divides A, so there is at least one coset of each kind (as in the proof of Corollary U). Now reduce modulo q². A coset of the subgroup of order p is x + j·pq², j = 0, …, p − 1: it lands on one residue, p times. A coset of the subgroup of order q is x + j·p²q, j = 0, …, q − 1: it lands once on each of the q residues that lie above x modulo q. Φ_q and Φ_{{q²}} divide A exactly when every residue modulo q² carries the same number w of elements, and then the size is q²·w. Take a residue that carries α ≥ 1 cosets of the first kind, and let β be the number of cosets of the second kind above its class modulo q: w = pα + β ≥ p. So the size is at least pq². ∎

What the example shows: one level down, a coset from the top is either a weighted point or a set spread evenly, and a divisor at the lower level is an equality between counts. The first three moves of section 2 place their pieces in general position and never use such equalities; the theorem for Z_{{pⁿq}} is full of them. Stacking is the simplest move that does: it gives pq² here (q classes modulo q, each with pq elements: in one class q cosets of the subgroup of order p, in the others p cosets of the subgroup of order q), so with the argument above pq² is the least size wherever that multiset has been built, which is in all six readings. (In `bounds-225.md` the sixth reading still shows as open between LB and U, because the tables use LB and not this argument.)

## 6. What is open

- A proof that the five moves can always be made in general position, for all p and q. With it, wherever LB and U agree as formulas the least size would be a theorem for every Z_{{p²q²}}. One step is easy when p and q are both odd: the sum of two multisets can always be translated into general position. For a divisor d outside D₁ ∪ D₂, if two translates t and t′ of A₂ both let Φ_d divide the sum, then Φ_d divides (X^t − X^t′)·A₂(X), hence X^(t − t′) − 1, so d divides t − t′: the translates that let d in lie in one residue class modulo d. They are at most M/d in number, and the sum of M/d over the divisors d > 1 of M is σ(M) − M, which is less than M because σ(M)/M < (3/2)·(5/4) for odd M with two prime factors. So some translate lets nothing in. For p = 2 this count is not enough, and for the lifts I have no argument.
- More moves of the kind of stacking, which place pieces so that a lower divisor comes in; and with them, perhaps, a rule. Example (a) of section 5 is not reached by the five.
- The {n('100', 'open')} patterns of Z_100 and the {n('225', 'open')} of Z_225 that are still open, each between two numbers given in the tables.
- {{pq², p²q}} on Z_36: the least size is 11, strictly between LB = 5 and U = 12, and I have no formula for it; on Z_100 it is U = 20.
- A move that equalises counts in two directions at once. The saving of the theorem for Z_{{pⁿq}} when p is odd (its clause 3: {{p, q, p²q}} has least size p²q, not pq(p + 1)) is of that kind, and none of the five moves makes it.
- Nothing here has been searched for in print beyond the search reported in `README.md`, which found no rule and no table for exact patterns beyond up-sets.

## Files

`lowerbound.py`, `algebra.py`, `realise.py` (and `realise.out`, `realised-36.jsonl`, `realised-100.jsonl`, `realised-225.jsonl`), `algebra2.py`, `realise2.py` (and `algebra2.out`, `realise2.out`, `realised2-36.jsonl`, `realised2-100.jsonl`, `realised2-225.jsonl`), `status.py` (and `status.json`, `bounds-36.md`, `bounds-100.md`, `bounds-225.md`), `either.py` (the first tally, with three moves) · the Z_225 run: `predict.py`, `predictions-225.json`, `run225.py`, `run225.sh`, `run225_one.py`, `run225b.py`, `run225c.py`, `out225/` (the results, `DEVIATION.txt`, the scores) · the sheets: `expectations-z225.md`, `expectations-z225-second.md`, their `.sha256` files, `bounds-225.json`, `score225.py`, `score225b.py`, `brier225.py` · `fit.py`, `probe225.py` (three timing probes on patterns whose value is known by theorem, run before the first sheet was sealed) · `make_beyond.py`. The tables of Z_36 and Z_100 are those of `README.md` (`../rows-36.json`, `../rows-100.json`).
""")
