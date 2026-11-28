"""The gasket page remade for a visitor with a phone, first stage: the picture under a thumb.
27 November 2026, after a plain reader's visit to the page as built (reader27/visit-1.md): on a phone the picture was 336 by 208 px with
lettering of 3 to 6 px that did not grow; a pinch did nothing; a thumb that meant to scroll the page threw the gasket out of its frame;
a tap on a circle did nothing; magnifying aimed at the middle of the view, which is empty.
It is made from the page as it stood (out27/page.src.stage0.html.txt) so that it can be run again.   python -I out27/remake.py
What it changes:
  - on a screen too narrow for the picture at 1000 by 620 the canvas is drawn at the screen's own width, square (less on a short screen),
    and at the screen's own sharpness; where there is room it is the picture of 1000 by 620 as before, pixel for pixel;
  - the lengths that were written for 1000 by 620 (295, 150, 589) are worked out from the picture's size;
  - a tap or click on a circle chooses it: a ring round it, and a sentence under the picture; the two buttons then magnify about it,
    if it is small enough to have room to grow (about the middle of a large circle there is only its inside);
  - two fingers magnify; one finger moves the picture when it sets off sideways, and scrolls the page when it sets off up or down
    (touch-action: pan-y), and a touch the browser takes back puts the picture where it was;
  - "Magnified 0.125 times" is "Drawn back 8 times"; with nothing in view the sentence says how to get the gasket back;
  - the two "Table" buttons say whether they show or hide."""
H = '/home/agent2/gasket/'
if __name__ == '__main__':
    s = open(H + 'out27/page.src.stage0.html.txt', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:110], s.count(a)); s = s.replace(a, b)
    # ---- style
    rep("canvas#g { display: block; width: 1000px; max-width: 100%; height: auto; border-radius: 4px; touch-action: none; cursor: crosshair; }",
        "canvas#g { display: block; width: 1000px; max-width: 100%; height: auto; border-radius: 4px; touch-action: pan-y; cursor: crosshair; }")
    # ---- the picture's size
    rep("var cv = $('g'), g = cv.getContext('2d'), W = 1000, H = 620, pack = null, view = null, drawn = [], hover = -1, custom = null, lastRes = null, leftOutMost = 0;",
        """var cv = $('g'), g = cv.getContext('2d'), W = 1000, H = 620, DPR = 1, NARROW = false, pack = null, view = null, drawn = [], hover = -1, sel = null, custom = null, lastRes = null, leftOutMost = 0;
  // The picture's size.  Where the page has room it is 1000 by 620, as it always was.  On a narrower screen it is drawn at the screen's own
  // width, square (less on a short screen), and at the screen's own sharpness, so that a number in a circle is as large as its circle allows.
  function R0() { return Math.min(W, H) / 2 - 15; }                 /* the outer circle's radius in pixels when the whole gasket is shown: 295 in the picture of 1000 by 620 */
  function base() { return pack.place.strip ? R0() * 150 / 295 : R0() * Math.abs(pack.root[0]); }      /* pixels to a unit of length at "the whole gasket" */
  function fit() {
    var box = cv.parentNode, cs = getComputedStyle(box), avail = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight), narrow = avail < 700;
    var w = narrow ? Math.max(240, Math.round(avail)) : 1000, h = narrow ? Math.round(Math.min(w, Math.max(240, window.innerHeight * 0.62))) : 620, dpr = narrow ? Math.min(3, window.devicePixelRatio || 1) : 1;
    if (w === W && h === H && dpr === DPR && narrow === NARROW && cv.width === Math.round(W * DPR)) return false;
    var old = R0(); W = w; H = h; DPR = dpr; NARROW = narrow; cv.width = Math.round(W * DPR); cv.height = Math.round(H * DPR); cv.style.width = narrow ? W + 'px' : ''; cv.style.height = narrow ? H + 'px' : '';
    if (view) view.s *= R0() / old;
    return true;
  }""")
    rep("function home() { var c = pack.place.circles[0]; if (pack.place.strip) view = { cx: 1, cy: 0, s: 150 }; else view = { cx: c[1] / c[0], cy: c[2] / c[0], s: 295 * Math.abs(c[0]) }; draw(); }",
        "function home() { var c = pack.place.circles[0]; fit(); sel = null; if (pack.place.strip) view = { cx: 1, cy: 0, s: R0() * 150 / 295 }; else view = { cx: c[1] / c[0], cy: c[2] / c[0], s: R0() * Math.abs(c[0]) }; draw(); }")
    rep("    g.fillStyle = '#1a1a19'; g.fillRect(0, 0, W, H); g.lineWidth = 1; g.textAlign = 'center'; g.textBaseline = 'middle';",
        "    g.setTransform(DPR, 0, 0, DPR, 0, 0); g.fillStyle = '#1a1a19'; g.fillRect(0, 0, W, H); g.lineWidth = 1; g.textAlign = 'center'; g.textBaseline = 'middle';")
    # ---- the chosen circle: a ring, and a sentence
    rep("    var t = pack.type, fams = t.quad || [], words = hiWords();\n",
        """    var si = selIndex(); if (si >= 0 && view.s / Math.abs(drawn[si][0]) <= 3e6) { c = drawn[si]; b = c[0]; g.strokeStyle = '#f0efec'; g.lineWidth = 2.5; g.beginPath(); g.arc(W / 2 + c[3] / b * view.s, H / 2 - c[4] / b * view.s, Math.max(3, view.s / Math.abs(b)), 0, 6.2832); g.stroke(); g.lineWidth = 1; }
    $('gpick').innerHTML = pickWords(si);
    var t = pack.type, fams = t.quad || [], words = hiWords();
""")
    rep("$('hiName').textContent = words; var mag = view.s / (pack.place.strip ? 150 : 295 * Math.abs(pack.root[0]));", "$('hiName').textContent = words; var mag = view.s / base();")
    rep("* view.s / c[0] >= 589) insideOf = c[0]; }                 /* the whole view (half a diagonal is 589 px) lies inside this circle */",
        "* view.s / c[0] >= Math.ceil(Math.sqrt(W * W + H * H) / 2)) insideOf = c[0]; }                 /* the whole view (half a diagonal, 589 px in the picture of 1000 by 620) lies inside this circle */")
    rep("+ '. Magnified ' + (mag >= 100 ? group(Math.round(mag)) : +mag.toPrecision(3)) + ' times.' + (insideOf ?",
        "+ '. ' + (mag >= 0.9995 ? 'Magnified ' + (mag >= 100 ? group(Math.round(mag)) : +mag.toPrecision(3)) + ' times.' : 'Drawn back ' + (+(1 / mag).toPrecision(3)) + ' times.') + (ncirc === 0 ? ' Nothing of the gasket is in view: \\u201cThe whole gasket\\u201d brings it back.' : '') + (insideOf ?")
    rep("  function zoomAt(f, px, py) { var wx = view.cx + (px - W / 2) / view.s, wy = view.cy - (py - H / 2) / view.s, s = view.s * f, lim = (pack.place.strip ? 150 : 295 * Math.abs(pack.root[0]));",
        """  // the circle that was chosen by a tap or a click: kept by what it is, not by its place in the list, which changes with every drawing
  function selIndex() { var i, c; if (!sel) return -1; for (i = 0; i < drawn.length; i++) { c = drawn[i]; if (c[0] === sel[0] && c[1] === sel[1] && c[2] === sel[2] && (c[5] || 0) === sel[3]) return i; } return -1; }
  function pickWords(i) { var b, h, facts = [];
    if (i < 0) return sel ? 'The circle marked <b>' + group(sel[0]) + '</b> is out of the picture now. \\u201cThe whole gasket\\u201d shows everything again.' : (NARROW ? 'Tap' : 'Click') + ' a circle, and this line says what its number is.';
    b = drawn[i][0]; [1, 2, 3, 6].forEach(function (u) { var n; if (b % u === 0 && G.isSquare(b / u)) { n = Math.round(Math.sqrt(b / u)); facts.push(group(b) + ' = ' + (u === 1 ? '' : u + ' \\u00d7 ') + group(n) + ' \\u00d7 ' + group(n) + (u === 1 ? ', a square' : u === 2 ? ', twice a square' : u === 3 ? ', three times a square' : ', six times a square')); } });
    h = 'The circle marked <b>' + group(b) + '</b>. ' + (facts.length ? facts.join('; ') + '. ' : 'Not a square, nor 2, 3 or 6 times one. ') + 'Divided by 24 it leaves ' + (b % 24) + '. ' + (small(i) ? '\\u201cMagnify\\u201d now closes in on this circle.' : 'Choose a small circle, and \\u201cMagnify\\u201d closes in on it.');
    return h; }
  function small(i) { return view.s / Math.abs(drawn[i][0]) < 0.3 * Math.min(W, H) / 2; }             /* a circle that still has room to grow in the picture; magnifying about the middle of a large one shows only its inside */
  function target() { var i = selIndex(), c, x, y; if (i < 0 || !small(i)) return [W / 2, H / 2]; c = drawn[i]; x = W / 2 + c[3] / c[0] * view.s; y = H / 2 - c[4] / c[0] * view.s; return x >= 0 && x <= W && y >= 0 && y <= H ? [x, y] : [W / 2, H / 2]; }
  function zoomAt(f, px, py) { var wx = view.cx + (px - W / 2) / view.s, wy = view.cy - (py - H / 2) / view.s, s = view.s * f, lim = base();""")
    # ---- the pointer: one finger or the mouse moves and chooses; two fingers magnify
    rep("""  var drag = null;
  cv.addEventListener('pointerdown', function (e) { var p = at(e); drag = { x: p[0], y: p[1], cx: view.cx, cy: view.cy, moved: false }; cv.setPointerCapture(e.pointerId); });
  cv.addEventListener('pointermove', function (e) { var p = at(e), t = $('gtip'), r, cr; if (drag) {""",
        """  var drag = null, pts = {}, pinch = null;
  function fingers() { return Object.keys(pts); }
  cv.addEventListener('pointerdown', function (e) { var p = at(e), f; pts[e.pointerId] = p; f = fingers();
    if (f.length === 2) { if (drag && drag.moved) { view.cx = drag.cx; view.cy = drag.cy; } drag = null; pinch = { d: Math.max(1, Math.hypot(pts[f[0]][0] - pts[f[1]][0], pts[f[0]][1] - pts[f[1]][1])) }; return; }
    if (f.length > 2) return;
    drag = { x: p[0], y: p[1], cx: view.cx, cy: view.cy, moved: false, id: e.pointerId }; try { cv.setPointerCapture(e.pointerId); } catch (x) {} });
  cv.addEventListener('pointermove', function (e) { var p = at(e), t = $('gtip'), r, cr, f, d;
    if (pts[e.pointerId]) pts[e.pointerId] = p;
    if (pinch) { f = fingers(); if (f.length === 2) { d = Math.max(1, Math.hypot(pts[f[0]][0] - pts[f[1]][0], pts[f[0]][1] - pts[f[1]][1])); if (Math.abs(d - pinch.d) > 1) { zoomAt(d / pinch.d, (pts[f[0]][0] + pts[f[1]][0]) / 2, (pts[f[0]][1] + pts[f[1]][1]) / 2); pinch.d = d; } } return; }
    if (drag) {""")
    rep("""    var i = pick(p[0], p[1]); if (i !== hover) { hover = i; draw(); } if (i < 0) { t.style.display = 'none'; return; } t.innerHTML = tipFor(i);""",
        """    if (e.pointerType === 'touch') return;                       /* a finger has no hovering: what it taps is said under the picture */
    var i = pick(p[0], p[1]); if (i !== hover) { hover = i; draw(); } if (i < 0) { t.style.display = 'none'; return; } t.innerHTML = tipFor(i);""")
    rep("""  cv.addEventListener('pointerup', function () { drag = null; }); cv.addEventListener('pointerleave', function () { if (!drag) { hover = -1; $('gtip').style.display = 'none'; draw(); } });""",
        """  cv.addEventListener('pointerup', function (e) { var p = at(e), i, c; delete pts[e.pointerId]; if (fingers().length < 2) pinch = null;
    if (drag && drag.id === e.pointerId && !drag.moved) { i = pick(p[0], p[1]); if (i >= 0) { c = drawn[i]; sel = [c[0], c[1], c[2], c[5] || 0]; } else sel = null; drag = null; draw(); return; }      /* a tap or a click: the circle under it is chosen */
    if (drag && drag.id === e.pointerId) drag = null; });
  cv.addEventListener('pointercancel', function (e) { delete pts[e.pointerId]; if (fingers().length < 2) pinch = null;                                      /* the browser took the touch for its own, to scroll the page: the picture goes back where it was */
    if (drag && drag.id === e.pointerId) { if (drag.moved) { view.cx = drag.cx; view.cy = drag.cy; draw(); } drag = null; } });
  cv.addEventListener('pointerleave', function () { if (!drag) { hover = -1; $('gtip').style.display = 'none'; draw(); } });""")
    rep("$('zin').addEventListener('click', function () { zoomAt(2, W / 2, H / 2); }); $('zout').addEventListener('click', function () { zoomAt(0.5, W / 2, H / 2); }); $('home').addEventListener('click', home);",
        "$('zin').addEventListener('click', function () { var p = target(); zoomAt(2, p[0], p[1]); }); $('zout').addEventListener('click', function () { var p = target(); zoomAt(0.5, p[0], p[1]); }); $('home').addEventListener('click', home);\n  window.addEventListener('resize', function () { if (fit()) draw(); });")
    # ---- the sentence for the chosen circle, under the picture; the table buttons
    rep("""      <p class="say" id="gsay" aria-live="polite"></p>""", """      <p class="say" id="gpick" aria-live="polite"></p>
      <p class="say" id="gsay" aria-live="polite"></p>""")
    rep("""<button id="gtab" aria-pressed="false">Table</button>""", """<button id="gtab" aria-pressed="false">Show the table</button>""")
    rep("""<button id="ctab" aria-pressed="false">Table</button>""", """<button id="ctab" aria-pressed="false">Show the table</button>""")
    rep("$('gtab').addEventListener('click', function () { var on = $('gtable').classList.toggle('on'); this.setAttribute('aria-pressed', on); if (on) gtable(); });",
        "$('gtab').addEventListener('click', function () { var on = $('gtable').classList.toggle('on'); this.setAttribute('aria-pressed', on); this.textContent = on ? 'Hide the table' : 'Show the table'; if (on) gtable(); });")
    rep("$('ctab').addEventListener('click', function () { var on = $('ctable').classList.toggle('on'); this.setAttribute('aria-pressed', on); if (on) ctable(); });",
        "$('ctab').addEventListener('click', function () { var on = $('ctable').classList.toggle('on'); this.setAttribute('aria-pressed', on); this.textContent = on ? 'Hide the list' : 'Show the list'; if (on) ctable(); });")
    rep("""<button id="ctab" aria-pressed="false">Show the table</button>""", """<button id="ctab" aria-pressed="false">Show the list</button>""")
    # the handle the tests use: the picture's size and the chosen circle as well
    rep("window.GasketPage = { view: function () { return view; },", "window.GasketPage = { view: function () { return view; }, size: function () { return { W: W, H: H, dpr: DPR, narrow: NARROW }; }, chosen: function () { return sel; },")
    # the rule of 27 November's earlier mend (a menu no wider than the page) is in the page as it stood; it is put back here
    rep("  select, button { cursor: pointer; } button:hover, select:hover { background: #32322f; }\n", "  select, button { cursor: pointer; } button:hover, select:hover { background: #32322f; }\n") 
    open(H + 'out27/stage1.html', 'w', encoding='utf8').write(s); open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('gasket page: the picture under a thumb (stage 1)')
