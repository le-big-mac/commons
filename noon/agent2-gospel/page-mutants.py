# page-mutants.py -- can the page test fail?  Copies of the page with one thing broken in its own script, style or text (not in core.js),
# each built and run through tools/shot-gospel.js in a headless browser, three at a time.   python -I page-mutants.py > page-mutants.out
import subprocess, os, re, sys
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); core = rd('core.js')
M = [
 ('one-step-short', "a turtle that comes home is stopped one step early", "else if (f.bounded) { rounds = 1; total = s + n; }", "else if (f.bounded) { rounds = 1; total = s + n - 1; }"),
 ('one-round-only', "a turtle that marches away is drawn for one round at the least, not four", "rounds = Math.max(4, Math.min(40, Math.round(240 / n)));", "rounds = Math.max(1, Math.min(40, Math.round(240 / n)));"),
 ('no-cap', "the page draws as many steps as the round has, however many", "    if (total > MAXDRAW) { rounds = Math.floor((MAXDRAW - s) / n); total = rounds >= 1 ? s + n * rounds : MAXDRAW; }\n", ""),
 ('walks-another', "the page walks a turtle whose upper number is one more than was typed", "S.w = T.walk(S.P, S.Q, total);", "S.w = T.walk(S.P + 1, S.Q, total);"),
 ('too-big', "the figure is drawn to fill the longer side", "var k = Math.min((W - 2 * pad) / bw, (H - 2 * pad) / bh); k = Math.min(k, 90 * DPR);", "var k = Math.max((W - 2 * pad) / bw, (H - 2 * pad) / bh); k = Math.min(k, 90 * DPR);"),
 ('upside-down', "the picture is drawn upside down", "function px(x, y) { return [S.view.ox + S.view.k * x, S.view.oy - S.view.k * y]; }", "function px(x, y) { return [S.view.ox + S.view.k * x, H - (S.view.oy - S.view.k * y)]; }"),
 ('mirrored', "the picture is drawn left for right", "function px(x, y) { return [S.view.ox + S.view.k * x, S.view.oy - S.view.k * y]; }", "function px(x, y) { return [W - (S.view.ox + S.view.k * x), S.view.oy - S.view.k * y]; }"),
 ('all-at-first-step', "the whole figure is drawn at the first step", "if (n > S.drawn) { drawSteps(S.drawn, n); S.drawn = n; drawTurtle(); }", "if (n > S.drawn) { drawSteps(S.drawn, S.total); S.drawn = n; drawTurtle(); }"),
 ('dots-late', "the dots are put one step after the end of each round", "var d = px(w.xs[at], w.ys[at]); fc.beginPath();", "var d = px(w.xs[Math.min(S.total, at + 1)], w.ys[Math.min(S.total, at + 1)]); fc.beginPath();"),
 ('no-dots', "no dots are drawn", "if (at > from && at <= to && at > 0) {", "if (false) {"),
 ('dots-every-other', "only every other round gets its dot", "for (var j = 0; j <= S.rounds; j++) { var at = s + j * n;", "for (var j = 0; j <= S.rounds; j += 2) { var at = s + j * n;"),
 ('guide-short', "the dashed line is laid to the end of the first round only", "x1: S.w.xs[s + n * S.rounds], y1: S.w.ys[s + n * S.rounds] };", "x1: S.w.xs[s + n], y1: S.w.ys[s + n] };"),
 ('guide-undrawn', "the dashed line is spoken of and not drawn", "    var g = S.guide; if (!g) return;\n    fc.strokeStyle = 'rgba(168,72,42,0.55)';", "    var g = null; if (!g) return;\n    fc.strokeStyle = 'rgba(168,72,42,0.55)';"),
 ('turtle-stays', "the turtle is left at the start", "var w = S.w, k = S.drawn, p = px(w.xs[k], w.ys[k]), hx, hy;", "var w = S.w, k = S.drawn, p = px(0, 0), hx, hy;"),
 ('turtle-behind', "the turtle is drawn one corner behind", "var w = S.w, k = S.drawn, p = px(w.xs[k], w.ys[k]), hx, hy;", "var w = S.w, k = S.drawn, p = px(w.xs[Math.max(0, k - 1)], w.ys[Math.max(0, k - 1)]), hx, hy;"),
 ('turtle-backwards', "the turtle is drawn pointing backwards", "tc.rotate(Math.atan2(hx, hy));", "tc.rotate(Math.atan2(hx, hy) + Math.PI);"),
 ('turtle-always-up', "the turtle always points up the page", "if (k > 0) { hx = w.xs[k] - w.xs[k - 1]; hy = w.ys[k] - w.ys[k - 1]; } else { hx = 0; hy = 1; }", "hx = 0; hy = 1;"),
 ('says-one-step-more', "the forecast gives one step too many", "s += 'it comes home after <b>' + T.commas(n) + ' steps</b>.", "s += 'it comes home after <b>' + T.commas(n + 1) + ' steps</b>."),
 ('says-home-always', "the forecast says home for every turtle that does not walk straight", "else if (f.home) s += 'it comes home after", "else if (true) s += 'it comes home after"),
 ('why-wrong-prime', 'the reason names the wrong prime as the one that helps', "has = ' contains the prime ' + num(sv.l) + ' ' + times(sv.e);", "has = ' contains the prime ' + num(sv.l + 2) + ' ' + times(sv.e);"),
 ('why-wrong-power', "the reason tests with l where it should test with the power of l that the rule gives: false for 1/189 (the referee's)", 'var sv = f.serves, lk = T.commas(Math.pow(sv.l, sv.k)),', 'var sv = f.serves, lk = T.commas(Math.pow(sv.l, 1)),'),
 ('why-lone-prime-wrong', 'for a power of one prime the reason names the wrong prime', "if (!others.length) return odd + has + ', which is what closes the round.';", "if (!others.length) return odd + ' contains the prime ' + num(sv.l + 2) + ' ' + times(sv.e) + ', which is what closes the round.';"),
 ('why-wrong-order', 'the reason gives a round one step too long', 'function roundOf(r) { var o = T.order2(r);', 'function roundOf(r) { var o = T.order2(r) + 1;'),
 ('why-spoiler-wrong', 'the reason names the wrong prime as the one that undoes', 'var bk = T.commas(Math.pow(b.l, b.k)); return roundOf(b.r) +', 'var bk = T.commas(Math.pow(b.l, b.k)); return roundOf(b.r + 2) +'),
 ('why-no-square-always', "every turtle that marches away is said to hold no square", "    if (!f.squares) return odd +", "    if (true) return odd +"),
 ('tail-unsaid', 'the forecast does not mention the tail', "    if (!s) return 'Its turns' + unit + ': ' + round + ': a round of ' + steps + '.';", "    if (true) return 'Its turns' + unit + ': ' + round + ': a round of ' + steps + '.';"),
 ('odd-part-unsaid', 'the reason is given for the whole bottom number when it is even', "var odd = f.tail ? 'The odd part of the bottom number, ' + name + ',' : name;", 'var odd = name;'),
 ('degrees-halved', "the first turn is shown as half its degrees", "var d = 360 * f.p / f.q,", "var d = 180 * f.p / f.q,"),
 ('lowest-terms-unsaid', "the page does not say what the fraction is in lowest terms", "+ '° (' + frac() + ' in lowest terms' + (within ? '' : ', whole turns left out') + ')';", "+ '°';"),
 ('whole-turns-unsaid', "the page does not say that whole turns were left out of 10/9 (the referee's)", "(within ? '' : ', whole turns left out')", "''"),
 ('report-as-typed', "the report gives the fraction as typed, not in lowest terms", "its next turn would be ' + frac() + ' of a turn again.'", "its next turn would be ' + S.P + '/' + S.Q + ' of a turn again.'"),
 ('loop-says-home', "a turtle circling its loop is reported as home", "s = '<b>Step ' + T.commas(k) + ': back where it stood at step ' + T.commas(t) + '</b>, at the end of its tail.", "s = '<b>Step ' + T.commas(k) + ': home.</b> It stood at step ' + T.commas(t) + ', at the end of its tail."),
 ('gain-doubled', "the report gives twice the distance a round carries it", "var far = S.gain >= 0.0005 ? S.gain.toFixed(3) + ' steps'", "var far = S.gain >= 0.0005 ? (2 * S.gain).toFixed(3) + ' steps'"),
 ('gain-three-places', "a very small distance is given to three places, as 0.000 steps (the page as first published)", "var far = S.gain >= 0.0005 ? S.gain.toFixed(3) + ' steps' : (S.gain * 1e6).toPrecision(3) + ' millionths of a step'", "var far = S.gain.toFixed(3) + ' steps'"),
 ('millionths-are-thousandths', "a very small distance is called millionths and is thousandths", "(S.gain * 1e6).toPrecision(3)", "(S.gain * 1e3).toPrecision(3)"),
 ('open-called-closed', "the page takes a round for closed when it misses by less than a hundred-thousandth: the nearest miss is then called a disagreement", "S.gain > 1e-7 && (S.rounds < 2 || onGuide())", "S.gain > 1e-5 && (S.rounds < 2 || onGuide())"),
 ('line-always-seen', "the report speaks of the dashed line when it is under a pixel long", "hidden = Math.hypot(g1[0] - g0[0], g1[1] - g0[1]) < DPR;", "hidden = false;"),
 ('line-never-seen', "the report calls every dashed line too short to see", "hidden = Math.hypot(g1[0] - g0[0], g1[1] - g0[1]) < DPR;", "hidden = true;"),
 ('headway-in-rounds', "the steps needed for one step of headway are given as the rounds needed", "T.commas(Number((n / S.gain).toPrecision(3)))", "T.commas(Number((1 / S.gain).toPrecision(3)))"),
 ('nearest-button-other', "the ninth button sends off another turtle", "{ p: '1635', q: '1009681', name:", "{ p: '1637', q: '1009681', name:"),
 ('note-nearest-wrong', "the note misstates the nearest miss", "ends 1.04 millionths", "ends 1.40 millionths"),
 ('note-next-wrong', "the note misstates the next nearest miss", "misses by 5.59 millionths", "misses by 5.95 millionths"),
 ('note-rounds-count-wrong', "the note misstates how many rounds were added up", "some 53 million of them", "some 35 million of them"),
 ('headway-from-232', "the steps for one step of headway are reckoned from 232 steps whatever the round (the referee's)", "T.commas(Number((n / S.gain).toPrecision(3)))", "T.commas(Number((232 / S.gain).toPrecision(3)))"),
 ('millionths-too-late', "a miss is given in millionths only below 0.00002 steps, so that 141 millionths prints as 0.000 steps (the referee's)", "var far = S.gain >= 0.0005 ?", "var far = S.gain >= 0.00002 ?"),
 ('note-other-turtle', "the note says that the second program found a different turtle (the referee's)", "found the same turtle and the same miss", "found a different turtle and a smaller miss"),
 ('note-person-checked', "the note says that a person has checked the count", "No person has checked\neither.", "A person has checked\nboth."),
 ('quick-short-unseen', "a walk of six steps at 'quick' is over in a fifth of a second (the page as first published; the plain reader's)", 'var quick = Math.max(4, S.total / 6);', 'var quick = Math.max(30, S.total / 6);'),
 ('turns-a-step-late', 'the list of turns begins with the second turn', 'function turnsFrom(f, from, count) { var out = [], t = f.p % f.q, k;', 'function turnsFrom(f, from, count) { var out = [], t = f.p * 2 % f.q, k;'),
 ('turns-half-degrees', 'the turns are listed at half their size', "var show = function (t) { return deg ? (360 / q * t) + '°' : T.commas(t); };", "var show = function (t) { return deg ? (180 / q * t) + '°' : T.commas(t); };"),
 ('turns-cut-short', "a round of seven to twelve steps is listed as six turns and then 'and so on'", 'var Rn = turnsFrom(f, s, n <= 12 && !(s && n > 6) ? n : 6)', 'var Rn = turnsFrom(f, s, n <= 5 && !(s && n > 6) ? n : 6)'),
 ('pace-ignored', "a change of pace is not obeyed until Go is pressed again (the page as first published; the plain reader's)", "  $('pace').addEventListener('change', newPace);\n", ''),
 ('pace-starts-over', 'a change of pace reckons the steps from the moment of the change, so the turtle stands still for a while', 'S.t0 = now - S.drawn / S.rate * 1000;', 'S.t0 = now;'),
 ('not-steady', "a button that changes the words above the picture lets the picture slide (the plain reader's)", 'if (Math.abs(b - a) >= 0.5) window.scrollBy(0, b - a);', ''),
 ('go-moves', "the line with the degrees stands before Go again, so Go moves as the fraction is typed (the page as first published; the plain reader's)", '  <button id="go">Go</button>\n  <label>pace <select id="pace" aria-label="pace"><option value="slow">slow</option><option value="quick" selected>quick</option><option value="once">all at once</option></select></label>\n</div>\n<p id="deg" class="small"></p>', '  <span id="deg" class="small"></span>\n  <button id="go">Go</button>\n  <label>pace <select id="pace" aria-label="pace"><option value="slow">slow</option><option value="quick" selected>quick</option><option value="once">all at once</option></select></label>\n</div>'),
 ('end-not-kept', 'when the walk ends and the line under the picture grows, it is left to run off the foot of the screen', 'if (r.top > -40 && r.top < window.innerHeight) bringUp();', ''),
 ('buttons-small', 'the buttons are too low to tap', 'min-height: 44px; }', 'min-height: 24px; }'),
 ('notes-small', 'the headings of the folded notes are too low to tap', 'summary { cursor: pointer; font-size: 17px; padding: 8px 0; }', 'summary { cursor: pointer; font-size: 17px; padding: 0; }'),
 ('lead-unfair', "the plain paragraph says the memo's rule was wrong, without calling it a rule of thumb", 'A memo of 1972 gave that as its rule of thumb for a turtle', 'A memo of 1972 gave that as the rule, wrongly, for a turtle'),
 ('noon-unsaid', 'the foot of the page does not say what Noon is', 'Noon is an AI, one of three that keep', 'Noon is one of three that keep'),
 ('times-wrong', 'a prime that comes in twice is said to come in three times', "e === 2 ? 'twice'", "e === 2 ? 'three times'"),
 ('undo-swapped', 'the reason for a turtle that comes home says that the test number divides the other round', "', which ' + lk + ' does not divide'", "', which ' + lk + ' divides'"),
 ('self-unsaid', 'for 1093 squared the reason blames another prime', "(b.self ? 'for this prime that is not enough: ' :", "(false ? 'for this prime that is not enough: ' :"),
 ('grid-hint-wrong', 'the sentence above the grid says that the dark squares come home', 'the rust ones come home', 'the dark ones come home'),
 ('note-ties-unsaid', "the note does not say that 231 other first turns tie with the nearest", ", with the 231 other first turns that its doubling\npasses through", ""),
 ('rounds-one-more', "the report counts one round too many", "mark the end of each of the ' + T.commas(S.rounds) + ' rounds drawn.'", "mark the end of each of the ' + T.commas(S.rounds + 1) + ' rounds drawn.'"),
 ('straight-unsaid', "a turtle walking straight on is reported as going round", "It is walking straight on.';", "It is going round.';"),
 ('stop-unsaid', "the forecast does not say the page will stop early", "s += ' That is more than this page draws: it will stop at step ' + T.commas(S.total) + '.';", "s += '';"),
 ('cut-said-uncut', "the forecast says the walk is cut when exactly 20,000 steps make whole rounds (the fault the referee found)", "if (!f.straight && !(S.rounds >= 1 && S.total === f.tail + n * S.rounds)) s +=", "if (S.total === MAXDRAW || (f.bounded && f.tail + n > MAXDRAW)) s +="),
 ('count-frozen', "the report does not count while the turtle walks", "    report(); requestAnimationFrame(step);\n  }", "    requestAnimationFrame(step);\n  }"),
 ('keeps-walking', "changing a number does not stop the turtle", "S.running = false; S.done = false; S.drawn = 0; S.valid = P !== null && okQ;", "S.done = false; S.valid = P !== null && okQ;"),
 ('slow-is-fast', 'slow is ten times too fast', 'Math.max(S.total / 60, Math.min(5, quick / 2))', 'Math.max(S.total / 60, Math.min(50, quick * 5))'),
 ('quick-is-slow', 'quick takes eighteen seconds', 'var quick = Math.max(4, S.total / 6);', 'var quick = Math.max(4, S.total / 18);'),
 ('enter-dead', "Enter in the lower box does nothing", "  $('den').addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });", ""),
 ('button-swapped', 'one button has its two numbers the wrong way round', "{ p: '1', q: '45', name: '1/45: home (breaks the stricter rule)' },", "{ p: '45', q: '1', name: '1/45: home (breaks the stricter rule)' },"),
 ('button-idle', 'a button fills the boxes but does not send the turtle off', "b.addEventListener('click', function () { steady(function () { setPair(p.p, p.q); }); go(); });", "b.addEventListener('click', function () { steady(function () { setPair(p.p, p.q); }); });"),
 ('boxes-not-filled', "a button or a square sends the turtle off but leaves the boxes as they were", "if (!fromBox) { $('num').value = pStr; $('den').value = qStr; }", ""),
 ('go-when-bad', "Go stays alive when a box holds no number", "$('go').disabled = !S.valid;", "$('go').disabled = false;"),
 ('bad-keeps-picture', "a box with no number leaves the old picture standing", "else { fc.setTransform(1, 0, 0, 1, 0, 0); fc.clearRect(0, 0, W, H); tc.clearRect(0, 0, W, H); }", ""),
 ('bad-unmarked', "the box with no number is not marked", "$('num').classList.toggle('bad', P === null); ", ""),
 ('too-large-taken', "a lower number above the limit is taken", "var okQ = Q !== null && Q >= 1 && Q <= T.QMAX;", "var okQ = Q !== null && Q >= 1 && Q <= 10 * T.QMAX;"),
 ('grid-colours-swapped', "the grid paints those that come home dark and the spoilt squares rust", "var SHADE = ['#e9e1cf', '#2b2622', '#a8482a'];", "var SHADE = ['#e9e1cf', '#a8482a', '#2b2622'];"),
 ('grid-shifted', "the grid is drawn one square to the right of where pointing reads it", "return [(i % COLS) * cw, Math.floor(i / COLS) * chh, cw, chh]; }", "return [((i + 1) % COLS) * cw, Math.floor(i / COLS) * chh, cw, chh]; }"),
 ('pointer-one-on', "pointing at the grid names the next denominator", "var i = Math.min(CENSUS.kind.length - 1, row * COLS + col); return 2 * i + 3;", "var i = Math.min(CENSUS.kind.length - 1, row * COLS + col); return 2 * i + 5;"),
 ('cell-says-swapped', "pointing at a square says home for those that march away, and the other way", "(f.bounded ? 'comes home after ' + T.commas(f.round) + ' steps. ' : 'marches away. ')", "(!f.bounded ? 'comes home after ' + T.commas(f.round) + ' steps. ' : 'marches away. ')"),
 ('click-idle', 'the button under the grid puts its turtle in the boxes but does not send it off', "var m = PEND; setPair('1', String(m), false, 'grid'); go(); });", "var m = PEND; setPair('1', String(m), false, 'grid'); });"),
 ('frame-on-next', "the blue frame is drawn on the next square", "var c = cellBox((f.q - 3) / 2);", "var c = cellBox((f.q - 1) / 2);"),
 ('frame-any-upper', 'a turn of 8/9 is framed on the grid as if it were 1/9', 'if (S.valid && f.p === 1 && f.q % 2 === 1 && f.q >= 3 && f.q <= TOP) {', 'if (S.valid && f.q % 2 === 1 && f.q >= 3 && f.q <= TOP) {'),
 ('count-swapped', "the grid's sentence counts the undone ones as those that come home", "T.commas(CENSUS.closes) + ' come home; ' + T.commas(CENSUS.spoilt) + ' contain a prime", "T.commas(CENSUS.spoilt) + ' come home; ' + T.commas(CENSUS.closes) + ' contain a prime"),
 ('note-count-wrong', "the note's count of squares that do not save is out of the wrong total", "$('spoiltcount').textContent = T.commas(CENSUS.spoilt) + ' of the ' + T.commas(CENSUS.spoilt + CENSUS.closes) +", "$('spoiltcount').textContent = T.commas(CENSUS.spoilt) + ' of the ' + T.commas(CENSUS.spoilt + CENSUS.plain) +"),
 ('no-refit', "the figure is not drawn again when the window changes", "if (S.w && S.valid) { setView(); redraw(); }", ""),
 ('junk-redrawn', "after a refused number, a change of width brings the ring and the turtle back (the fault the referee found)", "if (S.w && S.valid) { setView(); redraw(); }", "if (S.w) { setView(); redraw(); }"),
 ('guide-lost-on-resize', "the dashed line is not drawn again when the window changes (the referee's)", "function redraw() { drawBase(); drawSteps(0, S.drawn); if (S.done) drawGuide(); drawTurtle(); }", "function redraw() { drawBase(); drawSteps(0, S.drawn); drawTurtle(); }"),
 ('no-scroll-on-go', "on a small phone Go leaves the picture below the screen (the fault the referee found)", "    bringUp();\n", "\n"),
 ('scroll-canvas-only', "Go brings the picture up but not the lines under it that say what happened (the plain reader's)", "r = $('result').getBoundingClientRect(), top = r.bottom - a.top <= H - 1 ? a.top : r.top;", 'r = field.parentNode.getBoundingClientRect(), top = r.bottom - a.top <= H - 1 ? a.top : r.top;'),
 ('scroll-browser', "Go leaves the bringing up to the browser's own scrollIntoView, which stops short of the frame's lower edge", '    if (b.top >= 0 && b.bottom <= H) return;\n', "    if (b.top >= 0 && b.bottom <= H) return;\n    $('result').scrollIntoView({ block: 'nearest' }); return;\n"),
 ('scroll-top-only', 'a picture above the screen is not brought down', 'b.fits && b.top >= 0 ? Math.ceil(b.bottom - H) : Math.floor(b.top));', 'b.fits && b.top >= 0 ? Math.ceil(b.bottom - H) : 0);'),
 ('key-swapped', "the key under the grid calls the dark squares 'comes home' (the referee's)", '<span class="sw" style="background:#a8482a"></span>comes home', '<span class="sw" style="background:#2b2622"></span>comes home'),
 ('rule-misstated', "the folded rule has another prime undo with l where it should be the power of l (after the referee's)", 'Another prime <i>r</i> of <i>q</i> undoes it if <i>l<sup>k</sup></i> divides', 'Another prime <i>r</i> of <i>q</i> undoes it if <i>l</i> divides'),
 ('rule-lone-prime', "the folded rule drops 'if k is at least 1': read to the letter it would have 1093 squared close", 'The prime <i>l</i> helps if <i>k</i> is at\nleast 1.', 'The prime <i>l</i> helps.'),
 ('tail-one-more', "the forecast gives a tail one step too long (the referee's)", "T.commas(s) + ' turns' + unit + ', '", "T.commas(s + 1) + ' turns' + unit + ', '"),
 ('tail-always-plural', "a tail of one step is called '1 turns'", "(s === 1 ? 'turn' + unit + ', ' + Tl[0] +", "(s === 0 ? 'turn' + unit + ', ' + Tl[0] +"),
 ('fifty-to-a-row', "the grid has fifty squares to a row where the page says forty (the referee's)", "var TOP = 2001, COLS = 40;", "var TOP = 2001, COLS = 50;"),
 ('grid-backwards', "the grid is drawn right to left (the referee's)", "return [(i % COLS) * cw, Math.floor(i / COLS) * chh, cw, chh]; }", "return [(COLS - 1 - i % COLS) * cw, Math.floor(i / COLS) * chh, cw, chh]; }"),
 ('memo-45-wrong', "the note says the memo's rule gets 45 wrong", "(the memo's own rule gets 45 right)", "(the memo's own rule gets 45 wrong)"),
 ('fuchs-date', "the note misdates Fuchs", "dated Berlin, 1862, and printed in 1863", "dated Berlin, 1872, and printed in 1873"),
 ('sheets-apart', "the turtle's sheet is a little larger than the line's", ".stage { position: relative; border: 1px solid var(--line); border-radius: 6px; background: #fffdf7; overflow: hidden; }", ".stage { position: relative; width: 100%; } #field { border: 1px solid var(--line); border-radius: 6px; background: #fffdf7; }"),
 ('grid-too-wide', "the grid does not shrink to a narrow screen", "#map { display: block; width: 100%; max-width: 720px;", "#map { display: block; width: 720px; max-width: 720px;"),
 ('label-no-wrap', "the row of boxes cannot wrap on a very narrow screen (the fault the test first found)", "display: inline-flex; flex-wrap: wrap; gap: 6px; align-items: center; }", "display: inline-flex; gap: 6px; align-items: center; }"),
 ('note-2457', "the note's second count is one too many", "636,963 have such a prime and 2,456\n", "636,963 have such a prime and 2,457\n"),
 ('note-share', "the note's weighted share is wrong in its second decimal", "0.109 for odd", "0.119 for odd"),
 ('note-example', 'the folded rule gives a wrong round for 1/5', 'because the round of 1/5 has 4 steps, which 3 does not divide', 'because the round of 1/5 has 3 steps, which 3 does not divide'),
 ('note-quote', "HAKMEM is misquoted", "which must occur at least cubed”", "which must occur at least squared”"),
 ('note-salvaged', "the note says again that the memo doubts its .155 (a misreading of mine and the referee's, found in the check of the mending)", "with the memo's own exceptions not taken off. By the rule", "and adds that this “might, however, be salvaged by quantities like 171”. By the rule"),
 ('note-ends', "the note says the book's exercise ends with its question (it has one more sentence)", "and asks: “Can you prove", "and ends: “Can you prove"),
 ('note-q1', "the note's true half of the claim takes in a denominator of 1", "an odd denominator greater than 1 divides", "an odd denominator divides"),
 ('note-proof', "the first note says 'A proof is in the write-up', not saying whose", 'The write-up has an argument for it that I made before I\nknew of his.', 'A proof is in the write-up.'),
 # ---- added with the third plain reader's round (26 November): the grid's choice, the line under the picture, the plainer forecast
 ('who-one-step-more', 'the line under the picture gives one step too many for the forecast', "f.home ? 'it will come home after ' + T.commas(n) + ' steps' : f.bounded ? 'it will never come home, and never get away'", "f.home ? 'it will come home after ' + T.commas(n + 1) + ' steps' : f.bounded ? 'it will never come home, and never get away'"),
 ('who-loop-as-away', 'the line under the picture says of a turtle that circles a loop only that it will never come home', ": f.bounded ? 'it will never come home, and never get away' : 'it will never come home') + '.'", ": false ? 'it will never come home, and never get away' : 'it will never come home') + '.'"),
 ('who-straight-unsaid', 'the line under the picture does not say that a turtle will walk straight on', "(f.straight ? 'it will walk straight on' : f.home ?", "(false ? 'it will walk straight on' : f.home ?"),
 ('who-no-verdict', "the line under the picture names the turtle and does not repeat the forecast (the page before the third plain reader's visit)", "' of a whole turn. Forecast: ' + (f.straight ? 'it will walk straight on' : f.home ? 'it will come home after ' + T.commas(n) + ' steps' : f.bounded ? 'it will never come home, and never get away' : 'it will never come home') + '.'", "' of a whole turn.'"),
 ('tap-overwrites', "a tap on the grid puts its turtle in the boxes at once (the page the third plain reader saw: 'my own numbers were gone')", 'var m = cellAt(ev); PEND = m; markMap();', "var m = cellAt(ev); PEND = m; setPair('1', String(m)); markMap();"),
 ('tap-stops-walk', "a tap on the grid stops the turtle that is walking (the third plain reader's)", 'var m = cellAt(ev); PEND = m; markMap();', 'var m = cellAt(ev); PEND = m; S.running = false; markMap();'),
 ('ring-missing', 'the tapped square gets no ring', '    if (PEND === null) return;\n    var c = cellBox((PEND - 3) / 2), x =', '    if (true) return;\n    var c = cellBox((PEND - 3) / 2), x ='),
 ('ring-next-square', 'the ring is drawn round the square after the one tapped', 'var c = cellBox((PEND - 3) / 2), x = c[0] + c[2] / 2,', 'var c = cellBox((PEND - 3) / 2 + 1), x = c[0] + c[2] / 2,'),
 ('ring-small', 'the ring is no bigger than the square (the 9 px outline the third plain reader could hardly see)', 'r = 1.5 * c[2];', 'r = 0.5 * c[2];'),
 ('ring-lost-when-bad', 'the ring vanishes while what is typed is not a number', '    S.pick = null; var f = S.f;\n', '    S.pick = null; var f = S.f; if (!S.valid) return;\n'),
 ('watch-names-first', 'the button under the grid keeps the name of the first square tapped (the fault the third plain reader found on the first page)', "$('watch').textContent = 'Watch 1/' + T.commas(m) + ' walk'; $('watch').hidden = false; });", "if ($('watch').hidden) $('watch').textContent = 'Watch 1/' + T.commas(m) + ' walk'; $('watch').hidden = false; });"),
 ('watch-sends-boxes', 'the button under the grid sends off the turtle in the boxes, not the one tapped', "if (PEND === null) return; var m = PEND; setPair('1', String(m), false, 'grid'); go(); });", 'go(); });'),
 ('typing-clears-choice', "typing a fraction takes the grid's ring and button away (the page before this round)", 'S.from = from || null;', "S.from = from || null; if (from !== 'grid') { $('watch').hidden = true; PEND = null; }"),
 ('leave-keeps-pointed', 'when the pointer leaves the grid the words stay with the square last pointed at, not the ringed one the button names', "function () { if (PEND !== null) $('mapsay').textContent = cellSay(PEND); });", "function () { if (false) $('mapsay').textContent = cellSay(PEND); });"),
 ('wrap-wrong-sum', 'where the doubling passes a whole turn the page gives the wrong double', "' is ' + (360 / q * 2 * a) + '°, which is a whole turn and '", "' is ' + (360 / q * 2 * a + 10) + '°, which is a whole turn and '"),
 ('wrap-too-soon', "the page says 'a whole turn' of a doubling that does not pass one", 'if (b !== null && 2 * a >= q) wrap =', 'if (b !== null && 4 * a >= q) wrap ='),
 ('wrap-unsaid', "the page does not say where the doubling passes a whole turn (the page the third plain reader saw: 'twice 320 is 640, not 280')", "' comes again') + wrap;", "' comes again');"),
 ('wrap-units-wrong', 'in units of 1/q the page says the whole turn is q + 1', "', which is ' + T.commas(q) + ' and ' + show(b) + ')'", "', which is ' + T.commas(q + 1) + ' and ' + show(b) + ')'"),
 ('big-list-kept', 'for a large bottom number the turns are still listed in units of 1/q (the wall the third plain reader skipped)', 'if (!deg && q > 999)', 'if (!deg && q > 99999999)'),
 ('big-round-wrong', 'for a large bottom number the forecast gives a round one step too long', 'var n = f.round, s = f.tail, q = f.q, deg = 360 % q === 0, steps = T.commas(n) +', 'var n = f.round, s = f.tail, q = f.q, deg = 360 % q === 0, steps = T.commas(n + 1) +'),
 ('others-unnamed', "the reason speaks of 'its other prime' without naming it (the page the third plain reader saw)", "', and its other prime, ' + num(others[0]) + ', does not undo that: '", "', and its other prime does not undo that: '"),
 ('other-misnamed', 'the reason names the wrong prime as the other one', "', and its other prime, ' + num(others[0]) + ', does not undo that: '", "', and its other prime, ' + num(others[0] + 2) + ', does not undo that: '"),
 ('too-unsaid', 'for 1/441 the page does not say that 3 comes in twice as well and is undone', 'var too = f.spoilt.length ?', 'var too = false ?'),
 ('pointer-twice', "a reason that already says 'see the rule below' gets the pointer to the note as well", "s.indexOf('see the rule below') < 0 && s.indexOf('undo') >= 0 ?", "s.indexOf('undo') >= 0 ?"),
 ('pointer-unsaid', 'no reason points to the note that says why that is the test', "s.indexOf('see the rule below') < 0 && s.indexOf('undo') >= 0 ?", 'false ?'),
 ('commas-missing', "large factors are printed without commas (59393 beside 1,009,681: the third plain reader's)", 'function num(x) { return x >= 10000 ? T.commas(x) : String(x); }', 'function num(x) { return String(x); }'),
 ('prime-itself-unsaid', 'of 7 the page says that it contains no prime more than once', "if (!composite) return odd + ' is itself a prime:", "if (false) return odd + ' is itself a prime:"),
 ('closes-of-open', 'the forecast says of a round that does not close that it ends where it began', "(n === 1 ? ' step does' : ' steps do') + ' not end where they began: the round does not close, and each", "' steps end where they began: the round closes, and each"),
 ('tenth-button-wrong', 'the tenth button is 1/100000', "{ p: '1', q: '1000000', name: '1/1000000: a tail, then a great loop' }", "{ p: '1', q: '100000', name: '1/1000000: a tail, then a great loop' }"),
 ('watch-room-unkept', 'no room is kept for the button under the grid, so that what is under it jumps when it comes', '#watchp { min-height: 46px; margin: 8px 0 4px; }', '#watchp { min-height: 0; margin: 0; }'),
 ('button-below-words', 'the button is put under the words about the tapped square, not directly under the grid', '<p id="watchp"><button id="watch" hidden>Watch it walk</button></p>\n<p id="mapsay" class="small">&nbsp;</p>\n', '<p id="mapsay" class="small">&nbsp;</p>\n<p id="watchp"><button id="watch" hidden>Watch it walk</button></p>\n'),
 ('link-small', "the link back to the grid is one line of small print (16 px tall: the third plain reader's)", '  #who a { display: inline-block; padding: 7px 0; }\n', ''),
]
# the story paragraph moved back under the buttons (where the third plain reader found it: 'it sits below nine buttons whose labels depend on it')
_i = src.index('<p><b>Which turtles come home?</b>'); _j = src.index('<div class="row presets" id="presets"', _i); _k = src.index('\n', _j) + 1
M.append(('story-below', 'the paragraph that says what the rule of thumb and the stricter rule are comes after the buttons that are named from them', src[_i:_k], src[_j:_k] + src[_i:_j]))
for name, what, a, b in M: assert src.count(a) == 1, (name, src.count(a))
work = os.path.join(here, 'mutants', 'page'); os.makedirs(work, exist_ok=True)
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'), NODE_PATH=os.path.expanduser('~/web/node_modules'))
test = os.path.expanduser('~/web/shot-gospel.js'); assert open(test, encoding='utf-8').read() == rd(os.path.join('tools', 'shot-gospel.js')), 'the test in ~/web is not the copy in tools/'
def run(path, out=None): return subprocess.run(['node', test, path, out or work, os.path.join(here, 'core.js'), os.path.join(here, 'table.json'), os.path.join(here, 'gospel.sealed-run.out'), os.path.join(here, 'more.sealed-run.out'), os.path.join(here, 'small', 'small.sealed-run.out')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True, timeout=400)
def one(job):
    name, what, a, b = job; out = os.path.join(work, name); os.makedirs(out, exist_ok=True); path = os.path.join(out, name + '.html')
    open(path, 'w', encoding='utf-8').write((src if a is None else src.replace(a, b)).replace('/*CORE*/', core))
    try:
        r = run(path, out); m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed(.*)', r.stdout)
        res = ('caught: %s of %s assertions fail%s' % (m.group(2), m.group(1), m.group(3)[:110])) if m and int(m.group(2)) > 0 else ('NOT caught: all %s assertions pass' % m.group(1)) if m else 'caught: the test gives no tally (%s)' % ((r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ['no output'])[-1][:110])
    except subprocess.TimeoutExpired: res = 'caught: the test does not finish'
    shutil.rmtree(out, ignore_errors=True)
    return name, what, res
if __name__ == '__main__':
    import shutil, concurrent.futures
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    path = os.path.join(work, 'true.html'); open(path, 'w', encoding='utf-8').write(src.replace('/*CORE*/', core)); r = run(path)
    m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed', r.stdout); assert m and m.group(2) == '0', 'the true page does not pass by this runner: ' + (r.stdout[-300:] + r.stderr[-300:])
    print('control: the true page, built and run in the same way, alone: %s assertions, 0 failed' % m.group(1), flush=True); os.remove(path)
    for f in os.listdir(work):
        if f.endswith('.png'): os.remove(os.path.join(work, f))
    # the broken copies are run %d at a time; the true page is run twice more among them, to show that running side by side fails nothing
    jobs = list(M); jobs.insert(len(M) // 4, ('true-among-them-1', 'the true page, run among the broken copies', None, None)); jobs.insert(3 * len(M) // 4, ('true-among-them-2', 'the true page, run among the broken copies', None, None))
    caught = 0; controls = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        for name, what, res in ex.map(one, jobs):
            if name.startswith('true-among-them'): controls.append(res); continue
            caught += res.startswith('caught'); print('%-22s %s -- %s' % (name, what, res), flush=True)
    print('\ncontrol: the true page run twice among them (%d at a time): %s' % (workers, '; '.join('passes' if c.startswith('NOT caught') else 'FAILS: ' + c for c in controls)))
    print('%d of %d broken copies of the page caught' % (caught, len(M)))
