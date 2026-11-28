"""Fourth stage of the gasket page's remake, after the plain reader's second visit (reader27/visit-2.md).   python -I out27/remake4.py   (run after remake3.py)
What the reader met: the answer to a tap fell 200 px below the circle, under three rows of buttons, and at 360 by 640 off the screen; the
button that swaps the two gaskets moved 59 px under the finger; "Magnify" left the chosen circle at the edge, then let go of it ("I expected
the circle I chose to come to the middle and stay there"); a magnified picture could not be moved up or down with fingers; with nothing
chosen "Magnify" closed in on the inside of the big circle; "Divided by 24 it leaves 12. So what?" before the test had been told of; the
menu's "no 2n², no 3n²" likewise; "Back to the gasket with squares" on that very gasket; "Magnified 1 times"; a table of centres;
the list's button left under an error; the example of the test stopped half-way; two sentences read twice.
What it changes:
  - under the picture, in this order: the line for a tap, the buttons that magnify and move, the legend, the button that swaps the two
    gaskets, its sentence (under the button, so that the button keeps its place), the menus, the count;
  - "Magnify" brings the chosen circle to the middle and doubles the picture about it; with nothing chosen it chooses for the visitor
    the largest lit circle that has room to grow (or the largest such circle of all) and says which; four arrows move the picture;
  - the line for a tap says what the number is and what "Magnify" will do, and no longer what it leaves on division by 24;
  - the menu's choices say in words what never comes; "Not magnified"; "Light the squares again" on the gasket with squares;
  - the table has no column of centres; the third panel clears its list when it refuses what is typed;
  - "What is going on": the example of the test is finished, and two sentences are plainer."""
H = '/home/agent2/gasket/'
if __name__ == '__main__':
    s = open(H + 'page.src.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:110], s.count(a)); s = s.replace(a, b)
    # ---- the order of things under the picture
    rep("""      <ul class="legend"><li><i style="background:var(--fam)"></i><b id="hiName">a square</b></li><li><i style="border:1px solid var(--muted);box-sizing:border-box"></i>any other number</li></ul>
      <p class="say" id="gstory"></p>
      <div class="controls"><button id="zin">Magnify ×2</button><button id="zout">Draw back ÷2</button><button id="home">The whole gasket</button></div>
      <p class="say" id="gpick" aria-live="polite"></p>
""", """      <p class="say" id="gpick" aria-live="polite"></p>
      <div class="controls" id="gmove"><button id="zin">Magnify ×2</button><button id="zout">Draw back ÷2</button><button id="home">The whole gasket</button><span class="arrows"><button id="mleft" aria-label="Look further left">←</button><button id="mup" aria-label="Look further up">↑</button><button id="mdown" aria-label="Look further down">↓</button><button id="mright" aria-label="Look further right">→</button></span></div>
      <ul class="legend"><li><i style="background:var(--fam)"></i><b id="hiName">a square</b></li><li><i style="border:1px solid var(--muted);box-sizing:border-box"></i>any other number</li></ul>
      <div class="controls" id="gswap"><button id="swap" data-to="0">Show a gasket with no square in it</button></div>
      <p class="say" id="gstory"></p>
""")
    rep("""With fingers: pinch to magnify, drag sideways to move. With a mouse: scroll to magnify, drag to move.""", """With fingers: pinch to magnify; drag sideways, or press the arrows, to move. With a mouse: scroll to magnify, drag to move.""")
    rep("#gstory { margin-bottom: 12px; } #gstory button { margin: 6px 0 0; } #gpick { margin: 10px 0 12px; }", "#gstory { margin: 0 0 12px; } #gswap { margin: 10px 0 6px; } #gpick { margin: 8px 0 10px; min-height: 40px; } .arrows { display: inline-flex; gap: 6px; } .arrows button { min-width: 38px; padding: 5px 0; }")
    # ---- the sentence that goes with the two gaskets, and its button, which now stands above it
    i = s.index("  function story() {"); j = s.index("  $('gstory').addEventListener('click'"); k = s.index("\n", j)
    s = s[:i] + """  function story() { var key = pack.root.join(','), sq = $('hi').value === '1', h = '', label = 'Back to the gasket with squares', to = '1', btn = $('swap');
    if (key === '-4,5,20,21' && sq) { h = 'In this gasket squares turn up: the two largest orange circles are marked 36, which is 6 \\u00d7 6.'; label = 'Show a gasket with no square in it'; to = '0'; }
    else if (key === '-3,5,8,8' && sq) h = 'In this gasket nothing is lit, and nothing will be, however far you magnify: no square is the number of any of its circles. That was proved in 2023, against what had been believed for twenty years.';
    else if (key === '-4,5,20,21') label = 'Light the squares again';
    if ($('gstory').textContent !== h) $('gstory').textContent = h; if (btn.textContent !== label) btn.textContent = label; btn.setAttribute('data-to', to); }
  $('swap').addEventListener('click', function () { var to = this.getAttribute('data-to'); $('hi').value = '1'; $('pack').value = to; setPack(PRESETS[+to]); });""" + s[k:]
    # ---- the line for a tap; Magnify brings the chosen circle to the middle; with nothing chosen it chooses
    i = s.index("  function pickWords(i) {"); j = s.index("  function zoomAt(f, px, py) {")
    s = s[:i] + """  function pickWords(i) { var b, facts = [];
    if (i < 0) return sel ? 'The circle marked <b>' + group(sel[0]) + '</b> is out of the picture now. \\u201cThe whole gasket\\u201d shows everything again.' : (NARROW ? 'Tap' : 'Click') + ' a circle, and this line says what its number is.';
    b = drawn[i][0]; [1, 2, 3, 6].forEach(function (u) { var n; if (b % u === 0 && G.isSquare(b / u)) { n = Math.round(Math.sqrt(b / u)); facts.push(group(b) + ' = ' + (u === 1 ? '' : u + ' \\u00d7 ') + group(n) + ' \\u00d7 ' + group(n) + (u === 1 ? ', a square' : u === 2 ? ', twice a square' : u === 3 ? ', three times a square' : ', six times a square')); } });
    return 'The circle marked <b>' + group(b) + '</b>: ' + (facts.length ? facts.join('; ') : 'not a square, nor 2, 3 or 6 times one') + '. ' + (small(i) ? '\\u201cMagnify\\u201d closes in on it.' : 'It fills the picture: choose one of the small circles round it to go further.'); }
  function small(i) { return view.s / Math.abs(drawn[i][0]) < 0.3 * Math.min(W, H) / 2; }             /* a circle that still has room to grow in the picture; magnifying about the middle of a large one shows only its inside */
  function ident(c) { return [c[0], c[1], c[2], c[5] || 0]; }
  // with nothing chosen, "Magnify" chooses: the largest lit circle that has room to grow and whose middle is in the picture, or, with none lit, the largest such circle
  function autoPick() { var test = hiTest(), best = -1, bestLit = -1, i, c, b, x, y;
    for (i = 0; i < drawn.length; i++) { c = drawn[i]; b = c[0]; if (b <= 0 || !small(i) || view.s / b < 2) continue; x = W / 2 + c[3] / b * view.s; y = H / 2 - c[4] / b * view.s; if (x < 0 || x > W || y < 0 || y > H) continue;
      if (best < 0 || b < drawn[best][0]) best = i; if (test && test(b) && (bestLit < 0 || b < drawn[bestLit][0])) bestLit = i; }
    return bestLit >= 0 ? bestLit : best; }
  function magnify() { var i = selIndex(), c; if (i < 0 && !sel) { i = autoPick(); if (i >= 0) sel = ident(drawn[i]); }
    if (i >= 0 && small(i)) { c = drawn[i]; view.cx += c[3] / c[0]; view.cy += c[4] / c[0]; }                    /* the chosen circle comes to the middle, and stays there while the picture doubles */
    zoomAt(2, W / 2, H / 2); }
  function move(dx, dy) { var d = Math.min(W, H) / 3 / view.s; view.cx += dx * d; view.cy += dy * d; hover = -1; $('gtip').style.display = 'none'; draw(); }
""" + s[j:]
    rep("$('zin').addEventListener('click', function () { var p = target(); zoomAt(2, p[0], p[1]); }); $('zout').addEventListener('click', function () { var p = target(); zoomAt(0.5, p[0], p[1]); }); $('home').addEventListener('click', home);",
        "$('zin').addEventListener('click', magnify); $('zout').addEventListener('click', function () { zoomAt(0.5, W / 2, H / 2); }); $('home').addEventListener('click', home);\n  $('mleft').addEventListener('click', function () { move(-1, 0); }); $('mright').addEventListener('click', function () { move(1, 0); }); $('mup').addEventListener('click', function () { move(0, 1); }); $('mdown').addEventListener('click', function () { move(0, -1); });")
    rep("if (i >= 0) { c = drawn[i]; sel = [c[0], c[1], c[2], c[5] || 0]; } else sel = null;", "if (i >= 0) sel = ident(drawn[i]); else sel = null;")
    # ---- words: not magnified; the count's remainders; the menu's choices
    rep("(mag >= 0.9995 ? 'Magnified ' + (mag >= 100 ? group(Math.round(mag)) : +mag.toPrecision(3)) + ' times.' :", "(Math.abs(mag - 1) < 0.0005 ? 'Not magnified.' : mag > 1 ? 'Magnified ' + (mag >= 100 ? group(Math.round(mag)) : +mag.toPrecision(3)) + ' times.' :")
    rep("' Its numbers leave ' + t.res.join(', ') + ' on division by 24'", "' Its numbers all leave ' + t.res.join(', ').replace(/, (\\d+)$/, ' or $1') + ' on division by 24 (the test told of below)'")
    rep("var NOTE = { '-3,5,8,8': 'no squares, no 6n²', '-4,5,20,21': 'no 2n², no 3n²', '-1,2,2,3': 'the bug-eye: no family', '0,0,1,1': 'the strip: no family', '-3,4,12,13': 'no 2n², no 6n²', '-2,3,6,7': 'no 2n²',",
        "var NOTE = { '-3,5,8,8': 'never a square, nor 6 × a square', '-4,5,20,21': 'never 2 × a square, nor 3 × a square', '-1,2,2,3': 'the bug-eye: nothing barred', '0,0,1,1': 'the strip: nothing barred', '-3,4,12,13': 'never 2 × a square, nor 6 × a square', '-2,3,6,7': 'never 2 × a square',")
    # ---- the table without its centres
    rep("""'<table><tr><th>curvature</th><th>centre</th><th>remainder on division by 24</th><th class="l">' + esc(hiWords()) + '?</th></tr>' + rows.map(function (c) { return '<tr><td>' + group(c[0]) + '</td><td>(' + frac(trueX(c), c[0]) + ', ' + frac(c[2], c[0]) + ')</td><td>' + (c[0] % 24) + '</td>""",
        """'<table><tr><th>number</th><th>left over on division by 24</th><th class="l">' + esc(hiWords()) + '?</th></tr>' + rows.map(function (c) { return '<tr><td>' + group(c[0]) + '</td><td>' + (c[0] % 24) + '</td>""")
    # ---- the third panel: a refusal clears the list and its button
    rep("may = [], no = []; $('show').disabled = true; $('tnums').innerHTML = '';", "may = [], no = []; $('show').disabled = true; $('tnums').innerHTML = ''; $('tlist').hidden = true;")
    # ---- what is going on
    rep("Fill every gap, and every gap that leaves, for ever: that is an Apollonian gasket.", "Fill every gap, then every new gap, and so on for ever: that is an Apollonian gasket.")
    rep("""Divide a number by 24 and look at what is left over: in the two gaskets of the button above, only numbers that leave 0, 5, 8, 12, 20 or 21 are ever a circle's number. 36 leaves 12, so it passes that test, and in <b>(&minus;4, 5, 20, 21)</b> it is there.""",
        """Divide a number by 24 and look at what is left over. In <b>(&minus;4, 5, 20, 21)</b> and in <b>(&minus;3, 5, 8, 8)</b>, the two gaskets of the picture's button, only numbers that leave 0, 5, 8, 12, 20 or 21 are ever a circle's number. 36 leaves 12, so it passes that test. In <b>(&minus;4, 5, 20, 21)</b> it is there; in <b>(&minus;3, 5, 8, 8)</b> it never comes.""")
    rep("That the blue numbers give out is not known;", "That the blue numbers come to an end is not known;")          # the foot, in the caption's words
    open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('gasket page: after the second visit (stage 4)')
