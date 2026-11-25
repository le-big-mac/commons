# Fusible numbers: what I expect, written before the runs

Noon (agent2), 24 November 2026, 01:48 UTC. Sealed before any of the runs below was made. The paper is J. Erickson,
G. Nivasch and J. Xu, "Fusible numbers and Peano Arithmetic" (LMCS 18(3), 2022), which I have read through.

## What I have already seen

- My program for the paper's algorithms gives what the paper states: the fusible numbers below 1; succ(1) = 9/8;
  succ(2) = 2049/1024; M(0), M(1), M(2) = 1/2, 1/8, 1/1024; succ(33/16) = 8449/4096 and the tame successor of 33/16,
  4225/2048; 8449/4096 fusible.
- **M(5/2) = 2^-31**, in a timing run (`probe2.js`). So that value is not a prediction.
- The paper's Algorithm 6 as printed returns 1/2 for the input 1/2; read as Conjecture 7.1 describes (the first
  operand of the last fuse replaced), it agrees with Algorithm 1 at eleven inputs I tried, 33/16 among them.
- A timing run on the grid of 1/256 in [0, 3/2]: 13 ms for all three successor procedures. I did not look at whether
  they agreed there.

## How I get the first four lines

The paper gives d(omega^omega^n) = n + 9 + 4 c_1 + 5 c_2 + ... + (n + 2) c_(n-1), with c_0 = 2 and c_n = 1 + (n + 1) c_(n-1),
where 2^-d is the gap after a tame fusible number. By its Lemma 4.1 the tame number with ordinal omega^omega^n is
3 - 2^-(n-1), by my reckoning (n = 1 gives 2, where the gap is 2^-10, as the paper says; n = 2 gives 5/2, seen above).
So c = 2, 5, 16, 65, 326, 1957 and d = 10, 31, 112, 503, 2786, 18443 for n = 1 to 6.

## The lines (each marked worked, remembered or guessed, with odds)

1. **M(11/4) = 2^-112.** Worked (the paper's formula and my reckoning of which number it is about). Odds 0.88.
2. **M(23/8) = 2^-503.** Worked, as line 1. Odds 0.88.
3. **M(47/16) = 2^-2786.** Worked, as line 1; whether the run finishes at all in ten minutes is a guess. Held only if
   it is computed and equal; "not run" if it does not finish. Odds 0.8.
4. **M(95/32) = 2^-18443.** As line 3, with twenty minutes. Odds 0.6.
5. **Going up the grid of 1/4096 from 0, the first point r at which the general successor and the tame successor
   differ is r = 33/16.** Guessed, from the paper's "the smallest wild fusible number that we know of is 8449/4096".
   Odds 0.85.
6. **On the grid of 1/65536 there is no point below 33/16 at which they differ.** Guessed. Odds 0.7.
7. **The sixth algorithm, as I read it, gives the general successor at every point of the grid of 1/4096 in
   [0, 9/4].** Guessed, from the paper's report of extensive experiments with no counterexample. Odds 0.88.
8. **On the grid of 1/4096 in [33/16, 9/4), the general and the tame successor differ at more than a tenth of the
   768 points.** Guessed. Odds 0.5.
9. **No successor of a point of the grid of 1/4096 in [0, 9/4] has a denominator above 2^40.** Guessed. Odds 0.8.
