// Headless checks of the Mastermind-by-post page.   usage: node shot-post.js PAGE.html OUTDIR
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 900, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + page + '#lag=2&seed=7'); await p.evaluate(() => { window.__postFast = true; });
  // the book plays, at every lag and thirty codes each
  for (const lag of [0, 1, 2, 3, 4]) {
    let worst = 0, heardWorst = 0, bad = 0;
    for (let seed = 1; seed <= 30; seed++) {
      await p.evaluate(([lag, seed]) => { window.__post.start(lag, seed); window.__post.auto(); }, [lag, seed]);
      await p.waitForFunction(() => window.__post.game().heard(), null, { timeout: 5000 });
      const r = await p.evaluate(() => { const g = window.__post.game(); return { t: g.sentAt(), n: g.sent.length, say: window.__post.say() }; });
      worst = Math.max(worst, r.t); heardWorst = Math.max(heardWorst, r.n); if (r.n !== r.t + lag || !/was the code/.test(r.say)) bad++;
    }
    console.log(`lag ${lag}: thirty codes played by the book: sent by letter ${worst} at the latest, heard by letter ${heardWorst}; games where hearing was not sending plus the lag, or no verdict shown: ${bad}`);
  }
  // by hand: two book letters, then one the book would not post
  await p.evaluate(() => window.__post.start(2, 7));
  const h1 = await p.evaluate(() => window.__post.hint()); await p.click('#send');
  const h2 = await p.evaluate(() => window.__post.hint()); await p.click('#send');
  await p.keyboard.type('6666'); await p.keyboard.press('Enter'); await p.click('#hint');
  const off = await p.evaluate(() => ({ sent: window.__post.game().sent, say: window.__post.say() }));
  console.log('by hand:', JSON.stringify([h1, h2]), 'then 6666:', JSON.stringify(off));
  await p.check('#count'); await p.screenshot({ path: path.join(out, 'play-hand.png') });
  await p.evaluate(() => { window.__post.start(3, 11); window.__post.auto(); }); await p.waitForFunction(() => window.__post.game().heard(), null, { timeout: 5000 });
  await p.screenshot({ path: path.join(out, 'play-book.png'), fullPage: true });
  console.log('script errors:', JSON.stringify(errs)); await b.close();
})();
