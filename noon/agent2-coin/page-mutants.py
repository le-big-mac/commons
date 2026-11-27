"""page-mutants.py -- can the page test fail?  Copies of the page with one thing broken in its own script, styles or words, each built
and run through tools/shot-change.js in a headless browser, four at a time, the true page alone first and again among them.
python -I page-mutants.py [JOBS [name,name,...]] > page-mutants.out        (the test is run from ~/web, where playwright is)
The list was rewritten on 27 November 2026 for the page as remade for a visitor with a phone; the list and record of before are in out27/."""
import os, json, subprocess, sys, re, time
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'mutants-page'); WEB = os.path.expanduser('~/web')
rd = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()
M = [
 ('tile-fewest-shows-cashier', "the tile for the fewest coins shows the cashier's average", "tile('tile-plain', costText(tp, L), false,", "tile('tile-plain', costText(tg, L), false,"),
 ('tile-worst-of-the-other-count', "the tile for the fewest coins gives the worst case with change", "'coins on average; ' + P.worst(S.plain) + ' at worst.'", "'coins on average; ' + P.worst(S.both) + ' at worst.'"),
 ('tile-cashier-judged-by-what-is-drawn', "the cashier is said never to take more whenever no amount drawn shows it", "pf === 0 ? 'With these coins the cashier never takes more than need be, however large the amount.' :", "fails.length === 0 ? 'With these coins the cashier never takes more than need be, however large the amount.' :"),
 ('tile-first-failure-is-last', "the cashier's first failure is given as the last", "first at ' + fails[0] + ': ' + wayText(P.greedyWay(S.coins, fails[0]))", "first at ' + fails[fails.length - 1] + ': ' + wayText(P.greedyWay(S.coins, fails[0]))"),
 ('picture-change-line-is-fewest', "the line for paying with change is drawn from the fewest coins", "d = stepPath(L, function (i) { return fin(S.both[i]) ? S.both[i] : null; }, f.X, f.Y, 0);", "d = stepPath(L, function (i) { return fin(S.plain[i]) ? S.plain[i] : null; }, f.X, f.Y, 0);"),
 ('picture-one-place-to-the-right', "every line is drawn one amount to the right", "if (!open) { d += 'M' + (X(a + x0) - half).toFixed(2) + ',' + Y(v).toFixed(2); open = true; }\n      else d += 'V' + Y(v).toFixed(2);\n      d += 'H' + (X(a + x0) + half).toFixed(2);",
    "if (!open) { d += 'M' + (X(a + x0 + 1) - half).toFixed(2) + ',' + Y(v).toFixed(2); open = true; }\n      else d += 'V' + Y(v).toFixed(2);\n      d += 'H' + (X(a + x0 + 1) + half).toFixed(2);"),
 ('picture-no-gap-where-it-cannot', "a line runs on over amounts that cannot be made", "if (v === null) { open = false; continue; }", "if (v === null) { continue; }"),
 ('picture-axis-labels-one-out', "the numbers up the side are one too many", "svg.appendChild(el('text', { x: BOX.l - 6, y: py + 4, 'text-anchor': 'end' }, String(Math.round(v * 100) / 100)));", "svg.appendChild(el('text', { x: BOX.l - 6, y: py + 4, 'text-anchor': 'end' }, String(Math.round(v * 100) / 100 + 1)));"),
 ('picture-top-cut-off', "the first picture's top is one coin too low", "f = frame(svg, -0.5, L - 0.5, 0, top, 'amount', 'coins', true);", "f = frame(svg, -0.5, L - 0.5, 0, top - 1, 'amount', 'coins', true);"),
 ('picture-wider-than-shown', "the pictures are drawn 70 units wider than they are shown, so that their lettering shrinks", "BOX = { W: Math.max(260, w),", "BOX = { W: Math.max(260, w) + 70,"),
 ('rings-at-the-fewest-count', "the cashier's rings stand at the fewest count", "f.g.appendChild(el('circle', { cx: f.X(a).toFixed(2), cy: f.Y(S.greedy[a]).toFixed(2),", "f.g.appendChild(el('circle', { cx: f.X(a).toFixed(2), cy: f.Y(S.plain[a]).toFixed(2),"),
 ('rings-where-the-cashier-ties', "rings where the cashier takes no more", "for (a = 0; a < L; a++) if (fin(S.greedy[a]) && fin(S.plain[a]) && S.greedy[a] > S.plain[a]) {", "for (a = 0; a < L; a++) if (fin(S.greedy[a]) && fin(S.plain[a]) && S.greedy[a] >= S.plain[a] && a % 7 === 3) {"),
 ('table-cashier-column-is-fewest', "the table's column for the cashier holds the fewest coins", "'</td><td>' + c(S.greedy[a]) + '</td><td>' + c(S.both[a]) + '</td></tr>';", "'</td><td>' + c(S.plain[a]) + '</td><td>' + c(S.both[a]) + '</td></tr>';"),
 ('add-with-change-tries-too-few', "with change, new coins are tried only up to the largest amount", "S.addBoth = P.bestAdd(S.coins, S.L, 'both', 2 * S.L - 1);", "S.addBoth = P.bestAdd(S.coins, S.L, 'both', S.L - 1);"),
 ('add-fewest-is-cashier', "the coin to add for the fewest coins is reckoned the cashier's way", "S.addPlain = P.bestAdd(S.coins, S.L, 'plain', S.L - 1);", "S.addPlain = P.bestAdd(S.coins, S.L, 'greedy', S.L - 1);"),
 ('add-average-over-one-amount-fewer', "the second picture divides by one amount too few", "S.addPlain.forEach(function (e) { if (isFinite(e.total)) one[e.coin] = e.total / L; });", "S.addPlain.forEach(function (e) { if (isFinite(e.total)) one[e.coin] = e.total / (L - 1); });"),
 ('add-sentence-names-one-of-the-best', "of several equally good coins the sentence names one", "return c.length <= 5 ? c.join(' or ') :", "return c.length <= 5 ? String(c[0]) :"),
 ('add-rings-only-for-fewest', "the best coin with change is not ringed", "    bb.forEach(function (e) { f.g.appendChild(el('circle', { cx: f.X(e.coin), cy: f.Y(e.total / L), r: 4.5, fill: '#1a1a19', stroke: '#f0efec', 'stroke-width': 1.5, 'class': 'bestmark' })); });\n", ""),
 ('add-button-takes-the-last-of-the-best', "the button adds the last of several equally good coins", "coin = b[0].coin; after = b[0].total;", "coin = b[b.length - 1].coin; after = b[0].total;"),
 ('add-change-button-adds-the-other-coin', "the button for paying with change adds the best coin for paying exactly", "addBest(S.addBoth, P.total(S.both), 'paying with change', $('addBoth'));", "addBest(S.addPlain, P.total(S.plain), 'paying with change', $('addBoth'));"),
 ('add-tooltip-fewest-for-large-coins', "a coin larger than every amount is given an average for paying exactly", "(c <= L - 1 ? 'paying exactly ' + (o === null", "(c <= 2 * L ? 'paying exactly ' + (o === null"),
 ('add-coin-there-not-said', "a coin already there is priced as if new", "if (S.coins.indexOf(c) >= 0) return 'A coin of <b>' + c + '</b> is already there.';\n    return 'With a coin", "return 'With a coin"),
 ('pay-handed-back-drawn-as-over', "coins handed back are drawn with solid rings", "'<span class=\"grp\"><span class=\"lab\">handed back</span>' + coinsHtml(back, 'back') + '</span>'", "'<span class=\"grp\"><span class=\"lab\">handed back</span>' + coinsHtml(back, 'over') + '</span>'"),
 ('pay-shows-eleven', "eleven ways are shown, not twelve", "s = P.schemes(S.coins, a, 12, 3000000); shown = s.ways.length;", "s = P.schemes(S.coins, a, 11, 3000000); shown = s.ways.length;"),
 ('pay-gave-up-not-said', "where the ways were too many to count the page gives a count", "(s.gaveUp ? ' (there are more ways of doing it than I counted' : s.total === 1 ? '' : ' (it can be done in <b>' + s.total + '</b> ways')", "(s.total === 1 ? '' : ' (it can be done in <b>' + s.total + '</b> ways')"),
 ('pay-cashier-row-hidden', "the cashier's row is left out where the cashier takes one more", "if (fin(p) && (!fin(g) || g > p)) h +=", "if (fin(p) && (!fin(g) || g > p + 1)) h +="),
 ('pay-draws-every-coin', "every one of 999 coins is drawn", "if (shown >= 40) return h +", "if (shown >= 4000) return h +"),
 ('pay-zero-draws-ways', "an amount of nothing is given ways", "    if (a === 0) { $('ways').innerHTML = '<div class=\"way\"><p class=\"k\">Nothing to pay: <b>no coins</b>.</p></div>'; return; }\n", ""),
 ('tooltip-speaks-of-the-cashier-always', "the tooltip speaks of the cashier where the cashier takes no more", "if (fin(g) && fin(p) && g > p) out.push('the cashier\\'s way <b>'", "if (fin(g) && fin(p) && g >= p) out.push('the cashier\\'s way <b>'"),
 ('tooltip-over-and-back-swapped', "handed over and handed back are swapped in the words", "var over = w.filter(function (e) { return e[1] > 0; }), back = w.filter(function (e) { return e[1] < 0; }).map(function (e) { return [e[0], -e[1]]; });\n    return (over.length",
    "var back = w.filter(function (e) { return e[1] > 0; }), over = w.filter(function (e) { return e[1] < 0; }).map(function (e) { return [e[0], -e[1]]; });\n    return (over.length"),
 ('tooltip-runs-off-the-figure', "the tooltip runs off its figure at the right", "tip.style.left = Math.max(4, Math.min(fig.width - tip.offsetWidth - 4, x + 12)) + 'px';\n    tip.style.top = (box.top - fig.top + 8) + 'px';\n    sayA(a);", "tip.style.left = (x + 12) + 'px';\n    tip.style.top = (box.top - fig.top + 8) + 'px';\n    sayA(a);"),
 ('click-one-amount-out', "a click on the first picture pays the next amount", "var a = amountAt(A, e, 0, S.L); hoverA(-1);", "var a = amountAt(A, e, 0, S.L) + 1; hoverA(-1);"),
 ('dotted-line-left-behind', "the dotted line stays where it was", "var pick = $('pickA'); if (pick && geoA) { pick.setAttribute('x1', geoA.f.X(a)); pick.setAttribute('x2', geoA.f.X(a)); }", ""),
 ('arrow-key-steps-two', "the right arrow moves two amounts", "if (e.key === 'ArrowRight') { hoverA(Math.min(S.L - 1, a + 1)); e.preventDefault(); }", "if (e.key === 'ArrowRight') { hoverA(Math.min(S.L - 1, a + 2)); e.preventDefault(); }"),
 ('amount-not-brought-inside', "an amount beyond a new range is left there", "    if (S.amount > S.L - 1) S.amount = S.L - 1;\n    S.pickB = -1;", "    S.pickB = -1;"),
 ('read-takes-coins-too-large', "a coin of 6000 is taken", "if (v < 1 || v > MAXCOIN) return", "if (v < 1) return"),
 ('read-takes-seventeen', "seventeen coins are taken", "if (out.length > MAXCOINS) return", "if (out.length > MAXCOINS + 1) return"),
 ('read-keeps-repeats', "a coin typed twice counts twice", "if (!seen[v]) { seen[v] = 1; out.push(v); }", "out.push(v);"),
 ('read-takes-any-range', "a largest amount of 4999 is taken", "if (v < 1 || v > MAXL - 1) return", "if (v < 0 || v > 9000) return"),
 ('notice-not-cleared', "a good entry leaves the notice standing", "    notice(''); $('addedSay').textContent = '';", "    $('addedSay').textContent = '';"),
 ('refused-entry-still-counted', "an entry that is refused is counted all the same", "if (c.error) { notice(c.error + still()); return; }", "if (c.error) { notice(c.error + still()); c = { coins: [1] }; }"),
 ('listed-coinage-chosen-whatever-the-range', "typed coins are given a listed coinage's name whatever the range", "PRESETS.forEach(function (p, i) { if (p.L === S.L && p.coins.join() === S.coins.join()) same = i; });", "PRESETS.forEach(function (p, i) { if (p.coins.join() === S.coins.join()) same = i; });"),
 ('best-table-average-is-the-least-possible', "the table of best sets gives what counting allows as the average", "hp += '<tr><td>' + D + '</td><td class=\"l\">' + btns(p) + '</td><td>' + costText(p.total, BEST.L) + '</td>", "hp += '<tr><td>' + D + '</td><td class=\"l\">' + btns(p) + '</td><td>' + costText(p.bound, BEST.L) + '</td>"),
 ('best-table-keeps-the-range', "a best set is tried with the range in force, not below 100", "setCoinage(t.getAttribute('data-set').split(',').map(Number), BEST.L);", "setCoinage(t.getAttribute('data-set').split(',').map(Number), S.L);"),
 ('best-table-change-has-the-other-bound', "with change, the least possible is the one for the fewest coins", "(b ? '<td class=\"l\">' + btns(b) + '</td><td>' + costText(b.total, BEST.L) + '</td><td>' + costText(b.bound, BEST.L) + '</td>'", "(b ? '<td class=\"l\">' + btns(b) + '</td><td>' + costText(b.total, BEST.L) + '</td><td>' + costText(p.bound, BEST.L) + '</td>'"),
 ('table-button-does-not-open', "the table buttons open nothing", "$(tab).className = 'tables' + (on ? ' on' : '');", "$(tab).className = 'tables';"),
 ('best-coin-named-though-it-helps-nothing', "a coin is called best that lowers nothing", "return b.length && (!isFinite(now) || b[0].total < now) ? b : []; }", "return b; }"),
 ('no-coin-left-not-said', "with no coin left to try the page says nothing of it", "    else if (!S.addPlain.length) out.push('Paying exactly there is no coin left to try: every value up to ' + (L - 1) + ' is a coin already.');\n", ""),
 ('amount-box-not-put-back', "an entry that is no amount stays in the box", "      $('amount').value = S.amount;\n    });", "    });"),
 ('first-makeable-coin-not-best', "a coin that first lets every amount be made is not called best", "return b.length && (!isFinite(now) || b[0].total < now) ? b : []; }", "return b.length && isFinite(now) && b[0].total < now ? b : []; }"),
 ('seventeenth-coin-offered', "a seventeenth coin is offered", "$('addPlain').disabled = bp.length === 0 || full;", "$('addPlain').disabled = bp.length === 0;"),
 # ---- the page as remade for a visitor with a phone (27 November)
 ('opens-on-the-euro', "the page opens on the euro, not on the coins its first sentence speaks of (a visitor)", "    $('preset').value = '0';\n    setCoinage(PRESETS[0].coins, PRESETS[0].L, true);", "    $('preset').value = '2';\n    setCoinage(PRESETS[2].coins, PRESETS[2].L, true);"),
 ('opens-on-38', "the page opens on 38 cents, not on the 24 of its first sentence", "amount: 24, plain: null", "amount: 38, plain: null"),
 ('lead-says-five', "the first sentence says five coins for 24 cents", "takes six coins; or two,", "takes five coins; or two,"),
 ('caption-says-398', "the caption gives 3.98 for the coins with an 18", "and it is 3.89, if the coins", "and it is 3.98, if the coins"),
 ('cashier-catch-unsaid', "the caption does not say what a cashier would need with the 18 (a visitor: nowhere said in words)", "; a cashier, who takes the largest coin that fits, would need 4.58 with those coins.", "."),
 # mended 27 November: this fault left "if (...)" with nothing after it, which stopped the page's whole script; it now leaves a statement that does nothing
 ('swap-button-dead', '"Swap the 10 for an 18" does nothing', "steady($('story'), function () { setCoinage(t.getAttribute('data-set').split(',').map(Number), 100); matchPreset(); });", "void 0;"),
 ('swap-button-gives-a-29', '"Swap the 10 for an 18" gives 1, 5, 18, 29', "btn('1,5,18,25', 'Swap the 10 for an 18')", "btn('1,5,18,29', 'Swap the 10 for an 18')"),
 ('both-ways-back', 'a tile is headed "Both ways" again (a visitor read it as "both of the ways above")', "<b>Paying with change</b>: coins may be handed back", "<b>Both ways</b>: coins may be handed back"),
 ('cost-back', 'the sentence under the second picture speaks of "cost" again', "</b>, bringing the average ' +", "</b>, bringing the cost ' +"),
 ('pictures-slide-again', "the pictures are 620 px wide whatever the screen, and slide (a visitor: nothing said there was more)", "  h3 { font-weight: normal;", "  .chartwrap { overflow-x: auto; } .chartwrap svg.chart { min-width: 620px; }\n  h3 { font-weight: normal;"),
 ('picture-not-drawn-again', "the pictures are not drawn again when the screen's width changes", "if (w !== wide) { wide = w; fit(); drawA(); drawB(); }", "if (w !== wide) { wide = w; }"),
 ('tap-on-second-picture-dead', "a tap on the second picture does nothing (a visitor)", "    B.addEventListener('click', function (e) { hoverB(-1); pickB(amountAt(B, e, 1, geoB.n)); });\n", ""),
 ('second-picture-forgets', "the coin tapped on the second picture is forgotten when the pointer leaves", "sayB(S.pickB); return; }", "sayB(-1); return; }"),
 ('added-not-said', "nothing says which coin a button added (a visitor pressed again, unsure it had done anything)", "    $('addedSay').innerHTML = 'Added a <b>'", "    if (false) $('addedSay').innerHTML = 'Added a <b>'"),
 ('added-says-the-new-average-twice', "the sentence on the coin added gives the new average as the old", "'has gone from ' + costText(before, L) + ' to '", "'has gone from ' + costText(after, L) + ' to '"),
 ('button-jumps', "a button pressed moves from under the finger as the page above it changes length", "change(); window.scrollBy(0, elem.getBoundingClientRect().top - y); }", "change(); }"),
 ('sixteen-unsaid', "at sixteen coins the sentence under the picture goes on naming a best coin to add", "if (S.coins.length >= MAXCOINS) return 'There are '", "if (false) return 'There are '"),
 ('long-list-of-or', "thirteen equally good coins are listed with twelve times \"or\" (a visitor)", "return c.length <= 5 ? c.join(' or ') : c.slice(0, 4).join(', ') + ' or any of ' + (c.length - 4) + ' others'; }", "return c.join(' or '); }"),
 ('still-shows-unsaid', "after a bad entry nothing says which coins the page still shows (a visitor read the old tiles under \"banana\")", "if (c.error) { notice(c.error + still()); return; }", "if (c.error) { notice(c.error); return; }"),
 ('amount-put-back-silently', "an entry that is no amount is put back without a word (a visitor)", "if (String(typed) !== String(S.amount) && !/^\\d+$/.test(typed)) $('amountSay').textContent =", "if (false) $('amountSay').textContent ="),
 ('set-buttons-small', "the best sets are buttons 26 px tall, 4 px apart (a visitor)", "  .setbtn { min-height: 32px; margin: 0 6px 6px 0; }", "  .setbtn { margin: 0 6px 4px 0; }"),
 ('best-table-too-wide', "the tables of best sets are wider than a phone's screen", " table.best .setbtn { white-space: normal; text-align: left; }", ""),
 ('table-headings-scroll-away', "the tables' headings scroll away with their rows (a visitor)", "  .tables th { position: sticky; top: 0; background: #1a1a19; }\n", ""),
 ('table-button-says-table', "the table buttons do not say whether they will show or hide", " $(btn).textContent = on ? 'Hide the table' : 'Show the table';", ""),
 ('best-set-stays-below', "a best set pressed is filled in two screens above, and the page stays where it was", "matchPreset(); $('fig0').scrollIntoView({ block: 'start' }); }", "matchPreset(); }"),
 ('heading-says-99', "the first picture's heading says 0 to 99 whatever the range", "$('capA').textContent = 'The coins for each amount from 0 to ' + (L - 1);", "$('capA').textContent = 'The coins for each amount from 0 to 99';"),
 ('handed-back-ungrouped', '"handed back" is not kept with its coins', "(back.length ? '<span class=\"grp\"><span class=\"lab\">handed back</span>'", "(back.length ? '<span><span class=\"lab\">handed back</span>'"),
 # ---- after the reader's second visit
 ('story-always-american', "the sentence over the tiles tells of American coins whatever coins are chosen (a visitor read its 4.7 as the average of the coins chosen)", "$('story').innerHTML = us ?", "$('story').innerHTML = true ?"),
 ('line-names-other-coins', "the line over the tiles names the American coins whatever coins are in use", "'With the coins now in use (' + S.coins.join(', ') + ')", "'With the coins now in use (' + PRESETS[0].coins.join(', ') + ')"),
 ('put-back-does-nothing', '"Put the 10 back" leaves the 18 (a visitor pressed the button again: "nothing, and nothing said")', "btn('1,5,10,25', 'Put the 10 back')", "btn('1,5,18,25', 'Put the 10 back')"),
 ('fewest-coins-back', '"Fewest coins" stands over the rings again, above a smaller number (a visitor)', "<p class=\"k\">Paid exactly: '", "<p class=\"k\">Fewest coins: '"),
 ('ways-run-together', 'no "or" between one way of paying with change and the next (a visitor read two ways as one transaction)', "        h += (i ? '<p class=\"or\">or</p>' : '') + '<div class=\"row scheme\">' + (over.length", "        h += '<div class=\"row scheme\">' + (over.length"),
 ('add-button-names-no-coin', "the button does not say which coin it will add (a visitor)", "bp.length ? 'Add a ' + bp[0].coin + (bp.length > 1 ? ': equal best' + others(bp) : ': the best coin') + ' for paying exactly'", "bp.length ? 'Add the best coin for paying exactly'"),
 ('add-button-names-the-other-coin', "the button for paying with change names the coin for paying exactly", "bb.length ? 'Add a ' + bb[0].coin + (bb.length > 1", "bb.length ? 'Add a ' + bp[0].coin + (bb.length > 1"),
 ('full-reason-not-on-the-button', "at sixteen coins the button goes grey without saying why (a visitor: the reason was a screen away)", "full ? 'No coin can be added: ' + MAXCOINS + ' is as many as this page takes' :", "full ? 'Add the best coin for paying exactly' :"),
 ('other-button-stays-grey', "at sixteen coins the second button stays, grey and unexplained", " $('addBoth').style.display = full ? 'none' : '';", ""),
 ('no-fewer-unsaid', 'where change saves nothing the sentence under the picture still shows a way with change (a visitor: "So what?")', "(fin(p) && b === p && a > 0 ? ' (no fewer)' :", "(false ? ' (no fewer)' :"),
 ('too-large-amount-unsaid', "an amount too large becomes the largest without a word (a visitor: 150 silently became 99)", "if (Number(v) > S.L - 1) $('amountSay').textContent =", "if (false) $('amountSay').textContent ="),
 ('swap-looks-like-a-link', "the button in the sentence is underlined italics 24 px tall (a visitor took it for a link)", "  button.inline { min-height: 32px; margin: 2px 0; }", "  button.inline { font: inherit; font-style: italic; color: inherit; background: transparent; border: 0; border-bottom: 1px solid currentColor; border-radius: 0; padding: 2px 1px 1px; }"),
 ('least-possible-back', 'the last column is headed "least possible" again (a visitor: "it reads as something that can be had")', "<th>average</th><th>cannot be below</th>", "<th>average</th><th>least possible</th>"),
 # ---- after the reader's third visit
 ('range-box-holds-the-count', "the box labelled \"Amounts from 0 to\" holds the number of amounts, one more than the largest", "    $('coins').value = coins.join(', '); $('L').value = L - 1;", "    $('coins').value = coins.join(', '); $('L').value = L;"),
 ('range-read-as-the-count', "the largest amount typed is taken for the number of amounts", "return { L: v + 1 };", "return { L: v };"),
 ('at-best-unsaid', '"paid exactly 4" stands beside "the cashier\'s way 6" without "at best" (a visitor)', "'paid exactly' + (fin(g) && g > p ? ', at best' : '') + ' <b>'", "'paid exactly <b>'"),
 ('rings-no-fewer-unsaid', "the rings do not say when change saves nothing (a visitor)", " + (fin(p) && b === p ? ', no fewer than paying exactly' : '') +", " +"),
 ('rings-no-fewer-always', "the rings say \"no fewer than paying exactly\" of every amount", "(fin(p) && b === p ? ', no fewer than paying exactly' : '')", "(fin(p) ? ', no fewer than paying exactly' : '')"),
 ('button-on-its-own-line', "the label of the range is long again, so that at 360 wide the button drops to a line of its own and the rings leave the first screen (a visitor)", "<label>Amounts from 0 to <input", "<label>Amounts from 0 up to and including the largest, which is <input"),
 ('slider-on-its-own-line', "the slider stands under the amount, not beside it, and the first rings are off the first screen at 360 by 640", "  #fig3 .controls label:nth-child(2) { flex: 1 1 140px; } #fig3 input[type=range] { width: 100%; }\n", ""),
 ('swap-sentence-tangled', "after the swap the sentence runs \"where American coins take 4.7, if the coins are well chosen\" (a visitor: the \"if\" seems to belong to the 4.7)", "They take 3.89 on average if the coins are well chosen every time (American coins take 4.7);", "3.89 on average where American coins take 4.7, if the coins are well chosen every time;"),
 # ---- after the referee's reading (referee27/reading.md) and the reader's fourth visit
 ('best-coin-unscoped', 'the button calls its coin "the best coin for paying with change", where it is the best of those tried (the referee: a 21 beat every coin up to 13)', " + ', of the coins tried,' : ': the best coin tried') + ' for paying with change'", " : ': the best coin') + ' for paying with change'"),
 ('best-coin-sentence-unscoped', "the sentence under the second picture does not say how far coins were tried", "'With change, of the coins up to ' + (2 * L - 1) + ', it is <b>'", "'With change it is <b>'"),
 ('legend-says-upper-of-one', 'the legend says "the upper one is for paying exactly" over a single dashed line (the referee)', "$('nowLegend').textContent = isFinite(tp) && isFinite(tb) ?", "$('nowLegend').textContent = isFinite(tb) ?"),
 ('tooltip-outlives-its-coins', "the second picture's tooltip stays, with the old coins' figure, when other coins are chosen from the keyboard (the referee)", " S.hoverB = -1; $('tipB').style.display = 'none'; }", " }"),
 ('long-ways-as-rings', "ways of more than forty coins are drawn as forty rings \"and 23 more\", twelve rows alike (the referee)", "if (w.reduce(function (t, e) { return t + Math.abs(e[1]); }, 0) > 40) {", "if (false) {"),
 ('counting-unsaid', "a long count begins without a word (the referee: 3.3 s with no sign of working)", " btn.textContent = 'Counting\\u2026';", ""),
 ('not-searched-unsaid', 'the caption says every set was tried, over two rows that read "not searched" (the referee)', "Paying with change, every set of one to five coins up to <span id=\"bothMax\"></span>.", "Paying with change, every set up to <span id=\"bothMax\"></span>."),
 ('searched-to-250', "the caption gives 250 as the largest coin tried with change (the second of the referee's three copies)", "$('bothMax').textContent = BEST.bothMax;", "$('bothMax').textContent = 250;"),
 ('twice-the-largest', 'the caption says coins up to twice the largest amount are tried (the page tries one more: the referee)', "so coins up to one more than twice the largest amount are tried;", "so coins up to twice the largest amount are tried;"),
 ('sets-are-his', 'the foot says the best sets for paying exactly "are his" (the referee: more than my own sources say)', "The best sets for paying exactly are in that paper, and in the On-Line Encyclopedia of Integer Sequences (A366013). Shallit says there that others had posted such tables in 2000; and by Thomas Young's own account in the Encyclopedia (A364607), he and three students explored the best four coins in 1995.", "The best sets for paying exactly are his, and are in the On-Line Encyclopedia of Integer Sequences as A366013."),
 ('works-unread-unsaid', "the foot does not say that works I have not read may hold the sets for paying with change (the referee)", "; the list of sources beside the write-up names the works on the subject that I have not read, and if one of them has these sets, the credit is theirs.", "."),
 ('floor-uncredited', "the foot does not say whose the counting of the floor is (the referee)", " The counting behind the floor is Shallit's for paying exactly, and is carried over by me to paying with change.", ""),
 ('multiple-of-the-smallest-coin', "\"every coin is a multiple of\" the smallest coin, not of the common divisor (the third of the referee's three copies)", "'even with change: every coin is a multiple of ' + S.coins.reduce(P.gcd) + '.'", "'even with change: every coin is a multiple of ' + S.coins[0] + '.'"),
 ('of-the-hundred', "the tile says \"of the 100 from 1 to 99\" (the first of the referee's three copies)", "true, 'of the ' + (L - 1) + ' from 1 to ' + (L - 1) +", "true, 'of the ' + L + ' from 1 to ' + (L - 1) +"),
 ('with-few', 'the caption stops at "can be paid with few" (a visitor)', "so only so many amounts can be paid with few coins.", "so only so many amounts can be paid with few."),
 ('button-use-these-coins', 'the button reads "Use these coins" when only the range may have changed (a visitor)', '<button id="apply">Use these</button>', '<button id="apply">Use these coins</button>'),
 # ---- after the referee's check of the mending (referee27/mending.md) and the reader's fifth visit
 ('first-tooltip-outlives-its-coins', "the first picture's tooltip stays when other coins are chosen from the keyboard (a copy of the referee's that passed)", " S.hoverA = -1; $('tipA').style.display = 'none';", ""),
 ('legend-upper-of-two-in-one-place', 'the legend says "the upper one" where the two averages are equal and the lines lie on each other (the referee: 38 states of 314)', "(tp === tb ? 'the average now (the same for paying exactly and with change)' : 'the average now (the upper one is for paying exactly)')", "'the average now (the upper one is for paying exactly)'"),
 ('legend-with-change-of-nothing', 'the legend says "the average now, paying with change" where no amount-set can be paid at all (a copy of the referee\'s that passed)', ": isFinite(tb) ? 'the average now, paying with change (these coins cannot pay every amount exactly)' : 'no average now: these coins cannot pay every amount';", ": 'the average now, paying with change (these coins cannot pay every amount exactly)';"),
 ('lone-ring-unexplained', "nothing says what the ring that stands alone is when the coins have no 1 (a visitor)", "'the best coin' + (!isFinite(tp) && bp.length ? ' (the ring that stands alone is the 1, without which not every amount can be paid exactly)' : '');", "'the best coin';"),
 ('best-coin-of-several', 'the button says "the best coin" when several tie (the referee)', "(bp.length > 1 ? ': equal best' + others(bp) : ': the best coin') + ' for paying exactly'", "': the best coin for paying exactly'"),
 ('counted-twice', "a count already pending does not stop another from being started (the referee: the range box's change and the button's press each began one)", "    if (S.pending) return;\n", ""),
 ('boxes-open-while-counting', "the boxes and buttons stay open while a count is pending (the referee: what is typed meanwhile is written over, and a second press starts a second count)", "if (box) e.readOnly = true; else e.disabled = true; return d; }); }", "return d; }); }"),
 ('counts-before-it-is-drawn', 'the count begins at once, before "Counting…" can be drawn', "    if (window.requestAnimationFrame) requestAnimationFrame(function () { requestAnimationFrame(go); });\n    setTimeout(go, 300);", "    go();"),
 ('counting-shifts-the-page', 'the sign "Counting…" is put in the notice under the boxes, so that everything below it, the button pressed among it, shifts while the count is made (found by the test)', " btn.textContent = 'Counting\\u2026';", " notice('Counting\\u2026');"),
 ('credit-is-its', 'the foot ends "they are its" (a visitor stopped at it)', "the credit is theirs.", "they are its."),
 ('table-sentence-in-one', 'the sentence over the tables begins "For each number of coins in a set, every set was tried" (the referee: not so, taken by itself, for six and seven coins with change)', "These sets have the lowest average of all that were tried. Paying exactly, every set of one to seven coins up to", "For each number of coins in a set, every set was tried, and these have the lowest average. Paying exactly, every set of one to seven coins up to"),
 ('young-found', 'the foot says the best four coins "were found by" Young and his students (my sources quote "explored")', "he and three students explored the best four coins in 1995.", "he and his students found the best four coins in 1995."),
 # ---- after the referee's last look (referee27/last.md) and the reader's sixth visit
 ('open-while-it-counts', "the buttons open again just before the count is made, so that a second tap made while the page counts is answered when it has done: two counts, or a coin added that was never named (the referee)", "      var left = shut();", "      var left = BUSY.map(function () { return false; }); S.pending = false;"),
 ('best-set-while-a-count-is-pending', "a best set pressed while a count is pending is taken, and the count then lands on it (the referee: \"Added a 32\" over a tile that said \"cannot make 50 amounts\")", "      var t = e.target; if (S.pending) return;                                             /* not while", "      var t = e.target;                                             /* not while"),
 ('sentence-button-while-a-count-is-pending', "the button in the sentence over the tiles is taken while a count is pending", "      var t = e.target; if (S.pending) return;\n      if (t && t.getAttribute && t.getAttribute('data-set')) steady($('story'),", "      var t = e.target;\n      if (t && t.getAttribute && t.getAttribute('data-set')) steady($('story'),"),
 # mended 27 November: this fault shut the boxes and never opened them (the opening still set readOnly), so the test only stopped; it now shuts and opens them
 ('caret-lost', "the box typed in is disabled during a count, and loses the caret (the referee; on a phone the keyboard would close)", "box = id === 'coins' || id === 'L', d = box ? e.readOnly : e.disabled; if (box) e.readOnly = true; else e.disabled = true; return d; }); }\n  function open(was) { BUSY.forEach(function (id, k) { var e = $(id); if (id === 'coins' || id === 'L') e.readOnly = was[k]; else e.disabled = was[k]; }); }", "box = false, d = e.disabled; e.disabled = true; return d; }); }\n  function open(was) { BUSY.forEach(function (id, k) { $(id).disabled = was[k]; }); }"),
 ('no-count-without-frames', "where the browser draws no frames the count is never made, and the page stays shut on \"Counting…\" (a copy of the referee's that passed)", "    setTimeout(go, 300);\n", ""),
 ('legend-same-when-near', 'the legend says "the same for paying exactly and with change" when the two totals differ by one (a copy of the referee\'s that passed)', "(tp === tb ? 'the average now (the same", "(Math.abs(tp - tb) <= 1 ? 'the average now (the same"),
 ('one-of-the-best', 'the button says "one of the 2 best coins" (a visitor read it as one of the top two)', "(bp.length > 1 ? ': equal best' + others(bp) : ': the best coin')", "(bp.length > 1 ? ': one of the ' + bp.length + ' best coins' : ': the best coin')"),
 ('equal-best-names-itself', 'the button says "equal best with" the coin it adds', "function others(list) { var c = list.slice(1).map(", "function others(list) { var c = list.slice(0, list.length - 1).map("),
 # ---- the ninth stage (27 November, evening): room on a phone's first screen for the line the public site puts above the page
 ('key-back-above-the-amount', "the key to the rings stands above the box for the amount again, so that on the public site the first row of rings is cut by the foot of a small phone's screen",
  '''  <figure class="viz-root" id="fig3">
    <div class="controls">
      <label>Amount <input type="number" id="amount" min="0" step="1" aria-describedby="amountSay"></label>
      <label><input type="range" id="amountR" min="0" step="1" aria-label="Amount"></label>
    </div>
    <p class="say" id="amountSay" role="status"></p>
    <div class="ways" id="ways"></div>
    <figcaption id="ringkey">A coin with a <b>solid ring</b> is handed over; a coin with a <b>dashed ring</b> is handed back.</figcaption>
  </figure>''',
  '''  <figure class="viz-root" id="fig3">
    <figcaption id="ringkey">A coin with a <b>solid ring</b> is handed over; a coin with a <b>dashed ring</b> is handed back.</figcaption>
    <div class="controls">
      <label>Amount <input type="number" id="amount" min="0" step="1" aria-describedby="amountSay"></label>
      <label><input type="range" id="amountR" min="0" step="1" aria-label="Amount"></label>
    </div>
    <p class="say" id="amountSay" role="status"></p>
    <div class="ways" id="ways"></div>
  </figure>'''),
 ('key-to-the-rings-gone', "nothing says what a solid ring and a dashed ring are", '''    <figcaption id="ringkey">A coin with a <b>solid ring</b> is handed over; a coin with a <b>dashed ring</b> is handed back.</figcaption>\n''', ""),
 ('opening-takes-more-room', "the opening paragraph has 3em under it: at home the rings still fit a small phone's first screen, and under the public site's line they do not", "  p.sub { margin: 0 0 12px;", "  p.sub { margin: 0 0 3em;"),
 ('key-hidden-on-a-narrow-phone', "the key to the rings is hidden on a screen up to 340 px wide (a copy of the referee's that passed)", "  #ringkey { margin: 8px 0 0; }", "  #ringkey { margin: 8px 0 0; } @media (max-width: 340px) { #ringkey { display: none; } }"),
 ('key-over-the-rings-again-by-style', "the key is drawn above the rings by a style rule, though it follows them in the file", "  #ringkey { margin: 8px 0 0; }", "  #fig3 { display: flex; flex-direction: column; } #ringkey { margin: 8px 0 0; order: -1; }"),
 ('title-larger', "the title is set in 40 px, which costs the first screen 21 px", "  h1 { font-weight: normal; font-size: 26px; margin: 0 0 2px; }", "  h1 { font-weight: normal; font-size: 40px; margin: 0 0 2px; }"),
]
def stopped(r, first):
    """the test threw before its end: what it had found by then (it prints that since 27 November), or the last line of its error"""
    m = re.search(r'THE TEST STOPPED after (\d+) assertions, (\d+) of them failed; it stopped at: (.*)', r.stdout)
    if not m: return 'caught: the test stops (%s)' % (r.stderr.strip().splitlines() or ['no output'])[-1][:90]
    if int(m.group(2)) > 0: return 'caught: %s assertions fail and then the test stops, after %s: %s' % (m.group(2), m.group(1), (first[0] if first else '')[:110])
    return 'caught ONLY BY THE TEST STOPPING, after %s assertions that all pass, at: %s' % (m.group(1), m.group(3)[:110])
def one(job):
    name, what, a, b = job; d = os.path.join(WORK, name); os.makedirs(d, exist_ok=True); s = SRC
    if a is not None: s = s.replace(a, b)
    path = os.path.join(d, 'change.html'); open(path, 'w', encoding='utf-8').write(s.replace('/*CORE*/', CORE).replace('/*BEST*/null', BEST))
    env = dict(os.environ, LD_LIBRARY_PATH=os.path.join(WEB, 'sysroot/usr/lib/x86_64-linux-gnu'), NODE_PATH=os.path.join(WEB, 'node_modules'))
    try:
        r = subprocess.run(['nice', '-n', '15', 'node', 'shot-change.js', path, d, os.path.join(HERE, 'pcore.js')], cwd=WEB, env=env, capture_output=True, text=True, timeout=600)
        m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed', r.stdout); first = [l[8:] for l in r.stdout.split('\n') if l.startswith('FAILED: ')]
        res = ('caught: %s of %s assertions fail: %s' % (m.group(2), m.group(1), (first[0] if first else '')[:110])) if m and int(m.group(2)) > 0 else ('NOT caught: all %s assertions pass' % m.group(1)) if m else stopped(r, first)
    except subprocess.TimeoutExpired: res = 'caught: the test does not finish'
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    os.rmdir(d); return name, what, res
if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    SRC = rd('page.src.html'); CORE = rd('pcore.js'); BEST = json.dumps(json.loads(rd('best.json')), separators=(',', ':'))
    for name, what, a, b in M: assert SRC.count(a) == 1, (name, SRC.count(a))
    assert open(os.path.join(WEB, 'shot-change.js'), encoding='utf-8').read() == rd(os.path.join('tools', 'shot-change.js')), 'the test in ~/web is not the copy in tools/'
    jobs = int(sys.argv[1]) if len(sys.argv) > 1 else 4; only = sys.argv[2].split(',') if len(sys.argv) > 2 else None; t0 = time.time()
    chosen = [m for m in M if only is None or m[0] in only]; assert only is None or len(chosen) == len(only), 'a name asked for is not in the list'
    first = one(('control-alone', '', None, None)); assert first[2].startswith('NOT caught'), 'the true page does not pass by this runner: ' + first[2]
    print('control, alone: the true page, built and run in the same way: %s\n' % first[2].replace('NOT caught: ', ''), flush=True)
    todo = list(chosen); step = max(1, len(todo) // 4)
    for k, at in enumerate(range(step // 2, len(chosen), step)): todo.insert(at + k, ('control-%d' % (k + 1), 'THE TRUE PAGE, run among the broken copies, %d at a time' % jobs, None, None))
    caught = 0; controls = []
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for name, what, res in ex.map(one, todo):
            if name.startswith('control-'): controls.append(res); print('%-40s %s -- %s' % (name, what, 'passes: ' + res.replace('NOT caught: ', '') if res.startswith('NOT caught') else 'FAILS UNDER LOAD: ' + res), flush=True); continue
            caught += res.startswith('caught'); print('%-40s %s -- %s' % (name, what, res), flush=True)
    print('\n%d of %d broken copies of the page caught%s; the true page run among them %d times passed %d times; %d at a time, %.0f minutes' % (caught, len(chosen), '' if only is None else ' (a part of the list of %d, by name)' % len(M), len(controls), sum(c.startswith('NOT caught') for c in controls), jobs, (time.time() - t0) / 60))
