/* The doubling turtle: how many odd denominators m up to N give a bounded path, by Fuchs's rule in the form
   "for some prime power l^e of m, l divides the order of 2 modulo l^e more often than it divides the order of 2
   modulo any other prime of m".   usage: ./count N      (N up to 10^8; about 0.5 GB of memory for 10^8)
   Prints the counts at each power of ten up to N.  Noon (agent2), 26 November 2026. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static uint32_t *spf;                       /* smallest prime factor */
static uint64_t powmod(uint64_t b, uint64_t e, uint64_t m) { uint64_t r = 1; b %= m; while (e) { if (e & 1) r = (unsigned __int128)r * b % m; b = (unsigned __int128)b * b % m; e >>= 1; } return r; }
/* the order of 2 modulo the prime r, from the factors of r - 1 */
static uint32_t ord_prime(uint32_t r) { uint32_t o = r - 1, t = r - 1; while (t > 1) { uint32_t s = spf[t]; while (t % s == 0) t /= s; while (o % s == 0 && powmod(2, o / s, r) == 1) o /= s; } return o; }
static int val(uint64_t o, uint32_t l) { int k = 0; while (o % l == 0) { o /= l; k++; } return k; }
/* how often l divides the order of 2 modulo l^e: found by powering, so nothing is assumed about 1093 or 3511 */
static int val_self(uint32_t l, int e) { uint64_t mod = 1; for (int i = 0; i < e; i++) mod *= l; uint64_t d = ord_prime(l); int k = 0; uint64_t o = d; while (powmod(2, o, mod) != 1) { o *= l; k++; } return k; }

int main(int argc, char **argv) {
  uint64_t N = strtoull(argv[1], 0, 10);
  spf = calloc(N + 1, sizeof(uint32_t)); if (!spf) { fprintf(stderr, "no memory\n"); return 1; }
  for (uint64_t i = 2; i <= N; i++) if (!spf[i]) { for (uint64_t j = i; j <= N; j += i) if (!spf[j]) spf[j] = (uint32_t)i; }
  uint64_t odd = 0, withsq = 0, bounded = 0, mark = 1000;
  for (uint64_t m = 3; m <= N; m += 2) {
    uint32_t ps[16]; int es[16], n = 0, sq = 0; uint64_t t = m;
    while (t > 1) { uint32_t l = spf[t]; int e = 0; while (t % l == 0) { t /= l; e++; } ps[n] = l; es[n] = e; n++; if (e >= 2) sq = 1; }
    odd++;
    if (sq) {
      withsq++; int b = 0;
      for (int i = 0; i < n && !b; i++) if (es[i] >= 2) {
        int here = val_self(ps[i], es[i]); if (here < 1) continue;
        int spoilt = 0; for (int j = 0; j < n && !spoilt; j++) if (j != i && val(ord_prime(ps[j]), ps[i]) >= here) spoilt = 1;
        if (!spoilt) b = 1;
      }
      bounded += b;
    }
    if (m + 2 > mark || m + 2 > N) { if (m + 2 > mark) { printf("odd m up to %llu: %llu; with a square %llu; bounded %llu = %.5f of all, %.5f of those with a square\n", (unsigned long long)mark, (unsigned long long)odd, (unsigned long long)withsq, (unsigned long long)bounded, (double)bounded / odd, (double)bounded / withsq); mark *= 10; } }
  }
  return 0;
}
