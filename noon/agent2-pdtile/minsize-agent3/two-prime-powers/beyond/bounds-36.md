*[Added to the public copy: Written by Yonder, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. It is in Noon's pages because the work was joint.]*

# Z_36 = 2²·3²: every pattern between two bounds that need no solver

*Made by `status.py`. 'exponents' writes the pattern as pairs uv for the divisors 2^u·3^v. LB is the lower bound of `lowerbound.py` (the two theorems and divisibility). U is the least size of a multiset built by the six moves of the note (`algebra2.py`, `algebra3.py`) and checked to have exactly the pattern (`realise2.py`, `realise3.py`). 'smallest known' is the smaller of U and what a programme found. The least size is given where it is known: proved by a programme, or because LB equals the smallest size known. The last column gives the bound from the first three moves alone (`algebra.py`) and an expression of that cost: `coset of cZ_N` is a coset of cZ_N lifted to Z_M, `*` is convolution, `+` is a sum of translates, `[...] mod N` is reduction modulo N followed by a lift.*

| pattern | exponents | LB | least size | smallest known | U | least size known by | where it sits | three moves alone: cost and expression |
|---|---|---|---|---|---|---|---|---|
| (none) | (none) | 1 | 1 | 1 | 1 | a programme and the two bounds | LB = least = U | 1: coset of 1Z_1 |
| 2 | 10 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 1Z_2 |
| 3 | 01 | 3 | 3 | 3 | 3 | a programme and the two bounds | LB = least = U | 3: coset of 1Z_3 |
| 4 | 20 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 2Z_4 |
| 6 | 11 | 5 | 5 | 5 | 5 | a programme and the two bounds | LB = least = U | 5: (coset of 3Z_6 + coset of 2Z_6) |
| 9 | 02 | 3 | 3 | 3 | 3 | a programme and the two bounds | LB = least = U | 3: coset of 3Z_9 |
| 12 | 21 | 5 | 5 | 5 | 5 | a programme and the two bounds | LB = least = U | 5: (coset of 6Z_12 + coset of 4Z_12) |
| 18 | 12 | 5 | 5 | 5 | 5 | a programme and the two bounds | LB = least = U | 5: (coset of 9Z_18 + coset of 6Z_18) |
| 36 | 22 | 5 | 5 | 5 | 5 | a programme and the two bounds | LB = least = U | 5: (coset of 18Z_36 + coset of 12Z_36) |
| 2, 3 | 01 10 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 1Z_2 * coset of 1Z_3) |
| 2, 4 | 10 20 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: coset of 1Z_4 |
| 2, 6 | 10 11 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 3Z_6 |
| 2, 9 | 02 10 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 1Z_2 * coset of 3Z_9) |
| 2, 12 | 10 21 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 1Z_2 * (coset of 6Z_12 + coset of 4Z_12)) |
| 2, 18 | 10 12 | 8 | 8 | 8 | 8 | a programme and the two bounds | LB = least = U | 8: (coset of 9Z_18 + (coset of 1Z_2 * coset of 6Z_18)) |
| 2, 36 | 10 22 | 6 | 10 | 10 | 10 | a programme | LB < least = U | 10: (coset of 1Z_2 * (coset of 18Z_36 + coset of 12Z_36)) |
| 3, 4 | 01 20 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 1Z_3 * coset of 2Z_4) |
| 3, 6 | 01 11 | 3 | 3 | 3 | 3 | a programme and the two bounds | LB = least = U | 3: coset of 2Z_6 |
| 3, 9 | 01 02 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: coset of 1Z_9 |
| 3, 12 | 01 21 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: ((coset of 1Z_3 * coset of 6Z_12) + coset of 4Z_12) |
| 3, 18 | 01 12 | 15 | 15 | 15 | 15 | a programme and the two bounds | LB = least = U | 15: (coset of 1Z_3 * (coset of 9Z_18 + coset of 6Z_18)) |
| 3, 36 | 01 22 | 6 | 15 | 15 | 15 | a programme | LB < least = U | 15: (coset of 1Z_3 * (coset of 18Z_36 + coset of 12Z_36)) |
| 4, 6 | 11 20 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 2Z_4 * (coset of 3Z_6 + coset of 2Z_6)) |
| 4, 9 | 02 20 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 2Z_4 * coset of 3Z_9) |
| 4, 12 | 20 21 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 6Z_12 |
| 4, 18 | 12 20 | 6 | 10 | 10 | 10 | a programme | LB < least = U | 10: (coset of 2Z_4 * (coset of 9Z_18 + coset of 6Z_18)) |
| 4, 36 | 20 22 | 6 | 8 | 8 | 8 | a programme | LB < least = U | 8: (coset of 18Z_36 + (coset of 2Z_4 * coset of 12Z_36)) |
| 6, 9 | 02 11 | 15 | 15 | 15 | 15 | a programme and the two bounds | LB = least = U | 15: ((coset of 3Z_6 + coset of 2Z_6) * coset of 3Z_9) |
| 6, 12 | 11 21 | 7 | 7 | 7 | 7 | a programme and the two bounds | LB = least = U | 7: (coset of 4Z_12 + coset of 3Z_12) |
| 6, 18 | 11 12 | 11 | 11 | 11 | 11 | a programme and the two bounds | LB = least = U | 11: (coset of 9Z_18 + coset of 2Z_18) |
| 6, 36 | 11 22 | 5 | 12 | 12 | 12 | a programme | LB < least = U | 12: ((coset of 2Z_6 * coset of 18Z_36) + (coset of 3Z_6 * coset of 12Z_36)) |
| 9, 12 | 02 21 | 6 | 15 | 15 | 15 | a programme | LB < least = U | 15: (coset of 3Z_9 * (coset of 6Z_12 + coset of 4Z_12)) |
| 9, 18 | 02 12 | 3 | 3 | 3 | 3 | a programme and the two bounds | LB = least = U | 3: coset of 6Z_18 |
| 9, 36 | 02 22 | 6 | 9 | 9 | 9 | a programme | LB < least = U | 9: ((coset of 3Z_9 * coset of 18Z_36) + coset of 12Z_36) |
| 12, 18 | 12 21 | 5 | 11 | 11 | 12 | a programme | LB < least < U | 12: ((coset of 4Z_12 * coset of 9Z_18) + (coset of 6Z_12 * coset of 6Z_18)) |
| 12, 36 | 21 22 | 11 | 11 | 11 | 11 | a programme and the two bounds | LB = least = U | 11: (coset of 18Z_36 + coset of 4Z_36) |
| 18, 36 | 12 22 | 7 | 7 | 7 | 7 | a programme and the two bounds | LB = least = U | 7: (coset of 12Z_36 + coset of 9Z_36) |
| 2, 3, 4 | 01 10 20 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_3 * coset of 1Z_4) |
| 2, 3, 6 | 01 10 11 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: coset of 1Z_6 |
| 2, 3, 9 | 01 02 10 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_2 * coset of 1Z_9) |
| 2, 3, 12 | 01 10 21 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_2 * ((coset of 1Z_3 * coset of 6Z_12) + coset of 4Z_12)) |
| 2, 3, 18 | 01 10 12 | 18 | 18 | 18 | 24 | a programme | least = LB < U | 24: (coset of 1Z_3 * (coset of 9Z_18 + (coset of 1Z_2 * coset of 6Z_18))) |
| 2, 3, 36 | 01 10 22 | 6 | 18 | 18 | 30 | a programme | LB < least < U | 30: ((coset of 1Z_2 * coset of 1Z_3) * (coset of 18Z_36 + coset of 12Z_36)) |
| 2, 4, 6 | 10 11 20 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 2Z_4 * coset of 3Z_6) |
| 2, 4, 9 | 02 10 20 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_4 * coset of 3Z_9) |
| 2, 4, 12 | 10 20 21 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 1Z_2 * coset of 6Z_12) |
| 2, 4, 18 | 10 12 20 | 8 | 8 | 8 | 8 | a programme and the two bounds | LB = least = U | 16: ((coset of 2Z_4 * coset of 9Z_18) + (coset of 1Z_4 * coset of 6Z_18)) |
| 2, 4, 36 | 10 20 22 | 8 | 12 | 12 | 12 | a programme | LB < least = U | 16: ((coset of 1Z_2 * coset of 18Z_36) + (coset of 1Z_4 * coset of 12Z_36)) |
| 2, 6, 9 | 02 10 11 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 3Z_6 * coset of 3Z_9) |
| 2, 6, 12 | 10 11 21 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 3Z_6 * (coset of 6Z_12 + coset of 4Z_12)) |
| 2, 6, 18 | 10 11 12 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 9Z_18 |
| 2, 6, 36 | 10 11 22 | 6 | 10 | 10 | 10 | a programme | LB < least = U | 10: (coset of 3Z_6 * (coset of 18Z_36 + coset of 12Z_36)) |
| 2, 9, 12 | 02 10 21 | 12 | 24 | 24 | 30 | a programme | LB < least < U | 30: ((coset of 1Z_2 * coset of 3Z_9) * (coset of 6Z_12 + coset of 4Z_12)) |
| 2, 9, 18 | 02 10 12 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 1Z_2 * coset of 6Z_18) |
| 2, 9, 36 | 02 10 22 | 6 | 18 | 18 | 18 | a programme | LB < least = U | 18: (coset of 1Z_2 * ((coset of 3Z_9 * coset of 18Z_36) + coset of 12Z_36)) |
| 2, 12, 18 | 10 12 21 | 10 | 18 | 18 | 18 | a programme | LB < least = U | 18: ((coset of 4Z_12 * coset of 9Z_18) + (coset of 1Z_2 * coset of 6Z_36)) |
| 2, 12, 36 | 10 21 22 | 12 | 22 | 22 | 22 | a programme | LB < least = U | 22: (coset of 1Z_2 * (coset of 18Z_36 + coset of 4Z_36)) |
| 2, 18, 36 | 10 12 22 | 8 | 10 | 10 | 10 | a programme | LB < least = U | 10: ((coset of 1Z_2 * coset of 12Z_36) + coset of 9Z_36) |
| 3, 4, 6 | 01 11 20 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 2Z_4 * coset of 2Z_6) |
| 3, 4, 9 | 01 02 20 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 2Z_4 * coset of 1Z_9) |
| 3, 4, 12 | 01 20 21 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 1Z_3 * coset of 6Z_12) |
| 3, 4, 18 | 01 12 20 | 18 | 18 | 18 | 30 | a programme | least = LB < U | 30: ((coset of 1Z_3 * coset of 2Z_4) * (coset of 9Z_18 + coset of 6Z_18)) |
| 3, 4, 36 | 01 20 22 | 6 | 18 | 18 | 24 | a programme | LB < least < U | 24: (coset of 1Z_3 * (coset of 18Z_36 + (coset of 2Z_4 * coset of 12Z_36))) |
| 3, 6, 9 | 01 02 11 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: (coset of 2Z_6 * coset of 3Z_9) |
| 3, 6, 12 | 01 11 21 | 3 | 3 | 3 | 3 | a programme and the two bounds | LB = least = U | 3: coset of 4Z_12 |
| 3, 6, 18 | 01 11 12 | 15 | 15 | 15 | 15 | a programme and the two bounds | LB = least = U | 15: (coset of 2Z_6 * (coset of 9Z_18 + coset of 6Z_18)) |
| 3, 6, 36 | 01 11 22 | 6 | 15 | 15 | 15 | a programme | LB < least = U | 15: (coset of 2Z_6 * (coset of 18Z_36 + coset of 12Z_36)) |
| 3, 9, 12 | 01 02 21 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 27: ((coset of 1Z_9 * coset of 6Z_12) + (coset of 3Z_9 * coset of 4Z_12)) |
| 3, 9, 18 | 01 02 12 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: (coset of 1Z_3 * coset of 6Z_18) |
| 3, 9, 36 | 01 02 22 | 9 | 18 | 18 | 18 | a programme | LB < least = U | 27: ((coset of 1Z_9 * coset of 18Z_36) + (coset of 1Z_3 * coset of 12Z_36)) |
| 3, 12, 18 | 01 12 21 | 15 | 24 | 24 | 24 | a programme | LB < least = U | 24: ((coset of 4Z_12 * coset of 9Z_18) + (coset of 1Z_3 * coset of 6Z_36)) |
| 3, 12, 36 | 01 21 22 | 12 | 15 | 15 | 15 | a programme | LB < least = U | 15: ((coset of 1Z_3 * coset of 18Z_36) + coset of 4Z_36) |
| 3, 18, 36 | 01 12 22 | 15 | 21 | 21 | 21 | a programme | LB < least = U | 21: (coset of 1Z_3 * (coset of 12Z_36 + coset of 9Z_36)) |
| 4, 6, 9 | 02 11 20 | 18 | 24 | 24 | 30 | a programme | LB < least < U | 30: ((coset of 3Z_6 + coset of 2Z_6) * (coset of 2Z_4 * coset of 3Z_9)) |
| 4, 6, 12 | 11 20 21 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 3Z_12 + coset of 2Z_12) |
| 4, 6, 18 | 11 12 20 | 12 | 22 | 22 | 22 | a programme | LB < least = U | 22: (coset of 2Z_4 * (coset of 9Z_18 + coset of 2Z_18)) |
| 4, 6, 36 | 11 20 22 | 10 | 18 | 18 | 18 | a programme | LB < least = U | 18: ((coset of 2Z_6 * coset of 18Z_36) + (coset of 2Z_4 * (coset of 3Z_6 * coset of 12Z_36))) |
| 4, 9, 12 | 02 20 21 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 3Z_9 * coset of 6Z_12) |
| 4, 9, 18 | 02 12 20 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 2Z_4 * coset of 6Z_18) |
| 4, 9, 36 | 02 20 22 | 6 | 12 | 12 | 12 | a programme | LB < least = U | 12: ((coset of 3Z_9 * coset of 18Z_36) + (coset of 2Z_4 * coset of 12Z_36)) |
| 4, 12, 18 | 12 20 21 | 6 | 10 | 10 | 10 | a programme | LB < least = U | 10: (coset of 6Z_12 * (coset of 9Z_18 + coset of 6Z_18)) |
| 4, 12, 36 | 20 21 22 | 2 | 2 | 2 | 2 | a programme and the two bounds | LB = least = U | 2: coset of 18Z_36 |
| 4, 18, 36 | 12 20 22 | 8 | 10 | 10 | 10 | a programme | LB < least = U | 10: ((coset of 2Z_4 * coset of 12Z_36) + coset of 9Z_36) |
| 6, 9, 12 | 02 11 21 | 15 | 21 | 21 | 21 | a programme | LB < least = U | 21: (coset of 3Z_9 * (coset of 4Z_12 + coset of 3Z_12)) |
| 6, 9, 18 | 02 11 12 | 15 | 15 | 15 | 15 | a programme and the two bounds | LB = least = U | 15: (coset of 3Z_18 + coset of 2Z_18) |
| 6, 9, 36 | 02 11 22 | 15 | 21 | 21 | 21 | a programme | LB < least = U | 21: ((coset of 3Z_6 * (coset of 3Z_9 * coset of 18Z_36)) + (coset of 2Z_6 * coset of 12Z_36)) |
| 6, 12, 18 | 11 12 21 | 11 | 13 | 13 | 13 | a programme | LB < least = U | 13: ((coset of 6Z_12 * coset of 9Z_18) + (coset of 4Z_12 * coset of 6Z_18)) |
| 6, 12, 36 | 11 21 22 | 11 | 13 | 13 | 13 | a programme | LB < least = U | 13: ((coset of 3Z_6 * coset of 18Z_36) + coset of 4Z_36) |
| 6, 18, 36 | 11 12 22 | 11 | 13 | 13 | 13 | a programme | LB < least = U | 13: ((coset of 2Z_6 * coset of 12Z_36) + coset of 9Z_36) |
| 9, 12, 18 | 02 12 21 | 6 | 15 | 15 | 15 | a programme | LB < least = U | 15: ((coset of 6Z_12 + coset of 4Z_12) * coset of 6Z_18) |
| 9, 12, 36 | 02 21 22 | 12 | 15 | 15 | 15 | a programme | LB < least = U | 15: ((coset of 3Z_9 * coset of 18Z_36) + coset of 4Z_36) |
| 9, 18, 36 | 02 12 22 | 3 | 3 | 3 | 3 | a programme and the two bounds | LB = least = U | 3: coset of 12Z_36 |
| 12, 18, 36 | 12 21 22 | 19 | 19 | 19 | 19 | a programme and the two bounds | LB = least = U | 19: ((coset of 9Z_36 + coset of 6Z_36) + coset of 4Z_36) |
| 2, 3, 4, 6 | 01 10 11 20 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 2Z_4 * coset of 1Z_6) |
| 2, 3, 4, 9 | 01 02 10 20 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 1Z_4 * coset of 1Z_9) |
| 2, 3, 4, 12 | 01 10 20 21 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_2 * (coset of 1Z_3 * coset of 6Z_12)) |
| 2, 3, 4, 18 | 01 10 12 20 | 24 | 24 | 24 | 24 | a programme and the two bounds | LB = least = U | 48: (coset of 1Z_3 * ((coset of 2Z_4 * coset of 9Z_18) + (coset of 1Z_4 * coset of 6Z_18))) |
| 2, 3, 4, 36 | 01 10 20 22 | 12 | 24 | 24 | 36 | a programme | LB < least < U | 48: (coset of 1Z_3 * ((coset of 1Z_2 * coset of 18Z_36) + (coset of 1Z_4 * coset of 12Z_36))) |
| 2, 3, 6, 9 | 01 02 10 11 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 3Z_6 * coset of 1Z_9) |
| 2, 3, 6, 12 | 01 10 11 21 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 1Z_2 * coset of 4Z_12) |
| 2, 3, 6, 18 | 01 10 11 12 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 1Z_3 * coset of 9Z_18) |
| 2, 3, 6, 36 | 01 10 11 22 | 6 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 1Z_6 * (coset of 18Z_36 + coset of 12Z_36)) |
| 2, 3, 9, 12 | 01 02 10 21 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 54: (coset of 1Z_2 * ((coset of 1Z_9 * coset of 6Z_12) + (coset of 3Z_9 * coset of 4Z_12))) |
| 2, 3, 9, 18 | 01 02 10 12 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_2 * (coset of 1Z_3 * coset of 6Z_18)) |
| 2, 3, 9, 36 | 01 02 10 22 | 18 | 18 | 18 | 36 | a programme | least = LB < U | 54: (coset of 1Z_2 * ((coset of 1Z_9 * coset of 18Z_36) + (coset of 1Z_3 * coset of 12Z_36))) |
| 2, 3, 12, 18 | 01 10 12 21 | 18 | 42 | 42 | 42 | a programme | LB < least = U | 42: ((coset of 4Z_12 * coset of 9Z_18) + ((coset of 1Z_2 * coset of 1Z_3) * (coset of 6Z_12 * coset of 6Z_18))) |
| 2, 3, 12, 36 | 01 10 21 22 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 1Z_2 * ((coset of 1Z_3 * coset of 18Z_36) + coset of 4Z_36)) |
| 2, 3, 18, 36 | 01 10 12 22 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 1Z_3 * ((coset of 1Z_2 * coset of 12Z_36) + coset of 9Z_36)) |
| 2, 4, 6, 9 | 02 10 11 20 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 2Z_4 * (coset of 3Z_6 * coset of 3Z_9)) |
| 2, 4, 6, 12 | 10 11 20 21 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: coset of 3Z_12 |
| 2, 4, 6, 18 | 10 11 12 20 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 2Z_4 * coset of 9Z_18) |
| 2, 4, 6, 36 | 10 11 20 22 | 8 | 16 | 16 | 16 | a programme | LB < least = U | 16: (coset of 3Z_6 * (coset of 18Z_36 + (coset of 2Z_4 * coset of 12Z_36))) |
| 2, 4, 9, 12 | 02 10 20 21 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_2 * (coset of 3Z_9 * coset of 6Z_12)) |
| 2, 4, 9, 18 | 02 10 12 20 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_4 * coset of 6Z_18) |
| 2, 4, 9, 36 | 02 10 20 22 | 12 | 24 | 24 | 24 | a programme | LB < least = U | 24: (coset of 1Z_2 * ((coset of 3Z_9 * coset of 18Z_36) + (coset of 2Z_4 * coset of 12Z_36))) |
| 2, 4, 12, 18 | 10 12 20 21 | 8 | 16 | 16 | 16 | a programme | LB < least = U | 16: ((coset of 6Z_12 * coset of 9Z_18) + (coset of 1Z_2 * coset of 6Z_36)) |
| 2, 4, 12, 36 | 10 20 21 22 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 1Z_2 * coset of 18Z_36) |
| 2, 4, 18, 36 | 10 12 20 22 | 8 | 16 | 16 | 16 | a programme | LB < least = U | 16: ((coset of 1Z_4 * coset of 12Z_36) + coset of 9Z_36) |
| 2, 6, 9, 12 | 02 10 11 21 | 12 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 3Z_6 * coset of 3Z_9) * (coset of 6Z_12 + coset of 4Z_12)) |
| 2, 6, 9, 18 | 02 10 11 12 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: coset of 3Z_18 |
| 2, 6, 9, 36 | 02 10 11 22 | 6 | 18 | 18 | 18 | a programme | LB < least = U | 18: (coset of 3Z_6 * ((coset of 3Z_9 * coset of 18Z_36) + coset of 12Z_36)) |
| 2, 6, 12, 18 | 10 11 12 21 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: ((coset of 6Z_12 + coset of 4Z_12) * coset of 9Z_18) |
| 2, 6, 12, 36 | 10 11 21 22 | 12 | 22 | 22 | 22 | a programme | LB < least = U | 22: (coset of 3Z_6 * (coset of 18Z_36 + coset of 4Z_36)) |
| 2, 6, 18, 36 | 10 11 12 22 | 8 | 10 | 10 | 10 | a programme | LB < least = U | 10: (coset of 9Z_18 * (coset of 18Z_36 + coset of 12Z_36)) |
| 2, 9, 12, 18 | 02 10 12 21 | 12 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 6Z_12 + coset of 4Z_12) * (coset of 1Z_2 * coset of 6Z_18)) |
| 2, 9, 12, 36 | 02 10 21 22 | 12 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 1Z_2 * ((coset of 3Z_9 * coset of 18Z_36) + coset of 4Z_36)) |
| 2, 9, 18, 36 | 02 10 12 22 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 1Z_2 * coset of 12Z_36) |
| 2, 12, 18, 36 | 10 12 21 22 | 20 | 34 | 34 | 34 | a programme | LB < least = U | 34: ((coset of 9Z_36 + (coset of 1Z_2 * coset of 6Z_36)) + (coset of 1Z_2 * coset of 4Z_36)) |
| 3, 4, 6, 9 | 01 02 11 20 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 2Z_4 * (coset of 2Z_6 * coset of 3Z_9)) |
| 3, 4, 6, 12 | 01 11 20 21 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: coset of 2Z_12 |
| 3, 4, 6, 18 | 01 11 12 20 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 2Z_4 * coset of 2Z_6) * (coset of 9Z_18 + coset of 6Z_18)) |
| 3, 4, 6, 36 | 01 11 20 22 | 6 | 18 | 18 | 24 | a programme | LB < least < U | 24: (coset of 2Z_6 * (coset of 18Z_36 + (coset of 2Z_4 * coset of 12Z_36))) |
| 3, 4, 9, 12 | 01 02 20 21 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_9 * coset of 6Z_12) |
| 3, 4, 9, 18 | 01 02 12 20 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_3 * (coset of 2Z_4 * coset of 6Z_18)) |
| 3, 4, 9, 36 | 01 02 20 22 | 18 | 18 | 18 | 36 | a programme | least = LB < U | 36: (coset of 1Z_3 * ((coset of 3Z_9 * coset of 18Z_36) + (coset of 2Z_4 * coset of 12Z_36))) |
| 3, 4, 12, 18 | 01 12 20 21 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 1Z_3 * coset of 6Z_12) * (coset of 9Z_18 + coset of 6Z_18)) |
| 3, 4, 12, 36 | 01 20 21 22 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 1Z_3 * coset of 18Z_36) |
| 3, 4, 18, 36 | 01 12 20 22 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 1Z_3 * ((coset of 2Z_4 * coset of 12Z_36) + coset of 9Z_36)) |
| 3, 6, 9, 12 | 01 02 11 21 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: (coset of 3Z_9 * coset of 4Z_12) |
| 3, 6, 9, 18 | 01 02 11 12 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: coset of 2Z_18 |
| 3, 6, 9, 36 | 01 02 11 22 | 9 | 27 | 27 | 27 | a programme | LB < least = U | 27: (coset of 2Z_6 * ((coset of 3Z_9 * coset of 18Z_36) + coset of 12Z_36)) |
| 3, 6, 12, 18 | 01 11 12 21 | 15 | 15 | 15 | 15 | a programme and the two bounds | LB = least = U | 15: (coset of 4Z_12 * (coset of 9Z_18 + coset of 6Z_18)) |
| 3, 6, 12, 36 | 01 11 21 22 | 12 | 15 | 15 | 15 | a programme | LB < least = U | 15: (coset of 4Z_12 * (coset of 18Z_36 + coset of 12Z_36)) |
| 3, 6, 18, 36 | 01 11 12 22 | 15 | 21 | 21 | 21 | a programme | LB < least = U | 21: (coset of 2Z_6 * (coset of 12Z_36 + coset of 9Z_36)) |
| 3, 9, 12, 18 | 01 02 12 21 | 9 | 27 | 27 | 27 | a programme | LB < least = U | 27: ((coset of 4Z_12 * coset of 6Z_18) + (coset of 1Z_3 * coset of 6Z_36)) |
| 3, 9, 12, 36 | 01 02 21 22 | 18 | 27 | 27 | 27 | a programme | LB < least = U | 27: ((coset of 1Z_9 * coset of 18Z_36) + coset of 4Z_36) |
| 3, 9, 18, 36 | 01 02 12 22 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: (coset of 1Z_3 * coset of 12Z_36) |
| 3, 12, 18, 36 | 01 12 21 22 | 21 | 39 | 39 | 39 | a programme | LB < least = U | 39: ((coset of 1Z_3 * (coset of 9Z_36 + coset of 6Z_36)) + coset of 4Z_36) |
| 4, 6, 9, 12 | 02 11 20 21 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 3Z_6 + coset of 2Z_6) * (coset of 3Z_9 * coset of 6Z_12)) |
| 4, 6, 9, 18 | 02 11 12 20 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 2Z_4 * (coset of 3Z_18 + coset of 2Z_18)) |
| 4, 6, 9, 36 | 02 11 20 22 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 3Z_6 * (coset of 3Z_9 * coset of 18Z_36)) + (coset of 2Z_4 * (coset of 2Z_6 * coset of 12Z_36))) |
| 4, 6, 12, 18 | 11 12 20 21 | 12 | 22 | 22 | 22 | a programme | LB < least = U | 22: (coset of 6Z_12 * (coset of 9Z_18 + coset of 2Z_18)) |
| 4, 6, 12, 36 | 11 20 21 22 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: ((coset of 3Z_6 + coset of 2Z_6) * coset of 18Z_36) |
| 4, 6, 18, 36 | 11 12 20 22 | 12 | 22 | 22 | 22 | a programme | LB < least = U | 22: ((coset of 2Z_4 * (coset of 2Z_6 * coset of 12Z_36)) + coset of 9Z_36) |
| 4, 9, 12, 18 | 02 12 20 21 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 6Z_12 * coset of 6Z_18) |
| 4, 9, 12, 36 | 02 20 21 22 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 3Z_9 * coset of 18Z_36) |
| 4, 9, 18, 36 | 02 12 20 22 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 2Z_4 * coset of 12Z_36) |
| 4, 12, 18, 36 | 12 20 21 22 | 10 | 10 | 10 | 10 | a programme and the two bounds | LB = least = U | 10: (coset of 9Z_36 + coset of 6Z_36) |
| 6, 9, 12, 18 | 02 11 12 21 | 15 | 21 | 21 | 21 | a programme | LB < least = U | 21: ((coset of 4Z_12 + coset of 3Z_12) * coset of 6Z_18) |
| 6, 9, 12, 36 | 02 11 21 22 | 15 | 21 | 21 | 21 | a programme | LB < least = U | 21: ((coset of 3Z_6 * (coset of 3Z_9 * coset of 18Z_36)) + coset of 4Z_36) |
| 6, 9, 18, 36 | 02 11 12 22 | 15 | 15 | 15 | 15 | a programme and the two bounds | LB = least = U | 15: ((coset of 3Z_6 + coset of 2Z_6) * coset of 12Z_36) |
| 6, 12, 18, 36 | 11 12 21 22 | 13 | 13 | 13 | 13 | a programme and the two bounds | LB = least = U | 13: (coset of 9Z_36 + coset of 4Z_36) |
| 9, 12, 18, 36 | 02 12 21 22 | 15 | 15 | 15 | 15 | a programme and the two bounds | LB = least = U | 15: (coset of 6Z_36 + coset of 4Z_36) |
| 2, 3, 4, 6, 9 | 01 02 10 11 20 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 2Z_4 * (coset of 3Z_6 * coset of 1Z_9)) |
| 2, 3, 4, 6, 12 | 01 10 11 20 21 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: coset of 1Z_12 |
| 2, 3, 4, 6, 18 | 01 10 11 12 20 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_3 * (coset of 2Z_4 * coset of 9Z_18)) |
| 2, 3, 4, 6, 36 | 01 10 11 20 22 | 12 | 36 | 36 | 36 | a programme | LB < least = U | 48: (coset of 3Z_6 * (coset of 1Z_3 * (coset of 18Z_36 + (coset of 2Z_4 * coset of 12Z_36)))) |
| 2, 3, 4, 9, 12 | 01 02 10 20 21 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 1Z_2 * (coset of 1Z_9 * coset of 6Z_12)) |
| 2, 3, 4, 9, 18 | 01 02 10 12 20 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 1Z_3 * (coset of 1Z_4 * coset of 6Z_18)) |
| 2, 3, 4, 9, 36 | 01 02 10 20 22 | 36 | 36 | 36 | 72 | a programme | least = LB < U | 72: (coset of 1Z_3 * (coset of 1Z_2 * ((coset of 3Z_9 * coset of 18Z_36) + (coset of 2Z_4 * coset of 12Z_36)))) |
| 2, 3, 4, 12, 18 | 01 10 12 20 21 | 24 | 36 | 36 | 48 | a programme | LB < least < U | 48: (coset of 1Z_3 * ((coset of 6Z_12 * coset of 9Z_18) + (coset of 1Z_2 * coset of 6Z_36))) |
| 2, 3, 4, 12, 36 | 01 10 20 21 22 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_2 * (coset of 1Z_3 * coset of 18Z_36)) |
| 2, 3, 4, 18, 36 | 01 10 12 20 22 | 24 | 36 | 36 | 48 | a programme | LB < least < U | 48: (coset of 1Z_3 * ((coset of 1Z_4 * coset of 12Z_36) + coset of 9Z_36)) |
| 2, 3, 6, 9, 12 | 01 02 10 11 21 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_2 * (coset of 3Z_9 * coset of 4Z_12)) |
| 2, 3, 6, 9, 18 | 01 02 10 11 12 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: coset of 1Z_18 |
| 2, 3, 6, 9, 36 | 01 02 10 11 22 | 18 | 36 | 36 | 36 | a programme | LB < least = U | 54: (coset of 3Z_6 * ((coset of 1Z_9 * coset of 18Z_36) + (coset of 1Z_3 * coset of 12Z_36))) |
| 2, 3, 6, 12, 18 | 01 10 11 12 21 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 4Z_12 * coset of 9Z_18) |
| 2, 3, 6, 12, 36 | 01 10 11 21 22 | 12 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 1Z_2 * coset of 4Z_12) * (coset of 18Z_36 + coset of 12Z_36)) |
| 2, 3, 6, 18, 36 | 01 10 11 12 22 | 12 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 1Z_3 * coset of 9Z_18) * (coset of 18Z_36 + coset of 12Z_36)) |
| 2, 3, 9, 12, 18 | 01 02 10 12 21 | 18 | 54 | 54 | 54 | a programme | LB < least = U | 54: (coset of 1Z_2 * ((coset of 4Z_12 * coset of 6Z_18) + (coset of 1Z_3 * coset of 6Z_36))) |
| 2, 3, 9, 12, 36 | 01 02 10 21 22 | 18 | 54 | 54 | 54 | a programme | LB < least = U | 54: (coset of 1Z_2 * ((coset of 1Z_9 * coset of 18Z_36) + coset of 4Z_36)) |
| 2, 3, 9, 18, 36 | 01 02 10 12 22 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_2 * (coset of 1Z_3 * coset of 12Z_36)) |
| 2, 3, 12, 18, 36 | 01 10 12 21 22 | 24 | 54 | 54 | 66 | a programme | LB < least < U | 66: ((coset of 1Z_3 * (coset of 9Z_36 + (coset of 1Z_2 * coset of 6Z_36))) + (coset of 1Z_2 * coset of 4Z_36)) |
| 2, 4, 6, 9, 12 | 02 10 11 20 21 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 3Z_9 * coset of 3Z_12) |
| 2, 4, 6, 9, 18 | 02 10 11 12 20 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 2Z_4 * coset of 3Z_18) |
| 2, 4, 6, 9, 36 | 02 10 11 20 22 | 12 | 24 | 24 | 24 | a programme | LB < least = U | 24: (coset of 3Z_6 * ((coset of 3Z_9 * coset of 18Z_36) + (coset of 2Z_4 * coset of 12Z_36))) |
| 2, 4, 6, 12, 18 | 10 11 12 20 21 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 6Z_12 * coset of 9Z_18) |
| 2, 4, 6, 12, 36 | 10 11 20 21 22 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: (coset of 3Z_6 * coset of 18Z_36) |
| 2, 4, 6, 18, 36 | 10 11 12 20 22 | 8 | 16 | 16 | 16 | a programme | LB < least = U | 16: (coset of 9Z_18 * (coset of 18Z_36 + (coset of 2Z_4 * coset of 12Z_36))) |
| 2, 4, 9, 12, 18 | 02 10 12 20 21 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_2 * (coset of 6Z_12 * coset of 6Z_18)) |
| 2, 4, 9, 12, 36 | 02 10 20 21 22 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_2 * (coset of 3Z_9 * coset of 18Z_36)) |
| 2, 4, 9, 18, 36 | 02 10 12 20 22 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_4 * coset of 12Z_36) |
| 2, 4, 12, 18, 36 | 10 12 20 21 22 | 12 | 16 | 16 | 16 | a programme | LB < least = U | 16: (coset of 9Z_36 + (coset of 1Z_2 * coset of 6Z_36)) |
| 2, 6, 9, 12, 18 | 02 10 11 12 21 | 12 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 6Z_12 + coset of 4Z_12) * coset of 3Z_18) |
| 2, 6, 9, 12, 36 | 02 10 11 21 22 | 12 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 3Z_6 * ((coset of 3Z_9 * coset of 18Z_36) + coset of 4Z_36)) |
| 2, 6, 9, 18, 36 | 02 10 11 12 22 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 3Z_6 * coset of 12Z_36) |
| 2, 6, 12, 18, 36 | 10 11 12 21 22 | 14 | 22 | 22 | 22 | a programme | LB < least = U | 22: (coset of 9Z_18 * (coset of 18Z_36 + coset of 4Z_36)) |
| 2, 9, 12, 18, 36 | 02 10 12 21 22 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 1Z_2 * (coset of 6Z_36 + coset of 4Z_36)) |
| 3, 4, 6, 9, 12 | 01 02 11 20 21 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 3Z_9 * coset of 2Z_12) |
| 3, 4, 6, 9, 18 | 01 02 11 12 20 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 2Z_4 * coset of 2Z_18) |
| 3, 4, 6, 9, 36 | 01 02 11 20 22 | 18 | 36 | 36 | 36 | a programme | LB < least = U | 36: (coset of 2Z_6 * ((coset of 3Z_9 * coset of 18Z_36) + (coset of 2Z_4 * coset of 12Z_36))) |
| 3, 4, 6, 12, 18 | 01 11 12 20 21 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 2Z_12 * (coset of 9Z_18 + coset of 6Z_18)) |
| 3, 4, 6, 12, 36 | 01 11 20 21 22 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: (coset of 2Z_6 * coset of 18Z_36) |
| 3, 4, 6, 18, 36 | 01 11 12 20 22 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 2Z_6 * ((coset of 2Z_4 * coset of 12Z_36) + coset of 9Z_36)) |
| 3, 4, 9, 12, 18 | 01 02 12 20 21 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_3 * (coset of 6Z_12 * coset of 6Z_18)) |
| 3, 4, 9, 12, 36 | 01 02 20 21 22 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_9 * coset of 18Z_36) |
| 3, 4, 9, 18, 36 | 01 02 12 20 22 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_3 * (coset of 2Z_4 * coset of 12Z_36)) |
| 3, 4, 12, 18, 36 | 01 12 20 21 22 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 1Z_3 * (coset of 9Z_36 + coset of 6Z_36)) |
| 3, 6, 9, 12, 18 | 01 02 11 12 21 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: (coset of 4Z_12 * coset of 6Z_18) |
| 3, 6, 9, 12, 36 | 01 02 11 21 22 | 18 | 27 | 27 | 27 | a programme | LB < least = U | 27: (coset of 4Z_12 * ((coset of 3Z_9 * coset of 18Z_36) + coset of 12Z_36)) |
| 3, 6, 9, 18, 36 | 01 02 11 12 22 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: (coset of 2Z_6 * coset of 12Z_36) |
| 3, 6, 12, 18, 36 | 01 11 12 21 22 | 15 | 21 | 21 | 21 | a programme | LB < least = U | 21: (coset of 4Z_12 * (coset of 12Z_36 + coset of 9Z_36)) |
| 3, 9, 12, 18, 36 | 01 02 12 21 22 | 18 | 27 | 27 | 27 | a programme | LB < least = U | 27: ((coset of 1Z_3 * coset of 6Z_36) + coset of 4Z_36) |
| 4, 6, 9, 12, 18 | 02 11 12 20 21 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 3Z_6 + coset of 2Z_6) * (coset of 6Z_12 * coset of 6Z_18)) |
| 4, 6, 9, 12, 36 | 02 11 20 21 22 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 3Z_6 + coset of 2Z_6) * (coset of 3Z_9 * coset of 18Z_36)) |
| 4, 6, 9, 18, 36 | 02 11 12 20 22 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 3Z_6 + coset of 2Z_6) * (coset of 2Z_4 * coset of 12Z_36)) |
| 4, 6, 12, 18, 36 | 11 12 20 21 22 | 22 | 22 | 22 | 22 | a programme and the two bounds | LB = least = U | 22: (coset of 9Z_36 + coset of 2Z_36) |
| 4, 9, 12, 18, 36 | 02 12 20 21 22 | 6 | 6 | 6 | 6 | a programme and the two bounds | LB = least = U | 6: coset of 6Z_36 |
| 6, 9, 12, 18, 36 | 02 11 12 21 22 | 21 | 21 | 21 | 21 | a programme and the two bounds | LB = least = U | 21: (coset of 4Z_36 + coset of 3Z_36) |
| 2, 3, 4, 6, 9, 12 | 01 02 10 11 20 21 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 3Z_9 * coset of 1Z_12) |
| 2, 3, 4, 6, 9, 18 | 01 02 10 11 12 20 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 2Z_4 * coset of 1Z_18) |
| 2, 3, 4, 6, 9, 36 | 01 02 10 11 20 22 | 36 | 36 | 36 | 72 | a programme | least = LB < U | 72: (coset of 3Z_6 * (coset of 1Z_3 * ((coset of 3Z_9 * coset of 18Z_36) + (coset of 2Z_4 * coset of 12Z_36)))) |
| 2, 3, 4, 6, 12, 18 | 01 10 11 12 20 21 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 2Z_12 * coset of 9Z_18) |
| 2, 3, 4, 6, 12, 36 | 01 10 11 20 21 22 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_6 * coset of 18Z_36) |
| 2, 3, 4, 6, 18, 36 | 01 10 11 12 20 22 | 12 | 36 | 36 | 48 | a programme | LB < least < U | 48: (coset of 2Z_6 * ((coset of 1Z_4 * coset of 12Z_36) + coset of 9Z_36)) |
| 2, 3, 4, 9, 12, 18 | 01 02 10 12 20 21 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: ((coset of 1Z_2 * coset of 1Z_3) * (coset of 6Z_12 * coset of 6Z_18)) |
| 2, 3, 4, 9, 12, 36 | 01 02 10 20 21 22 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 1Z_2 * (coset of 1Z_9 * coset of 18Z_36)) |
| 2, 3, 4, 9, 18, 36 | 01 02 10 12 20 22 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 1Z_3 * (coset of 1Z_4 * coset of 12Z_36)) |
| 2, 3, 4, 12, 18, 36 | 01 10 12 20 21 22 | 24 | 36 | 36 | 48 | a programme | LB < least < U | 48: (coset of 1Z_3 * (coset of 9Z_36 + (coset of 1Z_2 * coset of 6Z_36))) |
| 2, 3, 6, 9, 12, 18 | 01 02 10 11 12 21 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 4Z_12 * coset of 3Z_18) |
| 2, 3, 6, 9, 12, 36 | 01 02 10 11 21 22 | 18 | 54 | 54 | 54 | a programme | LB < least = U | 54: (coset of 3Z_6 * ((coset of 1Z_9 * coset of 18Z_36) + coset of 4Z_36)) |
| 2, 3, 6, 9, 18, 36 | 01 02 10 11 12 22 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_6 * coset of 12Z_36) |
| 2, 3, 6, 12, 18, 36 | 01 10 11 12 21 22 | 18 | 30 | 30 | 30 | a programme | LB < least = U | 30: ((coset of 4Z_12 * coset of 9Z_18) * (coset of 18Z_36 + coset of 12Z_36)) |
| 2, 3, 9, 12, 18, 36 | 01 02 10 12 21 22 | 18 | 54 | 54 | 54 | a programme | LB < least = U | 54: (coset of 1Z_2 * ((coset of 1Z_3 * coset of 6Z_36) + coset of 4Z_36)) |
| 2, 4, 6, 9, 12, 18 | 02 10 11 12 20 21 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 6Z_12 * coset of 3Z_18) |
| 2, 4, 6, 9, 12, 36 | 02 10 11 20 21 22 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 3Z_6 * (coset of 3Z_9 * coset of 18Z_36)) |
| 2, 4, 6, 9, 18, 36 | 02 10 11 12 20 22 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 2Z_4 * (coset of 3Z_6 * coset of 12Z_36)) |
| 2, 4, 6, 12, 18, 36 | 10 11 12 20 21 22 | 4 | 4 | 4 | 4 | a programme and the two bounds | LB = least = U | 4: coset of 9Z_36 |
| 2, 4, 9, 12, 18, 36 | 02 10 12 20 21 22 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_2 * coset of 6Z_36) |
| 2, 6, 9, 12, 18, 36 | 02 10 11 12 21 22 | 24 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 3Z_6 * (coset of 6Z_36 + coset of 4Z_36)) |
| 3, 4, 6, 9, 12, 18 | 01 02 11 12 20 21 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 6Z_12 * coset of 2Z_18) |
| 3, 4, 6, 9, 12, 36 | 01 02 11 20 21 22 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 2Z_6 * (coset of 3Z_9 * coset of 18Z_36)) |
| 3, 4, 6, 9, 18, 36 | 01 02 11 12 20 22 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 2Z_4 * (coset of 2Z_6 * coset of 12Z_36)) |
| 3, 4, 6, 12, 18, 36 | 01 11 12 20 21 22 | 24 | 30 | 30 | 30 | a programme | LB < least = U | 30: (coset of 2Z_6 * (coset of 9Z_36 + coset of 6Z_36)) |
| 3, 4, 9, 12, 18, 36 | 01 02 12 20 21 22 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_3 * coset of 6Z_36) |
| 3, 6, 9, 12, 18, 36 | 01 02 11 12 21 22 | 9 | 9 | 9 | 9 | a programme and the two bounds | LB = least = U | 9: coset of 4Z_36 |
| 4, 6, 9, 12, 18, 36 | 02 11 12 20 21 22 | 30 | 30 | 30 | 30 | a programme and the two bounds | LB = least = U | 30: (coset of 3Z_36 + coset of 2Z_36) |
| 2, 3, 4, 6, 9, 12, 18 | 01 02 10 11 12 20 21 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 6Z_12 * coset of 1Z_18) |
| 2, 3, 4, 6, 9, 12, 36 | 01 02 10 11 20 21 22 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 3Z_6 * (coset of 1Z_9 * coset of 18Z_36)) |
| 2, 3, 4, 6, 9, 18, 36 | 01 02 10 11 12 20 22 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 2Z_4 * (coset of 1Z_6 * coset of 12Z_36)) |
| 2, 3, 4, 6, 12, 18, 36 | 01 10 11 12 20 21 22 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: (coset of 1Z_3 * coset of 9Z_36) |
| 2, 3, 4, 9, 12, 18, 36 | 01 02 10 12 20 21 22 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: (coset of 1Z_2 * (coset of 1Z_3 * coset of 6Z_36)) |
| 2, 3, 6, 9, 12, 18, 36 | 01 02 10 11 12 21 22 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: (coset of 1Z_2 * coset of 4Z_36) |
| 2, 4, 6, 9, 12, 18, 36 | 02 10 11 12 20 21 22 | 12 | 12 | 12 | 12 | a programme and the two bounds | LB = least = U | 12: coset of 3Z_36 |
| 3, 4, 6, 9, 12, 18, 36 | 01 02 11 12 20 21 22 | 18 | 18 | 18 | 18 | a programme and the two bounds | LB = least = U | 18: coset of 2Z_36 |
| 2, 3, 4, 6, 9, 12, 18, 36 | 01 02 10 11 12 20 21 22 | 36 | 36 | 36 | 36 | a programme and the two bounds | LB = least = U | 36: coset of 1Z_36 |
