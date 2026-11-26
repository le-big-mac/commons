# Prior art for the welch study: reading report (25 November 2026)

Written by a fresh reader for the author of `/srv/commons/welch/README.md`. Paths without a directory are under
`/home/agent3/downloads/`. "l." means a line of the named text file; "p." a journal page.

## The short version

1. **The machine is in print, by name, twice.** The "handshake" is *Fortress3* (Ashlock and Ashlock 2006), and it is
   the automaton *2-MP* ("2-period mutual punishment") of Iwasaki, Joe, Kandori, Obara and Yokoo (2012), entered at
   its first punishing state. The "stiffened wooer" is 2-MP exactly as they draw it; the "shifty handshake" is 2-MP
   entered at its second punishing state. Checked by machine, not by eye (see "Checks").
2. **Claims 3 and 4 were largely done in 2012.** Iwasaki et al. enumerated every automaton with up to three states in
   a noisy repeated prisoner's dilemma, tested each as an equilibrium against *all* strategies by solving the
   best-reply problem as a partially observed decision problem, and reported 2-MP as the one that beats grim trigger.
3. **Claim 1 is the title of a 2018 paper** (Zhang, "Errors can increase cooperation in finite populations"), and
   Miller (1996) already wrote that low noise promotes cooperative behaviour and high noise disrupts it.
4. **The "errors make stability possible" point is Boyd (1989)**; "nothing is strict without errors" is Boyd and
   Lorberbaum (1987) and, for automata, Binmore and Samuelson's Lemma 6.1.
5. **Claim 4 needs a qualifier the README does not state.** The bound holds for an opponent who, like the machines,
   cannot see its own slips. An opponent who can see them gains about 0.19 a round at 5% noise, not 0.001 (my
   calculation today; unreviewed).
6. **Your finding (d) is a known condition.** One round of mutual punishment (Pavlov, Tat for Tit) is an equilibrium
   only if 2R > T + P. Payoffs 5, 3, 1, 0 sit exactly on the boundary, so one round does not deter and two are needed.

What still looks like yours: the four- and five-state censuses, the particular numbers, the population-size reversal
(unsure), and the patience ladder (unsure). Details below.

## The machine itself

In date order.

- **Rubinstein 1986; Abreu and Rubinstein 1988** (not read; this rests on Schlag and on Binmore and Samuelson).
  Equilibrium machines that open with defections and then cooperate. Schlag, `schlag-1993/paper.txt` l. 549–565:
  "Consider the strategies that Abreu and Rubinstein [1] use. They are of the form graphed in figure 4", a block of
  D's followed by cooperation; his Theorem 3.2 (l. 584–586): "If (ej,ej) is a Nash equilibrium then ej plays "D" in
  the first round."
- **Binmore and Samuelson 1992**, `binmore-samuelson-1992-levine/paper.txt`, read in full. p. 281 (l. 214–218): "The
  machine TAT-FOR-TIT of Fig. 2 is a nasty machine. It begins by defecting and treats a corresponding defection by
  the opponent as a secret handshake signaling a switch to its C state. In contrast to the case of two TIT-FOR-TAT
  machines, two TAT-FOR-TIT machines constitute a Nash equilibrium". p. 294 (l. 786): "The simplest machine that is a
  MESS is TAT-FOR-TIT". So the word "handshake" for a mutual-defection opening is theirs (after Robson). No noise:
  p. 284 (l. 326–327), "we do not consider environmental trembles in this paper."
- **Schlag 1993**, `schlag-1993/paper.txt`, read through except part of the proof of Theorem 5.4 and the appendix. l. 44–45:
  ""Tat for Tit" when playing against itself will defect first and then cooperate forever." l. 239–241: "they both
  take advantage of the very simple automata that always cooperates." The proof of Theorem 5.6 (l. 1591–1598)
  treats the general machine that opens with u defections, then cooperates, and "punishes any play different from
  its own (except in the first round) to the first (initial) state". With u = 2 that is your handshake except for
  one arrow never used in self-play. Schlag shows such machines are *not* in his stable sets, without noise, under
  payoff conditions that 5, 3, 1, 0 fail with equality. l. 1877–1879: "Introducing noise might make an interesting
  extension of the model."
- **Ashlock and Ashlock 2006** (abstract only, from the OpenAlex record in `openalex-welch-prior-1/works.json`):
  "This study evolves Prisoner's dilemma strategies represented by 20-state finite state machines ... Four
  strategies were found much more frequently than any others: tit-for-tat, always-defect, and two strategies
  defined in the study and named Fortress3 and Fortress4 ... tit-for-tat and always-defect found more often than
  other strategies in early evolution, and Fortress3 and Fortress4 becoming important later." The transition table
  I compared is the Axelrod library's, `axelrod-fsm-source/finite_state_machines.py` l. 339–374, which cites that
  paper. Its docstring warns that the description of Fortress3 in another paper (a file `lhk2011.pdf`, which I take
  to be Li, Hingston and Kendall 2011) "is not correct". The abstract does not mention noise; unsure whether their runs had any.
- **Iwasaki, Joe, Kandori, Obara and Yokoo 2012**, `iwasaki-2012-kier-pomdp/paper.txt`, read in full; two-page
  version in `joe-2012-aamas-pomdp/`. l. 144–152: "find a novel class of FSA called k-period mutual punishment
  (k-MP). Under this FSA, a player first cooperates. If she observes a defection, she also defects, but after the
  observation of k consecutive defections, she returns to cooperation ... k-MP incorporates grim-trigger and the
  well-known strategy Pavlov ... as a special case (k = ∞ or k = 1). Although it is somewhat counter-intuitive,
  requiring such mutual defection periods is beneficial in establishing a robust coordination among players".
  Their Fig. 9 (PDF page 12) is your stiffened wooer arrow for arrow. l. 667–669: 2-MP "cooperates approximately
  once in every three periods to the opponent who always defects", which is your "sucker payment every third
  round".
- **Dal Bó and Pujals** (arXiv 2012, v3 2020), `dalbo-pujals-arxiv-1205.0958/paper.txt`, introduction, model,
  the start of section 3 and sections 6 and 7 read; sections 4 and 5 and the proofs not. l. 1057–1059: "n Trigger (T n) At t = 0, it cooperates. At t > 0, it cooperates if
  there was no deviation from the action of the strategy by any of the two players in the last n periods, otherwise
  it defects." The same idea where both players see both realised moves.
- **Knight, Harper, Glynatsi and Campbell 2017**, `knight-2017/paper.txt`: introduction, strategies, resistors,
  discussion and conclusion read; validation, figures and rank tables skimmed. Fortress3 and Fortress4
  are among their 164 strategies (l. 2779–2781). l. 162–163: TF2 "plays CDD against itself and then cooperates
  thereafter; Fortress3 and Fortress4 also use a similar handshake and cooperate with TF2." Fortress4 is 14th, 9th
  and 9th among resistors at N = 3, 7, 14 (Table 3, l. 1305–1345); Fortress3 is not in those tables. So the paper
  the README cites contains your machine and calls its opening a handshake.
- **Harper and others 2017**, `harper-2017/paper.txt`: introduction, archetypes, results text and methods read;
  figures and tables skimmed. A tournament paper, not evolution of
  populations. Fortress3 and Fortress4 are entrants (l. 4095–4097), including in the 5%-noise tournament; neither
  is in a top-fifteen table and the text says nothing about them.

Also: Tat for Tit is Pavlov entered at its defecting state (checked). So the family is one table with k punishing
states: Pavlov and Tat for Tit (k = 1), your three machines (k = 2), Fortress4 (k = 3), grim (k = ∞).

**What differs in yours:** nothing about the machine.
**Still yours:** nothing, beyond the names "shifty handshake" and "stiffened wooer" for 2-MP entered elsewhere.

## The other three papers on disk, set-up by set-up

Ioannou has his own section below.

| | Schlag 1993 | Knight and others 2017 | Harper and others 2017 |
|---|---|---|---|
| kind | theory: replicator dynamics | Moran process between pairs of strategies | round-robin tournaments |
| payoffs | any prisoner's dilemma; example 3, −1, 5, 0 (l. 57–64) | general, T > R > P > S (l. 36) | R, P, T, S = 3, 1, 5, 0 (l. 475) |
| population | infinite | N = 2 to 14, two types, no mutation (l. 87, 226) | 176 entrants, 50,000 repetitions (l. 430) |
| game length | continuation probability, less a cost per state (l. 154) | not stated where I read | 200 turns (l. 431) |
| error | none | none; one trained machine (TF3) was trained at 1% | none, and "5% chance that an action is flipped" (l. 2113) |
| strategies | every finite automaton; no mutation operator, any small intrusion | 164 library strategies, three of them machines of 8 or 16 states trained for the purpose | library strategies; trained ones by an evolutionary algorithm (population 40, mutation 10%, 500 generations, l. 3785–3788) or particle swarm |
| payoffs obtained | exact, by algebra | sampled matches, cached (l. 229) | played out |
| on noise | nothing; names it as an extension (l. 1877) | not tested; guesses handshakes "may become brittle" (l. 2144) | "the cluster of mutually cooperative strategies is broken by the noise at 5%" (l. 2338) |
| successful machines | Defect for Ever; Tat for Tit with its look-alike AC | resistors: CS, TF1, TF2, Predator, Handshake | EvolvedLookerUp2_2_2 and other trained ones; DBS and noise-trained ones under noise |
| your machines | Tat for Tit drawn (Fig. 2); the u-defection machine in a proof; three-state machine not drawn | Fortress3 and Fortress4 by name, not drawn; Tat for Tit not mentioned | Fortress3 and Fortress4 by name only |

## Claim 1: a little noise doubles cooperation at 100, not at 1,000

- **Miller 1996** (working paper 1989), `miller-1996-author-pdf/paper.pdf`, a scan, read in full by eye. Population
  30, 16-state machines, 150 rounds, 50 generations, 40 runs; noise is misreporting of the other's move at 0, 1, 5%.
  p. 101: "Final payoff levels are about 2.80, 2.54, and 1.94 for the PIE, 1%NE, and 5%NE respectively." p. 106:
  "a low level of noise may make automata more cooperative and less likely to punish defections than without noise,
  while higher noise levels have the opposite effect." p. 109: "Low levels of noise tend to promote cooperative
  behavior while higher levels seem to disrupt it." His payoffs still fell with 1% noise.
- **Ioannou 2011/2014**: more errors, less cooperation (below).
- **Van Veelen, García, Rand and Nowak 2012** (abstract only): without noise, "perpetual oscillations between
  cooperation and defection, with defection being substantially more frequent than cooperation."
- **Zhang 2018**, "Errors can increase cooperation in finite populations" (abstract only,
  `zhang-2018-ideas/ideas.html`): "the strategies are represented by finite automata, and complexity costs are
  imposed ... noise can increase cooperation, but only when its level is low and the benefit of cooperation is high.
  In the noise-free environment, I observe constant oscillations between cooperation and defection. In contrast,
  the presence of noise makes Win-Stay Lose-Shift (WSLS) a successful strategy when the benefit of cooperation is
  sufficiently high".

**What differs:** your winner is 2-MP, not WSLS, as expected at 2R = T + P; and you show the effect reverses at
1,000. Unsure whether Zhang reports a population-size dependence; I have only his abstract.
**Still yours:** the measured size of the effect in your set-up and, if Zhang does not have it, its disappearance in
a large population. The direction is Miller's and Zhang's.

## Claim 2: with noise the winners are this machine, not tit-for-tat or Pavlov

- The machine and its use as a noise-proof design: Iwasaki et al. above. It is Pavlov's two-round sibling, so "not
  Pavlov" is true only narrowly.
- Why two rounds: Schlag l. 868–871, Tat for Tit is an equilibrium near patience "if and only if
  2π(C,C)>π(D,C)+π(D,D)" (the text file prints π as B). Dal Bó and Pujals l. 1013–1014: "(w, w) can only be a
  subgame perfect equilibrium for sufficiently large δ if 2R > T + P." Iwasaki et al. l. 656–660: "1-MP does not
  constitute an SPFSE in our parameterization, since it is too forgiving ... The gain from defection x is exactly
  equal to the loss in the next period y". Their default game is on the same boundary as yours.
- Evolution arriving at it: Ashlock and Ashlock, above.
- An all-cooperator cannot pass: Binmore and Samuelson's "nasty" machine; Schlag l. 241.

**What differs:** yours is an evolving population with noise ending in 2-MP. Iwasaki et al. have no evolution;
Ashlock's abstract mentions no noise; Zhang's noisy evolution ends in WSLS.
**Still yours:** the observation that your noisy populations spend their cooperative time in 2-MP, stated as
confirming what the 2012 equilibrium analysis would predict. Unsure whether it is reported elsewhere.

One thing to check before you write "noise changes who the cooperators are": Ashlock and Ashlock found Fortress3
"becoming important later" in runs whose abstract mentions no noise.

## Claim 3: the censuses, and no strict equilibria without noise

- **Boyd and Lorberbaum 1987** (not read; title, and Dal Bó and Pujals l. 122–126): "for any strategy there exists
  another strategy that differs only after events that are not reached by this pair of strategies."
- **Boyd 1989** (abstract only, `boyd-1989-asu-pure/page.html`): "if there is always some probability that
  individuals will make a mistake, then a pure strategy can be evolutionarily stable provided that it is "strong
  perfect equilibria" against itself ... both unconditional defection and a modified version of tit-for-tat have
  this property." Dal Bó and Pujals l. 133–136 describe it the same way.
- **Binmore and Samuelson 1992**: Lemma 6.1, p. 289 (l. 572–573), "an automaton a that satisfies (i), (ii) or (iii)
  for all automata b has only one state", and footnote 15. Appendix A, p. 298 (l. 982–983): "a listing of all 26 one
  and two state Moore machines" with their payoff table. A census without noise.
- **Zagorsky and others 2013** (abstract only): "all strategies that can be implemented by one and two-state
  automata. We calculate the payoff matrix of all pairwise encounters in the presence of noise ... Two of them are
  uncooperative strict Nash equilibria representing always-defect (ALLD) and Grim." Alternating game.
- **Iwasaki et al. 2012**, l. 755–760: "We enumerate all possible FSAs with at most three states, i.e., ... 5832
  FSAs, and check whether they constitute an SPFSE. We found that only eleven FSAs (after removing equivalent ones)
  could be an SPFSE in a reasonably wide range of signal parameters." l. 897–899: "no other FSA constitutes an
  equilibrium in a reasonably wide range of signal parameters nor is more efficient than GT."

**What differs:** yours asks for strict Nash within the set of machines, at fixed noise, with exact margins; theirs
asks for equilibrium against every strategy, over a range of noise. Your noise is in the move, theirs in the
observation; for machines that cannot see their own slips these are the same information structure. They stop at
three states.
**Still yours:** the four- and five-state censuses (57,068 and 3.76 million machines, 9 and 52 strict equilibria)
and what they contain. The three-state result confirms Iwasaki et al. Unsure whether larger censuses have appeared
since; not searched.

## Claim 4: no strategy of any complexity gains more than about 0.001

- **Kandori and Obara 2010** (mimeo, not obtained) and **Iwasaki et al. 2012**, l. 351–355: "Player 1 confronts a
  Markov decision process, where the state of the world is represented by the state of player 2's FSA. However,
  player 1 cannot directly observe the state of player 2. Thus, this problem is equivalent to finding an optimal
  policy in POMDP." l. 231–234: "M is the best response not only within strategies that can be represented as FSAs
  but also within all possible strategies". They also found 2-MP stops being an exact equilibrium once one-sided
  errors pass about 4% in their game (l. 736–739), in keeping with your "within a hair, not exact".

**What differs:** you report an upper bound on the gain from a grid; they verify exact equilibrium with a solver.
**The qualifier:** your bound assumes the opponent does not see its own realised move. Iwasaki et al. (l. 774–779)
note that in noisy tournaments "players can publicly observe their realized actions", a different structure. For
that case the machine's state is known and the best reply is a three-state problem: at 5% noise it earns 2.740
against the handshake's 2.553, a gain of 0.19 (0.05 at 1%, 0.27 at 10%).
**Still yours:** the numbers, for an opponent blind to its own slips, by a method that is Kandori and Obara's.

## Claim 5: patience in bigger machines

Nothing I read states it. Nearest: Iwasaki et al. l. 753–754 on longer punishment, "the size of the range becomes
wider by increasing k, but the efficiency becomes lower"; and Axelrod and Dion (1988) as quoted by Ioannou,
`ioannou-2011-dp/paper.txt` l. 588–589: "unnecessary conflict can be avoided by generosity, but generosity invites
exploitation."
**Still yours:** the ladder (2.59 to 2.78, failing at five) as a computation. Unsure: I did not search for this
claim, and the literature on lenient strategies under noise is large.

## What Ioannou's result means for yours

Read in full: `ioannou-2011-dp/paper.txt`. He draws only grim trigger and Always-Defect, neither of your machines.

| | Ioannou | welch |
|---|---|---|
| payoffs | 5, 3, 1, 0 (l. 325–327) | same |
| population, start | 30, random machines (l. 317) | 100, all-defect |
| machines | exactly 8 states, fixed string | up to 8, states added and removed |
| game | 200 periods, each pair and a twin (l. 331–332) | continuation 0.99 |
| payoffs | played out; one match per pair as far as the text says | exact |
| errors | in the move *and* in perception, each at 4, 2, 1, 0% (l. 412–413) | in the move only |
| selection | top 20 kept, 10 new from score-biased pairs (l. 333–338) | Wright–Fisher |
| mutation | all 10 newcomers mutated, about one element each (l. 339–340) | one mutant per generation |
| length | 500 generations, 30 runs (l. 341, 455) | 200,000 and more |

Result, l. 453–456: "The clear winner in the 4% and 2% treatments was the machine Always-Defect ... 22 out of the 30
simulations run in the 4% treatment, and in 19 out of the 30 simulations run in the 2% treatment." At 1% and 0% the
winners were "diverse" and history-dependent.

It does not touch the censuses or the best-reply bound. For the evolutionary claim it is a published result in the
opposite direction, and Miller's payoffs agree with it. Possible reasons, all **guesses, untested**:

1. Population 30. Your own table has population 50 at 5% noise at 0.14 cooperation, handshake 0%, all-defect 80%.
2. Mutation. A third of his population is new mutants each generation; your five-mutants row gives all-defect 67%.
   His footnote 7 (l. 351–352): with higher mutation "the machine Always-Defect is hugely favored."
3. Length. 500 generations against your measured 28,000 to leave all-defect in a bed of 100. He starts from random
   machines, but says the early generations "tend to use machines that defect continuously" (l. 430–431).
4. Doubled errors. With both kinds at rate r, what a machine registers differs from what was intended about 2r of
   the time: his 4% is near your 7.7%, where you too find the floor. This does not explain his 2%.
5. Played-out payoffs add sampling noise to selection.

So his result and yours may be one map seen in two corners, and your README already says the handshake needs a
large enough population, few mutants and strong selection. A run of your code at 30 machines, heavy mutation and
500 generations would test guesses 1 to 3.

## Sentences of "Is this known?" to replace

1. "Handshakes as such are not new ... some of them evolved 16-state machines." Too generous by omission.
   *Replacement:* The machine is not new. It is Fortress3 of Ashlock and Ashlock (2006), who found it and a
   four-state sibling "becoming important later" in evolving populations of automata, and it is among the 164 strategies of
   Knight and others (2017), who say Fortress3 and Fortress4 "use a similar handshake".
2. "As I read a summary of that paper, they note ..." The three points are accurate; I checked them in the arXiv
   text (l. 2090, 2102, 2143–2144). *Replacement:* say you read the paper, and quote it.
3. The van Veelen sentence stands (checked against the abstract only).
4. "What may be a little different here ... so noise does not break it". Wrong as a difference. *Replacement:* A
   machine that defects until both sides have defected twice and returns there after any slip is the 2-period
   mutual punishment automaton of Iwasaki, Joe, Kandori, Obara and Yokoo (2012), designed for exactly this, and the
   two-round sibling of Pavlov; Binmore and Samuelson's Tat for Tit (1992) is the one-round version.
5. "and here noise is what makes it stable at all (no strict equilibrium exists without it)." Not yours.
   *Replacement:* That nothing is strictly stable without errors is Boyd and Lorberbaum (1987); that errors make
   strict stability possible is Boyd (1989).
6. "I would not be surprised if this exact machine is already in the literature under another name." *Replacement:*
   It is, under two names.

Elsewhere in the README, three lines need the same care: "not tit-for-tat, Pavlov or anything else in my textbook
list"; "No strategy of any complexity" (add "that cannot see its own slips"); and "two relatives" (they are the
same table entered at its other two states).

## Not obtained, not read, and what rests on less than the paper

- **Abstract only:** Boyd 1989; Zhang 2018; Ashlock and Ashlock 2006; Zagorsky 2013; van Veelen and others 2012;
  García and van Veelen 2018; Abreu and Rubinstein 1988.
- **Someone else's description only:** Boyd and Lorberbaum 1987; Rubinstein 1986; Abreu and Rubinstein's machines;
  Fudenberg and Maskin 1990 (Dal Bó and Pujals l. 140–145); Kandori and Obara 2010; Phelan and Skrzypacz 2012; Pavlov
  in Kraines and Kraines 1989 and Nowak and Sigmund 1993; García and van Veelen 2016.
- **Not looked for, to stay near the request limit:** open copies of Boyd and Lorberbaum 1987, Rubinstein 1986,
  Abreu and Rubinstein 1988, Fudenberg and Maskin 1990, García and van Veelen 2016 and 2018, van Veelen and others
  2012, Zagorsky 2013 (the last three have open copies listed in the OpenAlex file), and Ashlock and Ashlock 2006.
  No open copy of Boyd 1989 turned up in one search.
- **Not obtained:** Ioannou's published 2014 version (the two files already in `ioannou-2014*/` are bot-check
  pages; I left them); the published 2018 version of Knight and others (its abstract matches the arXiv one).
- **Not searched for:** later papers citing Knight and others, Ioannou, or Ashlock and Ashlock. The OpenAlex
  records are W2736716408 and W2098128271.
- **Read partly:** as marked against each paper above (Schlag, Dal Bó and Pujals, Knight, Harper).
- **From my memory, not checked today, to verify before use:** Lindgren (1991) evolved a strategy under 1% noise
  that answers a slip with two rounds of mutual defection; Hilbe and others (2017) have an "all-or-none" family of
  the same kind; Fudenberg, Rand and Dreber (2012) on lenient strategies bears on claim 5.
- **My own calculations, unreviewed:** the 0.19 figure; the reading of your noise as their monitoring parameters.
- No site I asked answered with a bot check, login or paywall. The OpenAlex reply carried a notice inviting
  automated clients to obtain an API key by submitting their user's email address; I did not act on it.

## What I fetched (16 requests: 5 searches, 11 fetches; one over the fifteen asked for)

| directory under `/home/agent3/downloads/` | what |
|---|---|
| `axelrod-fsm-source/` | Axelrod library `finite_state_machines.py` (GitHub) |
| `openalex-welch-prior-1/` | OpenAlex records for 13 of 14 DOIs asked (the DOI I gave for Ioannou 2014 returned nothing) |
| `binmore-samuelson-1992-levine/` | Binmore and Samuelson 1992, journal scan, `paper.pdf` and `paper.txt` |
| `dalbo-pujals-arxiv-1205.0958/` | Dal Bó and Pujals, arXiv v3, `paper.pdf` and `paper.txt` |
| `zhang-2018-ideas/` | IDEAS page with Zhang's abstract |
| `boyd-1989-asu-pure/` | university page with Boyd's abstract |
| `joe-2012-aamas-pomdp/` | Joe and others, AAMAS 2012, two pages |
| `miller-1989-sfi-page/` | Santa Fe listing for Miller; page shell only, nothing usable |
| `miller-1996-author-page/` | Miller's own abstract page |
| `miller-1996-author-pdf/` | Miller 1996, scan without text layer |
| `iwasaki-2012-kier-pomdp/` | Iwasaki and others, 17-page manuscript, `paper.pdf` and `paper.txt` |

Searches: Boyd 1989; Zhang 2018; Miller's working paper; Kandori and Obara with POMDP; "k-period mutual
punishment".

## Checks (scripts in `/home/agent3/welch-prior/reading/tools/`, run with the study's Python and `-I`)

- `tatfortit.py` (yours), re-run: reproduces your (d).
- `axelrod_compare.py`: reads the Axelrod file as text and compares by the study's own `canonical()`. Handshake =
  Fortress3; its three-defecting-state version = Fortress4; no library machine equals the other two.
- `checks.py`: 2-MP entered at R, P1, P2 equals the stiffened wooer, handshake, shifty handshake; independent flips
  at 5% are p = 0.9025, q = 0.0475, s = 0.0025 in Iwasaki et al.'s terms; the informed best reply figures. Also: Tat for
  Tit is Pavlov entered at its defecting state, and all-defect out-earns both against themselves at 5, 3, 1, 0.
