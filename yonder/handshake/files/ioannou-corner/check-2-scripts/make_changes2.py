"""Second reader: write changes2.json and check it against the README as it stands: every "old" must occur exactly once and no two may
overlap. Also writes two previews (all changes applied; only the must ones) for reading through.

How the list is laid out. The ten changes marked must rest on the paper, on the sealed and unsealed files that were rerun, on counts made
in exact replays of those runs, and on a measurement of Figure 4. Everything that rests on the second reader's own new runs is kept in one
change, S11, which is not marked must and can be left out without leaving any other change pointing at nothing.
usage: python -I -B make_changes2.py"""
import json
README = '/home/agent3/welch-prior/corner/README.md'
OUT = '/home/agent3/welch-prior/corner/check-2-scripts/'
C = []
def ch(id, must, old, new, why): C.append(dict(id=id, old=old, new=new, why=why, must=must))

ch('S1-where-the-paper-is-short', True,
   "changed with a 4% chance. 500 generations, a random start, errors of both kinds, 30 runs at each rate. Still not his: payoffs\nare exact where his are played out, and games end at random after 200 rounds on average.",
   "changed with a 4% chance. 500 generations, a random start, errors of both kinds, 30 runs at each rate. Still not his: payoffs are exact where his are played out (one match of 200 rounds a pair, as far as the paper says), and games end at random after 200 rounds on average where his last exactly 200.\n\n"
   "The paper gives the scheme a paragraph and a figure, and in six places I had to choose. (1) What a string is made of. The paper gives each element \"a 4% independent chance of mutation, which implies an expectation of 1 element-mutation per string\", so a string has 25 elements; that they are eight moves, sixteen arrows and the start state is my guess. (2) How many elements change. The text has each element changed with a 4% chance; Figure 3 says \"switching one element at random\". I followed the text, which is nearly word for word from Miller (1996), whose approach he says he uses, and Miller is plain that each place has its own chance. (3) How the pairs are drawn. The paper says only \"with the probabilities biased by their scores\". I took chances in proportion to the raw score; Miller draws in proportion to a normalised score (the score less the mean, over the standard deviation, plus 2, cut off at zero). (4) Which of a pair is copied. It is \"the better performer\" in the text and \"the winner of the pair's match\" in Figure 3; I took the one with the higher total score. (5) Ties for the twentieth place. The paper is silent. In `elite.py` the machine listed first wins and the twenty kept are listed first, so a newcomer never displaces a kept machine that scores exactly what it scores; and with exact payoffs a newcomer that behaves as a kept machine does scores exactly what that machine scores. With payoffs played out, as his are, such ties hardly arise once there are errors. (6) What makes a machine \"the winner\" of a run. The paper does not say. Mine is the commonest machine over the last 100 generations, as in the first run. None of the other readings was tried under seal.",
   "The section presents 25 elements, the 4% rule, the proportional draw, the better of a pair and the commonest machine as his scheme. The paper does not state the first, speaks with two voices on the second and fourth (text against Figure 3), and is silent on the rest. The tie rule is not mentioned anywhere in the note. Miller (1996, pp. 94 to 99 and footnotes 6 and 7, read from the scan on disk) is where Ioannou's wording comes from.")

ch('S2-figure-4-column-head', True,
   "his Figure 4, by the reader's eye",
   "his Figure 4 at generation 500, by the first reader's eye",
   "The four figures are where his smoothed curves end, at generation 500. The column beside it is a mean over the last 100 generations, and the head should show that they are not the same thing.")

ch('S3-payoff-at-1-percent', True,
   "| 1% | 1 | 11 | 2.57 | 2.55 | 75% |",
   "| 1% | 1 | 11 | 2.56 | 2.55 | 75% |",
   "The mean is 2.5649. `elite_score.out` prints 2.565 and the table rounded that a second time.")

ch('S4-what-the-columns-are', True,
   "He reports Always-Defect as the winner in 19 of 30 runs at 2% and 22 of 30 at 4%, and diverse history-dependent machines at\n1% and 0%.",
   "He reports Always-Defect as the winner in 19 of 30 runs at 2% and 22 of 30 at 4%, and diverse history-dependent machines at 1% and 0%. My columns are all over the last 100 generations of a run, and the standard errors of my four mean payoffs are 0.07, 0.06, 0.12 and 0.08. The Figure 4 column is the end of his smoothed curves (the second reader measured 2.85, 2.54, 1.94 and 1.45 off the page image); over generations 400 to 500 his curves average about 2.80, 2.52, 1.89 and 1.45, which is the fairer thing to set beside mine.",
   "A reader cannot tell what is compared with what. His Figure 4 is a local-polynomial smooth of the average payoff by generation, over the thirty machines and the thirty runs, drawn for all 500 generations (his footnote 10). Measured from the embedded image by pixel, calibrated on its tick marks: 2.85, 2.54, 1.94, 1.45 at generation 500; 2.80, 2.52, 1.89, 1.45 as means over generations 400 to 500 (`read_fig4.out`).")

ch('S5-why-D8-failed', True,
   "I had taken the reader's\ncounts (6, 16, 18 and 29) for what the scheme gives, and my writing of it gave 0, 1, 9 and 20.",
   "For D1 to D3 I had taken the reader's counts (6, 16, 18 and 29) for what the scheme gives, and my writing of it gave 0, 1, 9 and 20. D8 failed for another reason. Its line of reason says that no run led by the handshake \"is reported by the reader\"; the reader's report names none, but the reader's own output (`check-scripts/check_elitist.out`) lists the handshake as the leader in 7 runs of 30 at 1% and 7 at 2%. D8 would have failed on the reader's run as well.",
   "The sentence explains all four failures by the difference between the two writings. That covers D1 to D3 only. Counted from `check-scripts/elitist.json`, the handshake at any entry state led 7 and 8 runs of 30 at 1% and 2% with all newcomers mutated, and 9 and 5 with 64% mutated; the output file prints the first of its three forms as leader in 7 and 7.")

ch('S6-how-the-two-writings-differ', True,
   "The two writings differ in one\nthing, the mutation. Mine changes elements of an eight-state string, as the paper describes, so about a third of newcomers are\nunchanged copies and changes in states a machine does not use are carried along. The reader's minimises each machine and\napplies my study's mutation once, which always changes something.",
   "The two writings differ in the mutation, and in how ties for the twentieth place are broken (the reader's at random, mine in favour of the machine listed first). Mine changes elements of an eight-state string, as the paper's text describes, so about a third of newcomers (36%) are unchanged copies and changes in states a machine does not use are carried along. The reader's minimises each machine and applies my study's mutation once, which works only on the states a machine uses and can add or remove a state. It does not always change something: by the second reader's count 24, 44, 43 and 63% of its newcomers at the four error rates were the same machine as their parent, against 49, 53, 58 and 67% of mine.",
   "Three things. The scripts differ in tie-breaking too (`check_elitist.py` rounds to 8 places and shuffles; `elite.py` uses a stable sort). \"As the paper describes\" hides that Figure 3 says one element. And the study's `mutate()` does not always change something: it redraws an arrow to any state including the one it had, most of its moves do nothing to a one-state machine, and many changes vanish when the machine is minimised. The shares are counted over all newcomers in replays that reproduce `elite_run.json` and `elite_after.json` field for field (`replay_summary.out`).")

ch('S7-what-the-one-test-shows', True,
   "the counts are 5, 18, 18 and 30, which is the reader's\nresult. So the difference is the mutation and not a slip in either script, as far as that one test goes.",
   "the counts are 5, 18, 18 and 30, which is the reader's result within the scatter of thirty runs. So the difference between the two writings is the mutation, as far as that one test goes. The test cannot show a slip in what the two scripts share (the payoff routine, and the same reading of the paper where it is short), nor one in my string mutation, which it takes out; the second reader read that routine against the paper and found none. Nor is the difference in the unchanged copies: the reader's own run with 36% of newcomers left unchanged gave 8, 14, 18 and 30. What it is in the two kinds of mutation that does it, I have not found out.",
   "\"Not a slip in either script\" is more than the test can show: it swaps my mutation out, so a slip in it would go unseen, and both scripts share `payoff2` and one reading of the paper. The 8, 14, 18 and 30 are the rows marked 0.64 in `check-scripts/check_elitist.out`.")

ch('S8-close-to-his-figure-4', True,
   "- With mutation done his way my mean payoffs are close to those of his Figure 4 at every error rate, and all-defect takes\n  over as the error rises, as in his paper, though at 2% in 9 runs of 30 against his 19.",
   "- With mutation done as his text has it and payoffs exact, my mean payoffs over the last hundred generations are within 0.15 of the end of his Figure 4's curves at every error rate, and all-defect takes over as the error rises, as in his paper. That is less than it looks. At 2% all-defect leads 9 runs of 30 against his 19, which is beyond chance (p = 0.02) if his winner is counted as mine is, so his \"clear winner\" at 2% is not reproduced. And earlier in the run my payoffs are above his at 1, 2 and 4%: about generation 50 they are 2.25, 2.09 and 1.64 against his 2.00, 1.71 and 1.34, which is two to three of my standard errors (his are not given). The table falls short of showing that my writing is his algorithm.",
   "The sentence says more than the run shows. The table sets a mean over my last 100 generations beside the last point of his curves; over the course of the run mine recover from the early fall sooner than his (the sealed run's own payoffs by generation, from a replay that reproduces it field for field, each run averaged over 21 generations about the fiftieth). Fisher's exact test of 9 of 30 against 19 of 30 gives p = 0.019.")

ch('S9-no-hump', True,
   "- There is no hump. Cooperation falls steadily as the error rises. The rise of cooperation with a little noise in my study\n  belongs to that study's set-up (a start from all-defect, a hundred machines, very long runs) and does not appear in this one.",
   "- There is no hump at these four rates. Cooperation falls at each step of the error rate (the first step, from 84% to 75%, is about two standard errors; no rate between 0% and 1% was run). The rise of cooperation with a little noise in my study does not appear here. This run does not say which of that study's differences the rise depends on: the study starts from all-defect, has a hundred machines, errors in the move only, another selection and another mutation, and runs at least four hundred times as long.",
   "\"Belongs to that study's set-up\" names a cause that this run did not test, and lists three of the differences where there are at least six. \"No hump\" is shown at 0, 1, 2 and 4% and nowhere between.")

ch('S10-the-handshake', False,
   "- At 1% error the three-state machine of my study leads more runs than any other machine (11 of 30, counting its three\n  entry states), and at 2% it is second to all-defect (7 against 9).",
   "- At 1% error the three-state machine of my study (Fortress3 in print, by the prior-art note) leads more runs than any other machine (11 of 30, counting its three entry states, which are the same three states begun at each in turn), and at 2% it is second to all-defect (7 against 9, which thirty runs cannot tell apart). It is not peculiar to my kind of mutation: with the reader's kind it led 5 to 9 runs of 30 at 1% and 5 to 8 at 2%.",
   "Optional. A stranger may take the machine for a new one, which the prior-art note says it is not; may not know what an entry state is; and should know that the first reader's runs had the handshake too (7 and 8 runs at 1% and 2%, 9 and 5 with 64% mutated, 5 and 5 in `elite_after.json`), so that its showing here is not a product of the string mutation. Seven against nine is no difference (p = 0.8).")

SIDE = (
   "**A second reader's side runs** (`check-2-scripts/`; made by the fresh instance that checked the section above, after it had seen all of it; not sealed, and checked by nobody). Each is `elite.py` with the thing named changed, the other reading of each of the six places among them, on fresh seeds, 30 runs a rate, measured as in the table above.\n\n"
   "| | all-defect the commonest machine at 0, 1, 2, 4% | mean payoff a round at 0, 1, 2, 4% |\n"
   "|---|---|---|\n"
   "| the sealed run | 0, 1, 9, 20 | 2.71, 2.56, 2.07, 1.46 |\n"
   "| the same again on fresh seeds | 0, 2, 9, 17 | 2.73, 2.50, 2.13, 1.57 |\n"
   "| exactly one element switched in every newcomer (Figure 3) | 0, 0, 8, 23 | 2.84, 2.63, 2.10, 1.50 |\n"
   "| each element changed at 8% | 0, 0, 4, 23 | 2.63, 2.54, 2.19, 1.45 |\n"
   "| each element changed at 12% | 0, 0, 5, 20 | 2.68, 2.46, 2.19, 1.61 |\n"
   "| pairs drawn by Miller's normalised score | 0, 1, 7, 23 | 2.70, 2.45, 2.10, 1.46 |\n"
   "| the one of a pair that did better in the game between the two is copied (Figure 3) | 0, 7, 10, 23 | 2.69, 2.01, 1.85, 1.39 |\n"
   "| ties for the twentieth place broken at random | TIES1 | TIESPAY1 |\n"
   "| the same again on other seeds | TIES2 | TIESPAY2 |\n"
   "| exact payoffs over exactly 200 rounds | 0, 2, 3, 21 | 2.76, 2.49, 2.37, 1.50 |\n"
   "| matches played out once over 200 rounds, errors drawn (the paper) | PLAYED1 | PLAYEDPAY1 |\n"
   "| the same again on other seeds | PLAYED2 | PLAYEDPAY2 |\n"
   "| played out five times a pair and averaged (as Miller did) | 0, 1, 3, 13 | 2.83, 2.60, 2.35, 1.70 |\n"
   "| played out once, pairs drawn by Miller's normalised score | 0, 1, 5, 13 | 2.86, 2.59, 2.29, 1.81 |\n"
   "| played out once, the winner of the pair's match copied | 0, 1, 3, 13 | 2.71, 2.45, 2.16, 1.72 |\n"
   "| played out once, exactly one element switched | 0, 0, 1, 14 | 2.80, 2.61, 2.45, 1.85 |\n"
   "| played out once, with those three together | 0, 0, 4, 16 | 2.71, 2.50, 2.22, 1.61 |\n"
   "| his paper | not said, not said, 19, 22 | 2.80, 2.52, 1.89, 1.45 (Figure 4 over generations 400 to 500) |\n\n"
   "WHATTHEYSHOW\n\n")

ch('S11-second-readers-side-runs', False,
   "**The first sealed sheet**: C1 to C7 all held",
   SIDE + "**The first sealed sheet**: C1 to C7 all held",
   "Not marked must, because it is new work of the second reader's and no one has checked it; but it is the part of this reading that bears hardest on the section. It puts a new paragraph and table before the paragraph on the first sealed sheet. No other change points at it, so it can be left out whole. If it goes in, it wants what the first reader's side run got: doing again under seal.")

ch('S12-files', False,
   "`elite_after.py`, `elite_after.json`, `elite_after.out`.",
   "`elite_after.py`, `elite_after.json`, `elite_after.out`. The second reader's scripts and outputs, and its list of changes: `check-2-scripts/`.",
   "Optional. Wanted if S11 goes in, or if the second reader's report is kept beside the note.")

ch('S13-header', False,
   "four of the eight held, and that run says more than the first. It is the section \"The second sheet\" below, which is mine and was written after the reading.",
   "four of the eight held, and that run says more than the first, though less than its table suggests: his result at 2% is not reproduced, and his paper leaves open several choices I had to make. It is the section \"The second sheet\" below, which is mine and was written after the first reading.",
   "Optional. Someone who reads only the header should not come away thinking the second run reproduces his scheme. \"The reading\" becomes \"the first reading\" now that there are two.")

ch('S14-which-run-was-sealed', False,
   "- How a newcomer is mutated matters here as much as the error rate does: at 1% all-defect is the commonest machine in 1\n  run of 30 with one kind of mutation and in 18 with the other.",
   "- How a newcomer is mutated matters here as much as the error rate does: at 1% all-defect is the commonest machine in 1 run of 30 with one kind of mutation (the sealed run) and in 18 with the other (not sealed), which is far beyond chance, and the mean payoff is 2.56 with the one and 1.79 with the other.",
   "Optional. The sentence is right as it stands (1 of 30 against 18 of 30, p = 3 in a million). The change says which of the two runs was sealed and adds the payoffs, which carry the comparison with the error rate: 0.77 is about the fall from 1% error to between 2% and 4%.")

def fill(text, vals):
    for k, v in vals.items():
        assert text.count(k) == 1, k
        text = text.replace(k, v)
    return text

if __name__ == '__main__':
    import os, sys
    D = OUT
    def row(f):
        R = json.load(open(D + f)); c = [[x for x in R if x['rate'] == r] for r in (0.0, 0.01, 0.02, 0.04)]
        return ', '.join(str(sum(x['top_is_alld'] for x in cc)) for cc in c), ', '.join(f'{sum(x["payoff"] for x in cc) / len(cc):.2f}' for cc in c)
    vals = {}
    for key, f in (('TIES1', 'replay_ties_fresh.json'), ('TIES2', 'second_ties.json'), ('PLAYED1', 'replay_played_fresh.json'), ('PLAYED2', 'second_played.json')):
        a, b = row(f); vals[key] = a; vals[key.replace('TIES', 'TIESPAY').replace('PLAYED', 'PLAYEDPAY')] = b
    vals['WHATTHEYSHOW'] = open(D + 'what_they_show.txt').read().strip()
    for c in C:
        if c['id'] == 'S11-second-readers-side-runs': c['new'] = fill(c['new'], vals)
    s = open(README).read()
    spans = []
    for c in C:
        n = s.count(c['old'])
        assert n == 1, (c['id'], n)
        assert c['old'] != c['new']
        i = s.index(c['old']); spans.append((i, i + len(c['old']), c['id']))
    spans.sort()
    for (a0, a1, ida), (b0, b1, idb) in zip(spans, spans[1:]): assert a1 <= b0, (ida, idb)
    json.dump(C, open(OUT + 'changes2.json', 'w'), indent=1, ensure_ascii=False)
    for name, pick in (('preview-all-changes.txt', lambda c: True), ('preview-must-only.txt', lambda c: c['must'])):
        t = s
        for c in C:
            if pick(c): t = t.replace(c['old'], c['new'])
        open(OUT + name, 'w').write(t)
    back = json.load(open(OUT + 'changes2.json'))
    assert back == C
    print(len(C), 'changes;', sum(c['must'] for c in C), 'must; every "old" occurs exactly once in README.md and none overlap; order in the file:', [x[2] for x in spans])
    for bad in ('/tmp', 'agent1', 'agent2', 'toolu_', 'session'):
        assert not any(bad in json.dumps(c) for c in C), bad
