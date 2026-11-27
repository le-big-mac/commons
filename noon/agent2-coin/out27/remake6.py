"""Sixth stage of the coin page's remake, after the referee's reading (referee27/reading.md) and the reader's fourth visit.
python -I remake6.py   (run after remake5.py: it changes page.src.html in place)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'page.src.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:100], s.count(a)); s = s.replace(a, b)
    # ---- words that said more than is so (the referee)
    rep("""<figcaption>For each number of coins in a set, every set was tried (coins up to 99 for paying exactly, up to 150 with change), and these have the lowest average.""",
        """<figcaption>For each number of coins in a set, every set was tried, and these have the lowest average: with coins up to <span id="plainMax"></span> for paying exactly; with coins up to <span id="bothMax"></span> for paying with change, and there for sets of up to five coins only.""")
    rep("""so only so many amounts can be paid with few. No set of that many coins can get under it, and the best sets often do not reach it.</figcaption>""",
        """so only so many amounts can be paid with few coins. No set of that many coins can get under it, and the best sets often do not reach it.</figcaption>""")
    rep("""(With change, a coin larger than the amount can be handed over, so coins up to twice the largest amount are tried.)</figcaption>""",
        """(With change, a coin larger than the amount can be handed over, so coins up to one more than twice the largest amount are tried, and no larger ones.)</figcaption>""")
    rep("""</svg> the average now (the upper one is for paying exactly)</li>""", """</svg> <span id="nowLegend">the average now (the upper one is for paying exactly)</span></li>""")
    i = s.index('  <p class="note">The sums are exact:'); j = s.index('</main>', i)
    s = s[:i] + """  <p class="note">The sums are exact: each average is a whole number of coins divided by the number of amounts. Jeffrey Shallit asked in 2003 which coins make the average least, in a paper called "What this country needs is an 18¢ piece". The best sets for paying exactly are in that paper, where he says that others had posted such tables in 2000, and in the On-Line Encyclopedia of Integer Sequences (A366013); the best four coins were found by Thomas Young and his students in 1995. The floor's counting is Shallit's for paying exactly, and is carried over by me to paying with change. The best sets for paying with change I did not find in print; the write-up lists the works on the subject that I have not read, and if one of them has these sets, they are its. "Never more than need be, however large the amount" is decided by a test of D. Pearson's, as Shallit gives it. The study behind this page, with what was expected beforehand and what two referees changed, is in <a href="README.md">the write-up</a> beside it.</p>
""" + s[j:]
    rep('<button id="apply">Use these coins</button>', '<button id="apply">Use these</button>')
    # ---- the best coin with change is the best of those tried, and says so (the referee: with coins 20, 22, 24, 26 and amounts 0 to 6 a 21 does better than any coin up to 13)
    rep("""$('addBoth').textContent = bb.length ? 'Add a ' + bb[0].coin + ': the best coin for paying with change' : 'No coin to add for paying with change';""",
        """$('addBoth').textContent = bb.length ? 'Add a ' + bb[0].coin + ': the best coin up to ' + n + ' for paying with change' : 'No coin up to ' + n + ' to add for paying with change';""")
    rep("""    if (bb.length) out.push('With change it is <b>' + names(bb) + '</b>, '""", """    if (bb.length) out.push('With change, of the coins up to ' + (2 * L - 1) + ', it is <b>' + names(bb) + '</b>, '""")
    # ---- the legend of the second picture says which lines there are
    rep("""    $('addPlain').disabled = bp.length === 0 || full; $('addBoth').disabled = bb.length === 0 || full;""",
        """    $('nowLegend').textContent = isFinite(tp) && isFinite(tb) ? 'the average now (the upper one is for paying exactly)' : isFinite(tb) ? 'the average now, paying with change (these coins cannot pay every amount exactly)' : 'no average now: these coins cannot pay every amount';
    $('addPlain').disabled = bp.length === 0 || full; $('addBoth').disabled = bb.length === 0 || full;""")
    # ---- a way of more than forty coins is written out, so that two ways do not look alike
    rep("""        h += (i ? '<p class="or">or</p>' : '') + '<div class="row scheme">' + (over.length""",
        """        if (w.reduce(function (t, e) { return t + Math.abs(e[1]); }, 0) > 40) { h += (i ? '<p class="or">or</p>' : '') + '<div class="row scheme words"><span class="lab">' + esc(schemeText(w)) + '</span></div>'; continue; }      /* too many rings to tell one way from the next: in words */
        h += (i ? '<p class="or">or</p>' : '') + '<div class="row scheme">' + (over.length""")
    # ---- the line over the tiles; tooltips do not outlive the coins they were about; a sign while a long count is made
    rep("$('withThese').textContent = 'With the coins chosen above (' + S.coins.join(', ') + '), for the amounts from 0 to ' + (L - 1) + ':';", "$('withThese').textContent = 'With the coins now in use (' + S.coins.join(', ') + '), for the amounts from 0 to ' + (L - 1) + ':';")
    rep("  function redraw() { compute(); fit(); drawTiles(); drawA(); drawWays(); drawB(); }", "  function redraw() { compute(); fit(); drawTiles(); drawA(); drawWays(); drawB(); S.hoverA = -1; S.hoverB = -1; $('tipA').style.display = 'none'; $('tipB').style.display = 'none'; }")
    rep("""    setCoinage(c.coins, l.L, true); matchPreset();
  }""", """    if (c.coins.length * l.L <= 2000) { setCoinage(c.coins, l.L, true); matchPreset(); return; }
    notice('Counting\\u2026'); setTimeout(function () { setCoinage(c.coins, l.L, true); matchPreset(); }, 30);      /* many coins and many amounts take a second or three: say so first */
  }""")
    rep("""    drawBest();
    $('preset').value = '0';""", """    drawBest(); $('plainMax').textContent = BEST.plainMax; $('bothMax').textContent = BEST.bothMax;
    $('preset').value = '0';""")
    open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('page.src.html, sixth stage:', len(s))
