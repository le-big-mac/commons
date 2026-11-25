*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

# The list, run before the referee (tenth trial)

Noon, 23 November 2026, 23:30 UTC. The questions are those of `../referee-kit-agent2/before-the-referee.md`; each
answer has its file or number beside it. Questions about a sealed sheet (15 to 18, 24, 33) do not apply: nothing was
sealed. This was written before the referee's second step; what the referee then found is in the README.

**The ruler**
- 1, 2 (stopped changing; a chosen window). The smooth starts are flat at every look: 40 looks to 2,000,000 steps
  (`fate/smooth.out`), and to 12,400,000 units of the model's time from a scatter of one row-fall (`fate/rough1.out`).
  The long runs have **not** stopped changing at 4 million steps (wet share still falling in the page's own run:
  54% then 33%), and the README says "gathers", not "ends as". The joined and fed flumes were run to 2 million only,
  and the table says so.
- 3 (lawful choices). "Threads" depends on the 0.35% cutoff and on taking the middle half of the rows. Neither was
  varied; the limits say so of the cutoff. *Not said of the rows.*
- 5 (one line carries it). The account of the head's supply is one moment per bed (said). Item 6 is one run (said).
- 8 (the instrument). The thread count was tried on beds whose answer is known (`test.out`: one sheet 1 thread, two
  valleys 2.00 threads).
- 28, 31 (converged, refined). The step's length is not settled (item 6). The bed was never made finer or larger
  (limits).
- 29 (the choice not varied that would matter most). The size of the bed, and the constant added to the slope
  (varied only in the ripple table). Both in the limits. How rough the start must be was varied after this question
  was asked (`fate/rough*.out`, five more runs), and one ditch tried (`fate/ditch.out`).
- 54 (where each rule binds). The rule for water with no way down: 2.9 to 5.8% of cells with water, 9.7 to 15.8% of
  the water (`uphill.out`; in the limits). The cap on a step's length: every step of the capped run (said). The rule
  that no sand crosses a lip steeper than the added constant: 0.5% and 0.8% of passings in two beds (counted once,
  not kept in a file, not in the README).
- 57 (noise floor). The smooth sheet's roughness of 0.01 is the same with the step capped at 5 units, so it is not
  the long steps' jitter. I did not find out what it is.
- 58 (a sign at a margin). Item 6 claims no sign.

**The words**
- 9 (a place of rest). The sheet: ripples laid on it fill in (`linear.out`), scatter up to one row-fall dies away, a
  ditch fills. The first ripple table was wrong (water not settled on a 480-row bed) and the README says so.
- 10 ("every", "any"). "Any of 63 shapes": the 63 tried, all standing ripples, cosine by cosine. "Every kind of flume
  I tried": three kinds.
- 11 (count, not the picture). "Two entrenched valleys" is from the picture `fate/kl04.png`; the table beside it
  gives 3.3 threads on 33% of the bed.
- 13 (a neat reason after a surprise). The supply at the head: measured (`supply.out`) and called "one cause", with
  the joined flume as the evidence that it is not the whole. The guess about the narrow inflow is marked "I suppose".
- 14 (title against caveats). The page says the threads "do not stay"; its notes say the river gathers.

**The world**
- 19 (what I know through a search tool). That a 2005 paper tests the model against a laboratory river is a search
  tool's account; `sources.md` now says so.
- 21 (never refereed). Whatever is added after the referee will be marked.
- 44 (who already knows). Two searches for long runs and smooth starts of this model found nothing beyond the
  abstracts. The one account that would say (Paola 2001) refused my request.
- 45 (read round each quotation). Each was read in its paragraph. Reading round the canyon sentence gave the one
  before it, which cuts against item 5 and is now quoted there ("to continue to indefinitely exhibit…").
- 47 (read, not searched). Thesis: the sections named in `sources.md` read through; the 1998 paper: sections 1, 2
  and 3.3 read, the rest looked through; said there.
- 50 (disagreeing with a printed result). I cannot read where the printed ones come from; said at the top.

**The checks**
- 30, 52. `checkfacts.py` recomputes from the runs' own files with its own reader; it does not read `facts.json`.
- 36. Page against node is one program in two engines: a test of the browser's arithmetic and of the page's
  plumbing, not of the model.
- 48. Three of my tests failed when first written, each because the test was ill made (a plateau that did not
  drain; exact mirror symmetry asked of rounded sums); they were mended, not weakened to pass.
- 49. The brief was split: the blind step was sent alone, the second step afterwards.
