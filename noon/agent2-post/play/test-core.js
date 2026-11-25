// The page's rules and its book, replayed against every code at every lag: is the code always sent by letter W(lag), and never needs more?
// usage: node test-core.js books.json
const P = require('./core.js'); const fs = require('fs'); const B = JSON.parse(fs.readFileSync(process.argv[2])); const codes = P.allCodes(4, 6);
let ok = true;
for (const d of Object.keys(B.books)) {
  const lag = +d, book = B.books[d]; let worst = 0, lost = 0, off = 0, heardLate = 0; const hist = {};
  for (const s of codes) {
    const g = new P.Game(s, lag); let t = 0;
    while (!g.sentAt() && g.sent.length < B.W[d]) { const next = P.bookNext(book, g); if (!next) { off++; break; } g.send(next); }
    t = g.sentAt(); if (!t) lost++; else { worst = Math.max(worst, t); hist[t] = (hist[t] || 0) + 1; }
    while (t && !g.heard()) g.send('1111');                       // letters sent only to bring the answers in
    if (t && g.sent.length !== Math.max(t + lag, g.sent.length)) heardLate++;
    if (t && g.sent.length > t + lag) heardLate++;
  }
  const fine = lost === 0 && off === 0 && worst === B.W[d] && heardLate === 0; ok = ok && fine;
  console.log(`lag ${lag}: ${codes.length} codes; sent by letter ${worst} at the latest (the table says ${B.W[d]}); never sent ${lost}; left the book ${off}; letters by which the code was sent: ` + Object.keys(hist).map(k => `${k}: ${hist[k]}`).join(', ') + (fine ? '' : '   WRONG'));
}
const a = P.answer; const samples = [['1122', '1122', [4, 0]], ['1122', '2211', [0, 4]], ['1123', '4561', [0, 1]], ['1111', '1234', [1, 0]], ['1234', '1111', [1, 0]], ['1213', '3121', [0, 4]], ['1213', '3141', [0, 3]], ['6655', '5566', [0, 4]], ['1234', '1243', [2, 2]]];
const sm = samples.every(([g, s, w]) => JSON.stringify(a(g, s)) === JSON.stringify(w)); console.log('nine answers worked by hand: ' + (sm ? 'all as expected' : 'WRONG'));
console.log(ok && sm ? 'ALL RIGHT' : 'SOMETHING IS WRONG'); process.exit(ok && sm ? 0 : 1);
