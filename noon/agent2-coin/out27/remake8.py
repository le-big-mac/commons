"""Eighth stage of the coin page's remake, after the referee's last look (referee27/last.md) and the reader's sixth visit
(reader/visit-6.md).   python -I remake8.py   (run after remake7.py)"""
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'page.src.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:100], s.count(a)); s = s.replace(a, b)
    # ---- words
    rep("""<figcaption>For each number of coins in a set, every set was tried, and these have the lowest average. Paying exactly, coins up to <span id="plainMax"></span> were tried. Paying with change, coins up to <span id="bothMax"></span>, and only sets of up to five coins.""",
        """<figcaption>These sets have the lowest average of all that were tried. Paying exactly, every set of one to seven coins up to <span id="plainMax"></span> was tried. Paying with change, every set of one to five coins up to <span id="bothMax"></span>.""")
    rep("""are tried; where the coins in use are large beside the amounts, a larger coin still could do better.)</figcaption>""", """are tried; where the coins in use are large beside the amounts, a still larger coin could do better.)</figcaption>""")
    rep("""The floor's counting is Shallit's for paying exactly, and is carried over by me to paying with change.""", """The counting behind the floor is Shallit's for paying exactly, and is carried over by me to paying with change.""")
    # ---- the buttons that add a coin, when several coins tie: "equal best with ..." (a visitor read "one of the 3 best coins" as one of the top three)
    rep("""  function names(list) {""", """  function others(list) { var c = list.slice(1).map(function (e) { return e.coin; }); return c.length === 0 ? '' : c.length <= 2 ? ' with ' + c.join(' and ') : ' with ' + c.length + ' others'; }
  function names(list) {""")
    rep("""bp.length ? 'Add a ' + bp[0].coin + (bp.length > 1 ? ': one of the ' + bp.length + ' best coins' : ': the best coin') + ' for paying exactly'""",
        """bp.length ? 'Add a ' + bp[0].coin + (bp.length > 1 ? ': equal best' + others(bp) : ': the best coin') + ' for paying exactly'""")
    rep("""bb.length ? 'Add a ' + bb[0].coin + (bb.length > 1 ? ': one of the ' + bb.length + ' best coins tried' : ': the best coin tried') + ' for paying with change'""",
        """bb.length ? 'Add a ' + bb[0].coin + (bb.length > 1 ? ': equal best' + others(bb) + ', of the coins tried,' : ': the best coin tried') + ' for paying with change'""")
    # ---- a count that is pending: nothing else may start one, and the buttons stay shut a third of a second after it lands
    rep("""    S.pending = true; var was = BUSY.map(function (id) { var d = $(id).disabled; $(id).disabled = true; return d; }), label = btn.textContent, done = false;
    btn.style.minWidth = Math.ceil(btn.getBoundingClientRect().width) + 'px'; btn.textContent = 'Counting\\u2026';
    function go() { if (done) return; done = true; BUSY.forEach(function (id, k) { $(id).disabled = was[k]; }); btn.textContent = label; btn.style.minWidth = ''; S.pending = false; S.counts = (S.counts || 0) + 1; work(); }""",
        """    S.pending = true; var was = shut(), label = btn.textContent, done = false;
    btn.style.minWidth = Math.ceil(btn.getBoundingClientRect().width) + 'px'; btn.textContent = 'Counting\\u2026';
    function go() {
      if (done) return; done = true; open(was); btn.textContent = label; btn.style.minWidth = ''; S.counts = (S.counts || 0) + 1; work();
      var left = shut();              /* as the count has left them; a tap made while the page was counting is delivered now, and must find them shut (the referee: a second tap counted twice, and added a coin whose name the visitor had not seen) */
      setTimeout(function () { open(left); S.pending = false; }, 350);
    }""")
    rep("""  var BUSY = ['coins', 'L', 'apply', 'preset', 'addPlain', 'addBoth'];""", """  var BUSY = ['coins', 'L', 'apply', 'preset', 'addPlain', 'addBoth'];
  /* the two boxes are made read-only, not disabled, so that the one being typed in keeps its caret (and a phone its keyboard) */
  function shut() { return BUSY.map(function (id) { var e = $(id), box = id === 'coins' || id === 'L', d = box ? e.readOnly : e.disabled; if (box) e.readOnly = true; else e.disabled = true; return d; }); }
  function open(was) { BUSY.forEach(function (id, k) { var e = $(id); if (id === 'coins' || id === 'L') e.readOnly = was[k]; else e.disabled = was[k]; }); }""")
    rep("""      var t = e.target; if (t && t.getAttribute && t.getAttribute('data-set')) { setCoinage(t.getAttribute('data-set').split(',').map(Number), BEST.L); matchPreset(); $('fig0').scrollIntoView({ block: 'start' }); }""",
        """      var t = e.target; if (S.pending) return;                                             /* not while a count is pending (the referee: a best set pressed then was lost, or left a sentence about other coins) */
      if (t && t.getAttribute && t.getAttribute('data-set')) { setCoinage(t.getAttribute('data-set').split(',').map(Number), BEST.L); matchPreset(); $('fig0').scrollIntoView({ block: 'start' }); }""")
    rep("""      var t = e.target; if (t && t.getAttribute && t.getAttribute('data-set')) steady($('story'), function () {""", """      var t = e.target; if (S.pending) return;
      if (t && t.getAttribute && t.getAttribute('data-set')) steady($('story'), function () {""")
    open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('page.src.html, eighth stage:', len(s))
