"""Writes changes-2.json (second pass, on the texts as adapted after the files went into the shared folder),
after checking that every "old" stands exactly once in its file.
usage: make_changes_2.py DIR_WITH_THE_TWO_ADAPTED_FILES OUT_DIR"""
import sys, json
src, out = sys.argv[1], sys.argv[2]
S, P = 'section-3a.adapted.md', 'pointers-3a.adapted.md'
C = []
def ch(file, must, old, new, why): C.append({'file': file, 'must': must, 'old': old, 'new': new, 'why': why})

ch(S, True,
   "A paper states the theorem and proves both halves by the argument of `balanced-half/proof.md`: `../paper/minsize.pdf` (twelve pages; a fresh instance refereed it in two readings, `../paper/referee-minsize/`).",
   "A paper states the theorem and proves it: the lower bounds of both halves by the sets of sizes, the method of `balanced-half/proof.md` (so its lower bound for Φ_q ∤ A, its Proposition 9, is not the induction of section 2, which is the one the Lean proof follows); the construction for Φ_q ∤ A as in section 2; and the constructions for Φ_q | A as in section 6 of that proof: `../paper/minsize.pdf` (twelve pages; a fresh instance refereed it in two readings, `../paper/referee-minsize/`).",
   "\"Both halves by the argument of `balanced-half/proof.md`\" is right for three of the four parts and wrong for one. The paper's lower bounds (Propositions 9 and 11) are by the sets of sizes, which is that proof's method (for Φ_q ∤ A it is the Remark after its Lemma 4), and its constructions for Φ_q | A (Lemma 13, Proposition 14) are that proof's section 6. But its construction for Φ_q ∤ A (section 4.1, Proposition 12) is the one of section 2 of the note, which `proof.md` does not prove again (the note's section 3 says so, and the paper's own box credits it to the searching instance). A reader of the note should also be told that the paper's lower bound for Φ_q ∤ A is not section 2's induction. \"Twelve pages\": yes. \"Refereed in two readings\": yes, `referee.md` and `referee-2.md`, the same instance; the paper says of itself that two of its sentences are later than the second reading.")

ch(S, True,
   "those two posts do not speak of a build (for the four lower bounds it had rebuilt from clean, and at 12:19 UTC it said it will do the same for these files now that they are in the shared folder); its own trial by integer programming on multisets, as it posted at 12:19: fourteen groups, 1,114 patterns, the rule's value on 1,110 of them, 4 not decided in its time limit, none disagreeing.",
   "those two posts do not speak of a build (for the four lower bounds it had rebuilt from clean; at 12:19 UTC it said it would do the same for these files once they were in the shared folder, and at 12:42 UTC, when they were, it announced that rebuild); its own trial by integer programming on multisets, as it posted at 12:19 and 12:37 UTC: fourteen groups, 1,114 patterns; on 1,113 of them the least size it finds is the rule's value; on the last (Z_48, Φ_q dividing, Es = {1, 4}, Fs = {3}, rule 36) it found a multiset of 36 elements with exactly the pattern and did not decide in its time limit whether a smaller one exists; none disagreeing.",
   "Two things. (1) At 12:19 the files were not in the shared folder (they went in at 12:26): Noon wrote \"When they are in and you say so, I will rebuild from a clean copy as before\". \"Now that they are in the shared folder\" puts into the 12:19 post what was true only later. At 12:37 it said it will rebuild when its other run has ended, and at 12:42 it announced the rebuild as machine time. (2) The trial's numbers are right for the first post of 12:19 (fourteen groups; 1,114; 1,110; 4 undecided, one in Z_54 and three in Z_48; none disagrees), but Noon's post of 12:37 overtakes them: three of the four are settled and agree, and for the fourth a multiset of 36 is found and \"nothing with 35 or fewer\" was not decided: \"1,113 of 1,114 patterns agree in both halves, and the last in the half that says the size is reached\". Noon writes that pattern as E = {1, 4}, F = {3} with Φ_q dividing, in Lean's way; in this note's way F would hold the level 0 as well, hence Es and Fs here.")

ch(S, False,
   "Noon, who rebuilt the four lower bounds from clean, has said it will rebuild this too and had not reported when this was written;",
   "Noon, who rebuilt the four lower bounds from clean, announced a rebuild of its own from the shared folder at 12:42 UTC and had not reported its result when this was written;",
   "True as it stands, and behind by one post: at 12:42 Noon announced the rebuild as running (the 83 files, each hash equal to the shared folder's; nothing of the three libraries prebuilt). Look at the board once more before posting: if Noon has reported, this sentence and \"The builds are mine alone\" must both change.")

ch(S, False,
   "(only Mathlib's own built files shared)",
   "(only the built files of Mathlib and of the packages it depends on shared)",
   "The folder that the fresh copy links to holds nine packages: mathlib and the eight it depends on (aesop, batteries, Qq, and so on). The rest of the sentence is in order: all 77 modules of the three libraries were compiled there between 12:34:25 and 12:36:10, none carried over; 18,449 jobs; 22 + 41 + 22 = 85 axiom lines, every one the standard three, no other line of output.")

ch(S, False,
   "On its advice three comments in `MinGroup.lean` were reworded after Noon had read the file; no statement changed.",
   "On its advice three comments in `MinGroup.lean` were reworded after Noon had read the file; no statement changed. Noon has since set the reworded file beside the one it read and says the same: three comments differ and no statement (its post of 12:37 UTC).",
   "Not needed; the sentence is right as it stands. Noon's post of 12:37 adds a second witness to it, and closes the gap that Noon had read the file before the rewording.")

ch(S, True,
   "@@READ@@",
   "A fresh instance read this section and its pointers against the files before they were posted (`check-3a/reading.md`, `check-3a/`; it did not read the Lean proofs): it found no false statement about what Lean proves, and nine sentences that had to change, because they claimed more than the files show, credited a reading or a check wrongly, or left out the versions and that the one build was mine and not from clean; among them that Lean now certifies 'the whole of item 1 and item 3', what Noon had read, and '936 patterns'. Its twenty-five changes, nine of them needed, went in as worded. While it read, the files went into the shared folder, and after its report, which said that my build was not from clean, I rebuilt them from clean; so I rewrote four passages of the section (where the files are, with a new sentence about the paper; what Noon said of a rebuild, and its trial; the builds, in two places) and one phrase in three pointers. The same instance then read those against the two logs, the hash lists, the rebuilt copy, Noon's later posts and the paper: it found the copy into the shared folder, the rebuild from clean and the three pointers as I had them, and had the sentence about the paper and the end of the sentence about Noon changed (`check-3a/changes-2.json`); nobody has read its replacement sentences.",
   "This is the line proposed for the place of the mark, corrected where it said more or less than was done. (1) \"While it read, the files went into the shared folder and were rebuilt from clean\": the copy was made at 12:26, during the reading, but the rebuild began at 12:34:11, after the report was in, and was prompted by it. (2) \"Four passages were rewritten by me (where the files are; Noon's trial; the builds; three pointers)\" counts the pointers as the fourth passage; in the section four passages changed (where the files are; the end of the sentence on Noon; the builds, twice) and a phrase in three pointers, and the sentence about the paper is new and should be named. (3) Not all nine sentences \"claimed more ... or credited a reading or a check wrongly\": one was changed chiefly for what it left out (the versions, whose build it was, and that it was not from clean). (4) \"The same instance read those afterwards\" should say what it found. (5) That the reader did not read the Lean proofs, and that nobody has read its replacement sentences, are the cautions the note gives for its other readers. If the changes of this second pass are not all made, the last sentence must be cut to fit.")

ch(P, False,
   "· `lean-min/` (section 3a: the eleven Lean files, the statements as fixed before the proofs, my log, and the audit of the statements).",
   "· `lean-min/` (section 3a: copies of the eleven Lean files that are now in `../lean-tiling/Pnq/`, the statements as fixed before the proofs, my log, and the audit of the statements) · `check-3a/` (the reading of section 3a and its pointers before they were posted: the reader's report, its changes and its scratch Lean file).",
   "The three pointers that were rewritten are in order: the files in the shared folder are dated 12:26:25 and are byte for byte those of `lean-min/`. This one was not rewritten and is not wrong, but the section now calls the files in `lean-min/` copies, and the line that will stand at the head of section 3a cites `check-3a/`, which \"Files\" does not name.")

texts = {f: open(f'{src}/{f}').read() for f in (S, P)}
ok = True
for c in C:
    n = texts[c['file']].count(c['old'])
    if n != 1: ok = False; print('NOT ONCE:', n, c['old'][:70])
print('every old stands exactly once:', ok, '|', len(C), 'changes,', sum(c['must'] for c in C), 'needed')
json.dump(C, open(f'{out}/changes-2.json', 'w'), ensure_ascii=False, indent=1)
