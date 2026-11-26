// identities.c -- two exact identities per m as a check on the VALUES of periods.c's sums (same tables and
// same summation loop, copied): over all cosets C of <2> in the units mod m,
//   sum_C S_C = mu(m)            and      sum_C |S_C|^2 = sum_{h in <2>} c_m(h-1)   (c_m = Ramanujan's sum,
//   c_m(k) = mu(m/g) phi(m)/phi(m/g), g = gcd(m,k)).   Only every STRIDE-th odd m is taken, plus ten named m.
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <omp.h>
static uint32_t *spf;
static uint32_t gcd32(uint32_t a, uint32_t b) { while (b) { uint32_t t = a % b; a = b; b = t; } return a; }
static void muphi(uint32_t k, int *mu, int64_t *phi) { int m_ = 1; int64_t p_ = 1; while (k > 1) { uint32_t p = spf[k]; int e = 0; while (k % p == 0) { k /= p; e++; p_ *= (e == 1) ? (p - 1) : p; } if (e > 1) m_ = 0; else m_ = -m_; } *mu = m_; *phi = p_; }
int main(int argc, char **argv) {
    uint32_t N = argc > 1 ? (uint32_t)atol(argv[1]) : 2000000u; uint32_t STRIDE = argc > 2 ? (uint32_t)atol(argv[2]) : 200u;
    const uint32_t named[10] = { 1009681, 1741011, 1108251, 652805, 1793689, 1395365, 273605, 1699081, 1915235, 1018469 };
    spf = calloc(N + 1, sizeof(uint32_t));
    for (uint32_t i = 2; i <= N; i++) if (!spf[i]) for (uint32_t j = i; j <= N; j += i) if (!spf[j]) spf[j] = i;
    double worst1 = 0, worst2 = 0, worst2rel = 0; long long nm = 0, terms = 0; uint32_t w1m = 0, w2m = 0;
    #pragma omp parallel
    {
        uint8_t *vis = malloc(N + 8); double *A = malloc(sizeof(double) * 2 * 4200), *B = malloc(sizeof(double) * 2 * 4200);
        const long double TWOPI = 6.283185307179586476925286766559005768L;
        #pragma omp for schedule(dynamic, 4)
        for (int64_t mm = 3; mm <= (int64_t)N; mm += 2) {
            uint32_t m = (uint32_t)mm; int take = ((m / 2) % STRIDE == 0);
            for (int i = 0; i < 10; i++) if (m == named[i]) take = 1;
            if (!take) continue;
            uint32_t pr[12]; int np = 0; uint32_t r = m;
            while (r > 1) { uint32_t p = spf[r]; pr[np++] = p; while (r % p == 0) r /= p; }
            int mu_m; int64_t phi_m; muphi(m, &mu_m, &phi_m);
            int bits = 32 - __builtin_clz(m); int s = (bits + 1) / 2;
            uint32_t mask = (1u << s) - 1, nA = ((m - 1) >> s) + 1, nB = 1u << s;
            for (uint32_t h = 0; h < nA; h++) { long double sn, cs; sincosl(TWOPI * (long double)(h << s) / (long double)m, &sn, &cs); A[2 * h] = (double)cs; A[2 * h + 1] = (double)sn; }
            for (uint32_t l = 0; l < nB; l++) { long double sn, cs; sincosl(TWOPI * (long double)l / (long double)m, &sn, &cs); B[2 * l] = (double)cs; B[2 * l + 1] = (double)sn; }
            memset(vis, 0, m); vis[0] = 1;
            for (int i = 0; i < np; i++) for (uint32_t j = pr[i]; j < m; j += pr[i]) vis[j] = 1;
            uint32_t n = 0; int self = 0; long double T = 0;
            { uint32_t x = 1; do { if (x == m - 1) self = 1;
                  uint32_t g = (x == 1) ? m : gcd32(m, x - 1); int mu_q; int64_t phi_q; muphi(m / g, &mu_q, &phi_q);
                  T += (long double)mu_q * (long double)(phi_m / phi_q);
                  x <<= 1; if (x >= m) x -= m; n++; } while (x != 1); }
            long double sum1 = 0, sum2 = 0; long long lt = 0;
            for (uint32_t a = 1; a <= (m - 1) / 2; a++) {
                if (vis[a]) continue;
                double sr = 0, si = 0, er = 0, ei = 0; uint32_t x = a;
                do {
                    uint32_t hi = x >> s, lo = x & mask;
                    double ar = A[2 * hi], ai = A[2 * hi + 1], br = B[2 * lo], bi = B[2 * lo + 1];
                    double tr = ar * br - ai * bi, ti = ar * bi + ai * br;
                    double s1 = sr + tr, bb = s1 - sr; er += (sr - (s1 - bb)) + (tr - bb); sr = s1;
                    double s2 = si + ti, cc = s2 - si; ei += (si - (s2 - cc)) + (ti - cc); si = s2;
                    vis[x] = 1; vis[m - x] = 1;
                    x <<= 1; if (x >= m) x -= m; lt++;
                } while (x != a);
                double re = sr + er, im = si + ei; int w = self ? 1 : 2;
                sum1 += w * (long double)re; sum2 += w * ((long double)re * re + (long double)im * im);
            }
            double d1 = fabs((double)(sum1 - mu_m)), d2 = fabs((double)(sum2 - T));
            #pragma omp critical
            { nm++; terms += lt; if (d1 > worst1) { worst1 = d1; w1m = m; } if (d2 > worst2) { worst2 = d2; w2m = m; } if (T > 0 && d2 / (double)T > worst2rel) worst2rel = d2 / (double)T; }
        }
        free(vis); free(A); free(B);
    }
    printf("N=%u stride=%u : %lld values of m, %lld terms\n", N, STRIDE, nm, terms);
    printf("largest |sum_C S_C - mu(m)| = %.3e (m=%u)\n", worst1, w1m);
    printf("largest |sum_C |S_C|^2 - sum_h c_m(h-1)| = %.3e (m=%u) ; largest relative = %.3e\n", worst2, w2m, worst2rel);
    return 0;
}
