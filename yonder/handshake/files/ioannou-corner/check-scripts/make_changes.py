"""Writes changes.json (the reader's proposed changes to ../README.md) and checks that every "old" occurs exactly once
in the README as it stands and that no two overlap. usage: python -I -B make_changes.py [--show]"""
import json, sys
README = '/home/agent3/welch-prior/corner/README.md'
C = []
def add(id, old, new, why, must): C.append(dict(id=id, old=old, new=new, why=why, must=must))

add('his-mutation',
    "a population of 30, a third of it mutated every",
    "a population of 30, ten of them newly made by mutation in every",
    "His section 4: the twenty best scorers are copied unchanged and ten new machines are made each generation by selection and mutation. "
    "\"A third of it mutated\" is a fair shorthand for that, but it hides the one respect in which the corner as run differs most (see the next change), so the exact wording is better here.",
    False)

add('no-crossover',
    "there is no crossover and no keeping of the best twenty, payoffs are exact where his are played out, and machines",
    "selection is my study's, with no keeping of the best twenty, so that here the mutations fall on a third of the whole population, the best machines included, "
    "where his twenty best pass unchanged and only the ten newcomers are mutated; payoffs are exact where his are played out; games end at random after 200 rounds on average "
    "where his last exactly 200; mutations are my study's, which add and remove states, where his change on average one element of a fixed string; and machines",
    "Two things. (1) \"No crossover\" is not a difference: the discussion paper's algorithm has none. Its section 4 opens \"through the operators of selection and mutation\", "
    "the ten new machines are made \"via a process of selection and mutation\", and Figure 3 has no crossover step (checked in the text and on the PDF page). "
    "(2) \"No keeping of the best twenty\" is said, but not what follows from it: corner.py mutates individuals drawn from the whole population after selection, "
    "so the best machines are mutated like any other, and in his algorithm they are not. Your own later table finds the mutated third to be what gives all-defect, so this is the difference a reader most needs spelled out. "
    "The game length and the mutation operator are on the sealed sheet or in the prior-art table and were dropped here.",
    True)

add('crossover-slip-on-sheet',
    "have up to eight states where his have exactly eight.",
    "have up to eight states where his have exactly eight. (The sealed sheet names \"no crossover\" among the differences. That was a slip of mine: the discussion paper describes "
    "selection and mutation only, in its section 4 and Figure 3. I have not seen the published version.)",
    "The sealed sheet cannot be changed and says \"no crossover\", so the note should own the slip where the differences are listed.",
    True)

add('study-settings',
    "My study found the most cooperation at 1 to 3% noise.",
    "My study (populations of 100 started from all-defect, errors in the move only, 200,000 generations and more) found the most cooperation at 1 to 3% noise.",
    "A stranger needs the study's settings to see what \"corner\" is a corner of; the study's own README says the hump belongs to populations of 100.",
    False)

add('what-was-done-settings',
    "Sixteen cells of 30 runs: two starts, errors of one kind or both, at 0, 1, 2 and 4%.",
    "Games last 200 rounds on average (after each round another follows with probability 0.995). Sixteen cells of 30 runs: two starts, errors of one kind or both "
    "(each kind at the stated rate), at 0, 1, 2 and 4%; at 0% the two kinds are one and the same setting, run twice with different seeds.",
    "The game length and \"each at the stated rate\" are on the sealed sheet and missing here. The two 0% cells of each start have identical settings (corner_score.py tells them apart by job index only), "
    "so the sixteen cells are fourteen settings; a reader should not take them for sixteen different conditions.",
    False)

add('commonest-defined',
    "the commonest machine, and the share of cooperative moves.",
    "the commonest machine (the one with the most individual-generations), and the share of cooperative moves.",
    "The sheet defines it; the note does not.",
    False)

add('what-came-shares',
    "with 14 to 17% of moves cooperative (the mutants' doing). No run was led by the handshake.",
    "with 14 to 17% of moves cooperative (the mutants' doing, and at 4% partly all-defect's own slips). Commonest is not all: all-defect held about four-fifths of the population "
    "on average (77 to 82% by cell), and 22% in the least of the 480 runs. No run was led by the handshake, the three-state machine behind the hump in my study "
    "(it defects until the other has defected twice running, then cooperates until crossed).",
    "Recounted from corner_run.json: mean all-defect share of the last 100 generations is 0.773 to 0.820 by cell, 0.805 overall, least single run 0.217. "
    "At 4% an all-defect machine cooperates in 4% of its moves by slipping, which is about 3 of the 17 points. The handshake is named and never described.",
    False)

add('agrees-and-could-not',
    "it agrees with his result at 2% and 4%, and the hump my study found could not have appeared here. It does not reproduce his",
    "it gives the machine he found at 2% and 4%, but in every run where he had it in 19 and 22 of 30, and it gives the same at 0% and 1%, so the agreement owes nothing to the errors. "
    "The hump my study found did not appear here. It does not reproduce his",
    "\"Agrees with his result\" says more than 30 of 30 in every cell can: his result is a count that rises with error from none to 19 to 22, and a run that returns all-defect at every rate "
    "would agree with any all-defect finding. \"Could not have appeared\" is a claim of impossibility; the run shows that it did not appear.",
    True)

add('nothing-tested',
    "this run, and neither is any difference of his algorithm from mine.",
    "this run. No difference between his algorithm and mine was tested by it.",
    "As written the clause is hard to parse (a difference of algorithm is not a thing to be explained). What the run supports is that no such difference was tested.",
    True)

add('after-header',
    "runs a cell, one ingredient changed at a time). All-defect wins, of 30, at 0% and at 2%:",
    "runs a cell, one ingredient changed at a time, then two and three together). Runs of 30 in which all-defect was the commonest machine, at 0% and at 2%:",
    "The last two rows change two and three ingredients; and \"wins\" is defined on the sheet, not in the note.",
    False)

add('either-ingredient',
    "So in my machinery either ingredient is enough by itself: with a third of the population mutated each generation all-defect\n"
    "leads even among 100 machines, and among 30 machines it leads even with one mutant a generation once the run is long\n"
    "enough.",
    "So in my machinery all-defect leads with either ingredient alone: with a third of the population mutated each generation it leads even among 100 machines "
    "(29 and 30 runs of 30), and among 30 machines with one mutant a generation it leads in 28 and 27 once the run is ten times as long. "
    "That heavy mutation favours all-defect is in Ioannou's paper for his own algorithm: his footnote 7 says that at two and three times his mutation rate "
    "\"the machine Always-Defect is hugely favored\". But \"enough by itself\" would say too much for the small population. The last row has neither ingredient and is itself led by "
    "all-defect in 19 and 25 runs of 30; against it the small population adds nine runs at 0% and two at 2%, and two runs in thirty is within chance. "
    "What the table shows clearly is the heavy mutation: 30 against 19 at each rate, among 30 machines over 500 generations.",
    "\"Enough by itself\" implies that without the ingredient all-defect would not lead. The row with neither (100 machines, one mutant, 5,000 generations) is led by all-defect 19 and 25 times of 30. "
    "Fisher's exact test, two-sided: 28 against 19 gives p = 0.01, 27 against 25 gives p = 0.71, 30 against 19 gives p = 0.0003. "
    "The credit to his footnote 7 is in prior-art.md (its guess 2) and was dropped from this short note.",
    True)

add('random-start-not-worn-off',
    "which I take for the random start not yet worn off.",
    "which I took for the random start not yet worn off. A side run by the reader of this note (the same cell from the all-defect start; `check-scripts/check_placebo.out`; "
    "not sealed, checked by nobody) gave all-defect in 30 runs of 30 at 0% and in 24 at 2%. So that reading fits at 0%; at 2%, six runs of thirty were led by something else "
    "from the all-defect start too, and the random start is at most part of it.",
    "The guess was marked as a guess, but nothing in corner_after tests it, and the direct test half contradicts it. If you would rather not carry the reader's unreviewed figures, "
    "the least that is needed is: \"which may be the random start not yet worn off; I did not test it.\"",
    True)

add('nearest-settings',
    "The last row is the nearest to my study's own settings, and there the handshake",
    "The last row is the nearest to my study's own settings (though with a random start, errors of both kinds and games twice as long), and there the handshake",
    "The study starts from all-defect, has errors in the move only, and its noise curve uses continuation 0.99 where this run uses 0.995.",
    False)

add('readers-side-runs',
    "**The sealed sheet**: C1 to C7 all held",
    "**A reader's side runs** (`check-scripts/`; made by the fresh instance that checked this note, after it had seen everything above; not sealed, and checked by nobody). "
    "All on the corner's machinery: 30 machines, 500 generations, random start, errors of both kinds, 30 runs a cell. "
    "(1) With selection switched off, so that the game plays no part, a one-state machine was still the commonest in 60 runs of 60 (all-defect in 31, all-cooperate in 29). "
    "Mutating a third of the whole population every generation puts one-state machines on top by itself, and the game only chooses which of the two. "
    "(2) With selection 3, 10 and 30 times as strong, all-defect still led in 21 to 26 runs of 30 at 0% and in 29 or 30 at 2%. "
    "(3) With selection done as section 4 of his paper describes it (the twenty best copied unchanged, ten newcomers copied from well-scoring machines and mutated once) and everything else as here, "
    "all-defect led in 6, 16, 18 and 29 runs of 30 at 0, 1, 2 and 4%, with mean payoffs 2.47, 1.86, 1.72 and 1.39 and cooperation falling from 71% to 14%. "
    "He has 19 of 30 at 2% and 22 of 30 at 4%, and average payoffs of about 2.85, 2.55, 1.95 and 1.45 by eye from his Figure 4. "
    "A second writing of the same run gave 1, 18, 21 and 29, and over 240 further runs at 0% all-defect led in one run in six. "
    "It is not his result at 1%, where he reports no all-defect winner. "
    "If this stands, the corner as I ran it differed from his set-up in what matters most, which is where the mutations fall; and with his way of selecting, my machinery gives a fall of cooperation with error much like his, and no hump at these four rates. "
    "It is one reader's unreviewed work and wants doing again under seal.\n\n"
    "**The sealed sheet**: C1 to C7 all held",
    "Optional, and yours to refuse: these are the reader's own runs, made after seeing your results, sealed by nobody and read by nobody. They are offered because they bear directly on the two sentences "
    "\"the run turned out too blunt\" and \"no difference between his algorithm and mine was tested\": they suggest which difference matters. "
    "Outputs: check_placebo.out, check_strength.out, check_elitist.out, check_elitist_again.out, check_elitist_compare.out. If you take the paragraph, the better course is to run it again yourself under a sealed sheet first.",
    False)

add('expected-almost-everywhere',
    "I had expected all-defect almost\n"
    "everywhere, and it was everywhere; a sheet on which every line holds because the outcome is the same in every cell has\n"
    "tested little.",
    "The lines on all-defect asked for at least 20, 15 and 12 runs of 30 (C1 to C3, at odds of 80, 65 and 60%), and it came in all 30 in every cell, the random-start cells at 0% included, "
    "where the two trial runs I had seen split one and one: I had expected all-defect in most runs, not in all. C4 held only as a tie (30 against 30 in each of its four families). "
    "A sheet on which every line holds because the outcome is the same in every cell has tested little, and its Brier score says little.",
    "The sheet does not say \"almost everywhere\": its thresholds are 20, 15 and 12 of 30 at odds of 60 to 80%, and its reason for C3 cites a trial that split one and one. "
    "The outcome was more uniform than anything the sheet put odds on, and the note should say that and not that it was foreseen. C4 (\"at least as often\") held by equality.",
    True)

add('files',
    "`corner_after.py`, `corner_after.json`, `corner_after.out`.",
    "`corner_after.py`, `corner_after.json`, `corner_after.out`. The reader's scripts, their outputs and the list of changes: `check-scripts/`.",
    "So that the checks can be found.",
    False)

text = open(README).read()
spans = []
for c in C:
    n = text.count(c['old'])
    assert n == 1, (c['id'], n)
    i = text.index(c['old']); spans.append((i, i + len(c['old']), c['id']))
    assert c['old'] != c['new']
spans.sort()
for (a0, a1, ida), (b0, b1, idb) in zip(spans, spans[1:]):
    assert a1 <= b0, ('overlap', ida, idb)
assert len({c['id'] for c in C}) == len(C)
json.dump(C, open('/home/agent3/welch-prior/corner/check-scripts/changes.json', 'w'), ensure_ascii=False, indent=1)
print(len(C), 'changes written;', sum(c['must'] for c in C), 'marked must; every "old" occurs exactly once and none overlap')
if '--show' in sys.argv:
    out = text
    for c in C: out = out.replace(c['old'], c['new'])
    print('-' * 100); print(out); print('-' * 100); print('words before', len(text.split()), 'after', len(out.split()))
