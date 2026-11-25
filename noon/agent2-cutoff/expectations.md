# Expectations for the arXiv's daily cutoff, written at 17:07:19 UTC on 22 November, before anything was fetched

Question. The arXiv announces new papers once a day. As I remember it, papers received before 14:00 US Eastern
time on a weekday go into that evening's mailing, and within a mailing papers are listed in the order received,
so the first paper in after 14:00 heads the next day's list. Do authors time their submissions to that
moment? Hurrying to get in before it would be procrastination; waiting to be first after it would be finagling
for the top of the list. I remember studies of astrophysics papers finding the second (and finding that papers
at the top are cited more). I have looked nothing up, and I have not fetched anything. (From the words
"procrastinator" and "finagling".)

Data, fixed now. The arXiv's public API. Every paper whose first version is dated from 1 January to 30 June
2025 and whose primary category is in one of these groups: astro-ph (all six of its categories); hep-th;
hep-ph; gr-qc; quant-ph; maths (math.CO and math.AP together); cs.CL. The time of a paper is the API's
"published" time of its first version, turned into US Eastern time. Only Mondays to Fridays count.
"After" is the ten minutes from 14:00:00 to 14:09:59 Eastern; "before" is 13:50:00 to 13:59:59; "the ratio" of
a group is its number of papers after over its number before, all weekdays of the half-year together.
If the API will not give a group in full, the group is dropped and I say so; if "published" turns out not to be
the time of receipt to the second, the study stops there and says so.

"Between" includes its ends. Each line says whether it is worked, remembered or guessed.

T1. (remembered) astro-ph: the ratio is at least 3.                                                   odds 0.80
T2. (guessed) astro-ph: of the papers in the ten minutes after, at least 40% come in the first 60 seconds.  odds 0.60
T3. (remembered loosely) hep-th: the ratio is at least 1.5.                                            odds 0.65
T4. (guessed) quant-ph: the ratio is at least 1.5.                                                    odds 0.55
T5. (guessed) maths: the ratio is between 0.6 and 1.6.                                                odds 0.60
T6. (guessed) cs.CL: the ratio is between 0.6 and 2.0.                                                odds 0.55
T7. (guessed) astro-ph has the largest ratio of the seven groups.                                     odds 0.70
T8. (guessed) No rush to get in: in no group do the ten minutes before the cutoff hold more than 1.5 times
    as many papers as the ten minutes from 13:00:00 to 13:09:59.                                      odds 0.55
T9. (remembered: the cutoff is kept in Eastern time, so it moves by an hour against the API's clock when the
    United States changes its clocks, which in 2025 was on 9 March) In astro-ph the busiest single minute of
    the day by the API's clock (UTC) is 19:00 for papers of January and February and 18:00 for papers of
    April, May and June.                                                                              odds 0.80
