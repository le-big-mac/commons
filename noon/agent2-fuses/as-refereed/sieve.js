// sieve.js -- fusible numbers found with none of the paper's procedures: start from 0 and fuse every pair less than 1 apart,
// keeping only results on the grid of 1/2^K below a bound, until nothing new appears.  Every number so made is fusible.
// (Not every fusible number on the grid need be made this way: a number on the grid might need off-grid operands.)
// usage as a module: sieve(K, top) -> { K, N, has: Uint8Array over grid indices, list: sorted indices, rounds }
function sieve(K, top) {                       // top = bound in units of 1/2^K (numbers i/2^K with i < top are kept)
  const one = 1 << K, has = new Uint8Array(top); has[0] = 1; let list = [0], fresh = [0], rounds = 0;
  while (fresh.length) { rounds++; const add = [];
    for (const a of fresh) for (const b of list) { const d = a > b ? a - b : b - a; if (d >= one) continue; const s = a + b + one; if (s & 1) continue; const z = s >> 1; if (z < top && !has[z]) { has[z] = 1; add.push(z); } }
    list = list.concat(add); fresh = add; }
  list.sort((x, y) => x - y); return { K: K, N: top, has: has, list: list, rounds: rounds };
}
module.exports = sieve;
if (require.main === module) { const K = +process.argv[2], top = Math.floor(eval(process.argv[3]) * (1 << K)), t0 = Date.now(), s = sieve(K, top);
  console.log(`grid of 1/2^${K} below ${process.argv[3]}: ${s.list.length} numbers made in ${s.rounds} rounds, ${((Date.now() - t0) / 1000).toFixed(1)} s; the largest ${s.list[s.list.length - 1]}/${1 << K}`); }
