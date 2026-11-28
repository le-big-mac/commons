// Referee's driver: plays the page as a phone and at a desk and writes down what it prints.  node drive.js PAGE OUT.json
const { chromium } = require('playwright');
const fs = require('fs');
const QUADS = ['-11, 21, 24, 28', '-6, 11, 14, 15', '-23, 48, 49, 52', '-8, 12, 25, 25', '-12, 25, 25, 28', '-15, 24, 40, 49', '0, 0, 1, 1', '-12, 16, 49, 49',
  '-20, 36, 49, 49', '-16, 32, 33, 41', '-7, 8, 56, 57', '-16, 20, 81, 81', '-4, 8, 9, 9', '-7, 9, 32, 32', '-15, 32, 32, 33', '-15, 28, 33, 40', '-7, 12, 17, 20',
  '-5, 7, 18, 18', '-8, 13, 21, 24', '-3, 5, 8, 8', '-4, 5, 20, 21', '5, 20, 21, 96', '48, 49, 52, 321', '-2, 4, 4, 6', '1, 2, 3, 4', '4, -5, -20, -21', '-1, 2, 2, 3', '-2, 3, 6, 7', '-3, 4, 12, 13'];
const MILLION = ['-1, 2, 2, 3', '-23, 48, 49, 52', '-4, 8, 9, 9', '-16, 32, 33, 41', '-8, 12, 25, 25', '0, 0, 1, 1', '-7, 9, 32, 32'];
(async () => {
  const url = 'file://' + process.argv[2], out = { snaps: [], charts: [], taps: [], third: [], errs: [], misc: [] };
  const browser = await chromium.launch();
  for (const mode of ['phone', 'desk']) {
    const ctx = await browser.newContext(mode === 'phone' ? { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true } : { viewport: { width: 1100, height: 800 } });
    const p = await ctx.newPage(); p.on('pageerror', e => out.errs.push(mode + ': ' + String(e)));
    await p.goto(url); await p.waitForTimeout(600);
    const press = async sel => { if (mode === 'phone') await p.tap(sel); else await p.click(sel); await p.waitForTimeout(40); };
    const snap = async (extra) => Object.assign(await p.evaluate(() => { const GP = window.GasketPage, t = id => document.getElementById(id).textContent, pk = GP.pack();
      return { gsay: t('gsay'), gkind: t('gkind'), gstory: t('gstory'), gpick: t('gpick'), lead: t('lead'), swap: t('swap'), hiName: t('hiName'), view: GP.view(), size: GP.size(), root: pk.root, place: pk.place.circles, strip: !!pk.place.strip, drawn: GP.drawn(), leftOut: GP.leftOut(), chosen: GP.chosen(), menu: document.getElementById('pack').selectedOptions[0].textContent }; }), extra, { mode });
    out.misc.push({ mode, first: await snap({ kind: 'opening' }), body: await p.evaluate(() => document.querySelector('main').innerText), byline: await p.evaluate(() => { const e = document.querySelector('.noon-by'); return e ? e.innerText : null; }) });
    // ---- first picture: seven gaskets, seven lights, whole; then magnified by the page's own buttons
    for (let k = 0; k < 7; k++) {
      await p.selectOption('#pack', String(k)); await p.waitForTimeout(40);
      for (const h of ['none', '1', '2', '3', '6', 'q', 'five']) { await p.selectOption('#hi', h); await p.waitForTimeout(30); out.snaps.push(await snap({ kind: 'whole', pack: k, hi: h })); }
      for (const h of ['1', 'five', '6']) {
        await p.selectOption('#hi', h); await press('#home');
        for (let z = 1; z <= 4; z++) { await press('#zin'); out.snaps.push(await snap({ kind: 'magnify x' + z, pack: k, hi: h })); }
        await press('#mright'); out.snaps.push(await snap({ kind: 'magnify x4, right', pack: k, hi: h }));
        await press('#mup'); out.snaps.push(await snap({ kind: 'magnify x4, right, up', pack: k, hi: h }));
        await press('#zout'); out.snaps.push(await snap({ kind: 'then draw back once', pack: k, hi: h }));
        await press('#home'); await press('#zout'); out.snaps.push(await snap({ kind: 'whole, drawn back once', pack: k, hi: h }));
        await press('#home');
      }
    }
    // a deep look: squares in (-3,5,8,8) and (-4,5,20,21), Magnify thirty times
    for (const k of [0, 1]) { await p.selectOption('#pack', String(k)); await p.selectOption('#hi', '1'); await press('#home');
      for (let z = 1; z <= 30; z++) { await press('#zin'); if (z % 10 === 0) out.snaps.push(await snap({ kind: 'deep x' + z, pack: k, hi: '1' })); } await press('#home'); }
    // the lead sentence with another light, and the story after one Magnify
    await p.selectOption('#pack', '1'); await p.selectOption('#hi', 'five'); out.misc.push({ mode, what: 'lead with fives lit', lead: await p.textContent('#lead'), gsay: await p.textContent('#gsay'), hiName: await p.textContent('#hiName') });
    await p.selectOption('#hi', '1'); await press('#home'); await press('#zin'); await press('#zin'); out.misc.push({ mode, what: 'story after two Magnify', gstory: await p.textContent('#gstory'), gsay: await p.textContent('#gsay'), drawnB: (await p.evaluate(() => window.GasketPage.drawn().map(c => c[0]))).filter(b => b > 0 && Math.round(Math.sqrt(b)) ** 2 === b).sort((a, b) => a - b).slice(0, 6) });
    await press('#home');
    // ---- second picture
    for (let i = 0; i < 6; i++) {
      await p.selectOption('#cpack', String(i)); await p.waitForTimeout(80);
      const ch = await p.evaluate(() => { const GP = window.GasketPage, r = document.getElementById('chart').getBoundingClientRect(); return { marks: GP.marks(), strip: GP.strip(), csay: document.getElementById('csay').textContent, cpick: document.getElementById('cpick').textContent, name: document.getElementById('cpack').selectedOptions[0].textContent, rect: [r.left, r.top, r.width, r.height], texts: [...document.querySelectorAll('#chart text')].map(t => t.textContent), scrollY: window.scrollY }; });
      out.charts.push(Object.assign({ mode, i }, ch));
      // taps: in each row the first mark, the last, and three between; and one place with nothing
      const rows = ch.strip.rows.length, f = ch.rect[2] / ch.strip.W;
      for (let k = 0; k < rows; k++) { const ms = ch.marks.filter(m => m[1] === k); if (!ms.length) continue;
        const pickAt = [0, Math.floor(ms.length / 5), Math.floor(ms.length / 2), Math.floor(ms.length * 0.9), ms.length - 1];
        for (const j of pickAt) { const m = ms[j]; await p.evaluate(() => document.getElementById('chart').scrollIntoView({ block: 'center' })); await p.waitForTimeout(30);
          const r = await p.evaluate(() => { const r = document.getElementById('chart').getBoundingClientRect(); return [r.left, r.top]; });
          const x = r[0] + m[0] * f, y = r[1] + (ch.strip.top + k * ch.strip.row + 16) * f;
          if (mode === 'phone') await p.touchscreen.tap(x, y); else await p.mouse.click(x, y); await p.waitForTimeout(40);
          out.taps.push({ mode, i, row: k, rowName: ch.strip.rows[k], aimed: m[2], aimedX: m[0], line: await p.textContent('#cpick'), picked: await p.evaluate(() => window.GasketPage.strip().picked) }); } }
      await p.click('#ctab'); out.charts[out.charts.length - 1].table = await p.textContent('#ctable'); await p.click('#ctab');
    }
    // ---- third panel
    if (mode === 'desk') for (const N of ['100000', '1000000']) for (const q of (N === '100000' ? QUADS : MILLION)) {
      await p.fill('#quad', q); await p.selectOption('#upto', N); const t0 = Date.now(); await p.click('#try'); await p.waitForTimeout(150);
      out.third.push({ q, N: +N, ms: Date.now() - t0, tsay: await p.textContent('#tsay'), nums: await p.textContent('#tnums'), bold: await p.evaluate(() => [...document.querySelectorAll('#tnums b')].map(b => b.textContent)), showDisabled: await p.evaluate(() => document.getElementById('show').disabled), listBtn: await p.evaluate(() => { const b = document.getElementById('tlist'); return b.hidden ? null : b.textContent; }) }); }
    if (mode === 'phone') for (const q of ['-4, 8, 9, 9', '-23, 48, 49, 52']) { await p.fill('#quad', q); await p.tap('#try'); await p.waitForTimeout(300); out.third.push({ q, N: 100000, phone: true, tsay: await p.textContent('#tsay'), nums: await p.textContent('#tnums'), bold: await p.evaluate(() => [...document.querySelectorAll('#tnums b')].map(b => b.textContent)) }); }
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(process.argv[3], JSON.stringify(out));
  console.log('snaps', out.snaps.length, 'charts', out.charts.length, 'taps', out.taps.length, 'third', out.third.length, 'page errors', out.errs.length, out.errs.slice(0, 3));
})().catch(e => { console.error('DRIVER FAILED', e); process.exit(1); });
