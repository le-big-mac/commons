"""remake5.py -- the fifth stage of the gasket page's remake for a phone: what the plain reader's third visit found (reader27/visit-3.md),
and one slip of my own (the strip's arrow keys still reckoned with a width of 960).  It changes page.src.html in place, from
out27/page.src.stage4.html.txt to out27/page.src.stage5.html.txt.        python -I out27/remake5.py
  1. The second picture's tap answers for the ROW tapped, in a line under the picture that covers nothing, and the answer goes when the
     gasket is changed.  A mouse that only points still gets the box.  The line's labels are written out (10,000; 100 million), as many as fit.
  2. The line under the gasket says what is seen: "To go further in, tap a smaller circle round it" while circles round it can
     be seen; "It fills the whole picture now" when they cannot; "The circle you chose, marked 36, is out of the picture now".
     It has room for three lines on a phone, so the buttons under it keep their place.
  3. The menu's names are short enough to be read with the menu closed; the button that swaps the two gaskets stands directly under the
     line for a chosen circle, with its sentence, above the buttons that magnify.
  4. One word for one thing: "number" for curvature in the third panel and under the picture, "ruled out" for barred, the families in
     words.  The sentence under the picture is two: what is drawn now, and what is true of the gasket."""
import os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = os.path.join(HERE, 'page.src.html')
def rep(s, a, b, n=1):
    assert s.count(a) == n, (s.count(a), a[:90]); return s.replace(a, b)
def main():
    s = open(P, encoding='utf-8').read()
    assert s == open(os.path.join(HERE, 'out27', 'page.src.stage4.html.txt'), encoding='utf-8').read(), 'page.src.html is not stage 4'
    # ---------------------------------------------------------------- styles and the page's own words
    s = rep(s, "#gpick { margin: 8px 0 10px; min-height: 40px; }", "#gpick { margin: 8px 0 10px; min-height: 40px; } #cpick { min-height: 2.8em; } #gfig .legend { margin: 2px 0 12px; }\n  @media (max-width: 760px) { #gpick { min-height: 4.2em; } h1 { font-size: min(26px, 5.5vw); } }      /* room for three lines, so that the buttons under the line keep their place when it grows */")
    s = rep(s, "Each circle is marked with a whole number: the smaller the circle, the bigger its number. Squares are lit in orange.", "The smaller a circle, the bigger its number. Squares are lit in orange.")
    swap = '      <div class="controls" id="gswap"><button id="swap" data-to="0">Show a gasket with no square in it</button></div>\n      <p class="say" id="gstory"></p>\n'
    s = rep(s, swap, '')
    s = rep(s, '      <p class="say" id="gpick" aria-live="polite"></p>\n', '      <p class="say" id="gpick" aria-live="polite"></p>\n' + swap)
    s = rep(s, '      <p class="say" id="gsay" aria-live="polite"></p>\n', '      <p class="say" id="gsay" aria-live="polite"></p>\n      <p class="say" id="gkind"></p>\n')
    s = rep(s, "The rest (<b>blue</b>) come to an end: after the last of them, every number that passes the test and is in no such family is there, as far as I looked. Each mark is one missing number. The line runs from 1 to a hundred million, and each step along it is ten times the one before.",
               "The rest (<b>blue</b>) come to an end: past the last blue mark, the only numbers missing are the orange ones, as far as I looked. Each mark is one missing number; where they crowd they run together into a band. The line runs from 1 to a hundred million, and each faint upright line stands at ten times the one before it.")
    s = rep(s, 'aria-label="Missing curvatures on a logarithmic scale"', 'aria-label="The missing numbers of a gasket, marked along a line from 1 to a hundred million. The left and right arrow keys go through those in no family."')
    s = rep(s, '      <div class="tip" id="ctip"></div>\n', '      <div class="tip" id="ctip"></div>\n      <p class="say" id="cpick" aria-live="polite"></p>\n')
    s = rep(s, "<label>Four curvatures <input", "<label>Four numbers <input")
    s = rep(s, "Below, such a family is called barred.", "Here such a family is said to be ruled out.")
    # ---------------------------------------------------------------- names
    s = rep(s, "var NOTE = { '-3,5,8,8': 'never a square, nor 6 × a square', '-4,5,20,21': 'never 2 × a square, nor 3 × a square', '-1,2,2,3': 'the bug-eye: nothing barred', '0,0,1,1': 'the strip: nothing barred', '-3,4,12,13': 'never 2 × a square, nor 6 × a square', '-2,3,6,7': 'never 2 × a square', '-23,48,49,52': 'the paper’s first figure: by its caption, no n⁴, 4n⁴, 9n⁴, 36n⁴' };",
               "var NOTE = { '-3,5,8,8': 'no squares or 6× squares', '-4,5,20,21': 'no 2× or 3× squares', '-1,2,2,3': 'nothing ruled out', '0,0,1,1': 'a strip, nothing ruled out', '-3,4,12,13': 'no 2× or 6× squares', '-2,3,6,7': 'no 2× squares', '-23,48,49,52': 'the paper’s figure' };      /* short enough to be read with the menu closed on a phone; what each means is said in full under the picture */")
    s = rep(s, "function famName(u) { return u === 1 ? 'n²' : u + 'n²'; }", "function famWords(u) { return u === 1 ? 'a square' : (u === 2 ? 'twice' : u === 3 ? 'three times' : u === 6 ? 'six times' : u + ' times') + ' a square'; }      /* in a sentence */\n  function famRow(u) { return u === 1 ? 'squares' : u + '× squares'; }      /* in a label */")
    # ---------------------------------------------------------------- the menus
    s = rep(s, "h += '<option value=\"' + i + '\">' + qname(q) + ' — ' + NOTE[q.join(',')] + '</option>'; }); if (custom) h += '<option value=\"c\">' + qname(custom) + ' — from the third panel</option>'; $('pack').innerHTML = h; }",
               "h += '<option value=\"' + i + '\">' + qname(q) + ': ' + NOTE[q.join(',')] + '</option>'; }); if (custom) h += '<option value=\"c\">' + qname(custom) + ': from the third panel</option>'; $('pack').innerHTML = h; fitMenu($('pack')); }\n"
               "  // A closed menu shows its chosen name on one line and cuts what does not fit.  Where a menu is narrower than its longest name, its type is made smaller until the name fits (not below 11 px).\n"
               "  function fitMenu(sel) { var c = document.createElement('canvas').getContext('2d'), cs, px, room, widest = 0, i; sel.style.fontSize = ''; cs = getComputedStyle(sel); px = parseFloat(cs.fontSize); c.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + px + 'px ' + cs.fontFamily;\n"
               "    for (i = 0; i < sel.options.length; i++) widest = Math.max(widest, c.measureText(sel.options[i].textContent).width);\n"
               "    room = sel.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - 18;                 /* 18 px for the arrow at the menu's right-hand end, measured in a picture of the closed menu */\n"
               "    if (widest > room) sel.style.fontSize = Math.max(11, Math.floor(px * room / widest * 10) / 10) + 'px'; }\n"
               "  function fitMenus() { ['pack', 'hi', 'cpack', 'upto'].forEach(function (id) { fitMenu($(id)); }); }")
    s = rep(s, "window.addEventListener('resize', function () { if (fit()) draw(); });", "window.addEventListener('resize', function () { fitMenus(); if (fit()) draw(); });")
    s = rep(s, "qname(d.root) + (d.nick ? ' — ' + d.nick : '') + '</option>'; }).join(''); $('cpack').value = '2';", "qname(d.root) + (d.nick ? ': ' + d.nick : '') + '</option>'; }).join(''); $('cpack').value = '2';")
    s = rep(s, "$('pack').value = '1'; setPack(PRESETS[1]); chart(); look();", "$('pack').value = '1'; fitMenus(); setPack(PRESETS[1]); chart(); look();")
    # ---------------------------------------------------------------- the gasket: the line for a chosen circle
    s = rep(s, "    var insideOf = 0; for (i = 0; i < drawn.length && !insideOf; i++) { c = drawn[i]; if (c[0] > 0 && (1 - Math.sqrt(c[3] * c[3] + c[4] * c[4])) * view.s / c[0] >= Math.ceil(Math.sqrt(W * W + H * H) / 2)) insideOf = c[0]; }                 /* the whole view (half a diagonal, 589 px in the picture of 1000 by 620) lies inside this circle */\n",
               "    var insideOf = 0; for (i = 0; i < drawn.length && !insideOf; i++) if (insideIt(i)) insideOf = drawn[i][0];\n")
    s = rep(s, "(insideOf ? ' The whole view lies inside the circle of curvature ' + group(insideOf) + '.' : '') + ' Its numbers all leave ' + t.res.join(', ')",
               "(insideOf ? ' The whole picture is inside the circle marked ' + group(insideOf) + '.' : '');\n    var kind = 'The numbers of this gasket all leave ' + t.res.join(', ')")
    s = rep(s, "'; it is proved (Haag, Kertzer, Rickards and Stange, 2023) that it has no number of the form ' + fams.map(famName).join(' or ') : '; the theorem of 2023 names no family of squares barred from it') + (t.quartic ? ' (for this kind there may be a family of fourth powers as well: see the third panel)' : '') + '.';",
               "'; it is proved (Haag, Kertzer, Rickards and Stange, 2023) that none of them is ' + fams.map(famWords).join(' or ') : '; the theorem of 2023 rules out no family of squares in it') + (t.quartic ? ' (for this kind there may be a family of fourth powers as well: see the third panel)' : '') + '.' + (pack.root.join(',') === '-23,48,49,52' ? ' This is the gasket of the paper\\u2019s first figure, whose caption says that the old guess fails in it for every remainder; by the paper\\u2019s table that means no number in it is n⁴, 4n⁴, 9n⁴ or 36n⁴.' : '');\n    if ($('gkind').innerHTML !== kind) $('gkind').innerHTML = kind;                 /* what is true of the gasket, apart from what is drawn of it now */")
    s = rep(s, "    if (i < 0) return sel ? 'The circle marked <b>' + group(sel[0]) + '</b> is out of the picture now. \\u201cThe whole gasket\\u201d shows everything again.' :",
               "    if (i < 0) return sel ? 'The circle you chose, marked <b>' + group(sel[0]) + '</b>, is out of the picture now. \\u201cThe whole gasket\\u201d shows everything again.' :")
    s = rep(s, "    return 'The circle marked <b>' + group(b) + '</b>: ' + (facts.length ? facts.join('; ') : 'not a square, nor 2, 3 or 6 times one') + '. ' + (small(i) ? '\\u201cMagnify\\u201d closes in on it.' : 'It fills the picture: choose one of the small circles round it to go further.'); }",
               "    return 'The circle marked <b>' + group(b) + '</b>: ' + (facts.length ? facts.join('; ') : 'not a square, nor 2, 3 or 6 times one') + '. ' +\n      (insideIt(i) ? 'It fills the whole picture now: \\u201cDraw back\\u201d shows what is round it.' : small(i) ? '\\u201cMagnify\\u201d closes in on it.' : 'To go further in, ' + (NARROW ? 'tap' : 'click') + ' a smaller circle round it.'); }\n"
               "  function insideIt(i) { var c = drawn[i]; return c[0] > 0 && (1 - Math.sqrt(c[3] * c[3] + c[4] * c[4])) * view.s / c[0] >= Math.ceil(Math.sqrt(W * W + H * H) / 2); }      /* the whole view (half a diagonal, 589 px in the picture of 1000 by 620) lies inside this circle */")
    # the two sentences that go with the swap button begin "Here": the first is then two lines on a phone 360 wide, and whole on its first screen
    s = rep(s, "h = 'In this gasket squares turn up: the two largest orange circles are marked 36, which is 6 \\u00d7 6.';", "h = 'Here squares turn up: the two largest orange circles are marked 36 (6 \\u00d7 6).';")
    s = rep(s, "h = 'In this gasket nothing is lit, and nothing will be, however far you magnify:", "h = 'Here nothing is lit, and nothing will be, however far you magnify:")
    # ---------------------------------------------------------------- the strip
    s = rep(s, "  var cur = null, marks = [];\n", "  var cur = null, marks = [], cpicked = null;\n  var DECADE = ['1', '10', '100', '1,000', '10,000', '100,000', '1 million', '10 million', '100 million'], meas = document.createElement('canvas').getContext('2d'); meas.font = '12px system-ui, -apple-system, \"Segoe UI\", sans-serif';      /* the strip's lettering, to measure a label before it is placed */\n")
    s = rep(s, "rows.push({ name: famName(u), col: 'var(--fam)', list: list, u: u }); });", "rows.push({ name: famRow(u), col: 'var(--fam)', list: list, u: u }); });")
    s = rep(s, "END = TOP + (rows.length - 1) * ROW + 32 + (CNARROW ? 6 : 14), xl;", "END = TOP + (rows.length - 1) * ROW + 32 + (CNARROW ? 6 : 14), xl, placed = []; cur.top = TOP; cur.row = ROW;")
    s = rep(s, """    for (e = 0; e <= 8; e++) { svg += '<line x1="' + X(Math.pow(10, e)) + '" y1="' + (CNARROW ? 30 : 20) + '" x2="' + X(Math.pow(10, e)) + '" y2="' + END + '" stroke="#2c2c2a"/>';
      if (!CNARROW || e % 2 === 0) svg += '<text x="' + X(Math.pow(10, e)) + '" y="' + (END + 18) + '" text-anchor="' + (CNARROW && e === 0 ? 'start' : CNARROW && e === 8 ? 'end' : 'middle') + '">' + (e < 4 ? group(Math.pow(10, e)) : '10' + '<tspan dy="-5" font-size="9">' + e + '</tspan>') + '</text>'; }
""", """    for (e = 0; e <= 8; e++) svg += '<line x1="' + X(Math.pow(10, e)) + '" y1="' + (CNARROW ? 30 : 20) + '" x2="' + X(Math.pow(10, e)) + '" y2="' + END + '" stroke="#2c2c2a"/>';
    // the labels under the line, written out: the two ends first, then the middle, then the rest, each only if it stands 10 px clear of those already placed
    (CNARROW ? [0, 8, 4, 2, 6] : [0, 8, 4, 2, 6, 1, 3, 5, 7]).forEach(function (e) { var w = meas.measureText(DECADE[e]).width, x = X(Math.pow(10, e)), a = e === 0 ? x : e === 8 ? x - w : x - w / 2;
      if (a < 0 || a + w > CW || placed.some(function (q) { return a < q[1] + 10 && a + w > q[0] - 10; })) return; placed.push([a, a + w]);
      svg += '<text class="dec" x="' + x + '" y="' + (END + 18) + '" text-anchor="' + (e === 0 ? 'start' : e === 8 ? 'end' : 'middle') + '">' + DECADE[e] + '</text>'; });
""")
    s = rep(s, """    svg += '<line id="cx" x1="0" y1="' + (CNARROW ? 30 : 20) + '" x2="0" y2="' + END + '" stroke="#f0efec" visibility="hidden"/>';""",
               """    svg += '<line id="cx" x1="0" y1="0" x2="0" y2="0" stroke="#f0efec" visibility="hidden"/><line id="cxp" x1="0" y1="0" x2="0" y2="0" stroke="#f0efec" stroke-width="2" visibility="hidden"/>';      /* the mark pointed at, and the mark chosen */""")
    s = rep(s, "that are in the famil' + (d.families.length > 1 ? 'ies ' : 'y ') + d.families.map(famName).join(' and ') + ', none of which is ever there' : '; the paper finds no family barred from this gasket') + '.';\n",
               "that are ' + d.families.map(famRow).join(' or ') + ', none of which is ever there' : '; the paper rules out no family in this gasket') + '.';\n    cpicked = null; $('ctip').style.display = 'none'; $('cpick').textContent = (CNARROW ? 'Tap' : 'Click') + ' a mark, and this line says which number it is.';      /* an answer about the gasket that was here goes with it */\n")
    s = rep(s, "'In a family: every ' + d.families.map(famName).join(' and every ') + ' that leaves one of the remainders ' + G.type(d.root).res.join(', ') + ' on division by 24. '",
               "'In a family: every number that is ' + d.families.map(famWords).join(' or ') + ' and leaves ' + G.type(d.root).res.join(', ').replace(/, (\\d+)$/, ' or $1') + ' on division by 24. '")
    old_cmove = s[s.index("  function cmove(px) {"):s.index("  $('cpack').addEventListener('change', function () { kpos = 0; chart(); });")]
    assert old_cmove.count('\n') == 8, old_cmove.count('\n')
    new_cmove = r"""  // A pointer or a finger on the strip: the row it is in (the nearest row, by height), and in that row the mark nearest to it across, if one is
  // within 12 px.  crowd is how many marks of the row are within those 12 px: where the marks run into a band, a finger cannot choose one of them.
  function near(px, py) { var r = $('chart').getBoundingClientRect(), f = CW / r.width, x = (px - r.left) * f, y = (py - r.top) * f, k = Math.max(0, Math.min(cur.rows.length - 1, Math.round((y - cur.top - 16) / cur.row))), best = null, bd = 1e9, n = 0, i, m;
    for (i = 0; i < marks.length; i++) { m = marks[i]; if (m[1] !== k) continue; if (Math.abs(m[0] - x) <= 12) n++; if (Math.abs(m[0] - x) < bd) { bd = Math.abs(m[0] - x); best = m; } }
    return { row: k, mark: bd <= 12 ? best : null, crowd: n }; }
  function lineAt(id, m) { var l = document.getElementById(id), y; if (!l) return; if (!m) { l.setAttribute('visibility', 'hidden'); return; } y = cur.top + m[1] * cur.row; l.setAttribute('x1', m[0]); l.setAttribute('x2', m[0]); l.setAttribute('y1', y - 5); l.setAttribute('y2', y + 37); l.setAttribute('visibility', 'visible'); }
  function sqWords(v, u) { var n = Math.round(Math.sqrt(v / u)); return (u === 1 ? '' : u + ' × ') + group(n) + ' × ' + group(n); }
  // a mouse that only points: the box beside the pointer, as before, but for the row pointed at
  function cmove(px, py) { var h = near(px, py), m = h.mark, t = $('ctip'), r, fr, xx, row; lineAt('cx', m); if (!m) { t.style.display = 'none'; return null; } row = cur.rows[m[1]];
    t.innerHTML = '<b>' + group(m[2]) + '</b><br><span>' + (row.u ? 'never a number here: ' + sqWords(m[2], row.u) : 'missing, in no family') + '</span><br><span>remainder ' + (m[2] % 24) + ' on division by 24</span>'; t.style.display = 'block';
    r = $('chart').getBoundingClientRect(); fr = $('cfig').getBoundingClientRect(); xx = r.left - fr.left + m[0] * r.width / CW + 10; if (xx + 280 > fr.width) xx -= 300; t.style.left = Math.max(4, xx) + 'px'; t.style.top = (r.top - fr.top + 6) + 'px'; return m; }
  // a tap, a click or a key: the answer goes in the line under the picture, where it covers nothing, and stays until another is asked for
  function cpick(m, crowd, row) { cpicked = m; lineAt('cxp', m);
    if (!m) { $('cpick').innerHTML = 'Nothing is marked there in the row “' + esc(cur.rows[row].name) + '”.'; return; } var r = cur.rows[m[1]];
    $('cpick').innerHTML = '<b>' + group(m[2]) + '</b> ' + (r.u ? '= ' + sqWords(m[2], r.u) + ', so it is never the number of a circle in this gasket' : 'is missing, and is in no family') + '. It leaves ' + (m[2] % 24) + ' on division by 24.' + (crowd > 1 ? ' It is the nearest of the ' + group(crowd) + ' marks crowded there.' : ''); }
  $('chart').addEventListener('pointermove', function (e) { if (e.pointerType === 'touch') return; cmove(e.clientX, e.clientY); });        /* a finger has no hovering */
  $('chart').addEventListener('pointerdown', function (e) { var h = near(e.clientX, e.clientY); cpick(h.mark, h.crowd, h.row); });
  window.addEventListener('resize', function () { if (cfit()) chart(); }); $('chart').addEventListener('pointerleave', function () { $('ctip').style.display = 'none'; lineAt('cx', null); });
  var kpos = 0; $('chart').addEventListener('keydown', function (e) { if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return; e.preventDefault(); var list = cur.rows[0].list; kpos = Math.max(0, Math.min(list.length - 1, kpos + (e.key === 'ArrowRight' ? 1 : -1) * (e.shiftKey ? 20 : 1))); cpick(marks[kpos], 1, 0); });        /* the marks of the first row come first in the list of marks, in order */
"""
    s = s.replace(old_cmove, new_cmove)
    # ---------------------------------------------------------------- any gasket: one word for one thing
    s = rep(s, ", so they are not the curvatures of four circles that all touch.", ", so they are not the numbers of four circles that all touch.")
    s = rep(s, "'<b>' + qname(rootq) + '</b> is the root of its gasket (its four largest circles). '", "'<b>' + qname(rootq) + '</b> are the four largest circles of their gasket. '")
    s = rep(s, "h += t.quad === null ? 'The page could not work out which families are barred from it. ' : fam.length ? 'By the paper’s theorem no curvature in it is of the form <b>' + fam.map(famName).join('</b> or <b>') + '</b>. ' : 'The paper’s theorem names no family of squares barred from it. ';",
               "h += t.quad === null ? 'The page could not work out which families are ruled out in it. ' : fam.length ? 'By the paper’s theorem no number in it is <b>' + fam.map(famWords).join('</b> or <b>') + '</b>. ' : 'The paper’s theorem rules out no family of squares in it. ';")
    s = rep(s, "which decides whether a family of fourth powers is barred; the page", "which decides whether a family of fourth powers is ruled out; the page")
    s = rep(s, "'the curvature ' + group((may.concat(no))[0]) + ' is of the form n⁴, 4n⁴, 9n⁴ or 36n⁴, so no such family is barred here. ' : 'no curvature up to '", "'the number ' + group((may.concat(no))[0]) + ' is of the form n⁴, 4n⁴, 9n⁴ or 36n⁴, so no such family is ruled out here. ' : 'no number up to '")
    s = rep(s, "'the curvature ' + group(may[0]) + ' is of the form n⁴ or 4n⁴, so the barred family is 9n⁴ and 36n⁴. ' : no.length ? 'the curvature ' + group(no[0]) + ' is of the form 9n⁴ or 36n⁴, so the barred family is n⁴ and 4n⁴. '",
               "'the number ' + group(may[0]) + ' is of the form n⁴ or 4n⁴, so the family ruled out is 9n⁴ and 36n⁴. ' : no.length ? 'the number ' + group(no[0]) + ' is of the form 9n⁴ or 36n⁴, so the family ruled out is n⁴ and 4n⁴. '")
    s = rep(s, "' circles with curvature up to ' + group(N) + ': <b>' + group(miss.length) + '</b> numbers that pass the test of remainders are missing' + (fam.length ? ', ' + group(miss.length - spor.length) + ' of them in the barred famil' + (fam.length > 1 ? 'ies' : 'y') + ' (marked with an orange square) and '",
               "' circles with a number up to ' + group(N) + ': <b>' + group(miss.length) + '</b> numbers that pass the test are missing' + (fam.length ? ', ' + group(miss.length - spor.length) + ' of them in the famil' + (fam.length > 1 ? 'ies' : 'y') + ' ruled out (marked with an orange square) and '")
    s = rep(s, "strip: function () { return { W: CW, left: CL, right: CR, narrow: CNARROW }; }", "strip: function () { return { W: CW, left: CL, right: CR, narrow: CNARROW, top: cur.top, row: cur.row, rows: cur.rows.map(function (r) { return r.name; }), picked: cpicked }; }")
    assert 'famName' not in s and 'barred' not in s, (s.count('famName'), s.count('barred'))
    open(P, 'w', encoding='utf-8').write(s); open(os.path.join(HERE, 'out27', 'page.src.stage5.html.txt'), 'w', encoding='utf-8').write(s)
    print('page.src.html: stage 5,', len(s), 'characters')
if __name__ == '__main__':
    main()
