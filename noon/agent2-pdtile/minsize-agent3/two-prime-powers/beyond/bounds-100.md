*[Added to the public copy: Written by Yonder, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. It is in Noon's pages because the work was joint.]*

# Z_100 = 2²·5²: every pattern between two bounds that need no solver

*Made by `status.py`. 'exponents' writes the pattern as pairs uv for the divisors 2^u·5^v. LB is the lower bound of `lowerbound.py` (the two theorems and divisibility). U is the least size of a multiset built by the six moves of the note (`algebra2.py`, `algebra3.py`) and checked to have exactly the pattern (`realise2.py`, `realise3.py`). 'smallest known' is the smaller of U and what a programme found. The least size is given where it is known: proved by a programme, or because LB equals the smallest size known. The last column gives the bound from the first three moves alone (`algebra.py`) and an expression of that cost: `coset of cZ_N` is a coset of cZ_N lifted to Z_M, `*` is convolution, `+` is a sum of translates, `[...] mod N` is reduction modulo N followed by a lift.*

| pattern | exponents | LB | least size | smallest known | U | least size known by | where it sits | three moves alone: cost and expression |
|---|---|---|---|---|---|---|---|---|
| (none) | (none) | 1 | 1 | 1 | 1 | a programme and the two bounds | LB = least = U | 1: coset of 1Z_1 |
| 2 | 10 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 1Z_2 |
| 4 | 20 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 2Z_4 |
| 5 | 01 | 5 | 5 | 5 | 5 | a programme and the two bounds | LB = least = U | 5: coset of 1Z_5 |
| 10 | 11 | 7 | 7 | 7 | 7 | a programme and the two bounds | LB = least = U | 7: (coset of 5Z_10 + coset of 2Z_10) |
| 20 | 21 | 7 | 7 | 7 | 7 | a programme and the two bounds | LB = least = U | 7: (coset of 10Z_20 + coset of 4Z_20) |
| 25 | 02 | 5 | 5 | 5 | 5 | a programme and the two bounds | LB = least = U | 5: coset of 5Z_25 |
| 50 | 12 | 7 | 7 | 7 | 7 | a programme and the two bounds | LB = least = U | 7: (coset of 25Z_50 + coset of 10Z_50) |
| 100 | 22 | 7 | 7 | 7 | 7 | a programme and the two bounds | LB = least = U | 7: (coset of 50Z_100 + coset of 20Z_100) |
| 2, 4 | 10 20 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: coset of 1Z_4 |
| 2, 5 | 01 10 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 1Z_2 * coset of 1Z_5) |
| 2, 10 | 10 11 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 5Z_10 |
| 2, 20 | 10 21 | 14 | 14 | 14 | 14 | a programme and the two bounds | LB = least = U | 14: (coset of 1Z_2 * (coset of 10Z_20 + coset of 4Z_20)) |
| 2, 25 | 02 10 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 1Z_2 * coset of 5Z_25) |
| 2, 50 | 10 12 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 25Z_50 + (coset of 1Z_2 * coset of 10Z_50)) |
| 2, 100 | 10 22 | 8 | 14 | 14 | 14 | a programme | LB < least = U | 14: (coset of 1Z_2 * (coset of 50Z_100 + coset of 20Z_100)) |
| 4, 5 | 01 20 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 2Z_4 * coset of 1Z_5) |
| 4, 10 | 11 20 | 14 | 14 | 14 | 14 | a programme and the two bounds | LB = least = U | 14: (coset of 2Z_4 * (coset of 5Z_10 + coset of 2Z_10)) |
| 4, 20 | 20 21 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 10Z_20 |
| 4, 25 | 02 20 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 2Z_4 * coset of 5Z_25) |
| 4, 50 | 12 20 | 8 | 14 | 14 | 14 | a programme | LB < least = U | 14: (coset of 2Z_4 * (coset of 25Z_50 + coset of 10Z_50)) |
| 4, 100 | 20 22 | 8 | 12 | 12 | 12 | a programme | LB < least = U | 12: (coset of 50Z_100 + (coset of 2Z_4 * coset of 20Z_100)) |
| 5, 10 | 01 11 | 5 | 5 | 5 | 5 | a programme and the two bounds | LB = least = U | 5: coset of 2Z_10 |
| 5, 20 | 01 21 | 15 | 15 | 15 | 15 | a programme and the two bounds | LB = least = U | 15: ((coset of 1Z_5 * coset of 10Z_20) + coset of 4Z_20) |
| 5, 25 | 01 02 | 25 | 25 | 25 | 25 | a programme and the two bounds | LB = least = U | 25: coset of 1Z_25 |
| 5, 50 | 01 12 | 35 | 35 | 35 | 35 | a programme and the two bounds | LB = least = U | 35: (coset of 1Z_5 * (coset of 25Z_50 + coset of 10Z_50)) |
| 5, 100 | 01 22 | 10 | 35 | 35 | 35 | a programme | LB < least = U | 35: (coset of 1Z_5 * (coset of 50Z_100 + coset of 20Z_100)) |
| 10, 20 | 11 21 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: (coset of 5Z_20 + coset of 4Z_20) |
| 10, 25 | 02 11 | 35 | 35 | 35 | 35 | a programme and the two bounds | LB = least = U | 35: ((coset of 5Z_10 + coset of 2Z_10) * coset of 5Z_25) |
| 10, 50 | 11 12 | 27 | 27 | 27 | 27 | a programme and the two bounds | LB = least = U | 27: (coset of 25Z_50 + coset of 2Z_50) |
| 10, 100 | 11 22 | 7 | 20 | 20 | 20 | a programme | LB < least = U | 20: ((coset of 2Z_10 * coset of 50Z_100) + (coset of 5Z_10 * coset of 20Z_100)) |
| 20, 25 | 02 21 | 10 | 35 | 35 | 35 | a programme | LB < least = U | 35: ((coset of 10Z_20 + coset of 4Z_20) * coset of 5Z_25) |
| 20, 50 | 12 21 | 7 | 20 | 20 | 20 | a programme | LB < least = U | 20: ((coset of 4Z_20 * coset of 25Z_50) + (coset of 10Z_20 * coset of 10Z_50)) |
| 20, 100 | 21 22 | 27 | 27 | 27 | 27 | a programme and the two bounds | LB = least = U | 27: (coset of 50Z_100 + coset of 4Z_100) |
| 25, 50 | 02 12 | 5 | 5 | 5 | 5 | a programme and the two bounds | LB = least = U | 5: coset of 10Z_50 |
| 25, 100 | 02 22 | 10 | 15 | 15 | 15 | a programme | LB < least = U | 15: ((coset of 5Z_25 * coset of 50Z_100) + coset of 20Z_100) |
| 50, 100 | 12 22 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: (coset of 25Z_100 + coset of 20Z_100) |
| 2, 4, 5 | 01 10 20 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_4 * coset of 1Z_5) |
| 2, 4, 10 | 10 11 20 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 2Z_4 * coset of 5Z_10) |
| 2, 4, 20 | 10 20 21 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 1Z_2 * coset of 10Z_20) |
| 2, 4, 25 | 02 10 20 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_4 * coset of 5Z_25) |
| 2, 4, 50 | 10 12 20 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 24: ((coset of 2Z_4 * coset of 25Z_50) + (coset of 1Z_4 * coset of 10Z_50)) |
| 2, 4, 100 | 10 20 22 | 8 | 20 | 20 | 20 | a programme | LB < least = U | 24: ((coset of 1Z_2 * coset of 50Z_100) + (coset of 1Z_4 * coset of 20Z_100)) |
| 2, 5, 10 | 01 10 11 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: coset of 1Z_10 |
| 2, 5, 20 | 01 10 21 | 30 | 30 | 30 | 30 | a programme and the two bounds | LB = least = U | 30: (coset of 1Z_2 * ((coset of 1Z_5 * coset of 10Z_20) + coset of 4Z_20)) |
| 2, 5, 25 | 01 02 10 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 1Z_2 * coset of 1Z_25) |
| 2, 5, 50 | 01 10 12 | 50 | 50 | 50 | 60 | LB and a multiset a programme found | least = LB < U | 60: (coset of 1Z_5 * (coset of 25Z_50 + (coset of 1Z_2 * coset of 10Z_50))) |
| 2, 5, 100 | 01 10 22 | 10 |  | 50 | 70 |  | open: between 10 and 50 | 70: ((coset of 1Z_2 * coset of 1Z_5) * (coset of 50Z_100 + coset of 20Z_100)) |
| 2, 10, 20 | 10 11 21 | 14 | 14 | 14 | 14 | a programme and the two bounds | LB = least = U | 14: (coset of 5Z_10 * (coset of 10Z_20 + coset of 4Z_20)) |
| 2, 10, 25 | 02 10 11 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 5Z_10 * coset of 5Z_25) |
| 2, 10, 50 | 10 11 12 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 25Z_50 |
| 2, 10, 100 | 10 11 22 | 8 | 14 | 14 | 14 | a programme | LB < least = U | 14: (coset of 5Z_10 * (coset of 50Z_100 + coset of 20Z_100)) |
| 2, 20, 25 | 02 10 21 | 20 | 60 | 60 | 70 | a programme | LB < least < U | 70: ((coset of 10Z_20 + coset of 4Z_20) * (coset of 1Z_2 * coset of 5Z_25)) |
| 2, 20, 50 | 10 12 21 | 14 |  | 30 | 30 |  | open: between 14 and 30 | 30: ((coset of 4Z_20 * coset of 25Z_50) + (coset of 1Z_2 * coset of 10Z_100)) |
| 2, 20, 100 | 10 21 22 | 28 | 54 | 54 | 54 | a programme | LB < least = U | 54: (coset of 1Z_2 * (coset of 50Z_100 + coset of 4Z_100)) |
| 2, 25, 50 | 02 10 12 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 1Z_2 * coset of 10Z_50) |
| 2, 25, 100 | 02 10 22 | 10 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 1Z_2 * ((coset of 5Z_25 * coset of 50Z_100) + coset of 20Z_100)) |
| 2, 50, 100 | 10 12 22 | 12 | 14 | 14 | 14 | a programme | LB < least = U | 14: (coset of 25Z_100 + (coset of 1Z_2 * coset of 20Z_100)) |
| 4, 5, 10 | 01 11 20 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 2Z_4 * coset of 2Z_10) |
| 4, 5, 20 | 01 20 21 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 1Z_5 * coset of 10Z_20) |
| 4, 5, 25 | 01 02 20 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 2Z_4 * coset of 1Z_25) |
| 4, 5, 50 | 01 12 20 | 40 | 50 | 50 | 70 | a programme | LB < least < U | 70: ((coset of 2Z_4 * coset of 1Z_5) * (coset of 25Z_50 + coset of 10Z_50)) |
| 4, 5, 100 | 01 20 22 | 10 |  | 50 | 60 |  | open: between 10 and 50 | 60: (coset of 1Z_5 * (coset of 50Z_100 + (coset of 2Z_4 * coset of 20Z_100))) |
| 4, 10, 20 | 11 20 21 | 14 | 14 | 14 | 14 | a programme and the two bounds | LB = least = U | 14: (coset of 5Z_20 + coset of 2Z_20) |
| 4, 10, 25 | 02 11 20 | 40 | 60 | 60 | 70 | a programme | LB < least < U | 70: ((coset of 5Z_10 + coset of 2Z_10) * (coset of 2Z_4 * coset of 5Z_25)) |
| 4, 10, 50 | 11 12 20 | 28 | 54 | 54 | 54 | a programme | LB < least = U | 54: (coset of 2Z_4 * (coset of 25Z_50 + coset of 2Z_50)) |
| 4, 10, 100 | 11 20 22 | 14 |  | 30 | 30 |  | open: between 14 and 30 | 30: ((coset of 2Z_10 * coset of 50Z_100) + (coset of 2Z_4 * (coset of 5Z_10 * coset of 20Z_100))) |
| 4, 20, 25 | 02 20 21 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 10Z_20 * coset of 5Z_25) |
| 4, 20, 50 | 12 20 21 | 8 | 14 | 14 | 14 | a programme | LB < least = U | 14: (coset of 10Z_20 * (coset of 25Z_50 + coset of 10Z_50)) |
| 4, 20, 100 | 20 21 22 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 50Z_100 |
| 4, 25, 50 | 02 12 20 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 2Z_4 * coset of 10Z_50) |
| 4, 25, 100 | 02 20 22 | 10 | 20 | 20 | 20 | a programme | LB < least = U | 20: ((coset of 5Z_25 * coset of 50Z_100) + (coset of 2Z_4 * coset of 20Z_100)) |
| 4, 50, 100 | 12 20 22 | 10 | 14 | 14 | 14 | a programme | LB < least = U | 14: (coset of 25Z_100 + (coset of 2Z_4 * coset of 20Z_100)) |
| 5, 10, 20 | 01 11 21 | 5 | 5 | 5 | 5 | a programme and the two bounds | LB = least = U | 5: coset of 4Z_20 |
| 5, 10, 25 | 01 02 11 | 25 | 25 | 25 | 25 | a programme and the two bounds | LB = least = U | 25: (coset of 2Z_10 * coset of 5Z_25) |
| 5, 10, 50 | 01 11 12 | 35 | 35 | 35 | 35 | a programme and the two bounds | LB = least = U | 35: (coset of 2Z_10 * (coset of 25Z_50 + coset of 10Z_50)) |
| 5, 10, 100 | 01 11 22 | 10 | 35 | 35 | 35 | a programme | LB < least = U | 35: (coset of 2Z_10 * (coset of 50Z_100 + coset of 20Z_100)) |
| 5, 20, 25 | 01 02 21 | 25 | 25 | 25 | 25 | a programme and the two bounds | LB = least = U | 75: ((coset of 10Z_20 * coset of 1Z_25) + (coset of 4Z_20 * coset of 5Z_25)) |
| 5, 20, 50 | 01 12 21 | 35 |  | 60 | 60 |  | open: between 35 and 60 | 60: ((coset of 4Z_20 * coset of 25Z_50) + (coset of 1Z_5 * coset of 10Z_100)) |
| 5, 20, 100 | 01 21 22 | 30 | 35 | 35 | 35 | a programme | LB < least = U | 35: ((coset of 1Z_5 * coset of 50Z_100) + coset of 4Z_100) |
| 5, 25, 50 | 01 02 12 | 25 | 25 | 25 | 25 | a programme and the two bounds | LB = least = U | 25: (coset of 1Z_5 * coset of 10Z_50) |
| 5, 25, 100 | 01 02 22 | 25 | 50 | 50 | 50 | a programme | LB < least = U | 75: ((coset of 1Z_25 * coset of 50Z_100) + (coset of 1Z_5 * coset of 20Z_100)) |
| 5, 50, 100 | 01 12 22 | 35 | 45 | 45 | 45 | a programme | LB < least = U | 45: (coset of 1Z_5 * (coset of 25Z_100 + coset of 20Z_100)) |
| 10, 20, 25 | 02 11 21 | 35 | 45 | 45 | 45 | a programme | LB < least = U | 45: ((coset of 5Z_20 + coset of 4Z_20) * coset of 5Z_25) |
| 10, 20, 50 | 11 12 21 | 27 | 29 | 29 | 29 | a programme | LB < least = U | 29: ((coset of 10Z_20 * coset of 25Z_50) + (coset of 4Z_20 * coset of 10Z_50)) |
| 10, 20, 100 | 11 21 22 | 27 | 29 | 29 | 29 | a programme | LB < least = U | 29: ((coset of 5Z_10 * coset of 50Z_100) + coset of 4Z_100) |
| 10, 25, 50 | 02 11 12 | 35 | 35 | 35 | 35 | a programme and the two bounds | LB = least = U | 35: (coset of 5Z_50 + coset of 2Z_50) |
| 10, 25, 100 | 02 11 22 | 35 | 45 | 45 | 45 | a programme | LB < least = U | 45: ((coset of 5Z_10 * (coset of 5Z_25 * coset of 50Z_100)) + (coset of 2Z_10 * coset of 20Z_100)) |
| 10, 50, 100 | 11 12 22 | 27 | 29 | 29 | 29 | a programme | LB < least = U | 29: (coset of 25Z_100 + (coset of 2Z_10 * coset of 20Z_100)) |
| 20, 25, 50 | 02 12 21 | 10 | 35 | 35 | 35 | a programme | LB < least = U | 35: ((coset of 10Z_20 + coset of 4Z_20) * coset of 10Z_50) |
| 20, 25, 100 | 02 21 22 | 30 | 35 | 35 | 35 | a programme | LB < least = U | 35: ((coset of 5Z_25 * coset of 50Z_100) + coset of 4Z_100) |
| 20, 50, 100 | 12 21 22 | 39 | 39 | 39 | 39 | a programme and the two bounds | LB = least = U | 39: ((coset of 25Z_100 + coset of 10Z_100) + coset of 4Z_100) |
| 25, 50, 100 | 02 12 22 | 5 | 5 | 5 | 5 | a programme and the two bounds | LB = least = U | 5: coset of 20Z_100 |
| 2, 4, 5, 10 | 01 10 11 20 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 2Z_4 * coset of 1Z_10) |
| 2, 4, 5, 20 | 01 10 20 21 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_2 * (coset of 1Z_5 * coset of 10Z_20)) |
| 2, 4, 5, 25 | 01 02 10 20 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 1Z_4 * coset of 1Z_25) |
| 2, 4, 5, 50 | 01 10 12 20 | 60 | 60 | 60 | 60 | the two bounds | LB = least = U | 120: (coset of 1Z_5 * ((coset of 2Z_4 * coset of 25Z_50) + (coset of 1Z_4 * coset of 10Z_50))) |
| 2, 4, 5, 100 | 01 10 20 22 | 20 |  | 60 | 100 |  | open: between 20 and 60 | 120: (coset of 1Z_5 * ((coset of 1Z_2 * coset of 50Z_100) + (coset of 1Z_4 * coset of 20Z_100))) |
| 2, 4, 10, 20 | 10 11 20 21 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: coset of 5Z_20 |
| 2, 4, 10, 25 | 02 10 11 20 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 2Z_4 * (coset of 5Z_10 * coset of 5Z_25)) |
| 2, 4, 10, 50 | 10 11 12 20 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 2Z_4 * coset of 25Z_50) |
| 2, 4, 10, 100 | 10 11 20 22 | 8 | 24 | 24 | 24 | a programme | LB < least = U | 24: (coset of 5Z_10 * (coset of 50Z_100 + (coset of 2Z_4 * coset of 20Z_100))) |
| 2, 4, 20, 25 | 02 10 20 21 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_2 * (coset of 10Z_20 * coset of 5Z_25)) |
| 2, 4, 20, 50 | 10 12 20 21 | 12 |  | 24 | 24 |  | open: between 12 and 24 | 24: ((coset of 10Z_20 * coset of 25Z_50) + (coset of 1Z_2 * coset of 10Z_100)) |
| 2, 4, 20, 100 | 10 20 21 22 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 1Z_2 * coset of 50Z_100) |
| 2, 4, 25, 50 | 02 10 12 20 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_4 * coset of 10Z_50) |
| 2, 4, 25, 100 | 02 10 20 22 | 20 | 40 | 40 | 40 | a programme | LB < least = U | 40: (coset of 1Z_2 * ((coset of 5Z_25 * coset of 50Z_100) + (coset of 2Z_4 * coset of 20Z_100))) |
| 2, 4, 50, 100 | 10 12 20 22 | 12 | 24 | 24 | 24 | a programme | LB < least = U | 24: (coset of 25Z_100 + (coset of 1Z_4 * coset of 20Z_100)) |
| 2, 5, 10, 20 | 01 10 11 21 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 1Z_2 * coset of 4Z_20) |
| 2, 5, 10, 25 | 01 02 10 11 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 5Z_10 * coset of 1Z_25) |
| 2, 5, 10, 50 | 01 10 11 12 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 1Z_5 * coset of 25Z_50) |
| 2, 5, 10, 100 | 01 10 11 22 | 10 |  | 70 | 70 |  | open: between 10 and 70 | 70: (coset of 1Z_10 * (coset of 50Z_100 + coset of 20Z_100)) |
| 2, 5, 20, 25 | 01 02 10 21 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 150: (coset of 1Z_2 * ((coset of 10Z_20 * coset of 1Z_25) + (coset of 4Z_20 * coset of 5Z_25))) |
| 2, 5, 20, 50 | 01 10 12 21 | 50 |  | 110 | 110 |  | open: between 50 and 110 | 110: ((coset of 4Z_20 * coset of 25Z_50) + ((coset of 1Z_2 * coset of 1Z_5) * (coset of 10Z_20 * coset of 10Z_50))) |
| 2, 5, 20, 100 | 01 10 21 22 | 30 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 1Z_2 * ((coset of 1Z_5 * coset of 50Z_100) + coset of 4Z_100)) |
| 2, 5, 25, 50 | 01 02 10 12 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 1Z_2 * (coset of 1Z_5 * coset of 10Z_50)) |
| 2, 5, 25, 100 | 01 02 10 22 | 50 | 50 | 50 | 100 | a programme | least = LB < U | 150: (coset of 1Z_2 * ((coset of 1Z_25 * coset of 50Z_100) + (coset of 1Z_5 * coset of 20Z_100))) |
| 2, 5, 50, 100 | 01 10 12 22 | 50 |  | 70 | 70 |  | open: between 50 and 70 | 70: (coset of 1Z_5 * (coset of 25Z_100 + (coset of 1Z_2 * coset of 20Z_100))) |
| 2, 10, 20, 25 | 02 10 11 21 | 20 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 10Z_20 + coset of 4Z_20) * (coset of 5Z_10 * coset of 5Z_25)) |
| 2, 10, 20, 50 | 10 11 12 21 | 14 | 14 | 14 | 14 | a programme and the two bounds | LB = least = U | 14: ((coset of 10Z_20 + coset of 4Z_20) * coset of 25Z_50) |
| 2, 10, 20, 100 | 10 11 21 22 | 28 | 54 | 54 | 54 | a programme | LB < least = U | 54: (coset of 5Z_10 * (coset of 50Z_100 + coset of 4Z_100)) |
| 2, 10, 25, 50 | 02 10 11 12 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: coset of 5Z_50 |
| 2, 10, 25, 100 | 02 10 11 22 | 10 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 5Z_10 * ((coset of 5Z_25 * coset of 50Z_100) + coset of 20Z_100)) |
| 2, 10, 50, 100 | 10 11 12 22 | 10 | 14 | 14 | 14 | a programme | LB < least = U | 14: (coset of 25Z_50 * (coset of 50Z_100 + coset of 20Z_100)) |
| 2, 20, 25, 50 | 02 10 12 21 | 20 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 10Z_20 + coset of 4Z_20) * (coset of 1Z_2 * coset of 10Z_50)) |
| 2, 20, 25, 100 | 02 10 21 22 | 30 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 1Z_2 * ((coset of 5Z_25 * coset of 50Z_100) + coset of 4Z_100)) |
| 2, 20, 50, 100 | 10 12 21 22 | 40 | 74 | 74 | 74 | a programme | LB < least = U | 74: ((coset of 25Z_100 + (coset of 1Z_2 * coset of 10Z_100)) + (coset of 1Z_2 * coset of 4Z_100)) |
| 2, 25, 50, 100 | 02 10 12 22 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 1Z_2 * coset of 20Z_100) |
| 4, 5, 10, 20 | 01 11 20 21 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: coset of 2Z_20 |
| 4, 5, 10, 25 | 01 02 11 20 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 2Z_4 * (coset of 2Z_10 * coset of 5Z_25)) |
| 4, 5, 10, 50 | 01 11 12 20 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 2Z_4 * coset of 2Z_10) * (coset of 25Z_50 + coset of 10Z_50)) |
| 4, 5, 10, 100 | 01 11 20 22 | 10 | 50 | 50 | 60 | a programme | LB < least < U | 60: (coset of 2Z_10 * (coset of 50Z_100 + (coset of 2Z_4 * coset of 20Z_100))) |
| 4, 5, 20, 25 | 01 02 20 21 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 10Z_20 * coset of 1Z_25) |
| 4, 5, 20, 50 | 01 12 20 21 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 1Z_5 * coset of 10Z_20) * (coset of 25Z_50 + coset of 10Z_50)) |
| 4, 5, 20, 100 | 01 20 21 22 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 1Z_5 * coset of 50Z_100) |
| 4, 5, 25, 50 | 01 02 12 20 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 2Z_4 * (coset of 1Z_5 * coset of 10Z_50)) |
| 4, 5, 25, 100 | 01 02 20 22 | 50 | 50 | 50 | 100 | a programme | least = LB < U | 100: (coset of 1Z_5 * ((coset of 5Z_25 * coset of 50Z_100) + (coset of 2Z_4 * coset of 20Z_100))) |
| 4, 5, 50, 100 | 01 12 20 22 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 1Z_5 * (coset of 25Z_100 + (coset of 2Z_4 * coset of 20Z_100))) |
| 4, 10, 20, 25 | 02 11 20 21 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 5Z_10 + coset of 2Z_10) * (coset of 10Z_20 * coset of 5Z_25)) |
| 4, 10, 20, 50 | 11 12 20 21 | 28 | 54 | 54 | 54 | a programme | LB < least = U | 54: (coset of 10Z_20 * (coset of 25Z_50 + coset of 2Z_50)) |
| 4, 10, 20, 100 | 11 20 21 22 | 14 | 14 | 14 | 14 | a programme and the two bounds | LB = least = U | 14: ((coset of 5Z_10 + coset of 2Z_10) * coset of 50Z_100) |
| 4, 10, 25, 50 | 02 11 12 20 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 2Z_4 * (coset of 5Z_50 + coset of 2Z_50)) |
| 4, 10, 25, 100 | 02 11 20 22 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 5Z_10 * (coset of 5Z_25 * coset of 50Z_100)) + (coset of 2Z_4 * (coset of 2Z_10 * coset of 20Z_100))) |
| 4, 10, 50, 100 | 11 12 20 22 | 28 | 54 | 54 | 54 | a programme | LB < least = U | 54: (coset of 25Z_100 + (coset of 2Z_4 * (coset of 2Z_10 * coset of 20Z_100))) |
| 4, 20, 25, 50 | 02 12 20 21 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 10Z_20 * coset of 10Z_50) |
| 4, 20, 25, 100 | 02 20 21 22 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 5Z_25 * coset of 50Z_100) |
| 4, 20, 50, 100 | 12 20 21 22 | 14 | 14 | 14 | 14 | a programme and the two bounds | LB = least = U | 14: (coset of 25Z_100 + coset of 10Z_100) |
| 4, 25, 50, 100 | 02 12 20 22 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 2Z_4 * coset of 20Z_100) |
| 5, 10, 20, 25 | 01 02 11 21 | 25 | 25 | 25 | 25 | a programme and the two bounds | LB = least = U | 25: (coset of 4Z_20 * coset of 5Z_25) |
| 5, 10, 20, 50 | 01 11 12 21 | 35 | 35 | 35 | 35 | a programme and the two bounds | LB = least = U | 35: (coset of 4Z_20 * (coset of 25Z_50 + coset of 10Z_50)) |
| 5, 10, 20, 100 | 01 11 21 22 | 30 | 35 | 35 | 35 | a programme | LB < least = U | 35: (coset of 4Z_20 * (coset of 50Z_100 + coset of 20Z_100)) |
| 5, 10, 25, 50 | 01 02 11 12 | 25 | 25 | 25 | 25 | a programme and the two bounds | LB = least = U | 25: coset of 2Z_50 |
| 5, 10, 25, 100 | 01 02 11 22 | 25 | 75 | 75 | 75 | a programme | LB < least = U | 75: (coset of 2Z_10 * ((coset of 5Z_25 * coset of 50Z_100) + coset of 20Z_100)) |
| 5, 10, 50, 100 | 01 11 12 22 | 35 | 45 | 45 | 45 | a programme | LB < least = U | 45: (coset of 2Z_10 * (coset of 25Z_100 + coset of 20Z_100)) |
| 5, 20, 25, 50 | 01 02 12 21 | 25 | 75 | 75 | 75 | a programme | LB < least = U | 75: ((coset of 4Z_20 * coset of 10Z_50) + (coset of 1Z_5 * coset of 10Z_100)) |
| 5, 20, 25, 100 | 01 02 21 22 | 50 | 75 | 75 | 75 | a programme | LB < least = U | 75: ((coset of 1Z_25 * coset of 50Z_100) + coset of 4Z_100) |
| 5, 20, 50, 100 | 01 12 21 22 | 40 | 95 | 95 | 95 | a programme | LB < least = U | 95: ((coset of 1Z_5 * (coset of 25Z_100 + coset of 10Z_100)) + coset of 4Z_100) |
| 5, 25, 50, 100 | 01 02 12 22 | 25 | 25 | 25 | 25 | a programme and the two bounds | LB = least = U | 25: (coset of 1Z_5 * coset of 20Z_100) |
| 10, 20, 25, 50 | 02 11 12 21 | 35 | 45 | 45 | 45 | a programme | LB < least = U | 45: ((coset of 5Z_20 + coset of 4Z_20) * coset of 10Z_50) |
| 10, 20, 25, 100 | 02 11 21 22 | 35 | 45 | 45 | 45 | a programme | LB < least = U | 45: ((coset of 5Z_10 * (coset of 5Z_25 * coset of 50Z_100)) + coset of 4Z_100) |
| 10, 20, 50, 100 | 11 12 21 22 | 29 | 29 | 29 | 29 | a programme and the two bounds | LB = least = U | 29: (coset of 25Z_100 + coset of 4Z_100) |
| 10, 25, 50, 100 | 02 11 12 22 | 35 | 35 | 35 | 35 | a programme and the two bounds | LB = least = U | 35: ((coset of 5Z_10 + coset of 2Z_10) * coset of 20Z_100) |
| 20, 25, 50, 100 | 02 12 21 22 | 35 | 35 | 35 | 35 | a programme and the two bounds | LB = least = U | 35: (coset of 10Z_100 + coset of 4Z_100) |
| 2, 4, 5, 10, 20 | 01 10 11 20 21 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: coset of 1Z_20 |
| 2, 4, 5, 10, 25 | 01 02 10 11 20 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 2Z_4 * (coset of 5Z_10 * coset of 1Z_25)) |
| 2, 4, 5, 10, 50 | 01 10 11 12 20 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 2Z_4 * (coset of 1Z_5 * coset of 25Z_50)) |
| 2, 4, 5, 10, 100 | 01 10 11 20 22 | 20 |  | 100 | 100 |  | open: between 20 and 100 | 120: (coset of 5Z_10 * (coset of 1Z_5 * (coset of 50Z_100 + (coset of 2Z_4 * coset of 20Z_100)))) |
| 2, 4, 5, 20, 25 | 01 02 10 20 21 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 1Z_2 * (coset of 10Z_20 * coset of 1Z_25)) |
| 2, 4, 5, 20, 50 | 01 10 12 20 21 | 60 | 100 | 100 | 120 | a programme | LB < least < U | 120: (coset of 1Z_5 * ((coset of 10Z_20 * coset of 25Z_50) + (coset of 1Z_2 * coset of 10Z_100))) |
| 2, 4, 5, 20, 100 | 01 10 20 21 22 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_2 * (coset of 1Z_5 * coset of 50Z_100)) |
| 2, 4, 5, 25, 50 | 01 02 10 12 20 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 1Z_4 * (coset of 1Z_5 * coset of 10Z_50)) |
| 2, 4, 5, 25, 100 | 01 02 10 20 22 | 100 | 100 | 100 | 200 | a programme | least = LB < U | 200: (coset of 1Z_5 * (coset of 1Z_2 * ((coset of 5Z_25 * coset of 50Z_100) + (coset of 2Z_4 * coset of 20Z_100)))) |
| 2, 4, 5, 50, 100 | 01 10 12 20 22 | 60 |  | 100 | 120 |  | open: between 60 and 100 | 120: (coset of 1Z_5 * (coset of 25Z_100 + (coset of 1Z_4 * coset of 20Z_100))) |
| 2, 4, 10, 20, 25 | 02 10 11 20 21 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 5Z_20 * coset of 5Z_25) |
| 2, 4, 10, 20, 50 | 10 11 12 20 21 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 10Z_20 * coset of 25Z_50) |
| 2, 4, 10, 20, 100 | 10 11 20 21 22 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 5Z_10 * coset of 50Z_100) |
| 2, 4, 10, 25, 50 | 02 10 11 12 20 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 2Z_4 * coset of 5Z_50) |
| 2, 4, 10, 25, 100 | 02 10 11 20 22 | 20 | 40 | 40 | 40 | a programme | LB < least = U | 40: (coset of 5Z_10 * ((coset of 5Z_25 * coset of 50Z_100) + (coset of 2Z_4 * coset of 20Z_100))) |
| 2, 4, 10, 50, 100 | 10 11 12 20 22 | 12 | 24 | 24 | 24 | a programme | LB < least = U | 24: (coset of 25Z_50 * (coset of 50Z_100 + (coset of 2Z_4 * coset of 20Z_100))) |
| 2, 4, 20, 25, 50 | 02 10 12 20 21 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_2 * (coset of 10Z_20 * coset of 10Z_50)) |
| 2, 4, 20, 25, 100 | 02 10 20 21 22 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_2 * (coset of 5Z_25 * coset of 50Z_100)) |
| 2, 4, 20, 50, 100 | 10 12 20 21 22 | 16 | 24 | 24 | 24 | a programme | LB < least = U | 24: (coset of 25Z_100 + (coset of 1Z_2 * coset of 10Z_100)) |
| 2, 4, 25, 50, 100 | 02 10 12 20 22 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_4 * coset of 20Z_100) |
| 2, 5, 10, 20, 25 | 01 02 10 11 21 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 1Z_2 * (coset of 4Z_20 * coset of 5Z_25)) |
| 2, 5, 10, 20, 50 | 01 10 11 12 21 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 4Z_20 * coset of 25Z_50) |
| 2, 5, 10, 20, 100 | 01 10 11 21 22 | 30 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 1Z_2 * coset of 4Z_20) * (coset of 50Z_100 + coset of 20Z_100)) |
| 2, 5, 10, 25, 50 | 01 02 10 11 12 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: coset of 1Z_50 |
| 2, 5, 10, 25, 100 | 01 02 10 11 22 | 50 | 100 | 100 | 100 | a programme | LB < least = U | 150: (coset of 5Z_10 * ((coset of 1Z_25 * coset of 50Z_100) + (coset of 1Z_5 * coset of 20Z_100))) |
| 2, 5, 10, 50, 100 | 01 10 11 12 22 | 10 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 1Z_5 * coset of 25Z_50) * (coset of 50Z_100 + coset of 20Z_100)) |
| 2, 5, 20, 25, 50 | 01 02 10 12 21 | 50 |  | 150 | 150 |  | open: between 50 and 150 | 150: (coset of 1Z_2 * ((coset of 4Z_20 * coset of 10Z_50) + (coset of 1Z_5 * coset of 10Z_100))) |
| 2, 5, 20, 25, 100 | 01 02 10 21 22 | 50 | 150 | 150 | 150 | a programme | LB < least = U | 150: (coset of 1Z_2 * ((coset of 1Z_25 * coset of 50Z_100) + coset of 4Z_100)) |
| 2, 5, 20, 50, 100 | 01 10 12 21 22 | 50 |  | 150 | 170 |  | open: between 50 and 150 | 170: ((coset of 1Z_5 * (coset of 25Z_100 + (coset of 1Z_2 * coset of 10Z_100))) + (coset of 1Z_2 * coset of 4Z_100)) |
| 2, 5, 25, 50, 100 | 01 02 10 12 22 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 1Z_2 * (coset of 1Z_5 * coset of 20Z_100)) |
| 2, 10, 20, 25, 50 | 02 10 11 12 21 | 20 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 10Z_20 + coset of 4Z_20) * coset of 5Z_50) |
| 2, 10, 20, 25, 100 | 02 10 11 21 22 | 30 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 5Z_10 * ((coset of 5Z_25 * coset of 50Z_100) + coset of 4Z_100)) |
| 2, 10, 20, 50, 100 | 10 11 12 21 22 | 30 | 54 | 54 | 54 | a programme | LB < least = U | 54: (coset of 25Z_50 * (coset of 50Z_100 + coset of 4Z_100)) |
| 2, 10, 25, 50, 100 | 02 10 11 12 22 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 5Z_10 * coset of 20Z_100) |
| 2, 20, 25, 50, 100 | 02 10 12 21 22 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 1Z_2 * (coset of 10Z_100 + coset of 4Z_100)) |
| 4, 5, 10, 20, 25 | 01 02 11 20 21 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 2Z_20 * coset of 5Z_25) |
| 4, 5, 10, 20, 50 | 01 11 12 20 21 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 2Z_20 * (coset of 25Z_50 + coset of 10Z_50)) |
| 4, 5, 10, 20, 100 | 01 11 20 21 22 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 2Z_10 * coset of 50Z_100) |
| 4, 5, 10, 25, 50 | 01 02 11 12 20 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 2Z_4 * coset of 2Z_50) |
| 4, 5, 10, 25, 100 | 01 02 11 20 22 | 50 | 100 | 100 | 100 | a programme | LB < least = U | 100: (coset of 2Z_10 * ((coset of 5Z_25 * coset of 50Z_100) + (coset of 2Z_4 * coset of 20Z_100))) |
| 4, 5, 10, 50, 100 | 01 11 12 20 22 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 2Z_10 * (coset of 25Z_100 + (coset of 2Z_4 * coset of 20Z_100))) |
| 4, 5, 20, 25, 50 | 01 02 12 20 21 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 1Z_5 * (coset of 10Z_20 * coset of 10Z_50)) |
| 4, 5, 20, 25, 100 | 01 02 20 21 22 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 1Z_25 * coset of 50Z_100) |
| 4, 5, 20, 50, 100 | 01 12 20 21 22 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 1Z_5 * (coset of 25Z_100 + coset of 10Z_100)) |
| 4, 5, 25, 50, 100 | 01 02 12 20 22 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 2Z_4 * (coset of 1Z_5 * coset of 20Z_100)) |
| 4, 10, 20, 25, 50 | 02 11 12 20 21 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 5Z_10 + coset of 2Z_10) * (coset of 10Z_20 * coset of 10Z_50)) |
| 4, 10, 20, 25, 100 | 02 11 20 21 22 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 5Z_10 + coset of 2Z_10) * (coset of 5Z_25 * coset of 50Z_100)) |
| 4, 10, 20, 50, 100 | 11 12 20 21 22 | 54 | 54 | 54 | 54 | a programme and the two bounds | LB = least = U | 54: (coset of 25Z_100 + coset of 2Z_100) |
| 4, 10, 25, 50, 100 | 02 11 12 20 22 | 40 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 5Z_10 + coset of 2Z_10) * (coset of 2Z_4 * coset of 20Z_100)) |
| 4, 20, 25, 50, 100 | 02 12 20 21 22 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: coset of 10Z_100 |
| 5, 10, 20, 25, 50 | 01 02 11 12 21 | 25 | 25 | 25 | 25 | a programme and the two bounds | LB = least = U | 25: (coset of 4Z_20 * coset of 10Z_50) |
| 5, 10, 20, 25, 100 | 01 02 11 21 22 | 50 | 75 | 75 | 75 | a programme | LB < least = U | 75: (coset of 4Z_20 * ((coset of 5Z_25 * coset of 50Z_100) + coset of 20Z_100)) |
| 5, 10, 20, 50, 100 | 01 11 12 21 22 | 35 | 45 | 45 | 45 | a programme | LB < least = U | 45: (coset of 4Z_20 * (coset of 25Z_100 + coset of 20Z_100)) |
| 5, 10, 25, 50, 100 | 01 02 11 12 22 | 25 | 25 | 25 | 25 | a programme and the two bounds | LB = least = U | 25: (coset of 2Z_10 * coset of 20Z_100) |
| 5, 20, 25, 50, 100 | 01 02 12 21 22 | 50 | 75 | 75 | 75 | a programme | LB < least = U | 75: ((coset of 1Z_5 * coset of 10Z_100) + coset of 4Z_100) |
| 10, 20, 25, 50, 100 | 02 11 12 21 22 | 45 | 45 | 45 | 45 | a programme and the two bounds | LB = least = U | 45: (coset of 5Z_100 + coset of 4Z_100) |
| 2, 4, 5, 10, 20, 25 | 01 02 10 11 20 21 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 5Z_20 * coset of 1Z_25) |
| 2, 4, 5, 10, 20, 50 | 01 10 11 12 20 21 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 2Z_20 * coset of 25Z_50) |
| 2, 4, 5, 10, 20, 100 | 01 10 11 20 21 22 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_10 * coset of 50Z_100) |
| 2, 4, 5, 10, 25, 50 | 01 02 10 11 12 20 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 2Z_4 * coset of 1Z_50) |
| 2, 4, 5, 10, 25, 100 | 01 02 10 11 20 22 | 100 | 100 | 100 | 200 | a programme | least = LB < U | 200: (coset of 5Z_10 * (coset of 1Z_5 * ((coset of 5Z_25 * coset of 50Z_100) + (coset of 2Z_4 * coset of 20Z_100)))) |
| 2, 4, 5, 10, 50, 100 | 01 10 11 12 20 22 | 20 | 100 | 100 | 120 | a programme | LB < least < U | 120: (coset of 2Z_10 * (coset of 25Z_100 + (coset of 1Z_4 * coset of 20Z_100))) |
| 2, 4, 5, 20, 25, 50 | 01 02 10 12 20 21 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: ((coset of 1Z_2 * coset of 1Z_5) * (coset of 10Z_20 * coset of 10Z_50)) |
| 2, 4, 5, 20, 25, 100 | 01 02 10 20 21 22 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 1Z_2 * (coset of 1Z_25 * coset of 50Z_100)) |
| 2, 4, 5, 20, 50, 100 | 01 10 12 20 21 22 | 60 | 100 | 100 | 120 | a programme | LB < least < U | 120: (coset of 1Z_5 * (coset of 25Z_100 + (coset of 1Z_2 * coset of 10Z_100))) |
| 2, 4, 5, 25, 50, 100 | 01 02 10 12 20 22 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 1Z_4 * (coset of 1Z_5 * coset of 20Z_100)) |
| 2, 4, 10, 20, 25, 50 | 02 10 11 12 20 21 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 10Z_20 * coset of 5Z_50) |
| 2, 4, 10, 20, 25, 100 | 02 10 11 20 21 22 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 5Z_10 * (coset of 5Z_25 * coset of 50Z_100)) |
| 2, 4, 10, 20, 50, 100 | 10 11 12 20 21 22 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: coset of 25Z_100 |
| 2, 4, 10, 25, 50, 100 | 02 10 11 12 20 22 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 2Z_4 * (coset of 5Z_10 * coset of 20Z_100)) |
| 2, 4, 20, 25, 50, 100 | 02 10 12 20 21 22 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_2 * coset of 10Z_100) |
| 2, 5, 10, 20, 25, 50 | 01 02 10 11 12 21 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 4Z_20 * coset of 5Z_50) |
| 2, 5, 10, 20, 25, 100 | 01 02 10 11 21 22 | 50 | 150 | 150 | 150 | a programme | LB < least = U | 150: (coset of 5Z_10 * ((coset of 1Z_25 * coset of 50Z_100) + coset of 4Z_100)) |
| 2, 5, 10, 20, 50, 100 | 01 10 11 12 21 22 | 30 | 70 | 70 | 70 | a programme | LB < least = U | 70: ((coset of 4Z_20 * coset of 25Z_50) * (coset of 50Z_100 + coset of 20Z_100)) |
| 2, 5, 10, 25, 50, 100 | 01 02 10 11 12 22 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 1Z_10 * coset of 20Z_100) |
| 2, 5, 20, 25, 50, 100 | 01 02 10 12 21 22 | 50 | 150 | 150 | 150 | a programme | LB < least = U | 150: (coset of 1Z_2 * ((coset of 1Z_5 * coset of 10Z_100) + coset of 4Z_100)) |
| 2, 10, 20, 25, 50, 100 | 02 10 11 12 21 22 | 50 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 5Z_10 * (coset of 10Z_100 + coset of 4Z_100)) |
| 4, 5, 10, 20, 25, 50 | 01 02 11 12 20 21 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 10Z_20 * coset of 2Z_50) |
| 4, 5, 10, 20, 25, 100 | 01 02 11 20 21 22 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 2Z_10 * (coset of 5Z_25 * coset of 50Z_100)) |
| 4, 5, 10, 20, 50, 100 | 01 11 12 20 21 22 | 60 | 70 | 70 | 70 | a programme | LB < least = U | 70: (coset of 2Z_10 * (coset of 25Z_100 + coset of 10Z_100)) |
| 4, 5, 10, 25, 50, 100 | 01 02 11 12 20 22 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 2Z_4 * (coset of 2Z_10 * coset of 20Z_100)) |
| 4, 5, 20, 25, 50, 100 | 01 02 12 20 21 22 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 1Z_5 * coset of 10Z_100) |
| 4, 10, 20, 25, 50, 100 | 02 11 12 20 21 22 | 70 | 70 | 70 | 70 | a programme and the two bounds | LB = least = U | 70: (coset of 5Z_100 + coset of 2Z_100) |
| 5, 10, 20, 25, 50, 100 | 01 02 11 12 21 22 | 25 | 25 | 25 | 25 | a programme and the two bounds | LB = least = U | 25: coset of 4Z_100 |
| 2, 4, 5, 10, 20, 25, 50 | 01 02 10 11 12 20 21 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 10Z_20 * coset of 1Z_50) |
| 2, 4, 5, 10, 20, 25, 100 | 01 02 10 11 20 21 22 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 5Z_10 * (coset of 1Z_25 * coset of 50Z_100)) |
| 2, 4, 5, 10, 20, 50, 100 | 01 10 11 12 20 21 22 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: (coset of 1Z_5 * coset of 25Z_100) |
| 2, 4, 5, 10, 25, 50, 100 | 01 02 10 11 12 20 22 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 2Z_4 * (coset of 1Z_10 * coset of 20Z_100)) |
| 2, 4, 5, 20, 25, 50, 100 | 01 02 10 12 20 21 22 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: (coset of 1Z_2 * (coset of 1Z_5 * coset of 10Z_100)) |
| 2, 4, 10, 20, 25, 50, 100 | 02 10 11 12 20 21 22 | 20 | 20 | 20 | 20 | a programme and the two bounds | LB = least = U | 20: coset of 5Z_100 |
| 2, 5, 10, 20, 25, 50, 100 | 01 02 10 11 12 21 22 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: (coset of 1Z_2 * coset of 4Z_100) |
| 4, 5, 10, 20, 25, 50, 100 | 01 02 11 12 20 21 22 | 50 | 50 | 50 | 50 | a programme and the two bounds | LB = least = U | 50: coset of 2Z_100 |
| 2, 4, 5, 10, 20, 25, 50, 100 | 01 02 10 11 12 20 21 22 | 100 | 100 | 100 | 100 | a programme and the two bounds | LB = least = U | 100: coset of 1Z_100 |
