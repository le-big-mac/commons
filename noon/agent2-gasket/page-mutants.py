"""page-mutants.py -- can the page test fail?  Copies of the page with one thing broken in its own script, styles or words (not in
gcore.js), each built and run through tools/shot-gasket.js in a headless browser, four at a time, the true page alone first and again
among them.      python -I page-mutants.py [JOBS [name,name,...]] > page-mutants.out      (the test is run from ~/web, where playwright is)
The list was rewritten on 27 November 2026 for the page as remade for a visitor with a phone; the list of eight that went
before is out27/page-mutants.stage0.py.txt, and its eight faults are the first eight here, pointed at the page as it now is."""
import os, subprocess, sys, re, time
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'mutants-page'); WEB = os.path.expanduser('~/web')
rd = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()
M = [
 # ---- the eight of the list before the remake
 ('big-circle-label-unguarded', "the number of a very large circle is placed without asking whether there is a place (the error a referee found in the first page)", "if (b > 0 && at2 && at2[0] > 30", "if (b > 0 && at2[0] > 30"),
 ('pointer-upside-down', "the pointer's height is read upside down", "wy = -(py - H / 2) / view.s, best", "wy = (py - H / 2) / view.s, best"),
 ('fives-wrong', "\"multiples of 5\" lights numbers one more than a multiple of 5", "return function (b) { return b % 5 === 0; };", "return function (b) { return b % 5 === 1; };"),
 ('strip-centre-forgets-period', "a circle's centre in the strip is given without the periods it was moved along", "function trueX(c) { return BigInt(c[1]) + 2n * BigInt(c[5] || 0) * BigInt(c[0]); }", "function trueX(c) { return BigInt(c[1]); }"),
 ('squares-as-doubles', "\"squares\" lights twice a square", "var u = +h; return function (b)", "var u = +h * 2; return function (b)"),
 ('left-out-unsaid', "the page does not say when circles are left out for want of exact numbers", "(res.leftOut ? ' (some circles may be missing here", "(false ? ' (some circles may be missing here"),
 ('inside-of-wrong', 'the page says the view is inside a circle when it is not, and not when it is', '>= Math.ceil(Math.sqrt(W * W + H * H) / 2); }', '< Math.ceil(Math.sqrt(W * W + H * H) / 2); }'),
 ('chart-drops-a-family', "the chart leaves out the last family", "d.families.forEach(function (u) { var list = [];", "d.families.slice(0, -1).forEach(function (u) { var list = [];"),
 # ---- the picture's size
 ('picture-never-fitted', "the picture is 1000 by 620 on every screen, as it was, and a phone shrinks it", "narrow = avail < 700;", "narrow = false;"),
 ('picture-not-sharp', "on a phone the picture is drawn at one dot to the pixel, whatever the screen", "dpr = narrow ? Math.min(3, window.devicePixelRatio || 1) : 1;", "dpr = 1;"),
 ('picture-taller-than-a-short-screen', 'on a short screen the picture is as tall as it is wide', 'Math.round(Math.min(w, Math.max(200, window.innerHeight * 0.62)))', 'Math.round(Math.min(w, Math.max(200, window.innerHeight * 2)))'),
 ('picture-drawn-in-a-corner', "the drawing forgets the screen's sharpness, so on a phone the gasket fills a corner of its frame", "g.setTransform(DPR, 0, 0, DPR, 0, 0);", "g.setTransform(1, 0, 0, 1, 0, 0);"),
 ('turned-phone-keeps-old-scale', "when the picture changes size the gasket keeps its old scale", "if (view) view.s *= R0() / old;", ""),
 ('turned-phone-not-redrawn', 'the picture does not answer when the screen changes size', "window.addEventListener('resize', function () { fitMenus(); if (fit()) draw(); });", "window.addEventListener('resize', function () { fitMenus(); });"),
 ('whole-gasket-too-big', "\"the whole gasket\" draws the outer circle wider than the picture", "function R0() { return Math.min(W, H) / 2 - 15; }", "function R0() { return Math.max(W, H) / 2 - 15; }"),
 # ---- choosing a circle
 ('tap-chooses-nothing', "a tap on a circle does not choose it", "if (i >= 0) sel = ident(drawn[i]); else sel = null; drag = null; draw(); return; }", "drag = null; draw(); return; }"),
 ('tap-off-a-circle-keeps-the-choice', "a tap on the black between circles leaves the last circle chosen", "if (i >= 0) sel = ident(drawn[i]); else sel = null; drag", "if (i >= 0) sel = ident(drawn[i]); drag"),
 ('chosen-forgets-the-period', "a circle chosen in the strip is remembered without the period it stands in", "function ident(c) { return [c[0], c[1], c[2], c[5] || 0]; }", "function ident(c) { return [c[0], c[1], c[2], 0]; }"),
 ('chosen-by-number-alone', "the chosen circle is found again by its number alone, so its twin is ringed as well as it", "if (c[0] === sel[0] && c[1] === sel[1] && c[2] === sel[2] && (c[5] || 0) === sel[3]) return i;", "if (c[0] === sel[0]) return i;"),
 ('no-ring', "the chosen circle is not ringed", "var si = selIndex(); if (si >= 0 && view.s", "var si = selIndex(); if (false && view.s"),
 ('line-never-says-six-times', "the line for a chosen circle never says six times a square", "[1, 2, 3, 6].forEach(function (u) { var n; if", "[1, 2, 3].forEach(function (u) { var n; if"),
 ('line-says-twice-for-three-times', "the line for a chosen circle says twice a square of three times a square", "u === 2 ? ', twice a square' : u === 3 ? ', three times a square'", "u === 2 ? ', twice a square' : u === 3 ? ', twice a square'"),
 ('line-always-says-magnify', 'the line says Magnify closes in on a circle that has no more room', "small(i) ? '\\u201cMagnify\\u201d closes in on it.'", "true ? '\\u201cMagnify\\u201d closes in on it.'"),
 ('line-silent-when-out-of-picture', 'the line does not say when the chosen circle has left the picture', "return sel ? 'The circle you chose, marked <b>'", "return false ? 'The circle you chose, marked <b>'"),
 ('line-says-click-on-a-phone', "the line says Click on a phone", "(NARROW ? 'Tap' : 'Click')", "'Click'"),
 ('whole-gasket-keeps-the-choice', "\"The whole gasket\" leaves the last circle chosen", "fit(); sel = null; if (pack.place.strip)", "fit(); if (pack.place.strip)"),
 # ---- magnify and move
 ('large-counts-as-small', "a circle that fills the picture counts as one with room to grow", "< 0.3 * Math.min(W, H) / 2; }", "< 30 * Math.min(W, H) / 2; }"),
 ('magnify-does-not-centre', "Magnify does not bring the chosen circle to the middle", "{ c = drawn[i]; view.cx += c[3] / c[0]; view.cy += c[4] / c[0]; }", "{ }"),
 ('magnify-centres-upside-down', "Magnify takes the chosen circle's height upside down", "view.cx += c[3] / c[0]; view.cy += c[4] / c[0]; }", "view.cx += c[3] / c[0]; view.cy -= c[4] / c[0]; }"),
 ('magnify-chooses-nothing', "with nothing chosen, Magnify chooses nothing and doubles about the middle", "if (i < 0 && !sel) { i = autoPick(); if (i >= 0) sel = ident(drawn[i]); }", ""),
 ('magnify-chooses-again-after-losing', "when the chosen circle has left the picture Magnify chooses another", "if (i < 0 && !sel) { i = autoPick();", "if (i < 0) { i = autoPick();"),
 ('magnify-ignores-the-light', "with nothing chosen, Magnify takes the largest circle, lit or not", "return bestLit >= 0 ? bestLit : best; }", "return best; }"),
 ('magnify-chooses-off-the-picture', "with nothing chosen, Magnify may take a circle whose middle is outside the picture", "if (x < 0 || x > W || y < 0 || y > H) continue;", ""),
 ('magnify-chooses-the-smallest-lit', "with nothing chosen, Magnify takes the smallest lit circle", "(bestLit < 0 || b < drawn[bestLit][0])) bestLit = i;", "(bestLit < 0 || b > drawn[bestLit][0])) bestLit = i;"),
 ('magnify-by-three', "Magnify trebles", "zoomAt(2, W / 2, H / 2); }\n  function move", "zoomAt(3, W / 2, H / 2); }\n  function move"),
 ('draw-back-magnifies', "Draw back doubles", "$('zout').addEventListener('click', function () { zoomAt(0.5, W / 2, H / 2); });", "$('zout').addEventListener('click', function () { zoomAt(2, W / 2, H / 2); });"),
 ('draw-back-without-end', "the picture can be drawn back eighty times", "if (s < lim / 8) s = lim / 8;", "if (s < lim / 80) s = lim / 80;"),
 ('up-arrow-goes-down', "the up arrow looks further down", "$('mup').addEventListener('click', function () { move(0, 1); });", "$('mup').addEventListener('click', function () { move(0, -1); });"),
 ('left-arrow-goes-right', "the left arrow looks further right", "$('mleft').addEventListener('click', function () { move(-1, 0); });", "$('mleft').addEventListener('click', function () { move(1, 0); });"),
 ('arrows-step-small', "an arrow moves the picture a thirtieth of its size", "var d = Math.min(W, H) / 3 / view.s;", "var d = Math.min(W, H) / 30 / view.s;"),
 ('whole-gasket-does-nothing', "\"The whole gasket\" does nothing", "$('home').addEventListener('click', home);", ""),
 # ---- fingers
 ('finger-cannot-scroll-the-page', "a finger on the picture cannot scroll the page", "touch-action: pan-y;", "touch-action: none;"),
 ('pinch-does-nothing', "two fingers do not magnify", "zoomAt(d / pinch.d, (pts[f[0]][0] + pts[f[1]][0]) / 2, (pts[f[0]][1] + pts[f[1]][1]) / 2); pinch.d = d;", "pinch.d = d;"),
 ('pinch-the-wrong-way', "fingers moving apart draw the picture back", "zoomAt(d / pinch.d, (pts", "zoomAt(pinch.d / d, (pts"),
 ('pinch-about-the-corner', "two fingers magnify about the picture's corner, not about the place between them", "(pts[f[0]][0] + pts[f[1]][0]) / 2, (pts[f[0]][1] + pts[f[1]][1]) / 2); pinch.d = d;", "0, 0); pinch.d = d;"),
 ('scroll-leaves-the-picture-moved', "when the browser takes a swipe to scroll the page, the picture stays where the swipe had pushed it", "{ if (drag.moved) { view.cx = drag.cx; view.cy = drag.cy; draw(); } drag = null; } });", "{ drag = null; } });"),
 ('finger-drag-the-wrong-way', "a finger dragged left moves the picture right", "view.cx = drag.cx - (p[0] - drag.x) / view.s;", "view.cx = drag.cx + (p[0] - drag.x) / view.s;"),
 ('finger-shows-the-pointer-box', "a finger on the picture brings up the pointer's box", "if (e.pointerType === 'touch') return;                       /* a finger has no hovering", "/* a finger has no hovering"),
 # ---- the sentence under the picture
 ('drawn-back-unsaid', "a picture drawn back is said to be magnified", "'Drawn back ' + (+(1 / mag).toPrecision(3)) + ' times.'", "'Magnified ' + (+mag.toPrecision(3)) + ' times.'"),
 ('not-magnified-unsaid', "the whole gasket is said to be magnified 1 times", "(Math.abs(mag - 1) < 0.0005 ? 'Not magnified.'", "(false ? 'Not magnified.'"),
 ('magnification-of-the-desk', "on a phone the magnification is reckoned from the picture of 1000 by 620", "function base() { return pack.place.strip ? R0() * 150 / 295 : R0() * Math.abs(pack.root[0]); }", "function base() { return pack.place.strip ? 150 : 295 * Math.abs(pack.root[0]); }"),
 ('nothing-in-view-unsaid', "with no circle in view the page does not say how to come back", "(ncirc === 0 ? ' Nothing of the gasket is in view", "(false ? ' Nothing of the gasket is in view"),
 ('no-family-ever-named', "the sentence under the picture never names a barred family", "var t = pack.type, fams = t.quad || [], words = hiWords();", "var t = pack.type, fams = [], words = hiWords();"),
 ('a-remainder-dropped', 'the sentence about the gasket leaves out the first remainder', "'Every number in this gasket leaves ' + t.res.join(', ')", "'Every number in this gasket leaves ' + t.res.slice(1).join(', ')"),
 ('lit-count-one-over', "the count of lit circles is one too many", "', <b>' + group(lit) + '</b> of them '", "', <b>' + group(lit + 1) + '</b> of them '"),
 # ---- the two gaskets and their button
 ('opens-on-the-gasket-without-squares', "the page opens on (-3, 5, 8, 8), where nothing is lit", "$('pack').value = '1'; fitMenus(); setPack(PRESETS[1]); chart(); look();", "$('pack').value = '0'; fitMenus(); setPack(PRESETS[0]); chart(); look();"),
 ('story-of-no-squares-with-fives-lit', "the sentence that nothing is lit stands under (-3, 5, 8, 8) whatever is lit", "else if (key === '-3,5,8,8' && sq) h =", "else if (key === '-3,5,8,8') h ="),
 ('story-of-squares-with-fives-lit', "the sentence about 36 stands under (-4, 5, 20, 21) whatever is lit", "if (key === '-4,5,20,21' && sq) { h =", "if (key === '-4,5,20,21') { h ="),
 ('swap-does-not-light-squares', "the button that swaps the gaskets leaves the lights as they were", "var to = this.getAttribute('data-to'); $('hi').value = '1'; $('pack').value = to;", "var to = this.getAttribute('data-to'); $('pack').value = to;"),
 ('swap-stays', "the button that should show the gasket without squares shows the one with them", "label = 'Show a gasket with no square in it'; to = '0'; }", "label = 'Show a gasket with no square in it'; to = '1'; }"),
 ('swap-leaves-the-menu', "the button swaps the gasket and the menu still names the other", "$('hi').value = '1'; $('pack').value = to; setPack", "$('hi').value = '1'; setPack"),
 ('menu-note-of-another-gasket', 'the menu says of (-3, 5, 8, 8) what is true of (-4, 5, 20, 21)', "'-3,5,8,8': 'no squares or 6× squares'", "'-3,5,8,8': 'no 2× or 3× squares'"),
 ('story-below-its-button-moved-up', "the sentence that changes length stands above the button that changes it, so the button jumps under the thumb", "<div class=\"controls\" id=\"gswap\"><button id=\"swap\" data-to=\"0\">Show a gasket with no square in it</button></div>\n      <p class=\"say\" id=\"gstory\"></p>", "<p class=\"say\" id=\"gstory\"></p>\n      <div class=\"controls\" id=\"gswap\"><button id=\"swap\" data-to=\"0\">Show a gasket with no square in it</button></div>"),
 # ---- the table
 ('table-button-keeps-its-name', "the table's button says Show when the table is shown", "this.textContent = on ? 'Hide the table' : 'Show the table';", "this.textContent = 'Show the table';"),
 ('table-remainder-by-12', "the table gives what is left on division by 12", "'</td><td>' + (c[0] % 24) + '</td><td class=\"l\">'", "'</td><td>' + (c[0] % 12) + '</td><td class=\"l\">'"),
 ('table-yes-for-no', "the table says yes for no", "(test(c[0]) ? 'yes' : 'no')", "(test(c[0]) ? 'no' : 'yes')"),
 ('table-of-the-smallest', "the table lists the forty smallest circles in view", ".sort(function (a, b) { return a[0] - b[0]; }).slice(0, 40), test = hiTest();", ".sort(function (a, b) { return b[0] - a[0]; }).slice(0, 40), test = hiTest();"),
 # ---- the strip of missing numbers
 ('strip-never-fitted', "the strip is 960 wide on every screen, and a phone shrinks it", "narrow = avail < 700, w = narrow ? Math.max(240, Math.round(avail)) : 960;", "narrow = false, w = 960;"),
 ('strip-every-decade-labelled', 'on a phone every power of ten is tried for a label, so the labels are 1, 10, 100 and not every second step', '(CNARROW ? [0, 8, 4, 2, 6] : [0, 8, 4, 2, 6, 1, 3, 5, 7])', '([0, 8, 4, 2, 6, 1, 3, 5, 7])'),
 ('strip-rows-unnamed-on-a-phone', "on a phone the rows of the strip have no names", "'\" fill=\"#f0efec\">' + esc(r.name) + '</text>' : '<text x=\"54\"", "'\" fill=\"#f0efec\"></text>' : '<text x=\"54\""),
 ('strip-tap-does-nothing', 'a tap on the strip gives no answer', "$('chart').addEventListener('pointerdown', function (e) { var h = near(e.clientX, e.clientY); cpick(h.mark, h.crowd, h.row); });", ''),
 ('strip-box-for-a-moving-finger', 'a finger that moves on the strip brings up the box that covers the marks', "if (e.pointerType === 'touch') return; cmove(e.clientX, e.clientY); });", 'cmove(e.clientX, e.clientY); });'),
 ('strip-last-is-the-last-but-one', "the strip gives the last missing number but one as the last", "var last = d.sporadic[d.sporadic.length - 1]; xl = X(last);", "var last = d.sporadic[d.sporadic.length - 2]; xl = X(last);"),
 ('strip-answers-across-rows', 'the strip answers by how far across the tap is, whatever row it is in (the fault a visitor found)', 'if (m[1] !== k) continue; if (Math.abs(m[0] - x) <= 12) n++;', 'if (Math.abs(m[0] - x) <= 12) n++;'),
 ('strip-not-refitted', "the strip does not answer when the screen changes size", "window.addEventListener('resize', function () { if (cfit()) chart(); });", ""),
 ('strip-list-button-keeps-its-name', "the list's button says Show when the list is shown", "this.textContent = on ? 'Hide the list' : 'Show the list';", "this.textContent = 'Show the list';"),
 ('strip-count-in-families-wrong', "the strip's sentence gives the count in no family for the count in the families", "'; and <b>' + group(d.inFamilies) + '</b> that are '", "'; and <b>' + group(d.sporadic.length) + '</b> that are '"),
 # ---- any gasket
 ('draw-it-draws-the-last-looked-at', "\"Draw it above\" draws the gasket last looked at, whatever has been typed since (the fault a visitor found)", "if (look() !== true || !custom) return; fillPacks();", "if (!custom) return; fillPacks();"),
 ('missing-list-button-never-shown', "the button that opens the list of missing numbers never appears", "$('tlist').hidden = !miss.length;", "$('tlist').hidden = true;"),
 ('missing-list-always-open', "the list of missing numbers stands open under the sentence, six hundred numbers long", "#tnums { display: none; } #tnums.on { display: block; }", "#tnums { display: block; }"),
 ('refusal-keeps-the-old-list', "after a refusal the last gasket's list and its button stay", "$('show').disabled = true; $('tnums').innerHTML = ''; $('tlist').hidden = true;", "$('show').disabled = true;"),
 ('in-no-family-counts-the-family', 'the third panel counts the numbers in the families as those in none', 'spor = miss.filter(function (v) { return !ruled(v); });', 'spor = miss.filter(function (v) { return ruled(v); });'),
 ('common-divisor-let-through', "four numbers with a common divisor are let through", "if (!G.isPrimitive(q)) {", "if (false) {"),
 # ---- words that do not change
 ('about-36-leaves-0', "the page says 36 leaves 0 on division by 24", "36 leaves 12, so it passes that test.", "36 leaves 0, so it passes that test."),
 ('about-families-swapped', "the page gives each of its two gaskets the other's barred families", "In <b>(&minus;3, 5, 8, 8)</b> it is the squares, and the numbers six times a square; in <b>(&minus;4, 5, 20, 21)</b> it is the numbers twice a square and three times a square.", "In <b>(&minus;4, 5, 20, 21)</b> it is the squares, and the numbers six times a square; in <b>(&minus;3, 5, 8, 8)</b> it is the numbers twice a square and three times a square."),
 ('lead-says-bigger-is-bigger', "the first sentence says the bigger a circle, the bigger its number", "The smaller a circle, the bigger its number.", "The bigger a circle, the bigger its number."),
 ('menu-wider-than-a-phone', "a menu is as wide as its longest option, and wider than a phone", "select, input[type=text] { max-width: 100%; box-sizing: border-box; } .controls label { max-width: 100%; min-width: 0; }", ""),
 # ---- the fifth stage: what the reader's third visit found
 ('line-never-says-it-fills', 'the line never says that the chosen circle fills the whole picture', "insideIt(i) ? 'It fills the whole picture now", "false ? 'It fills the whole picture now"),
 ('fills-said-too-early', 'a circle is said to fill the whole picture when it reaches half way to the corners', '>= Math.ceil(Math.sqrt(W * W + H * H) / 2); }', '>= Math.ceil(Math.sqrt(W * W + H * H) / 4); }'),
 ('line-has-room-for-two-lines', 'the line for a chosen circle has room for two lines, so the buttons under it move when it grows (the fault a visitor found)', '#gpick { min-height: 4.2em; }', '#gpick { min-height: 0; }'),
 ('title-as-large-as-at-a-desk', 'the title is as large on a phone as at a desk, and takes two lines', 'h1 { font-size: min(26px, 5.5vw); }', 'h1 { font-size: 26px; }'),
 ('swap-under-the-buttons-again', "the button that swaps the gaskets and its sentence are back under the buttons that magnify and the legend, below a small phone's first screen (the fault a visitor found)", '      <div class="controls" id="gswap"><button id="swap" data-to="0">Show a gasket with no square in it</button></div>\n      <p class="say" id="gstory"></p>\n      <div class="controls" id="gmove"><button id="zin">Magnify ×2</button><button id="zout">Draw back ÷2</button><button id="home">The whole gasket</button><span class="arrows"><button id="mleft" aria-label="Look further left">←</button><button id="mup" aria-label="Look further up">↑</button><button id="mdown" aria-label="Look further down">↓</button><button id="mright" aria-label="Look further right">→</button></span></div>\n      <ul class="legend"><li><i style="background:var(--fam)"></i><b id="hiName">a square</b></li><li><i style="border:1px solid var(--muted);box-sizing:border-box"></i>any other number</li></ul>\n', '      <div class="controls" id="gmove"><button id="zin">Magnify ×2</button><button id="zout">Draw back ÷2</button><button id="home">The whole gasket</button><span class="arrows"><button id="mleft" aria-label="Look further left">←</button><button id="mup" aria-label="Look further up">↑</button><button id="mdown" aria-label="Look further down">↓</button><button id="mright" aria-label="Look further right">→</button></span></div>\n      <ul class="legend"><li><i style="background:var(--fam)"></i><b id="hiName">a square</b></li><li><i style="border:1px solid var(--muted);box-sizing:border-box"></i>any other number</li></ul>\n      <div class="controls" id="gswap"><button id="swap" data-to="0">Show a gasket with no square in it</button></div>\n      <p class="say" id="gstory"></p>\n'),
 ('kind-sentence-run-into-the-count', 'what is true of the gasket is not said under the picture', "if ($('gkind').innerHTML !== kind) $('gkind').innerHTML = kind;", ''),
 ('paper-figure-on-every-gasket', "every gasket is said to be the one of the paper's first figure", "(pack.root.join(',') === '-23,48,49,52' ? ' This is the gasket", "(true ? ' This is the gasket"),
 ('three-times-said-as-twice', 'three times a square is called twice a square in the sentences', "u === 2 ? 'twice' : u === 3 ? 'three times' : u === 6 ? 'six times'", "u === 2 ? 'twice' : u === 3 ? 'twice' : u === 6 ? 'six times'"),
 ('menu-type-not-fitted', 'a menu narrower than its longest name keeps its type, and the name is cut (the fault a visitor found)', 'if (widest > room) sel.style.fontSize', 'if (false) sel.style.fontSize'),
 ('menu-type-too-small', "a menu's type is fitted without a floor, and a fifth smaller than it need be", "Math.max(11, Math.floor(px * room / widest * 10) / 10) + 'px'", "Math.floor(px * room / widest * 8) / 10 + 'px'"),
 ('menu-names-long-again', "the menu's names are long again", "'-4,5,20,21': 'no 2× or 3× squares'", "'-4,5,20,21': 'never 2 × a square, nor 3 × a square'"),
 ('strip-labels-run-together', "the strip's labels are placed without asking whether they are clear of one another", 'if (a < 0 || a + w > CW || placed.some(function (q) { return a < q[1] + 10 && a + w > q[0] - 10; })) return;', 'if (a < 0 || a + w > CW) return;'),
 ('strip-row-ignores-height', 'the strip answers every tap for its first row', 'k = Math.max(0, Math.min(cur.rows.length - 1, Math.round((y - cur.top - 16) / cur.row)))', 'k = 0'),
 ('strip-answer-stays-with-another-gasket', "the strip's answer and its white line stay when another gasket is chosen (the fault a visitor found)", "cpicked = null; $('ctip').style.display = 'none'; $('cpick').textContent = (CNARROW ? 'Tap' : 'Click') + ' a mark, and this line says which number it is.';", "if (!$('cpick').textContent) $('cpick').textContent = (CNARROW ? 'Tap' : 'Click') + ' a mark, and this line says which number it is.';"),
 ('strip-crowd-unsaid', 'the strip does not say when the mark it names is one of many under the finger', "(crowd > 2 ? ' It is one of '", "(false ? ' It is one of '"),
 ('strip-crowd-counts-every-row', 'the count of marks under the finger takes in the other rows', 'if (m[1] !== k) continue; if (Math.abs(m[0] - x) <= 12) n++;', 'if (Math.abs(m[0] - x) <= 12) n++; if (m[1] !== k) continue;'),
 ('strip-white-line-down-every-row', 'the white line at the chosen mark runs down every row', "l.setAttribute('y1', y - 5); l.setAttribute('y2', y + 37);", "l.setAttribute('y1', 0); l.setAttribute('y2', 400);"),
 ('strip-white-line-at-the-finger', 'nothing is drawn at the chosen mark', "function cpick(m, crowd, row) { cpicked = m; lineAt('cxp', m);", 'function cpick(m, crowd, row) { cpicked = m;'),
 ('strip-keys-one-mark-on', "the strip's arrow keys answer for the mark after the one they are on", 'cpick(marks[kpos], 1, 0); });', 'cpick(marks[kpos + 1], 1, 0); });'),
 ('strip-six-times-dropped', 'the strip writes six times a square as a square', "return (u === 1 ? '' : u + ' × (') + group(n) + ' × ' + group(n) + (u === 1 ? '' : ')'); }", "return group(n) + ' × ' + group(n); }"),
 ('strip-nothing-there-unsaid', 'a tap where a row has no mark is answered with the mark nearest, however far', 'return { row: k, mark: bd <= 12 ? best : null, crowd: n }; }', 'return { row: k, mark: best, crowd: n }; }'),
 ('strip-box-ignores-the-row', 'at a desk the box beside the pointer is left up when the pointer is where its row has no mark', "lineAt('cx', m); if (!m) { t.style.display = 'none'; return null; }", "lineAt('cx', m); if (!m) { return null; }"),
 ('third-panel-says-curvature', 'the third panel says curvature where the page says number', "'By the paper’s theorem no number in it is <b>'", "'By the paper’s theorem no curvature in it is <b>'"),
 ('inside-said-as-before', 'the count says the whole view lies inside the circle of curvature 36', "' The whole picture is inside the circle marked ' + group(insideOf) + '.'", "' The whole view lies inside the circle of curvature ' + group(insideOf) + '.'"),
 # ---- the sixth stage: the wordings the reader's fourth visit stopped at
 ('strip-two-marks-called-a-crowd', 'two marks under the finger are called a crowd (the wording a visitor stopped at)', "(crowd > 2 ? ' It is one of '", "(crowd > 1 ? ' It is one of '"),
 ('strip-product-reads-as-a-cube', 'the strip writes six times a square as 6 × 6 × 6, which reads as a cube (the wording a visitor stopped at)', "return (u === 1 ? '' : u + ' × (') + group(n) + ' × ' + group(n) + (u === 1 ? '' : ')'); }", "return (u === 1 ? '' : u + ' × ') + group(n) + ' × ' + group(n); }"),
 ('line-product-reads-as-a-cube', 'the line under the gasket writes three times a square as 3 × 2 × 2', "(u === 1 ? '' : u + ' \\u00d7 (') + group(n) + ' \\u00d7 ' + group(n) + (u === 1 ? '' : ')')", "(u === 1 ? '' : u + ' \\u00d7 ') + group(n) + ' \\u00d7 ' + group(n)"),
 ('fourth-power-note-on-every-gasket', 'every gasket is said to be of a kind where fourth powers may be ruled out', "(t.quartic && pack.root.join(',') !== '-23,48,49,52' ? ' In some gaskets with these remainders", "(true ? ' In some gaskets with these remainders"),
 ('fourth-powers-sorted-wrongly', 'the third panel takes 9 times a fourth power for a fourth power when it looks among the circles', '(u === 1 || u === 4 ? may : no).push(v)', '(u === 1 || u === 9 ? may : no).push(v)'),
 ('fourth-powers-the-other-pair', 'the third panel names the wrong pair of forms as ruled out', "h += may.length ? 'In this gasket 9 times and 36 times a fourth power are ruled out as well.", "h += may.length ? 'In this gasket the fourth powers, and 4 times a fourth power, are ruled out as well."),
 ('fourth-powers-found-means-ruled-out', 'where a fourth power is among the circles the third panel says they are all ruled out', "'In this gasket the fourth powers are not ruled out, nor 4, 9 or 36 times a fourth power. The page finds that by looking: '", "'In this gasket the fourth powers are all ruled out, and 4, 9 and 36 times a fourth power. The page finds that by looking: '"),
 ('proved-in-2023-on-every-gasket', 'a gasket with no family ruled out is said to have one', "fams.length ? 'None of them is ' + fams.map(famWords).join(' or ') + ': that was proved in 2023.'", "true ? 'None of them is ' + (fams.length ? fams : [1]).map(famWords).join(' or ') + ': that was proved in 2023.'"),
 # ---- the seventh stage: what the referee's reading found, and the referee's own broken copies
 ('first-sentence-always-squares', 'the first sentence says squares are lit whatever is lit (the fault the referee found)', "function litLead() { var h = $('hi').value; return h === 'none'", "function litLead() { var h = '1'; return h === 'none'"),
 ('swap-sentence-of-the-picture', 'the sentence under the swap button speaks of the two largest orange circles of the picture, which may be magnified (the fault the referee found)', "h = 'Squares turn up in this gasket: the smallest is 36 (6 \\u00d7 6), on two circles.';", "h = 'Here squares turn up: the two largest orange circles are marked 36 (6 \\u00d7 6).';"),
 ('counts-circles-out-of-the-picture', '"N circles drawn" counts circles of which nothing is in the picture (the fault the referee found)', 'return c[0] !== 0 && seen(c); }).length;', 'return c[0] !== 0; }).length;'),
 ('lit-count-out-of-the-picture', 'the count of lit circles takes in lit circles of which nothing is in the picture', '{ if (seen(c)) lit++; g.fillStyle', '{ lit++; g.fillStyle'),
 ('outer-circle-always-counted', 'the circle round the rest is counted when its edge is out of the picture and the picture is inside it', 'return b > 0 || (dx + W / 2) * (dx + W / 2) + (dy + H / 2) * (dy + H / 2) >= r * r; }', 'return true; }'),
 ('table-lists-circles-out-of-the-picture', 'the table lists circles of which nothing is in the picture', 'return c[0] > 0 && seen(c); })', 'return c[0] > 0; })'),
 ('fourth-power-pair-not-counted', 'the pair of fourth-power forms shown to be ruled out is left out of the count of the families and not marked (the fault the referee found)', 'var q4 = t.quartic && t.k !== 1 ? (may.length ? [9, 36] : no.length ? [1, 4] : []) : [],', 'var q4 = [],'),
 ('fourth-power-pair-the-other', 'the other pair of fourth-power forms is counted and marked', '(may.length ? [9, 36] : no.length ? [1, 4] : [])', '(may.length ? [1, 4] : no.length ? [9, 36] : [])'),
 ('signs-turned-told-not-descartes', 'four numbers with every sign turned are told they do not satisfy the equation (the fault the referee found)', "eq && s4 < 0 ? 'Those four satisfy the equation, but", "false ? 'Those four satisfy the equation, but"),
 ('signs-turned-offered-as-typed', 'four numbers with every sign turned are offered back as they were typed', "q.map(function (x) { return x > 0 ? '−' + x : String(-x); }).join(', ') + '.'", "q.join(', ') + '.'"),
 ('look-does-not-say-looking', 'a look does not say that it is looking', "$('tsay').textContent = 'Looking through the circles\\u2026'; $('show').disabled = true;", "$('show').disabled = true;"),
 ('no-word-without-script', 'a browser that runs no script is told nothing', '  <noscript><p class="sub">This page draws its pictures with a script, and the script is off or has not loaded. Without it there is nothing here to see or to press; what is below is only the words.</p></noscript>\n', ''),
 ('empty-pictures-without-script', 'a browser that runs no script is shown the empty pictures, menus and buttons', '<noscript><style>figure, h2.fig { display: none; }</style></noscript>\n', ''),
 ('keys-up-and-down-exchanged', "the up key looks further down (a broken copy of the referee's that passed)", "else if (k === 'ArrowUp') view.cy += d; else if (k === 'ArrowDown') view.cy -= d;", "else if (k === 'ArrowUp') view.cy -= d; else if (k === 'ArrowDown') view.cy += d;"),
 ('colours-exchanged', "the blue and the orange are exchanged (a broken copy of the referee's that passed)", '--spor: #3987e5; --fam: #d95926;', '--spor: #d95926; --fam: #3987e5;'),
 ('list-of-another-gasket', '"Show the list" opens the list of the first gasket, whichever is shown (a broken copy of the referee\'s that passed)', 'function ctable() { var d = cur.d;', 'function ctable() { var d = DATA[0];'),
 ('equation-with-a-three', "Descartes's equation is printed with 3 for 2 (a broken copy of the referee's that passed)", '(a + b + c + d)² = 2(a² + b² + c² + d²)', '(a + b + c + d)² = 3(a² + b² + c² + d²)'),
 ('a-thousand-times-further', 'the note says the authors looked a thousand times further (a broken copy the referee made and did not run)', 'at least a hundred times further', 'at least a thousand times further'),
 ('come-to-an-end-flatly', 'the caption says flatly that the blue numbers come to an end', 'seem to come to an end', 'come to an end'),
 ('pinch-about-the-middle', "two fingers magnify about the picture's middle, not about the place between them", '(pts[f[0]][0] + pts[f[1]][0]) / 2, (pts[f[0]][1] + pts[f[1]][1]) / 2); pinch.d = d;', 'W / 2, H / 2); pinch.d = d;'),
 ('hover-ring-only', 'a pointer over a circle rings it, a choice does not: the chosen circle is ringed only while the pointer stays on it', 'var si = selIndex(); if (si >= 0 && view.s', 'var si = selIndex(); if (si >= 0 && si === hover && view.s'),
 # ---- the eighth stage: the referee's check of the mending, its two further broken copies, and the reader's fifth visit
 ('outer-circle-counted-from-outside', 'the circle round the rest is counted when the picture lies wholly outside it (the case the referee found left)', 'if (qx * qx + qy * qy > r * r) return false; return b > 0 ||', 'if (b > 0 && qx * qx + qy * qy > r * r) return false; return b > 0 ||'),
 ('one-circle-of-them', 'with one circle in the picture the count says "1 of them a square"', "ncirc === 1 ? ', and it is ' + (lit ? '' : 'not ') + words :", "false ? ', and it is ' + (lit ? '' : 'not ') + words :"),
 ('one-circle-always-is', 'with one circle in the picture, and that not lit, the count says it is a square', "', and it is ' + (lit ? '' : 'not ') + words", "', and it is ' + words"),
 ('squares-not-ruled-out-where-none-can-be', 'where no square can pass the test the page says the theorem does not rule out the squares (the sentence the referee and the reader would not have)', "return can.indexOf(1) >= 0 ? who + ' does not rule out the squares in it, nor '", "return true ? who + ' does not rule out the squares in it, nor '"),
 ('zero-circle-unexplained', 'the third panel does not say what a circle numbered 0 is', " + (rootq.indexOf(0) >= 0 ? 'A circle numbered 0 is a straight line. ' : '');", ';'),
 ('old-list-button-while-looking', "the last look's button for its list stays while a new look is going on", "$('tlist').hidden = true; $('tnums').innerHTML = ''; setTimeout(look, 30); }", 'setTimeout(look, 30); }'),
 ('too-large-at-300', "numbers above 300 are refused as too large (a broken copy of the referee's that passed)", 'var big = q.some(function (x) { return Math.abs(x) > 1e6; })', 'var big = q.some(function (x) { return Math.abs(x) > 300; })'),
 ('draw-above-stays-below', '"Draw it above" draws the gasket and leaves the visitor two screens below it (a broken copy of the referee\'s that passed)', " $('pack').value = 'c'; setPack(custom); $('gfig').scrollIntoView({ behavior: 'smooth' }); });", " $('pack').value = 'c'; setPack(custom); });"),
 ('more-count-wrong', 'the count of missing numbers not listed is wrong by 540 (a broken copy the referee made and did not run)', "' … (' + group(miss.length - 600) + ' more)'", "' … (' + group(miss.length - 60) + ' more)'"),
 ('fourth-power-written-without-its-form', '9 is written as 1 × 1 × 1 × 1', "(u === 1 ? '' : u + ' × (') + r + ' × ' + r + ' × ' + r + ' × ' + r + (u === 1 ? '' : ')'); };", "r + ' × ' + r + ' × ' + r + ' × ' + r; };"),
 # ---- the ninth stage: the reader's sixth visit and the referee's last check
 ('empty-picture-line-silent', 'with the gasket gone from the picture the line under it still asks for a tap (what a visitor found at its sixth visit)', "if (ncirc === 0 && !sel) $('gpick').innerHTML = ", "if (false) $('gpick').innerHTML = "),
 ('nought-of-them', 'with no circle in the picture the count says "0 of them a square"', "($('hi').value === 'none' || ncirc === 0 ? ''", "($('hi').value === 'none' ? ''"),
 ('not-when-not-known', 'where one pair of fourth-power forms is ruled out and the page has not found which, the rest are flatly "not" in a family ruled out (the sentence the referee would not sign)', " + (t.quartic && t.k !== 1 && !q4.length ? ', or not known to be' : '') : '') + '.';", " : '') + '.';"),
 ('enter-does-nothing', "the Enter key in the box of four numbers does nothing (a broken copy of the referee's that passed)", " $('quad').addEventListener('keydown', function (e) { if (e.key === 'Enter') lookSoon(); });", ''),
 ('ten-thousand-looks-a-hundred-thousand', '"Look as far as 10,000" looks as far as 100,000 (a broken copy the referee thought of)', '<option value="10000">10,000</option>', '<option value="100000">10,000</option>'),
]
def stopped(r, first):
    """the test threw before its end: what it had found by then, or the last line of its error"""
    m = re.search(r'THE TEST STOPPED after (\d+) assertions, (\d+) of them failed(.*); it stopped at: (.*)', r.stdout)
    if not m: return 'caught: the test stops (%s)' % ((r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ['no output'])[-1][:90])
    if int(m.group(2)) > 0: return 'caught: %s assertions fail and then the test stops, after %s: %s' % (m.group(2), m.group(1), m.group(3).lstrip(': ').split(' | ')[0][:110])
    return 'caught ONLY BY THE TEST STOPPING, after %s assertions that all pass, at: %s' % (m.group(1), m.group(4)[:110])
def one(job):
    name, what, a, b = job; d = os.path.join(WORK, name); os.makedirs(d, exist_ok=True); s = SRC
    if a is not None: s = s.replace(a, b)
    path = os.path.join(d, 'gasket.html'); open(path, 'w', encoding='utf-8').write(s.replace('/*CORE*/', CORE).replace('/*DATA*/[]', DATA))
    env = dict(os.environ, LD_LIBRARY_PATH=os.path.join(WEB, 'sysroot/usr/lib/x86_64-linux-gnu'), NODE_PATH=os.path.join(WEB, 'node_modules'))
    try:
        r = subprocess.run(['nice', '-n', '15', 'timeout', '-k', '10', '500', 'node', 'shot-gasket.js', path, d, os.path.join(HERE, 'gcore.js'), os.path.join(HERE, 'data.json')], cwd=WEB, env=env, capture_output=True, text=True, timeout=560)
        m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed(.*)', r.stdout)
        res = ('caught: %s of %s assertions fail%s' % (m.group(2), m.group(1), m.group(3).split(' | ')[0][:112])) if m and int(m.group(2)) > 0 else ('NOT caught: all %s assertions pass' % m.group(1)) if m else ('caught: the test does not finish' if r.returncode in (124, 137) else stopped(r, None))
    except subprocess.TimeoutExpired: res = 'caught: the test does not finish'
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    os.rmdir(d); return name, what, res
if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    SRC = rd('page.src.html'); CORE = rd('gcore.js'); DATA = rd('data.json')
    names = [m[0] for m in M]; assert len(set(names)) == len(names), 'a name is used twice'
    bad = [(name, SRC.count(a)) for name, what, a, b in M if SRC.count(a) != 1]; assert not bad, bad
    assert open(os.path.join(WEB, 'shot-gasket.js'), encoding='utf-8').read() == rd(os.path.join('tools', 'shot-gasket.js')), 'the test in ~/web is not the copy in tools/'
    if len(sys.argv) > 1 and sys.argv[1] == 'list': print('%d faults, each pattern found once in page.src.html' % len(M)); sys.exit(0)
    jobs = int(sys.argv[1]) if len(sys.argv) > 1 else 4; only = sys.argv[2].split(',') if len(sys.argv) > 2 else None; t0 = time.time()
    chosen = [m for m in M if only is None or m[0] in only]; assert only is None or len(chosen) == len(only), 'a name asked for is not in the list'
    first = one(('control-alone', '', None, None)); assert first[2].startswith('NOT caught'), 'the true page does not pass by this runner: ' + first[2]
    print('control, alone: the true page, built and run in the same way: %s\n' % first[2].replace('NOT caught: ', ''), flush=True)
    todo = list(chosen); step = max(1, len(todo) // 4)
    for k, at in enumerate(range(step // 2, len(chosen), step)): todo.insert(at + k, ('control-%d' % (k + 1), 'THE TRUE PAGE, run among the broken copies, %d at a time' % jobs, None, None))
    caught = 0; controls = []; kinds = {'assert': 0, 'stop-after-failures': 0, 'stop-only': 0, 'no-finish': 0}
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for name, what, res in ex.map(one, todo):
            if name.startswith('control-'): controls.append(res); print('%-40s %s -- %s' % (name, what, 'passes: ' + res.replace('NOT caught: ', '') if res.startswith('NOT caught') else 'FAILS UNDER LOAD: ' + res), flush=True); continue
            caught += res.startswith('caught'); print('%-40s %s -- %s' % (name, what, res), flush=True)
            if res.startswith('caught'): kinds['stop-only' if 'ONLY BY THE TEST STOPPING' in res else 'no-finish' if 'does not finish' in res else 'stop-after-failures' if 'then the test stops' in res or 'the test stops (' in res else 'assert'] += 1
    print('\n%d of %d broken copies of the page caught%s (%d by assertions that fail at the end of a whole run, %d by assertions that fail before the test stops, %d only by the test stopping, %d by the test not finishing); the true page run among them %d times passed %d times; %d at a time, %.0f minutes' % (caught, len(chosen), '' if only is None else ' (a part of the list of %d, by name)' % len(M), kinds['assert'], kinds['stop-after-failures'], kinds['stop-only'], kinds['no-finish'], len(controls), sum(c.startswith('NOT caught') for c in controls), jobs, (time.time() - t0) / 60))
