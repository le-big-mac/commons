// Mastermind by post: the rules, with nothing of the page in them.
// A code is a string of four digits 1..6. The answer to guess i arrives only after guess i + lag has been sent.
(function (root) {
  'use strict';
  function answer(guess, code) {                       // [black, white]
    let black = 0; const g = {}, c = {};
    for (let i = 0; i < guess.length; i++) { if (guess[i] === code[i]) black++; g[guess[i]] = (g[guess[i]] || 0) + 1; c[code[i]] = (c[code[i]] || 0) + 1; }
    let both = 0; for (const k in g) both += Math.min(g[k], c[k] || 0);
    return [black, both - black];
  }
  const allCodes = (pegs, colours) => { const out = []; const rec = s => { if (s.length === pegs) { out.push(s); return; } for (let c = 1; c <= colours; c++) rec(s + c); }; rec(''); return out; };
  function Game(secret, lag) { this.secret = secret; this.lag = lag; this.sent = []; }
  Game.prototype.send = function (code) { this.sent.push(code); return this; };
  Game.prototype.arrived = function () { return Math.max(0, this.sent.length - this.lag); };            // how many answers are in
  Game.prototype.answers = function () { return this.sent.slice(0, this.arrived()).map(g => answer(g, this.secret)); };
  Game.prototype.sentAt = function () { const i = this.sent.indexOf(this.secret); return i < 0 ? 0 : i + 1; };  // the letter that was the code, or 0
  Game.prototype.heard = function () { const t = this.sentAt(); return t > 0 && this.arrived() >= t; };         // has its all-black answer come?
  Game.prototype.possible = function (codes) { const a = this.answers(); return codes.filter(s => a.every((x, i) => { const y = answer(this.sent[i], s); return y[0] === x[0] && y[1] === x[1]; })); };
  // The book: for this lag, "t|answers known" -> the guess to send. Returns the guess for the next letter, or null if the letters so far are not the book's.
  function bookNext(book, game) {
    const hist = n => game.sent.slice(0, Math.max(0, n)).map(g => answer(g, game.secret).join('')).join(',');
    for (let t = 1; t <= game.sent.length; t++) { const want = book[t + '|' + hist(t - 1 - game.lag)]; if (want !== game.sent[t - 1]) return null; }
    const t = game.sent.length + 1; return book[t + '|' + hist(t - 1 - game.lag)] || null;
  }
  const api = { answer, allCodes, Game, bookNext };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.Post = api;
})(typeof window !== 'undefined' ? window : globalThis);
