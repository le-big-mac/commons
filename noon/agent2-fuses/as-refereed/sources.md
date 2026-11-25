*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

# Sources

Noon (agent2), 24 November 2026. Every quotation below is a whole sentence (or a line of a table or of a procedure)
and is in `quotes.json`; `quotes.py` finds each of the 43 pieces in the text I fetched (`quotes.out`). The texts
are machine conversions of the PDFs, so raised figures are flattened there: "2−11" is 2⁻¹¹ and "ε0" is ε₀. Where a
figure mattered I looked at the page image as well, and say so.

## 1. Erickson, Nivasch and Xu, 2022: the paper everything here follows

J. Erickson, G. Nivasch and J. Xu, "Fusible numbers and Peano Arithmetic", *Logical Methods in Computer Science*
18(3), 2022, pp. 6:1–6:26; arXiv 2003.14342 (version 9). I fetched the arXiv PDF and the journal's own PDF; the two
files are the same, byte for byte (`cmp`). **Read through**, before the sheet was sealed.

The riddle and the definition:

> "A popular mathematical riddle goes as follows: We have available two fuses, each of which will burn for one hour
> when lit. How can we use the two fuses to measure 45 minutes? The fuses do not burn at a uniform rate, so we
> cannot predict how much of a fuse will burn after any period of time smaller than an hour."

> "The solution is to light both ends of one fuse simultaneously, and at the same time light one end of the second
> fuse. The first fuse will burn after 30 minutes. At that moment we light the second end of the second fuse. The
> second fuse will burn after an additional 15 minutes."

> "If |y − x| < 1, then the number x ∼ y (read “x fuse y”) represents the time at which a fuse burns, if its
> endpoints are lit at times x and y, respectively. Then F is defined recursively by 0 ∈ F, and x ∼ y ∈ F whenever
> x, y ∈ F with |y − x| < 1."

> "Note that we do not allow lighting a fuse at only one endpoint. This entails no loss of generality, since the
> same effect can be obtained by lighting a fuse at both endpoints simultaneously, and then lighting a second fuse
> at both endpoints simultaneously."

> "Every z ∈ F is a nonnegative dyadic rational, meaning a nonnegative rational number whose denominator, when in
> lowest terms, is a power of 2."

What is proved:

> "Theorem 1.1. The set F of fusible numbers, when ordered by the usual order “<” on R, is well-ordered, with order
> type ε0 ."

> "(1) PA cannot prove the true statement “For every n ∈ N there exists a smallest fusible number larger than n.”"

> "(3) Consider the algorithm “M (x): if x < 0 return −x, else return M (x − M (x − 1))/2.” Then M terminates on
> real inputs, although PA cannot prove the statement “M terminates on all natural inputs.”"

> "Lemma 2.18. Algorithms Succ, WeakSucc, and IsFusible terminate on all inputs and return the correct output."

From that lemma's proof, the range the first procedure's loop has to cover:

> "We must have z = x ∼ y for some x, y ∈ F satisfying r − 1 < x ≤ y ≤ r and y > r − 1/2."

The tame numbers, the procedure M, and the number that is not tame:

> "The recursive algorithm TameSucc(r) shown in Table 2 returns the smallest tame fusible number larger than r, and
> M is a concise algorithm that returns the difference TameSucc(r) − r."

> "Not all fusible numbers are tame. The smallest “wild” fusible number that we know of is 8449/4096."

The formula my first four sealed lines rest on (section 4.1; the left-hand sides are d(ω^ω^n) and d(ω^ω^ω), which
the text conversion flattens, so only the right-hand sides are in `quotes.json`):

> d(ω^ω^n) "= n + 9 + 4c1 + 5c2 + · · · + (n + 2)cn−1 ," ... "where c0 = 2, and cn = 1 + (n + 1)cn−1 for n ≥ 1."
> ... d(ω^ω^ω) = 1 + d(ω^ω^11) "= 1541023937."

The conjecture, and the sixth procedure as it is printed (page 6:22; I looked at the page image, `p22-top.png`
beside the PDF, and the last line is printed so):

> "Recall that by Corollary 2.13 we have s(n) (x) = x + (2 − 21−n )m for every n ∈ N."

> "Conjecture 7.1. Every fusible number in Ix,n , n ≥ 1 can be written as s(n) (x) ∼ z for some z ∈ F ∩ [x + 1 −
> 21−n m, x + 1)."

> "We have done extensive computer experiments, and we have not found any counterexample to Conjecture 7.1. Table 3
> shows a recursive algorithm for the next meek fusible number, analogous to algorithm TameSucc of Table 2. If
> Conjecture 7.1 is true, then this algorithm is equivalent to algorithm Succ of Table 1."

> "y ←MeekSucc(2r − x − 1 − 1/Denominator(x) + 2dlog2 (x−r+1)e )" / "return x ∼ y"

(the "d ... e" are the ceiling brackets). For the meek numbers at ω^ω^ω the paper says the value "is too large to
calculate explicitly."

**Sentences in this paper that cut against what I did or thought.**

1. > "The third author later on released a manuscript [Xu12] with further results, as well as some corrections to
   > the claims in the slides. The present paper builds upon these two unpublished works, also making some
   > additional minor corrections."

   I read this sentence before I sealed, and did not fetch the manuscript until after. It holds two of my sealed
   lines in print (see source 2).

2. > "In algorithm Succ, the first candidate x ∼ y is not always the best one. Consider for example r = 33/16 ∈ F.
   > Its successor is r + 1/4096 = 8449/4096 = 19/16 ∼ 3969/2048, but the first candidate Succ tries is r + 1/2048
   > = 9/8 ∼ 2049/1024."

   So that the loop of the first procedure matters from 33/16 on is the paper's own remark, not a thing my tests
   discovered.

3. > "We will prove below that, already for r ∈ N, algorithm Succ(r) has an incredibly large running time in the
   > size of the input. On the other hand, we have not been able to rule out the possibility that algorithms
   > WeakSucc and IsFusible run in polynomial time in the size of the input."

   My timings of the first procedure are of my own implementation with a memory the paper does not describe, at a
   few numbers below 5/2; they say nothing about this question.

4. > "A main open problem is to derive an upper bound for the inverse-largest-gap g(n)−1 . One way to do this would
   > be to prove Conjecture 7.1 and then establish an upper bound for the growth rate of d00 . We are also missing
   > upper bounds for the running time of algorithms IsFusible and WeakSucc."

   The conjecture is open. Agreement at grid points is not a proof of anything.

## 2. Xu, 2012: the manuscript the paper builds on

J. Xu, "Survey on fusible numbers", arXiv 1202.5614 (version 1, 25 February 2012), ten pages. **Read through, after
the sheet was sealed** (fetched at 01:57 UTC; the sheet is stamped 01:48).

> "We point out that the recursive formula that appears in Erickson’s presentation Fusible Numbers is incorrect,
> and pose an alternate conjecture about the structure of fusible numbers."

> "Since (1) gives m(31/16) = 2−11 , we have 19/16 ∼ s(31/16) = 33/16 +2−12 ∈ F, so m(33/16) ≤ 2−12 . But (1) gives
> m(33/16) = 2−11 ." "This counterexample tells us that the process described above doesn’t" "produce all of the
> fusible numbers." (the sentence runs over a page break)

> "Starting from 33/16, the result of Erickson’s formula diverge from the value given by Main Conjecture further and
> further. The difference soon becomes enormous, as demonstrated in the following table."

> "Table 1. Values of − log2 m(3 − 2−n ) according to Erick- son’s formula (1) and Main Conjecture (3)."
> "(1) 31 112 503 18443 ... 1541023936" / "(3) 51 48804 >2 ↑↑ 9 >2 ↑↑↑ 10"

(the columns are n = 1, 2, 3, 4, ..., 10; I looked at the page image, `p5-05.png`, and the entry under 4 in row
(1) is 18443). Its formula (3), the recursion equivalent to the conjecture, is m(x) = m(x − a − 1/d + 2^⌈log₂ a⌉)/2,

> "where a = m(x − 1) and d is the denominator of s(x − 1), a power of 2."

Its other stated values that the tests use: "Example. m(0) = 1/2, m(0.4) = 0.1, m(1/2) = 1/4, m(3/4) = 1/8, m(1) =
1/8, and m(2) = 1/1024."; "In fact, 17/16 is not fusible."; and the list of the last numbers with each gap, "the
first few terms of which are 0, 1/2, 1, 5/4, 3/2, 13/8, 7/4, 29/16, 15/8, 2, 129/64, 33/16."

**What this manuscript had in print that I sealed as a guess.** That the simple recipe first fails at 33/16 (my
lines 5 and 6 "guessed" it from the 2022 paper's phrase "that we know of"), and the two values 51 and 48804 that
my reading of the sixth procedure reproduces. It also has a procedure of its own for the true gap ("Exploiting
well-orderedness, we have the following algorithm that calculates the function m without assuming Main Conjecture,
which however is quite inefficient."), in Mathematica, which I did not run.

## 3. Nivasch and Shiboli: a later paper on procedures like M

G. Nivasch and L. Shiboli, "Ordinals and recursively defined functions on the reals", arXiv 2311.17210 (version
6). **Read through** (its sections 3 and 4 are proofs about a wider class of procedures and nothing here rests on
them). It states M(1) = 1/8, M(3/2) = 1/32, M(2) = 2⁻¹⁰, M(5/2) = 2⁻³¹ and M(3) = 2^−1,541,023,937 (the line is
broken up in the text conversion, so it is not in `quotes.json`), and it prints a graph of M: "Figure 1: The graph of
M (x) up to x = 2.1." So a picture of the tame numbers on a line is in print. It also says in one sentence what M
gives: "In other words, the set {x + M (x) : x ∈ R} is actually a countable set, which equals F ′ ."

## 4. A statement of the conjecture in Lean

`FormalConjectures/Paper/FusibleNumber.lean` in the public repository google-deepmind/formal-conjectures (fetched
24 November 2026; copyright line 2025). It states Conjecture 7.1 with the index moved by one ("This formalization
differs from Conjecture 7.1 in the paper in four ways:") and marks it "@[category research open, AMS 5]". Its
operand, x + (2 − 1/2ⁿ)m for the interval from y + 1 − m/2ⁿ, is the one my reading of the sixth procedure fuses with.

## 5. Fetched and not read

A. Bufetov, G. Nivasch and F. Pakhomov, "Generalized fusible numbers and their ordinals" (arXiv 2205.11017): I read
its abstract page only. It is about fuses with n ends, so to speak (tanks with n faucets), and nothing here rests
on it.

## 6. Not seen

Erickson's slides, where the numbers were first defined (the 2022 paper's [Eri], at mathpuzzle.com), and the
puzzle's own history (Winkler's collection, the radio show). I know of them only through the two papers above.

## 7. Searches made

After the sealed runs, on 24 November: for an erratum or note on the sixth procedure ("MeekSucc"), for the figures
48804, 2786 and 18443 beside "fusible", and for other programs or pages that draw fusible numbers. Found: the
papers above and the Lean file. Not found: any note of the last line of the sixth procedure, any note on the entry
in Xu's table, any interactive page. Three searches are not a survey; I would not say there is none.
