/* How nearly can a round of the doubling turtle close without closing?
   For every odd m from 3 to N and every coset a<2> of the powers of 2 in the units modulo m, the sum of e(x/m) over
   the coset (e(t) = exp(2 pi i t)).  That sum is one round of the turtle whose first turn is a/m of a whole turn.
   By the rule (Fuchs, 1863) all of these are nought for a given m, or none is: nought exactly when the order of 2
   modulo m differs from its order modulo the product of the primes of m.  For those m only the coset of 1 is
   added up, as a control (it should come to nought within rounding).

   usage: ./small N K mode [T]    N: largest m.  K: how many of the smallest sums to list.
                                  mode 0: add up.  mode 1: no cosines; only the counts and the sums the model needs.
                                  T: threads (default 12).
   A coset and its negative are one line: if -1 is a power of 2 modulo m they are the same coset and the sum is real;
   if not, the two sums are complex conjugates, and the pair is counted once.
   Noon (agent2), 26 November 2026. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <omp.h>

void trig(const double *t, double *c, double *s, int n);

#define CH 2048
#define NB 60                       /* bins of a quarter of a decade, from 1e-11 up */
#define NBK 4
static const uint32_t BK[NBK] = { 1500, 20000, 200000, 2000000 };
#define PAGE_N 20000                /* the page draws at most this many steps */

typedef struct { double v; uint32_t m, a, n; int real; } hit;
typedef struct {
  hit *top; int ntop, K; double worst;            /* the K smallest so far; worst = the largest of them */
  uint64_t hist[2][NB];
  uint64_t nm_open, nm_closed, cos_real, cos_pair, terms;
  double Hr, Hc, Hr_page, Hc_page;                /* sums for the model: 2/sqrt(2 pi n) over real cosets, 1/n over pairs */
  uint64_t cos_real_page, cos_pair_page;
  double minr[NBK], minc[NBK], min1[NBK];         /* least real, least complex, least for the coset of 1, by size of m */
  double minr_page, minc_page;                    /* the same for rounds of at most PAGE_N steps */
  uint32_t minr_page_m, minr_page_a, minc_page_m, minc_page_a;
  double ctl_max; uint32_t ctl_m;                 /* control: the largest sum of a round that the rule says closes */
  double ctl_min_open1;                           /* and the least sum, coset of 1, of a round that it says does not */
} acc;

static void push(acc *A, double v, uint32_t m, uint32_t a, uint32_t n, int real) {
  if (A->ntop < A->K) { hit h = { v, m, a, n, real }; A->top[A->ntop++] = h; if (v > A->worst) A->worst = v; return; }
  if (v >= A->worst) return;
  int w = 0; for (int i = 1; i < A->K; i++) if (A->top[i].v > A->top[w].v) w = i;
  hit h = { v, m, a, n, real }; A->top[w] = h;
  double x = 0; for (int i = 0; i < A->K; i++) if (A->top[i].v > x) x = A->top[i].v; A->worst = x;
}
static int cmp(const void *p, const void *q) { double a = ((const hit *)p)->v, b = ((const hit *)q)->v; return a < b ? -1 : a > b; }

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: small N K mode [T]\n"); return 2; }
  uint32_t N = (uint32_t)atol(argv[1]); int K = atoi(argv[2]), mode = atoi(argv[3]), T = argc > 4 ? atoi(argv[4]) : 12;
  uint32_t *spf = calloc(N + 1, sizeof *spf);
  for (uint32_t i = 2; i <= N; i++) if (!spf[i]) for (uint32_t j = i; j <= N; j += i) if (!spf[j]) spf[j] = i;
  acc *all = calloc(T, sizeof *all);
  double t0 = omp_get_wtime();
  #pragma omp parallel num_threads(T)
  {
    acc *A = &all[omp_get_thread_num()];
    A->K = K; A->top = malloc(K * sizeof(hit)); A->ntop = 0; A->worst = 0;
    for (int b = 0; b < NBK; b++) A->minr[b] = A->minc[b] = A->min1[b] = 1e300;
    A->minr_page = A->minc_page = 1e300; A->ctl_min_open1 = 1e300;
    uint64_t *vis = malloc(((N >> 6) + 2) * sizeof *vis);
    double *ang = malloc(CH * sizeof *ang), *cs = malloc(CH * sizeof *cs), *sn = malloc(CH * sizeof *sn);
    #pragma omp for schedule(dynamic, 64)
    for (long i = 0; i < (long)((N - 1) / 2); i++) {     /* the largest m first, so that the threads share the load evenly */
      uint32_t m = 2 * (uint32_t)((long)((N - 1) / 2) - i) + 1; if (m > N) continue;
      uint32_t pr[12]; int np = 0; uint32_t r = m, rad = 1;
      while (r > 1) { uint32_t p = spf[r]; pr[np++] = p; rad *= p; while (r % p == 0) r /= p; }
      double w = 2 * M_PI / m; int closed = 0; uint32_t n = 0;
      int bk = 0; while (m > BK[bk] && bk < NBK - 1) bk++;
      memset(vis, 0, ((m >> 6) + 1) * sizeof *vis);
      for (int i = 0; i < np; i++) for (uint32_t x = pr[i]; x < m; x += pr[i]) vis[x >> 6] |= 1ULL << (x & 63);
      for (uint32_t a = 1; a <= m / 2; a++) {
        if (vis[a >> 6] >> (a & 63) & 1) continue;
        uint32_t x = a, len = 0, neg = m - a; int real = 0;
        double sr = 0, si = 0, cr = 0, ci = 0;
        for (;;) {
          int c = 0, done = 0;
          while (c < CH) {
            vis[x >> 6] |= 1ULL << (x & 63); uint32_t y = m - x; vis[y >> 6] |= 1ULL << (y & 63);
            if (x == neg) real = 1;
            ang[c++] = x * w; x <<= 1; if (x >= m) x -= m;
            if (x == a) { done = 1; break; }
          }
          if (!mode) {
            trig(ang, cs, sn, c);
            for (int i = 0; i < c; i++) {            /* Neumaier's compensated sum */
              double t = sr + cs[i]; cr += fabs(sr) >= fabs(cs[i]) ? (sr - t) + cs[i] : (cs[i] - t) + sr; sr = t;
              t = si + sn[i];        ci += fabs(si) >= fabs(sn[i]) ? (si - t) + sn[i] : (sn[i] - t) + si; si = t;
            }
          }
          len += c; if (done) break;
        }
        A->terms += len;
        double v = hypot(sr + cr, si + ci);
        if (a == 1) {                                  /* the coset of 1 is the powers of 2: its length is the order */
          n = len;
          if (rad != m) { uint32_t o = 1, z = 2 % rad; while (z != 1) { z = z * 2 % rad; o++; } closed = (o != n); }
          if (closed) { A->nm_closed++; if (v > A->ctl_max) { A->ctl_max = v; A->ctl_m = m; } break; }
          A->nm_open++; if (v < A->ctl_min_open1) A->ctl_min_open1 = v;
          if (v < A->min1[bk]) A->min1[bk] = v;
        }
        int page = len <= PAGE_N;
        if (real) { A->cos_real++; A->Hr += 2 / sqrt(2 * M_PI * len); if (page) { A->cos_real_page++; A->Hr_page += 2 / sqrt(2 * M_PI * len); } }
        else      { A->cos_pair++; A->Hc += 1.0 / len;                if (page) { A->cos_pair_page++; A->Hc_page += 1.0 / len; } }
        if (mode) continue;
        if (real) { if (v < A->minr[bk]) A->minr[bk] = v; if (page && v < A->minr_page) { A->minr_page = v; A->minr_page_m = m; A->minr_page_a = a; } }
        else      { if (v < A->minc[bk]) A->minc[bk] = v; if (page && v < A->minc_page) { A->minc_page = v; A->minc_page_m = m; A->minc_page_a = a; } }
        int b = (int)floor((log10(v > 1e-300 ? v : 1e-300) + 11) * 4); if (b < 0) b = 0; if (b >= NB) b = NB - 1;
        A->hist[real][b]++;
        push(A, v, m, a, len, real);
      }
    }
    free(vis); free(ang); free(cs); free(sn);
  }
  /* put the threads' tallies together */
  acc S; memset(&S, 0, sizeof S); S.K = K; S.top = malloc((size_t)K * T * sizeof(hit)); S.ntop = 0;
  for (int b = 0; b < NBK; b++) S.minr[b] = S.minc[b] = S.min1[b] = 1e300;
  S.minr_page = S.minc_page = 1e300; S.ctl_min_open1 = 1e300;
  for (int t = 0; t < T; t++) { acc *A = &all[t];
    for (int i = 0; i < A->ntop; i++) S.top[S.ntop++] = A->top[i];
    for (int k = 0; k < 2; k++) for (int b = 0; b < NB; b++) S.hist[k][b] += A->hist[k][b];
    S.nm_open += A->nm_open; S.nm_closed += A->nm_closed; S.cos_real += A->cos_real; S.cos_pair += A->cos_pair; S.terms += A->terms;
    S.Hr += A->Hr; S.Hc += A->Hc; S.Hr_page += A->Hr_page; S.Hc_page += A->Hc_page; S.cos_real_page += A->cos_real_page; S.cos_pair_page += A->cos_pair_page;
    for (int b = 0; b < NBK; b++) { if (A->minr[b] < S.minr[b]) S.minr[b] = A->minr[b]; if (A->minc[b] < S.minc[b]) S.minc[b] = A->minc[b]; if (A->min1[b] < S.min1[b]) S.min1[b] = A->min1[b]; }
    if (A->minr_page < S.minr_page) { S.minr_page = A->minr_page; S.minr_page_m = A->minr_page_m; S.minr_page_a = A->minr_page_a; }
    if (A->minc_page < S.minc_page) { S.minc_page = A->minc_page; S.minc_page_m = A->minc_page_m; S.minc_page_a = A->minc_page_a; }
    if (A->ctl_max > S.ctl_max) { S.ctl_max = A->ctl_max; S.ctl_m = A->ctl_m; }
    if (A->ctl_min_open1 < S.ctl_min_open1) S.ctl_min_open1 = A->ctl_min_open1;
  }
  qsort(S.top, S.ntop, sizeof(hit), cmp);
  printf("odd m from 3 to %u: %llu whose rounds do not close, %llu whose rounds close (by the rule)\n", N, (unsigned long long)S.nm_open, (unsigned long long)S.nm_closed);
  printf("cosets added up: %llu real (the coset is its own negative), %llu pairs of conjugates; %llu terms; %.1f s on %d threads; mode %d\n",
         (unsigned long long)S.cos_real, (unsigned long long)S.cos_pair, (unsigned long long)S.terms, omp_get_wtime() - t0, T, mode);
  printf("the model's sums: over real cosets of 2/sqrt(2 pi n): %.4f; over pairs of 1/n: %.4f\n", S.Hr, S.Hc);
  printf("   for rounds of at most %d steps: %llu real, sum %.4f; %llu pairs, sum %.4f\n", PAGE_N, (unsigned long long)S.cos_real_page, S.Hr_page, (unsigned long long)S.cos_pair_page, S.Hc_page);
  if (!mode) {
    printf("control: the largest sum of a round that the rule says closes (coset of 1): %.3e at m = %u; the least that it says does not: %.6f\n", S.ctl_max, S.ctl_m, S.ctl_min_open1);
    double cr = 1e300, cc = 1e300, c1 = 1e300;
    for (int b = 0; b < NBK; b++) { if (BK[b] > N && (b == 0 || BK[b - 1] >= N)) break;
      if (S.minr[b] < cr) cr = S.minr[b]; if (S.minc[b] < cc) cc = S.minc[b]; if (S.min1[b] < c1) c1 = S.min1[b];
      printf("m up to %7u: least real sum %.6e, least complex sum %.6e, least sum for the coset of 1 %.6e\n", BK[b] < N ? BK[b] : N, cr, cc, c1); }
    printf("rounds of at most %d steps: least real sum %.6e (m = %u, a = %u), least complex %.6e (m = %u, a = %u)\n", PAGE_N, S.minr_page, S.minr_page_m, S.minr_page_a, S.minc_page, S.minc_page_m, S.minc_page_a);
    printf("how many sums lie below each size (real cosets; pairs):\n");
    uint64_t ar = 0, ac = 0;
    for (int b = 0; b < NB; b++) { ar += S.hist[1][b]; ac += S.hist[0][b]; if ((b + 1) % 4 == 0 && b < 52) printf("   below 1e%+03d: %llu real, %llu pairs\n", (b + 1) / 4 - 11, (unsigned long long)ar, (unsigned long long)ac); }
    printf("the %d smallest:\n", K < S.ntop ? K : S.ntop);
    for (int i = 0; i < K && i < S.ntop; i++) printf("   %.9e  m = %u  a = %u  round of %u steps  %s\n", S.top[i].v, S.top[i].m, S.top[i].a, S.top[i].n, S.top[i].real ? "real" : "complex");
  }
  return 0;
}
