// test.js -- core.js against what the sources state and against what the theorems demand.   node --stack-size=20000 test.js
// Sources: ENX = Erickson, Nivasch, Xu, "Fusible numbers and Peano Arithmetic" (2022); Xu = "Survey on fusible numbers" (2012);
// NS = Nivasch and Shiboli, "Ordinals and recursively defined functions on the reals" (arXiv 2311.17210v6).
const F = require(process.env.CORE || './core.js'), P = require('./core-mapmemo.js'), fs = require('fs');
const f = new F.Fusible(), D = F.D, S = F.str, Q = F.parse, eq = (a, b) => F.cmp(a, b) === 0;
let pass = 0, fail = 0; const lines = [];
function ok(name, cond, detail) { if (cond) pass++; else fail++; lines.push((cond ? 'ok    ' : 'FAIL  ') + name + (detail ? '   [' + detail + ']' : '')); }
function all(name, n, bad, extra) { ok(name + ': ' + (n - bad.length) + ' of ' + n, bad.length === 0 && n > 0, (bad.length ? 'first failures: ' + bad.slice(0, 5).join('; ') : '') + (extra || '')); }
let seed = 20261124; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648, pow2 = e => D(1, e);

// ---- 1. the arithmetic, against plain BigInt fractions
{ const bad = []; let n = 0;
  for (let i = 0; i < 4000; i++) { const ea = Math.floor(rnd() * 40), eb = Math.floor(rnd() * 40), na = BigInt(Math.floor((rnd() - 0.5) * 2e9)), nb = BigInt(Math.floor((rnd() - 0.5) * 2e9));
    const a = D(na, ea), b = D(nb, eb), E = BigInt(Math.max(ea, eb)), A = na << (E - BigInt(ea)), B = nb << (E - BigInt(eb)); n++;
    const s = F.add(a, b), d = F.sub(a, b), fu = F.fuse(a, b);
    const same = (x, num, e) => (x[0] << (e - BigInt(x[1]))) === num;                    // x == num / 2^e, with e >= x[1]
    if (!(same(s, A + B, E) && same(d, A - B, E) && same(fu, A + B + (1n << E), E + 1n) && F.cmp(a, b) === (A < B ? -1 : A > B ? 1 : 0) && eq(Q(S(a)), a) && (a[1] === 0 || (a[0] & 1n) === 1n))) bad.push(S(a) + ' , ' + S(b)); }
  all('add, sub, cmp, fuse, parse and str agree with BigInt fractions on random pairs', n, bad); }

// ---- 2. what the sources state
ok('ENX: 0 ~ 0 = 1/2 and 0 ~ 1/2 = 3/4 (the 45 minutes of the riddle)', eq(F.fuse(F.ZERO, F.ZERO), D(1, 1)) && eq(F.fuse(F.ZERO, D(1, 1)), D(3, 2)));
{ const bad = []; let n = 0; for (let k = 0; k <= 40; k++) { const z = F.sub(F.UNIT, pow2(k)); n++; if (!(f.isFusible(z) && eq(f.succ(z), F.sub(F.UNIT, pow2(k + 1))))) bad.push(S(z)); }
  all('ENX: the fusible numbers below 1 are the numbers 1 - 2^-n (each is fusible and its successor is the next), n = 0..40', n, bad); }
{ const bad = []; let n = 0; for (let i = 0; i < 1024; i++) { const r = D(i, 10), is = f.isFusible(r); let want = false; for (let k = 0; k <= 10; k++) if (eq(r, F.sub(F.UNIT, pow2(k)))) want = true; n++; if (is !== want) bad.push(S(r)); }
  all('ENX: no other number k/1024 below 1 is fusible', n, bad); }
ok('Xu: m(1/2) = 1/4, m(3/4) = 1/8, m(1) = 1/8, m(2) = 1/1024 (by Algorithm 1)', eq(F.sub(f.succ(D(1, 1)), D(1, 1)), D(1, 2)) && eq(F.sub(f.succ(D(3, 2)), D(3, 2)), D(1, 3)) && eq(f.succ(F.UNIT), D(9, 3)) && eq(f.succ(D(2, 0)), Q('2049/1024')));
ok('Xu: 9/8 is fusible, as (0 ~ 0) ~ (0 ~ (0 ~ 0)); 17/16 is not', eq(F.fuse(F.fuse(F.ZERO, F.ZERO), F.fuse(F.ZERO, F.fuse(F.ZERO, F.ZERO))), D(9, 3)) && f.isFusible(D(9, 3)) && !f.isFusible(D(17, 4)));
ok('NS: M(1) = 1/8, M(3/2) = 1/32, M(2) = 2^-10, M(5/2) = 2^-31', eq(f.M(F.UNIT), D(1, 3)) && eq(f.M(D(3, 1)), D(1, 5)) && eq(f.M(D(2, 0)), pow2(10)) && eq(f.M(D(5, 1)), pow2(31)));
ok('ENX: M(0) = 1/2', eq(f.M(F.ZERO), D(1, 1)));
ok('ENX: the tame successor of 33/16 is 4225/2048; "the smallest wild fusible number that we know of is 8449/4096": Algorithm 1 gives it as the successor of 33/16, Algorithm 2 calls it fusible, and it is 19/16 ~ 3969/2048 with both of those fusible',
  eq(f.tameSucc(D(33, 4)), Q('4225/2048')) && eq(f.succ(D(33, 4)), Q('8449/4096')) && f.isFusible(Q('8449/4096')) && eq(F.fuse(D(19, 4), Q('3969/2048')), Q('8449/4096')) && f.isFusible(D(19, 4)) && f.isFusible(Q('3969/2048')));
ok('Xu: formula (1) gives m(31/16) = 2^-11 and m(33/16) = 2^-11, while 33/16 + 2^-12 is fusible', eq(f.M(D(31, 4)), pow2(11)) && eq(f.M(D(33, 4)), pow2(11)) && f.isFusible(F.add(D(33, 4), pow2(12))));
{ const g = ['0', '1/2', '1', '5/4', '3/2', '13/8', '7/4', '29/16', '15/8', '2', '129/64', '33/16'], bad = [];
  g.forEach((s, i) => { const a = Q(s); if (!(f.isFusible(a) && eq(F.sub(f.succ(a), a), pow2(i + 1)))) bad.push(s + ' gap ' + S(F.sub(f.succ(a), a))); });
  all('Xu: after the n-th of 0, 1/2, 1, 5/4, 3/2, 13/8, 7/4, 29/16, 15/8, 2, 129/64, 33/16 the next fusible number is 2^-n away (Algorithm 1)', g.length, bad); }
{ const want = [10, 31, 112, 503, 2786, 18443, 141744], bad = []; let c = 2; const cs = [2];
  for (let n = 1; n <= 7; n++) { if (n > 1) { c = 1 + n * c; cs.push(c); } let d = n + 9; for (let k = 1; k < n; k++) d += (k + 3) * cs[k]; const m = new F.Fusible().M(F.sub(D(3, 0), pow2(n - 1)));
    if (!(d === want[n - 1] && m[0] === 1n && m[1] === d)) bad.push('n = ' + n + ': formula ' + d + ', M ' + (m[0] === 1n ? '2^-' + m[1] : S(m))); }
  all('ENX: d(w^w^n) = n + 9 + 4 c_1 + ... + (n + 2) c_(n-1) is the exponent of M(3 - 2^-(n-1)), n = 1..7 (10, 31, 112, 503, 2786, 18443, 141744)', 7, bad); }
ok('Xu, table 1, row (3), and ENX section 7.2 by hand (v_2(1) = 51): the meek gap after 5/2 is 2^-51', eq(f.meekM(D(5, 1)), pow2(51)));
ok('ENX: Algorithm 6 as printed returns 1/2 for the input 1/2 (not a number greater than 1/2); as I read it, 3/4', (() => { try { f.meekSucc(D(1, 1), true); return false; } catch (e) { return /would return 1\/2$/.test(e.message); } })() && eq(f.meekSucc(D(1, 1)), D(3, 2)));
ok('ENX: 3 and 7 are fusible (Algorithm 3 returns them at once: n = (n - 1/2) ~ (n - 1/2))', eq(f.weakSucc(D(3, 0)), D(3, 0)) && eq(f.weakSucc(D(7, 0)), D(7, 0)));

// ---- 3. what the theorems demand, at many places.  The sample: random dyadics in [-1, 2.07) with denominators up to 2^24,
// every k/256 in [-1, 2.07), and for each of the first 600 of those its successor, the successor less 2^-30 and plus 2^-30.
const sample = []; for (let i = 0; i < 2500; i++) { const e = Math.floor(rnd() * 25); sample.push(D(Math.floor((rnd() * 3.07 - 1) * Math.pow(2, e)), e)); }
for (let i = -256; i < 530; i++) sample.push(D(i, 8));
for (let i = 0; i < 600; i++) { const z = f.succ(sample[i]); sample.push(z, F.sub(z, pow2(30)), F.add(z, pow2(30))); }
{ const b1 = [], b2 = [], b3 = [], b4 = [], b5 = [], b6 = []; let nf = 0;
  for (const r of sample) { const s = f.succ(r), w = f.weakSucc(r), t = f.tameSucc(r), k = f.meekSucc(r), isf = f.isFusible(r); if (isf) nf++;
    if (!(F.cmp(s, r) > 0 && f.isFusible(s))) b1.push(S(r));
    if (!eq(w, isf ? r : s)) b2.push(S(r));
    if (!(F.cmp(s, k) <= 0 && F.cmp(k, t) <= 0)) b3.push(S(r));
    if (!(eq(F.add(r, f.M(r)), r[0] < 0n ? F.ZERO : t) && eq(F.add(r, f.meekM(r)), r[0] < 0n ? F.ZERO : k))) b4.push(S(r));
    if (!(f.isFusible(t) && f.isFusible(k))) b5.push(S(r));
    const g = F.sub(f.succ(s), s); if (!(g[0] === 1n && g[1] === f.succ(s)[1] && eq(F.sub(f.succ(f.succ(s)), f.succ(s)), F.half(g)))) b6.push(S(s)); }
  const n = sample.length;
  all('Algorithm 1 returns a number greater than r that Algorithm 2 calls fusible', n, b1, nf + ' of the sample are themselves fusible');
  all('Algorithm 3 returns r when Algorithm 2 calls r fusible, and otherwise what Algorithm 1 returns', n, b2);
  all('general successor <= meek successor <= tame successor', n, b3);
  all('r + M(r) is the tame successor and r + meekM(r) the meek one (0 for negative r)', n, b4);
  all('tame and meek successors are fusible by Algorithm 2', n, b5);
  all('ENX Lemma 2.12 and Corollary 2.13: after a fusible z the gap is 1/Denominator(s(z)), and the next gap is half of it', n, b6); }
// closure: fuse pairs of numbers the program calls fusible; the result must be called fusible, and must not fall strictly
// between any r of the sample and the successor the program gave for r
{ const fus = []; for (const r of sample) { const s = f.succ(r); if (fus.length < 700) fus.push(s); }
  const made = []; const bad = []; let n = 0;
  for (let i = 0; i < 6000; i++) { const x = fus[Math.floor(rnd() * fus.length)], y = fus[Math.floor(rnd() * fus.length)], dxy = F.sub(x, y); if (F.cmp(dxy, F.UNIT) >= 0 || F.cmp(dxy, D(-1, 0)) <= 0) continue; const z = F.fuse(x, y); if (F.cmp(z, Q('17/8')) >= 0) continue; n++; made.push(z); if (!f.isFusible(z)) bad.push(S(x) + ' ~ ' + S(y)); }
  all('x ~ y is fusible by Algorithm 2 for pairs of successors less than 1 apart (results below 17/8)', n, bad);
  made.sort(F.cmp); const bad2 = []; let m = 0;
  for (const r of sample) { const s = f.succ(r); let a = 0, b = made.length; while (a < b) { const mid = (a + b) >> 1; if (F.cmp(made[mid], r) > 0) b = mid; else a = mid + 1; } if (a < made.length) { m++; if (F.cmp(made[a], s) < 0) bad2.push(S(r) + ': ' + S(made[a]) + ' < ' + S(s)); } }
  all('none of those fused numbers lies between an r of the sample and the successor Algorithm 1 gave for it', m, bad2); }
// every number below 17/8 made by trees of height at most 6, exhaustively
{ let level = [F.ZERO], seen = new Map([[F.key(F.ZERO), F.ZERO]]);
  for (let h = 1; h <= 6; h++) { const cur = Array.from(seen.values()); for (const x of cur) for (const y of cur) { const d = F.sub(x, y); if (F.cmp(d, F.UNIT) >= 0 || F.cmp(d, D(-1, 0)) <= 0) continue; const z = F.fuse(x, y); if (F.cmp(z, Q('17/8')) < 0 && !seen.has(F.key(z))) seen.set(F.key(z), z); } }
  const allz = Array.from(seen.values()).sort(F.cmp), bad = [], bad2 = []; for (const z of allz) if (!f.isFusible(z)) bad.push(S(z));
  all('every number below 17/8 made from 0 by trees of height at most 6 (never using a number of 17/8 or more) is fusible by Algorithm 2', allz.length, bad);
  let m = 0; for (const r of sample) { let a = 0, b = allz.length; while (a < b) { const mid = (a + b) >> 1; if (F.cmp(allz[mid], r) > 0) b = mid; else a = mid + 1; } if (a < allz.length) { m++; if (F.cmp(allz[a], f.succ(r)) < 0) bad2.push(S(r)); } }
  all('and none of them lies between an r of the sample and its successor by Algorithm 1', m, bad2); }

// ---- 4. the memory of gaps gives what a memory of single answers gives (core-mapmemo.js)
{ const p = new P.Fusible(), bad = [], badW = []; let n = 0; for (const r of sample) { if (F.cmp(r, D(2, 0)) >= 0) continue; n++; if (!eq(f.succ(r), p.succ(r))) bad.push(S(r)); if (!eq(f.weakSucc(r), p.weakSucc(r))) badW.push(S(r)); }
  all('Algorithm 1 with the memory of gaps = with a memory of single answers (the sample below 2)', n, bad); all('the same for Algorithm 3', n, badW); }

// ---- 5. against the sieve (sieve.js: closure on a grid, none of the paper's procedures), on the whole grid of 1/16384 below 35/16
{ const sieve = require('./sieve.js'), K = 14, top = 35 * (1 << K) / 16, sv = sieve(K, top), g = new F.Fusible();
  const miss = [], extra = []; let nf = 0; for (let i = 0; i < top; i++) { const is = g.isFusible(D(i, K)); if (is) nf++; if (sv.has[i] && !is) miss.push(i + '/16384'); if (!sv.has[i] && is) extra.push(i + '/16384'); }
  all('Algorithm 2 calls fusible every grid number the sieve made (' + sv.list.length + ' made)', sv.list.length, miss);
  all('and calls no other grid number fusible (' + nf + ' called fusible)', nf, extra);
  const above = [], differ = []; let offgrid = 0, same = 0, wildSame = 0, j = 0, n = 0;
  for (let i = 0; i < top; i++) { while (j < sv.list.length && sv.list[j] <= i) j++; if (j >= sv.list.length) break; n++; const r = D(i, K), z = g.succ(r), c = F.cmp(z, D(sv.list[j], K));
    if (c > 0) above.push(S(r)); else if (z[1] > K) offgrid++; else if (c === 0) { same++; if (!eq(z, g.tameSucc(r))) wildSame++; } else differ.push(S(r)); }
  all('Algorithm 1 never gives a successor greater than the next number the sieve made', n, above);
  all('and when its successor is on the grid it is that number (' + wildSame + ' of these where the tame successor is another number; at ' + offgrid + ' more points the successor is finer than the grid)', same, differ); }

// ---- 6. what the page adds: the certificate of a small gap, the columns of the picture, recipes, the two membership tests
for (const meek of [false, true]) { const full = new F.Fusible(), bad = []; let n = 0, exact = 0, small = 0;
  for (let i = 0; i < 3000; i++) { const e = Math.floor(rnd() * 22), r = D(Math.floor((rnd() * 3.4 - 1) * Math.pow(2, e)), e), p = Math.floor(rnd() * 40), truth = meek ? full.meekM(r) : full.M(r), g = new F.Fusible().gapOrSmall(r, p, 0, meek); n++;
    if (g === null) bad.push(S(r) + ' null'); else if (g.gap) { exact++; if (!eq(g.gap, truth)) bad.push(S(r) + ' p=' + p); } else { small++; if (!(g.small > p && F.cmp(truth, pow2(g.small)) <= 0)) bad.push(S(r) + ' p=' + p + ' small ' + g.small); } }
  all('gapOrSmall, ' + (meek ? 'meek' : 'tame') + ' rule: the exact gap where it gives one (' + exact + '), a true bound where it says "at most 2^-k" (' + small + '), at random dyadics in [-1, 2.4)', n, bad); }
{ const full = new F.Fusible(), g = new F.Fusible(), bad = []; let n = 0; const seen = [0, 0, 0, 0, 0];
  for (let i = 0; i < 2500; i++) { const p = 8 + Math.floor(rnd() * 33), a = D(Math.floor(rnd() * 2.3 * Math.pow(2, p)), p), lo = F.sub(a, pow2(p + 20)), w = pow2(p);
    const want = F.cmp(full.M(lo), w) < 0 ? 1 : F.cmp(full.meekM(lo), w) < 0 ? 2 : 0, got = g.column(a, p, 0); n++; seen[got]++; if (got !== want) bad.push(S(a) + ' p=' + p + ': ' + got + ' for ' + want); }
  all('column(): tame, wild only or empty as the full procedures say, at random columns below 2.3 with widths 2^-8 to 2^-40 (empty ' + seen[0] + ', tame ' + seen[1] + ', wild only ' + seen[2] + ')', n, bad); }
{ const g = new F.Fusible(), bad = [], badM = [], badT = []; let n = 0, nrec = 0, wild = 0;
  const verify = node => { const okm = new Map(); const go = nd => { const k = F.key(nd.v); if (okm.has(k)) return okm.get(k); let r; if (!nd.a) r = nd.v[0] === 0n; else { const d = F.sub(nd.a.v, nd.b.v); r = F.cmp(d, F.UNIT) < 0 && F.cmp(d, D(-1, 0)) > 0 && eq(F.fuse(nd.a.v, nd.b.v), nd.v) && go(nd.a) && go(nd.b); } okm.set(k, r); return r; }; return go(node); };
  for (let i = 0; i < 35 * 256; i++) { const r = D(i, 12), isf = g.isFusible(r), rec = g.recipe(r), t = g.tameSucc(r), k = g.meekSucc(r); n++; if (rec) nrec++;
    if (!!rec !== isf || (rec && !verify(rec)) || !g.recipe(k) || !verify(g.recipe(k))) bad.push(S(r)); if (g.isMeek(r) !== isf) badM.push(S(r));
    if (g.isTame(t) !== true) badT.push(S(t)); if (!eq(t, k)) { wild++; if (g.isTame(k) !== false) badT.push(S(k)); } }
  all('recipe(): one for a point of the grid of 1/4096 below 35/16 exactly when Algorithm 2 calls it fusible (' + nrec + '), one for every meek successor, and each checks from 0 up with fuses less than 1 apart', n, bad);
  all('isMeek() says what Algorithm 2 says on that grid', n, badM);
  all('isTame(): true of every tame successor on that grid, false of the ' + wild + ' meek successors that are not the tame successor', n, badT); }
{ const bad = []; let n = 0; for (const r of sample) { const z = f.succ(r); if (F.cmp(z, D(13, 3)) >= 0) continue; n++; if (!f.isFusible(F.add(z, D(1, 1)))) bad.push(S(z)); }
  all('z + 1/2 is fusible by Algorithm 2 for fusible z below 13/8 (what the picture relies on above 3)', n, bad); }

// ---- 7. added after the referee, who showed a wrong program these tests passed (the first procedure stepping y down by
// two units, wrong at 2175/1024 and at 29 points of the grid of 1/16384 below 35/16, where its successors are finer
// than the sieve's grid) and a rule no test reached (the half-unit rule of the picture)
{ const g = new F.Fusible(), bad = [], badR = []; let n = 0, same = 0;
  const verify = node => { const okm = new Map(); const go = nd => { const k = F.key(nd.v); if (okm.has(k)) return okm.get(k); let r; if (!nd.a) r = nd.v[0] === 0n; else { const d = F.sub(nd.a.v, nd.b.v); r = F.cmp(d, F.UNIT) < 0 && F.cmp(d, D(-1, 0)) > 0 && eq(F.fuse(nd.a.v, nd.b.v), nd.v) && go(nd.a) && go(nd.b); } okm.set(k, r); return r; }; return go(node); };
  const one = r => { const z = g.succ(r), k = g.meekSucc(r), rec = g.recipe(k); n++; if (!rec || !verify(rec)) badR.push(S(r)); if (F.cmp(z, k) > 0) bad.push(S(r) + ': ' + S(z) + ' > ' + S(k)); if (eq(z, k)) same++; };
  for (let i = 0; i < 35 * 1024; i++) one(D(i, 14));
  for (let i = 0; i < 1500; i++) { const e = 1 + Math.floor(rnd() * 24); one(D(Math.floor((2.07 + rnd() * 0.11) * Math.pow(2, e)), e)); }
  all('the meek successor has a recipe that checks, on the grid of 1/16384 below 35/16 and at 1,500 random dyadics in [2.07, 2.18)', n, badR);
  all('Algorithm 1 never gives a successor greater than that number, which is fusible for certain (equal to it at ' + same + ')', n, bad); }
{ const full = new F.Fusible(), g = new F.Fusible(), bad = []; g.belowFrom = F.UNIT; let n = 0; const seen = [0, 0, 0, 0, 0]; let greyTrue = 0, empties = 0;
  for (let i = 0; i < 2500; i++) { const p = 8 + Math.floor(rnd() * 33), a = D(Math.floor((1 + rnd() * 1.3) * Math.pow(2, p)), p), lo = F.sub(a, pow2(p + 20)), w = pow2(p);
    const tame = F.cmp(full.M(lo), w) < 0, meek = F.cmp(full.meekM(lo), w) < 0, got = g.column(a, p, 0); n++; seen[got]++; if (!meek) empties++;
    if (got === 3 ? !meek : got !== (tame ? 1 : meek ? 2 : 0)) bad.push(S(a) + ' p=' + p + ': ' + got); if (got === 3 && meek) greyTrue++; }
  all('the half-unit rule, tried from 1 upward where ' + empties + ' of the columns are empty: every column it paints grey (' + seen[3] + ') holds a meek number, and the rest are as the full procedures say', n, bad); }
ok('fractions are read in lowest terms (3/6, 6/12 and 5/10 are 1/2; 66/32 is 33/16), and 7/0, 1/3 and 2/6 are refused',
  eq(Q('3/6'), D(1, 1)) && eq(Q('6/12'), D(1, 1)) && eq(Q('5/10'), D(1, 1)) && eq(Q('66/32'), D(33, 4)) && ['7/0', '1/3', '2/6'].every(t => { try { Q(t); return false; } catch (e) { return true; } }));

fs.writeSync(1, lines.join('\n') + '\n\n' + pass + ' pass, ' + fail + ' fail\n'); process.exit(fail ? 1 : 0);
