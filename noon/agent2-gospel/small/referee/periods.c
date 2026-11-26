// periods.c -- all sums S(m,a) = sum_{k<n} exp(2 pi i a 2^k / m), odd m in [3,N], a prime to m,
// one coset of each pair {a<2>, -a<2>}.
// Roots of unity: e(x/m) = A[x>>s] * B[x & mask], both tables from sincosl (long double) rounded to double.
// Summation: TwoSum-compensated (Neumaier-like) in double, real and imaginary parts separately.
// Compile: gcc -O2 -march=native -ffp-contract=off -fopenmp periods.c -o periods -lm
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <omp.h>

typedef struct { double ab, re, im; uint32_t m, a, n; int self; } rec_t;

static int cmp_rec(const void *x, const void *y) {
    double a = ((const rec_t *)x)->ab, b = ((const rec_t *)y)->ab;
    return (a > b) - (a < b);
}

int main(int argc, char **argv) {
    uint32_t N = argc > 1 ? (uint32_t)atol(argv[1]) : 2000000u;
    const char *out = argc > 2 ? argv[2] : "small.txt";
    #ifndef KEEPV
#define KEEPV 1e-2
#endif
    const double ZERO = 1e-8, KEEP = KEEPV;
    uint32_t *spf = calloc(N + 1, sizeof(uint32_t));
    for (uint32_t i = 2; i <= N; i++) if (!spf[i]) for (uint32_t j = i; j <= N; j += i) if (!spf[j]) spf[j] = i;

    int nth = omp_get_max_threads();
    rec_t **recs = calloc(nth, sizeof(rec_t *));
    size_t *nrec = calloc(nth, sizeof(size_t)), *cap = calloc(nth, sizeof(size_t));
    // global tallies
    long long tot_real = 0, tot_cplx = 0, terms = 0;
    long long m_zero = 0, m_nonzero = 0, m_mixed = 0, fuchs_mismatch = 0, cnt_bad = 0;
    long long zero_cosets = 0;
    double w_real = 0, w_cplx = 0;        // sum n^-1/2 over real cosets, sum 1/n over complex pairs (non-zero m only)
    double maxzero = 0; uint32_t maxzero_m = 0, maxzero_n = 0;
    double minnz = 1e300;

    #pragma omp parallel
    {
        int t = omp_get_thread_num();
        uint8_t *vis = malloc(N + 8);
        double *A = malloc(sizeof(double) * 2 * 4200), *B = malloc(sizeof(double) * 2 * 4200);
        long long l_real = 0, l_cplx = 0, l_terms = 0, l_mz = 0, l_mnz = 0, l_mixed = 0, l_fm = 0, l_bad = 0, l_zc = 0;
        double l_wr = 0, l_wc = 0, l_maxzero = 0, l_minnz = 1e300; uint32_t l_mzm = 0, l_mzn = 0;
        const long double TWOPI = 6.283185307179586476925286766559005768L;

        #pragma omp for schedule(dynamic, 8) nowait
        for (int64_t mm = (int64_t)(N | 1) - ((N & 1) ? 0 : 0); mm >= 3; mm -= 2) {
            uint32_t m = (uint32_t)mm;
            if (m > N) continue;
            // factor
            uint32_t pr[12]; int np = 0; uint32_t r = m, rad = 1;
            while (r > 1) { uint32_t p = spf[r]; pr[np++] = p; rad *= p; while (r % p == 0) r /= p; }
            // tables
            int bits = 32 - __builtin_clz(m);
            int s = (bits + 1) / 2;
            uint32_t mask = (1u << s) - 1, nA = ((m - 1) >> s) + 1, nB = 1u << s;
            for (uint32_t h = 0; h < nA; h++) {
                long double sn, cs; sincosl(TWOPI * (long double)(h << s) / (long double)m, &sn, &cs);
                A[2 * h] = (double)cs; A[2 * h + 1] = (double)sn;
            }
            for (uint32_t l = 0; l < nB; l++) {
                long double sn, cs; sincosl(TWOPI * (long double)l / (long double)m, &sn, &cs);
                B[2 * l] = (double)cs; B[2 * l + 1] = (double)sn;
            }
            memset(vis, 0, m);
            vis[0] = 1;
            for (int i = 0; i < np; i++) for (uint32_t j = pr[i]; j < m; j += pr[i]) vis[j] = 1;
            // order of 2 mod m and whether -1 is a power of 2
            uint32_t n = 0; int self = 0;
            { uint32_t x = 1; do { if (x == m - 1) self = 1; x <<= 1; if (x >= m) x -= m; n++; } while (x != 1); }
            int fuchs_zero = 0;
            if (rad != m) { uint32_t x = 1, nr = 0; do { x <<= 1; if (x >= rad) x -= rad; nr++; } while (x != 1); fuchs_zero = (nr != n); }
            long long cos_here = 0, zero_here = 0;
            for (uint32_t a = 1; a <= (m - 1) / 2; a++) {
                if (vis[a]) continue;
                double sr = 0, si = 0, er = 0, ei = 0; uint32_t x = a, cnt = 0;
                do {
                    uint32_t hi = x >> s, lo = x & mask;
                    double ar = A[2 * hi], ai = A[2 * hi + 1], br = B[2 * lo], bi = B[2 * lo + 1];
                    double tr = ar * br - ai * bi, ti = ar * bi + ai * br;
                    double s1 = sr + tr, bb = s1 - sr; er += (sr - (s1 - bb)) + (tr - bb); sr = s1;
                    double s2 = si + ti, cc = s2 - si; ei += (si - (s2 - cc)) + (ti - cc); si = s2;
                    vis[x] = 1; vis[m - x] = 1;
                    x <<= 1; if (x >= m) x -= m;
                    cnt++;
                } while (x != a);
                if (cnt != n) l_bad++;
                l_terms += cnt;
                double re = sr + er, im = si + ei, ab = hypot(re, im);
                cos_here++;
                if (ab < ZERO) {
                    zero_here++;
                    if (ab > l_maxzero) { l_maxzero = ab; l_mzm = m; l_mzn = n; }
                } else {
                    if (ab < l_minnz) l_minnz = ab;
                    if (ab < KEEP) {
                        if (nrec[t] == cap[t]) { cap[t] = cap[t] ? 2 * cap[t] : 4096; recs[t] = realloc(recs[t], cap[t] * sizeof(rec_t)); }
                        rec_t q = { ab, re, im, m, a, n, self }; recs[t][nrec[t]++] = q;
                    }
                }
            }
            if (zero_here == 0) l_mnz++; else if (zero_here == cos_here) l_mz++; else l_mixed++;
            if ((zero_here == cos_here) != fuchs_zero) l_fm++;
            l_zc += zero_here;
            if (!fuchs_zero) {
                if (self) { l_real += cos_here; l_wr += cos_here / sqrt((double)n); }
                else { l_cplx += cos_here; l_wc += cos_here / (double)n; }
            }
        }
        #pragma omp critical
        {
            tot_real += l_real; tot_cplx += l_cplx; terms += l_terms; m_zero += l_mz; m_nonzero += l_mnz; m_mixed += l_mixed;
            fuchs_mismatch += l_fm; cnt_bad += l_bad; zero_cosets += l_zc; w_real += l_wr; w_cplx += l_wc;
            if (l_maxzero > maxzero) { maxzero = l_maxzero; maxzero_m = l_mzm; maxzero_n = l_mzn; }
            if (l_minnz < minnz) minnz = l_minnz;
        }
        free(vis); free(A); free(B);
    }
    size_t tot = 0; for (int t = 0; t < nth; t++) tot += nrec[t];
    rec_t *all = malloc((tot + 1) * sizeof(rec_t)); size_t k = 0;
    for (int t = 0; t < nth; t++) { memcpy(all + k, recs[t], nrec[t] * sizeof(rec_t)); k += nrec[t]; }
    qsort(all, tot, sizeof(rec_t), cmp_rec);
    FILE *f = fopen(out, "w");
    fprintf(f, "# N=%u  columns: |S| re im m a n self(1 if -1 in <2>)\n", N);
    for (size_t i = 0; i < tot; i++) fprintf(f, "%.17e %.17e %.17e %u %u %u %d\n", all[i].ab, all[i].re, all[i].im, all[i].m, all[i].a, all[i].n, all[i].self);
    fclose(f);
    printf("N=%u threads=%d terms=%lld\n", N, nth, terms);
    printf("m with every sum < %.0e (zero): %lld ; m with no sum < %.0e: %lld ; mixed m: %lld\n", ZERO, m_zero, ZERO, m_nonzero, m_mixed);
    printf("disagreements with the criterion ord_m(2) != ord_rad(m)(2): %lld ; orbit-length disagreements: %lld\n", fuchs_mismatch, cnt_bad);
    printf("zero cosets (pairs counted once): %lld ; largest computed |S| among them: %.3e at m=%u n=%u\n", zero_cosets, maxzero, maxzero_m, maxzero_n);
    printf("non-zero m: real cosets %lld (sum n^-1/2 = %.6g) ; complex pairs %lld (sum 1/n = %.6g)\n", tot_real, w_real, tot_cplx, w_cplx);
    printf("least non-zero |S| = %.17e ; records kept below %.0e: %zu\n", minnz, KEEP, tot);
    const double th[5] = { 1e-2, 1e-3, 1e-4, 1e-5, 1e-6 };
    for (int j = 0; j < 5; j++) {
        long long cs = 0, cn = 0;
        for (size_t i = 0; i < tot; i++) if (all[i].ab < th[j]) { if (all[i].self) cs++; else cn++; }
        printf("0<|S|<%.0e : self-negative %lld , others %lld\n", th[j], cs, cn);
    }
    printf("smallest 25 overall:\n");
    for (size_t i = 0; i < tot && i < 25; i++) printf("%.15e m=%u a=%u n=%u self=%d\n", all[i].ab, all[i].m, all[i].a, all[i].n, all[i].self);
    printf("smallest 25 not self-negative:\n");
    for (size_t i = 0, c = 0; i < tot && c < 25; i++) if (!all[i].self) { printf("%.15e m=%u a=%u n=%u re=%.15e im=%.15e\n", all[i].ab, all[i].m, all[i].a, all[i].n, all[i].re, all[i].im); c++; }
    return 0;
}
