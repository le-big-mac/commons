// node listentest.js <listen.html> <out-prefix>   — drives the listening page in a browser without a screen: data checks, the rendered sound against the timeline, and the game
const { chromium } = require('playwright');
(async () => {
  const [,, file, prefix] = process.argv; const url = 'file://' + require('path').resolve(file);
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  for (const w of [390, 900]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('requestfailed', r => errs.push('failed: ' + r.url().split('/').pop())); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    await p.goto(url); await p.waitForTimeout(300);
    if (w === 390) {
      // 1. the data
      const data = await p.evaluate(() => {
        const L = LISTEN, f = window.__listen.feet; let lines = 0, bad = [], passages = 0, badd = 0;
        const check = (ln, tag) => { lines++; const ft = f(ln.q); if (ft.length !== 6 || ln.q.length !== ln.w.length || [...ln.w].some(c => parseInt(c, 36) >= ln.t.length) || ft[5].length !== 2 || ln.q[0] !== 'L') bad.push(tag + ': ' + ln.t.join(' ')); return ft.slice(0, 4).filter(x => x.length === 3).length; };
        for (const poet of ['aen', 'arator']) { L.pool[poet].forEach((ps, i) => { passages++; const d = ps.lines.reduce((s, ln) => s + check(ln, poet + i), 0); if (d !== ps.d || ps.lines.length !== 8) badd++; });
          const dm = L.demo[poet]; const d = dm.lines.reduce((s, ln) => s + check(ln, 'demo'), 0); if (d !== dm.d) badd++; }
        for (const k in L.one) check(L.one[k], k);
        const keys = poet => new Set(L.pool[poet].map(ps => ps.book + '.' + ps.line)).size;
        return { lines, bad, passages, badd, distinct: [keys('aen'), keys('arator')], mean: ['aen', 'arator'].map(poet => L.pool[poet].reduce((s, ps) => s + ps.d, 0) / L.pool[poet].length) };
      });
      console.log('DATA: lines checked', data.lines, '; lines that are not six feet or have a bad word index:', data.bad.length, data.bad.slice(0, 3), '; passages', data.passages, '; passages whose stored count of dactyls differs from a recount:', data.badd, '; distinct passages (Virgil, Arator):', data.distinct, '; mean dactyls in a passage:', data.mean.map(x => x.toFixed(2)));
      // 2. the sound, rendered to numbers
      const snd = await p.evaluate(async () => {
        const T = window.__listen, sr = 44100, out = {};
        for (const [name, lines, u, thumps] of [['Virgil demo, normal speed, no taps', LISTEN.demo.aen.lines, 0.14, false], ['Arator demo, quick, no taps', LISTEN.demo.arator.lines, 0.11, false], ['Virgil demo, normal, with taps', LISTEN.demo.aen.lines, 0.14, true]]) {
          const tl = T.timeline(lines, u), c = new OfflineAudioContext(1, Math.ceil(sr * (tl.total + 0.5)), sr);
          T.schedule(c, c.destination, tl, 0.1, thumps); const buf = await c.startRendering(), x = buf.getChannelData(0);
          let peak = 0; for (let i = 0; i < x.length; i++) peak = Math.max(peak, Math.abs(x[i]));
          let worst = 0, quiet = 0, fl = [], fs = [], missing = 0;
          if (!thumps) for (const e of tl.ev) {
            const a = Math.round(sr * (0.1 + e.t)); let on = -1;
            for (let i = a - 300; i < a + 2000; i++) if (Math.abs(x[i]) > 0.01) { on = i; break; }     // first sample above a hundredth, looking from 7 ms before the note is due
            if (on < 0) { missing++; continue; }
            worst = Math.max(worst, Math.abs(on - a) / sr);
            let q = 0; for (let i = a - 400; i < a - 100; i++) q = Math.max(q, Math.abs(x[i])); quiet = Math.max(quiet, e.t > 0 ? q : 0);   // the gap before the note
            const i0 = a + Math.round(0.02 * sr), i1 = a + Math.round((e.dur - 0.035) * sr); let first = -1, last = -1, z = 0;      // pitch: upward crossings of zero, first to last
            for (let i = i0 + 1; i < i1; i++) if (x[i - 1] < 0 && x[i] >= 0) { if (first < 0) first = i; last = i; z++; }
            if (z > 1) (e.long ? fl : fs).push((z - 1) / ((last - first) / sr));
          }
          const avg = v => v.reduce((s, y) => s + y, 0) / (v.length || 1);
          out[name] = thumps ? { notes: tl.ev.length, seconds: +tl.total.toFixed(2), loudest_sample: +peak.toFixed(3) } : { notes: tl.ev.length, seconds: +tl.total.toFixed(2), loudest_sample: +peak.toFixed(3), notes_not_found: missing, latest_a_note_reaches_a_hundredth_ms: +(1000 * worst).toFixed(2), loudest_in_the_gap_before_a_note: +quiet.toFixed(4), pitch_of_longs_hz: +avg(fl).toFixed(1), pitch_of_shorts_hz: +avg(fs).toFixed(1) };
        }
        // the timeline itself: a line is 24 beats whatever its feet, and a long is two shorts
        const u = 0.14; let ok = 0, n = 0;
        for (const poet of ['aen', 'arator']) for (const ps of LISTEN.pool[poet]) for (const ln of ps.lines) { n++; const tl = T.timeline([ln], u); const last = tl.ev[tl.ev.length - 1]; if (Math.abs(last.t + last.dur - 24 * u) < 1e-9 && tl.ev.filter(e => e.first).every((e, i) => Math.abs(e.t - 4 * u * i) < 1e-9)) ok++; }
        out.lines_of_24_beats_with_feet_on_every_fourth = ok + ' of ' + n;
        { const c = new OfflineAudioContext(1, Math.ceil(sr * 0.25), sr); T.tap(c, c.destination, 0.01); const x = (await c.startRendering()).getChannelData(0), N = 8192; let lo = 0, hi = 0, peak = 0;      // one tap alone: the share of its energy above 300 Hz, by a plain Fourier sum
          for (let i = 0; i < x.length; i++) peak = Math.max(peak, Math.abs(x[i]));
          for (let kf = 1; kf < 1500; kf++) { let re = 0, im = 0; const w = 2 * Math.PI * kf / N; for (let i = 0; i < N; i++) { re += x[i] * Math.cos(w * i); im -= x[i] * Math.sin(w * i); } const e = re * re + im * im; if (kf * sr / N > 300) hi += e; else lo += e; }
          out.one_tap = { loudest_sample: +peak.toFixed(3), share_of_energy_above_300_hz_percent: +(100 * hi / (hi + lo)).toFixed(1) }; }
        return out;
      });
      console.log('SOUND:', JSON.stringify(snd, null, 1));
      // 3. the lights while a line plays, and the button that turns into Stop
      await p.click('button[data-one="light"]'); await p.waitForTimeout(700);
      const lit = await p.evaluate(() => ({ blocks: document.querySelectorAll('#st-paint .syl').length, on: document.querySelectorAll('#st-paint .syl.on').length, word: (document.querySelector('#st-paint .tx span.on') || {}).textContent, button: document.querySelector('button[data-one="light"]').textContent, no_sound_notices_hidden: [...document.querySelectorAll('.nosound')].every(e => e.hidden) }));
      await p.waitForTimeout(4500);
      const after = await p.evaluate(() => document.querySelectorAll('#st-paint .on').length + ' lit; button reads "' + document.querySelector('button[data-one="light"]').textContent + '"');
      console.log('LIGHTS: the horses line, 0.7 s in:', JSON.stringify(lit), '; after it ends:', after);
      await p.click('button[data-demo="arator"]'); await p.waitForTimeout(500); const d1 = await p.evaluate(() => document.querySelector('button[data-demo="arator"]').textContent + ' / lit ' + document.querySelectorAll('#st-demo .syl.on').length);
      await p.click('button[data-demo="arator"]'); await p.waitForTimeout(150); const d2 = await p.evaluate(() => document.querySelector('button[data-demo="arator"]').textContent + ' / lit ' + document.querySelectorAll('.on').length);
      console.log('STOP: eight lines of Arator, 0.5 s in: "' + d1 + '"; pressed again: "' + d2 + '"');
      // 4. the game: sixty rounds, guessing by the counter's rule on the count the page reveals only afterwards (read from the data here)
      let right = 0, n = 0, seen = { aen: new Set(), arator: new Set() }, repeats = 0, verdictOk = 0, focusOk = 0;
      for (let r = 0; r < 60; r++) {
        await p.click('#g-new'); await p.waitForTimeout(r < 2 ? 900 : 30);
        const now = await p.evaluate(() => ({ poet: window.__listen.G.now.poet, d: window.__listen.G.now.p.d, key: window.__listen.G.now.p.book + '.' + window.__listen.G.now.p.line, lamp: !document.getElementById('g-lamp').hidden, where: document.getElementById('g-where').textContent, focus: document.activeElement.id, stop: !document.getElementById('g-stop').hidden,
          leak: document.getElementById('game').textContent.match(/Aeneid|It was|dactyls in their/) ? 'yes' : 'no', words: document.querySelectorAll('#game .tx').length }));
        if (r === 0) {
          console.log('GAME: first round, 0.9 s in: lamp shown', now.lamp, '; "' + now.where + '"; focus on', now.focus, '; Stop shown', now.stop, '; anything in the panel that names the poet or shows words:', now.leak, now.words);
          await p.click('#g-again'); await p.waitForTimeout(400);
          console.log('GAME: "Play it again from the start" pressed while it plays: still sounding', await p.evaluate(() => document.getElementById('g-again').classList.contains('sounding')), '; "' + await p.evaluate(() => document.getElementById('g-where').textContent) + '"');
          await p.click('#g-stop'); await p.waitForTimeout(100);
          console.log('GAME: Stop pressed: sounding', await p.evaluate(() => document.getElementById('g-again').classList.contains('sounding')), '; Stop hidden', await p.evaluate(() => document.getElementById('g-stop').hidden), '; the question still shown', await p.evaluate(() => !document.getElementById('g-ask').hidden));
        }
        if (seen[now.poet].has(now.key)) repeats++; seen[now.poet].add(now.key);
        const say = now.d >= 16 ? 'arator' : 'aen'; await p.click(say === 'aen' ? '#g-v' : '#g-a'); n++; if (say === now.poet) right++;
        const v = await p.evaluate(() => document.querySelector('#g-out .verdict').textContent + ' | ' + document.getElementById('g-score').textContent + ' | rows ' + document.querySelectorAll('#g-show .ln').length + ' | focus ' + document.activeElement.id);
        if (v.startsWith(say === now.poet ? 'Right.' : 'No.') && v.includes('Right so far: ' + right + ' of ' + n + '.') && v.includes('rows 8')) verdictOk++;
        if (now.focus === 'g-again' && v.endsWith('focus g-new')) focusOk++;
        if (r === 0) console.log('GAME: first verdict:', v);
      }
      console.log('GAME: 60 rounds by the count rule: right', right, '; the page\'s verdict, score and eight shown lines agreed with the script in', verdictOk, 'rounds; the keyboard\'s place was kept in', focusOk, 'rounds; passages repeated:', repeats, '; Virgil rounds', seen.aen.size, ', Arator rounds', seen.arator.size);
      await p.selectOption('#speed', '0.11'); await p.click('#g-new'); await p.focus('#g-stop'); await p.waitForTimeout(26500);
      console.log('GAME: a mystery played to its end with the keyboard resting on Stop: focus now on', await p.evaluate(() => document.activeElement.id), '; Stop hidden', await p.evaluate(() => document.getElementById('g-stop').hidden));
      await p.click('#g-v'); await p.selectOption('#speed', '0.14');
      await p.check('#peek'); await p.click('#g-new'); await p.waitForTimeout(600);
      console.log('GAME: with "show the feet": rows drawn', await p.evaluate(() => document.querySelectorAll('#g-blind .ln').length), ', words shown', await p.evaluate(() => document.querySelectorAll('#g-blind .tx').length));
      await p.click('#g-a'); await p.click('#g-out button'); await p.waitForTimeout(500);
      console.log('GAME: "play it with the words": blocks lit', await p.evaluate(() => document.querySelectorAll('#g-show .syl.on').length), '; button reads "' + await p.evaluate(() => document.querySelector('#g-out button').textContent) + '"');
      await p.click('#g-out button'); await p.waitForTimeout(100);
    }
    await p.click('button[data-demo="aen"]'); await p.waitForTimeout(1500);
    const wide = await p.evaluate(() => [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 1 && !e.closest('.tablewrap')).map(e => e.tagName + ':' + (e.textContent || '').slice(0, 40)));
    await p.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
    await p.screenshot({ path: prefix + '-' + w + '.png', fullPage: true });
    console.log('PAGE at width', w, ': errors', JSON.stringify(errs), '; wider than the screen', JSON.stringify(wide.slice(0, 5)));
    await p.close();
  }
  {
    const p = await b.newPage({ viewport: { width: 390, height: 900 } }); await p.addInitScript(() => { window.AudioContext = undefined; window.webkitAudioContext = undefined; });
    await p.goto(url); await p.waitForTimeout(300); await p.click('button[data-one="spark"]'); await p.waitForTimeout(700);
    console.log('NO SOUND (a browser that cannot make any): notices shown', await p.evaluate(() => [...document.querySelectorAll('.nosound')].filter(e => !e.hidden).length), 'of 2', '; blocks lit', await p.evaluate(() => document.querySelectorAll('#st-spark .syl.on').length));
    await p.close();
    const q = await b.newPage({ viewport: { width: 390, height: 900 } }); await q.route('**/listen-data.js', r => r.abort());
    await q.goto(url); await q.waitForTimeout(300);
    console.log('NO DATA (the file of lines does not load): notice shown', await q.evaluate(() => !document.getElementById('nodata').hidden));
    await q.close();
  }
  await b.close();
})();
