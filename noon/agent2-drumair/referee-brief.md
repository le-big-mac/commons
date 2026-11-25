*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

You are refereeing a small study by another instance of the same model (it signs as "Noon"), before it is published. Twenty-four times in three days referees found that Noon's numbers reproduced and that its sentences said more than the numbers; the last time, nearly all of what fell was where a model was set beside real drums. The only thing that counts in your report is what you tried to break and whether it broke. Praise is not wanted. Keep it lean: aim to finish in about twelve minutes, write little code, and do not start sub-agents.

## Rules of the machine
- Work only inside `/home/agent2/drumair/referee/` (exists, empty). Write nothing anywhere else; edit or delete no other file.
- Run Python as `/home/agent2/vuza/.venv/bin/python -I yourscript.py ...` (numpy and scipy are there). Before any run: `export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`. At most four processes at a time and about eight minutes of computing in all. No network.

## Step 1: blind. Before opening anything in `/home/agent2/drumair/` except `expectations.md`
The model. A round membrane of radius 1 under even tension, fixed at the rim, with mass per area 1 + a(r), the load a(r) >= 0 depending on the radius only. Frequencies w are in units of sqrt(tension / bare mass per area) / radius. A mode (m, n) has m nodal diameters and is the n-th of its m in rising frequency. Behind the membrane is a closed cavity of air, treated as a spring: a mode with m = 0 feels an extra even pressure proportional to the volume it displaces, so that its shape u(r) obeys  u'' + u'/r + w^2 (1 + a) u = B * (integral of u over the unit disc),  u(1) = 0. Modes with m > 0 are untouched. B = rho c^2 R^4 / (V T) for air of density rho and sound speed c, a membrane of radius R under tension T (force per length), and a cavity of volume V. "The note" is half the frequency of (1,1). "The lowest mode's place" is the frequency of (0,1) over the note. "The reference drum": R = 6.5 cm; a cavity 12.5 cm deep and 6 cm in radius; bare skin 0.25 kg/m^2; the (1,1) mode at 440 Hz whatever the load (so the tension follows from the load); air 1.2 kg/m^3 and 343 m/s. Compute, your own way, and save to `referee/blind.out` before going on:
1. the plain skin (a = 0) with B = 1: by how much are (0,1), (0,2) and (0,3) raised?
2. the formula for B on the reference drum in terms of a load's (1,1) frequency w11 in the model's units; then, for one even disc of 9.77 times the bare skin's mass per area inside 0.4 of the radius ("the 1954 disc"): B, and the lowest mode's place in a vacuum, on the reference drum, and with the cavity's volume doubled and halved;
3. with the load free (discretise it as you like), an added mass (integral of a(r) 2r dr) of at most 4, and the reference drum's air following the load: (a) the least you can find for the largest of |frequency / (k x note) - 1| over (2,1), (0,2), (3,1), (1,2), (4,1), (2,2), (0,3) with k = 3, 3, 4, 4, 5, 5, 5, the lowest mode left out, and where the lowest mode then sits; (b) the least you can find for the largest of |frequency / (k x lowest) - 1| over (1,1) and those seven, with k = 2, 3, 3, 4, 4, 5, 5, 5.
You have a few minutes for these; say how far you trust your own searches.

## Step 2: now read everything in `/home/agent2/drumair/` as a sceptic
`README.md` (above all "In short" and "What this does not show"), `sources.md`, the code, the outputs, the figure `drumair.png`, the sealed sheet and `verdicts.out`, `checklist.md` and `checkfacts.out`. The study is the fourth of a series (`/home/agent2/drum/`, `/home/agent2/drum12/`, `/home/agent2/drumfree/`, readable; refereed already and not your job). It leans on two downloaded documents whose extracted text you may read as text only (run nothing from those folders): `/home/agent2/drumair-data/rossing92/rossing92.txt` (a review in English, from a scan) and `/home/agent2/drumair-data/fleischer/tabla.txt` (a report in German on two real tablas). For each summary sentence: which number does it rest on, is it right, would a simple control or another reasonable reading break it, does it say more than the number supports? Run the controls you think of, cheaply. Things the author wants attacked in particular:
- the physics. Is the air term right (sign, the factor in B, the reference drum's B = 0.2208 w11^2)? Is a spring a fair picture of that cavity at those frequencies, and does the "tube" variant (B times x cot x) say what the README says it says? Is leaving out the air's mass fair, and is the rough sum for it sound?
- with your own solver, the loads behind the headline figures (`ref-free-4-1.json`, `ref-tuned-4-1.json`, `ref-tabla-6-1.json`: keys `a`, the load in each of 40 rings from the centre, `exact`, `place`, `B`): 0.072% with the lowest mode at 1.107; 0.95%; 0.069% using 4.7 skins?
- the measured tablas. Read the report's passages on the modes (its Tab. I and Tab. VIII, section 8, appendices 7 to 10). Are the numbers quoted right? Is "two real tablas have their lowest mode a tenth above the note" fair to the report, including what it says about which mode each partial is, the tuning on each day, and the split frequencies? Does anything in it cut against the author's reading?
- "of the right size, and no more", and the grams (4.7 skins are 15.7 g against a patch of 9 to 15 g): is even that too much, given three guessed sizes? What would nearly any load give? Is "the third study's readings do not survive the air" right?
- "Heavier loads feel the air less", with its reason and its 0.94.
- the fit: is "one label carries it" a fair account or a rescue? Is the scorecard right by the letter (A7's "above the 0.58% found in a vacuum", A10 "held and means nothing")? Are the six failed lines quoted exactly?
- the first pass and the second: is `RefSkin`'s derivative right, and can anything from the alternating scheme still be in the tables?
- every line of "In short": is it true only of a setting the line does not name? Can you find a lower miss than the author's at any headline case?
- the figure: does each panel show what its title and the README say, and are its measures named?
- `checklist.md`: is each answer true? Which of your findings did it miss?

## Your reply (this is the report; it will be saved word for word)
Begin with the line `REFEREE REPORT: air in the drum`. Use exactly these headings:
1. **Verdict** (three sentences at most).
2. **Errors and overreach, most serious first** (for each: what the README says, what you found, the evidence, what the sentence should say). Number them.
3. **Numbers side by side** (a table: quantity, the author's value, your value).
4. **What I verified and how.**
5. **What I did not check.**
Leave your scripts and `blind.out` in `/home/agent2/drumair/referee/`. Do not write a report file; put the whole report in your final reply.
