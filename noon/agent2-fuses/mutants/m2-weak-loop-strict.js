// core.js -- fusible numbers, after J. Erickson, G. Nivasch and J. Xu, "Fusible numbers and Peano Arithmetic" (Logical
// Methods in Computer Science 18(3), 2022).  A fuse burns for exactly one unit of time, at an uneven rate.  Light its two
// ends at times x and y, less than a unit apart, and it is gone at x ~ y = (x + y + 1)/2.  0 is fusible, and x ~ y is
// fusible whenever x and y are.  Every fusible number is a dyadic rational, so everything here is exact: a number is
// held as [n, e], meaning n / 2^e, with n a BigInt and odd unless the number is a whole one (then e = 0).
// The five procedures are the paper's Algorithms 1, 3, 2, 4, 5 and 6, written as they stand there, with a memory.
(function (root) {
  'use strict';
  var Z = 0n, ONE = 1n, TWO = 2n;
  function norm(n, e) { if (n === Z) return [Z, 0]; while (e > 0 && (n & ONE) === Z) { n >>= ONE; e--; } return [n, e]; }
  function D(n, e) { return norm(BigInt(n), e || 0); }                       // D(3, 2) is 3/4
  function lift(a, e) { return a[0] << BigInt(e - a[1]); }                   // numerator of a over 2^e, for e >= a[1]
  function add(a, b) { var e = Math.max(a[1], b[1]); return norm(lift(a, e) + lift(b, e), e); }
  function sub(a, b) { var e = Math.max(a[1], b[1]); return norm(lift(a, e) - lift(b, e), e); }
  function cmp(a, b) { var e = Math.max(a[1], b[1]), d = lift(a, e) - lift(b, e); return d < Z ? -1 : d > Z ? 1 : 0; }
  function half(a) { return norm(a[0], a[1] + 1); }
  function dbl(a) { return a[1] > 0 ? [a[0], a[1] - 1] : [a[0] * TWO, 0]; }
  function neg(a) { return [-a[0], a[1]]; }
  function isNeg(a) { return a[0] < Z; }
  function key(a) { return a[0].toString(36) + '/' + a[1]; }
  function str(a) { return a[1] === 0 ? a[0].toString() : a[0].toString() + '/' + (ONE << BigInt(a[1])).toString(); }
  function num(a) { if (a[1] < 1000) return Number(a[0]) / Math.pow(2, a[1]); var s = a[1] - 900; return Number(a[0] >> BigInt(s)) / Math.pow(2, 900); }
  var ZERO = [Z, 0], UNIT = [ONE, 0], HALF = [ONE, 1];
  function fuse(x, y) { return half(add(add(x, y), UNIT)); }                 // x ~ y
  function ulp(a) { return [ONE, a[1]]; }                                    // 1 / Denominator(a)
  function parse(s) { var p = String(s).split('/'); if (p.length === 1) return D(p[0], 0); var q = BigInt(p[1]), e = 0; while (q > ONE) { if (q & ONE) throw new Error('not a dyadic fraction: ' + s); q >>= ONE; e++; } return norm(BigInt(p[0]), e); }

  // A memory of answers already found.  One Map holds at most 2^24 entries, so this is a row of Maps of eight million each;
  // when there are more than `cap` of them the oldest is dropped (dropped counts them).  An answer forgotten is found again,
  // so dropping changes how long a run takes and nothing else.
  function Memo(cap) { this.maps = [new Map()]; this.cap = cap || 12; this.dropped = 0; }
  Memo.prototype.get = function (k) { for (var i = this.maps.length - 1, v; i >= 0; i--) { v = this.maps[i].get(k); if (v !== undefined) return v; } };
  Memo.prototype.set = function (k, v) { var m = this.maps[this.maps.length - 1]; if (m.size >= 8000000) { m = new Map(); this.maps.push(m); if (this.maps.length > this.cap) { this.maps.shift(); this.dropped++; } } m.set(k, v); };
  Memo.prototype.count = function () { var n = 0; this.maps.forEach(function (m) { n += m.size; }); return n; };

  // A second kind of memory, for the two general procedures.  If the smallest fusible number above t is z, it is also the
  // smallest above every number in [t, z), whatever those are.  So answers are kept as gaps: z with the least t known to
  // have z as its answer, in order of z, and a question is answered by the first z above it if that gap reaches down far
  // enough.  (strict = false is the same for "greater than or equal": the gap is then closed at z.)
  function Gaps(strict) { this.z = []; this.lo = []; this.strict = strict; }
  Gaps.prototype.find = function (t) { var a = 0, b = this.z.length, m, c; while (a < b) { m = (a + b) >> 1; c = cmp(this.z[m], t); if (this.strict ? c > 0 : c >= 0) b = m; else a = m + 1; } return a; };
  Gaps.prototype.get = function (t) { var i = this.find(t); if (i < this.z.length && cmp(this.lo[i], t) <= 0) return this.z[i]; };
  Gaps.prototype.set = function (t, z) { var i = this.find(t); if (i < this.z.length && cmp(this.z[i], z) === 0) { if (cmp(t, this.lo[i]) < 0) this.lo[i] = t; } else { this.z.splice(i, 0, z); this.lo.splice(i, 0, t); } };
  Gaps.prototype.count = function () { return this.z.length; };

  function Fusible(cap) { this.gS = new Gaps(true); this.gW = new Gaps(false); this.mS = new Memo(cap); this.mW = new Memo(cap); this.mT = new Memo(cap); this.mM = new Memo(cap); this.mK = new Memo(cap); this.mK2 = new Memo(cap); this.mKM = new Memo(cap); this.calls = { succ: 0, weak: 0, tame: 0, m: 0, meek: 0, meekM: 0 }; this.depthM = 0; this.depthK = 0; }
  // Algorithm 1: the smallest fusible number greater than r
  Fusible.prototype.succ = function (r) {
    if (isNeg(r)) return ZERO;
    var got = this.gS.get(r); if (got) return got; this.calls.succ++;
    var min = null, y = r, x, z, r2 = dbl(r), lim = sub(r, HALF);
    do {
      x = this.succ(sub(sub(r2, y), UNIT));
      y = this.succ(sub(sub(r2, x), UNIT));
      z = fuse(x, y); if (min === null || cmp(z, min) < 0) min = z;
      y = sub(y, ulp(y));
    } while (cmp(y, lim) > 0);
    this.gS.set(r, min); return min;
  };
  // Algorithm 3: the smallest fusible number greater than or equal to r
  Fusible.prototype.weakSucc = function (r) {
    if (r[0] <= Z) return ZERO;
    var got = this.gW.get(r); if (got) return got; this.calls.weak++;
    var min = null, y = r, x, z, t, r2 = dbl(r), lim = sub(r, HALF), ans = null;
    do {
      t = sub(sub(r2, y), UNIT); x = this.weakSucc(t); if (cmp(x, t) === 0) { ans = r; break; }
      t = sub(sub(r2, x), UNIT); y = this.weakSucc(t); if (cmp(y, t) === 0) { ans = r; break; }
      z = fuse(x, y); if (min === null || cmp(z, min) < 0) min = z;
      y = sub(y, ulp(y));
    } while (cmp(y, lim) > 0);
    if (ans === null) ans = min;
    this.gW.set(r, ans); return ans;
  };
  // Algorithm 2
  Fusible.prototype.isFusible = function (r) { return !isNeg(r) && cmp(this.weakSucc(r), r) === 0; };
  // Algorithm 4: the smallest TAME fusible number greater than r
  Fusible.prototype.tameSucc = function (r) {
    if (isNeg(r)) return ZERO;
    var k = key(r), got = this.mT.get(k); if (got) return got; this.calls.tame++;
    var x = this.tameSucc(sub(r, UNIT)), y = this.tameSucc(sub(sub(dbl(r), x), UNIT)), z = fuse(x, y);
    this.mT.set(k, z); return z;
  };
  // Algorithm 5: M(r) = tameSucc(r) - r.  The paper's procedure is "if r < 0 return -r, else return M(r - M(r - 1))/2".
  // It is done here with a list of unfinished calls in place of the machine's own stack, because the calls nest as deep
  // as the answer's exponent; the arithmetic, the order of the calls and the memory are those of the recursive form.
  // With a budget (a number of steps), the procedure gives up and returns null when the budget is spent.
  Fusible.prototype.M = function (r0, budget) {
    if (isNeg(r0)) return neg(r0);
    var memo = this.mM, stack = [[r0, 0]], val = null, top, r, k, got, a, steps = 0;
    while (stack.length) {
      if (budget && ++steps > budget) return null;
      top = stack[stack.length - 1]; r = top[0];
      if (top[1] === 0) {                                   // first visit: is the answer known?  else ask for M(r - 1)
        if (isNeg(r)) { val = neg(r); stack.pop(); continue; }
        k = key(r); got = memo.get(k); if (got) { val = got; stack.pop(); continue; }
        this.calls.m++; if (stack.length > this.depthM) this.depthM = stack.length; top[1] = 1; stack.push([sub(r, UNIT), 0]);
      } else if (top[1] === 1) { a = sub(r, val); top[1] = 2; stack.push([a, 0]); }      // val is M(r - 1): ask for M(r - M(r - 1))
      else { val = half(val); memo.set(key(r), val); stack.pop(); }                      // val is M(r - M(r - 1)): halve it
    }
    return val;
  };
  // The same for the meek numbers: meekM(r) = MeekSucc(r) - r.  In the 2012 survey's form (its formula 3):
  //   m(x) = -x for x < 0, else m(x - a - 1/d + 2^ceil(log2 a)) / 2, with a = m(x - 1) and d the denominator of x - 1 + a.
  // Done with a list of unfinished calls, like M above, because the calls nest as deep as the answer's exponent.
  Fusible.prototype.meekM = function (r0, budget) {
    if (isNeg(r0)) return neg(r0);
    var memo = this.mKM, stack = [[r0, 0]], val = null, top, r, k, got, a, p, q, x, steps = 0;
    while (stack.length) {
      if (budget && ++steps > budget) return null;
      top = stack[stack.length - 1]; r = top[0];
      if (top[1] === 0) {
        if (isNeg(r)) { val = neg(r); stack.pop(); continue; }
        k = key(r); got = memo.get(k); if (got) { val = got; stack.pop(); continue; }
        this.calls.meekM++; if (stack.length > this.depthK) this.depthK = stack.length; top[1] = 1; stack.push([sub(r, UNIT), 0]);
      } else if (top[1] === 1) {
        a = val; x = add(sub(r, UNIT), a);                                   // a = m(r - 1); x = the meek successor of r - 1
        p = UNIT; if (cmp(a, UNIT) > 0) { while (cmp(p, a) < 0) p = dbl(p); } else { for (;;) { q = half(p); if (cmp(q, a) < 0) break; p = q; } }
        top[1] = 2; stack.push([add(sub(sub(r, a), ulp(x)), p), 0]);
      } else { val = half(val); memo.set(key(r), val); stack.pop(); }
    }
    return val;
  };
  // Algorithm 6: the smallest MEEK fusible number greater than r (conjectured in the paper to be the same as succ).
  // As printed, the procedure ends "return x ~ y" with x = MeekSucc(r - 1); for r = 1/2 that returns 1/2, which is not
  // greater than r.  Conjecture 7.1 fuses with s^(n) of the number before x, which is x + 1/Denominator(x) - 2^ceil(log2(x-r+1)),
  // and the argument printed for the second call is 2r - 1 minus exactly that; so I return THAT number fused with y.
  // With printed = true the procedure is run as printed.
  Fusible.prototype.meekSucc = function (r, printed) {
    if (isNeg(r)) return ZERO;
    var memo = printed ? this.mK2 : this.mK, k = key(r), got = memo.get(k); if (got) return got; this.calls.meek++;
    var x = this.meekSucc(sub(r, UNIT), printed), g = add(sub(x, r), UNIT);   // x - r + 1, which is positive
    // 2^ceil(log2 g): the least power of two that is not less than g
    var p = UNIT, q; if (cmp(g, UNIT) > 0) { while (cmp(p, g) < 0) p = dbl(p); } else { for (;;) { q = half(p); if (cmp(q, g) < 0) break; p = q; } }
    var a = sub(add(x, ulp(x)), p), y = this.meekSucc(sub(sub(dbl(r), a), UNIT), printed), z = fuse(printed ? x : a, y);
    if (printed && cmp(z, r) <= 0) throw new Error('as printed, MeekSucc(' + str(r) + ') would return ' + str(z));
    memo.set(k, z); return z;
  };
  var api = { D: D, parse: parse, str: str, num: num, add: add, sub: sub, cmp: cmp, half: half, dbl: dbl, neg: neg, fuse: fuse, ulp: ulp, key: key, Memo: Memo, Gaps: Gaps, ZERO: ZERO, UNIT: UNIT, HALF: HALF, Fusible: Fusible };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.Fuse = api;
})(typeof window !== 'undefined' ? window : this);
