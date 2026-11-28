// live-drive.js -- the public page itself opened as a phone, after a push: first screen, a tap, the swap, Magnify, a tap on the strip, a look.
//      cd ~/web && node ~/gasket/out27/live-drive.js URL
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(), out = {}; const url = process.argv[2];
  for (const [w, h] of [[390, 844], [360, 640]]) { const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }), p = await ctx.newPage(), errs = []; p.on('pageerror', e => errs.push(String(e)));
    const resp = await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(900); const o = out[w + 'x' + h] = { status: resp.status() };
    const bot = id => p.evaluate(q => Math.round(document.getElementById(q).getBoundingClientRect().bottom), id), txt = id => p.evaluate(q => document.getElementById(q).textContent.replace(/\s+/g, ' ').trim(), id);
    o.line = await p.evaluate(() => { const l = document.querySelector('p.noon-by'); return l ? Math.round(l.getBoundingClientRect().height) : null; });
    o.wide = await p.evaluate(() => Math.max(document.documentElement.scrollWidth, innerWidth)); o.lead = await txt('lead'); o.bottoms = { picture: await bot('g'), tapLine: await bot('gpick'), swap: await bot('swap'), story: await bot('gstory') }; o.count = (await txt('gsay')).slice(0, 80);
    const st = await p.evaluate(() => { const GP = window.GasketPage, r = document.getElementById('g').getBoundingClientRect(), v = GP.view(), z = GP.size(), c = GP.drawn().filter(c => c[0] === 36)[0]; return [r.left + z.W / 2 + (c[1] / 36 - v.cx) * v.s, r.top + z.H / 2 - (c[2] / 36 - v.cy) * v.s]; });
    await p.touchscreen.tap(st[0], st[1]); await p.waitForTimeout(300); o.tapped = await txt('gpick'); await p.tap('#zin'); await p.waitForTimeout(300); o.magnified = (await txt('gsay')).slice(0, 90);
    await p.tap('#swap'); await p.waitForTimeout(400); o.swapped = [(await txt('gsay')).slice(0, 70), (await txt('gstory')).slice(0, 60), await txt('swap')];
    const g = await p.evaluate(() => { document.getElementById('chart').scrollIntoView({ block: 'center' }); const sv = document.getElementById('chart'), q = sv.querySelectorAll('path')[1].getBoundingClientRect(), r = sv.getBoundingClientRect(); return [r.left + r.width * 0.25, (q.top + q.bottom) / 2]; }); await p.waitForTimeout(300);
    const g2 = await p.evaluate(() => { const sv = document.getElementById('chart'), q = sv.querySelectorAll('path')[1].getBoundingClientRect(), r = sv.getBoundingClientRect(); return [r.left + r.width * 0.25, (q.top + q.bottom) / 2]; }); await p.touchscreen.tap(g2[0], g2[1]); await p.waitForTimeout(300); o.stripTap = await txt('cpick');
    await p.fill('#quad', '-4, 8, 9, 9'); await p.press('#quad', 'Enter'); await p.waitForFunction(() => !/^Looking/.test(document.getElementById('tsay').textContent), null, { timeout: 20000 }).catch(() => 0); o.look = (await txt('tsay')).slice(0, 130); o.errors = errs; await ctx.close(); }
  console.log(JSON.stringify(out, null, 1)); await b.close(); })();
