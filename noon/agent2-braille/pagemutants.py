"""pagemutants.py: the page broken on purpose, one fault at a time, and pagetest.js run on each broken copy.
    /usr/bin/python3 -I pagemutants.py     (a control run of the true page first; it must pass)"""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ENV = dict(os.environ, NODE_PATH=os.path.expanduser('~/web/node_modules'), LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'))
M = [
 ('a sentence\'s count gives the cells saved as one more', "(p.U - p.C) + ' saved, which is '", "(p.U - p.C + 1) + ' saved, which is '"),
 ('the percentage is of the contracted cells', "pct(1 - p.C / p.U) + '.'", "pct(p.U / p.C - 1) + '.'"),
 ('the second sentence shows the first', "b.addEventListener('click', function () { show(i); });", "b.addEventListener('click', function () { show(0); });"),
 ('every button is marked pressed', "b.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });", "b.setAttribute('aria-pressed', 'true'); });"),
 ('the marking cannot be put off', "var on = $('passage').classList.toggle('marks');", "var on = true;"),
 ('the braille under a word is the next word\'s', "b.textContent = w.braille;", "b.textContent = (p.words[(p.words.indexOf(w) + 1) % p.words.length]).braille;"),
 ('a higher share is drawn lower', "y = function (s) { return Y1 - (Y1 - Y0) * (s - lo) / (hi - lo); };", "y = function (s) { return Y0 + (Y1 - Y0) * (s - lo) / (hi - lo); };"),
 ('the years run backwards', "var x = function (y) { return X0 + (X1 - X0) * (y - yr0) / (yr1 - yr0); }", "var x = function (y) { return X1 - (X1 - X0) * (y - yr0) / (yr1 - yr0); }"),
 ('the dots\' shares are printed to one place', "var label = b.title + ', ' + b.year + ': ' + pct(b.s, 2)", "var label = b.title + ', ' + b.year + ': ' + pct(b.s, 1)"),
 ('the scale stops short, so the highest dot leaves the frame', "lo = 0.205, hi = 0.262", "lo = 0.205, hi = 0.243"),
 ('the means are of the first two eras only', "var s = DATA.mean[m[0]];", "var s = DATA.mean[m[0] === '3' ? '2' : m[0]];"),
 ('the Bible is drawn as a dot among the novels', "if (b.era === 0) return;", ""),
 ('the hover label is not kept inside the picture', "tip.style.left = Math.max(0, Math.min(f.width - w, px - w / 2)) + 'px';", "tip.style.left = (px - w / 2) + 'px';"),
 ('a dot reached by the keyboard shows nothing', "c.addEventListener('focus', on);", ""),
 ('the table leaves the Bible out', "tr.children[1].textContent = kjv.title; tr.children[2].textContent = pct(kjv.s, 2); $('booktable').tBodies[0].appendChild(tr);", "tr.children[1].textContent = kjv.title; tr.children[2].textContent = pct(kjv.s, 2);"),
 ('then and now are exchanged in the bars', "[['then', s.then], ['now', s.now]].forEach(", "[['then', s.now], ['now', s.then]].forEach("),
 ('each column of bars has a scale of its own', "b.style.width = (78 * t[1] / top) + '%';", "b.style.width = (78 * t[1] / Math.max.apply(null, list.map(function (q) { return Math.max(q.then, q.now); }))) + '%';"),
 ('the bars are all one length', "b.style.width = (78 * t[1] / top) + '%';", "b.style.width = '40%';"),
 ('the losers are listed under "Gained"', "bars(DATA.losers, 'losers'); bars(DATA.gainers, 'gainers');", "bars(DATA.losers, 'gainers'); bars(DATA.gainers, 'losers');"),
 ('an added text is given the next one\'s figure', "tr.children[2].textContent = pct(a.L, 2); $('added').tBodies[0].appendChild(tr);", "tr.children[2].textContent = pct(a.L + 0.001, 2); $('added').tBodies[0].appendChild(tr);"),
 ('the page says two of the six predictions held', "(DATA.held3[0] === 1 ? 'One' : DATA.held3[0])", "(DATA.held3[0] === 1 ? 'Two' : DATA.held3[0])"),
 ('the means of the first and last six are exchanged in the table', "L: DATA.sixL.first }].concat(", "L: DATA.sixL.last }].concat("),
 ('speech and narration are exchanged', "[['Narration (outside quotation marks)', DATA.speech.out], ['Speech (inside them)', DATA.speech.ins]", "[['Narration (outside quotation marks)', DATA.speech.ins], ['Speech (inside them)', DATA.speech.out]"),
 ('the signs that never occur are those of the middle six', "DATA.never['3'].join(', ') + '.';", "DATA.never['2'].join(', ') + '.';"),
 ('a wide passage that cannot wrap', "#passage { display: flex; flex-wrap: wrap;", "#passage { display: flex; flex-wrap: nowrap;"),
 ('the three largest signs are given with now first', "Math.round(s.then).toLocaleString('en-GB') + ' to ' + Math.round(s.now).toLocaleString('en-GB') + ')'; }).join(', ')", "Math.round(s.now).toLocaleString('en-GB') + ' to ' + Math.round(s.then).toLocaleString('en-GB') + ')'; }).join(', ')"),
]
def run(page):
    with tempfile.TemporaryDirectory(dir=HERE) as t:
        f = os.path.join(t, 'braille.html'); open(f, 'w', encoding='utf-8').write(page)
        r = subprocess.run(['node', os.path.join(HERE, 'pagetest.js'), f], env=ENV, capture_output=True, text=True, timeout=300)
        return r.returncode, [l for l in r.stdout.splitlines() if l.startswith('FAILED')], r.stderr.strip().splitlines()[-1:]
if __name__ == '__main__':
    true = open(os.path.join(HERE, 'braille.html'), encoding='utf-8').read()
    code, fails, err = run(true); print('control (the true page): %s' % ('passes' if code == 0 else 'FAILS %s %s' % (fails, err))); assert code == 0
    caught = 0
    for what, a, b in M:
        assert true.count(a) == 1, 'this fault does not find its text exactly once: ' + what
        code, fails, err = run(true.replace(a, b)); caught += code != 0
        print('%-62s %s' % (what, ('caught: ' + (fails[0][8:86] if fails else 'the test stopped: ' + ' '.join(err)[:60])) if code else 'PASSED, not caught'))
    print('%d of %d broken copies caught' % (caught, len(M)))
