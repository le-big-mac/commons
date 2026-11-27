const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const p = await ctx.newPage();
  const D = '/home/agent2/thunder/out/look4/';
  const out = []; const say = s => { out.push(s); fs.writeFileSync(D + 'a1.txt', out.join('\n')); };
  await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(700);
  await p.screenshot({ path: D + 'k1-first.png' });
  say('H ' + await p.evaluate(() => document.documentElement.scrollHeight) + ' W ' + await p.evaluate(() => document.documentElement.scrollWidth));
  say('=== FULL TEXT\n' + await p.evaluate(() => document.body.innerText));
  const controls = () => p.evaluate(() => [...document.querySelectorAll('button,input,canvas,label,a,summary,select')].filter(e => e.checkVisibility()).map(e => { const r = e.getBoundingClientRect(); let s = e, pin = ''; while (s && s !== document.body) { const q = getComputedStyle(s).position; if (q === 'sticky' || q === 'fixed') { pin = ' PINNED(' + s.tagName + '#' + s.id + ')'; break; } s = s.parentElement; } const li = e.closest('li'); const liI = li ? [...document.querySelectorAll('li')].indexOf(li) : -1; const x = r.left + r.width / 2, y = r.top + r.height / 2; const top = (y > 0 && y < innerHeight) ? document.elementFromPoint(x, y) : null; const ok = !!top && (top === e || e.contains(top) || (top.closest('label') === e)); return e.tagName + (e.id ? '#' + e.id : '') + ':"' + String(e.innerText || e.value || e.type || '').replace(/\n/g, ' ').slice(0, 42) + '" ' + Math.round(r.width) + 'x' + Math.round(r.height) + '@y' + Math.round(r.top) + (e.type === 'checkbox' ? ' checked=' + e.checked : '') + (liI >= 0 ? ' IN TIP ' + (liI + 1) : '') + pin + ((y > 0 && y < innerHeight) ? (ok ? ' reachable' : ' COVERED') : ' offscreen'); }).join('\n'));
  say('=== CONTROLS at top\n' + await controls());
  const pins = () => p.evaluate(() => [...document.querySelectorAll('*')].filter(e => { const s = getComputedStyle(e).position; return (s === 'sticky' || s === 'fixed') && e.checkVisibility(); }).map(e => { const r = e.getBoundingClientRect(); return e.tagName + '#' + e.id + ' ' + getComputedStyle(e).position + ' ' + Math.round(r.top) + '..' + Math.round(r.bottom); }).join(' ; '));
  say('=== PINNED at top: ' + await pins());
  say('=== TIPS: ' + await p.evaluate(() => [...document.querySelectorAll('li')].map((l, i) => { const r = l.getBoundingClientRect(); return (i + 1) + ' @' + Math.round(r.top + scrollY) + '..' + Math.round(r.bottom + scrollY); }).join(' , ')));
  for (const i of [0, 1, 2, 4]) {
    await p.evaluate(i => { const t = document.querySelectorAll('li')[i].getBoundingClientRect(); scrollBy(0, t.top - 600); }, i); await p.waitForTimeout(250);
    const pb = await p.evaluate(() => Math.max(0, ...[...document.querySelectorAll('*')].filter(e => { const s = getComputedStyle(e).position; return (s === 'sticky' || s === 'fixed') && e.checkVisibility(); }).map(e => e.getBoundingClientRect().bottom)));
    await p.evaluate(([i, pb]) => { const t = document.querySelectorAll('li')[i].getBoundingClientRect(); scrollBy(0, t.top - pb - 10); }, [i, pb]); await p.waitForTimeout(300);
    say('=== TIP ' + (i + 1) + ' under the pinned block: scrollY ' + Math.round(await p.evaluate(() => scrollY)) + ' | pinned: ' + await pins());
    say(await controls());
    await p.screenshot({ path: D + 'k2-tip' + (i + 1) + '-reading.png' });
  }
  await b.close();
})().catch(e => { console.log('ERR', e.message); process.exit(1); });
