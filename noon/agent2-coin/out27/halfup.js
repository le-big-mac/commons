/* halfup.js: the rounding of averages, old and new, against whole-number arithmetic in BigInt.   node out27/halfup.js
   Every total from 0 to 12 L for every number of amounts L from 2 to 1000, at three decimal places. */
const P = require('../pcore.js'), O = require('./pcore.before-27nov.js');
let n = 0, half = 0, halfL16 = 0, badNew = 0, differ = 0, differNotHalf = 0, oldDown = 0, oldWrong = 0, firstDown = '', firstUp = '';
for (let L = 2; L <= 1000; L++) for (let tot = 0; tot <= 12 * L; tot++) {
  const T = BigInt(tot), LL = BigInt(L), q = (2000n * T + LL) / (2n * LL), exact = q * LL === 1000n * T;
  let s = (q / 1000n) + '.' + String(q % 1000n).padStart(3, '0'); s = s.replace(/0+$/, '').replace(/\.$/, '');
  const want = (exact ? '' : 'about ') + s, a = P.meanText(tot, L, 3), o = O.meanText(tot, L, 3);
  const isHalf = (2000n * T) % LL === 0n && (1000n * T) % LL !== 0n;
  n++; if (isHalf) { half++; if (L % 16 === 0) halfL16++; }
  if (a !== want) badNew++;
  if (o !== want) { oldWrong++; if (isHalf) { oldDown++; if (!firstDown) firstDown = tot + '/' + L + ' = ' + (tot / L) + ' printed "' + o + '"'; } }
  else if (isHalf && !firstUp) firstUp = tot + '/' + L + ' = ' + (tot / L) + ' printed "' + o + '"';
  if (a !== o) { differ++; if (!isHalf) differNotHalf++; }
}
console.log(n + ' totals and ranges (every total from 0 to 12 L, L from 2 to 1000)');
console.log(half + ' of them fall half-way in the third decimal place; ' + halfL16 + ' of those have L a multiple of 16');
console.log('the function as it is now: ' + badNew + ' differ from half up in whole numbers');
console.log('the function as it was: ' + oldWrong + ' differ, ' + oldDown + ' of them half-way cases sent down; the first sent down: ' + firstDown + '; the first sent up: ' + firstUp);
console.log('old and new differ in ' + differ + '; ' + differNotHalf + ' of those are not half-way cases');
