"""test-remake8.py -- the page test for the ninth stage of the remake (out27/remake9.py), and for the referee's last broken copy that
passed (the Enter key in the box of four numbers) and its idea of another (a choice of "Look as far as" that looks elsewhere).
tools/shot-gasket.js is changed in place, from out27/shot-gasket.stage8.js.txt to out27/shot-gasket.stage9.js.txt, and copied to
~/web, where it is run.     python -I out27/test-remake8.py"""
import os, shutil
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); T = os.path.join(HERE, 'tools', 'shot-gasket.js')
def rep(s, a, b, n=1):
    assert s.count(a) == n, (s.count(a), a[:100]); return s.replace(a, b)
def main():
    s = open(T, encoding='utf-8').read()
    assert s == open(os.path.join(HERE, 'out27', 'shot-gasket.stage8.js.txt'), encoding='utf-8').read(), 'the test is not stage 8'
    # ---- nothing in the picture: the line under the picture says so; the count does not say "0 of them"
    s = rep(s, "/drawn, and it is /.test(t) ? (m[3] ? 0 : 1) : -1] : [-1, -1]; };", "/drawn, and it is /.test(t) ? (m[3] ? 0 : 1) : m[1] === '0' ? 0 : -1] : [-1, -1]; };")
    s = rep(s, "const sc2 = await F.state(), saidC = await F.text('#gsay');", "const sc2 = await F.state(), saidC = await F.text('#gsay'), pickC = await F.text('#gpick');")
    s = rep(s, "&& saidC.includes(': 0 circles drawn') && saidC.includes('Nothing of the gasket is in view: “The whole gasket” brings it back.'),", "&& saidC.includes(': 0 circles drawn. Not magnified. Nothing of the gasket is in view: “The whole gasket” brings it back.') && pickC === 'Nothing of the gasket is in view: “The whole gasket” brings it back.',")
    s = rep(s, "the count is of no circles, and the page says how to bring the gasket back (a referee:", "the count is of no circles, with no word of how many of none are lit, and the line directly under the picture says how to bring the gasket back, as the count does (a visitor: under the empty picture the line still read \"Tap a circle\"; a referee:")
    # ---- the third panel
    s = rep(s, "'In this gasket no fourth powers are ruled out. The page finds that by looking: '", "'In this gasket the fourth powers are not ruled out, nor 4, 9 or 36 times a fourth power. The page finds that by looking: '")
    s = rep(s, "    const turned = []; for (const [q, want] of [['4, -5, -20, -21',",
               "    // the kind with two pairs of fourth-power forms, looked at only as far as 10,000, where neither pair shows: the page does not know which is ruled out, and says so of its count\n"
               "    { const opts = await p.evaluate(() => [...document.getElementById('upto').options].map(o => [o.value, o.textContent])); await p.selectOption('#upto', { label: '10,000' }); await p.fill('#quad', '-39, 57, 128, 128'); await tryLook(p); const t5 = await text('#tsay'); await p.selectOption('#upto', '100000');\n"
               "      const r5 = [-39, 57, 128, 128], ty = G.type(r5), en5 = G.enumerate(r5, 10000), miss5 = G.missing(r5, 10000, en5), in5 = miss5.filter(v => G.inFamily(v, ty.quad)).length, any4 = [1, 4, 9, 36].some(u => { for (let n = 1; u * n ** 4 <= 10000; n++) if (en5.has(u * n ** 4)) return true; return false; });\n"
               "      must(opts.length === 3 && opts.every(o => grp(+o[0]) === o[1]) && (-39 + 57 + 128 + 128) ** 2 === 2 * (39 * 39 + 57 * 57 + 2 * 128 * 128) && ty.quartic && ty.k !== 1 && !any4 && t5.includes('up to 10,000 it finds none.') && t5.includes('circles with a number up to 10,000: ' + grp(miss5.length) + ' numbers that pass the test are missing, ' + grp(in5) + ' of them in the families ruled out (marked with an orange square) and ' + grp(miss5.length - in5) + ' not, or not known to be.'),\n"
               "        'each choice of \"Look as far as\" looks as far as it says; and for (−39, 57, 128, 128) looked at as far as 10,000, where none of the fourth-power forms is on a circle, the page says it has found none and that the missing numbers outside the families of squares are \"not, or not known to be\" in a family ruled out (a referee: one pair of fourth-power forms is ruled out there whichever it is, so \"2,183 not\" was more than the page knew)', t5.slice(-230)); }\n"
               "    await p.fill('#quad', '-6, 11, 14, 15'); await p.press('#quad', 'Enter'); await p.waitForFunction(() => !/^Looking/.test(document.getElementById('tsay').textContent)); await p.waitForTimeout(80); const entered = await text('#tsay');\n"
               "    must(entered.startsWith('(−6, 11, 14, 15) are the four largest circles of their gasket.'), 'the Enter key in the box of four numbers starts a look, as the button does (a referee\\'s broken copy in which it did nothing passed)', entered.slice(0, 70));\n"
               "    const turned = []; for (const [q, want] of [['4, -5, -20, -21',")
    open(T, 'w', encoding='utf-8').write(s); open(os.path.join(HERE, 'out27', 'shot-gasket.stage9.js.txt'), 'w', encoding='utf-8').write(s)
    shutil.copyfile(T, os.path.expanduser('~/web/shot-gasket.js')); print('tools/shot-gasket.js: stage 9,', s.count('must('), 'places where it asserts')
if __name__ == '__main__':
    main()
