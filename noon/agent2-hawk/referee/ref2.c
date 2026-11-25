// Referee's blind program: hawk-dove on a periodic lattice.
// usage: ref mode k r L gens seed [meanfrom]   mode: 0 one-at-a-time, 1 all-at-once, 2 well-mixed
// s[i]=1 dove, 0 hawk.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint64_t S[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t rnd(void) {
    uint64_t r = rotl(S[1] * 5, 7) * 9, t = S[1] << 17;
    S[2] ^= S[0]; S[3] ^= S[1]; S[1] ^= S[2]; S[0] ^= S[3]; S[2] ^= t; S[3] = rotl(S[3], 45);
    return r;
}
static uint64_t sm(uint64_t *x) { uint64_t z = (*x += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static inline uint32_t below(uint32_t n) { return (uint32_t)(((unsigned __int128)rnd() * n) >> 64); }
static inline double u01(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }

int L, N, K; double r;
uint8_t *s; int32_t *nb;

static inline double pay(int x) {
    int n = 0; const int32_t *p = nb + (size_t)x * K;
    for (int j = 0; j < K; j++) n += s[p[j]];
    return s[x] ? K * (1 - r) + n * r : n * (1 + r);
}
static inline double paymix(int x) { // K opponents drawn afresh from the whole lattice
    int n = 0; for (int j = 0; j < K; j++) n += s[below(N)];
    return s[x] ? K * (1 - r) + n * r : n * (1 + r);
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "args\n"); return 1; }
    int mode = atoi(argv[1]); K = atoi(argv[2]); r = atof(argv[3]); L = atoi(argv[4]);
    int gens = atoi(argv[5]); uint64_t seed = strtoull(argv[6], 0, 10);
    int from = argc > 7 ? atoi(argv[7]) : (gens * 2) / 3; // mean over gens from+1..gens, read every 50
    N = L * L; uint64_t z = seed; for (int i = 0; i < 4; i++) S[i] = sm(&z);
    s = malloc(N); nb = malloc(sizeof(int32_t) * (size_t)N * K);
    static const int dx[8] = {1, -1, 0, 0, 1, 1, -1, -1}, dy[8] = {0, 0, 1, -1, 1, -1, 1, -1};
    for (int i = 0; i < L; i++) for (int j = 0; j < L; j++) for (int q = 0; q < K; q++)
        nb[((size_t)i * L + j) * K + q] = ((i + dx[q] + L) % L) * L + (j + dy[q] + L) % L;
    long doves = 0; for (int i = 0; i < N; i++) { s[i] = rnd() >> 63; doves += s[i]; }
    double norm = 1.0 / (K * (1 + r)), sum = 0; int nread = 0;
    double *P = mode == 1 ? malloc(sizeof(double) * N) : 0; uint8_t *t = mode == 1 ? malloc(N) : 0;
    long firstzero = -1, firstall = -1; double trace[10]; int tg[10];
    for (int q = 0; q < 10; q++) { trace[q] = -1; tg[q] = (int)((long)gens * (q + 1) / 10); }
    double rmain = r; int gpre = argc > 9 ? atoi(argv[9]) : 0; if (gpre) { r = atof(argv[8]); norm = 1.0 / (K * (1 + r)); }
    for (int g = 1 - gpre; g <= gens; g++) {
        if (g == 1) { r = rmain; norm = 1.0 / (K * (1 + r)); }
        if (doves > 0 && doves < N) {
            if (mode == 0) {
                for (int c = 0; c < N; c++) {
                    int x = below(N), y = nb[(size_t)x * K + below(K)];
                    if (s[x] == s[y]) continue;
                    double d = pay(y) - pay(x);
                    if (d > 0 && u01() < d * norm) { doves += (int)s[y] - (int)s[x]; s[x] = s[y]; }
                }
            } else if (mode == 2) {
                for (int c = 0; c < N; c++) {
                    int x = below(N), y = below(N);
                    double px = paymix(x), py = paymix(y);
                    if (s[x] == s[y]) continue;
                    double d = py - px;
                    if (d > 0 && u01() < d * norm) { doves += (int)s[y] - (int)s[x]; s[x] = s[y]; }
                }
            } else {
                for (int x = 0; x < N; x++) P[x] = pay(x);
                for (int x = 0; x < N; x++) {
                    int y = nb[(size_t)x * K + below(K)]; t[x] = s[x];
                    double d = P[y] - P[x];
                    if (s[x] != s[y] && d > 0 && u01() < d * norm) t[x] = s[y];
                }
                memcpy(s, t, N); doves = 0; for (int x = 0; x < N; x++) doves += s[x];
            }
            if (doves == 0 && firstzero < 0) firstzero = g;
            if (doves == N && firstall < 0) firstall = g;
        }
        if (g > from && g % 50 == 0) { sum += (double)doves / N; nread++; }
        for (int q = 0; q < 10; q++) if (g == tg[q]) trace[q] = (double)doves / N;
    }
    // clumping at the end: mean dove neighbours of a dove
    double dn = 0; for (int x = 0; x < N; x++) if (s[x]) { for (int j = 0; j < K; j++) dn += s[nb[(size_t)x * K + j]]; }
    long hh[9] = {0}; for (int x = 0; x < N; x++) if (!s[x]) { int h = 0; for (int j = 0; j < K; j++) h += !s[nb[(size_t)x * K + j]]; hh[h]++; }
    printf("mode=%d k=%d r=%.3f L=%d gens=%d seed=%llu share=%.5f end_doves=%ld end_share=%.5f dove_nb_of_dove=%.4f k_x_share=%.4f extinct_gen=%ld allD_gen=%ld pre=%d hawks_by_hawk_nb(0,1,2,3,4+)=%ld,%ld,%ld,%ld,%ld trace@tenths=%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n",
           mode, K, r, L, gens, (unsigned long long)seed, sum / nread, doves, (double)doves / N,
           doves ? dn / doves : 0.0, K * (double)doves / N, firstzero, firstall,
           gpre, hh[0], hh[1], hh[2], hh[3], hh[4] + hh[5] + hh[6] + hh[7] + hh[8], trace[0], trace[1], trace[2], trace[3], trace[4], trace[5], trace[6], trace[7], trace[8], trace[9]);
    return 0;
}
