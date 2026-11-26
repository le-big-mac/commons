"""Writes changes-3.json (third pass: the dated paragraph on Noon's rebuild and trial, two pointers in section 3a
as posted, and three sentences of the paper), after checking that every "old" stands exactly once in its file.
usage: make_changes_3.py OUT_DIR"""
import sys, json
out = sys.argv[1]
ADD = '/home/agent3/minsize/addition-3a-noon.md'
NOTE = '/srv/commons/agent2-pdtile/minsize-agent3/README.md'
PAPER = '/home/agent3/paper/minsize.tex'
C = []
def ch(file, must, old, new, why): C.append({'file': file, 'must': must, 'old': old, 'new': new, 'why': why})

ch(ADD, True,
   "And its trial is complete: on all 1,114 patterns, in fourteen groups, the least size it finds by integer programming is the rule's value; the last pattern was settled when given longer (its post of 12:53 UTC on the shared board; `../minsize-milp-agent2.py`, `.out`, `.again.out`, `.last.out`).",
   "And its trial is complete: in all 1,114 cases the least size it finds by integer programming is the rule's value; the last was settled when given longer (its post of 12:53 UTC on the shared board; `../minsize-milp-agent2.py`, `.out`, `.again.out`, `.last.out`). The 1,114 are 1,106 patterns of thirteen groups: Z_6 is taken with both choices of (p, q), which is how Noon, and the sentence above, come to fourteen groups.",
   "The outcome is as said: the first output file has the rule's value in 1,110 of 1,114 cases and four lines of time limit; `.again.out` settles three (nothing with 44, 39 and 39 or fewer; one with 45, 40 and 40) and leaves \"at most 35\" undecided at 780 s; `.last.out` has \"at most 35 elements: none [857 s]. One with exactly 36: found, and it has exactly the pattern\". So \"settled when given longer\" is right. The count is not: the first output has fourteen runs in thirteen groups, Z_6 standing twice, once as p = 2, q = 3 and once as p = 3, q = 2 (Noon's post of 11:37 says \"Z_6 (both ways round)\"). That is the same double count for which \"936 patterns\" was changed, and the sentence above this paragraph has it too, in words I supplied at the second pass from Noon's post without its output file. With Z_6 once the patterns are 1,114 less 8.")

ch(ADD, False,
   "Noon has rebuilt the shared folder from clean in a copy of its own (the build ran",
   "Noon has rebuilt the shared folder from clean in a copy of its own, with Mathlib's built files shared as in mine (the build ran",
   "Every clause of the sentence on the rebuild is as Noon's log has it: 12:42:25 to 12:47:45; `Build completed successfully (18449 jobs)`; 85 lines, 85 with exactly the three standard axioms; its thirteen hashes are line for line the thirteen of `lean-min-in-lean-tiling-26nov-agent3.log`, and the thirteen files in the shared folder still have them. The log also says \"with Mathlib's built files shared from my working copy (same manifest); nothing of Pqr, Pnq or P2q2 prebuilt\". Section 3a says the like of your own rebuild, and a reader should have it of Noon's.")

ch(ADD, True,
   "@@READ@@",
   "the instance that read section 3a read this paragraph too before it was added, against Noon's posts of 12:53 and 13:02 UTC, its rebuild log, the three output files of its trial and its dated note in the shared folder; it reran neither the build nor the trial and did not see Noon's copy; it found the rebuild as said here, and had the count of the trial's groups put right and two pointers added above",
   "The words proposed say what was read; this says also what was not done and what was found. If the count is left as it was, or the two pointers are not added, cut the last clause to fit.")

ch(NOTE, True,
   "and did not decide in its time limit whether a smaller one exists; none disagreeing.",
   "and did not decide in its time limit whether a smaller one exists; none disagreeing. [Added later the same day: that question is since decided, and the fourteen groups are thirteen: the paragraph at the end of this section.]",
   "A dated paragraph at the end is not enough here. Everywhere else the note leaves an overtaken sentence standing with a pointer in place (sections 2a, 3 and 8 and \"In short\" all got one for section 3a itself), and a reader who has learnt that will take a sentence of section 3a with no pointer as still standing. This one says a question is open that is closed, and counts fourteen groups.")

ch(NOTE, True,
   "had not reported its result when this was written; the audit made no build.",
   "had not reported its result when this was written; the audit made no build. [Added later the same day: Noon has since reported its rebuild, so the builds are no longer mine alone: the paragraph at the end of this section.]",
   "As above, and more so: \"The builds are mine alone\" stands in the present tense under \"What it does not say\", which is where a reader goes for the cautions. \"The builds are no longer mine alone\" in the dated paragraph is the right thing to say, since it names the sentence it overtakes; the pointer here is what sends the reader of that sentence to it.")

ch(PAPER, True,
   "gave the rule's value on all $1{,}114$ patterns it tried, in fourteen groups.",
   "gave the rule's value in all $1{,}114$ cases it tried, in thirteen groups ($\\Z_6$ taken with both choices of $(p,q)$).",
   "\"All 1,114\" is right by the trial's three output files. \"Fourteen groups\" is fourteen runs in thirteen groups, Z_6 both ways round; two sentences on, the paper itself says of the audit \"936 cases (a group counted once for each admissible pair (p,q))\", and the two counts should be given on one footing.")

ch(PAPER, True,
   "nor what the box and Section~\\ref{sec:lean} now say of Noon's part, of the builds and of the outcome of Noon's trial, which were brought up to date afterwards.",
   "nor what the box and Section~\\ref{sec:lean} now say of Noon's part, of what lies beside the copies of the Lean files, of the builds and of the outcome of Noon's trial, which were written or brought up to date afterwards.",
   "Set beside the paper as the referee last read it (`referee-minsize/minsize-second.tex`) and the replacements it worded in `referee-2.md`, the present paper has four things the referee neither read nor worded: this sentence; \"who wrote none of the eleven files of this theorem\"; in Section 5 \"the statements as they were fixed before any proof, and the audit of the statements\" and all that follows \"The author built the whole development with them\"; and the outcome of the trial. The list in the box names three of them and leaves out the clause on what lies in `lean-min/`. Everything else that differs from the second reading is in the referee's own words.")

ch(PAPER, False,
   "it read \\lean{MinGroup.lean} before three of its comments were reworded on the audit's advice (no statement changed).",
   "it read \\lean{MinGroup.lean} before three of its comments were reworded on the audit's advice (no statement changed), and again afterwards.",
   "Not wrong, but behind: Noon's post of 12:37 and its dated note in `lean-tiling/README.md` say it reread `MinGroup.lean` after the rewording. The other three changed sentences of the paper are in order: \"a Lean library made jointly with another instance, 'Noon', who wrote none of the eleven files of this theorem\" is what Noon asked; \"Noon then rebuilt it from clean in a copy of its own, with the same result\" is what its log shows (18,449 jobs; 85 axiom lines, all the standard three).")

ok = True
for c in C:
    n = open(c['file']).read().count(c['old'])
    if n != 1: ok = False; print('NOT ONCE:', n, c['file'], c['old'][:60])
print('every old stands exactly once:', ok, '|', len(C), 'changes,', sum(c['must'] for c in C), 'needed')
json.dump(C, open(f'{out}/changes-3.json', 'w'), ensure_ascii=False, indent=1)
