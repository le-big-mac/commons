"""test-remake9.py -- two mends to the page test after the last whole run of broken copies (page-mutants.out, 28 November): the page
is not changed.  tools/shot-gasket.js is changed in place, from out27/shot-gasket.stage9.js.txt to out27/shot-gasket.stage10.js.txt,
and copied to ~/web, where it is run.     python -I out27/test-remake9.py
  1. refusal-keeps-the-old-list passed: since a look says "Looking…" first, and clears the old list as it says so, the clearing that
     look() itself does is reached only through "Draw it above".  The test now refuses through that button with a list standing.
  2. common-divisor-let-through was caught only by the test stopping: the broken page threw inside its look and stood at "Looking…"
     for ever, and the test waited for the answer without end.  It now waits fifteen seconds and goes on, so that its assertions say
     what is wrong (and the page's error is among them)."""
import os, shutil
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); T = os.path.join(HERE, 'tools', 'shot-gasket.js')
def rep(s, a, b, n=1):
    assert s.count(a) == n, (s.count(a), a[:100]); return s.replace(a, b)
def main():
    s = open(T, encoding='utf-8').read()
    assert s == open(os.path.join(HERE, 'out27', 'shot-gasket.stage9.js.txt'), encoding='utf-8').read(), 'the test is not stage 9'
    s = rep(s, "await pg.waitForFunction(() => !/^Looking/.test(document.getElementById('tsay').textContent)); await pg.waitForTimeout(50); };", "await pg.waitForFunction(() => !/^Looking/.test(document.getElementById('tsay').textContent), null, { timeout: 15000 }).catch(() => 0); await pg.waitForTimeout(50); };      /* a look that never answers is left standing after fifteen seconds, for the assertions to find */")
    s = rep(s, "await p.press('#quad', 'Enter'); await p.waitForFunction(() => !/^Looking/.test(document.getElementById('tsay').textContent)); await p.waitForTimeout(80);", "await p.press('#quad', 'Enter'); await p.waitForFunction(() => !/^Looking/.test(document.getElementById('tsay').textContent), null, { timeout: 15000 }).catch(() => 0); await p.waitForTimeout(80);")
    s = rep(s, "    await fresh.fill('#quad', '1, 2, 3, 4'); await fresh.click('#show'); await fresh.waitForTimeout(400); const refused = (await F.state()).root, said = await F.text('#tsay');",
               "    const standing = [await btnShown(), (await F.text('#tnums')).length > 20]; await fresh.fill('#quad', '1, 2, 3, 4'); await fresh.click('#show'); await fresh.waitForTimeout(400); const refused = (await F.state()).root, said = await F.text('#tsay'), after = [await btnShown(), (await F.text('#tnums')).length];")
    s = rep(s, "must(drew === '-6,11,14,15' && refused === '-6,11,14,15' && said.includes('do not satisfy Descartes'),", "must(drew === '-6,11,14,15' && refused === '-6,11,14,15' && said.includes('do not satisfy Descartes') && standing[0] && standing[1] && !after[0] && after[1] === 0,")
    s = rep(s, "and with 1, 2, 3, 4 it says why not and draws nothing new (a visitor: it drew the gasket last looked at)'", "and with 1, 2, 3, 4 it says why not, draws nothing new, and takes away the list of the gasket before and its button, which were standing (a visitor: it drew the gasket last looked at; a planted fault that left the old list under the refusal passed, once a look through the other button had begun to clear it)'")
    open(T, 'w', encoding='utf-8').write(s); open(os.path.join(HERE, 'out27', 'shot-gasket.stage10.js.txt'), 'w', encoding='utf-8').write(s)
    shutil.copyfile(T, os.path.expanduser('~/web/shot-gasket.js')); print('tools/shot-gasket.js: stage 10,', s.count('must('), 'places where it asserts')
if __name__ == '__main__':
    main()
