# page-mutants.py -- can the page test fail?  Copies of the page with one thing broken in its own script (not in rcore.js), each
# built and run through tools/shot-rhyme.js in a headless browser.   python -I page-mutants.py
import subprocess, os, re
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); core = rd('rcore.js'); data = rd('data.json').replace('</', '<\\/')
M = [
 ('measure-ignored', "the first figure always draws the first measure", "var s = $('s1'), key = $('measure').value, i, p, g, v, cx, cy, placed = [];", "var s = $('s1'), key = 'M', i, p, g, v, cx, cy, placed = [];"),
 ('upside-down', "the first figure is drawn upside down", "function y1(v) { return T1 + (Y1 - v) / (Y1 - Y0) * (H1 - T1 - B1); }", "function y1(v) { return T1 + (v - Y0) / (Y1 - Y0) * (H1 - T1 - B1); }"),
 ('cell-next-poet', "a click on a cell chooses the poet next to it", "if (f === fam && p === poet2) choose2(-1, -1); else choose2(f, p); });", "if (f === fam && p === poet2) choose2(-1, -1); else choose2(f, Math.min(p + 1, 31)); });"),
 ('more-repeats', "Show more lists the first couplets again", "fill($('list2'), listIdx, shown, to); shown = to;", "fill($('list2'), listIdx, 0, to - shown); shown = to;"),
 ('nothing-marked', "the rhyme words are not marked in the lines", "if (!m) return esc(line); var at", "if (m) return esc(line); var at"),
 ('second-word-in-first-line', "each line has the other line's word looked for in it", "v.innerHTML = mark(D.lines[f[4]], f[2]) + '<br>' + mark(D.lines[f[5]], f[3]);", "v.innerHTML = mark(D.lines[f[4]], f[3]) + '<br>' + mark(D.lines[f[5]], f[2]);"),
 ('lines-swapped', "the two lines of a couplet are shown in the wrong order", "v.innerHTML = mark(D.lines[f[4]], f[2]) + '<br>' + mark(D.lines[f[5]], f[3]);", "v.innerHTML = mark(D.lines[f[5]], f[3]) + '<br>' + mark(D.lines[f[4]], f[2]);"),
 ('endings-swapped', "today's endings are given to the wrong words", "f[2] + ' ends “' + f[7] + '”, ' + f[3] + ' ends “' + f[8] + '”'", "f[2] + ' ends “' + f[8] + '”, ' + f[3] + ' ends “' + f[7] + '”'"),
 ('verdicts-swapped', "pairs that still rhyme are shown as failing, and the others as rhyming", "h('button', p.ok === 1 ? 'yes' : p.ok === 0 ? 'no' : 'unk')", "h('button', p.ok === 0 ? 'yes' : p.ok === 1 ? 'no' : 'unk')"),
 ('groups-left-out-of-table', "the table of the first figure leaves the groups out", "    D.groups.forEach(function (g) { t += '<tr><td>' + GROUPNAME[g.id] + '</td><td></td>", "    [].forEach(function (g) { t += '<tr><td>' + GROUPNAME[g.id] + '</td><td></td>"),
 ('tip-next-poet', "the pointer's note in the second figure gives the next poet's count", "esc(D.families[f].name) + '<br>' + D.families[f].byPoet[p] + ' of ' + R.group3(D.poets[p].evaluable)", "esc(D.families[f].name) + '<br>' + D.families[f].byPoet[Math.min(p + 1, 31)] + ' of ' + R.group3(D.poets[p].evaluable)"),
 ('american-for-british', "the line under the first figure gives the American share as the British", "R.pct(p.M_B) + '% in the British, ' + R.pct(p.M_A) + '% in the American, '", "R.pct(p.M_A) + '% in the British, ' + R.pct(p.M_B) + '% in the American, '"),
 ('second-figure-does-not-follow', "choosing a poet in the first figure leaves the second as it was", "if (i >= 0) { poet2 = i; $('poetSel2').value = String(i); draw2(); list2(); } }", "}"),
 ('family-select-dead', "the list of families does nothing", "$('famSel').addEventListener('change', function () { choose2(+this.value, poet2); });", ""),
 ('circles-of-first-family', "every row of the second figure draws the first family's circles", "r = rad(R.rate(D, f, p)); if (r > 0)", "r = rad(R.rate(D, 0, p)); if (r > 0)"),
 ('look-does-not-clean', "a word typed with a capital or a space is not found", "function look(word) { var w = R.clean(word),", "function look(word) { var w = String(word),"),
 ('table-columns-swapped', "the table of the first figure has the British and American columns the wrong way round", "'</td><td>' + R.pct(p.M_B) + '</td><td>' + R.pct(p.M_A) + '</td><td>' + R.pct(p.M_Along) + '</td></tr>'; });\n    D.groups", "'</td><td>' + R.pct(p.M_A) + '</td><td>' + R.pct(p.M_B) + '</td><td>' + R.pct(p.M_Along) + '</td></tr>'; });\n    D.groups"),
 ('forty-is-thirty', "a list shows thirty couplets where the page says forty", "shown = Math.min(40, listIdx.length);", "shown = Math.min(30, listIdx.length);"),
 ('pair-list-of-all', "choosing a failing partner lists every failing rhyme of the word, not the pair's", "fill(vl, R.failsOfPair(X, w, p.word), 0, 60);", "fill(vl, R.failsOf(D, X, -1, -1), 0, 60);"),
]
for name, what, a, b in M: assert src.count(a) == 1, name
os.makedirs(os.path.join(here, 'mutants', 'page'), exist_ok=True); env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu')); caught = 0
test = os.path.expanduser('~/web/shot-rhyme.js'); assert open(test, encoding='utf-8').read() == rd(os.path.join('tools', 'shot-rhyme.js')), 'the test in ~/web is not the copy in tools/'
def run(path): return subprocess.run(['node', test, path, os.path.join(here, 'mutants', 'page'), os.path.join(here, 'rcore.js'), os.path.join(here, 'data.json'), os.path.join(here, 'expect.json')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True, timeout=300)
# the control: the true page, built here in the same way and run by the same command, must pass
path = os.path.join(here, 'mutants', 'page', 'true.html'); open(path, 'w', encoding='utf-8').write(src.replace('/*CORE*/', core).replace('/*DATA*/[]', data)); r = run(path)
m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed', r.stdout); assert m and m.group(2) == '0', 'the true page does not pass by this runner: ' + (r.stdout[-300:] + r.stderr[-300:])
print('control: the true page, built and run in the same way: %s assertions, 0 failed\n' % m.group(1), flush=True); os.remove(path)
for name, what, a, b in M:
    path = os.path.join(here, 'mutants', 'page', name + '.html'); open(path, 'w', encoding='utf-8').write(src.replace(a, b).replace('/*CORE*/', core).replace('/*DATA*/[]', data))
    try:
        r = run(path)
        m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed(.*)', r.stdout)
        res = ('caught: %s of %s assertions fail%s' % (m.group(2), m.group(1), m.group(3)[:90])) if m and int(m.group(2)) > 0 else ('NOT caught: all %s assertions pass' % m.group(1)) if m else 'caught: the test stops with an error'
    except subprocess.TimeoutExpired: res = 'caught: the test does not finish'
    caught += res.startswith('caught'); print('%-30s %s -- %s' % (name, what, res), flush=True)
    os.remove(path)
print('\n%d of %d broken copies of the page caught' % (caught, len(M)))
