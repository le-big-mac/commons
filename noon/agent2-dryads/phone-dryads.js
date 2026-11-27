// Can the Dryads page be used on a phone, and under a line put above it (the public copy has one)?
// At several screen sizes, with and without such a line: every control inside the screen, the picture given the room that is left,
// the caption inside the picture's width, and Ring ringing at a tap.   usage: node phone-dryads.js dryads.html OUTDIR
const { chromium } = require('playwright'), fs = require('fs'), path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]); fs.mkdirSync(out, { recursive: true });
  let n = 0, failed = 0; const must = (ok, what, detail) => { n++; if (!ok) failed++; console.log((ok ? 'ok   ' : 'FAIL ') + what + (detail ? '   [' + detail + ']' : '')); };
  // the public copy's line, as its builder writes it (the words are the builder's; only their height matters here)
  const bar = '\n<p style="font:13px/1.45 system-ui,sans-serif;margin:0;padding:6px 12px;background:#f3f1ec;color:#333;border-bottom:1px solid #d8d3c8">Written by Noon, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. <a href="../about.html" style="color:#1c5cab">How it was checked, and how it was not.</a> <a href="../index.html" style="color:#1c5cab">All of Noon\'s pages.</a></p>';
  const src = fs.readFileSync(page, 'utf8'), m = /<body[^>]*>/.exec(src); const withBar = path.join(out, 'with-line.html'); fs.writeFileSync(withBar, src.slice(0, m.index + m[0].length) + bar + src.slice(m.index + m[0].length));
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  for (const [w, h, touch] of [[390, 844, true], [360, 640, true], [412, 915, true], [320, 568, true], [1000, 800, false], [1280, 720, false]]) for (const [file, name] of [[page, 'as it is'], [withBar, 'under the public copy\'s line']]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: touch ? 2 : 1, hasTouch: touch, isMobile: touch }), p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
    await p.goto('file://' + file + '#seed=1123'); await p.waitForTimeout(500);
    const r = await p.evaluate(() => { const box = el => { const q = el.getBoundingClientRect(); return [q.left, q.top, q.right, q.bottom]; }, ids = ['play', 'again', 'line'].concat(innerWidth > 340 ? ['clock'] : []);      // (on the narrowest screens the clock is left out)
      return { W: innerWidth, H: innerHeight, sw: document.documentElement.scrollWidth, controls: ids.map(i => [i].concat(box(document.getElementById(i)))).concat([['about'].concat(box(document.querySelector('#bar a')))]),
        stage: box(document.getElementById('stage')), bar: box(document.getElementById('bar')), seed: getComputedStyle(document.getElementById('seed')).display, cap: window.__dryads.caption ? window.__dryads.caption() : null, first: document.body.firstElementChild.tagName }; });
    const outside = r.controls.filter(c => c[1] < 0 || c[2] < 0 || c[3] > r.W + 0.5 || c[4] > r.H + 0.5 || c[3] - c[1] < 20 /* and none squeezed to nothing */), tall = Math.min(r.controls[0][4] - r.controls[0][2], r.controls[1][4] - r.controls[1][2]);
    await p.screenshot({ path: path.join(out, w + 'x' + h + (file === page ? '' : '-line') + '.png') });
    const t0 = await p.evaluate(() => window.__dryads.now()); if (touch) await p.tap('#play'); else await p.click('#play'); await p.waitForTimeout(1500);
    const label = await p.evaluate(() => document.getElementById('play').textContent), t1 = await p.evaluate(() => window.__dryads.now());
    must(outside.length === 0 && r.sw <= r.W && r.bar[3] <= r.H + 0.5 && Math.abs(r.stage[3] - r.bar[1]) < 1.5 && r.stage[3] - r.stage[1] >= 250 && (file === page) === (r.first === 'CANVAS')
      && r.cap && r.cap.widest <= r.cap.room + 0.5 && (w >= 1000 ? r.cap.lines === 1 && r.seed !== 'none' : r.cap.lines >= 2 && r.seed === 'none' && tall >= 36)
      && label === 'Pause' && t1 > t0 + 0.8 && errs.length === 0,
      w + ' by ' + h + ', ' + name + ': Ring, Another grove, the line, the clock and "about" are all inside the screen; the picture has the room over the bar (250 px or more) and the bar ends at the foot of the screen; the caption is inside the picture\'s width' + (w >= 1000 ? ', on one line, and the seed is shown' : ', on two lines or more, the seed is left to the address, and the buttons are 36 px tall or more') + '; a ' + (touch ? 'tap' : 'click') + ' on Ring starts the piece',
      'picture ' + Math.round(r.stage[3] - r.stage[1]) + ' px tall; bar ' + Math.round(r.bar[1]) + ' to ' + Math.round(r.bar[3]) + ' of ' + r.H + '; caption ' + (r.cap ? r.cap.lines + ' lines, ' + Math.round(r.cap.widest) + ' of ' + Math.round(r.cap.room) : 'none') + (outside.length ? '; outside: ' + outside.map(c => c[0] + ' ' + c.slice(1).map(Math.round).join(',')).join(' | ') : '') + '; buttons ' + Math.round(tall) + ' px tall; ' + label + ' at ' + t1.toFixed(1) + ' s');
    await ctx.close(); }
  await b.close(); console.log('PHONE TEST: ' + n + ' assertions, ' + failed + ' failed'); process.exit(failed ? 1 : 0);
})();
