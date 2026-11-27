/* pcore.js: small change. Pure functions, no page, no files.
   Noon (agent2), 24 November 2026.

   A coinage is a list of distinct positive whole numbers (the coins).
   Three ways to count the coins an amount takes:
     plain  : the fewest coins that sum to the amount            (Shallit's opt)
     greedy : take the largest coin that fits, again and again   (Shallit's greedy)
     both   : the fewest coins changing hands when the payer may be given
              coins back: whole numbers n(d), sum of n(d)*d = amount,
              count = sum of |n(d)|                               (Cramer's efficient payment)
   INF marks an amount that cannot be made. */
(function (root) {
  'use strict';
  var INF = 1000000000;

  /* sorted, distinct, checked */
  function clean(coins) {
    var seen = Object.create(null), out = [], i, c;
    for (i = 0; i < coins.length; i++) {
      c = coins[i];
      if (typeof c !== 'number' || !(c >= 1) || c !== Math.floor(c) || c > 100000) {
        throw new Error('a coin must be a whole number from 1 to 100000: ' + c);
      }
      if (!seen[c]) { seen[c] = 1; out.push(c); }
    }
    out.sort(function (a, b) { return a - b; });
    return out;
  }

  /* fewest coins for each amount 0..L-1 */
  function plain(coins, L) {
    var c = clean(coins), m = new Int32Array(L), a, i, best, v;
    for (a = 1; a < L; a++) {
      best = INF;
      for (i = 0; i < c.length && c[i] <= a; i++) {
        v = m[a - c[i]] + 1;
        if (v < best) best = v;
      }
      m[a] = best;
    }
    return m;
  }

  /* the coins the greedy way takes for one amount, largest first: list of [coin, how many];
     null if it gets stuck */
  function greedyWay(coins, amount) {
    var c = clean(coins), r = amount, out = [], i, q;
    for (i = c.length - 1; i >= 0; i--) {
      q = Math.floor(r / c[i]);
      if (q > 0) { out.push([c[i], q]); r -= q * c[i]; }
    }
    return r === 0 ? out : null;
  }

  /* greedy count for each amount 0..L-1 */
  function greedy(coins, L) {
    var c = clean(coins), g = new Int32Array(L), a, r, n, i, q;
    for (a = 1; a < L; a++) {
      r = a; n = 0;
      for (i = c.length - 1; i >= 0; i--) {
        q = Math.floor(r / c[i]);
        n += q; r -= q * c[i];
      }
      g[a] = r === 0 ? n : INF;
    }
    return g;
  }

  /* fewest coins changing hands for each amount 0..L-1.
     A breadth-first search from 0 with steps of plus or minus one coin. The coins of a
     best way can be put in an order whose running sum never leaves the open interval
     (-cmax, amount + cmax): add a coin handed over while the sum is below the amount, a
     coin handed back while it is above. So a window of one largest coin on each side
     loses nothing. */
  function both(coins, L) {
    var c = clean(coins), cmax = c[c.length - 1];
    var lo = -(cmax - 1), hi = (L - 1) + (cmax - 1), size = hi - lo + 1;
    var dist = new Int32Array(size), queue = new Int32Array(size), head = 0, tail = 0;
    var i, x, y, d, out = new Int32Array(L), a;
    for (i = 0; i < size; i++) dist[i] = INF;
    dist[-lo] = 0; queue[tail++] = -lo;
    while (head < tail) {
      x = queue[head++]; d = dist[x] + 1;
      for (i = 0; i < c.length; i++) {
        y = x + c[i];
        if (y < size && dist[y] === INF) { dist[y] = d; queue[tail++] = y; }
        y = x - c[i];
        if (y >= 0 && dist[y] === INF) { dist[y] = d; queue[tail++] = y; }
      }
    }
    for (a = 0; a < L; a++) out[a] = dist[a - lo];
    return out;
  }

  function counts(coins, L, mode) {
    if (mode === 'plain') return plain(coins, L);
    if (mode === 'greedy') return greedy(coins, L);
    if (mode === 'both') return both(coins, L);
    throw new Error('mode must be plain, greedy or both: ' + mode);
  }

  /* sum of a table of counts; Infinity if some amount cannot be made */
  function total(m) {
    var s = 0, a;
    for (a = 0; a < m.length; a++) { if (m[a] >= INF) return Infinity; s += m[a]; }
    return s;
  }
  function worst(m) {
    var w = 0, a;
    for (a = 0; a < m.length; a++) { if (m[a] >= INF) return Infinity; if (m[a] > w) w = m[a]; }
    return w;
  }

  /* amounts below L where the greedy way takes more coins than need be */
  function greedyFails(coins, L) {
    var p = plain(coins, L), g = greedy(coins, L), out = [], a;
    for (a = 0; a < L; a++) if (g[a] > p[a]) out.push(a);
    return out;
  }

  /* Pearson's test. The least amount, of any size, for which the greedy way is not the
     fewest coins; 0 if there is none. Needs a coin of 1. */
  function pearson(coins) {
    var asc = clean(coins), n = asc.length, c = [], i, j, k, g, w, size, best = 0;
    if (asc[0] !== 1) throw new Error('the test needs a coin of 1');
    for (i = 0; i < n; i++) c.push(asc[n - 1 - i]);          /* largest first */
    function vec(x) {
      var v = [], t;
      for (t = 0; t < n; t++) { v.push(Math.floor(x / c[t])); x -= v[t] * c[t]; }
      return v;
    }
    function count(v) { var s = 0, t; for (t = 0; t < n; t++) s += v[t]; return s; }
    for (i = 1; i < n; i++) {
      g = vec(c[i - 1] - 1);
      for (j = i; j < n; j++) {
        w = 0; size = 0;
        for (k = 0; k <= j; k++) { w += g[k] * c[k]; size += g[k]; }
        w += c[j]; size += 1;
        if (size < count(vec(w)) && (best === 0 || w < best)) best = w;
      }
    }
    return best;
  }

  /* the same answer by trying every amount below the sum of the two largest coins, which
     is as far as a least failure can lie (Kozen and Zaks). A witness for pearson(). */
  function firstFailure(coins) {
    var c = clean(coins), n = c.length, top, f;
    if (c[0] !== 1) throw new Error('the test needs a coin of 1');
    if (n < 3) return 0;
    top = c[n - 1] + c[n - 2];
    f = greedyFails(c, top);
    return f.length ? f[0] : 0;
  }

  /* every coin that could be added, with the total it gives; best first */
  function bestAdd(coins, L, mode, maxCoin) {
    var c = clean(coins), have = Object.create(null), out = [], v, i;
    for (i = 0; i < c.length; i++) have[c[i]] = 1;
    for (v = 1; v <= maxCoin; v++) {
      if (have[v]) continue;
      out.push({ coin: v, total: total(counts(c.concat([v]), L, mode)) });
    }
    out.sort(function (p, q) { return p.total - q.total || p.coin - q.coin; });
    return out;
  }

  /* one way of making an amount with the fewest coins: list of [coin, how many], largest
     first; null if it cannot be made */
  function plainWay(coins, amount) {
    var c = clean(coins), m = plain(c, amount + 1), out = [], a = amount, i, used = Object.create(null);
    if (m[amount] >= INF) return null;
    while (a > 0) {
      for (i = c.length - 1; i >= 0; i--) {
        if (c[i] <= a && m[a - c[i]] === m[a] - 1) { used[c[i]] = (used[c[i]] || 0) + 1; a -= c[i]; break; }
      }
    }
    for (i = c.length - 1; i >= 0; i--) if (used[c[i]]) out.push([c[i], used[c[i]]]);
    return out;
  }

  /* all the ways of settling an amount with the fewest coins changing hands.
     Each way is a list of [coin, n], n > 0 handed over, n < 0 handed back, largest first.
     Keeps at most `limit` ways (default 200) and says so in .more; .total counts them all.
     Gives up after `budget` steps (default 3 million) and says so in .gaveUp; then .total
     is only how many were found so far. */
  function schemes(coins, amount, limit, budget) {
    var c = clean(coins), n = c.length, desc = [], i, k, out = [], more = false, steps = 0, gaveUp = false;
    if (limit === undefined) limit = 200;
    if (budget === undefined) budget = 3000000;
    for (i = 0; i < n; i++) desc.push(c[n - 1 - i]);
    k = both(c, amount + 1)[amount];
    if (k >= INF) return { count: Infinity, ways: [], more: false, total: 0, gaveUp: false };
    var cur = new Array(n), found = 0;
    for (i = 0; i < n; i++) cur[i] = 0;
    function walk(idx, rest, left) {
      var v, lim, way, t, r2;
      if (gaveUp) return;
      if (++steps > budget) { gaveUp = true; return; }
      if (idx === n) {
        if (rest === 0 && left === 0) {
          found++;
          if (out.length < limit) {
            way = [];
            for (t = 0; t < n; t++) if (cur[t] !== 0) way.push([desc[t], cur[t]]);
            out.push(way);
          } else more = true;
        }
        return;
      }
      for (v = left; v >= -left; v--) {
        r2 = rest - v * desc[idx];
        lim = left - Math.abs(v);
        if (idx === n - 1) { if (r2 !== 0 || lim !== 0) continue; }
        else if (Math.abs(r2) > lim * desc[idx + 1]) continue;
        cur[idx] = v;
        walk(idx + 1, r2, lim);
      }
      cur[idx] = 0;
    }
    walk(0, amount, k);
    return { count: k, ways: out, more: more || gaveUp, total: found, gaveUp: gaveUp };
  }

  /* Counting bounds: the least total that any set of D coins could reach over the amounts
     1..L-1. One way, an amount that takes k coins is a multiset of k of the D coins, and
     there are C(D+k-1, k) of those. Both ways it is a list of D whole numbers whose
     absolute values sum to k; a list and its negative give an amount and its negative, so
     at most half of them give amounts above 0. Fill the cheapest counts first. */
  function binom(n, k) { var r = 1, i; for (i = 1; i <= k; i++) r = r * (n - k + i) / i; return Math.round(r); }
  function multisets(D, k) { return binom(D + k - 1, k); }
  function signedLists(D, k) {
    var s = 0, j;
    if (k === 0) return 1;
    for (j = 1; j <= Math.min(D, k); j++) s += binom(D, j) * binom(k - 1, j - 1) * Math.pow(2, j);
    return s;
  }
  function bound(D, L, mode) {
    var left = L - 1, k = 1, s = 0, n;
    if (mode !== 'plain' && mode !== 'both') throw new Error('bound: mode must be plain or both');
    while (left > 0) {
      n = mode === 'plain' ? multisets(D, k) : signedLists(D, k) / 2;
      if (n > left) n = left;
      s += n * k; left -= n; k++;
    }
    return s;
  }

  /* a fraction total/L in lowest terms, and as a decimal string that is exact when it ends */
  function gcd(a, b) { while (b) { var t = a % b; a = b; b = t; } return a; }
  function meanText(tot, L, places) {
    if (!isFinite(tot)) return 'cannot make every amount';
    if (places === undefined) places = 3;
    /* rounded half up, in whole numbers: the machine's own rounding of tot / L sent 3/80 = 0.0375 down to 0.037 and
       1323/240 = 5.5125 up to 5.513 (a referee, 27 November 2026: 4,224 of 14,400 half-way cases went down) */
    var scale = Math.pow(10, places), n = Math.floor((2 * tot * scale + L) / (2 * L)), exact = n * L === tot * scale;
    var s = (n / scale).toFixed(places);
    if (s.indexOf('.') >= 0) s = s.replace(/0+$/, '').replace(/\.$/, '');
    return (exact ? '' : 'about ') + s;
  }

  var api = {
    INF: INF, clean: clean, plain: plain, greedy: greedy, greedyWay: greedyWay, both: both,
    counts: counts, total: total, worst: worst, greedyFails: greedyFails, pearson: pearson,
    firstFailure: firstFailure, bestAdd: bestAdd, plainWay: plainWay, schemes: schemes,
    gcd: gcd, meanText: meanText, multisets: multisets, signedLists: signedLists, bound: bound
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.pcore = api;
})(this);
