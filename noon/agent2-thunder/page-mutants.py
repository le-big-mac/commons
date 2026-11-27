# page-mutants.py -- can the page test fail?  Copies of the page with one thing broken in its own script (not in core.js), each built
# and run through tools/shot-thunder.js in a headless browser, four at a time, the true page among them as a control.   python -I page-mutants.py [JOBS] > page-mutants.out
import subprocess, os, re
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); core = rd('core.js')
M = [
 ('ring-slow', "the ring is drawn growing at four fifths of the speed of sound", "var R = Math.max(0, C * st.t);", "var R = Math.max(0, 0.8 * C * st.t);"),
 ('ring-squashed', "the ring is drawn as an oval", "R / (Z1 - Z0) * H, 0, Math.PI, 2 * Math.PI); sc.stroke();", "0.7 * R / (Z1 - Z0) * H, 0, Math.PI, 2 * Math.PI); sc.stroke();"),
 ('sound-early', "the sound starts at once, whatever the distance", "src.start(now + Math.max(0, r.t0 - st.offset), Math.max(0, st.offset - r.t0));", "src.start(now, 0);"),
 ('sound-late', "the sound comes half a second after the ring", "src.start(now + Math.max(0, r.t0 - st.offset), Math.max(0, st.offset - r.t0));", "src.start(now + 0.5 + Math.max(0, r.t0 - st.offset), Math.max(0, st.offset - r.t0));"),
 ('dry-to-speaker', "the loudspeaker gets the sound without the air", "for (var i = 0; i < n; i++) out[i] = r.p[i] * k;", "for (var i = 0; i < n; i++) out[i] = r.dry[i] * k;"),
 ('loudness-rule', "loudness is squeezed two to one, not four", "function level(peak) { return 0.9 * Math.min(1, Math.sqrt(Math.sqrt(peak / REF))); }", "function level(peak) { return 0.9 * Math.min(1, Math.sqrt(peak / REF)); }"),
 ('skip-three', "skipping the silence starts three seconds before the sound", "st.offset = skip ? Math.max(0, (r.firstHeard === null ? r.first : r.firstHeard) - 0.6) : 0;", "st.offset = skip ? Math.max(0, (r.firstHeard === null ? r.first : r.firstHeard) - 3) : 0;"),
 ('skip-ignored', "the silence is skipped whether asked or not", "var r = st.res, skip = document.getElementById('skip').checked;", "var r = st.res, skip = true;"),
 ('drag-no-sound', "dragging the listener leaves the old sound", "if (st.kind === 'bow' || st.kind === 'away') rebuild(); else compute(); }", "if (st.kind === 'bow' || st.kind === 'away') rebuild(); }"),
 ('bow-stays', "the bow stays where it was when the listener moves", "if (st.kind === 'bow' || st.kind === 'away') rebuild(); else compute(); }", "compute(); }"),
 ('drag-half', "the listener goes half as far as the hand", "st.L = [Math.max(X0 + 300, Math.min(X1 - 300, Math.round(w[0]))), 0];", "st.L = [Math.max(X0 + 300, Math.min(X1 - 300, Math.round((w[0] + st.L[0]) / 2))), 0];"),
 ('sky-press-moves', "a press anywhere moves the listener", "if (nearListener(ev) || onGround(ev)) { stop();", "if (true) { stop();"),
 ('ground-press-dead', "a press on the ground does nothing", "if (nearListener(ev) || onGround(ev)) { stop();", "if (nearListener(ev)) { stop();"),
 ('jag-always', "the stroke is crooked whether asked or not", "var jagOn = document.getElementById('jag').checked;", "var jagOn = true;"),
 ('bow-opens-crooked', "the bow opens crooked", "bow: false, away: true };", "bow: true, away: true };"),
 ('straight-opens-crooked', "the straight one opens crooked", "straight: false, bow: false,", "straight: true, bow: false,"),
 ('away-opens-smooth', "pointing away opens smooth", "bow: false, away: true };", "bow: false, away: false };"),
 ('away-askew', "pointing away does not point away: its far end is 600 m too high", "[st.L[0] + side * far * ce, far * se]];", "[st.L[0] + side * far * ce, far * se + 600]];"),
 ('drawn-ignored', "a drawn line is thrown away", "st.kind = 'own'; st.raw = d; st.seed++; rebuild(); }", "st.kind = 'own'; st.seed++; rebuild(); }"),
 ('drawn-backwards', "a drawn line is taken from its end to its beginning", "st.kind = 'own'; st.raw = d; st.seed++; rebuild(); }", "st.kind = 'own'; st.raw = d.reverse(); st.seed++; rebuild(); }"),
 ('finger-ignored', "only a mouse can draw", "if (st.draw) { stop(); st.t = 0; st.drawing = [inSky(toWorld(ev))];", "if (st.draw && ev.pointerType !== 'touch') { stop(); st.t = 0; st.drawing = [inSky(toWorld(ev))];"),
 ('no-cap', "a drawn line may be as long as you like", "if (step > 30 && st.drawn + step <= LONGEST) {", "if (step > 30) {"),
 ('not-kept-in', "a drawn line may leave the picture", "function inSky(w) { return [Math.max(X0, Math.min(X1, w[0])), Math.max(0, Math.min(Z1, w[1]))]; }", "function inSky(w) { return w; }"),
 ('short-line-silent', "a line too short is refused without a word", "say.textContent = 'Too short to be a stroke: draw a line at least 150 metres long. The stroke is as it was.';", ""),
 ('lit-behind', "the lit part trails half a second behind the ring", "var lo = C * (st.t - 0.05), hi = C * st.t;", "var lo = C * (st.t - 0.55), hi = C * (st.t - 0.5);"),
 ('trace-shifted', "the line under the picture is drawn a second late", "var ta = c / cols * tmax, tb = (c + 1) / cols * tmax,", "var ta = c / cols * tmax - 1, tb = (c + 1) / cols * tmax - 1,"),
 ('marker-wrong', "the marker on the line runs at half speed", "tc.fillRect(tx(Math.min(st.t, tmax)) - DPR,", "tc.fillRect(tx(Math.min(st.t / 2, tmax)) - DPR,"),
 ('says-far-for-near', "the sentence gives the farthest point's distance for the first sound", "from <b>' + km(fh * C)", "from <b>' + km(r.farthest)"),
 ('says-last', "the sentence gives the time of the last sound as the first", "The first sound comes <b>' + fh.toFixed(1) + ' s</b>", "The first sound comes <b>' + r.last.toFixed(1) + ' s</b>"),
 ('says-near-for-far', "the sentence gives the nearest point's distance for the last sound", "</b> away; the last from ' + km(r.farthest)", "</b> away; the last from ' + km(r.nearest)"),
 ('loudness-true-for-played', 'the sentence gives the fall in pressure as the fall in what is played', ": 'it is played about ' + times(Math.pow(shown(rel), 0.25)) + ' times quieter", ": 'it is played about ' + times(rel) + ' times quieter"),
 ('loudness-inverted', "the sentence compares the crack's pressure with the sound's upside down", 'var rel = REF / peak, CRACK', 'var rel = peak / REF, CRACK'),
 ('hidden-unsaid', "the sentence never says that part of the stroke is hidden", "(hiddenCount() > 0 ? ' The dim part of the stroke is more than half hidden from you by the bending of sound.' : '')", "''"),
 ('silence-unsaid', "a stroke deep in the shadow is described as if it could be heard", "by this model you would hear next to nothing.';\n      brief.textContent = which() + 'Next to nothing to hear from here.'; return; }", "by this model you would hear next to nothing.'; fh = r.first; }"),
 ('no-stop-at-end', "it never stops by itself", "if (st.t > st.res.last + 0.6) { stop();", "if (st.t > st.res.last + 600) { stop();"),
 ('negative-time', "the picture's clock runs 0.3 s behind the sound", "st.t = Math.max(0, st.ctx.currentTime - st.tFlash);", "st.t = st.ctx.currentTime - st.tFlash - 0.3;"),
 ('small-letters', "the lettering does not grow on a narrow screen", "FONT = Math.round(Math.max(11.5 * DPR, 20 * w / 1200));", "FONT = Math.round(20 * w / 1200);"),
 ('stroke-off-frame', "the stroke is drawn 3 km to the left", "sc.lineTo(wx(p[i + 1][0]), wz(p[i + 1][1]));", "sc.lineTo(wx(p[i + 1][0] - 3000), wz(p[i + 1][1]));"),
 ('sound-unsaid', 'the opening does not say to turn the sound on (two visitors with a phone, 27 November)', 'Turn your sound on, press <b>Strike</b>', 'Press <b>Strike</b>'),
 ('boxes-small', 'the boxes to tick are as small as the browser makes them (13 px)', '  input[type="checkbox"] { width: 22px; height: 22px; margin: 0; accent-color: var(--ink); }', '  input[type="checkbox"] { margin: 0; }'),
 ('labels-short', 'the labels of the boxes are too short for a finger', 'align-items: center; min-height: 44px; cursor: pointer; }', 'align-items: center; cursor: pointer; }'),
 ('picture-stays-away', 'on a wide screen a stroke chosen with the picture off the screen leaves it off', 'rebuild(); showScene(); }; }', 'rebuild(); }; }'),
 ('picture-jumps', 'on a wide screen a stroke chosen with the picture in sight moves the page all the same', 'if (r.top < 0 || r.bottom > window.innerHeight) window.scrollBy(0, Math.round(r.top - 8));', 'window.scrollBy(0, Math.round(r.top - 8));'),
 ('decibels-back', 'the small print speaks of decibels again', 'a sound a hundred times lower\nin pressure is played about three times quieter.', 'a sound ten decibels weaker\nis played two and a half decibels quieter.'),
 ('loudness-in-thousands', 'the pressure is given a thousand times too small', "', with about ' + times(rel) + ' times less pressure than '", "', with about ' + times(1000 * rel) + ' times less pressure than '"),
 ('tip-baseline', 'the tip gives the crooked bow a thousand times less pressure', 'something like a hundred times lower in pressure than the crack, and is played', 'something like a thousand times lower in pressure than the crack, and is played'),
 ('bow-yardstick-near', 'the crack that every sound is set against is a bow half as far off', 'var REF = TH.thunder(TH.arc(0, 0, 3000, 150, 95), [0, 0]).peak;', 'var REF = TH.thunder(TH.arc(0, 0, 1500, 150, 95), [0, 0]).peak;'),
 ('against-full-volume', 'full volume is a peak of 0.5 again, with the crack 1.44 times above it, so that the two figures under the picture do not go together as four to one (a visitor with a calculator)', 'var REF = TH.thunder(TH.arc(0, 0, 3000, 150, 95), [0, 0]).peak;', 'var REF = 0.5;'),
 ('squeeze-unsaid', "nothing by the two figures says why 190 times less pressure is played only 3 times quieter (a visitor's snag)", " times quieter (loudness is squeezed: see the foot of the page).'", " times quieter.'"),
 ('quieter-to-a-decimal', 'how much quieter it is played is rounded to a whole number, so that 2.4 and 2.6 read as 2 and 3 (the referee)', ": 'it is played about ' + times(Math.pow(shown(rel), 0.25)) + ' times quieter", ": 'it is played about ' + Math.round(Math.pow(shown(rel), 0.25)) + ' times quieter"),
 ('picture-not-pinned', 'on a phone the picture scrolls away with the page', '#pin { position: sticky; top: 0; z-index: 2; background: var(--paper); box-shadow: 0 7px 6px -6px rgba(43, 38, 34, 0.45); }', '#pin { background: var(--paper); }'),
 ('picture-jumps-on-a-phone', 'on a phone a stroke chosen throws the page up to the picture, and the button out from under the finger (a visitor)', "    if (getComputedStyle(document.getElementById('pin')).position === 'sticky') return;      // (on a phone it is pinned in sight, and nothing need move)\n", ''),
 ('sentence-above-buttons', "the sentence stands above the stroke's buttons again, so that they move as it changes length (a visitor)", '<div class="row" role="group" aria-label="The stroke">', '<p id="say" aria-live="polite"></p>\n<div class="row" role="group" aria-label="The stroke">'),
 ('figures-underlined', 'the figures in the sentence are underlined like links', '  #say b { font-weight: 600; }', '  #say b { font-weight: normal; border-bottom: 1px solid var(--muted); }'),
 ('away-quietest', 'the tip calls the stroke pointing away much the quietest', 'strung out over many seconds and carries about a tenth of the energy of an upright stroke heard from 3 km, where the page opens,', 'strung out over many seconds and is much the quietest here, about a tenth of the energy of an upright stroke,'),
 ('straight-then-nothing', "the tip says that after the straight stroke's crack there is nothing", 'and then next to nothing, with a faint click from its far end.', 'and then nothing.'),
 ('strike-scrolls-away', 'on a phone Strike is not pinned with the picture, and scrolls away (a visitor chose a stroke among the tips and had to scroll back up to hear it)', '<div class="row" id="strikerow"><button id="strike">Strike</button><span id="brief" aria-hidden="true"></span></div>\n</div>', '</div>\n<div class="row" id="strikerow"><button id="strike">Strike</button><span id="brief" aria-hidden="true"></span></div>'),
 ('tips-slide', 'on a phone no room is kept for the longest sentence, and the tips slide as it changes', ' #say { min-height: 17.5em; }\n', '\n'),
 ('picture-dead-to-scrolling', 'a swipe that begins on the picture never scrolls the page', 'touch-action: pan-y; cursor: crosshair; }', 'touch-action: none; cursor: crosshair; }'),
 ('drawing-scrolls', 'while a stroke is being drawn the picture lets the page scroll under the finger', '  #scene.drawing { touch-action: none; }', '  #scene.drawing { touch-action: pan-y; }'),
 ('loudest-thing', "the tip calls the bow's crack the loudest thing on the page (a stroke heard from its foot has more pressure: the referee)", 'One crack, as loud as this page plays anything.', 'One crack, the loudest thing on this page.'),
 ('half-a-second', "the tip gives the crooked bow half a second or more (18 of the referee's hundred were shorter)", 'a bang of about a third of a second to a second,', 'a bang of half a second or more,'),
 ('as-loud-too-wide', 'a sound a fifth below the crack is said to be as loud as the page plays anything', "return rel < 1.06 && rel > 1 / 1.06 ? ', as loud as this page plays anything.'", "return rel < 1.25 && rel > 1 / 1.06 ? ', as loud as this page plays anything.'"),
 ('louder-unsaid', "a sound with twice the crack's pressure is said to be as loud as the page plays anything, and no more", "return rel < 1.06 && rel > 1 / 1.06 ? ', as loud as this page plays anything.'", "return rel < 1.06 ? ', as loud as this page plays anything.'"),
 ('nearly-as-loud-too-long', 'a sound played a tenth quieter is said to be played very nearly as loud', "(times(Math.pow(shown(rel), 0.25)) === '1.0' ?", '(Math.pow(shown(rel), 0.25) < 1.15 ?'),
 ('nearly-as-loud-by-the-true', 'whether a sound is "very nearly as loud" goes by the unrounded figure again, so that at 1.23 times less pressure the page says "played about 1.0 times quieter" (found by the test, 27 November)', "(times(Math.pow(shown(rel), 0.25)) === '1.0' ?", "((0.9 / level(peak)).toFixed(1) === '1.0' ?"),
 ('second-from-unrounded', 'the second figure is worked from the first before it is rounded, so that one sentence in ten shows a pair a digit out (the referee: 140 times and 3.5, where the fourth root of 140 is 3.4)', ": 'it is played about ' + times(Math.pow(shown(rel), 0.25)) + ' times quieter", ": 'it is played about ' + times(Math.pow(rel, 0.25)) + ' times quieter"),
 ('silence-infinite', 'asked of no sound at all, the words for loudness speak of infinitely less pressure', "    if (!(peak > 0)) return '.';", "    "),
 ('ground-tap-to-strike', "a tap with the finger on the picture's ground which the browser hands to Strike is not given back to the picture (a visitor: nothing moved, and it played)", "    if (ev.target !== scene && within(scene, down)) sceneDown(ev);", "    "),
 ('tips-dead', 'the strokes named in the tips are buttons that do nothing', "      else if (!jag) choose(kind)();", "      else if (!jag) { }"),
 ('tip-wrong-stroke', 'the tip for the stroke pointing away chooses the straight one', '<button class="tip" data-kind="away">', '<button class="tip" data-kind="straight">'),
 ('tip-tick-unticks', '"tick crooked" in a tip unticks it, and "untick" ticks', "want = jag === 'on';", "want = jag !== 'on';"),
 ('tip-tick-dead', '"tick crooked" in a tip sets the box and leaves the stroke as it was', "      else { if (j.checked !== want) { j.checked = want; rebuild(); } else if (st.playing) strike(); showScene(); }", "      else { if (j.checked !== want) { j.checked = want; } else if (st.playing) strike(); showScene(); }"),
 ('tip-draw-dead', '"Draw your own" in the tips does not turn drawing on', "      if (b.getAttribute('data-draw')) { stop(); st.t = 0; setDraw(true); showScene(); }", "      if (b.getAttribute('data-draw')) { stop(); st.t = 0; }"),
 ('tip-draw-toggles', '"Draw your own" in the tips turns drawing off when it is on (the first of the referee\'s three copies that passed the test of round four)', "      if (b.getAttribute('data-draw')) { stop(); st.t = 0; setDraw(true); showScene(); }", "      if (b.getAttribute('data-draw')) { stop(); st.t = 0; setDraw(!st.draw); showScene(); }"),
 ('tip-plays', 'a stroke chosen in a tip is set off at once', "      else if (!jag) choose(kind)();", "      else if (!jag) { choose(kind)(); strike(); }"),
 ('tips-small', 'the buttons inside the tips are in letters of 11 px', "button.tip { font: inherit; font-style: italic;", "button.tip { font: 11px/1 serif; font-style: italic;"),
 ('panel-gone', 'the sentence that changes is on bare paper again, like the advice beneath it (a visitor could not tell the two apart)', " padding: 8px 12px; border-left: 3px solid var(--muted); background: #fbf7ee; }", " }"),
 ('no-shadow', 'the pinned picture casts no shadow on what passes beneath it', " box-shadow: 0 7px 6px -6px rgba(43, 38, 34, 0.45); }", " }"),
 ('click-as-strong', "the tip says that from 9 km the straight stroke's click has the pressure of its crack (it has a third)", 'from 9 km the click has a third of the pressure of', 'from 9 km the click has the pressure of'),
 ('two-to-three', 'the tip says the crooked bow is played two to three times quieter (the thirty tried here run from 2.8 to 3.8)', 'and is played three to four times quieter.', 'and is played two to three times quieter.'),
 ('tip-tick-on-whatever-shows', '"tick crooked" in a tip acts on whatever stroke is showing, not on the stroke its tip is about (the referee: 32 starting states in 40)', "      else if (st.kind !== kind) choose(kind, want)();", "      else if (false) choose(kind, want)();"),
 ('tip-tick-toggles', '"tick crooked" in a tip toggles the box instead of setting it, so that pressed where the stroke is already crooked it unticks (the second of the referee\'s three copies)', "      else { if (j.checked !== want) { j.checked = want; rebuild(); } else if (st.playing) strike(); showScene(); }", "      else { j.checked = !j.checked; rebuild(); showScene(); }"),
 ('tip-tick-as-it-opens', 'a stroke chosen by "tick crooked" from another stroke opens as its button opens it, smooth for the bow', "document.getElementById('jag').checked = crooked === undefined ? CROOKED[kind] : crooked;", "document.getElementById('jag').checked = CROOKED[kind];"),
 ('tip-draw-leaves-picture', 'on a wide screen "Draw your own" in a tip leaves the picture out of sight (the third of the referee\'s three copies)', "      if (b.getAttribute('data-draw')) { stop(); st.t = 0; setDraw(true); showScene(); }", "      if (b.getAttribute('data-draw')) { stop(); st.t = 0; setDraw(true); }"),
 ('tip-tick-leaves-picture', 'on a wide screen "tick crooked" in the tip of the stroke showing leaves the picture out of sight', "      else { if (j.checked !== want) { j.checked = want; rebuild(); } else if (st.playing) strike(); showScene(); }", "      else { if (j.checked !== want) { j.checked = want; rebuild(); } else if (st.playing) strike(); }"),
 ('corner-of-strike-dead', 'a tap on Strike near one of its corners, which the browser hands to the picture, is not given back to Strike: nothing plays (found by the test of round five)', "if (down && within(strikeBtn, down, 1)) strike();", ""),
 ('corner-of-strike-moves', 'a tap on Strike near one of its corners, handed to the picture, moves the listener', "    if (!within(scene, { x: ev.clientX, y: ev.clientY })) return;", "    "),
 ('handed-tap-plays', 'a tap with the finger on the ground, handed to Strike, plays', "    if (ev.detail > 0 && down && within(scene, down) && ev.timeStamp - down.t < 1500) return;", "    "),
 ('keyboard-strike-dead', 'straight after the listener has been moved, Strike pressed from the keyboard does nothing', "    if (ev.detail > 0 && down && within(scene, down) && ev.timeStamp - down.t < 1500) return;", "    if (down && within(scene, down) && ev.timeStamp - down.t < 1500) return;"),
 ('brief-hidden', 'on a phone the sentence in short is not shown (a visitor: "the sentence the page prints is off the screen while I read any tip")', "    #brief { display: block; min-height: 5em;", "    #brief { min-height: 5em;"),
 ('brief-on-wide', 'the sentence in short is shown on a wide screen too, where the sentence is in sight', "  #brief { display: none; }", "  #brief { display: block; }"),
 ('brief-stale', 'the sentence in short is written once and never again', "    brief.textContent = (which() + 'First sound '", "    if (!brief.textContent) brief.textContent = (which() + 'First sound '"),
 ('brief-pressure-inverted', 'the sentence in short gives the pressure upside down', "      : 'about ' + times(rel) + ' times less pressure than '", "      : 'about ' + times(1 / rel) + ' times less pressure than '"),
 ('brief-other-rounding', 'the sentence in short rounds the pressure its own way, so that it and the sentence differ in a digit', "      : 'about ' + times(rel) + ' times less pressure than '", "      : 'about ' + Math.round(rel) + ' times less pressure than '"),
 ('brief-smooth-for-crooked', 'the sentence in short says smooth for crooked', "? ', crooked' : ', smooth'", "? ', smooth' : ', crooked'"),
 ('brief-wrong-name', 'the sentence in short calls the stroke pointing away a straight one', "away: 'Pointing away', own:", "away: 'A straight one', own:"),
 ('brief-wrong-length', 'the sentence in short gives the time of the last sound for how long the thunder lasts', "'; lasts ' + lasts + (dur < 0.1", "'; lasts ' + r.last.toFixed(1) + ' s' + (dur < 0.1"),
 ('brief-silent-unsaid', 'of a stroke deep in the shadow the sentence in short says nothing', "      brief.textContent = which() + 'Next to nothing to hear from here.'; return; }", "      return; }"),
 ('brief-drag-unsaid', 'while the listener is dragged the sentence in short stays as it was', " brief.textContent = say.textContent.replace(/(\\d) km/g, '$1\\u00a0km');", ""),
 ('brief-no-room', 'no room is kept for the sentence in short, so that the pinned block shrinks while the listener is dragged', "    #brief { display: block; min-height: 5em;", "    #brief { display: block;"),
 ('brief-small', 'the sentence in short is in letters of 10 px', " min-height: 5em; font-size: 13px; line-height: 1.25;", " min-height: 5em; font-size: 10px; line-height: 1.6;"),
 ('brief-too-long', 'the sentence in short is longer than its room: it gives the last sound and its distance as well', "'; lasts ' + lasts + (dur < 0.1", "'; the last sound comes from ' + km(r.farthest) + ' away, so that the thunder lasts ' + lasts + (dur < 0.1"),
 ('pressure-not-bold', 'in the sentence the pressure figure is not in bold (a visitor: "the two loudness figures are not bold, though they are answers too")', "      + loud.replace(/about ([\\d.,]+ times)/, 'about <b>$1</b>')", "      + loud"),
 ('press-strike-unsaid', 'the things to try do not say to press Strike after each (a visitor: "choosing a stroke in a tip is silent")', "<p><b>Things to try</b> (press Strike after each).</p>", "<p><b>Things to try.</b></p>"),
 ('far-off-unnamed', 'the first tip says "far off" and names no place (the referee: usually in the middle from about 8 km, half the time at 5 and 6)', "Far off, at 8 km, it comes later", "Far off it comes later"),
 ('always-begins', 'the first tip says that close in the thunder begins with its loudest part, without "nearly always" (9 of 400 did not)', "the thunder nearly always begins with its loudest part.", "the thunder begins with its loudest part."),
 ('crack-stands-alone', 'the fourth tip does not say that far off the crack no longer stands alone (the referee: "then next to nothing" is untrue from 9 km)', "and the click is not, so that the crack no longer stands alone: from 9 km", "and the click is not: from 9 km"),
 ('brief-borders-own', 'the short form calls everything within a fifth of the crack "as loud as this page plays anything", where the sentence says "very nearly as loud" (the first of the two copies of the referee\'s that passed the test of round five)', "    return rel < 1.06 && rel > 1 / 1.06 ? 'as loud as this page plays anything.'\n      : rel <= 1 / 1.06 ? 'about '", "    return rel < 1.2 && rel > 1 / 1.2 ? 'as loud as this page plays anything.'\n      : rel <= 1 / 1.2 ? 'about '"),
 ('strike-not-by-keyboard', 'the keyboard cannot reach Strike (the second of the two)', '<button id="strike">Strike</button>', '<button id="strike" tabindex="-1">Strike</button>'),
 ('stop-is-narrower', 'the button is narrower when it reads Stop, so that the short form beside it slides and breaks its lines afresh while the thunder plays (a visitor)', "  strikeBtn.style.minWidth = Math.ceil(strikeBtn.getBoundingClientRect().width) + 'px';", "  "),
 ('half-pixel-row', 'half a pixel above Strike, where the browser already counts the finger as on it, a tap handed to the picture does nothing (the referee: six of nine)', "if (down && within(strikeBtn, down, 1)) strike();", "if (down && within(strikeBtn, down)) strike();"),
 ('tip-leaves-it-playing', 'a "tick" pressed while its own stroke, already crooked, is playing lets the sound run on, and the button above reads Stop (the referee: 6 cases in 280)', " else if (st.playing) strike(); showScene(); }", " showScene(); }"),
 ('finger-never-forgotten', 'the place where a finger last went down is remembered for ever, so that a click on Strike that brings no pointer is refused however long after a press on the picture (the referee)', " && ev.timeStamp - down.t < 1500) return;", ") return;"),
 ('brief-loudest-from-unrounded', 'the short form works out how far in the loudest moment is before rounding, so that it can differ by a tenth from the two times the sentence prints', "var into = (Number(r.tpeak.toFixed(1)) - Number(fh.toFixed(1))).toFixed(1);", "var into = (r.tpeak - fh).toFixed(1);"),
 ('brief-always-at-start', 'the short form says "loudest at its start" of every thunder', "into === '0.0' ? ', loudest at its start'", "true ? ', loudest at its start'"),
 ('brief-first-sound-wrong', 'the short form gives the loudest moment for the first sound', "which() + 'First sound ' + fh.toFixed(1) + ' s, from '", "which() + 'First sound ' + r.tpeak.toFixed(1) + ' s, from '"),
 ('brief-from-wrong', 'the short form gives the farthest point for where the first sound comes from', "' s, from ' + km(fh * C) + '; lasts '", "' s, from ' + km(r.farthest) + '; lasts '"),
 ('brief-about-dropped', 'the short form gives its figure flat where the sentence says "about" (the referee)', "      : 'about ' + times(rel) + ' times less pressure than '", "      : times(rel) + ' times less pressure than '"),
 ('brief-which-bow', 'of a crooked bow the short form says "less pressure than the bow\'s crack" (a visitor: "which bow?")', "(st.kind === 'bow' ? 'when smooth.' : 'the bow\\u2019s crack.')", "'the bow\\u2019s crack.'"),
 ('brief-below-strike', 'the short form begins beneath Strike, not beside it', " #strike { float: left; margin: 0 8px 4px 0; }", " "),
 ('brief-room-320', 'at 320 wide room is kept for four lines of the short form, where it takes five (the referee made this copy and did not run it)', " #brief { min-height: 6.25em; } }", " }"),
 ('ground-marks-odd', 'the marks on the ground read 1, 3, 5, 7 and 9 km where they stand at 0, 2, 4, 6 and 8 (the one copy of the referee\'s that passed the test of round six)', "letter(sc, st.marks, k + ' km',", "letter(sc, st.marks, (k + 1) + ' km',"),
 ('seconds-one-more', 'the seconds under the line of sound read one too many (a copy the referee made and did not run)', "var word = s === 0 ? 'flash' : s + ' s',", "var word = s === 0 ? 'flash' : (s + 1) + ' s',"),
 ('figure-parts-from-unit', 'in the short form a figure can part from its unit at the end of a line (a visitor: "lasts 7.7 / s")', ".replace(/(\\d) (s|km|times|thousandths)\\b/g, '$1\\u00a0$2')", ""),
 ('s-parts-from-in', 'in the short form "s" can part from "in" at the end of a line (a visitor: "loudest 0.4 s / in")', ".replace(/(\\d\\u00a0s) in\\b/g, '$1\\u00a0in')", ""),
 ('all-of-this', 'the small print gives the whole model to its source again, the page\'s own three parts with it (the referee)', "Three things in it are this page's own, matched to nothing that has been checked:\nhow fast the air takes the high notes away, how the hidden part fades, and most of the recipe for its made-up crooked\nstrokes. What this leaves out:", "What this leaves out:"),
 ('drawn-other-than-recorded', 'on the ground and under the line of sound the figure drawn is one more than the figure put on record (the referee\'s copy that passed the test of round seven)', "    c.fillText(word, x, y);\n    list.push({ word: word, at: at,", "    c.fillText(word.replace(/\\d/, function (d) { return String(Number(d) + 1); }), x, y);\n    list.push({ word: word, at: at,"),
 ('lettering-drawn-along', 'each word of lettering is drawn 40 px to the right of where the record says', "    c.fillText(word, x, y);\n    list.push({ word: word, at: at,", "    c.fillText(word, x + 40, y);\n    list.push({ word: word, at: at,"),
 ('ground-lettering-dark', 'the kilometres on the ground are drawn in the colour of the ground', "    c.fillText(word, x, y);\n    list.push({ word: word, at: at,", "    c.save(); if (/km/.test(word)) c.fillStyle = '#1b2118'; c.fillText(word, x, y); c.restore();\n    list.push({ word: word, at: at,"),
 ('word-away-from-tick', 'each kilometre is lettered three letters\' breadth from its tick', "letter(sc, st.marks, k + ' km', x + 0.25 * FONT,", "letter(sc, st.marks, k + ' km', x + 3 * FONT,"),
 ('times-parts', 'in the short form a figure can part from "times" at the end of a line (the referee: 41 states of 62 at 360 wide)', "(s|km|times|thousandths)", "(s|km)"),
 ('four-to-one-back', 'the small print says "four to one" again (a visitor: "sounded like dividing by four")', "squeezes loudness, or the quiet thunder", "squeezes loudness four to one, or the quiet thunder"),
 ('left-out-unsaid', 'the small print does not say that Glassner\'s random shifts and his changing of the waves\' length and paths are left out (the referee)', " Two things\nthat Glassner's program has are left out as well: small random shifts in each sound's time of flight, for the\nunsteadiness of the air; and bending that changes the length of the waves and curves their paths, where here it\nonly hides the foot of a stroke.", ""),
 ('no-measurement', 'the small print says the page\'s own three parts are "matched to no measurement" (the air\'s figure was chosen to a remembered value: the referee)', "this page's own, matched to nothing that has been checked:", "this page's own and are matched to no measurement:"),
 ('seconds-drawn-other', 'under the line of sound each label is drawn one second more than is put on record (the first of three copies of the referee\'s that passed the test of round eight)', "    c.fillText(word, x, y);\n    list.push({ word: word, at: at,", "    c.fillText(c === tc && / s$/.test(word) ? (Number(word.split(' ')[0]) + 1) + ' s' : word, x, y);\n    list.push({ word: word, at: at,"),
 ('a-sixth-mark', 'a sixth mark, "7 km", stands at 1 km on the ground, drawn past the function that keeps the record (the second of the three)', "    sc.fillStyle = 'rgba(244,239,226,0.45)'; letter(sc, st.words, 'cloud',", "    sc.fillText('7 km', wx(1000) + 0.25 * FONT, wz(0) + 0.3 * FONT);\n    sc.fillStyle = 'rgba(244,239,226,0.45)'; letter(sc, st.words, 'cloud',"),
 ('cloud-named-low', 'the word "cloud" stands 2 km below the cloud\'s base (the third of the three)', "letter(sc, st.words, 'cloud', 0.5 * FONT, wz(5000) - 1.25 * FONT,", "letter(sc, st.words, 'cloud', 0.5 * FONT, wz(3000) - 1.25 * FONT,"),
 ('you-far-off', '"you (drag)" stands a tenth of the picture away from the listener', "letter(sc, st.words, 'you (drag)', lx + (flip ? -14 : 14) * U,", "letter(sc, st.words, 'you (drag)', lx + (flip ? -140 : 140) * U,"),
 ('hint-always', '"Drag across the sky to draw" is lettered whether drawing is on or not', "    if (st.draw) { sc.fillStyle = 'rgba(255,217,138,0.95)';", "    if (true) { sc.fillStyle = 'rgba(255,217,138,0.95)';"),
 ('random-delays', 'the small print says "random delays" where the article has "random variation to the time of flight" (the referee)', "small random shifts in each sound's time of flight", "small random delays to each sound"),
]
for name, what, a, b in M: assert src.count(a) == 1, name
work = os.path.join(here, 'mutants', 'page'); os.makedirs(work, exist_ok=True)
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'), NODE_PATH=os.path.expanduser('~/web/node_modules'))
test = os.path.expanduser('~/web/shot-thunder.js'); assert open(test, encoding='utf-8').read() == rd(os.path.join('tools', 'shot-thunder.js')), 'the test in ~/web is not the copy in tools/'
def run(path, where): return subprocess.run(['nice', '-n', '15', 'node', test, path, where, os.path.join(here, 'core.js')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True, timeout=420)
def one(job):
    name, what, a, b = job; d = os.path.join(work, name); os.makedirs(d, exist_ok=True); path = os.path.join(d, name + '.html')
    open(path, 'w', encoding='utf-8').write((src if a is None else src.replace(a, b)).replace('/*CORE*/', core))
    try:
        r = run(path, d); m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed(.*)', r.stdout)
        res = ('caught: %s of %s assertions fail%s' % (m.group(2), m.group(1), m.group(3)[:110])) if m and int(m.group(2)) > 0 else ('NOT caught: all %s assertions pass' % m.group(1)) if m else 'caught: the test stops (%s)' % (r.stderr.strip().splitlines() or ['no output'])[-1][:90]
    except subprocess.TimeoutExpired: res = 'caught: the test does not finish'
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    os.rmdir(d); return name, what, res
if __name__ == '__main__':
    import sys, time
    from concurrent.futures import ThreadPoolExecutor
    jobs = int(sys.argv[1]) if len(sys.argv) > 1 else 4; t0 = time.time()
    first = one(('control-alone', 'the true page, built and run in the same way, with nothing else of this runner going', None, None))
    assert first[2].startswith('NOT caught'), 'the true page does not pass by this runner: ' + first[2]
    print('control, alone: the true page, built and run in the same way: %s\n' % first[2].replace('NOT caught: ', ''), flush=True)
    only = sys.argv[2].split(',') if len(sys.argv) > 2 else None; chosen = [m for m in M if only is None or m[0] in only]; assert only is None or len(chosen) == len(only), 'a name asked for is not in the list'
    todo = list(chosen); step = max(1, len(todo) // 4)
    for k, at in enumerate(range(step // 2, len(chosen), step)): todo.insert(at + k, ('control-%d' % (k + 1), 'THE TRUE PAGE, run among the broken copies, %d at a time' % jobs, None, None))
    caught = 0; controls = []
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for name, what, res in ex.map(one, todo):
            if name.startswith('control-'): controls.append(res); print('%-22s %s -- %s' % (name, what, 'passes: ' + res.replace('NOT caught: ', '') if res.startswith('NOT caught') else 'FAILS UNDER LOAD: ' + res), flush=True); continue
            caught += res.startswith('caught'); print('%-22s %s -- %s' % (name, what, res), flush=True)
    print('\n%d of %d broken copies of the page caught%s; the true page run among them %d times passed %d times; %d at a time, %.0f minutes' % (caught, len(chosen), '' if only is None else ' (a part of the list of %d, by name)' % len(M), len(controls), sum(c.startswith('NOT caught') for c in controls), jobs, (time.time() - t0) / 60))
