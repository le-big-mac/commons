*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

# INSPI: blind referee's report

Written 26 Nov 2026, started 14:20:50 UTC, before seeing anyone else's answer. I read only the two book files named in the brief and wrote only in `/home/agent2/inspi/referee/`.

Notation. Turns are counted in whole turns: a = ANGLE/360, INC/360 = p/q in lowest terms, e(x) = exp(2 pi i x). Step k (k = 0, 1, 2, ...) is made on heading h_k, then the turtle turns by a + k p/q. So h_0 = 0, h_k = k a + (p/q) k(k-1)/2, and the position after n steps is P_n = sum over k < n of e(h_k). (Right or left turning only mirrors the picture.) SIDE = 1.

## 1. When it comes home, and after how many steps (pencil; checked by three programs)

Book, section 1.3: "Looping Lemma Any program that is just a repetition of some basic loop of turtle instructions has precisely the structure of POLY with an angle input equal to T, the total turning in the loop." Unexpectedly closed: total turning a multiple of 360 and "the sidelength of the underlying POLY ... might turn out to be 0 as well! This corresponds to having a looping program in which the basic loop closes all by itself."

1. ANGLE is back to its first value (mod 360) after n steps iff n p/q is whole iff q divides n. So home can only happen at n = m q.
2. Shift identity: h_{k+q} - h_k = q a + (p/q)(2kq + q(q-1))/2 = h_q + k p. So e(h_{k+q}) = e(t) e(h_k) with **t = h_q = q a + p(q-1)/2**, in degrees **T = q ANGLE + 180 p (q-1)**. (Mod 360: T = q ANGLE if q is odd, q ANGLE + 180 if q is even, since then p is odd.) Each block of q steps is the block before it turned through T: this is the looping lemma for INSPI, with basic loop q steps and total turning T. It agrees with the book's answers "36A + 180 (mod 360)" for INC 10 and "nA + INC X n(n - 1)/2, or, equivalently, nA + (n - 1)180" for INC 360/n.
3. Put D = P_q. Then P_{mq} = D (1 + e(t) + ... + e((m-1)t)) and the heading after m q steps is m t.
4. If t is not whole: P_{mq} = D (1 - e(mt))/(1 - e(t)), which is 0 whenever m t is whole. So home at m q iff m t is whole. That needs t rational, t = s/r in lowest terms (r >= 2), and the first time is m = r.
5. If t is whole: P_{mq} = m D, so home iff D = 0. By the lemma in question 2, |D| = sqrt(q), so never.

**Result.** The turtle comes home iff ANGLE/360 is rational and T = q ANGLE + 180 p (q-1) is not a multiple of 360. Then the first home is after exactly **q r steps**, r = the denominator of T/360 in lowest terms (for whole degrees r = 360/gcd(T, 360)). If T is a multiple of 360 it never comes home; if ANGLE/360 is irrational its heading never returns.

Check: `analyse.py` sets this beside my simulation for all 129,240 whole-degree pairs: 0 disagreements (`analyse_out.txt`). The comparison can fail: with the 180 p (q-1) term dropped it disagrees on 105,300 pairs, and with the loop taken as 360 steps on 80,590 (`extra4_out.txt`). `offgrid.py` tries 18,224 cases with q in 1..16, 25, 27, 32 and ANGLE = u/v turn, v up to 16: 0 disagreements (`offgrid_out.txt`). The book's example (ANGLE 2, INC 20): T = 3096 = 216 mod 360, r = 5, home at 90 steps; program gives 90. Sure of this.

## 2. Can INSPI be unexpectedly closed? No. (pencil proof; checked by program)

Lemma. If T is a multiple of 360 then |D|^2 = q exactly.
Proof. t whole makes e(h_k) periodic in k with period q (step 2). |D|^2 = sum over k, l in 0..q-1 of e(h_k - h_l). For fixed l put k = l + d (mod q), d in 0..q-1; periodicity lets me use h_{l+d}. Now h_{l+d} - h_l = d a + (p/q)(2ld + d(d-1))/2 = h_d + l d p/q. So |D|^2 = sum over d of e(h_d) [sum over l = 0..q-1 of e(l d p/q)]. The bracket is a full geometric sum: q if q divides d p, i.e. d = 0, otherwise 0. So |D|^2 = q e(h_0) = q.

So whenever the total turning of the basic loop is a multiple of 360, **the turtle goes exactly sqrt(q) times SIDE with each repetition of its q-step loop**, q the denominator of INC/360 (whole degrees: q = 360/gcd(INC, 360)). It is never 0, so the basic loop never closes by itself. Example: INC 20, ANGLE 10 goes sqrt(18) = 4.243 every 18 steps (the book's own answer to exercise 9 of 1.1 names this family: "One example is an increment of 20 and an angle equal to 10 times an odd number.").

Check: over the 14,090 never-home whole-degree pairs the largest | |D| - sqrt(q) | is 4.3e-14 (`analyse_out.txt`); off grid 4.4e-15 over 2,832 cases (`offgrid_out.txt`). Sure.

Two cautions that belong with this answer (see 8): the basic loop must be the shortest one (q steps); and D = 0 does happen when T = 180.

## 3. Whole-degree count (programs)

Programs: `inspi_ref.py` (numpy; turning in exact integers; output `inspi_ref_out.json`, log `inspi_ref_run.log`, 46 s) and `literal.js` (node; one step at a time, no theory; output `literal_out.json`, 28 s). Tolerance for "at its starting point": distance below 1e-9. In `inspi_ref.py` every such decision at a return of heading and ANGLE was also made exactly, by reducing the count of steps on each of the 360 headings modulo the 360th cyclotomic polynomial in whole numbers; the two agreed on all 129,240 pairs. Largest distance called zero 1.4e-13; smallest called not zero 1.41421 (sqrt 2).

"Never" in `inspi_ref.py` means: at the first return of (heading, ANGLE) the position is not zero; later returns are at multiples of that time with multiples of that displacement. In `literal.js` it means only "not home in 5000 steps". Both give the same sets.

- Never come home: **14,090** of 129,240 (10.9%). Come home: 115,150.
- INC with such ANGLEs: **exactly the even INC**, all 179 of them (2, 4, ..., 358); each has 360/gcd(INC, 360) such ANGLEs. With g = gcd(INC, 360): ANGLE is a multiple of g when 8 divides INC, and ANGLE = g/2 mod g otherwise (pencil, from T = 0 mod 360). Every odd INC comes home from every ANGLE. Pencil total: sum over divisors d > 1 of 180 of d phi(d) = 11 x 61 x 21 - 1 = 14,090.
- Largest number of steps: **720**, reached by 55,296 pairs. Pencil bound: q even gives gcd(T, 360) >= q/2, so q r <= 720; q odd gives q r <= 360. Home times that occur: 4, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 30, 36, 40, 45, 48, 60, 72, 80, 90, 120, 144, 180, 240, 360, 720.

Sure (two programs and the formula agree).

## 4. Widest and narrowest (programs; all 115,150 measured)

All home-coming pairs were measured, twice: `inspi_ref.py` (convex hull, then all pairs of hull corners; 450 random pairs also by brute force, largest difference 1.1e-14) and `literal.js` (every pair of corners, brute force). "Corners" = all positions after each step; a point where the turn is 0 lies inside a straight stretch and cannot be an end of the greatest distance.

- **Widest: 83.5945684092**, 32 pairs, 720 steps: INC 135 or 225 with ANGLE 22, 23, 67, 68, 112, 113, 157, 158, 202, 203, 247, 248, 292, 293, 337, 338. These 32 are one figure: ANGLE -> ANGLE + INC starts the same closed path one corner later, ANGLE -> INC - ANGLE walks it backwards, (INC, ANGLE) -> (360 - INC, 360 - ANGLE) mirrors it. Here q = 8, T = 356, |D| = 2.8523, skeleton circle radius 40.865; twice the greatest distance from its centre gives 83.5945684092 again (`extra2_out.txt`).
- Next: 82.5067756 (INC 45, 315, same sixteen ANGLEs), 81.7366306 (INC 180; ANGLE 89, 91, 269, 271), 67.1645071 (INC 120, 240; ANGLE 1, 119, 121, 239, 241, 359), 58.0222976 (INC 90, 270).
- **Narrowest: 1.9318516526 = 2 cos 15 degrees**, 4 pairs, 6 steps: INC 180 with ANGLE 30, 150, 210, 330 (one figure; I checked ANGLE 30 by hand). Next: 1.9753767 = 2 cos 9 (INC 180; ANGLE 18, 162, 198, 342), 1.9923894, 1.9972591, 1.9996954 (INC 180; ANGLE 10.., 6.., 2..).

Sure of the numbers. See 8 for why "widest" is a property of the whole-degree grid.

## 5. Does a never-home turtle ever stand on its start again? No. (programs)

None of the 14,090 does, on any heading. `inspi_ref.py` checked each for ceil(loop/|D|) + 2 loops (up to 2880 steps); beyond that the distance is at least 2|D| >= 2.8 because after m loops and j more steps the position is m D + P_j with |P_j| <= j. `literal.js` (5000 steps) agrees.
Closest: **0.014030919392**, at step 15, by INC 2 with ANGLE 155 or 179 (heading then 15 degrees) and their mirrors INC 358 with ANGLE 181 or 205 (heading 345). Next distinct values: 0.014132139, 0.014926481.
Off grid, none of 2,832 never-home cases stood on its start again either. I have no proof; this is a finding by exhaustion.

## 6. On the start, facing as it began, with a different next turn? No. (programs)

No whole-degree pair, at any step up to its home time (home-coming pairs) or within the checked steps (never-home pairs); both programs give 0. None among the 18,224 off-grid cases. No proof. For whole degrees the third clause of "home" is therefore never the one that decides.

## 7. Web (about five minutes by the clock; eight searches; fourteen addresses fetched with client name research-script/1.0, each into its own folder f1..f14)

Quotations from Wikipedia are from the raw page text with link and formula markup removed; quotations from scanned papers are as the machine read them.

Has the exercise been answered? **I found no answer under the name INSPI.** Under other names the two halves are in print:

- Fergus Murray, "The Curlicue Fractal", https://oolong.co.uk/curlicue/ (f1). Same turtle: "This is the trail left by a turtle which takes steps of a fixed size and turns left faster and faster each step." He states the two behaviours and leaves the question open: "For some values, it will return to the starting position as well as its original orientation; for most, it will repeat the same few steps ad infinitum as it dances off into the distance. If you can put your finger on what makes the difference between these two sorts of behaviour, you are almost certainly a better mathematician than me." His program has ANGLE a multiple of INC, where my T is 180 p (q-1): it marches when q is odd and closes in 2q steps when q is even, which fits his "a number of steps equal to the denominator of that fraction if it is odd, or twice the denominator if it's even".
- D. H. Lehmer, "Incomplete Gauss sums", Mathematika 23 (1976) 125-135, copy at https://gkfweb.math.illinois.edu/oldnew/math595/2015/jli135/Incomplete%20gauss%20sums.pdf (f12; I read its first page and the top of its second). The marching rule for ANGLE = INC/2 is there (machine-read text, symbols garbled): "Km > JV so that m = qN + m0 (0 < m0 < JV), then clearly GN(m)=qGN(N) + GN(m0)", with "GN(N) is the ordinary Gauss sum" and its value "0, if JV = 4k + 2".
- Moore and van der Poorten, "On the thermodynamics of curves and other curlicues", https://maths.anu.edu.au/files/CMAProcVol22-MoorePoorten.pdf (f10; read as far as its section 2.4): "The secret lies in understanding the classical complete Gau£ sums, namely when r E Q." (as machine-read; "Gauss sums, namely when tau is rational").
- Berry and Goldberg, "Renormalisation of curlicues", Nonlinearity 1 (1988) 1-26: **not read**. scilit.com and iopscience.iop.org both answered 403 and I left them alone; Crossref and Semantic Scholar returned no abstract. A search summary (not the paper) says the sum for tau = p/q grows linearly when pq is even and retraces a finite pattern when pq is odd. That is my rule at ANGLE = INC/2 (T = 180 p q). Unverified at source.

Name of the fact: the modulus of a (generalised) **quadratic Gauss sum** is sqrt(q); my proof is its **zero periodic autocorrelation** form.
- Number theory: https://en.wikipedia.org/wiki/Quadratic_Gauss_sum (f3): "For b > 0 the Gauss sums can easily be computed by completing the square in most cases." and, for c odd, G(a,b,c) = epsilon_c sqrt(c) (a/c) e^{-2 pi i psi(a) b^2 / c}.
- Radio, radar, mobile telephony: https://en.wikipedia.org/wiki/Zadoff%E2%80%93Chu_sequence (f2): "Zadoff–Chu sequences are CAZAC sequences (constant-amplitude zero-autocorrelation waveform)." and "The auto correlation of a Zadoff–Chu sequence with a cyclically shifted version of itself is zero, i.e., it is non-zero only at one instant which corresponds to the cyclic shift." The page's x_u(n) = exp(-j pi u n (n + c_f + 2q)/N) is the turtle's heading sequence at the never-home ANGLEs (u = p, N = my q). Used in LTE synchronisation signals (same page).
- Physics: "curlicues" (Berry and Goldberg; Dekking and Mendes France 1981, cited in f10 and f11, not read), Cornu spiral and Fresnel integrals (Lehmer's abstract: "The analysis employs the Fresnel integrals and the Cornu spiral"). The Talbot effect in optics is from memory only: I fetched the Wikipedia page (f9) but only searched it for three words.
- MathWorld "Curlicue Fractal", https://mathworld.wolfram.com/CurlicueFractal.html (f4), treats only irrational parameters.
- f5 (404), f6, f7 (refusals), f8 (a redirect stub), f13, f14 (no abstract) gave nothing. Cellarosi, arXiv:0905.1092 (f11): I read only its first two pages.

## 8. What a careful write-up should also say

1. **Which loop.** "Unexpectedly closed" only means something for the shortest loop (q steps). Taken as a 360-step loop, every even INC has total turning 0 mod 360, and all 50,350 home-coming pairs with even INC have a home time dividing 360, so the 360-step "loop" closes with turning 0 (`extra2_out.txt`). That is an ordinary closed figure counted twice or more, not an unexpected one.
2. **D = 0 with the heading off.** With q even and ANGLE = INC the basic loop ends on the starting point facing backwards (T = 180): 315 whole-degree pairs, ANGLE = INC for every INC not divisible by 8, and no others (`extra_out.txt`, `extra4_out.txt`). Pencil: the terms k and q-1-k cancel. The POLY skeleton has side 0. Anyone who reads "closed" as "back at the start" will count these as closing in q steps; they are home at 2q.
3. **Passing through the start.** 54,723 of the 115,150 home-coming pairs stand on the start before coming home, on another heading.
4. **sqrt(q) holds only at T = 0.** Elsewhere |D| varies with ANGLE (mean square over ANGLE is q): 2.8523 against sqrt 8 = 2.8284 for INC 135, ANGLE 22; 0.01745 for INC 180, ANGLE 179; 0 in the 315 cases.
5. **Widest and longest are grid facts.** The widest figures sit half a degree either side of INC 135, ANGLE 22.5, which never comes home; on a finer grid the width is unbounded (radius |D| / (2 sin(T/2))). Likewise 720.
6. **Outside the lemma.** INC/360 irrational: no loop, never home. ANGLE/360 irrational with INC rational: bounded, never home. INC = 0 is POLY.
7. **How many figures.** Under start-shift, reversal and mirror the 115,150 pairs make 945 classes. Five pairs of different classes share a diameter to 13 figures, e.g. (INC 60, ANGLE 0) and (INC 180, ANGLE 60), both 12 steps, 3.4641016 (`extra3_out.txt`). They are different figures: in each pair the number of distinct corners or the list of distances between corners differs (7 against 12 corners in the example; `extra4_out.txt`). So equal width does not mean same figure, though for the widest and the narrowest each tie list is one class.

## What I did not do

No proof for questions 5 and 6 (exhaustive on whole degrees, sampled off grid). Did not read Berry and Goldberg, Dekking and Mendes France, or more of Lehmer and Cellarosi than stated. Did not run broken copies of my simulation programs (only two wrong formulas against the comparison); the safeguards are two programs written differently, the exact whole-number test, and the pencil formula as a third witness. Did not draw any figure. Did not test irrational cases numerically. Did not ask why the five pairs of classes in item 7 of section 8 share a width. Last edit at 14:35:26 UTC by `date -u` (start 14:20:50), inside the 30 minutes. Nothing of mine is left running.
