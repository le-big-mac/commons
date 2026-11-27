"""test-remake9.py: a test that stops must still say what it had found. Four planted faults were "caught" on 27 November
only by the test stopping (a button waited for that never opens), with the failed assertions lost.   python -I out27/test-remake9.py [FILE]   (after test-remake8.py)"""
import sys
if __name__ == '__main__':
    P = sys.argv[1] if len(sys.argv) > 1 else '/home/agent2/coin/tools/shot-change.js'; s = open(P, encoding='utf8').read()
    a = """  const fails = []; let asserts = 0; const must = (cond, what, ev) => { asserts++; if (!cond) fails.push(what + (ev ? '   [' + ev + ']' : '')); };
"""
    b = a + """  process.on('unhandledRejection', e => {                 /* a step that throws (a button waited for that never opens): say what was found before it, then stop */
    fails.forEach(f => console.log('FAILED: ' + f));
    console.log('THE TEST STOPPED after ' + asserts + ' assertions, ' + fails.length + ' of them failed; it stopped at: ' + String((e && e.message) || e).split('\\n')[0].slice(0, 160));
    b.close().catch(() => 0).then(() => process.exit(2)); });
"""
    assert s.count(a) == 1, s.count(a); s = s.replace(a, b); open(P, 'w', encoding='utf8').write(s); print('test: a stopped test prints what it had found')
