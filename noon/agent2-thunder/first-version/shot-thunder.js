// Headless checks of the thunder page, played by a made-up hand.   usage: node shot-thunder.js PAGE.html OUTDIR CORE.js
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]), TH = require(path.resolve(process.argv[4]));
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 1100, height: 1500 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page); await p.waitForTimeout(600);
  const fails = []; let asserts = 0;
  const must = (cond, what, detail) => { asserts++; if (!cond) fails.push(what); console.log((cond ? 'ok   ' : 'FAIL ') + what + (detail ? '   [' + detail + ']' : '')); };
  const state = () => p.evaluate(() => window.THUNDERSTATE());
  const box = async () => p.locator('#scene').boundingBox();
  const at = async (x, z) => { const bx = await box(), [X0, X1, Z0, Z1] = (await state()).view; return [bx.x + (x - X0) / (X1 - X0) * bx.width, bx.y + (1 - (z - Z0) / (Z1 - Z0)) * bx.height]; };
  const ink = () => p.evaluate(() => { const c = document.getElementById('scene'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let ring = 0, bolt = 0, x0 = 1e9, x1 = -1, y0 = 1e9, y1 = -1;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) { const i = 4 * (y * c.width + x), r = d[i], g = d[i + 1], bl = d[i + 2];
      if (r > 200 && g > 150 && g < 215 && bl < 150) ring++;
      if (r > 150 && g > 145 && bl > 135 && Math.abs(r - g) < 25) { bolt++; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; } }
    return { ring, bolt, x0, x1, y0, y1, w: c.width, h: c.height }; });

  // 1. as it opens
  let s = await state();
  must(errs.length === 0, 'the page opens without a script error', errs.join(' | ').slice(0, 200));
  must(s.kind === 'stroke' && s.listener[0] === 3000 && s.pieces > 1500, 'it opens on a made-up stroke with the listener 3 km off', s.pieces + ' pieces, ' + (s.length / 1000).toFixed(2) + ' km');
  must(Math.abs(s.first - s.nearest / 343) < 1e-9 && Math.abs(s.last - s.farthest / 343 - 0.005) < 1e-9, 'first and last sound are the nearest and farthest points at 343 m/s', s.first.toFixed(3) + ' s to ' + s.last.toFixed(3) + ' s');
  // 2. the stroke and the sound are the ones core.js makes here
  { const pts = TH.stroke(s.seed), res = TH.thunder(pts, s.listener), m = TH.measure(pts);
    must(pts.length - 1 === s.pieces && Math.abs(m.length - s.length) < 1e-6 && Math.abs(pts[0][0] - s.first3[0][0]) < 1e-9 && Math.abs(pts[pts.length - 1][1] - s.last1[1]) < 1e-9, 'the stroke on the page is the one core.js makes in node from the same seed');
    const snd = await p.evaluate(() => window.THUNDERSOUND(37)), k = s.level / res.peak; let worst = 0, dot = 0, aa = 0, bb = 0, n = 0;
    for (let i = 0, j = 0; i < res.p.length; i += 37, j++) { const v = Math.fround(res.p[i] * k); worst = Math.max(worst, Math.abs(v - snd[j])); dot += v * snd[j]; aa += v * v; bb += snd[j] * snd[j]; n++; }
    must(n === snd.length && worst < 1e-6 && dot / Math.sqrt(aa * bb) > 0.999999, 'the sound handed to the loudspeaker is core.js\'s, sample for sample (every 37th)', n + ' samples, worst difference ' + worst.toExponential(2));
    must(Math.abs(s.level - 0.9 * Math.min(1, Math.sqrt(res.peak / 0.01))) < 1e-12 && s.level <= 0.9, 'and its loudness is the stated half-decibel rule', s.level.toFixed(3)); }
  { const km = m => (m / 1000).toFixed(1) + ' km', want = ['nearest point is ' + km(s.nearest) + ' from you', 'first sound comes ' + s.first.toFixed(1) + ' s after the flash', 'farthest is ' + km(s.farthest),
      'lasts ' + (s.last - s.first).toFixed(1) + ' s', 'loudest ' + s.tpeak.toFixed(1) + ' s after', 'stroke is ' + km(s.length) + ' long'];
    must(want.every(w => s.say.includes(w)), 'the sentence under the picture gives the nearest and farthest points and the times, as core.js has them', s.say.slice(0, 150)); }
  const i0 = await ink();
  must(i0.bolt > 800 && i0.ring > 30 && i0.x0 >= 0 && i0.x1 < i0.w && i0.y0 >= 0 && i0.y1 < i0.h, 'the stroke and the listener are drawn inside the frame', 'bolt pixels ' + i0.bolt + ', listener pixels ' + i0.ring);
  await p.screenshot({ path: path.join(out, 'thunder-open.png'), fullPage: true });

  // 3. strike, the silence skipped: the ring moves at the speed of sound
  await p.click('#strike');
  let heardAt = null, quietBefore = true; const a0 = await state();
  for (let k = 0; k < 60 && heardAt === null; k++) { const e = await p.evaluate(() => window.THUNDEREAR()); if (e.loud > 1e-5) heardAt = e.t; else if (e.t > a0.first + 0.3) break; await p.waitForTimeout(25); }
  must(heardAt !== null && heardAt > a0.first - 0.03 && heardAt < a0.first + 0.15, 'the sound reaches the loudspeaker when the ring reaches the nearest point of the stroke', 'heard at ' + (heardAt === null ? 'never' : heardAt.toFixed(3)) + ' s after the flash; the nearest point is ' + a0.first.toFixed(3) + ' s away');
  { const both = await p.evaluate(() => [window.THUNDERSTATE().t, window.THUNDEREAR().t]);          // the clock the picture is drawn by, and the sound's own clock
    must(Math.abs(both[0] - both[1]) < 0.08, 'the picture\'s clock and the sound\'s clock agree to within a few frames', both.map(v => v.toFixed(3)).join(' and ')); }
  const a = await state(); await p.waitForTimeout(700); const c = await state();
  must(a.playing && c.playing && a.strikes === 1, 'Strike starts it', 'audio ' + c.audio);
  must(a.offset > 0 && Math.abs(a.offset - (a.first - 0.6)) < 1e-9 && a.t >= a.offset, 'with the silence skipped it begins 0.6 s before the first sound', 'offset ' + a.offset.toFixed(2) + ' s');
  // the dots that mark what is being heard lie between the ring and where it was a twentieth of a second ago
  { const dots = await p.evaluate(() => { const c = document.getElementById('scene'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data, out = [];
      for (let y = 0; y < c.height; y += 1) for (let x = 0; x < c.width; x += 1) { const i = 4 * (y * c.width + x); if (d[i] > 248 && Math.abs(d[i + 1] - 217) < 6 && Math.abs(d[i + 2] - 138) < 8) out.push([x, y]); }
      const st = window.THUNDERSTATE(); return { out, w: c.width, h: c.height, view: st.view, L: st.listener, t: st.t }; });
    const [X0, X1, Z0, Z1] = dots.view, rr = dots.out.map(([x, y]) => Math.hypot(X0 + x / dots.w * (X1 - X0) - dots.L[0], Z0 + (1 - y / dots.h) * (Z1 - Z0)));
    const lo = Math.min(...rr), hi = Math.max(...rr), R = 343 * dots.t;
    must(dots.out.length > 20 && hi < R + 110 && lo > R - 0.05 * 343 - 110, 'the lit part of the stroke lies at the ring (within the size of the dots)', dots.out.length + ' lit pixels, ' + lo.toFixed(0) + ' to ' + hi.toFixed(0) + ' m from the listener; the ring is at about ' + R.toFixed(0) + ' m'); }
  must(c.t - a.t > 0.5 && c.t - a.t < 1.2, 'time runs: 0.7 s later the clock has moved about 0.7 s', (c.t - a.t).toFixed(3));
  must(Math.abs(c.ring - 343 * c.t) < 1e-6 && c.ring > a.ring, 'the ring is 343 m for each second since the flash, and has grown', c.ring.toFixed(0) + ' m');
  const i1 = await ink();
  must(i1.ring > i0.ring + 400, 'a ring is drawn', i1.ring + ' ring-coloured pixels against ' + i0.ring + ' before');
  await p.locator('#scene').screenshot({ path: path.join(out, 'thunder-playing.png') });
  await p.click('#strike'); await p.waitForTimeout(150); s = await state();
  must(!s.playing && s.t === 0, 'pressing it again stops it');

  // 4. the ring is where it should be: at 5 s it meets the ground 1,715 m either side of the listener
  await p.evaluate(() => window.THUNDERSEEK(5)); await p.waitForTimeout(80);
  { const hit = await p.evaluate(([X0, X1, Z0, Z1, L]) => { const c = document.getElementById('scene'), g = c.getContext('2d'); const px = x => Math.round((x - X0) / (X1 - X0) * c.width), py = z => Math.round(c.height - (z - Z0) / (Z1 - Z0) * c.height);
      const near = (x, z) => { let n = 0; const d = g.getImageData(px(x) - 4, py(z) - 4, 9, 9).data; for (let i = 0; i < d.length; i += 4) if (d[i] > 180 && d[i + 1] > 130 && d[i + 1] < 215 && d[i + 2] < 150) n++; return n; };
      return [near(L + 1715 * Math.cos(1), 1715 * Math.sin(1)), near(L - 1715 * Math.cos(0.5), 1715 * Math.sin(0.5)), near(L + 1300 * Math.cos(1), 1300 * Math.sin(1)), near(L + 2100 * Math.cos(1), 2100 * Math.sin(1))]; }, [...s.view, s.listener[0]]);
    must(hit[0] > 0 && hit[1] > 0 && hit[2] === 0 && hit[3] === 0, 'five seconds after the flash the ring is drawn 1,715 m from the listener, and not at 1,300 or 2,100', hit.join(', ')); }
  { const tr = await p.evaluate(() => { const c = document.getElementById('trace'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let b0 = 1e9, b1 = -1, amber = [], blue = 0;
      for (let x = 0; x < c.width; x++) { let nb = 0, na = 0; for (let y = 0; y < c.height; y++) { const i = 4 * (y * c.width + x); if (d[i + 3] > 100 && d[i + 2] > 110 && d[i] < 90 && d[i + 2] > d[i] + 40) nb++; if (d[i + 3] > 100 && d[i] > 150 && d[i + 2] < 90 && d[i + 1] > 100) na++; }
        if (nb > 0) { blue += nb; if (x < b0) b0 = x; if (x > b1) b1 = x; } if (na > 20) amber.push(x); }
      return { b0, b1, blue, amber, w: c.width, dpr: window.devicePixelRatio || 1 }; });
    const tmax = Math.max(s.last + 0.5, 4), left = 6 * tr.dpr, span = tr.w - 12 * tr.dpr, tOf = x => (x - left) / span * tmax;
    must(tr.blue > 300 && Math.abs(tOf(tr.b0) - s.first) < 0.15 && Math.abs(tOf(tr.b1) - s.last) < 0.15, 'the line under the picture begins at the first sound and ends at the last', tOf(tr.b0).toFixed(2) + ' s to ' + tOf(tr.b1).toFixed(2) + ' s; the sound runs ' + s.first.toFixed(2) + ' to ' + s.last.toFixed(2));
    must(tr.amber.length > 0 && Math.abs(tOf((tr.amber[0] + tr.amber[tr.amber.length - 1]) / 2) - 5) < 0.08, '   ... and its marker stands at the time shown, five seconds', tr.amber.length ? tOf((tr.amber[0] + tr.amber[tr.amber.length - 1]) / 2).toFixed(2) : 'none'); }
  await p.evaluate(() => window.THUNDERSEEK(0));

  // 5. drag the listener to 6 km
  { const before = await state(), from = await at(before.listener[0], 60), to = await at(6000, 60);
    await p.mouse.move(from[0], from[1]); await p.mouse.down(); await p.mouse.move((from[0] + to[0]) / 2, to[1], { steps: 5 }); await p.mouse.move(to[0], to[1], { steps: 5 }); await p.mouse.up(); await p.waitForTimeout(300);
    const after = await state(), pts = TH.stroke(after.seed), res = TH.thunder(pts, after.listener);
    must(Math.abs(after.listener[0] - 6000) < 25 && after.computed === before.computed + 1, 'a made-up hand drags the listener to 6 km', 'x = ' + after.listener[0]);
    must(after.first > before.first + 5 && Math.abs(after.first - res.first) < 1e-9 && Math.abs(after.peak - res.peak) < 1e-12, 'and the sound is worked out again for the new place', 'first sound ' + before.first.toFixed(1) + ' s, then ' + after.first.toFixed(1) + ' s');
    must(after.level < before.level && after.peak < before.peak, 'further off it is quieter', before.peak.toFixed(4) + ' then ' + after.peak.toFixed(4)); }

  // 6. the other strokes
  await p.uncheck('#jag'); await p.click('#b-bow'); await p.waitForTimeout(300); s = await state();
  must(s.kind === 'bow' && s.square === s.pieces && Math.abs(s.nearest - 3000) < 1e-6 && Math.abs(s.farthest - 3000) < 1e-6, 'a smooth bow about the listener: every piece square-on and 3 km away', s.pieces + ' pieces');
  must(s.last - s.first < 0.0051, '   ... so the whole sound lasts one pulse', ((s.last - s.first) * 1000).toFixed(2) + ' ms');
  { const from = await at(s.listener[0], 60), to = await at(4000, 60); await p.mouse.move(from[0], from[1]); await p.mouse.down(); await p.mouse.move(to[0], to[1], { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(300);
    const s2 = await state(); must(Math.abs(s2.listener[0] - 4000) < 25 && s2.square === s2.pieces && Math.abs(s2.nearest - 3000) < 1e-6, 'the bow follows the listener when dragged', 'x = ' + s2.listener[0]); }
  await p.click('#b-straight'); await p.waitForTimeout(300); s = await state();
  must(s.kind === 'straight' && s.kink === 0 && Math.abs(s.length - 5000) < 1e-6, 'a straight one, smooth: 5 km and no crookedness');
  const straightSmooth = s.peak;
  await p.check('#jag'); await p.waitForTimeout(300); s = await state();
  must(s.kink > 14 && s.kink < 18 && s.length > 5000, 'made crooked: about 16 degrees a piece, and longer', s.kink.toFixed(1) + ' degrees, ' + (s.length / 1000).toFixed(2) + ' km');
  await p.click('#b-cloud'); await p.waitForTimeout(300); s = await state();
  must(s.kind === 'cloud' && s.last - s.first > 8, 'along the cloud: the thunder lasts many seconds', (s.last - s.first).toFixed(1) + ' s');
  await p.screenshot({ path: path.join(out, 'thunder-cloud.png'), fullPage: true });

  // 7. draw one
  await p.click('#b-draw'); await p.waitForTimeout(100); s = await state();
  must(s.draw && await p.getAttribute('#b-draw', 'aria-pressed') === 'true', 'Draw your own switches drawing on');
  { const before = s, pA = await at(1000, 4500), pB = await at(2500, 2500), pC = await at(1500, 800);
    await p.mouse.move(pA[0], pA[1]); await p.mouse.down(); await p.mouse.move(pB[0], pB[1], { steps: 12 }); await p.mouse.move(pC[0], pC[1], { steps: 12 }); await p.mouse.up(); await p.waitForTimeout(400);
    const after = await state();
    must(after.kind === 'own' && after.computed > before.computed && after.pieces !== before.pieces, 'a line drawn across the sky becomes the stroke', after.pieces + ' pieces, ' + (after.length / 1000).toFixed(2) + ' km');
    must(Math.abs(after.first3[0][0] - 1000) < 60 && Math.abs(after.first3[0][1] - 4500) < 60 && Math.abs(after.last1[0] - 1500) < 60 && Math.abs(after.last1[1] - 800) < 60, 'and it begins and ends where the hand did', after.first3[0].map(v => v.toFixed(0)).join(', ') + ' to ' + after.last1.map(v => v.toFixed(0)).join(', '));
    // a finger, too
    const q = await at(5000, 3000), q2 = await at(7000, 3500);
    await p.evaluate(([x0, y0, x1, y1]) => { const c = document.getElementById('scene'); const ev = (t, x, y) => c.dispatchEvent(new PointerEvent(t, { pointerType: 'touch', pointerId: 7, clientX: x, clientY: y, bubbles: true }));
      ev('pointerdown', x0, y0); for (let i = 1; i <= 10; i++) ev('pointermove', x0 + (x1 - x0) * i / 10, y0 + (y1 - y0) * i / 10); ev('pointerup', x1, y1); }, [q[0], q[1], q2[0], q2[1]]);
    await p.waitForTimeout(400); const fin = await state();
    must(fin.kind === 'own' && fin.computed > after.computed && Math.abs(fin.first3[0][0] - 5000) < 60 && Math.abs(fin.last1[0] - 7000) < 60, 'a made-up finger draws one too', fin.first3[0].map(v => v.toFixed(0)).join(', ') + ' to ' + fin.last1.map(v => v.toFixed(0)).join(', ')); }
  await p.click('#b-draw'); s = await state(); must(!s.draw, 'and drawing switches off again');

  // 8. played to its end without skipping: a short one
  await p.uncheck('#jag'); await p.click('#b-bow'); await p.waitForTimeout(200);
  { const from = await at((await state()).listener[0], 60), to = await at(700, 60); await p.mouse.move(from[0], from[1]); await p.mouse.down(); await p.mouse.move(to[0], to[1], { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(200); }
  await p.uncheck('#skip'); await p.click('#strike'); await p.waitForTimeout(300); s = await state();
  must(s.playing && s.offset === 0 && s.t < 1, 'without skipping, the clock starts at the flash', 't = ' + s.t.toFixed(2));
  await p.waitForTimeout(Math.ceil((s.last + 1.4) * 1000)); s = await state();
  must(!s.playing && s.ended >= 1 && Math.abs(s.t - (s.last + 0.6)) < 0.2, 'it plays to the end of the sound and stops by itself', 'stopped at ' + s.t.toFixed(2) + ' s; the sound ended at ' + s.last.toFixed(2));
  must(errs.length === 0, 'no script error in all of that', errs.join(' | ').slice(0, 300));

  // 9. narrow screens
  for (const w of [390, 320]) { await p.setViewportSize({ width: w, height: 800 }); await p.waitForTimeout(200);
    const over = await p.evaluate(() => document.scrollingElement.scrollWidth - window.innerWidth);
    must(over <= 0, 'at ' + w + ' wide nothing runs off the side', String(over));
    const v = await state(), bx = await box(), strip = (0 - v.view[2]) / (v.view[3] - v.view[2]) * bx.height, round = Math.abs((v.view[1] - v.view[0]) / bx.width - (v.view[3] - v.view[2]) / bx.height);
    must(strip >= 18 && round < 0.2, 'at ' + w + ' wide the ground has room for its lettering and the ring is still round', 'strip ' + strip.toFixed(1) + ' px; metres a pixel differ by ' + round.toFixed(3));
    if (w === 390) await p.screenshot({ path: path.join(out, 'thunder-390.png'), fullPage: true }); }
  console.log('PAGE TEST: ' + asserts + ' assertions, ' + fails.length + ' failed' + (fails.length ? ': ' + fails.join('; ') : ''));
  await b.close(); process.exit(fails.length ? 1 : 0);
})();
