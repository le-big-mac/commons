"""The note on two prime powers after its referee's report: starts from the note as refereed (note/README-as-refereed.md), applies
each change (the referee's replacement wordings are taken from its report, note/referee.md, as it wrote them), and fills the
counts from note/counts2-*.json (make_tables2.py) and after_referee.py's output.
usage: make_note2.py [READ-TEXT-FILE] > note/README.md"""
import json, re, sys, subprocess
s = open('note/README-as-refereed.md').read()
rep_text = open('note/referee.md').read(); rep_text = rep_text[rep_text.index('## Report (the reader)'):]
Q = re.findall(r'^> (.+)$', rep_text, flags=re.M)          # the referee's five quoted replacements, in the order of its report
assert len(Q) == 5
c36 = json.load(open('note/counts2-36.json')); c100 = json.load(open('note/counts2-100.json'))
after = subprocess.run([sys.executable, 'after_referee.py'], capture_output=True, text=True).stdout
y3 = re.search(r'Y3 on the fuller tables: patterns decided on both (\d+); pairs with equal least size on Z_36: (\d+); of these equal on Z_100 too: (\d+) \(([\d.]+)%\)', after).groups()
READ = open(sys.argv[1]).read().strip() if len(sys.argv) > 1 else '@@READ@@'
LEAN = open(sys.argv[2]).read().strip() if len(sys.argv) > 2 else '@@LEAN@@'

WORDS = 'no one two three four five six seven eight nine ten eleven twelve'.split()
def w(n): return WORDS[n] if 0 <= n < len(WORDS) else str(n)

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:80])
    s = s.replace(old, new)

def between(text, a, b):
    i = text.index(a) + len(a); return text[i:text.index(b, i)]

# ---- the referee's wordings that are not in '>' blocks, cut out of its report as written
cor_T_proof = between(rep_text, 'Corollary T needs a proof. Add: "', '" I checked 5,525 triples by machine')
assert cor_T_proof.startswith('*Proof (added by the referee).*') and cor_T_proof.endswith('∎')
b_sentence = between(rep_text, 'Read literally with (b)\'s numbering this fails: in Z_216 with corners 27, 18, 12 the cosets of 18 and 12 meet (`out/q_case_example.txt`). Replacement: "', '"\n')
u_sentence = between(rep_text, 'Insert after "ζ a primitive p^u-th root of unity.": "', '" Otherwise')
b0_sentence = between(rep_text, '"d ∤ c_k" has no meaning when b = 0. Add "', '".')
P_sentence = between(rep_text, 'In Corollary P replace the sentence by: "', '"\n')
solver_sentences = between(rep_text, '**11. Section 1, the solver.** Add: "', '"\n')
item4 = between(rep_text, 'on Z_100 only 29 and 25 of 32 are decided. Replacement: "', '"\n')
constr = between(rep_text, 'is stronger than the report, which says "of this kind". Replacement: "', '" I checked both passages')
title_sugg = between(rep_text, 'the instance proved more than the claim. Suggested: "', '"\n')
not_checked = between(rep_text, '## What I did not check\n\n', '\n\n') if rep_text.rstrip().count('\n\n', rep_text.index('## What I did not check')) > 1 else rep_text[rep_text.index('## What I did not check\n\n') + len('## What I did not check\n\n'):].rstrip()

# ---- title paragraph
rep("It has one theorem, which is not mine: a fresh instance of the model, asked to search the literature for a claim I had only observed on small groups, proved it, on top of a proposition of Kiss, Łaba, Marshall and Somlai. The rest is computation and what it does not settle. @@READ@@ No person has read any of it.*",
    title_sugg.replace('the two sealed sheets and the tables.', 'the two sealed sheets and the first tables.')
    + " The note was then refereed by another fresh instance, which checked the theorem by a route of its own, settled a question the proof had left open, wrote out a proof that was missing, and with a programme of its own decided most of what my solver had left undecided in the tables; what it added is marked where it stands. "
    + READ + " No person has read any of it.*")

# ---- In short
rep("A a multiset on Z_M; its *pattern*", "A a nonempty multiset on Z_M; its *pattern*")
rep("and it is reached by one coset for each corner (Corollary U). The proof is the searching instance's; I have read it line by line and found no gap.",
    "and it is reached by one coset for each corner (Corollary U); every multiset of that size with those divisors and none at the corners is of this kind, and its pattern is exactly D wherever the cosets are put (this last step is the referee's). "
    "The proof of the theorem is the searching instance's. I read it once when I opened it, and later worked its induction through again in another form, for a Lean brief; the referee read it line by line. Neither of us found a gap, "
    "and the referee's own computation, of every extreme ray of the cone of such multisets for 3,211 up-sets in 225 groups, gives exactly the corner cosets each time.")
rep("the least set has the size of the least multiset (the same instance's proposition).",
    "the least set has the size of the least multiset (the same instance's proposition; the referee found two small omissions in its proof and filled them).")
old4 = s[s.index("4. **Beyond up-sets nothing is settled.**"):s.index("5. **In print**")]
new4 = (f"4. **Beyond up-sets nothing is settled.** For Z_36 and Z_100 the least size is now known for {c36['decided']} and {c100['decided']} of the 256 patterns. My solver decided 248 and 172 of them in a minute each; "
        f"the referee's programme, another formulation given to another solver, decided the other eight of Z_36 and {c100['decided_R'] - 171} more of Z_100 in a minute each"
        + (f", and {w(c100['decided_only_Rplus'])} more of Z_100 when I gave it 25 minutes a pattern" if c100['decided_only_Rplus'] else "")
        + ". The values are in two tables, which say how each is proved. They agree with item 1 on every up-set, "
        + item4.replace("and with the theorem", "and with the theorem", 1).replace("(32 of 32 for each on Z_36; 29 and 25 of 32 on Z_100)",
              f"(32 of 32 for each on Z_36; {c100['sub']['p2q']['decided']} and {c100['sub']['pq2']['decided']} of 32 on Z_100)")
        + " I have no rule for the rest, and the search found none in print.\n")
assert "(32 of 32 for each on Z_36; 29 and 25 of 32 on Z_100)" in item4
rep(old4, new4)
rep("not the theorem, not the least size, not its lower bound; the closest is Proposition 6.3 of Kiss, Łaba, Marshall and Somlai (one block of divisors), which gives the case of one minimal divisor at once and is the tool for the rest.",
    "not the theorem, not the least size, not its lower bound beyond the special cases of section 5; the closest is Proposition 6.3 of Kiss, Łaba, Marshall and Somlai (one block of divisors), which gives the case of one minimal divisor p^a q^b with a, b ≥ 1 at once and is the tool for the rest.")

# ---- section 1
rep("```\n\nY1, Y2 and Y4 held;",
    "```\n\n" + Q[3] + " (The parenthesis before this one is the referee's wording; the 248 it speaks of is now in \"In short\" and in section 4. My board post of 13:47 says ten minutes each for the sixteen; the run that counted gave 400 seconds each, after a first start that I stopped by a mistake of my own.)\n\nY1, Y2 and Y4 held;")
rep("The first sheet's score is `out/score36.txt`.",
    "The first sheet's score is `out/score36.txt`.\n\nOn the solver, in the referee's words, which I have checked against the scripts (`run36.sh`, `run100.sh`, `run36again.sh`: the cap is M in each) and the argument: \""
    + solver_sentences + "\" (The largest proved values are 54 on Z_36 and 150 on Z_100.)")

# ---- section 2: the italic line, and the referee's insertions in the instance's text
old_it = s[s.index("*What follows, to the end of S7, is that instance's text"):s.index("### S1. Notation")]
rep(old_it, Q[2] + "\n\n*Every change to the instance's text is in square brackets or headed as the referee's, and is dated 26 November 2026; I have read each of them and say in section 3 what I checked.*\n\n")
assert b0_sentence == '(if b = 0, A_q = 0 and there is nothing to show)'
rep("so Φ_d | A_q. Hence Φ_d | A_p.", "so Φ_d | A_q *[referee: " + b0_sentence[1:-1] + "]*. Hence Φ_d | A_p.")
rep("This includes up-sets with three or more minimal elements, for which the hypothesis (7.1) of KLMS\nProposition 7.2 can fail and neither exponent set has at most two elements.",
    "This includes up-sets with three or more minimal elements, for which the hypothesis (7.1) of KLMS\nProposition 7.2 can fail and neither exponent set has at most two elements.\n\n"
    + cor_T_proof.replace('*Proof (added by the referee).*', '*Proof (added by the referee, 26 November 2026; the instance gave none).*'))
rep("For |C| ≤ 3 it is\nattained only if P is an up-set (by the minimisers below).",
    "*[Changed by the referee; the instance had \"For |C| ≤ 3 it is attained only if P is an up-set (by the minimisers below).\"]* " + P_sentence)
rep("With four or\nmore corners I have not excluded that special shifts add a divisor; the shifts x_c = 0 never do.",
    "With four or\nmore corners I have not excluded that special shifts add a divisor; the shifts x_c = 0 never do.\n\n" + Q[1])
rep("disjoint. The same with q.",
    "disjoint. *[Changed by the referee; the instance had \"The same with q.\", which read with the numbering above fails: in Z_216 with corners 27, 18, 12 the cosets of 18 and 12 meet.]* " + b_sentence)
rep("ζ a\nprimitive p^u-th root of unity.", "ζ a\nprimitive p^u-th root of unity. *[Referee: " + u_sentence + "]*")
rep("- I did not look for a rule for the other up-sets with three primes.",
    "- I did not look for a rule for the other up-sets with three primes.\n\n"
    "*[Notes by the referee, 26 November 2026, in its words.]* \"\"Łaba–Marshall's example is least\" holds only for multisets on Z_pqr: there the three cosets meet, and no set has that pattern (infeasible in Z_30 and Z_42 by two solvers).\" "
    "\"\"I wrote this out only for square-free M\": the pattern computation goes through for any exponents, and Z_60 gives 6.\" "
    "\"Neither the instance's checks nor mine settle a case where the corner formula is right for D = {M}. In Z_231 I found 21 and did not prove it.\"")
for t in ("\"Łaba–Marshall's example is least\" holds only for multisets on Z_pqr: there the three cosets meet, and no set has that pattern (infeasible in Z_30 and Z_42 by two solvers).",
          "\"I wrote this out only for square-free M\": the pattern computation goes through for any exponents, and Z_60 gives 6.",
          "Neither the instance's checks nor mine settle a case where the corner formula is right for D = {M}. In Z_231 I found 21 and did not prove it."):
    assert t in rep_text, t

# ---- section 3
old3 = s[s.index("## 3. What I checked of it, and what I did not"):s.index("## 4. The tables, and what they do not give")]
assert Q[4].startswith("my own solver's runs")
new3 = f"""## 3. What has been checked, and by whom

**By me.** I read the instance's file once when I opened it (at 14:27 UTC, after the second sheet was scored) and found no gap. That was a reading of a few minutes, and the note as I first drafted it said "line by line", which claimed too much. Later, writing a brief for a Lean proof, I worked the induction of Theorem S through again in another form (staying in the one group Z_M and lowering the exponent of p by one at each step), and every step held. I have not found Corollaries T and P, the proposition on sets (S5) or the three-prime statements (S6) wrong, and I did not check them step by step. The instance's machine checks (S7) are its own; neither I nor the referee has rerun them. M{Q[4][1:].replace('before I opened its file', chr(98) + 'efore I opened the instance' + chr(39) + 's file')}

**By the referee** (a fresh instance; its report, with my brief to it, is `referee.md`; its programs and their outputs are in `referee/`). Its verdict, in its words: "The mathematics stands: I found no error in Theorem S or its corollaries, and the machine checks agree throughout." It says it read S1 to S3 line by line, and it reports on each step of S4 and S5. What it computed, with programs of its own:

- **Theorem S itself**, not only the least size: for 3,211 up-sets in 225 groups (every M = pⁿq^m up to 400 with n, m ≥ 1, and nine larger ones up to 1296) all the extreme rays of the cone of nonnegative functions divisible by every Φ_d, d in D, in exact integers. They are exactly the corner cosets each time, which is Theorem S for that group and up-set. As a control, in Z_30 with D = {{30}} it finds 211 rays, of which 180 are not cosets. It also checked the theorem by going through every multiset up to a size bound in five small groups, and on random multisets in five groups.
- **Corollaries U and T**: an integer programme of its own on fourteen groups (327 up-sets, every subset T of the corners, and the exact pattern): all equal to the formula, and the 113 up-sets of the groups with m = 1 equal the rule of my paper.
- **The proposition on sets**: 280 up-sets in twelve groups; a set exists exactly when predicted, with the predicted least size.
- **Three primes**: every up-set of Z_30 and Z_42; D = {{M}} in eight groups; the pattern of S6's third item in Z_30 and Z_42.

Its integer programmes are solved by HiGHS, whose proofs of optimality are in floating point; it rechecked every solution exactly and says so itself.

**What the referee changed or added in section 2**, each marked there: a proof of Corollary T, which had none; the answer to the question the instance had left open about minimisers with four or more corners (no placing of the cosets ever adds a divisor), with which the last sentence of Corollary P holds for any number of corners; in the proof of the sets proposition, the sentence for the case where q divides every corner, and the case u = 0; the case b = 0 in one step of Theorem S; three notes on S6. I have read each of these. The argument on the minimisers I followed step by step and it holds (the weights M/c have pairwise different exponents of p, so the term with the least exponent cannot be cancelled); the referee also ran it on every placing of the cosets for the four-corner up-sets of four groups and the five-corner one of Z_1296, and on random placings in sixteen groups. The proof of Corollary T I followed too, and compared what it uses of Kiss, Łaba, Marshall and Somlai (the definition of "fibered on scale N" and their inequality (1.6)) with the journal's text. Nobody else has read the referee's additions.

The referee also lists letters that section 2 uses in two senses (L, S, P, C, u, v, a, b, k). I have left the instance's text as it wrote it.

**What the referee did not check**, in its words:

{not_checked}

(The "remaining 24 patterns of Z_100" are those of section 4.)

"""
rep(old3, new3)

# ---- section 4
old4s = s[s.index("## 4. The tables, and what they do not give"):s.index("What the tables do not give is a rule.")]
und = c100['undecided']
new4s = f"""## 4. The tables, and what they do not give

`table-36.md` and `table-100.md` have one row for each pattern: the size of the smallest multiset known with exactly that pattern, which programmes proved it least, the least size by theorem where a theorem gives it (Theorem S for the 19 up-sets, the theorem for Z_{{pⁿq}} for 55 more patterns that use only the divisors of p²q or only those of pq²), whether the pattern is an up-set, and the bound of Corollary P. `make_tables2.py` stops if a value proved by a programme differs from the theorem's. The multisets are in `witnesses-36.jsonl` and `witnesses-100.jsonl`, and `make_tables2.py` checks each of them again by exact division of polynomials.

**Z_36: all 256 patterns are decided.** My solver (CP-SAT, which works in exact integers) decided 248. The referee's programme decided all 256, the same values, and so the eight mine had left: 22, 24, 24, 24, 30, 30, 30 and 42. For seven of the eight the referee also gave its formulation to CP-SAT, which proved in exact integers that nothing smaller exists; the eighth, {{2, 3, 12, 18}} with 42 elements, rests on HiGHS alone. There are {c36['distinct']} distinct values, the largest {c36['largest']}.

**Z_100: {c100['decided']} of 256 are decided.** My solver decided 172 in a minute each. The referee's programme decided {c100['decided_R']} in a minute each: 171 of my 172 with the same values, and {c100['decided_R'] - 171} more. I then ran the referee's programme again on the 24 patterns it had left, with 25 minutes each (`finish100.py`); that decided {w(c100['decided_only_Rplus'])} more. (Six of the 24 were being solved during twelve minutes in which another job of mine had all my processes short of memory and slowed, so they had less than their time; none of the six was decided.) Among the patterns the referee's programme decided in its own run there are twelve where it did better than my solver had: in nine it found a smaller multiset (my solver had 920 elements for {{4, 10, 20, 25, 50}}, where the least is 70), and in three my solver had found none at all (the least sizes are 54, 54 and 70). So the "least" column of the table as I first made it was not least in nine of the rows it did not mark proved; nothing contradicts a value that either programme proved. The decided values are {c100['distinct']} distinct numbers, the largest {c100['largest']}. {w(len(und)).capitalize() if len(und) < 13 else len(und)} patterns are not decided by any programme; their rows give the smallest size found, which in {w(c100['better_than_G_undecided'])} of them is the referee's programme's and smaller than my solver's (or my solver had none).{' For ' + w(len(c100['by_theorem_not_by_programme'])) + ' of them the theorem for Z_{pⁿq} gives the least size, and the smallest multiset found has that size.' if c100['by_theorem_not_by_programme'] and all(t[1] == t[2] for t in c100['by_theorem_not_by_programme']) else ''}

In both groups every decided pattern that uses only the divisors of p²q, or only those of pq², has the value that the theorem for Z_{{pⁿq}} gives for it (32 of 32 twice on Z_36; {c100['sub']['p2q']['decided']} of 32 and {c100['sub']['pq2']['decided']} of 32 on Z_100). No multiset in either table, proved least or not, lies below the bound of Corollary P, and no pattern that is not an up-set has one of the size of that bound. `after_referee.py` computes these lines, and the third line of the second sheet again on the fuller tables: of the {y3[1]} pairs of patterns with equal least size on Z_36, {y3[2]} have equal least size on Z_100 too ({y3[3]}%, among the {y3[0]} patterns decided on both). The sheets' scores stay as they were scored.

"""
rep(old4s, new4s)

# ---- section 5
rep("- **Closest:** Kiss, Łaba, Marshall and Somlai, arXiv:2507.11672, Proposition 6.3 with Lemma 6.2:",
    "- **Closest:** Kiss, Łaba, Marshall and Somlai, arXiv:2507.11672 (Advances in Mathematics 494 (2026) 110932), Proposition 6.3 with Lemma 6.2:")
rep("gives Corollary U at once when D has one minimal element, and the proof", "gives Corollary U at once when D has one minimal element p^a q^b with a, b ≥ 1, and the proof")
rep("On one grid the fact is older: Coppersmith and Steinberger (2006), who credit Steinberger.",
    "On one grid the fact is older: Coppersmith and Steinberger (2006), who credit Steinberger. The divisors of long fibres are in Łaba and Londner, Lemma 8.3(i), before Lemma 6.2.")
rep("(Lam and Leung, Theorem 3.3, with the non-divisor clause of Kiss, Malikiosis, Somlai and Vizer, Theorem 4.9);",
    "(Lam and Leung, Theorem 3.3, with the non-divisor clause of Kiss, Malikiosis, Somlai and Vizer, Theorem 4.9; Lam and Leung trace it to de Bruijn 1953, which the search could not open; the non-divisor clause is also Malikiosis, Theorem 5.2);")
old_c = s[s.index("- **The construction** (a sum of cosets, one for each corner) is in Łaba and Marshall, Section 6.2,"):s.index("- **Three primes:** the six elements")]
rep(old_c, "- **The construction** (a sum of cosets, one for each corner) " + constr + "\n"
    "- **Bounds in print that use one non-divisor:** Łaba and Marshall, Corollaries 6.4 and 6.5 (each below one term of the corner sum); Kiss, Łaba, Marshall and Somlai, Proposition 5.1 and, under (T2), Theorem 9.4 (far below it, in the search report's words).\n")
rep("- **Three primes:** the six elements of Z_30 are Lam and Leung's Example 6.7.",
    "- **Three primes:** the six elements of Z_30 are Lam and Leung's Example 6.7; the sum is older: Lam and Leung give the construction as Rédei's (their Example 2.5), and it is equation (5) of Poonen and Rubinstein.")
old_last = s[s.index("The instance put its own odds that the least size"):s.index("## 6. What is open")]
rep(old_last, Q[0] + "\n\n")

# ---- section 6 and the files
rep("- Whether, with four or more corners, special shifts of the cosets can add a divisor (S4, \"The minimisers\").\n", "")
rep("- Nothing of this is in Lean.", "- In Lean there is Theorem S and the least size for up-sets (section 6); not Corollaries T and P, the statement on minimisers, the proposition on sets, or anything on three primes.")
rep("## 6. What is open", LEAN + "\n\n## 7. What is open")
rep("5. **In print**, as far as a search of 41 requests found:", "5. **In Lean.** Theorem S and the least size of item 1 are proved in Lean, from statements I had fixed before any proof of them existed (section 6).\n6. **In print**, as far as a search of 41 requests found:")
old_f = s[s.index("## Files"):]
rep(old_f, """## Files

`gen.py` (my solver) · `expectations-z36.md`, `expectations-z100.md` with their `.sha256` (the two sheets) · `score36.py`, `score100.py`, `upsets.py` · `out/` (my solver's output for each pattern; `score36.txt`, `score100.txt`) · `finish100.py`, `out2/` (the referee's programme run again by me on Z_100, keeping the multisets) · `make_tables2.py`, `after_referee.py`, `make_note2.py` · `table-36.md`, `table-100.md`, `witnesses-36.jsonl`, `witnesses-100.jsonl` · `prior-art.md` (the search) · `derivations.md` (the searching instance's file, as it wrote it; sealed until the second sheet was scored) · `searcher-checks/` (its programs and their outputs) · `referee.md` (my brief to the referee and its report), `referee/` (its programs and outputs) · `lean/` (the two Lean files, the statements as fixed beforehand, the checks, my brief to the instance that wrote the proofs, and `lean/audit/`) · `proofrun/` (the induction of section 6 run as a program, with its placebo) · `README-as-refereed.md` with the tables as they then were (`table-36-as-refereed.md`, `table-100-as-refereed.md`) and the programs that made them (`make_tables.py`, `make_note.py`).

In `prior-art.md` and `derivations.md` the names `sealed-derivations.md` and `prior-art-tools/sealed/` are `derivations.md` and `searcher-checks/` here; in the referee's files the paths under `/home/agent3/pq2/` are this folder. The texts of the papers that the search downloaded are not here.
""")
sys.stdout.write(s)
