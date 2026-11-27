"""test-remake8.py: assertions for the planted faults that the batch of 27 November did not catch.
 - notice-not-cleared: a refusal's notice left standing when coins are then chosen from the menu, a best set or the
   sentence over the tiles (the test had only cleared it by typing);
 - long-list-of-or: more than five equally good coins all listed with "or" (no coinage in the test had more than five).
 - counted-twice: the guard against a second count while one is pending, taken out. The test pressed the button twice,
   which the shut button already stops; the guard is what stops Enter in the range box, where the key begins a count
   and the browser then sends a "change" that would begin another.
python -I out27/test-remake8.py [FILE]   (after test-remake7.py; FILE is the test to change, tools/shot-change.js if not given)"""
import sys
if __name__ == '__main__':
    P = sys.argv[1] if len(sys.argv) > 1 else '/home/agent2/coin/tools/shot-change.js'; s = open(P, encoding='utf8').read()
    a = """    await setCoins('1, 5, 10, 25', 100); must((await text('#notice')) === '' && (await p.evaluate(() => getComputedStyle(document.querySelector('#notice')).display)) === 'none', 'a good entry clears the notice');
"""
    b = a + """    { const bad = async () => { await p.fill('#coins', '1, x, 5'); await p.click('#apply'); await settled(); return (await text('#notice')).includes('could not read'); };
      const off = async () => (await text('#notice')) === '' && (await p.evaluate(() => getComputedStyle(document.querySelector('#notice')).display)) === 'none';
      const b1 = await bad(); await p.selectOption('#preset', '2'); await settled(); const c1 = await off(), v1 = await p.inputValue('#coins');
      const b2 = await bad(); await p.click('#best-plain button[data-set="1,5,18,25"]'); await settled(); const c2 = await off(), v2 = await p.inputValue('#coins');
      const b3 = await bad(); await p.click('#story button'); await settled(); const c3 = await off(), v3 = await p.inputValue('#coins');
      must(b1 && c1 && b2 && c2 && b3 && c3 && v1 === '1, 2, 5, 10, 20, 50, 100, 200' && v2 === '1, 5, 18, 25' && v3 === '1, 5, 10, 25',
        "a refusal's notice goes when coins are then chosen some other way: from the menu, from a best set, from the sentence over the tiles (" + [b1, c1, b2, c2, b3, c3, v1, v2, v3].join(' | ') + ')');
      await setCoins('1, 5, 10, 25', 100); }
    { const c = [1, 2, 3, 4, 5, 6, 7, 8]; await setCoins(c.join(', '), 16); const sb = await text('#sayB');
      const ap = P.bestAdd(c, 16, 'plain', 15), ab = P.bestAdd(c, 16, 'both', 31), bp = ap.filter(e => e.total === ap[0].total).map(e => e.coin), bb = ab.filter(e => e.total === ab[0].total).map(e => e.coin);
      must(bp.join() === '9,10,11,12,13,14,15' && bb.join() === '9,10,11,12,13,14,15' && sb.includes('the best coin to add is 9, 10, 11, 12 or any of 3 others, bringing') && sb.includes('it is 9, 10, 11, 12 or any of 3 others, from') && !/ or \\d+ or \\d+ or /.test(sb) &&
        (await text('#addPlain')) === 'Add a 9: equal best with 6 others for paying exactly' && (await text('#addBoth')) === 'Add a 9: equal best with 6 others, of the coins tried, for paying with change',
        'seven equally good coins (coins 1 to 8, amounts to 15) are named as four of them "or any of 3 others", and on the buttons as "with 6 others" (a visitor met thirteen lines of "or"): ' + sb.slice(0, 160) + ' | ' + bp.join() + ' | ' + bb.join());
      await setCoins('1, 5, 10, 25', 100); }
    { const n0 = await p.evaluate(() => window.__coin.counts); await p.click('#L'); await p.fill('#L', '49'); await p.press('#L', 'Enter'); await settled(); await p.waitForTimeout(500);
      const st = await p.evaluate(() => [window.__coin.counts, window.__coin.L, document.getElementById('apply').textContent, ['coins', 'L'].some(id => document.getElementById(id).readOnly) || ['apply', 'preset', 'addPlain', 'addBoth'].some(id => document.getElementById(id).disabled), !!window.__coin.pending]);
      must(st[0] === n0 + 1 && st[1] === 50 && st[2] === 'Use these' && !st[3] && !st[4], 'Enter in the box for the range, which the browser follows with a "change" of its own, makes one count and leaves nothing shut (' + n0 + ' ' + JSON.stringify(st) + ')');
      if (!st[3]) await setCoins('1, 5, 10, 25', 100); }
"""
    assert s.count(a) == 1, s.count(a); s = s.replace(a, b); open(P, 'w', encoding='utf8').write(s); print('test: a notice cleared by the menu, a best set and the sentence')
