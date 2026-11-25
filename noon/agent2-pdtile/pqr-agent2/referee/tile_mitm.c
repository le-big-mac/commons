// tile_mitm.c -- referee: enumerate, by meet in the middle, ALL subsets A of Z_M (M = p0 p1 p2 <= 42) with
// Z_A containing a given pattern S and |A| = n, compute the exact pattern of each, and decide by brute force
// whether A tiles Z_M (search for B with A (+) B = Z_M).  Output: per exact pattern, #sets and #tiling sets.
// build: gcc -O2 -fopenmp -o tile_mitm tile_mitm.c
// run:   ./tile_mitm p0 p1 p2 outfile S:n [S:n ...]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>
typedef uint64_t set_t;
static int p[3], M;
static set_t FULL;
static int segoff[7], seglen[7], divd[7];
#define KL 48
static int8_t vecR[64][KL];
#define PL 100
static int cyc_cache_deg[64], cyc_cache[64][PL], cyc_have[64];
static void cyclo(int n, int *out, int *deg) {
    if (cyc_have[n]) { memcpy(out, cyc_cache[n], sizeof(int) * PL); *deg = cyc_cache_deg[n]; return; }
    int num[PL]; memset(num, 0, sizeof num);
    num[n] = 1; num[0] = -1; int nd = n;
    for (int e = 1; e < n; e++) if (n % e == 0) {
        int q[PL], qd; cyclo(e, q, &qd);
        int quo[PL]; memset(quo, 0, sizeof quo);
        int r[PL]; memcpy(r, num, sizeof r);
        for (int k = nd; k >= qd; k--) { int c = r[k]; if (c) { quo[k - qd] = c; for (int j = 0; j <= qd; j++) r[k - qd + j] -= c * q[j]; } }
        for (int k = 0; k < PL; k++) if (r[k]) { fprintf(stderr, "cyclo: inexact\n"); exit(1); }
        memcpy(num, quo, sizeof num); nd -= qd;
    }
    memcpy(cyc_cache[n], num, sizeof num); cyc_cache_deg[n] = nd; cyc_have[n] = 1;
    memcpy(out, num, sizeof(int) * PL); *deg = nd;
}
static void build_vectors(void) {
    divd[0] = p[0]; divd[1] = p[1]; divd[2] = p[2];
    divd[3] = p[0] * p[1]; divd[4] = p[0] * p[2]; divd[5] = p[1] * p[2]; divd[6] = M;
    int off = 0; memset(vecR, 0, sizeof vecR);
    for (int s = 0; s < 7; s++) {
        int phi[PL], deg; cyclo(divd[s], phi, &deg);
        segoff[s] = off; seglen[s] = deg;
        int cur[PL]; memset(cur, 0, sizeof cur); cur[0] = 1;
        for (int e = 0; e < M; e++) {
            for (int k = 0; k < deg; k++) vecR[e][off + k] = (int8_t)cur[k];
            for (int k = deg; k >= 1; k--) cur[k] = cur[k - 1];
            cur[0] = 0; int c = cur[deg];
            if (c) for (int k = 0; k <= deg; k++) cur[k] -= c * phi[k];
        }
        off += deg;
    }
    if (off != M - 1 || off > KL) { fprintf(stderr, "layout error\n"); exit(1); }
}
static inline set_t rotl(set_t A, int b) { return ((A << b) | (A >> (M - b))) & FULL; }
static int cover(set_t A, set_t covered) {
    if (covered == FULL) return 1;
    int u = __builtin_ctzll(~covered);
    set_t rem = A;
    while (rem) {
        int a = __builtin_ctzll(rem); rem &= rem - 1;
        int b = u - a; if (b < 0) b += M;
        if (b == 0) continue;
        set_t T = rotl(A, b);
        if (!(T & covered) && cover(A, covered | T)) return 1;
    }
    return 0;
}
typedef struct { uint8_t key[KL]; uint32_t idx; uint32_t pc; } rec_t;
static int cmprec(const void *a, const void *b) {
    int c = memcmp(((const rec_t *)a)->key, ((const rec_t *)b)->key, KL);
    if (c) return c;
    return (int)((const rec_t *)a)->pc - (int)((const rec_t *)b)->pc;
}
int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
    p[0] = atoi(argv[1]); p[1] = atoi(argv[2]); p[2] = atoi(argv[3]);
    M = p[0] * p[1] * p[2]; FULL = ((set_t)1 << M) - 1;
    build_vectors();
    int h1 = M / 2, h2 = M - h1;
    size_t n1 = (size_t)1 << h1, n2 = (size_t)1 << h2;
    int8_t (*R1)[KL] = malloc(n1 * KL), (*R2)[KL] = malloc(n2 * KL);
    memset(R1[0], 0, KL); memset(R2[0], 0, KL);
    for (size_t s = 1; s < n1; s++) { int b = __builtin_ctzl(s); size_t r = s & (s - 1); for (int k = 0; k < KL; k++) R1[s][k] = R1[r][k] + vecR[b][k]; }
    for (size_t s = 1; s < n2; s++) { int b = __builtin_ctzl(s); size_t r = s & (s - 1); for (int k = 0; k < KL; k++) R2[s][k] = R2[r][k] + vecR[h1 + b][k]; }
    int nj = argc - 5; int jS[64], jn[64];
    for (int i = 0; i < nj; i++) sscanf(argv[5 + i], "%d:%d", &jS[i], &jn[i]);
    static uint64_t cnt[64][128], til[64][128];
#pragma omp parallel for schedule(dynamic, 1)
    for (int job = 0; job < nj; job++) {
        int S = jS[job], n = jn[job];
        rec_t *a = malloc(n1 * sizeof(rec_t)), *b = malloc(n2 * sizeof(rec_t));
        uint8_t sel[KL]; memset(sel, 0, KL);
        for (int s = 0; s < 7; s++) if (S >> s & 1) for (int k = 0; k < seglen[s]; k++) sel[segoff[s] + k] = 1;
        size_t na = 0, nb = 0;
        for (size_t i = 0; i < n1; i++) { int pc = __builtin_popcountl(i); if (pc > n) continue;
            for (int k = 0; k < KL; k++) a[na].key[k] = sel[k] ? (uint8_t)(R1[i][k]) : 0; a[na].idx = (uint32_t)i; a[na].pc = pc; na++; }
        for (size_t i = 0; i < n2; i++) { int pc = __builtin_popcountl(i); if (pc > n) continue;
            for (int k = 0; k < KL; k++) b[nb].key[k] = sel[k] ? (uint8_t)(-R2[i][k]) : 0; b[nb].idx = (uint32_t)i; b[nb].pc = pc; nb++; }
        qsort(a, na, sizeof(rec_t), cmprec); qsort(b, nb, sizeof(rec_t), cmprec);
        size_t i = 0, j = 0;
        while (i < na && j < nb) {
            int c = memcmp(a[i].key, b[j].key, KL);
            if (c < 0) { i++; continue; }
            if (c > 0) { j++; continue; }
            size_t i2 = i, j2 = j;
            size_t sa[34], sb[34];   // bucket starts by popcount inside the group
            for (int u = 0; u < 34; u++) { sa[u] = (size_t)-1; sb[u] = (size_t)-1; }
            while (i2 < na && memcmp(a[i2].key, a[i].key, KL) == 0) { if (sa[a[i2].pc] == (size_t)-1) sa[a[i2].pc] = i2; i2++; }
            while (j2 < nb && memcmp(b[j2].key, b[j].key, KL) == 0) { if (sb[b[j2].pc] == (size_t)-1) sb[b[j2].pc] = j2; j2++; }
            for (int u = 0; u <= n && u <= h1; u++) {
                int v = n - u; if (v > h2) continue;
                if (sa[u] == (size_t)-1 || sb[v] == (size_t)-1) continue;
                for (size_t ii = sa[u]; ii < i2 && a[ii].pc == (uint32_t)u; ii++)
                    for (size_t jj = sb[v]; jj < j2 && b[jj].pc == (uint32_t)v; jj++) {
                        set_t A = (set_t)a[ii].idx | ((set_t)b[jj].idx << h1);
                        int mask = 0;
                        for (int s = 0; s < 7; s++) {
                            int z = 1;
                            for (int k = 0; k < seglen[s]; k++) if ((int8_t)(R1[a[ii].idx][segoff[s] + k] + R2[b[jj].idx][segoff[s] + k])) { z = 0; break; }
                            mask |= z << s;
                        }
                        cnt[job][mask]++;
                        if (M % n == 0 && cover(A, A)) til[job][mask]++;
                    }
            }
            i = i2; j = j2;
        }
        free(a); free(b);
    }
    FILE *f = fopen(argv[4], "w");
    fprintf(f, "# S n exactmask count tilingcount   (ALL subsets of Z_%d)\n", M);
    for (int job = 0; job < nj; job++) for (int m = 0; m < 128; m++) if (cnt[job][m])
        fprintf(f, "%d %d %d %llu %llu\n", jS[job], jn[job], m, (unsigned long long)cnt[job][m], (unsigned long long)til[job][m]);
    fclose(f);
    printf("done\n");
    return 0;
}
