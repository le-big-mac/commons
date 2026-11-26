// hprime.c -- the model's H with the TRUE mean square of the sums of each m in place of n.
// For the cosets C of <2> mod m: sum_C |S_C|^2 = T(m) = sum_{h in <2>} c_m(h-1) (exact, Ramanujan sums), so the
// mean square over the d = phi/n cosets is V = T/d, not n.  H = sum 2/sqrt(2 pi n), H' = sum 2/sqrt(2 pi V), real cosets only.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static uint32_t *spf;
static uint32_t gcd32(uint32_t a, uint32_t b) { while (b) { uint32_t t = a % b; a = b; b = t; } return a; }
static void muphi(uint32_t k, int *mu, int64_t *phi) {
    int m_ = 1; int64_t p_ = 1;
    while (k > 1) { uint32_t p = spf[k]; int e = 0; while (k % p == 0) { k /= p; e++; p_ *= (e == 1) ? (p - 1) : p; } if (e > 1) m_ = 0; else m_ = -m_; }
    *mu = m_; *phi = p_;
}
int main(int argc, char **argv) {
    uint32_t N = (uint32_t)atol(argv[1]);
    spf = calloc(N + 1, sizeof(uint32_t));
    for (uint32_t i = 2; i <= N; i++) if (!spf[i]) for (uint32_t j = i; j <= N; j += i) if (!spf[j]) spf[j] = i;
    double H = 0, Hp = 0; long long cosets = 0; double ratio_min = 9, ratio_max = 0;
    for (uint32_t m = 3; m <= N; m += 2) {
        int mu_m; int64_t phi_m; muphi(m, &mu_m, &phi_m);
        uint32_t rad = 1, r = m;
        while (r > 1) { uint32_t p = spf[r]; rad *= p; while (r % p == 0) r /= p; }
        uint32_t n = 0, x = 1; int self = 0; double T = 0;
        do {
            if (x == m - 1) self = 1;
            uint32_t g = (x == 1) ? m : gcd32(m, x - 1);
            int mu_q; int64_t phi_q; muphi(m / g, &mu_q, &phi_q);
            T += (double)mu_q * (double)(phi_m / phi_q);
            x = (x * 2) % m; n++;
        } while (x != 1);
        uint32_t nr = 0; x = 1;
        do { x = (x * 2) % rad; nr++; } while (x != 1);
        if (nr != n || !self) continue;
        double d = (double)(phi_m / n), V = T / d;
        cosets += phi_m / n; H += d * 2 / sqrt(2 * M_PI * n); Hp += d * 2 / sqrt(2 * M_PI * V);
        if (V / n < ratio_min) ratio_min = V / n;
        if (V / n > ratio_max) ratio_max = V / n;
    }
    printf("odd m <= %u: real cosets %lld ; H = %.4f ; H' (true mean square) = %.4f ; H'/H = %.4f ; V/n runs from %.3f to %.3f\n", N, cosets, H, Hp, Hp / H, ratio_min, ratio_max);
    return 0;
}
