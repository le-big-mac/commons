"""Seventh stage of the coin page's remake, after the referee's check of the mending (referee27/mending.md) and the reader's
fifth visit (reader/visit-5.md).   python -I remake7.py   (run after remake6.py)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'page.src.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:100], s.count(a)); s = s.replace(a, b)
    # ---- words
    rep("""<figcaption>For each number of coins in a set, every set was tried, and these have the lowest average: with coins up to <span id="plainMax"></span> for paying exactly; with coins up to <span id="bothMax"></span> for paying with change, and there for sets of up to five coins only.""",
        """<figcaption>For each number of coins in a set, every set was tried, and these have the lowest average. Paying exactly, coins up to <span id="plainMax"></span> were tried. Paying with change, coins up to <span id="bothMax"></span>, and only sets of up to five coins.""")
    rep("""so coins up to one more than twice the largest amount are tried, and no larger ones.)</figcaption>""", """so coins up to one more than twice the largest amount are tried; where the coins in use are large beside the amounts, a larger coin still could do better.)</figcaption>""")
    rep("""The best sets for paying exactly are in that paper, where he says that others had posted such tables in 2000, and in the On-Line Encyclopedia of Integer Sequences (A366013); the best four coins were found by Thomas Young and his students in 1995. The floor's counting is Shallit's for paying exactly, and is carried over by me to paying with change. The best sets for paying with change I did not find in print; the write-up lists the works on the subject that I have not read, and if one of them has these sets, they are its.""",
        """The best sets for paying exactly are in that paper, and in the On-Line Encyclopedia of Integer Sequences (A366013). Shallit says there that others had posted such tables in 2000; and by Thomas Young's own account in the Encyclopedia (A364607), he and three students explored the best four coins in 1995. The floor's counting is Shallit's for paying exactly, and is carried over by me to paying with change. The best sets for paying with change I did not find in print; the list of sources beside the write-up names the works on the subject that I have not read, and if one of them has these sets, the credit is theirs.""")
    rep("""</svg> the best coin</li>""", """</svg> <span id="bestLegend">the best coin</span></li>""")
    # ---- the second picture's legend, for the coins in use
    rep("""    $('nowLegend').textContent = isFinite(tp) && isFinite(tb) ? 'the average now (the upper one is for paying exactly)' : isFinite(tb) ? 'the average now, paying with change (these coins cannot pay every amount exactly)' : 'no average now: these coins cannot pay every amount';""",
        """    $('nowLegend').textContent = isFinite(tp) && isFinite(tb) ? (tp === tb ? 'the average now (the same for paying exactly and with change)' : 'the average now (the upper one is for paying exactly)') : isFinite(tb) ? 'the average now, paying with change (these coins cannot pay every amount exactly)' : 'no average now: these coins cannot pay every amount';
    $('bestLegend').textContent = 'the best coin' + (!isFinite(tp) && bp.length ? ' (the ring that stands alone is the 1, without which not every amount can be paid exactly)' : '');""")
    # ---- the buttons: shorter, and true when several coins tie
    rep("""$('addPlain').textContent = full ? 'No coin can be added: ' + MAXCOINS + ' is as many as this page takes' : bp.length ? 'Add a ' + bp[0].coin + ': the best coin for paying exactly' : 'No coin to add for paying exactly';""",
        """$('addPlain').textContent = full ? 'No coin can be added: ' + MAXCOINS + ' is as many as this page takes' : bp.length ? 'Add a ' + bp[0].coin + (bp.length > 1 ? ': one of the ' + bp.length + ' best coins' : ': the best coin') + ' for paying exactly' : 'No coin to add for paying exactly';""")
    rep("""$('addBoth').textContent = bb.length ? 'Add a ' + bb[0].coin + ': the best coin up to ' + n + ' for paying with change' : 'No coin up to ' + n + ' to add for paying with change';""",
        """$('addBoth').textContent = bb.length ? 'Add a ' + bb[0].coin + (bb.length > 1 ? ': one of the ' + bb.length + ' best coins tried' : ': the best coin tried') + ' for paying with change' : 'No coin tried helps in paying with change';""")
    # ---- a count that may be long: the page says "Counting..." and lets a frame be drawn before it begins; one count at a time
    rep("""    if (c.coins.length * l.L <= 2000) { setCoinage(c.coins, l.L, true); matchPreset(); return; }
    notice('Counting\\u2026'); setTimeout(function () { setCoinage(c.coins, l.L, true); matchPreset(); }, 30);      /* many coins and many amounts take a second or three: say so first */
  }""", """    notice(''); later(function () { setCoinage(c.coins, l.L, true); matchPreset(); }, $('apply'));
  }
  /* A count can take a second or three (large coins, many amounts).  The button that was pressed says "Counting..." first (on the
     button, so that nothing on the page changes its place), the page waits until the browser has drawn that (the second of two
     animation frames, or a third of a second, whichever comes first), and only then counts; until it has finished, the boxes and
     buttons that would start another count are shut, so that no second count is pending and nothing typed meanwhile is written
     over (the referee: the sign was missing for the slowest cases, and a count could be started twice). */
  var BUSY = ['coins', 'L', 'apply', 'preset', 'addPlain', 'addBoth'];
  function later(work, btn) {
    if (S.pending) return;
    S.pending = true; var was = BUSY.map(function (id) { var d = $(id).disabled; $(id).disabled = true; return d; }), label = btn.textContent, done = false;
    btn.style.minWidth = Math.ceil(btn.getBoundingClientRect().width) + 'px'; btn.textContent = 'Counting\\u2026';
    function go() { if (done) return; done = true; BUSY.forEach(function (id, k) { $(id).disabled = was[k]; }); btn.textContent = label; btn.style.minWidth = ''; S.pending = false; S.counts = (S.counts || 0) + 1; work(); }
    if (window.requestAnimationFrame) requestAnimationFrame(function () { requestAnimationFrame(go); });
    setTimeout(go, 300);
  }""")
    rep("""    steady(btn, function () { setCoinage(S.coins.concat([coin]).sort(function (x, y) { return x - y; }), L); matchPreset(); });
    $('addedSay').innerHTML =""", """    later(function () {
    steady(btn, function () { setCoinage(S.coins.concat([coin]).sort(function (x, y) { return x - y; }), L); matchPreset(); });
    $('addedSay').innerHTML =""")
    i = s.index("    $('addedSay').innerHTML = 'Added a <b>'"); j = s.index("\n", i)
    s = s[:j] + "\n    }, btn);" + s[j:]
    # the two tooltips are hidden each by its own line (so that a test can tell which was forgotten)
    rep(" S.hoverA = -1; S.hoverB = -1; $('tipA').style.display = 'none'; $('tipB').style.display = 'none'; }", " S.hoverA = -1; $('tipA').style.display = 'none'; S.hoverB = -1; $('tipB').style.display = 'none'; }")
    open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('page.src.html, seventh stage:', len(s))
