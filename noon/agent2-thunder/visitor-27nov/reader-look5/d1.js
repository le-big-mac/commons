const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const p = await ctx.newPage(); const D = '/home/agent2/thunder/out/look5/';
  await p.goto('file:///home/agent2/thunder/thunder.html'); await p.waitForTimeout(700);
  await p.screenshot({ path: D + 'a-first-390.png' });
  console.log('H ' + await p.evaluate(() => document.documentElement.scrollHeight) + ' W ' + await p.evaluate(() => document.documentElement.scrollWidth));
  console.log('=== FULL TEXT\n' + await p.evaluate(() => document.body.innerText));
  console.log('=== PIN CHILDREN\n' + await p.evaluate(() => [...document.getElementById('pin').querySelectorAll('*')].map(e => { const r = e.getBoundingClientRect(); return e.tagName + (e.id ? '#' + e.id : '') + (e.className ? '.' + String(e.className).replace(/ /g, '.') : '') + ' ' + Math.round(r.left) + ',' + Math.round(r.top) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' font ' + getComputedStyle(e).fontSize + ' "' + (e.children.length ? '' : (e.innerText || '').slice(0, 80)) + '"'; }).join('\n')));
  console.log('=== CONTROLS\n' + await p.evaluate(() => [...document.querySelectorAll('button,input,canvas,label,a')].filter(e => e.checkVisibility()).map(e => { const r = e.getBoundingClientRect(); const li = e.closest('li'); return e.tagName + (e.id ? '#' + e.id : '') + ':"' + String(e.innerText || e.type || '').replace(/\n/g, ' ').slice(0, 40) + '" ' + Math.round(r.width) + 'x' + Math.round(r.height) + '@' + Math.round(r.left) + ',' + Math.round(r.top) + (li ? ' IN TIP ' + ([...document.querySelectorAll('li')].indexOf(li) + 1) : '') + (e.getAttribute('aria-pressed') ? ' aria-pressed=' + e.getAttribute('aria-pressed') : '') + (e.className ? ' class=' + e.className : ''); }).join('\n')));
  await b.close();
})().catch(e => { console.log('ERR', e.message); process.exit(1); });
