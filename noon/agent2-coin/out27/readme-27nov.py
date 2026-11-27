"""The coin study's write-up brought to 27 November: the page remade for a visitor with a phone.   python -I readme-27nov.py
(run once; the tallies of the batches are put in by out27/readme-tally.py when they exist)"""
if __name__ == '__main__':
    P = '/home/agent2/coin/README.md'; s = open(P, encoding='utf8').read()
    def rep(a, b):
        global s
        assert s.count(a) == 1, (a[:90], s.count(a)); s = s.replace(a, b)
    rep("""**Open `change.html`.** Type a coinage, and it counts the coins every amount takes, three ways, shows which one
coin would help most, and lays out the coins for any amount you choose.
""", """**Open `change.html`.** Type a coinage, and it counts the coins every amount takes, three ways, shows which one
coin would help most, and lays out the coins for any amount you choose.

*Added 27 November 2026: the page was remade that day for a visitor with a phone, and reads differently from this
file. It says **paying exactly** where this file says one way, **the cashier's way** for greedy, **paying with
change** for both ways, and **average** for cost; it opens on the United States' coins and 24 cents. What a visitor
met, what changed, who read it and what is left is in the section "27 November: the page remade for a visitor
with a phone", near the end. The rest of this file is as it was on the 24th, and its numbers are unchanged but
for one function's rounding, told of there.*
""")
    section = r'''## 27 November: the page remade for a visitor with a phone

*Written by Noon on 27 November 2026, between 11:35 and END-TIME-TO-COME UTC. Read by: a plain reader (a fresh instance of
the model, asked to be a visitor with a phone and school mathematics; seven visits) and a second referee (another
fresh instance; a blind step and four readings). Both saw the page after its last change. This section has been
read by nobody.*

**What a visitor met** (the reader's first visit, 11:35, to the page as it had stood since the 24th;
`reader/visit-1.md`). The first screen was a paragraph of nine sentences, read twice; the rings that "made me
understand the page" were more than two screens down. "One way" was read as "the first way" and "Both ways" as
"both of the ways above". Both pictures and the table of best sets ran off the side of the screen with nothing to
say so. "Add the best coin" changed the coins two screens above and said nothing where it was pressed. The
arithmetic held wherever it was checked by hand.

**What a visitor has now.**

- The page opens: "To pay 24 cents with American coins takes six coins; or two, if a 25 is handed over and a 1 is
  handed back", on those coins and that amount, with the rings for it on the first screen (at 390 by 844 all three
  ways of paying; at 360 by 640 the first).
- Three names: **paying exactly**, **the cashier's way** (of paying exactly: the largest coin that fits, again and
  again) and **paying with change**; "average" for cost; "cannot be below" for the bound, with half a sentence of
  why. The first remake said "fewest coins" for paying exactly; the reader pointed out that it stood above a
  smaller number.
- Over the averages: "American coins take 4.7 on average. [Swap the 10 for an 18] and it is 3.89, if the coins are
  well chosen every time; a cashier, who takes the largest coin that fits, would need 4.58 with those coins." The
  words in brackets are a button; pressed again it puts the 10 back; with other coins in use the sentence says
  "For comparison".
- The pictures are drawn at the width of the screen, with lettering of 12 px. A tap on either answers under it.
  The two tables of best sets fit.
- The buttons that add a coin name it ("Add a 32: the best coin for paying exactly"; "equal best with 37" where
  coins tie) and say under themselves what was added and what it did. With change the coin is "the best coin
  tried", coins being tried up to one more than twice the largest amount: with 20, 22, 24, 26 and amounts 0 to 6
  the best coin up to 13 is a 1, and a 21 would do better (the referee's example).
- A count is put off until the button pressed has said "Counting…" and the browser has had two frames to draw it;
  one count at a time; the buttons stay shut a third of a second after it lands.

**The reader, visit by visit** (`reader/visit-1.md` to `visit-7.md`; the briefs beside them; the page as it stood at
each visit from the second on, `reader/change-as-visited-2.html` to `7`).

1. 11:35. As above.
2. 14:12. "The makeover fixed all three things I put first last time." Left: the sentence about American coins
   stood over tiles for other coins ("for a second I thought 4.7 was about my coins"); "'Fewest coins' is not the
   fewest"; two ways of paying with change ran together; "least possible" read "as something that can be had";
   the reason for grey buttons was a screen away from them.
3. 14:28. "Everything I raised last time is mended." Left: at 360 by 640 the rings had gone from the first screen;
   "paid exactly 4" beside "the cashier's way 6" read "as if the cashier's way were not exact".
4. 14:38. "I would send the page to a friend as it stands." From the sentence on the floor alone the reader worked
   out the two-coin figure by hand, 8.45.
5. 14:58. After the referee's reading the page said more exactly whose the results are and how far it had
   searched, and the reader found three sentences heavier for it; they were cut in two or shortened.
6. 15:13. "Counting…" on the pressed button was caught on film. "One of the 3 best coins" was read as one of the
   top three; it is now "equal best with …".
7. 15:40. "Nothing is worse, and I would send the page to a friend as it is."

**The referee** (`referee27/`: its five briefs and five reports).

- *Blind*, 14:29, from the rules alone, with a program of its own: the three averages, the worst cases and the
  cashier's failures for fourteen coinages; the best coin to add, with ties; twelve coins added one after another;
  every way of paying twelve amounts with change; the best four coins among 152,096 sets; Pearson's test on four
  coinages. I typed its figures into `referee27/blind-beside-pcore.js` and ran `pcore.js` beside them: 37
  comparisons, none differs.
- *Reading*, 14:37: in 314 states of the page, set against its own program, "0 disagreements". Faults in what the
  words claimed: "every set was tried" above two rows that read "not searched"; "the best coin for paying with
  change" where a coin beyond those tried is better; a legend that said "the upper one" of a single line; a foot
  that gave Shallit the best sets outright, where my own sources have him crediting posts of 2000 and Young's
  entry in the Encyclopedia for the best four; a tooltip that outlived its coins; twelve ways of 63 coins drawn as
  twelve rows alike. And averages that fall half-way in the third decimal were rounded as the machine's
  arithmetic has them, sometimes down: see below. Three broken copies of the page passed my test.
- *Mending*, 14:57: all 314 states again, no disagreement. The sign "Counting…" was missing for the slowest counts
  and a count could be started twice; the legend said "the upper one" of two lines in one place (38 states of
  314); two more broken copies passed.
- *Last*, 15:13: a tap that landed while the page counted was answered when it had done ("the button read 'Add a
  120'; a second tap during the count then added a 313 as well"); a best set pressed in the same instant as an
  add button left "Added a 32 … from 4.7 to 3.46" over a tile that said "cannot make 50 amounts". Two more
  broken copies passed.
- *Pending*, 15:39, 76 trials: "everything I found last time is cured in these trials." Sentences it would still
  not sign: "None, besides the one about the write-up", which is this section.

**One change to the counting program.** `pcore.js` printed an average by the machine's own rounding of a quotient,
which sends some half-way cases down: 3/80 = 0.0375 was "about 0.037", while 1323/240 = 5.5125 was "about 5.513".
Of the 14,400 half-way cases with a number of amounts that is a multiple of 16 up to 1,000 and an average up to 12,
4,224 went down (`out27/halfway.out`; the referee counted the same). `meanText` now rounds half up in whole
numbers; over 1,180,004 totals and ranges it is right in every one, and differs from the old function in those
4,224 and nowhere else. No number in this file changes (`checkfacts.js`: 52 facts pass, as before), and the 59
tests of the counting pass. CMUT-TALLY-TO-COME

**The test** (`tools/shot-change.js`) has 223 assertions, 174 before the remake; the page is driven at desk size
with a mouse and on a phone with taps. BATCH-TALLY-TO-COME Eight broken copies of the referee's passed my test at
one round or another; each is in the list now.

**The page and its test are made by scripts** from the files of the 24th, so that every change can be read:
`out27/remake.py` to `remake8.py` (the page) and `out27/test-remake.py` to `test-remake7.py` (the test), one
script for each round of reading.

**Not done, and what is left as it is.**

- A second tap about 0.4 s after the first, on a button that adds a coin, adds a second coin; its name has then
  been on the button for a few hundredths of a second. A press held down through a count and let go after the
  buttons open again is taken, and adds the coin the button names by then. Keys struck within about 0.4 s of
  Enter in the coins box are dropped (the box keeps its caret).
- The best coin to add with change is the best of those tried, and the page says how far it tried. I did not
  widen the search: no bound on a useful coin is known to me (with 50 and 51 and amounts 0 to 6, a 102 pays 2 in
  three coins where the coins in use need four, and 102 is more than the largest coin and the largest amount
  together).
- The best sets with change are searched with coins up to 150 and up to five coins, as before; the referee's own
  search to 200 found nothing better for three coins.
- With 240 amounts in a phone's width (Britain before 1971) an amount is about a pixel wide in the first picture,
  too close for a thumb; the box and the slider pick it.
- Not tried: a slow phone; any real phone; a screen reader.

'''
    rep("## Files\n", section + "## Files\n")
    rep("| `tools/shot-change.js` | the page opened in a headless browser: 174 assertions on what it shows |", "| `tools/shot-change.js` | the page opened in a headless browser, at desk size and as a phone: 223 assertions on what it shows (174 before 27 November; that test is kept as `tools/shot-change.before-27nov.js.txt`) |")
    rep("| `page-mutants.py`, `page-mutants.out` | the page broken 53 ways; its test catches 53 |", "| `page-mutants.py`, `page-mutants.out` | the page broken 135 ways, four copies at a time with the true page among them (27 November; the list and record of the 24th, 53 of 53, are `out27/page-mutants.before-27nov.py.txt` and `.out`) |\n| `reader/`, `referee27/`, `out27/` | 27 November: the plain reader's seven briefs and reports and the page as it stood at each visit; the second referee's five briefs and reports, with its blind figures set beside `pcore.js`; the scripts that make the page and its test from the files of the 24th, the page's source and test as they stood then, `pcore.js` as it stood, and the count of half-way roundings |")
    open(P, 'w', encoding='utf8').write(s); print('README: 27 November')
