*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

Start `Fri Nov 27 14:29:27 UTC 2026`, end `Fri Nov 27 14:30:30 UTC 2026` (both from `date -u`). The full blind report follows the marker.

===BLIND===

**Blind step: coin sums**

Start 14:29:27 UTC, end 14:30:30 UTC, 27 Nov 2026 (both from `date -u`). Nothing under /home/agent2/coin or /srv/commons was opened, and no web search was made. Two runs, one process each, 1.36 s and 0.34 s of machine time.

Files:
- /home/agent2/referee-coin-27/blind.py (the program)
- /home/agent2/referee-coin-27/blind-out.txt (its output)
- /home/agent2/referee-coin-27/check.py and check-out.txt (a second route to (c))

How each count was made:
- **(a)** is a table filled amount by amount.
- **(b)** is the literal cashier's rule.
- **(c)** is a breadth-first search over signed coins on the window from -(2·max coin + L) to 2L + 2·max coin.
- **Check on (c):** I recomputed it as the least of a(m) + a(m − n) over m from n to L + 1500. The two agreed on all 14 coinages and on the two item-2 winners. The check reuses my (a) table, so it is not fully independent.
- **Ways for (c)** are listed by signed count per coin, so the same coins in the same directions count once.

**Item 1**

Averages are sum/L over amounts 0 to L − 1.

| coinage | L | (a) sum, avg | (b) sum, avg | (c) sum, avg | max (a) | max (c) | amounts with (b) > (a) |
|---|---|---|---|---|---|---|---|
| {1,5,10,25} | 100 | 470, 4.70 | 470, 4.70 | 398, 3.98 | 9 | 7 | 0 |
| {1,5,18,25} | 100 | 389, 3.89 | 458, 4.58 | 348, 3.48 | 6 | 6 | 37 |
| {1,2,5,10,20,50,100,200} | 100 | 340, 3.40 | 340, 3.40 | 272, 2.72 | 6 | 4 | 0 |
| {1,5,10,25,50,100} | 100 | 420, 4.20 | 420, 4.20 | 312, 3.12 | 8 | 5 | 0 |
| {1,2,4,8,16,32,64} | 100 | 316, 3.16 | 316, 3.16 | 267, 2.67 | 6 | 4 | 0 |
| {1,3,9,27,81} | 100 | 390, 3.90 | 390, 3.90 | 318, 3.18 | 8 | 5 | 0 |
| {16,19,21} | 100 | cannot pay 50 | stuck at 87 | 388, 3.88 | 5 (payable only) | 6 | 0 of the 13 the cashier finishes |
| {19,20,23,32} | 100 | cannot pay 46 | stuck at 87 | 309, 3.09 | 5 (payable only) | 5 | 0 of the 13 the cashier finishes |
| {1,5,16,23,33} | 100 | 329, 3.29 | 411, 4.11 | 306, 3.06 | 6 | 5 | 46 |
| {1,3,6,12,24,30} | 240 | 1398, 5.825 | 1440, 6.000 | 1323, 5.5125 | 11 | 10 | 42 |
| {1,5,10,25,100,200} | 500 | 2950, 5.90 | 2950, 5.90 | 2211, 4.422 | 11 | 7 | 0 |
| {1,3,4} | 10 | 16, 1.6 | 17, 1.7 | 16, 1.6 | 3 | 3 | 1 |
| {2,4} | 100 | cannot pay 50 | cannot pay 50 | cannot pay 50 | 25 | 25 | 0 |
| {1,10,25} | 30 | 135, 4.5 | 135, 4.5 | 83, 83/30 = 2.7667 | 10 | 4 | 0 |

Where the largest counts fall:

| coinage | max (a) at | max (c) at |
|---|---|---|
| {1,5,10,25} | 94, 99 | 88, 92, 93, 97 |
| {1,5,18,25} | 14, 82, 83, 88, 89, 92, 95, 96, 99 | 83, 89, 96 |
| euro set | 88, 89, 98, 99 | 33, 34, 36, 37, 63, 64, 66, 67, 73, 74, 76, 77, 83, 84, 86, 87 |
| {1,5,10,25,50,100} | 94, 99 | 63, 67, 68, 72, 78, 82, 83, 87 |
| {1,2,4,...,64} | 63, 95 | 43, 45, 51, 53, 75, 77, 83, 85, 86, 87, 89, 90, 91, 93, 99 |
| {1,3,9,27,81} | 80 | 41, 43, 47, 49, 59, 61, 65, 67, 95, 97 |
| {16,19,21} | 15 amounts: 83, 85, 86, 88 to 99 | 71, 81, 87 |
| {19,20,23,32} | 99 | 99 |
| {1,5,16,23,33} | 14 | 75, 86, 91, 93, 96, 97 |
| {1,3,6,12,24,30} | 221, 227, 233, 239 | 218, 220, 224, 226, 230, 232, 236, 238 |
| {1,5,10,25,100,200} | 394, 399, 494, 499 | 24 amounts; my program printed only the first 20: 338, 342, 343, 347, 353, 357, 358, 362, 438, 442, 443, 447, 453, 457, 458, 462, 463, 467, 468, 472 |
| {1,3,4} | 9 | 9 |
| {2,4} | 98 | 98 |
| {1,10,25} | 19 | 4, 6, 7, 13, 17, 18, 22, 28, 29 |

Smallest amount where (b) takes more than (a):

| coinage | amount | (a) | (b) |
|---|---|---|---|
| {1,5,18,25} | 28 | 18+5+5 (3 coins) | 25+1+1+1 (4 coins) |
| {1,5,16,23,33} | 20 | 5+5+5+5 (4) | 16+1+1+1+1 (5) |
| {1,3,6,12,24,30} | 48 | 24+24 (2) | 30+12+6 (3) |
| {1,3,4} | 6 | 3+3 (2) | 4+1+1 (3) |

Amounts that cannot be paid:
- **{16,19,21}**
  - (a) cannot pay 50 of the 100 amounts; the 50 payable sum to 180, mean 3.6 over those.
  - (b) is stuck at 87 amounts; the 13 it finishes sum to 30.
  - (c) pays all 100.
  - The cashier is stuck at 37 amounts that (a) can pay. The smallest is 32 = 16+16: the cashier takes 21 and is left with 11.
- **{19,20,23,32}**
  - (a) cannot pay 46; the 54 payable sum to 161, mean 161/54 = 2.981.
  - (b) is stuck at 87; the 13 it finishes sum to 24.
  - (c) pays all 100.
  - The cashier is stuck at 41 amounts that (a) can pay. The smallest is 38 = 19+19: the cashier takes 32 and is left with 6.
- **{2,4}**
  - All three ways fail on the 50 odd amounts, with change as well.
  - The 50 even amounts sum to 625 in each way, mean 12.5 over those.
- For these three coinages the average over all L is undefined in every way that has an unpayable amount.

Extra, not asked: the number of amounts where (c) is below (a), in the order of the first table, is 32, 32, 41, 46, 31, 28, 50, 46, 18, 43, 280, 0, 0, 14.

**Item 2: best single new coin, L = 100**

| base | for (a), coin 1 to 99 | new (a) | for (c), coin 1 to 199 | new (c) |
|---|---|---|---|---|
| {1,5,10,25} | 32 alone | 346, avg 3.46 (from 4.70) | 48 alone | 295, avg 2.95 (from 3.98) |
| euro set | 33 and 37 tie | 286, avg 2.86 (from 3.40) | 33, 36 and 37 tie | 241, avg 2.41 (from 2.72) |

Runners-up, as coin (sum):
- {1,5,10,25}, (a): 22 (349), 33 (349), 23 (350), 28 (350), 18 (351).
- {1,5,10,25}, (c): 43 (296), 42 (299), 47 (299), 63 (299), 67 (300).
- Euro set, (a): 34 (287), 27 (288), 36 (288), 38 (289), 43 (289).
- Euro set, (c): 34 (242), 67 (243), 43 (244), 66 (244), 83 (244).

**Item 3: adding the best coin for (a) twelve times, from {1,5,10,25}, L = 100**

The smallest coin is taken when several tie.

| step | coin added | sum | average (a) | coins tying |
|---|---|---|---|---|
| 0 | start | 470 | 4.70 | |
| 1 | 32 | 346 | 3.46 | 32 |
| 2 | 4 | 308 | 3.08 | 4, 9, 24 |
| 3 | 44 | 276 | 2.76 | 44 |
| 4 | 42 | 257 | 2.57 | 42, 46, 55 |
| 5 | 9 | 240 | 2.40 | 9 |
| 6 | 55 | 230 | 2.30 | 55 |
| 7 | 39 | 222 | 2.22 | 39 |
| 8 | 19 | 214 | 2.14 | 19, 22, 57 |
| 9 | 12 | 207 | 2.07 | 12, 43, 66 |
| 10 | 43 | 200 | 2.00 | 43, 54, 63, 66, 70, 73 |
| 11 | 47 | 193 | 1.93 | 47 |
| 12 | 48 | 188 | 1.88 | 48 |

The final set is {1, 4, 5, 9, 10, 12, 19, 25, 32, 39, 42, 43, 44, 47, 48, 55}.

**Item 4: single amounts**

In every case asked, one way for (a) is the cashier's way, wherever the cashier is not stuck.

{1,5,10,25}:

| amount | (a) | (b) | (c) | one way for (a) | every way for (c): over; back |
|---|---|---|---|---|---|
| 24 | 6 | 6 | 2 | 10+10+1+1+1+1 | 25; 1 |
| 39 | 6 | 6 | 4 | 25+10+1+1+1+1 | 25+10+5; 1 and 25+25; 10+1 |
| 60 | 3 | 3 | 3 | 25+25+10 | 25+25+10; nothing |
| 68 | 7 | 7 | 6 | 25+25+10+5+1+1+1 | 25+25+10+10; 1+1 and 25+25+25; 5+1+1 |
| 71 | 5 | 5 | 5 | 25+25+10+10+1 | 25+25+10+10+1; nothing and 25+25+25+1; 5 |
| 78 | 6 | 6 | 6 | 25+25+25+1+1+1 | 25+25+25+1+1+1; nothing and 25+25+25+5; 1+1 |
| 99 | 9 | 9 | 5 | 25+25+25+10+10+1+1+1+1 | 25+25+25+25; 1 |

Euro set {1,2,5,10,20,50,100,200}:

| amount | (a) | (b) | (c) | one way for (a) | every way for (c): over; back |
|---|---|---|---|---|---|
| 38 | 5 | 5 | 3 | 20+10+5+2+1 | 20+20; 2 and 50; 10+2 |
| 67 | 4 | 4 | 4 | 50+10+5+2 | 50+10+5+2; nothing and 50+20+2; 5 and 50+20; 2+1 |
| 99 | 6 | 6 | 2 | 50+20+20+5+2+2 | 100; 1 |

{16,19,21}:

| amount | (a) | (b) | (c) | every way for (c): over; back |
|---|---|---|---|---|
| 1 | cannot | stuck at once | 4 | 19+19; 21+16 |
| 24 | cannot | takes 21, stuck with 3 | 3 | 21+19; 16 |

**Item 5: four coins from 1 to 99 containing a 1, L = 100**

- 152,096 sets were tried, with the table filled coin by coin.
- The least sum is 389, average 3.89.
- Exactly two sets reach it: {1, 5, 18, 25} and {1, 5, 18, 29}.
- Both were recomputed with the plain table, 389 each.

**Item 6: a test for all amounts**

Yes, I know two, both from memory and not looked up, so the attributions are recollection.

- **Kozen and Zaks (1994)**: if (b) ever takes more than (a), the smallest such amount is below the sum of the two largest coins. Trying every amount below that sum therefore decides it.
- **Pearson (a Cornell report of 1994, printed in Operations Research Letters in 2005)**: a test with about n² candidate amounts for n coins.
  - Write the coins as c1 > c2 > ... > cn = 1.
  - For each i from 2 to n and each j from i to n, take the cashier's way of paying c(i−1) − 1.
  - Keep its counts for coins up to cj, add one more cj, and drop the smaller coins.
  - The amount w this makes is a candidate.
  - If any candidate's coin count is less than the cashier's count for w, the smallest such w is the smallest amount where (b) takes more. If none, there is no such amount.

I programmed Pearson's test as I remember it and set it beside trying every amount below 10,000. They agreed on all four sets. That shows the program is right on these four, not that I have remembered the theorem's statement correctly.

| coinage | Pearson's test | by trying below 10,000 | two largest coins sum to | at the smallest amount |
|---|---|---|---|---|
| {1,5,10,25} | none | none | 35 | (b) never takes more |
| {1,5,18,25} | 28 | 28 (5185 such amounts below 10,000) | 43 | 18+5+5 (3) against 25+1+1+1 (4) |
| {1,3,6,12,24,30} | 48 | 48 (1992 such) | 54 | 24+24 (2) against 30+12+6 (3) |
| {1,10,25} | 30 | 30 (3990 such) | 35 | 10+10+10 (3) against 25+1+1+1+1+1 (6) |

For {1,10,25} with L = 30, item 1 shows no amount where (b) takes more, because the first one is 30 itself, one past the range.
