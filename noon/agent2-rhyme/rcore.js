// rcore.js -- the page's reckoning, with no drawing in it, so that node can test it against the Python tables.
// D is data.json: poets, groups, families, fails [poet, family, word 1, word 2, line 1, line 2, title, ending 1, ending 2],
// lines, titles, words, pairs [word 1, word 2, times, 1 still rhymes / 0 does not / 2 cannot be judged, poets as letters].
(function (root) {
  'use strict';
  var PCH = '0123456789abcdefghijklmnopqrstuv';
  function index(D) {
    var byWord = Object.create(null), widx = Object.create(null), failsBy = Object.create(null), failsPair = Object.create(null), i, p, f, k;      /* no inherited keys: "constructor" is a word like any other */
    for (i = 0; i < D.words.length; i++) widx[D.words[i]] = i;
    for (i = 0; i < D.pairs.length; i++) { p = D.pairs[i]; (byWord[p[0]] = byWord[p[0]] || []).push(i); if (p[1] !== p[0]) (byWord[p[1]] = byWord[p[1]] || []).push(i); }
    for (i = 0; i < D.fails.length; i++) { f = D.fails[i]; k = f[1] + ',' + f[0]; (failsBy[k] = failsBy[k] || []).push(i); k = f[2] < f[3] ? f[2] + '/' + f[3] : f[3] + '/' + f[2]; (failsPair[k] = failsPair[k] || []).push(i); }
    return { byWord: byWord, widx: widx, failsBy: failsBy, failsPair: failsPair };
  }
  function clean(s) { return String(s).toLowerCase().replace(/[^a-z]/g, ''); }
  function poetsOf(s) { var out = [], i; for (i = 0; i < s.length; i++) out.push(PCH.indexOf(s.charAt(i))); return out; }
  // every word the corpus rhymes with this one: [{ word, n, ok, poets }], the most frequent first
  function partners(D, X, word) {
    var w = X.widx[clean(word)], out = [], list, i, p;
    if (w === undefined) return null;
    list = X.byWord[w] || [];
    for (i = 0; i < list.length; i++) { p = D.pairs[list[i]]; out.push({ word: D.words[p[0] === w ? p[1] : p[0]], n: p[2], ok: p[3], poets: poetsOf(p[4]) }); }
    out.sort(function (a, b) { return b.n - a.n || (a.word < b.word ? -1 : a.word > b.word ? 1 : 0); });
    return out;
  }
  function tally(list) { var t = { n: 0, still: 0, not: 0, unjudged: 0 }, i; for (i = 0; i < list.length; i++) { t.n += list[i].n; if (list[i].ok === 1) t.still += list[i].n; else if (list[i].ok === 0) t.not += list[i].n; else t.unjudged += list[i].n; } return t; }
  // the failing pairs of a family (fam -1: every family) by a poet (poet -1: every poet), as indices into D.fails, in the corpus's order
  function failsOf(D, X, fam, poet) {
    var out = [], f, p, list;
    for (f = 0; f < D.families.length; f++) { if (fam >= 0 && f !== fam) continue;
      for (p = 0; p < D.poets.length; p++) { if (poet >= 0 && p !== poet) continue; list = X.failsBy[f + ',' + p]; if (list) out = out.concat(list); } }
    out.sort(function (a, b) { return a - b; }); return out;
  }
  function failsOfPair(X, w1, w2) { var a = clean(w1), b = clean(w2); return (X.failsPair[a < b ? a + '/' + b : b + '/' + a] || []).slice(); }
  function rate(D, fam, poet) { var ev = D.poets[poet].evaluable; return ev ? 1000 * D.families[fam].byPoet[poet] / ev : 0; }
  function groupRate(D, fam, g) { var ev = D.groups[g].evaluable; return ev ? 1000 * D.families[fam].byGroup[g] / ev : 0; }
  function failShare(o) { return o.evaluable ? 100 - o.M : 0; }
  function pct(x) { return (Math.round(x * 10) / 10).toFixed(1); }
  function group3(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  var api = { index: index, clean: clean, partners: partners, tally: tally, failsOf: failsOf, failsOfPair: failsOfPair, rate: rate, groupRate: groupRate, failShare: failShare, pct: pct, group3: group3, poetsOf: poetsOf };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.RCore = api;
})(this);
