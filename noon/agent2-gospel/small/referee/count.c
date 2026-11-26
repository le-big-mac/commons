// count.c -- how many cosets and terms SHOULD there be?  From Euler's function (by factoring m) and the
// order of 2, with no orbit marking: an independent tally to set beside the totals periods.c printed.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <omp.h>
int main(int argc, char **argv) {
    uint32_t N = argc > 1 ? (uint32_t)atol(argv[1]) : 2000000u;
    uint32_t *spf = calloc(N + 1, sizeof(uint32_t));
    for (uint32_t i = 2; i <= N; i++) if (!spf[i]) for (uint32_t j = i; j <= N; j += i) if (!spf[j]) spf[j] = i;
    long long terms = 0, zero_cosets = 0, real = 0, cplx = 0, zero_m = 0, nonzero_m = 0, bad = 0;
    #pragma omp parallel for schedule(dynamic, 64) reduction(+:terms,zero_cosets,real,cplx,zero_m,nonzero_m,bad)
    for (int64_t mm = 3; mm <= (int64_t)N; mm += 2) {
        uint32_t m = (uint32_t)mm, r = m, rad = 1; uint64_t phi = m;
        while (r > 1) { uint32_t p = spf[r]; rad *= p; phi = phi / p * (p - 1); while (r % p == 0) r /= p; }
        uint32_t n = 0, x = 1; int self = 0;
        do { x = (x * 2) % m; n++; if (x == m - 1) self = 1; } while (x != 1);
        uint32_t nr = 0; x = 1;
        do { x = (x * 2) % rad; nr++; } while (x != 1);
        if (phi % n) bad++;
        if (!self && (phi / n) % 2) bad++;
        long long cos_ = self ? phi / n : phi / n / 2;
        terms += cos_ * (long long)n;
        if (nr != n) { zero_cosets += cos_; zero_m++; } else { nonzero_m++; if (self) real += cos_; else cplx += cos_; }
    }
    printf("N=%u terms=%lld zero m=%lld non-zero m=%lld zero cosets=%lld real cosets=%lld complex pairs=%lld inconsistencies=%lld\n", N, terms, zero_m, nonzero_m, zero_cosets, real, cplx, bad);
    return 0;
}
