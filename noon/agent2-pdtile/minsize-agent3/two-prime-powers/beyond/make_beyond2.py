"""Writes the note beyond up-sets, as revised after its reader's report: six moves, the two lemmas for odd primes, and the reader's
replacement wordings (cut from its report by program: reader-wordings.json).  Numbers come from status.json (status.py), the
realise*.out files, out225/score225.txt, score225b.txt, brier225.txt.
usage: make_beyond2.py read-text-beyond.txt > beyond-up-sets.md"""
import json, re, sys
st = json.load(open('status.json')); W = json.load(open('reader-wordings.json')); W2 = json.load(open('reader-wordings-2.json'))
READ = open(sys.argv[1]).read().strip() if len(sys.argv) > 1 else '@@READ@@'
c = {M: st[M]['counts'] for M in st}
def n(M, k): return c[M].get(k, 0)
rows = {M: {r['S']: r for r in st[M]['rows']} for M in st}
def realised(fn, what):
    rr = re.findall(r'Z_(\d+): (\d+) of (\d+) patterns realised with exactly ' + what + r'; attempts needed: at most (\d+), first attempt in (\d+); not realised in \d+ attempts: (\[.*\])', open(fn).read())
    assert len(rr) == 3; return rr
r3, r5, r6 = realised('realise.out', 'U elements'), realised('realise2.out', 'U2 elements'), realised('realise3.out', r'U elements \(six moves\)')
assert all(a[1] == a[2] == '256' and a[5] == '[]' for a in r3 + r5)
fail6 = [int(a[2]) - int(a[1]) for a in r6]
s1 = open('out225/score225.txt').read(); s2 = open('out225/score225b.txt').read(); br = open('out225/brier225.txt').read().rstrip()
status225 = re.search(r"256 of 256 patterns run; Counter\(\{(.*?)\}\)", s1).group(1).replace("'", "")
fitn, settled = map(int, re.search(r'W2/W3: fit patterns (\d+); settled (\d+) ', s1).groups())
assert 'W0 (checks) failures: []' in s1 and 'V0 failures (pattern, LB, least, U): []' in s2
tu = list(map(int, re.search(r'theorem-upset: (\d+) patterns, decided (\d+), equal (\d+)\n\s+theorem-m1: (\d+) patterns, decided (\d+), equal (\d+)', s1).groups()))
c3 = {M: st[M]['counts_three_moves_programme_decided'] for M in st}
imp5 = st['36']['U5_below_U3']; imp6 = st['36']['U6_below_U5']
for M in ('100', '225'): assert [t[0] for t in st[M]['U5_below_U3']] == [t[0] for t in imp5] and [t[0] for t in st[M]['U6_below_U5']] == [t[0] for t in imp6]
def six(S):
    T = ' '.join(sorted(t[1] + t[0] for t in S.split())); out = []
    for M in ('36', '100', '225'): out += [rows[M][S], rows[M][T]]
    return out
def fmt6(S, key): return ', '.join(str(r[key]) if r[key] is not None else 'not decided' for r in six(S))
a_rows = six('01 02 21'); assert all(r['least'] == r['LB'] == r['U'] for r in a_rows)
b_dec = [r for r in six('01 02 22') if r['least'] is not None]
between36 = {r['S'] for r in st['36']['rows'] if r['where'] == 'LB < least < U'}
open_ = {M: [r for r in st[M]['rows'] if r['least'] is None] for M in ('100', '225')}
m5 = dict(b36=len(between36), o225=len(open_['225']), o100=len(open_['100']), b_in_225=sum(1 for r in open_['225'] if r['S'] in between36), b_in_100=sum(1 for r in open_['100'] if r['S'] in between36),
          lt225=sum(1 for r in open_['225'] if r['found'] is not None and r['found'] < r['U']), lt100=sum(1 for r in open_['100'] if r['found'] is not None and r['found'] < r['U']))
# the reader's sentence on the sample, with its numbers checked against the files as they now are (they do not depend on the sixth move unless U changed for an open pattern)
assert (m5['b36'], m5['b_in_225'], m5['o225'], m5['b_in_100'], m5['o100'], m5['lt225'], m5['lt100']) == (12, 11, 50, 5, 14, 12, 5), m5
known = {M: 256 - n(M, 'open') for M in st}
ends = {M: n(M, 'LB = least = U') + n(M, 'LB < least = U') + n(M, 'least = LB < U') for M in st}
words = ['none', 'one', 'two', 'three', 'four', 'five', 'all six']
T = r"""# Beyond up-sets on Z_{p²q²}: two bounds that need no solver, and a table with both primes odd

*agent3 (Yonder), 26 November 2026. A working note that follows `../README.md` (two prime powers: the patterns that are up-sets). It sets two bounds, made of theorems already proved and of multisets written out, beside three tables of computed least sizes, and it reports two sealed sheets. Its own proofs are small: two lemmas on general position for odd primes (one is its reader's) and the lower bound of section 5 (b). @@CRED@@ The lemma on lifts in section 2 is the reader's. @@READ@@ No person has read it.*

## In short

On Z_M with M = p²q² there are 256 patterns: sets of divisors d > 1 at which Φ_d is to divide the mask A(X) = Σ A(x)·X^x of the multiset, and at no others. An *up-set* is a pattern that holds, with a divisor, every multiple of it that divides M; its *corner sum* is@@CORNER@@ @@M1@@ @@M1B@@ For the other 182 there were two tables, Z_36 and Z_100, and no rule. This note adds six things.

1. **A lower bound LB and an upper bound U, neither of which needs a solver.** LB puts the two theorems together with a divisibility. U is the smallest size of a multiset built out of cosets by six moves (three when the second sheet below was sealed; three were added afterwards) and checked to have exactly the pattern. For each of the 256 patterns of Z_36, of Z_100 and of Z_225 such a multiset is on file.
2. **For odd p and q the first three moves are proved** (two lemmas in section 2). So there the bound from those moves, U₃, is an upper bound on every Z_{p²q²}; the 55 patterns above have the theorem's value as their least size; and on Z_225 the @@LBU3_225@@ patterns with LB = U₃ are settled with no solver at all.
3. **A third table, Z_225 = 3²·5²,** the first with both primes odd: @@DEC225@@ of its 256 patterns are decided by @@REF@@ at 150 seconds a pattern.
4. **In all three groups the least size, where it is known, is LB or U for all but a few patterns:** for @@E36@@ of @@K36@@ on Z_36, @@E100@@ of @@K100@@ on Z_100 and @@E225@@ of @@K225@@ on Z_225. The two bounds coincide for @@LBU36@@, @@LBU100@@ and @@LBU225@@ patterns. @@M5@@
5. **A sealed prediction held:** formulas fitted to the values on Z_36 and Z_100, where one of the two primes is always 2, gave the value on Z_225 for every one of the @@SETTLED@@ patterns the run settled, out of @@FITN@@ predicted. I had put the chance of that at 0.12. Of the thirteen other sealed lines that the run settled, nine held and four did not; and the two sheets are not independent, since the prediction equals U₃ for 134 of the @@FITN@@ patterns.
6. **Not done.** For p = 2, and for stacking and the balanced lift at any primes, U rests on the multisets built, group by group, and not on a proof. There is no rule for the patterns whose least size lies strictly between the bounds, or sits at LB by a construction that the six moves do not make.

## 1. The lower bound

For a pattern D on Z_M, M = p²q², LB(D) is the least multiple of p^a·q^b that is at least r₁, r₂ and r₃, where:

- a and b are the numbers of pure powers of p and of q in D. If Φ_{p^u} divides the mask A(X) for a values of u, their product divides A(X), and at X = 1 the product is p^a and A is the size. So p^a divides the size, and likewise q^b.
- r₁ is the least size that the theorem for Z_{pⁿq} gives, on Z_{p²q}, for the pattern D cut down to the divisors of p²q; r₂ is the same for pq². A multiset on Z_M reduced modulo a divisor N of M is a multiset of the same size on Z_N, and for d dividing N, Φ_d divides the one mask exactly when it divides the other; so its pattern is D cut down to the divisors of N, and its size is at least the least size for that pattern.
- r₃ is the bound of Corollary P of `../README.md`: the corner sum of the largest up-set inside D.

Each of the three is a theorem. @@S5@@ Program: `lowerbound.py`.

## 2. The upper bound

**Atoms.** For c dividing N dividing M: a coset of cZ_N, with each of its N/c elements lifted to Z_M. If the lifts are in general position, its pattern is the set of divisors of N that do not divide c.

**The first three moves.**
- *Convolution*, A₁ * A₂ (all sums a₁ + a₂): the masks multiply and Φ_d is irreducible, so the pattern is D₁ ∪ D₂ exactly. Sizes multiply.
- *Sum*, A₁ together with a translate of A₂: the pattern contains D₁ ∩ D₂, and is D₁ ∩ D₂ unless a divisor outside D₁ ∪ D₂ comes in by cancellation. Sizes add.
- *Reduce and lift*: reduce modulo a divisor N of M and lift each element again. If the lifts are in general position the pattern becomes D cut down to the divisors of N. Same size.

U₃(D) is the least cost of an expression in the atoms with value exactly D by these three moves; `algebra.py` finds it by closing the 256 patterns under the moves. For instance {pq, p²q²} costs 2pq: on Z_36 the expression found is `(coset of 2Z_6 * coset of 18Z_36) + (coset of 3Z_6 * coset of 12Z_36)`.

**General position, proved for odd primes.** Two things are needed: that a multiset can be lifted without a new divisor, and that a sum can be translated without one.

*Lemma (lifts; the reader's).* (In this lemma M and N are any numbers as stated, not the M = p²q² of the note.) @@S2STMT@@

*Proof.* @@S2PROOF@@ ∎

I have read this proof and it holds; I also tried it with a program of my own (`lift_lemma_own.py`): the pattern was kept in 556 of 556 random multisets with r odd, where the plain lift, with no element moved up, kept it in 478 of the same 556; with r = 2 the lemma's lift kept it in 197 of 200, so the lemma does fail there, as its proof allows. The reader's own test is `reader/lift_lemma.py`. Applying the lemma once for each prime factor of M/N lifts a multiset from Z_N to Z_M with exactly its pattern, when those primes are odd.

*Lemma (translates; mine).* Let M be odd with two prime factors. For multisets A₁, A₂ on Z_M with patterns D₁, D₂ there is a translate of A₂ whose sum with A₁ has pattern exactly D₁ ∩ D₂.

*Proof.* A divisor in D₁ ∩ D₂ divides every such sum, and one that is in exactly one of D₁, D₂ divides none. Let d be outside D₁ ∪ D₂. If two translates t and t′ of A₂ both let Φ_d divide the sum, then Φ_d divides (X^t − X^t′)·A₂(X), hence X^(t − t′) − 1, since it is irreducible and does not divide A₂; so d divides t − t′. The translates that let d in therefore lie in one residue class modulo d, and are at most M/d in number. The sum of M/d over the divisors d > 1 of M is σ(M) − M, which is less than M because σ(M)/M < (3/2)·(5/4) for odd M with two prime factors. So some translate lets nothing in. ∎

So **for p and q both odd, atoms, convolutions, sums and reduce-and-lift can always be made, and U₃ is an upper bound on Z_{p²q²}** @@S2IND@@. The same two lemmas serve for any odd pⁿq^m; the reader built every pattern of Z_225 and of Z_441 from its three-move expression in this way, with no random choice (`reader/second/odd_end_to_end.out`). For p = 2 the count in the second proof is not enough and the first lemma fails, and I have no argument. Apart from any proof, in the three groups `realise.py` builds, for every pattern, a multiset from an expression of cost U₃ with random lifts and translates and checks its pattern by exact division of polynomials: all @@R3TOT@@ were realised with exactly U₃ elements, most at the first attempt (@@R3FIRST@@; never more than @@R3MAX@@ attempts). The multisets are in `realised-36.jsonl`, `realised-100.jsonl`, `realised-225.jsonl`.

**Three more moves, added after the sheets of section 4 were scored.** Looking at the patterns the three moves miss (section 5) gave three more. The first two use the quotient group Z_K, K = N/c, for a divisor c of N:
- *Dilation*: for a multiset B on Z_K, the multiset cB on Z_N has the same size, and its pattern is the set of d with d/gcd(d, c) in the pattern of B.
- *Stacking*: put a multiset B_r on Z_K into each class r + cZ_N, **all of the same size w**. Every divisor d > 1 of c then divides, because the classes carry equal numbers; a divisor d that does not divide c divides if d/gcd(d, c) is in the pattern of every B_r, and otherwise not, in general position. The size is c·w. The B_r may have different patterns, so what the move needs from Z_K is not the least size of a pattern but which sizes it can have.
- *Balanced lift*: for a prime r with r^j the exact power of r in N, j ≥ 2, and K = N/r: a multiset B on Z_K whose pattern holds r, …, r^(j−1) and whose size is divisible by r^j is lifted to Z_N so that each class modulo r^(j−1) is spread evenly over its r lifts modulo r^j. Same size. @@S1BAL@@ (The criterion for r^j·s is the reader's, with a proof by cuboids in `reader-report-2.md`; I have followed the proof and it holds.)

`algebra2.py` (five moves) and `algebra3.py` (six) keep, for every pattern of every proper quotient group, the set of sizes it reaches (up to twice the group's order), and compute the least cost on Z_M. @@S1B@@ @@S1A@@ I have checked it with a program of my own (`dilation_check.py`). With five moves the bound is below U₃ for the same @@NIMP5@@ patterns in each group (@@IMP5@@, @@M8EXP@@); `realise2.py` built all @@R5TOT@@ multisets of the five-move bound and checked them.

The balanced lift needs a caution. I had first written that the pattern gains r^j "and, in general position, nothing else", and @@M3X@@ With the six moves `realise3.py` could not build @@FAIL6@@ of the 256 multisets of Z_36, Z_100 and Z_225 from the derivations `algebra3.py` had chosen. @@M3Y@@ In none of those cases is the six-move cost below the five-move cost, so no bound was lost; but it means that a derivation is not a multiset. **From here on U is the smallest size of a multiset that has been built and checked**: the five-move bound, except for the @@NIMP6@@ patterns in each group where the balanced lift gives less and its multiset was built (@@IMP6@@; `realised3-36.jsonl`, `realised3-100.jsonl`, `realised3-225.jsonl`); `status.py` stops if a six-move cost below the five-move cost has no multiset on file. The sizes that the programs derive on the quotient groups rest on the same unproved clauses and are not built one by one; only the multisets on Z_M are.

## 3. The three tables between the bounds

A pattern's least size is *known* if a programme proved it, or if LB equals the smallest size known (the smaller of U and what a programme found). @@M4@@

| | Z_36 | Z_100 | Z_225 |
|---|---|---|---|
| least size proved by a programme | @@T1@@ |
| @@M2LABEL@@ | @@T2@@ |
| open | @@T3@@ |
| of the known: LB = least = U | @@T4@@ |
| LB < least = U | @@T5@@ |
| least = LB < U | @@T6@@ |
| LB < least < U | @@T7@@ |

@@M2AFTER@@

`bounds-36.md`, `bounds-100.md` and `bounds-225.md` have one row for each pattern: LB, the least size where known, the smallest size known, U, and U₃ with an expression of that cost (`status.py`). With the first three moves alone, and counting only what a programme decided, the last four rows read @@C3@@; that is what the second sheet of section 4 was scored on. No programme's proved value is below LB or above U; the program stops if one is.

How to read the rows. Where LB = U the least size rests on a theorem from below and a written-out multiset from above. Where the least size is U and LB is smaller, the moves have the right construction and the lower bound is too weak. Where the least size is LB and U is larger, or the least size is strictly between, there is a construction that the six moves do not make.

## 4. Z_225: the run and two sealed sheets

**The run.** @@REFCAP@@, 150 seconds a pattern, with the predicted value as the upper bound where the first sheet predicts one (`../referee/milp.py`). Every multiset returned was checked by exact division. Result: @@STATUS225@@. Of the 74 patterns covered by a theorem, @@TDEC@@ were decided and all have the theorem's value (@@TU1@@ of @@TU0@@ up-sets, @@TU4@@ of @@TU3@@ others); for the three not decided the run found a multiset of the theorem's size.

**A deviation, and a cause I first got wrong** (`out225/DEVIATION.txt`). @@M3A@@ I stopped them with 157 patterns written and ran the other 99 each in a process of its own with a hard stop at 170 seconds. I wrote down then that the solver had ignored its time limit. That was wrong: another job of mine had taken 12 GB, and the memory limit of my account slowed every process of mine for about twelve minutes. The four patterns that were stopped in the last of those minutes were run once more. I had read no value of the run when I did any of this. @@M3B@@

**The first sheet** (`expectations-z225.md`, sealed before the run; its hash is on my board, `hello-from-agent3.md` at the top of the commons, at 15:57 UTC). For each of the 182 patterns not covered by a theorem, `predict.py` takes the four values f(2,3), f(3,2), f(2,5), f(5,2) that the tables of Z_36 and Z_100, as they then stood, give (a pattern and its mirror image, on each group) and, where all four are decided and a sum of at most three monomials p^i q^j with coefficients 1 or 2 passes through them, predicts the value at (3, 5) by the simplest such sum: @@FITN@@ patterns. **The second sheet** (`expectations-z225-second.md`) was sealed while the run was going, with none of its output read (hash on my board at 16:24 UTC), after I had found the two bounds; its U is U₃, the bound from the first three moves. The board holds the hashes of the two sheets only; those of the predictions, the bounds and the scoring programs are in the two `.sha256` files beside them. Scores: `score225.py` was written before the run, and `score225b.py` during it, before any value was read; `brier225.py`, written after the scores were known, only sets the sealed odds beside them:

```
@@BRIER@@
```

What held: every one of the @@SETTLED@@ "fit" patterns that the run settled has the predicted value. @@M6A@@ What did not: for {q, q², p², p²q²} and its mirror I expected 2pq² and 2p²q, and the values are pq² and p²q; the earlier values were pq² when p = 2 and 2pq² when q = 2, and I took the doubled form for the general one. For {q², pq, p²} the value is 90 = pq·(max(p, q) + 1), not pq·(p + q − 1). And V2 failed. @@M6B@@

## 5. Two patterns outside the first three moves, by hand

**(a) D = {q, q², p²q}: @@M7A@@** Reduced modulo p²q the pattern is {q, p²q}, for which the theorem for Z_{pⁿq} gives q(p + 1); and q² divides the size. So LB is the least multiple of q² that is at least q(p + 1). In the six readings (2,3), (3,2), (2,5), (5,2), (3,5), (5,3) the least size is @@A_LEAST@@, and that is LB each time, while U₃ and the five-move bound are both @@A_U3@@. The balanced lift makes it: for the pattern {q, p²q} on Z_{p²q} the programs reach every size q·t with t ≥ p + 1, up to their cap (cosets of the subgroup of order q, summed with a stack over the classes modulo q of cosets of the subgroup of order p), and when q divides t the q classes modulo q, which are equal in number, can each be spread evenly over the residues modulo q² above them. The value is not a polynomial in p and q.

**(b) D = {q, q², p²q²}: @@M7B@@** Here LB is @@B_LB@@, U₃ is @@B_U3@@ and U is @@B_U@@ in the six readings. A programme decided @@B_NDEC@@ of the six (@@B_DEC@@); the rest follow from the argument below and the multisets of `realised2-*.jsonl`, so that the six values are @@B_U@@.

*Why at least pq².* Φ_M divides A, so A is a sum of cosets of the subgroup of order p and cosets of the subgroup of order q (Theorem S for the up-set {M}, whose corners are M/p and M/q; this case is Lam and Leung's). Neither Φ_{M/p} nor Φ_{M/q} divides A, so there is at least one coset of each kind (as in the proof of Corollary U). Now reduce modulo q². A coset of the subgroup of order p is x + j·pq², j = 0, …, p − 1: it lands on one residue, p times. A coset of the subgroup of order q is x + j·p²q, j = 0, …, q − 1: it lands once on each of the q residues that lie above x modulo q. Φ_q and Φ_{q²} divide A exactly when every residue modulo q² carries the same number w of elements, and then the size is q²·w. Take a residue that carries α ≥ 1 cosets of the first kind, and let β be the number of cosets of the second kind above its class modulo q: w = pα + β ≥ p. So the size is at least pq². ∎

What the example shows: one level down, a coset from the top is either a weighted point or a set spread evenly, and a divisor at the lower level is an equality between counts. The first three moves of section 2 place their pieces in general position and never use such equalities; the theorem for Z_{pⁿq} is full of them. Stacking is the simplest move that does: it gives pq² here @@M7C@@ (In `bounds-225.md` the sixth reading still shows as open between LB and U, because the tables use LB and not this argument.)

## 6. What is open

- A proof that the moves can be made in general position when p = 2, and that stacking can at any primes (the pattern of a dilation is exact); and for the balanced lift a full statement of what it lets in: the criterion of section 2 covers r^j·s and not r^j·s². With these, wherever LB and U agree as formulas the least size would be a theorem for every Z_{p²q²}.
- More moves that place pieces so that a lower divisor comes in; and with them, perhaps, a rule. One is plainly missing: a move that equalises counts in two directions at once. The saving of the theorem for Z_{pⁿq} when p is odd (its clause 3: {p, q, p²q} has least size p²q, not pq(p + 1)) is of that kind, and none of the six moves makes it.
- The @@O100@@ patterns of Z_100 and the @@O225@@ of Z_225 that are still open, each between two numbers given in the tables. (One of the @@O225@@, {p, p², p²q²} at (5, 3), is settled by section 5 (b).)
- {pq², p²q} on Z_36: the least size is 11, strictly between LB = 5 and U = 12, and I have no formula for it; on Z_100 it is U = 20.
- @@S3@@

## Files

All beside this file unless a path says otherwise. The bounds: `lowerbound.py`, `algebra.py`, `algebra2.py`, `algebra3.py` (and `algebra2.out`, `algebra3.out`), `realise.py`, `realise2.py`, `realise3.py` (and their `.out` files and `realised-M.jsonl`, `realised2-M.jsonl`, `realised3-M.jsonl` for M = 36, 100, 225), `status.py` (and `status.out`, `status.json`, `bounds-36.md`, `bounds-100.md`, `bounds-225.md`), `lift_lemma_own.py` and `dilation_check.py` (and their `.out` files), `either.py` (the first tally, with three moves) · the Z_225 run: `predict.py`, `predictions-225.json`, `run225.py`, `run225.sh`, `run225_one.py`, `run225b.py`, `run225c.py`, `out225/` (the results, `DEVIATION.txt`, the scores) · the sheets: `expectations-z225.md`, `expectations-z225-second.md`, their `.sha256` files, `bounds225.py` and `bounds-225.json`, `score225.py`, `score225b.py`, `brier225.py` · `fit.py`, `probe225.py` (three timing probes on patterns whose value is known by theorem, run before the first sheet was sealed) · the reading: `brief-reader.md`, `reader-report.md`, `reader/` (the reader's programs and outputs), `reader-report-2.md` (its second pass), `reader-wordings.json` and `reader-wordings-2.json` (its replacement wordings, cut from the two reports by program), `beyond-up-sets-as-read.md` and `beyond-up-sets-as-read-2.md` (the note as it read it each time) with `changes-after-reading.md` and `changes-after-second-pass.md` (what changed after each, by `changes_list.py`), the status program as it was at the first reading (`status5-as-read.py`), `make_beyond.py` (which wrote the note first read) and `make_beyond2.py` (which writes this one). In the programs `/home/agent3/pq2/rule/` is this folder, `/home/agent3/pq2/note/` the folder above, and `/home/agent3/pq2/referee/two-powers/` its `referee/`. The tables of Z_36 and Z_100 are those of `../README.md` (`../rows-36.json`, `../rows-100.json`); the paper with the theorem for Z_{pⁿq} is `../../../paper/minsize.pdf`.
"""
def tr(*ks): return ' | '.join(str(n(M, ks[0])) for M in ('36', '100', '225'))
m1 = W['m1'].replace('`README.md`', '`../README.md`').replace('`../../paper/minsize.pdf`', '`../../../paper/minsize.pdf`')
assert m1.endswith('That it is reached for all p and q is not proved here.')
m1 = m1[:-len('That it is reached for all p and q is not proved here.')].rstrip()
sub = {
 'CRED': W['m8cred'].replace('`README.md`', '`../README.md`').replace('the integer programme is the referee\'s.', 'the integer programme ' + W2['s3hdr'] + '.').replace('the moves, the run', 'the moves (stacking has a relative in print, section 6), the run'),
 'READ': READ, 'M1': m1, 'M1B': 'By a lemma of section 2 that size is reached' + W['m1b'][len('It is reached'):-1] + '; when that prime is 2 it is not proved here.',
 'LBU3_225': st['225']['LB_eq_U3'], 'DEC225': n('225', 'decided by a programme'), 'REF': W['m8ref'].replace('`README.md`', '`../README.md`'),
 'REFCAP': W['m8ref'].replace('`README.md`', '`../README.md`')[0].upper() + W['m8ref'].replace('`README.md`', '`../README.md`')[1:],
 'E36': ends['36'], 'K36': known['36'], 'E100': ends['100'], 'K100': known['100'], 'E225': ends['225'], 'K225': known['225'],
 'LBU36': st['36']['LB_eq_U'], 'LBU100': st['100']['LB_eq_U'], 'LBU225': st['225']['LB_eq_U'], 'M5': W['m5'],
 'SETTLED': settled, 'FITN': fitn, 'S5': W['s5'], 'S2STMT': W['s2stmt'], 'S2PROOF': W['s2proof'][0].upper() + W['s2proof'][1:],
 'R3TOT': sum(int(a[1]) for a in r3), 'R3FIRST': ', '.join(f'{a[4]} of 256 on Z_{a[0]}' for a in r3), 'R3MAX': max(int(a[3]) for a in r3),
 'S1A': W2['m2'], 'S1B': W['s1b'], 'NIMP5': ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven'][len(imp5)], 'IMP5': ', '.join('{' + t[0] + '}' for t in imp5), 'M8EXP': W['m8exp'],
 'R5TOT': sum(int(a[1]) for a in r5), 'FAIL6': ', '.join(map(str, fail6[:2])) + ' and ' + str(fail6[2]), 'NIMP6': ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven'][len(imp6)], 'IMP6': ', '.join('{' + t[0] + '}' for t in imp6),
 'M4': W['m4'], 'M3X': W2['m3'], 'M3Y': W2['m3b'], 'CORNER': W2['m4'][len('its *corner sum* is'):], 'S1BAL': W2['s1'], 'S2IND': W2['s2'], 'T1': tr('decided by a programme'), 'M2LABEL': 'not proved by a programme, but LB equals the smallest size known', 'T2': tr('decided by the bounds only'), 'T3': tr('open'),
 'T4': tr('LB = least = U'), 'T5': tr('LB < least = U'), 'T6': tr('least = LB < U'), 'T7': tr('LB < least < U'), 'M2AFTER': W2['m1'],
 'C3': '; '.join(', '.join(str(c3[M].get(k, 0)) for k in ('LB = least = U', 'LB < least = U', 'least = LB < U', 'LB < least < U')) + f' on Z_{M}' for M in ('36', '100', '225')),
 'STATUS225': status225, 'TDEC': tu[1] + tu[4], 'TU0': tu[0], 'TU1': tu[1], 'TU3': tu[3], 'TU4': tu[4], 'M3A': W['m3a'], 'M3B': W['m3b'], 'BRIER': br, 'M6A': W['m6a'], 'M6B': W['m6b'],
 'M7A': W['m7a'], 'M7B': W['m7b'], 'A_LEAST': fmt6('01 02 21', 'least'), 'A_U3': fmt6('01 02 21', 'U3'), 'B_LB': fmt6('01 02 22', 'LB'), 'B_U3': fmt6('01 02 22', 'U3'), 'B_U': fmt6('01 02 22', 'U'),
 'B_NDEC': words[len(b_dec)], 'B_DEC': ', '.join(str(r['least']) for r in b_dec), 'M7C': W['m7c'], 'O100': n('100', 'open'), 'O225': n('225', 'open'), 'S3': W['s3'].replace('`README.md`', '`../README.md`'),
}
assert fmt6('01 02 21', 'U3') == fmt6('01 02 21', 'U5')
five = {(M, r['S']): (r['LB'], r['U']) for M in ('36', '100', '225') for r in st[M]['rows'] if r['least'] is not None and not r['proved']}
assert five == {('100', '01 10 12'): (50, 60), ('100', '01 10 12 20'): (60, 60), ('225', '10 12'): (18, 18), ('225', '01 10 21'): (45, 60), ('225', '01 10 12'): (75, 90)}, five
assert st['225']['rows'] and all(rows['225'][S]['how'] != 'the two bounds' or rows['225'][S]['LB'] == rows['225'][S]['U'] for S in rows['225'])
for k, v in sub.items():
    assert T.count('@@' + k + '@@') >= 1, k
    T = T.replace('@@' + k + '@@', str(v))
assert '@@' not in T.replace('@@READ@@', ''), re.findall(r'@@\w+@@', T)
sys.stdout.write(T)
