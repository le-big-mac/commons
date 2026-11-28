"""Third stage of the gasket page's remake: the second picture on a phone, and words.   python -I out27/remake3.py   (run after remake2.py)
After the plain reader's first visit (reader27/visit-1.md): the strip of missing numbers was 336 by 67 px with lettering of about 4 px
("Can I read it? No."), and a tap on it did nothing; "The scale is logarithmic" and "give out" stopped the reader; "the paper" and
"barred" were used before they were introduced.
What it changes:
  - on a narrow screen the strip is drawn at the screen's own width: each row's name above it, lettering of 12 px, every second step of
    the scale named; where there is room it is drawn 960 wide as before;
  - a tap on the strip answers as a pointer moving over it does, and the answer stays when the finger lifts;
  - the caption says what a mark is and how the line runs, without the word logarithmic; "give out" is "come to an end";
  - "What is going on" names the four mathematicians and says what "barred" will mean."""
H = '/home/agent2/gasket/'
if __name__ == '__main__':
    s = open(H + 'page.src.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:110], s.count(a)); s = s.replace(a, b)
    rep("  function X(v) { return 60 + 880 * Math.log10(v) / 8; }",
        """  var CW = 960, CL = 60, CR = 20, CNARROW = false;                 /* the strip's width and its margins: 960, 60 and 20 where there is room; on a narrow screen the screen's own width, 6 and 14 */
  function X(v) { return CL + (CW - CL - CR) * Math.log10(v) / 8; }
  function cfit() { var box = $('chart').parentNode, cs = getComputedStyle(box), avail = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight), narrow = avail < 700, w = narrow ? Math.max(240, Math.round(avail)) : 960;
    if (w === CW && narrow === CNARROW) return false; CW = w; CNARROW = narrow; CL = narrow ? 6 : 60; CR = narrow ? 14 : 20; return true; }""")
    rep("""    cur = { d: d, rows: rows }; marks = [];
    for (e = 0; e <= 8; e++) { svg += '<line x1="' + X(Math.pow(10, e)) + '" y1="20" x2="' + X(Math.pow(10, e)) + '" y2="' + (30 + rows.length * 44) + '" stroke="#2c2c2a"/><text x="' + X(Math.pow(10, e)) + '" y="' + (48 + rows.length * 44) + '" text-anchor="middle">' + (e < 4 ? group(Math.pow(10, e)) : '10' + '<tspan dy="-5" font-size="9">' + e + '</tspan>') + '</text>'; }
    rows.forEach(function (r, k) { y = 28 + k * 44; svg += '<text x="54" y="' + (y + 20) + '" text-anchor="end" fill="#f0efec">' + esc(r.name) + '</text>';""",
        """    cur = { d: d, rows: rows }; marks = []; cfit();
    var ROW = CNARROW ? 60 : 44, TOP = CNARROW ? 46 : 28, END = TOP + (rows.length - 1) * ROW + 32 + (CNARROW ? 6 : 14), xl;        /* a row's marks are 32 high; on a narrow screen its name stands above it */
    for (e = 0; e <= 8; e++) { svg += '<line x1="' + X(Math.pow(10, e)) + '" y1="' + (CNARROW ? 30 : 20) + '" x2="' + X(Math.pow(10, e)) + '" y2="' + END + '" stroke="#2c2c2a"/>';
      if (!CNARROW || e % 2 === 0) svg += '<text x="' + X(Math.pow(10, e)) + '" y="' + (END + 18) + '" text-anchor="' + (CNARROW && e === 0 ? 'start' : CNARROW && e === 8 ? 'end' : 'middle') + '">' + (e < 4 ? group(Math.pow(10, e)) : '10' + '<tspan dy="-5" font-size="9">' + e + '</tspan>') + '</text>'; }
    rows.forEach(function (r, k) { y = TOP + k * ROW; svg += CNARROW ? '<text x="' + CL + '" y="' + (y - 6) + '" fill="#f0efec">' + esc(r.name) + '</text>' : '<text x="54" y="' + (y + 20) + '" text-anchor="end" fill="#f0efec">' + esc(r.name) + '</text>';""")
    rep("""    var last = d.sporadic[d.sporadic.length - 1]; svg += '<line x1="' + X(last) + '" y1="16" x2="' + X(last) + '" y2="62" stroke="#f0efec" stroke-dasharray="2 2"/><text x="' + (X(last) + 5) + '" y="14">the last, ' + group(last) + '</text>';
    svg += '<line id="cx" x1="0" y1="20" x2="0" y2="' + (30 + rows.length * 44) + '" stroke="#f0efec" visibility="hidden"/>';
    $('chart').setAttribute('viewBox', '0 0 960 ' + (60 + rows.length * 44)); $('chart').innerHTML = svg;""",
        """    var last = d.sporadic[d.sporadic.length - 1]; xl = X(last);
    svg += '<line x1="' + xl + '" y1="' + (CNARROW ? 18 : 16) + '" x2="' + xl + '" y2="' + (TOP + 34) + '" stroke="#f0efec" stroke-dasharray="2 2"/><text x="' + (CNARROW && xl > CW * 0.5 ? xl - 5 : xl + 5) + '" y="14"' + (CNARROW && xl > CW * 0.5 ? ' text-anchor="end"' : '') + '>the last, ' + group(last) + '</text>';
    svg += '<line id="cx" x1="0" y1="' + (CNARROW ? 30 : 20) + '" x2="0" y2="' + END + '" stroke="#f0efec" visibility="hidden"/>';
    $('chart').setAttribute('viewBox', '0 0 ' + CW + ' ' + (END + 30)); $('chart').innerHTML = svg;""")
    rep("x = (px - r.left) * 960 / r.width,", "x = (px - r.left) * CW / r.width,")
    rep("best[0] * r.width / 960 + 10;", "best[0] * r.width / CW + 10;")
    rep("  $('chart').addEventListener('pointermove', function (e) { cmove(e.clientX); });", "  $('chart').addEventListener('pointermove', function (e) { cmove(e.clientX); }); $('chart').addEventListener('pointerdown', function (e) { cmove(e.clientX); });        /* a tap answers as a moving pointer does */\n  window.addEventListener('resize', function () { if (cfit()) chart(); });")
    rep("addEventListener('pointerleave', function () { $('ctip').style.display = 'none'; var l = document.getElementById('cx'); if (l) l.setAttribute('visibility', 'hidden'); })",
        "addEventListener('pointerleave', function (e) { if (e.pointerType === 'touch') return;        /* a finger that lifts leaves its answer standing */ $('ctip').style.display = 'none'; var l = document.getElementById('cx'); if (l) l.setAttribute('visibility', 'hidden'); })")
    rep("  .legend b { color: var(--text-primary); font-weight: 500; }", "  .legend b { color: var(--text-primary); font-weight: 500; } .legend li { flex-wrap: wrap; } @media (max-width: 480px) { .legend li { display: block; } .legend i { margin-right: 6px; vertical-align: -1px; } }")
    # ---- words
    rep("""<figcaption>For six gaskets I ran through every circle with curvature up to a hundred million and listed the whole numbers that pass the test of remainders and are not there. They are of two kinds. Some belong to a family the 2023 paper proves can never appear (<b>orange</b>). The rest (<b>blue</b>) give out: after the last of them, every number that passes the test is there, as far as I looked. The scale is logarithmic.</figcaption>""",
        """<figcaption>For six gaskets I went through every circle with a number up to a hundred million, and listed the numbers that pass the test and are not there. They are of two kinds. Some belong to a family that is proved never to appear (<b>orange</b>). The rest (<b>blue</b>) come to an end: after the last of them, every number that passes the test and is in no such family is there, as far as I looked. Each mark is one missing number. The line runs from 1 to a hundred million, and each step along it is ten times the one before.</figcaption>""")
    rep("""In 2023 four mathematicians showed that the guess is false: in many gaskets a whole family of numbers that pass the test never appears.""",
        """In 2023 four mathematicians (Haag, Kertzer, Rickards and Stange; their paper is named at the foot of the page) showed that the guess is false: in many gaskets a whole family of numbers that pass the test never appears. Below, such a family is called barred.""")
    rep("""<figcaption>Four whole-number curvatures of circles that all touch one another (they must satisfy Descartes's equation, (a + b + c + d)² = 2(a² + b² + c² + d²); a negative one is the circle round the rest).</figcaption>""",
        """<figcaption>Type the numbers of four circles that all touch one another. They must satisfy Descartes's equation, (a + b + c + d)² = 2(a² + b² + c² + d²); a number with a minus is the circle round the rest.</figcaption>""")
    rep("""', not one of whose members that passes the test of remainders is a curvature' : '; the paper finds no family barred from this gasket')""",
        """', none of which is ever there' : '; the paper finds no family barred from this gasket')""")
    rep("""'</b>, every circle with curvature up to ' + group(d.N) + ': <b>' + group(d.sporadic.length) + '</b> missing numbers in no family, the last of them '""",
        """'</b>, every circle with a number up to ' + group(d.N) + ': <b>' + group(d.sporadic.length) + '</b> numbers are missing that are in no family, the last of them '""")
    rep("""'; and <b>' + group(d.inFamilies) + '</b> in the famil' + (d.families.length > 1 ? 'ies ' : 'y ')""", """'; and <b>' + group(d.inFamilies) + '</b> that are in the famil' + (d.families.length > 1 ? 'ies ' : 'y ')""")
    rep("window.GasketPage = { view: function () { return view; },", "window.GasketPage = { view: function () { return view; }, strip: function () { return { W: CW, left: CL, right: CR, narrow: CNARROW }; },")
    open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('gasket page: the second picture on a phone, and words (stage 3)')
