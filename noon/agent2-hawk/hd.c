/* Hawks and doves on a lattice.   usage: hd MODE r L GENERATIONS SEED FROM EVERY [SNAPFILE SNAPEVERY]
   MODE: lattice4 | lattice8 | mixed4 | sync4.   Prints: mode r share_mean share_end doves_end dove_neighbours_per_dove_end
   and, on following lines starting with "t", the share at every EVERY-th generation.
   Site value 1 = dove, 0 = hawk.  Payoffs: D-D 1, D-H 1-r, H-D 1+r, H-H 0.  Rule and units as in expectations.md. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint64_t st[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t rnd(void) { uint64_t r = rotl(st[1] * 5, 7) * 9, t = st[1] << 17; st[2] ^= st[0]; st[3] ^= st[1]; st[1] ^= st[2]; st[0] ^= st[3]; st[2] ^= t; st[3] = rotl(st[3], 45); return r; }
static inline double uni(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static void seed(uint64_t s) { for (int i = 0; i < 4; i++) { s += 0x9E3779B97F4A7C15ULL; uint64_t z = s; z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; st[i] = z ^ (z >> 31); } }
static int L, N, K; static unsigned char *s; static int *nb; static double r;
static inline double payoff(int i) { int nd = 0; for (int j = 0; j < K; j++) nd += s[nb[i * K + j]]; return s[i] ? nd + (K - nd) * (1.0 - r) : nd * (1.0 + r); }
int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "usage\n"); return 2; }
    const char *mode = argv[1]; r = atof(argv[2]); L = atoi(argv[3]); long G = atol(argv[4]); seed(strtoull(argv[5], 0, 10)); long from = atol(argv[6]), every = atol(argv[7]);
    FILE *snap = argc > 9 ? fopen(argv[8], "wb") : 0; long snapevery = argc > 9 ? atol(argv[9]) : 0;
    K = strcmp(mode, "lattice8") == 0 ? 8 : 4; N = L * L; s = malloc(N); nb = malloc(sizeof(int) * N * K);
    for (int y = 0; y < L; y++) for (int x = 0; x < L; x++) { int i = y * L + x, xm = (x + L - 1) % L, xp = (x + 1) % L, ym = (y + L - 1) % L, yp = (y + 1) % L;
        nb[i * K] = y * L + xm; nb[i * K + 1] = y * L + xp; nb[i * K + 2] = ym * L + x; nb[i * K + 3] = yp * L + x;
        if (K == 8) { nb[i * K + 4] = ym * L + xm; nb[i * K + 5] = ym * L + xp; nb[i * K + 6] = yp * L + xm; nb[i * K + 7] = yp * L + xp; } }
    double p0 = getenv("HD_P0") ? atof(getenv("HD_P0")) : 0.5;      /* share of doves at the start; one half unless HD_P0 is set (used only in the checks made afterwards) */
    for (int i = 0; i < N; i++) s[i] = uni() < p0;
    double alpha = K * (1.0 + r), sum = 0; long cnt = 0; int mixed = strcmp(mode, "mixed4") == 0, sync = strcmp(mode, "sync4") == 0;
    unsigned char *s2 = sync ? malloc(N) : 0; double *P = sync ? malloc(sizeof(double) * N) : 0;
    long *list = 0; int nlist = 0, li = 0;      /* HD_SNAPLIST: a file of generations (ascending) at which to write the lattice, in place of every SNAPEVERY-th */
    if (snap && getenv("HD_SNAPLIST")) { FILE *fl = fopen(getenv("HD_SNAPLIST"), "r"); list = malloc(sizeof(long) * 100000); while (fl && nlist < 100000 && fscanf(fl, "%ld", &list[nlist]) == 1) nlist++; if (fl) fclose(fl); }
    if (snap) fwrite(s, 1, N, snap);
    for (long g = 1; g <= G; g++) {
        if (sync) {
            for (int i = 0; i < N; i++) P[i] = payoff(i);
            for (int i = 0; i < N; i++) { int y = nb[i * K + (int)(rnd() % K)]; s2[i] = (P[y] > P[i] && uni() < (P[y] - P[i]) / alpha) ? s[y] : s[i]; }
            memcpy(s, s2, N);
        } else if (mixed) {
            for (int n = 0; n < N; n++) { int x = rnd() % N, y = rnd() % N; if (x == y || s[x] == s[y]) continue;
                double px = 0, py = 0; for (int j = 0; j < K; j++) { int o = s[rnd() % N]; px += s[x] ? (o ? 1.0 : 1.0 - r) : (o ? 1.0 + r : 0.0); o = s[rnd() % N]; py += s[y] ? (o ? 1.0 : 1.0 - r) : (o ? 1.0 + r : 0.0); }
                if (py > px && uni() < (py - px) / alpha) s[x] = s[y]; }
        } else {
            for (int n = 0; n < N; n++) { int x = rnd() % N, y = nb[x * K + (int)(rnd() % K)]; if (s[x] == s[y]) continue;
                double px = payoff(x), py = payoff(y); if (py > px && uni() < (py - px) / alpha) s[x] = s[y]; }
        }
        if (g % every == 0) { long d = 0; for (int i = 0; i < N; i++) d += s[i]; double f = (double)d / N; printf("t %ld %.6f\n", g, f); if (g > from) { sum += f; cnt++; } }
        if (snap && (nlist ? (li < nlist && g == list[li] && ++li) : g % snapevery == 0)) fwrite(s, 1, N, snap);
    }
    long d = 0, dn = 0; for (int i = 0; i < N; i++) if (s[i]) { d++; for (int j = 0; j < K; j++) dn += s[nb[i * K + j]]; }
    printf("R %s %.4f %.6f %.6f %ld %.6f\n", mode, r, cnt ? sum / cnt : -1.0, (double)d / N, d, d ? (double)dn / d : 0.0);
    if (snap) fclose(snap); return 0;
}
