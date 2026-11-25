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
  function key(a) { return (a[0] << 32n) | BigInt(a[1]); }                  // one BigInt for the pair (the exponent is below 2^32)
  function str(a) { return a[1] === 0 ? a[0].toString() : a[0].toString() + '/' + (ONE << BigInt(a[1])).toString(); }
  function num(a) { if (a[1] < 1000) return Number(a[0]) / Math.pow(2, a[1]); var s = a[1] - 900; return Number(a[0] >> BigInt(s)) / Math.pow(2, 900); }
  var ZERO = [Z, 0], UNIT = [ONE, 0], HALF = [ONE, 1], THREE = [3n, 0];
  function fuse(x, y) { return half(add(add(x, y), UNIT)); }                 // x ~ y
  function ulp(a) { return [ONE, a[1]]; }                                    // 1 / Denominator(a)
  function parse(s) {                                                        // "7", "33/16", "3/6" (taken to lowest terms first)
    var p = String(s).split('/'); if (p.length === 1) return D(p[0], 0);
    var n = BigInt(p[0]), q = BigInt(p[1]), e = 0, a, b, t; if (q <= Z) throw new Error('nothing to divide by: ' + s);
    a = n < Z ? -n : n; b = q; while (b) { t = a % b; a = b; b = t; } if (a > ONE) { n /= a; q /= a; }
    while (q > ONE) { if (q & ONE) throw new Error('not a dyadic fraction: ' + s); q >>= ONE; e++; } return norm(n, e); }

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

  function Fusible(cap) { this.gS = new Gaps(true); this.gW = new Gaps(false); this.mS = new Memo(cap); this.mW = new Memo(cap); this.mT = new Memo(cap); this.mM = new Memo(cap); this.mK = new Memo(cap); this.mK2 = new Memo(cap); this.mKM = new Memo(cap); this.calls = { succ: 0, weak: 0, tame: 0, m: 0, meek: 0, meekM: 0 }; this.depthM = 0; this.depthK = 0; this.spent = 0; this.maxDepth = Infinity; this.limitCalls = Infinity; this.row = null; this.deadline = 0; this.belowFrom = THREE; }
  // Algorithm 1: the smallest fusible number greater than r
  Fusible.prototype.succ = function (r) {
    if (isNeg(r)) return ZERO;
    var got = this.gS.get(r); if (got) return got; if (++this.calls.succ > this.limitCalls) throw new Error('budget');
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
    var got = this.gW.get(r); if (got) return got; if (++this.calls.weak > this.limitCalls) throw new Error('budget');
    var min = null, y = r, x, z, t, r2 = dbl(r), lim = sub(r, HALF), ans = null;
    do {
      t = sub(sub(r2, y), UNIT); x = this.weakSucc(t); if (cmp(x, t) === 0) { ans = r; break; }
      t = sub(sub(r2, x), UNIT); y = this.weakSucc(t); if (cmp(y, t) === 0) { ans = r; break; }
      z = fuse(x, y); if (min === null || cmp(z, min) < 0) min = z;
      y = sub(y, ulp(y));
    } while (cmp(y, lim) >= 0);
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
  // With a budget (a number of steps), the procedure gives up and returns null when the budget is spent; and it gives
  // up when the clock passes this.deadline (a time in milliseconds), if one is set.  The page sets one; no run does.
  Fusible.prototype.M = function (r0, budget) {
    if (isNeg(r0)) return neg(r0);
    var memo = this.mM, stack = [[r0, 0]], val = null, top, r, k, got, a, steps = 0;
    while (stack.length) {
      if ((++steps > budget && budget) || ((steps & 255) === 0 && this.deadline && Date.now() > this.deadline)) { this.spent += steps; return null; }
      top = stack[stack.length - 1]; r = top[0];
      if (top[1] === 0) {                                   // first visit: is the answer known?  else ask for M(r - 1)
        if (isNeg(r)) { val = neg(r); stack.pop(); continue; }
        k = key(r); got = memo.get(k); if (got) { val = got; stack.pop(); continue; }
        this.calls.m++; if (stack.length > this.depthM) this.depthM = stack.length; if (stack.length > this.maxDepth) { this.spent += steps; return null; } top[1] = 1; stack.push([sub(r, UNIT), 0]);
      } else if (top[1] === 1) { a = sub(r, val); top[1] = 2; stack.push([a, 0]); }      // val is M(r - 1): ask for M(r - M(r - 1))
      else { val = half(val); memo.set(key(r), val); stack.pop(); }                      // val is M(r - M(r - 1)): halve it
    }
    this.spent += steps; return val;
  };
  // The same for the meek numbers: meekM(r) = MeekSucc(r) - r.  In the 2012 survey's form (its formula 3):
  //   m(x) = -x for x < 0, else m(x - a - 1/d + 2^ceil(log2 a)) / 2, with a = m(x - 1) and d the denominator of x - 1 + a.
  // Done with a list of unfinished calls, like M above, because the calls nest as deep as the answer's exponent.
  Fusible.prototype.meekM = function (r0, budget) {
    if (isNeg(r0)) return neg(r0);
    var memo = this.mKM, stack = [[r0, 0]], val = null, top, r, k, got, a, p, q, x, steps = 0;
    while (stack.length) {
      if ((++steps > budget && budget) || ((steps & 255) === 0 && this.deadline && Date.now() > this.deadline)) { this.spent += steps; return null; }
      top = stack[stack.length - 1]; r = top[0];
      if (top[1] === 0) {
        if (isNeg(r)) { val = neg(r); stack.pop(); continue; }
        k = key(r); got = memo.get(k); if (got) { val = got; stack.pop(); continue; }
        this.calls.meekM++; if (stack.length > this.depthK) this.depthK = stack.length; if (stack.length > this.maxDepth) { this.spent += steps; return null; } top[1] = 1; stack.push([sub(r, UNIT), 0]);
      } else if (top[1] === 1) {
        a = val; x = add(sub(r, UNIT), a);                                   // a = m(r - 1); x = the meek successor of r - 1
        p = UNIT; if (cmp(a, UNIT) > 0) { while (cmp(p, a) < 0) p = dbl(p); } else { for (;;) { q = half(p); if (cmp(q, a) < 0) break; p = q; } }
        top[1] = 2; stack.push([add(sub(sub(r, a), ulp(x)), p), 0]);
      } else { val = half(val); memo.set(key(r), val); stack.pop(); }
    }
    this.spent += steps; return val;
  };
  // For the picture.  Is the gap after r smaller than 2^-p?  Both rules have the form m(x) = m(x') / 2 with x' >= x - 1, and
  // m is never more than 1 at or above -1; so after k halvings the answer is at most 2^-k whatever the rest of the chain
  // does.  This follows the chain of halvings from r, working out in full only the inner values m(x - 1) it needs, and stops
  // as soon as it knows.  Returns { gap: g } (the exact gap, the chain having ended), { small: k } (the gap is at most
  // 2^-k, and k > p), or null (the budget of steps was spent on the inner values).  meek = true for the meek rule.
  Fusible.prototype.gapOrSmall = function (r, p, budget, meek) {
    if (isNeg(r)) return { gap: neg(r) };
    var memo = meek ? this.mKM : this.mM, x = r, k = 0, chain = [], got, inner, val, sx, pw, q, start = this.spent, left, j;
    for (;;) {
      if (isNeg(x)) { val = neg(x); break; }
      got = memo.get(key(x)); if (got) { val = got; break; }
      if (k > p) return { small: k };
      left = budget ? budget - (this.spent - start) : 0; if ((budget && left <= 0) || (this.deadline && Date.now() > this.deadline)) return null;
      inner = meek ? this.meekM(sub(x, UNIT), left) : this.M(sub(x, UNIT), left); if (inner === null) return null;
      chain.push(x);
      if (meek) { sx = add(sub(x, UNIT), inner); pw = UNIT; if (cmp(inner, UNIT) > 0) { while (cmp(pw, inner) < 0) pw = dbl(pw); } else { for (;;) { q = half(pw); if (cmp(q, inner) < 0) break; pw = q; } }
        x = add(sub(sub(x, inner), ulp(sx)), pw); } else x = sub(x, inner);
      k++;
    }
    for (j = chain.length - 1; j >= 0; j--) { val = half(val); memo.set(key(chain[j]), val); }
    return { gap: val };
  };
  // One column of the picture: the numbers from a (the column's left edge) up to a + 2^-p, each end moved down by
  // 2^-(p+20) so that a fusible number standing exactly on an edge is counted in the column it begins.  Returns
  //   0  no meek number in the column          1  a tame number in it          2  meek numbers in it but no tame one ("wild")
  //   3  a fusible number in it, kind not worked out          4  not worked out within the budget
  // 3 comes from the chain's certificate when the tame rule ran out of budget, or from below: if z is fusible so is
  // z + 1/2 (= z ~ z), so a column is occupied when the column half a unit below it is.  From this.belowFrom (3) upward
  // that is tried first.
  Fusible.prototype.column = function (a, p, budget, depth) {
    var w = [ONE, p], lo = sub(a, [ONE, p + 20]), t, m, c, below = false;
    if (cmp(a, this.belowFrom) >= 0 && (depth || 0) < 12) { below = true; c = this.columnMemo(sub(a, HALF), p, budget, (depth || 0) + 1); if (c >= 1 && c <= 3) return 3; }   // from 3 on, look half a unit below first
    t = this.gapOrSmall(lo, p, budget, false);
    if (t && (t.small || cmp(t.gap, w) < 0)) return 1;
    m = this.gapOrSmall(lo, p, budget, true);
    if (m && (m.small || cmp(m.gap, w) < 0)) return t ? 2 : 3;
    if (m) return 0;
    if (!below && (depth || 0) < 12 && cmp(a, UNIT) >= 0) { c = this.columnMemo(sub(a, HALF), p, budget, (depth || 0) + 1); if (c >= 1 && c <= 3) return 3; }
    return 4;
  };
  // the same with a memory for one zoom (this.row is a Map for the present p; columns half a unit apart ask for each other)
  Fusible.prototype.columnMemo = function (a, p, budget, depth) {
    if (!this.row || this.rowP !== p || this.rowB !== budget) { this.row = new Map(); this.rowP = p; this.rowB = budget; }
    var k = key(a), c = this.row.get(k); if (c === undefined) { c = this.column(a, p, budget, depth); this.row.set(k, c); } return c;
  };
  // A recipe for a meek number: how to make z from 0 with fuses, read off Conjecture 7.1's construction.  For z below 1,
  // z = 1 - 2^-n = 0 ~ (1 - 2^-(n-1)).  For z >= 1, let s be the meek successor of z - 1, m = 1/Denominator(s) the gap
  // below s, p the least power of two not less than s + 1 - z, a = s + m - p and y = 2z - 1 - a; then z = a ~ y, a is meek,
  // and z is meek exactly when y is.  Returns null when z is not a meek number, or when the budget runs out (this.gaveUp
  // is then true; the budget is the number of nodes visited, which also bounds how deep the calls nest, and twenty times
  // it is the number of steps allowed, in all, for the successors the recipe needs), else
  // a node { v: z, a: node, b: node } (a leaf for 0 has neither); equal numbers share one node.  The recipe is checked as
  // it is built: each node's two parts are less than 1 apart and fuse to its value.
  Fusible.prototype.recipe = function (z, budget) {
    var memo = this.mR || (this.mR = new Map()), self = this, left = { n: budget || 1e9, work: budget ? budget * 20 : 0 }; this.gaveUp = false;
    function go(z) {
      if (isNeg(z)) return null; if (--left.n < 0) { self.gaveUp = true; return null; }
      var k = key(z), got = memo.get(k); if (got !== undefined) return got;
      var node = null, a, y, s, m, g, p, q, na, ny, d;
      if (z[0] === Z) node = { v: ZERO };
      else if (cmp(z, UNIT) < 0) { g = sub(UNIT, z); if (g[0] === ONE) { a = sub(UNIT, dbl(g)); y = ZERO; } else { memo.set(k, null); return null; } }
      else { var before = self.spent; if (budget && left.work <= 0) s = null; else s = self.meekM(sub(z, UNIT), budget ? left.work : 0); left.work -= self.spent - before;
        if (s === null) { self.gaveUp = true; left.n = -1; return null; } s = add(sub(z, UNIT), s); m = ulp(s); g = sub(add(s, UNIT), z); p = UNIT; if (cmp(g, UNIT) > 0) { while (cmp(p, g) < 0) p = dbl(p); } else { for (;;) { q = half(p); if (cmp(q, g) <= 0) break; p = q; } }
        a = sub(add(s, m), p); y = sub(sub(dbl(z), UNIT), a); }
      if (!node) { d = sub(a, y); if (isNeg(y) || isNeg(a) || cmp(d, UNIT) >= 0 || cmp(d, [-ONE, 0]) <= 0 || cmp(fuse(a, y), z) !== 0) { memo.set(k, null); return null; }
        ny = go(y); na = ny ? go(a) : null; node = na && ny ? { v: z, a: na, b: ny } : null; }
      if (left.n >= 0) memo.set(k, node); return node;
    }
    return go(z);
  };
  // Is z a tame number?  The tame rule's own chain: 0 is; below 1 only the numbers 1 - 2^-n are; and from 1 on z is tame
  // exactly when 2z - 1 - s is, s being the tame successor of z - 1 (then z = s ~ (2z - 1 - s)).  null if the budget (steps
  // in all, for the whole chain) runs out; without a budget this does not return for a number like 3.
  Fusible.prototype.isTame = function (z, budget) {
    var g, m, n = 0, start = this.spent, left = 0;
    for (;;) {
      if (budget) { left = budget - (this.spent - start) - n; if (left <= 0) return null; }      // the chain is as long as the exponent of the gap after z: for 3, a billion and a half
      n++; if (isNeg(z)) return false; if (z[0] === Z) return true;
      if (cmp(z, UNIT) < 0) { g = sub(UNIT, z); return g[0] === ONE; }
      m = this.M(sub(z, UNIT), left); if (m === null) return null;
      z = sub(sub(dbl(z), UNIT), add(sub(z, UNIT), m));
    }
  };
  // Is z a meek number?  The same chain as recipe(), without building the recipe.  null if the budget runs out.
  Fusible.prototype.isMeek = function (z, budget) {
    var g, m, s, p, q, a, n = 0, start = this.spent, left = 0;
    for (;;) {
      if (budget) { left = budget - (this.spent - start) - n; if (left <= 0) return null; }
      n++; if (isNeg(z)) return false; if (z[0] === Z) return true;
      if (cmp(z, UNIT) < 0) { g = sub(UNIT, z); return g[0] === ONE; }
      m = this.meekM(sub(z, UNIT), left); if (m === null) return null;
      s = add(sub(z, UNIT), m); g = sub(add(s, UNIT), z); p = UNIT; if (cmp(g, UNIT) > 0) { while (cmp(p, g) < 0) p = dbl(p); } else { for (;;) { q = half(p); if (cmp(q, g) < 0) break; p = q; } }
      a = sub(add(s, ulp(s)), p); z = sub(sub(dbl(z), UNIT), a);
    }
  };
  // how many fuses a recipe uses (one for each different number in it other than 0), and its height as a tree
  function recipeSize(node) { var seen = new Map(), h = new Map(); function go(n) { var k = key(n.v), got = h.get(k); if (got !== undefined) return got; var x = n.a ? 1 + Math.max(go(n.a), go(n.b)) : 0; h.set(k, x); if (n.a) seen.set(k, 1); return x; } var height = go(node); return { fuses: seen.size, height: height }; }
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
  var api = { D: D, parse: parse, str: str, num: num, add: add, sub: sub, cmp: cmp, half: half, dbl: dbl, neg: neg, fuse: fuse, ulp: ulp, key: key, Memo: Memo, Gaps: Gaps, recipeSize: recipeSize, ZERO: ZERO, UNIT: UNIT, HALF: HALF, Fusible: Fusible };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.Fuse = api;
})(typeof window !== 'undefined' ? window : this);
