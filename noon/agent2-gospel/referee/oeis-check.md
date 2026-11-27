*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

# Check of the draft for the OEIS (two sequences from the doubling turtle)

Start: Thu Nov 26 21:23:15 UTC 2026 (`date -u`). Limit 8 minutes. End: see the last line.
Read: `/home/agent2/drafts-for-owner/6-oeis-two-sequences.md` whole, the two b-files' ends, five lines of `6-oeis/terms.py`. My program: `referee/oeis_check.py` → `oeis-check.out` (the blind step's `rule.py` and `brute.py`, not `terms.py`). OEIS searches: fourteen requests, client `research-script/1.0`, three seconds apart, in `referee/web-oeis6/`. I edited nothing of yours.

**In short.** The terms, the counts, the claims in the comments and the formula are all right by my own program. The faults are of packaging: the b-files are not the ones the draft describes, a time is left unfinished, the Python program is a pointer and not a program, and two cross-references are missing that the OEIS already has (A053850 and A244623).

## Faults

1. **The b-files are not what the draft says.** Moderate; an editor would see it at once.
   "A b-file of the 6,830 terms up to 100,000 is `6-oeis/b-A.txt`." and "A b-file of the 2,643 terms up to 100,000 is `6-oeis/b-B.txt`."
   On disk `b-A.txt` has 1,408 rows, the last 19975, and `b-B.txt` 488 rows, the last 19989: the terms up to 20,000. They are right as far as they go (equal to my first 1,408 and 488, indices 1..n). The cause is probably the draft's own "check you can make in two minutes": `terms.py` writes `b-A.txt` and `b-B.txt` into the folder it is run from (lines 38 and 39, a bare file name), so running it with 20000 writes short files over the long ones. Make the b-files again with 100000, and have the two-minute check not write them.

2. **An unfinished time.** Low.
   "(the last with fifteen and twelve terms, at 21:2x UTC, with a control search that found the Wieferich primes)". "21:2x" is a placeholder.

3. **"(Python) as in `6-oeis/terms.py` (functions `order2` and `rad`)."** Moderate for the OEIS.
   A program line there must be the program. Paste the dozen lines, or leave Python out.

4. **Two cross-references the OEIS already has.** Low to moderate. Found by terms (`web-oeis6/j.json`, `k.json`).
   - A053850, "Odd numbers divisible by a square > 1." Sequence B is A053850 less sequence A, and every term of A is in A053850. The draft says "The odd terms of A013929"; A053850 is exactly that and should be the reference in both entries.
   - A244623, "Odd prime powers that are not primes." The prime-power terms of A are A244623 less the squares of the Wieferich primes; the comment "For an odd prime p and e >= 2, p^e is a term unless…" should cite it.
   - A077816, "Wieferich numbers (1): n > 1 such that 2^A000010(n) == 1 (mod n^2)", is a near relation an editor may ask about; I did not work out how it sits to A or B.

5. **What the Lehmers are made to say.** Low.
   "D. H. and E. Lehmer (1981) state it as: the period vanishes if and only if t(m) = p*t(m/p) for some prime p dividing m, t being the order of 2."
   Their abstract states it for a general q: "n k =0 if and only if t(n)=pt(n/p) for some prime p dividing n", where t(n) "is the order of q modulo n". Say "with t(n) the order of q modulo n; here q = 2". And the cover note is right that the abstract is all that has been read: an editor may want the page of the paper.
   The paper's title: the publisher's page gives "Cyclotomy for non-squarefree modul I" in its own metadata (`web-f3/page.html`), plainly "moduli" broken. I could not confirm the title from a second source in the time.

6. **"Item 45".** Low.
   The memo heads it "PROBLEM 45 (Gosper):" (both transcriptions). The OEIS's usual form is "HAKMEM, Item 45", so this may stand, but the link wants an address, and the entry might say "Item 45 (headed Problem 45)".

7. **Small things an editor would send back.**
   - Comments in the OEIS are signed and dated; these are not.
   - "The same holds for the program GOSPEL…": true; and the entry could say that the numerator does not matter (any a = 2*Pi*p/q with p prime to q), which an editor may ask.
   - "the study's referee searched once": twice now, this check included.

## Found sound

By `oeis-check.out` unless said:
- **Data.** A's 60 terms equal my first 60; B's 50 terms equal my first 50.
- **Name of A** (orders modulo m and modulo the squarefree kernel) against my rule by primes: no disagreement for odd m below 10^5.
- **Counts.** A: 8, 75, 715, 6830, 65801 for k = 2..6, and 639,419 at k = 7 (my recount of the last reading). B: 1, 21, 229, 2643, 28913, and 307,706 = 947,125 − 639,419. For k = 8 and 9 B's figures equal "with a square" less A's in your `count.sealed-run.out` (9,471,540 − 6,241,943 = 3,229,597; 94,715,253 − 61,137,859 = 33,577,394); those two rest on `count.c`.
- **"9*r is a term, for a prime r > 3, exactly when 3 divides the order of 2 modulo r"**: no failure by adding up the round for r < 2000, none by the rule for r < 111,111.
- **"For an odd prime p and e >= 2, p^e is a term unless 2 has the same order modulo p^e as modulo p"**: 218 prime powers up to 10^6, no failure. 1093², 3511² not terms and 1093³ a term: the blind step's sums.
- **"If every prime dividing m divides it at least squared and none of them is a Wieferich prime, then m is a term"**: no failure among odd m up to 10^6; the reason given is right.
- **The formula.** A002326 is "Multiplicative order of 2 mod 2n+1", offset 0, so A002326((m−1)/2) is the order of 2 modulo m. A007947 is the squarefree kernel, offset 1. A013929 is "Numbers that are not squarefree". A001220 is the Wieferich primes. All four read on the OEIS today.
- **Examples.** 2 has order 12 modulo 45 and 4 modulo 15; 6 modulo 63 and modulo 21; the four sets of 45 are right. 171, 9009 and 2525 are terms of B, and 63 is its first.
- **Fuchs's form** in the comment is his theorem of page 386 with 2 for q; "the case of the prime 2 in a theorem of L. Fuchs (1863)" is fair. The reference to his paper is as on the scan.
- **The HAKMEM sentences** in B's comment are whole and exact: "But a denominator of 171 = 9 * 19 never loops, probably because 9 divides phi(19). Similarly for 9009 and 2525." The paraphrase before them keeps "it seems".
- **The PARI lines**, read and not run (no `gp` on this machine): `factor(m)[, 1]` is the column of primes, `factorback` of it their product, `znorder(Mod(2, ·))` the order; `m%2 && m>1` keeps the modulus odd and above 1, and `!issquarefree(m)` shuts out 1 in B. I think both run and give the sequences. Someone should still run them once.
- **Absent from the OEIS.** By terms: twelve terms of A, ten of B: "no sequence" (and the three searches of the blind step). By words: "order of 2" with "squarefree kernel"; "multiplicative order of 2" with rad; "order of 2" with vanish: no sequence. "Gaussian period" and "Kummer period vanish" return unrelated entries.
- **"How sure I am"** is straight: `terms.py` does check sums only to 4,001 whatever its argument, as the note says; "the study … to 20,000 and a blind referee to 12,001" is right.

## Not done

- PARI not run.
- The counts for k = 8 and 9 not recounted.
- The Lehmers' paper, Evans's and Mahler's unread, as before; the Lehmers' title not confirmed.
- I read five lines of `terms.py`, not the whole.
- I did not look for an OEIS entry on the turtle under other words than those named, nor read the comments of A053850 or A077816 for a mention of the order of 2.
End: Thu Nov 26 21:26:35 UTC 2026 (`date -u`). Nothing of mine is left running.
