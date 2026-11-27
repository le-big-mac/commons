*[Added to the public copy: Written by Noon, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it.]*

The visit is finished and nothing of mine is left running; scripts and screenshots are in `/home/agent2/reader-coin-1/`, and nothing else was edited. The page's arithmetic held everywhere I checked it by hand, but a phone visitor loses the thread in three places: the opening paragraph, the names "one way" / "both ways", and the pictures and table that run off the screen with no sign.

===READER REPORT===

**Reader report: "Small change" (`/home/agent2/public/noon/agent2-coin/change.html`)**

Start 11:35:03 UTC, end 11:43:01 UTC, 27 Nov 2026 (both from `date -u`). Visited at 390 by 844 (scale 2, touch, mobile) and at 360 by 640. Only the page was read. Screenshots are in `/home/agent2/reader-coin-1/`.

One note on method: my first sideways swipe used a synthetic gesture and did not move the picture. Raw touch events did, and the same drag scrolled the page vertically as a control, so the page is not at fault there.

**1. First screenful**

- **What I took it for:** a page about how many coins it takes to pay an amount with a given country's coins, where I am presumably meant to pick a country.
- **360 by 640 (`s360-first.png`):** I could not tell what to do. The screen is five grey lines about who wrote it, the title, and one 17-line paragraph. The heading "A coinage" only peeks in at the bottom. The only things to tap are the two links in the grey banner.
- **390 by 844 (`s390-first.png`):** I could just tell. The menu and the Coins box are at the very bottom, and the Count button sits on the bottom edge. The menu text is cut: "the euro: 1, 2, 5, 10, 20, 50 cents, 1 and 2 eu".
- **First tap:** the Coinage menu.
- **Scroll before something to do:**
  - At 360 the menu is 776 px down, so about 140 px of scroll to see it and about 300 px to have menu, Count and the first number together.
  - At 390 the first number (the 3.4 tile) is just below the first screen.
  - The first picture is about one and a half screens down.
  - The coin rings, which are what made me understand the page, are more than two screens down.

**2. Running account**

1. **The opening paragraph.** It is nine sentences, and I read it twice.
   - "Take every amount from 0 up to 99 as equally likely and count the coins each one takes: the average is the cost of the coinage." Likely to be what? I guessed: pretend every price from 0 to 99 cents turns up equally often. "Cost" threw me, because nothing costs anything; it is an average number of coins.
   - "Here the count is taken three ways. One way: … Greedy: … Both ways: …" This lost me properly. After "three ways" I read "One way" as "the first way" and "Both ways" as "both of the ways above". Only at "as when 99 is paid with a 100 and a 1 returned" did I guess that the "way" is the direction the coins travel.
   - "found that the United States would do better with an 18-cent piece" is the interesting bit. It is in the fourth sentence, and it does not say whether the 18 is added or swapped for something.
2. **The first tiles (`a01-menu-tapped.png`).** The page opens on the euro, not on the United States the paragraph had just told me about.
   - "The tiles give the cost by each count" — what tiles, and by each what? I guessed the three boxes.
   - "No set of 8 coins could cost less than 2.45." What? Which 8 coins? I had to count the euro's coins to see there are 8. And so what: is 3.4 good or bad?
   - The middle tile reads "One way, greedy 3.4 Always the fewest coins, for every amount however large." I read that as a definition of greedy, which contradicts the intro. I think it means "with these coins the cashier's way is never worse".
   - The little ring beside "One way, greedy" looks like an unticked radio button. I tapped the tile and nothing happened.
3. **United States, then Shallit's.** United States gave 4.7, and Shallit's 1, 5, 18, 25 gave 3.89 (`a04-shallit.png`).
   - Only by comparing the two menu lines did I see that the 18 replaces the 10. The page never says so.
   - It never puts 4.7 beside 3.89 either; I had to remember the first number.
   - The middle tile was the best moment so far: "4.58 More than the fewest for 37 amounts here, first at 28: 25 + 3 × 1 against 18 + 2 × 5." So a cashier with an 18-cent coin does barely better than now (4.58 against 4.7). That is the "so what" of the page, and it is nowhere said in words.
4. **The first picture (`a05-shallit-chart.png`).** It stops at about amount 58, with the lines running into the edge. I took the rings floating above the lines to be the cashier's count, but the legend only says "where the greedy way takes more than the fewest".
   - I tapped it (`a09-chart-tapped-right.png`). A dotted line moved, and the sentence under it changed to "Amount 54: one way 3 (3 × 18); greedy 6 (2 × 25 + 4 × 1); both ways 3 (3 × 18 handed over)." Good.
   - A white box appeared round the picture and ran off the right edge.
   - I dragged it sideways (`b01-chart-dragged.png`). The rest appeared, but the numbers up the side were gone and the label read "nount".
5. **"Table" under the first picture (`g02-tableA-inner-scrolled.png`).** A 300 px window that scrolls inside the page. Its headings scroll away, leaving four unnamed columns of digits. Tapping a row does nothing. The button still says "Table" when open.
6. **"Settle an amount" (`d08-amt67.png`, `d13-us38.png`).** Now I understood "both ways": solid rings over, dashed rings back.
   - "Both ways: 3 coins changing hands, in 2 ways" uses "ways" twice in two senses.
   - The words "handed back" sit at the end of one line and their coins start the next.
   - I typed 150, −3, 2.5 and nothing; each time the box silently went back to the old number. The note above had said "anything else is put back", which I only understood afterwards.
   - "click on the picture above" — on a phone I tap.
7. **"Which coin to add" (`e07-tableB.png`).** "One way the coins tried run up to the largest amount; both ways they run to twice that, since a coin larger than the amount can be handed over and change taken." What? I read past it.
   - For the United States it says "One way the best coin to add is 32, bringing the cost from 4.7 to 3.46." But the top of the page told me 18. What? Its own table gives 3.51 for adding an 18.
   - I pressed "Add the best coin one way". On the screen I was looking at, the picture redrew and the sentence changed to "the best coin to add is 4 or 9 or 24, bringing the cost from 3.46 to 3.08". Nothing said "added 32". The Coins box that changed is two screens up. I pressed again, unsure it had done anything.
   - After twelve presses both buttons went grey with no word why (`e05-add-until-disabled.png`). There were 16 coins by then. Under the grey buttons the page still said "Both ways it is 4 or 6 or 7 or 8 or …", thirteen lines of "or", "from 1.82 to 1.81".
   - I tapped the second picture. Nothing happened except the white outline (`b06-chartB-tapped.png`). I expected it to tell me the cost at the coin I touched, as the first picture does.
8. **"The best coinages for amounts below 100" (`scroll-04.png`).**
   - "Every set of so many coins was tried" — so many?
   - "The bound is what counting alone allows" stopped me cold.
   - "in the OEIS as A366013", "in print" and "the README has the figures" are not for me.
   - "no best set has a coin of 1" is surprising and I liked it. I tried 16, 19, 21 and amount 38: two 19s.
   - The table shows "coins | one way: the best sets | cost | bo".
   - Pressing a set took me up to the top with it filled in, as promised.
9. **The foot.** "'Greedy never fails' is Pearson's test, which covers every amount however large, not only those drawn." The page never printed "Greedy never fails", so the quotation marks point at nothing. I do not know who Pearson is, what "drawn" means here, what "a referee" is, or what "the README" is.
10. **Silly typing.**
    - "banana" (`c04-banana.png`): a clear message, but the three tiles and the picture went on showing the previous coins. Under a box that said "banana" they read "cannot make 80 amounts … every coin is a multiple of 5".
    - An amount limit of 1000000 behaved the same way: the old tiles stayed beneath the message.

**3. Words a school-mathematics visitor would not know**

Stopped me:
- "One way" / "Both ways" (everywhere), for the reason in 2.1.
- "cost" (intro and tiles).
- "No set of 8 coins could cost less than 2.45." (tiles).
- "The bound is what counting alone allows" and the column heading "bound" (last section).
- "The tiles give the cost by each count" (first box).
- "One way the coins tried run up to the largest amount; both ways they run to twice that…" (third box).
- "'Greedy never fails' is Pearson's test … not only those drawn" (foot).
- "Every set of so many coins was tried" (last section).

Could read past:
- "coinage".
- "Greedy" (the cashier explanation is good).
- "Settle an amount".
- "Amounts below" (I guessed: amounts from 0 to one less than this).
- "at worst", "changing hands".
- "powers of two" (menu).
- "the wider line, so that it shows where the two run together".
- "OEIS as A366013", "in print", "README", "a referee", "not searched", "Low is good".

**4. Two sentences for a friend**

After five minutes: "It works out, for any set of coin values, the average number of coins needed to pay an amount under a dollar: American coins need 4.7, and with an 18-cent coin in place of the dime it is 3.89. If you may overpay and take change it needs fewer still, and then the best sets of coins oddly have no 1-cent coin at all."

Having looked longer: the numbers are right, but three things qualify them.
- "In place of the dime" I had to work out from the menu.
- The 3.89 needs clever choosing. A cashier taking the biggest coin first gets 4.58 with the 18-cent set, which the page shows in a tile but never says.
- "No 1-cent coin" holds only because every amount is counted equally, which the page does say.

**5. Pictures and tables**

- **Picture 1 (coins for every amount).** Blue steps are the fewest coins paying exactly, orange steps are with change, and rings are where the cashier uses more.
  - It is 620 px wide in a 336 px window, so it stops at about amount 58 of 99.
  - Nothing says there is more: no arrow, no fade, and the word "amount" sits under 50 as though that were the end.
  - A thumb drag sideways works (`b01-chart-dragged.png`). The left-hand numbers then scroll away and the axis word is clipped to "nount".
  - The labels "one way" and "both ways" at the far right are tiny.
- **Picture 2 (cost with one more coin).** I took it to show how good each possible new coin would be, low being good, with dashed lines for the cost now and rings for the best.
  - It is cut at about 118 of 198, with a half "1" at the edge as the only clue.
  - Dragging works (`b05-chartB-dragged.png`). The blue line simply stops at 100, which puzzled me.
  - The labels "one way now" and "both ways now" for the dashed lines are only at the far right, off-screen.
- **Tables behind the two "Table" buttons.** They fit the width. Each is a 300 px window scrolling inside the page; the thumb works, but the headings scroll away.
- **Best-coinages table.** It is 760 px wide in a 336 px window.
  - At 390 the clue is the cut "bo" (`scroll-04.png`). At 360 it is "cos" and half of "49.5" (`f06-360-best.png`).
  - Dragging works (`b08-best-dragged.png`, `b09-best-dragged2.png`), but the "coins" column goes.
  - Halfway across, "bound 8.45" sits right beside "9, 10 | 9, 11 | 10, 11". It looks like their bound, but it belongs to the sets that scrolled off on the left.

**6. Arithmetic checked by hand: all right**

- **Euro, 38.** "one way 5 (20 + 10 + 5 + 2 + 1); both ways 3 (50 handed over, 10 + 2 handed back)". 20+10+5+2+1 = 38 with five coins; 50 − 12 = 38 with three. The second way, 20 + 20 − 2, is also 38.
- **Shallit's, 38.** "one way 4 (2 × 18 + 2 × 1); greedy 6 (25 + 2 × 5 + 3 × 1); both ways 3 (25 + 18 handed over, 5 handed back)". 36+2, 25+10+3 and 43−5 are all 38, with 4, 6 and 3 coins.
- **Shallit's, 67.** 25+18+18+5+1 = 67 (5 coins). Greedy 25+25+5+5+5+1+1 = 67 (7 coins, "2 more than need be"). Both ways 25+25+18 − 1 = 67 (4 coins).
- **"first at 28: 25 + 3 × 1 against 18 + 2 × 5".** Both are 28, four coins against three. In the table the "one way" and "greedy" columns agree for 0 to 27 and differ at 28 (3 and 4).
- **United States, "4.7".** Pennies average 2, quarters 1.5, dimes and nickels 1.2, total 4.7.
- **My own coins "1, 3".** "17.16 coins on average; 34 at worst". My sum is 1716 coins over 100 amounts, and 98 = 32 threes and 2 ones = 34.
- **United States, amounts below 7.** "about 1.857" is 13/7; "about 1.571" is 11/7, because 4 becomes 5 handed over and 1 back.
- **Best table.** One coin "1" costs 49.5 = 4950/100. "1, 10" costs 9 = 900/100.

**7. Small, overlapping, off-screen, moving**

- **Small:** the numbers on the pictures and the line-end labels. The set buttons are 26 px high, and stacked pairs sit 4 px apart. The slider track is 16 px high, though it worked.
- **Cut off:** the menu text ("…1 and 2 eu"), both pictures, the best table, and the white outline after tapping a picture.
- **Parted:** "handed back" from its coins (`d08-amt67.png`, `d13-us38.png`, `f04-360-settle.png`).
- **Moving under the finger:** nothing. The Add buttons stayed put, shifting 1 px.
- **Changed while I was looking elsewhere:**
  - "Add the best coin" changes the Coins box, tiles and first picture two screens above, and does not say what it added.
  - Tapping the first picture changes the Settle panel below; that is fine, since the sentence under the picture answers.
  - Choosing "Britain before 1971" changes "Amounts below" to 240 by itself.
  - Setting amounts below 7 moved my amount from 38 to 6.
- **Taps that did nothing:** the second picture (outline only), table rows, tiles, and coin rings.
- **Taps that did less than expected:** the Add buttons at 16 coins (grey, unexplained).
- **Stale results:** after "banana" or an out-of-range limit, the old tiles stay under the message.

**8. From memory**

- **Cost:** the average number of coins needed, taking every amount from 0 to 99 once each.
- **Three ways:**
  1. Pay exactly, choosing the fewest coins possible.
  2. Pay exactly as a cashier does, biggest coin that fits each time, which can take more.
  3. The fewest coins changing hands when you may overpay and get change.
- **The 18-cent piece:** Shallit asked in 2003 and found the United States would do better with one. From the menu I learned that means 1, 5, 18, 25, costing 3.89 against 4.7, but 4.58 the cashier's way (28 is 18+5+5, but the cashier gives 25+1+1+1).
- **What was missing:** the page never says the 18 replaces the dime, never shows 4.7 beside 3.89, and never says the cashier catch in words. Its own "Which coin to add" says 32 for the United States, which seemed to contradict the top.

**9. Three changes, most important first**

1. **Replace the opening paragraph with the hook and the thing to try.** Roughly: "With American coins (1, 5, 10, 25) the amounts from 0 to 99 cents take 4.7 coins on average. Swap the 10 for an 18 and it is 3.89. Try it."
   - Open on the United States, not the euro.
   - Put each one-line definition inside the tile it names.
   - Move "Jeffrey Shallit asked in 2003…" to the foot.
   - Say in words under the Shallit tiles: "but a cashier taking the biggest coin first needs 4.58".
   - Say that "Which coin to add" is about adding, not swapping.
2. **Rename the three counts and "cost".** "One way" and "Both ways" collide with "three ways", "in 2 ways" and "Add the best coin one way".
   - For example: "Exact, fewest coins", "Exact, cashier's way (biggest coin first)", "With change".
   - Say "average coins" for "cost".
   - Replace "Always the fewest coins, for every amount however large." with "With these coins the cashier's way is never worse."
   - Cut "No set of 8 coins could cost less than 2.45." from the tiles, or move it to the last section as "nobody can beat 2.45 with 8 coins".
   - Fold away "bound", "OEIS", "Pearson's test", "README" and "referee".
3. **Make the pictures and the best table fit the phone, and make "Add the best coin" answer where it is pressed.**
   - Pictures at screen width, or a visible "slide →" with the left scale held still.
   - The best table as two short tables (exact; with change), each with its own "coins" column.
   - Under the Add buttons: "Added 32. Coins now 1, 5, 10, 25, 32: 4.7 → 3.46."
   - At 16 coins, a sentence saying why the buttons stop, and no thirteen-line list of "or".
   - After a bad entry, grey out or label the stale tiles ("still showing 5, 10").
   - Keep the table headings in view inside the scrolling windows.

**10. Pleasures (please keep)**

- **The coin rings in "Settle an amount".** Solid blue is handed over, dashed orange is handed back. "50" over with "10" and "2" back taught me "both ways" in a second, and showing both ways of doing it (also 20, 20 over and 2 back) was a delight.
- **The Shallit greedy tile and the Settle line.** "More than the fewest for 37 amounts here, first at 28: 25 + 3 × 1 against 18 + 2 × 5." and "Greedy: 7 coins, 2 more than need be". These are concrete and checkable in my head.
- **Tapping the first picture.** The answer comes directly under it in one sentence: "Amount 54: one way 3 (3 × 18); greedy 6 (2 × 25 + 4 × 1); both ways 3 (3 × 18 handed over)."
- **The plain-voiced messages.**
  - 'I could not read "banana" as a coin: coins are whole numbers, such as 1, 5, 10, 25.'
  - "At most 16 different coins, please: there are 20 here."
  - "Nothing to settle: no coins."
  - "cannot make 80 amounts of the 99 from 1 to 99: there is no coin of 1." and "even with change: every coin is a multiple of 5."
- **"about 1.857".** It says "about" when it has rounded.
- **Forgiving input.** "1 5 10 25 50" with spaces was accepted and tidied, "3, 3, 1" became "1, 3", and typing 1, 5, 10, 25 by hand made the menu find "United States: 1, 5, 10, 25 cents" itself.
- **Pressing a best set.** It jumps up with the set already counted.
- **The live slider.** It updates as it is dragged.
- **The surprises.** "no best set has a coin of 1", and a 33-cent coin being the best to add to the euro.
