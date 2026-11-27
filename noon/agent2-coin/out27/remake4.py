"""Fourth stage of the coin page's remake, after the reader's second visit (reader/visit-2.md): "paying exactly" for "fewest coins"
(which stood above a smaller number); the story of the 18 follows the coins chosen, and its button can be pressed back; the ways of
paying with change are set apart; the buttons that add a coin say which coin; "cannot be below" for "least possible".
python -I remake4.py   (run after remake3.py: it changes page.src.html in place)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'page.src.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:100], s.count(a)); s = s.replace(a, b)
    # ---- styles
    rep("  button.inline { font: inherit; font-style: italic; color: inherit; background: transparent; border: 0; border-bottom: 1px solid currentColor; border-radius: 0; padding: 2px 1px 1px; }\n  @media (hover: hover) { button.inline:hover { background: #32322f; } }\n",
        "  button.inline { min-height: 32px; margin: 2px 0; }                 /* a button in a sentence looks like the page's other buttons (a visitor took an underlined one for a link) */\n  .or { color: var(--text-secondary); font-size: 13px; margin: 2px 0 0; }\n  #amountSay, #addedSay { min-height: 0; }\n")
    # ---- words
    rep('<button id="apply">Count</button>', '<button id="apply">Use these coins</button>')
    rep("""    <figcaption id="avgcap">Count every amount once, and take the average number of coins. With American coins it is 4.7. <button class="inline" data-set="1,5,18,25">Swap the 10 for an 18</button> and it is 3.89, if the coins are well chosen every time; a cashier, who takes the largest coin that fits, would need 4.58 with those coins.</figcaption>
    <div class="tiles">""", """    <figcaption id="avgcap">Count every amount once, and take the average number of coins it takes.</figcaption>
    <p class="say" id="story"></p>
    <p class="say" id="withThese"></p>
    <div class="tiles">""")
    rep("<span><b>Fewest coins</b>: paid exactly, with as few coins as can be</span>", "<span><b>Paying exactly</b>, with as few coins as can be</span>")
    rep("<span><b>The cashier's way</b>: paid exactly, taking the largest coin that fits, again and again</span>", "<span><b>The cashier's way</b> of paying exactly: the largest coin that fits, again and again</span>")
    rep("<span><b>With change</b>: coins may be handed back, and every coin that changes hands is counted</span>", "<span><b>Paying with change</b>: coins may be handed back, and every coin that changes hands is counted</span>")
    rep('aria-label="Number of coins for each amount, with the fewest coins and with change"', 'aria-label="Number of coins for each amount, paid exactly and paid with change"')
    rep("</svg> fewest coins (the wider line, so that it shows where the two run together)</li>", "</svg> paying exactly (the wider line, so that it shows where the two run together)</li>")
    rep("</svg> with change</li>\n      <li><svg width=\"14\" height=\"12\" viewBox=\"0 0 14 12\"><circle cx=\"7\" cy=\"6\" r=\"4\" fill=\"none\" stroke=\"#f0efec\" stroke-width=\"1.5\"/></svg> where the cashier's way takes more than the fewest</li>",
        "</svg> paying with change</li>\n      <li><svg width=\"14\" height=\"12\" viewBox=\"0 0 14 12\"><circle cx=\"7\" cy=\"6\" r=\"4\" fill=\"none\" stroke=\"#f0efec\" stroke-width=\"1.5\"/></svg> where the cashier's way takes more than need be (the ring stands at the cashier's count)</li>")
    rep("""      <button id="addPlain">Add the best coin for the fewest coins</button>
      <button id="addBoth">Add the best coin for paying with change</button>""", """      <button id="addPlain">Add the best coin for paying exactly</button>
      <button id="addBoth">Add the best coin for paying with change</button>""")
    rep("</svg> fewest coins</li>\n      <li><svg width=\"26\" height=\"12\" viewBox=\"0 0 26 12\"><line x1=\"1\" y1=\"6\" x2=\"25\" y2=\"6\" stroke=\"#d95926\" stroke-width=\"2.5\"/></svg> with change</li>",
        "</svg> paying exactly</li>\n      <li><svg width=\"26\" height=\"12\" viewBox=\"0 0 26 12\"><line x1=\"1\" y1=\"6\" x2=\"25\" y2=\"6\" stroke=\"#d95926\" stroke-width=\"2.5\"/></svg> paying with change</li>")
    rep("</svg> the average now (the upper one is for the fewest coins)</li>", "</svg> the average now (the upper one is for paying exactly)</li>")
    rep("""    <figcaption>For each number of coins every set was tried (coins up to 99 for the fewest coins, up to 150 with change), and these have the lowest average. Press a set to try it at the top of the page. "Least possible" is what counting alone allows: no set of that many coins could do better.</figcaption>
    <h3>For the fewest coins</h3>""", """    <figcaption>For each number of coins in a set, every set was tried (coins up to 99 for paying exactly, up to 150 with change), and these have the lowest average. Press a set to try it at the top of the page. The last column is what a count shows: no set of that many coins can get under that figure, and the best sets often do not reach it.</figcaption>
    <h3>Paying exactly</h3>""")
    rep("    <h3>With change</h3>\n    <p class=\"say\">From two coins up,", "    <h3>Paying with change</h3>\n    <p class=\"say\">From two coins up,")
    rep("the best sets for the fewest coins are his, and are in the On-Line Encyclopedia", "the best sets for paying exactly are his, and are in the On-Line Encyclopedia")
    rep('"Never more than the fewest, however large the amount" is decided by a test of D. Pearson\'s', '"Never more than need be, however large the amount" is decided by a test of D. Pearson\'s')
    rep("{ name: 'best five, fewest coins: 1, 5, 16, 23, 33', coins: [1, 5, 16, 23, 33], L: 100 }", "{ name: 'best five, paying exactly: 1, 5, 16, 23, 33', coins: [1, 5, 16, 23, 33], L: 100 }")
    # ---- script: the story, and the line that names the coins
    rep("""    $('capA').textContent = 'The coins for each amount from 0 to ' + (L - 1);""", """    $('capA').textContent = 'The coins for each amount from 0 to ' + (L - 1);
    var us = L === 100 && S.coins.join() === '1,5,10,25', sh = L === 100 && S.coins.join() === '1,5,18,25', btn = function (set, label) { return '<button class="inline" data-set="' + set + '">' + label + '</button>'; };
    $('story').innerHTML = us ? 'American coins take 4.7 on average. ' + btn('1,5,18,25', 'Swap the 10 for an 18') + ' and it is 3.89, if the coins are well chosen every time; a cashier, who takes the largest coin that fits, would need 4.58 with those coins.'
      : sh ? 'These are the American coins with the 10 swapped for an 18: 3.89 on average where American coins take 4.7, if the coins are well chosen every time; a cashier, who takes the largest coin that fits, needs 4.58 with these. ' + btn('1,5,10,25', 'Put the 10 back')
      : 'For comparison: American coins (1, 5, 10, 25, for the amounts from 0 to 99) take 4.7 on average, and 3.89 with the 10 swapped for an 18. ' + btn('1,5,10,25', 'Try the American coins');
    $('withThese').textContent = 'With the coins chosen above (' + S.coins.join(', ') + '), for the amounts from 0 to ' + (L - 1) + ':';""")
    rep("tile('tile-greedy', costText(tg, L), false, pf === 0 ? 'With these coins the cashier never takes more than the fewest, however large the amount.' :\n        (fails.length ? 'More than the fewest for '",
        "tile('tile-greedy', costText(tg, L), false, pf === 0 ? 'With these coins the cashier never takes more than need be, however large the amount.' :\n        (fails.length ? 'More than need be for '")
    rep("'The fewest for every amount here, but not for ' + pf + ': '", "'No more than need be for any amount here, but for ' + pf + ': '")
    rep("{ y: lastFinite(S.plain) === null ? null : f.Y(lastFinite(S.plain)), color: '#3987e5', text: 'fewest coins' },", "{ y: lastFinite(S.plain) === null ? null : f.Y(lastFinite(S.plain)), color: '#3987e5', text: 'exactly' },")
    rep("', with the fewest coins and with change' + (fails ? '; the cashier\\'s way takes more at '", "', paid exactly and paid with change' + (fails ? '; the cashier\\'s way takes more at '")
    rep("out.push(fin(p) ? 'fewest coins <b>' + p + '</b>'", "out.push(fin(p) ? 'paid exactly <b>' + p + '</b>'")
    rep("""      out.push('with change <b>' + b + '</b>' + (s && s.ways.length ? ' (' + esc(schemeText(s.ways[0])) + ')' : ''));""",
        """      out.push('with change <b>' + b + '</b>' + (fin(p) && b === p && a > 0 ? ' (no fewer)' : s && s.ways.length ? ' (' + esc(schemeText(s.ways[0])) + ')' : ''));      /* (a visitor: "with change 5 (3 × 25 + 1 handed over, 5 handed back) when five coins paid exactly would do. So what?") */""")
    rep("<th>amount</th><th>fewest coins</th><th>the cashier\\'s way</th><th>with change</th>", "<th>amount</th><th>paid exactly</th><th>the cashier\\'s way</th><th>with change</th>")
    rep("labels.push({ y: f.Y(tp / L), color: '#3987e5', text: 'fewest coins now' });", "labels.push({ y: f.Y(tp / L), color: '#3987e5', text: 'exactly, now' });")
    rep("labels.push({ y: f.Y(tb / L), color: '#d95926', text: 'with change now' });", "labels.push({ y: f.Y(tb / L), color: '#d95926', text: 'with change, now' });")
    # the buttons that add a coin say which; at sixteen coins they say why they stop
    rep("    $('addPlain').disabled = bp.length === 0 || full; $('addBoth').disabled = bb.length === 0 || full;",
        """    $('addPlain').disabled = bp.length === 0 || full; $('addBoth').disabled = bb.length === 0 || full;
    $('addPlain').textContent = full ? 'No coin can be added: ' + MAXCOINS + ' is as many as this page takes' : bp.length ? 'Add a ' + bp[0].coin + ': the best coin for paying exactly' : 'No coin to add for paying exactly';
    $('addBoth').textContent = bb.length ? 'Add a ' + bb[0].coin + ': the best coin for paying with change' : 'No coin to add for paying with change'; $('addBoth').style.display = full ? 'none' : '';""")
    rep("""    if (S.coins.length >= MAXCOINS) out.push('There are ' + MAXCOINS + ' coins, which is as many as this page takes, so no more can be added.');
    if (bp.length) out.push('For the fewest coins the best coin to add is <b>'""", """    if (S.coins.length >= MAXCOINS) return 'There are ' + MAXCOINS + ' coins, which is as many as this page takes, so no more can be added.';
    if (bp.length) out.push('Paying exactly, the best coin to add is <b>'""")
    rep("out.push('For the fewest coins there is no coin left to try: every value up to '", "out.push('Paying exactly there is no coin left to try: every value up to '")
    rep("out.push('For the fewest coins no single coin lowers the average of '", "out.push('Paying exactly no single coin lowers the average of '")
    rep("(c <= L - 1 ? 'fewest coins ' + (o === null", "(c <= L - 1 ? 'paying exactly ' + (o === null")
    rep("<th>new coin</th><th>fewest coins</th><th>with change</th>", "<th>new coin</th><th>paying exactly</th><th>with change</th>")
    rep("""<p class="k">Fewest coins: ' + (fin(p) ? '<b>' + plural(p, 'coin') + '</b>' : '<b>cannot be paid exactly</b> with these coins')""", """<p class="k">Paid exactly: ' + (fin(p) ? '<b>' + plural(p, 'coin') + '</b>' : '<b>it cannot be</b> with these coins')""")
    rep("""        h += '<div class="row scheme">' + (over.length""", """        h += (i ? '<p class="or">or</p>' : '') + '<div class="row scheme">' + (over.length""")
    rep("var head = '<tr><th>coins</th><th class=\"l\">the best sets</th><th>average</th><th>least possible</th></tr>'", "var head = '<tr><th>coins in the set</th><th class=\"l\">the best sets</th><th>average</th><th>cannot be below</th></tr>'")
    # the amount: a number too large is brought to the largest, and the page says so
    rep("""    $('amount').addEventListener('input', function () { if (/^\\d+$/.test($('amount').value)) setAmount(Number($('amount').value)); });""",
        """    $('amount').addEventListener('input', function () { var v = $('amount').value; if (/^\\d+$/.test(v)) { setAmount(Number(v)); if (Number(v) > S.L - 1) $('amountSay').textContent = v + ' is more than ' + (S.L - 1) + ', the largest amount here: the amount is ' + S.amount + '.'; } });""")
    rep("""      if (String(typed) !== String(S.amount)) $('amountSay').textContent =""", """      if (String(typed) !== String(S.amount) && !/^\\d+$/.test(typed)) $('amountSay').textContent =""")
    rep("""    $('addPlain').addEventListener('click', function () { addBest(S.addPlain, P.total(S.plain), 'with the fewest coins', $('addPlain')); });""", """    $('addPlain').addEventListener('click', function () { addBest(S.addPlain, P.total(S.plain), 'paying exactly', $('addPlain')); });""")
    rep("""    $('addBoth').addEventListener('click', function () { addBest(S.addBoth, P.total(S.both), 'with change', $('addBoth')); });""", """    $('addBoth').addEventListener('click', function () { addBest(S.addBoth, P.total(S.both), 'paying with change', $('addBoth')); });""")
    rep("""    [].forEach.call(document.querySelectorAll('button.inline'), function (b) { b.addEventListener('click', function () { steady(b, function () { setCoinage(b.getAttribute('data-set').split(',').map(Number), 100); matchPreset(); }); }); });""",
        """    $('story').addEventListener('click', function (e) {                                       /* the button in the story: it is made afresh each time, so the paragraph listens for it and is what is held steady */
      var t = e.target; if (t && t.getAttribute && t.getAttribute('data-set')) steady($('story'), function () { setCoinage(t.getAttribute('data-set').split(',').map(Number), 100); matchPreset(); });
    });""")
    open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('page.src.html, fourth stage:', len(s))
