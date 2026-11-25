// The chime's arithmetic, checked: the rows are an extent rung by lawful changes, the twelve hours use every row once and in order,
// noon and midnight come round, and the hour is struck the right number of times.   usage: node test.js
const Q = require('./core.js'); let ok = 0, bad = 0;
const check = (name, cond, detail) => { cond ? ok++ : bad++; console.log((cond ? 'PASS  ' : 'FAIL  ') + name + (detail !== undefined ? '   ' + detail : '')); };
const R = Q.ROWS;
check('120 rows, each an order of the five bells, no order twice, the first rounds', R.length === 120 && new Set(R.map(r => r.join(''))).size === 120 && R.every(r => r.slice().sort().join('') === '12345') && R[0].join('') === '12345');
const lawful = (a, b) => { let i = 0, moved = 0; while (i < 5) { if (a[i] === b[i]) i++; else if (i < 4 && a[i] === b[i + 1] && a[i + 1] === b[i]) { i += 2; moved++; } else return false; } return moved > 0; };
check('each row comes from the one before by swapping neighbours only, and the last goes back to rounds', R.every((r, i) => lawful(r, R[(i + 1) % 120])));
const seq = []; let strikes = [], lengths = [];
for (let h = 0; h < 12; h++) for (let q = 1; q <= 4; q++) { const c = Q.chime(h, q); seq.push(...c.rows); lengths.push(c.rows.length); if (q === 4) strikes.push(c.strikes); }
check('in twelve hours the 48 chimes ring rows 1 to 120 in order, each once', seq.length === 120 && seq.every((r, i) => r === i + 1));
check('a chime has as many rows as quarters have passed: 1, 2, 3, 4', lengths.every((n, i) => n === i % 4 + 1));
check('the hours struck are 1, 2, ... 12', strikes.join(',') === '1,2,3,4,5,6,7,8,9,10,11,12');
const noon = Q.at(12, 0), midnight = Q.at(0, 0), one = Q.at(13, 0), q1 = Q.at(12, 15), q3 = Q.at(23, 45);
check('twelve o\'clock, noon and midnight: rows 117 to 120, the last of them rounds, then twelve strokes', noon.rows.join(',') === '117,118,119,120' && midnight.rows.join(',') === noon.rows.join(',') && noon.strikes === 12 && midnight.strikes === 12 && R[120 % 120].join('') === '12345'
  && noon.notes.filter(n => n.row === 120).map(n => n.bell).join('') === '12345');
check('a quarter past twelve starts the extent again with row 1; one o\'clock strikes once; a quarter to midnight rings rows 114 to 116', q1.rows.join(',') === '1' && one.strikes === 1 && one.rows.join(',') === '7,8,9,10' && q3.rows.join(',') === '114,115,116' && q3.strikes === 0);
check('every hour from 0 to 23 and every quarter gives a chime of the right size', [...Array(24).keys()].every(h => [0, 15, 30, 45].every(m => { const c = Q.at(h, m); return c.rows.length === (m === 0 ? 4 : m / 15) && c.notes.filter(n => n.kind === 'bell').length === 5 * c.rows.length && c.strikes === (m === 0 ? (h % 12 || 12) : 0); })));
const c = Q.chime(11, 4), bells = c.notes.filter(n => n.kind === 'bell'), gaps = bells.slice(1).map((n, i) => +(n.t - bells[i].t).toFixed(4));
check('bells 0.42 s apart within a row and 1.26 s between rows; the first stroke of the hour 1.6 s after the last row\'s own time is up; strokes 2.2 s apart', gaps.every((g, i) => (i % 5 === 4 ? g === 1.26 : g === 0.42)) && +(c.notes.find(n => n.kind === 'hour').t - (bells[bells.length - 1].t + 0.42)).toFixed(4) === 1.6 && c.notes.filter(n => n.kind === 'hour').every((n, i, a) => i === 0 || +(n.t - a[i - 1].t).toFixed(4) === 2.2), gaps.slice(0, 6).join(' '));
check('the next boundary after 10:07:30 is 10:15:00, and after 10:15:00 exactly it is 10:30:00', Q.nextBoundary((10 * 60 + 7.5) * 60000) === (10 * 60 + 15) * 60000 && Q.nextBoundary((10 * 60 + 15) * 60000) === (10 * 60 + 30) * 60000);
console.log(`\n${ok} pass, ${bad} fail`); process.exit(bad ? 1 : 0);
