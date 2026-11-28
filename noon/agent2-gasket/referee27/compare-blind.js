// compare-blind.js -- the referee's blind figures (blind-report.md, read as text) set beside what my own program gives
// (gcore.js, data.json).  Nothing here is typed from the report by hand: each figure is read out of its table by a pattern.
//      node compare-blind.js > compare-blind.out
const fs = require('fs'), path = require('path'); const HERE = __dirname, G = require(path.join(HERE, '..', 'gcore.js'));
const DATA = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'data.json'), 'utf8')), R = fs.readFileSync(path.join(HERE, 'blind-report.md'), 'utf8');
const SEVEN = [[-3, 5, 8, 8], [-4, 5, 20, 21], [-1, 2, 2, 3], [0, 0, 1, 1], [-3, 4, 12, 13], [-2, 3, 6, 7], [-23, 48, 49, 52]];
const name = q => '(' + q.join(',') + ')', esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); let n = 0, bad = 0;
const check = (ok, what, ev) => { n++; if (!ok) bad++; console.log((ok ? 'same     ' : 'DIFFERENT') + ' ' + what + (ev ? '   [' + ev + ']' : '')); };
const sect = k => { const a = R.indexOf('\n## ' + k + '.'), b = R.indexOf('\n## ', a + 5); return R.slice(a, b < 0 ? R.length : b); };
// 1. remainders
{ const S = sect(1); for (const q of SEVEN) { const m = new RegExp('\\| ' + esc(name(q)) + ' \\| ([\\d, ]+) \\|').exec(S); check(m && m[1].trim() === G.type(q).res.join(', '), '1. remainders of ' + name(q), (m && m[1].trim()) + ' against ' + G.type(q).res.join(', ')); } }
// 2 and 3. the forms up to a million
const EN = {}; for (const q of SEVEN) EN[name(q)] = G.enumerate(q, 1000000);
{ const S = sect(3), cells = {};
  for (const q of SEVEN) { const line = S.split('\n').filter(l => l.startsWith('| ' + name(q) + ' |'))[0], parts = line.split('|').slice(2, 6).map(x => x.trim()), res = G.type(q).res, en = EN[name(q)];
    [1, 2, 3, 6].forEach((u, k) => { let adm = 0, pres = 0; const abs = []; for (let i = 1; u * i * i <= 1000000; i++) { const v = u * i * i; if (!res.includes(v % 24)) continue; adm++; if (en.has(v)) pres++; else abs.push(v); }
      const m = /^(\d+): (\d+) \/ (\d+)(?: \(([\d, ]+)\))?/.exec(parts[k]), none = /none admissible/.test(parts[k]);
      const ok = none ? adm === 0 : m && +m[1] === adm && +m[2] === pres && +m[3] === abs.length && (!m[4] || m[4].split(',').map(x => +x).join() === abs.join());
      check(ok, '3. ' + name(q) + ', the form ' + (u === 1 ? '' : u) + 'n^2 up to a million: admissible, present, absent' + (m && m[4] ? ', and the absent ones by name' : ''), parts[k] + ' against ' + adm + ': ' + pres + ' / ' + abs.length + (abs.length && abs.length < 8 ? ' (' + abs.join(', ') + ')' : '')); }); }
  const en = EN['(-4,5,20,21)'], res = G.type([-4, 5, 20, 21]).res, abs = []; for (let i = 1; i * i <= 1000000; i++) if (res.includes((i * i) % 24) && !en.has(i * i)) abs.push(i * i);
  const m = /The seven absent ones are ([\d, ]+)\./.exec(sect(2)); check(m && m[1].split(',').map(x => +x).join() === abs.join(), '2. the squares with a fitting remainder that are absent from (-4,5,20,21) up to a million', (m && m[1]) + ' against ' + abs.join(', '));
  check(/36 is not a curvature/.test(sect(2)) && !EN['(-3,5,8,8)'].has(36) && en.has(36) && en.has(144) && en.has(1296), '2. 36 is in (-4,5,20,21), with 144 and 1296, and not in (-3,5,8,8)');
  let sqB = 0; for (let i = 1; i * i <= 1000000; i++) if (EN['(-3,5,8,8)'].has(i * i)) sqB++; check(sqB === 0 && /No perfect square is a curvature up to 10\^8/.test(sect(2)), '2. no square is in (-3,5,8,8), mine up to a million, the referee\'s up to 10^8', sqB + ' found by mine');
  for (const [q, word] of [[[-23, 48, 49, 52], 'none is a curvature'], [[0, 0, 1, 1], 'all are curvatures']]) { const e2 = EN[name(q)], cnt = [], hit = []; for (const u of [1, 4, 9, 36]) { let c = 0, h = 0; for (let i = 1; u * i ** 4 <= 1000000; i++) { c++; if (e2.has(u * i ** 4)) h++; } cnt.push(c); hit.push(h); }
    const m2 = new RegExp('\\| ' + esc(name(q)) + ' \\| 10\\^6 \\| (\\d+) \\| (\\d+) \\| (\\d+) \\| (\\d+) \\| ([a-z ]+) \\|').exec(S);
    check(m2 && [m2[1], m2[2], m2[3], m2[4]].join() === cnt.join() && m2[5] === word && (word.startsWith('none') ? hit.every(h => h === 0) : hit.join() === cnt.join()), '3. ' + name(q) + ', the fourth-power forms up to a million: how many of each, and whether they are there', (m2 && m2.slice(1).join(' ')) + ' against ' + cnt.join(' ') + ', present ' + hit.join(' ')); } }
// 4. the numbers of (-3,5,8,8) missing and in no family
{ const S = sect(4), d = DATA.filter(x => x.root.join() === '-3,5,8,8')[0], a = S.indexOf('\n60 69 72'), list = S.slice(a).trim().split(/\s+/).map(Number), mine = d.sporadic.filter(v => v <= 1000000);
  check(list.length === mine.length && list.every((v, i) => v === mine[i]), '4. the list up to a million, number for number', list.length + ' numbers, the last ' + list[list.length - 1] + ', against ' + mine.length + ', the last ' + mine[mine.length - 1]);
  const m = /seven more appear \(([\d, ]+)\)\. The total becomes \*\*(\d+)\*\* and the largest \*\*(\d+)\*\*/.exec(S), more = d.sporadic.filter(v => v > 1000000);
  check(m && m[1].split(',').map(x => +x).join() === more.join() && +m[2] === d.sporadic.length && +m[3] === d.sporadic[d.sporadic.length - 1] && /\*\*To 10\^8:\*\* none more/.test(S), '4. the seven beyond a million, the total and the last; none more up to 10^8', (m && m[2] + ', ' + m[3]) + ' against ' + d.sporadic.length + ', ' + d.sporadic[d.sporadic.length - 1]); }
// 5. circles by size: every circle whose curvature is at most the threshold, the enclosing circle among them
{ const S = sect(5);
  for (const t of [674.2, 788.5, 874.2, 1685.7]) { const row = S.split('\n').filter(l => l.startsWith('| ' + t + ' |'))[0].split('|').map(x => x.trim());
    [[-4, 5, 20, 21], [-3, 5, 8, 8]].forEach((q, k) => { const pl = G.place(q), c = pl.circles[0]; let cnt = 0, sq = 0; const which = {};
      G.inView(pl, { cx: c[1] / c[0], cy: c[2] / c[0], hw: 1, hh: 1 }, 1 / t, b => { if (b === 0) return; cnt++; if (b > 0 && G.isSquare(b)) { sq++; which[b] = (which[b] || 0) + 1; } }, 5000000);
      check(+row[2 + 2 * k] === cnt && parseInt(row[3 + 2 * k], 10) === sq, '5. ' + name(q) + ', circles of curvature at most ' + t + ', and the squares among them', row[2 + 2 * k] + ', ' + row[3 + 2 * k] + ' against ' + cnt + ', ' + sq + ' ' + JSON.stringify(which)); }); } }
// 6e. the paper's own table as the referee read it, against my six lists
{ const S = sect(6); for (const d of DATA) { const m = new RegExp('\\| ' + esc(name(d.root)) + ' \\| (\\d+) \\| (\\d+) \\|').exec(S); check(m && +m[1] === d.sporadic.length && +m[2] === d.sporadic[d.sporadic.length - 1], '6e. ' + name(d.root) + ': the size and the largest of the sporadic set in the paper\'s appendix, as the referee read them, against my list', (m && m[1] + ', ' + m[2]) + ' against ' + d.sporadic.length + ', ' + d.sporadic[d.sporadic.length - 1]); } }
// 6b. the families by the paper's table, as the referee worked the types out, against my program's
{ const S = sect(6); for (const q of SEVEN.slice(0, 6)) { const line = S.split('\n').filter(l => l.startsWith('| ' + name(q) + ' |') && /\(\d, ?\d+, ?[−-]?1/.test(l))[0], cell = line.split('|')[4].trim(), mine = (G.type(q).quad || []).map(u => (u === 1 ? '' : u) + 'n²').join(', ') || 'none';
    check(cell === mine, '6b. ' + name(q) + ': the families missing by the paper\'s table', cell + ' against ' + mine); } }
console.log('\n' + n + ' comparisons, ' + bad + ' different');
