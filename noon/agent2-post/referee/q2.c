/* Referee's blind search for a witness to K(3) <= 5 (4 pegs, 6 colours):
 * g1..g4 blind, g5 = g5(a1).  Need: for every a1 a g5 with (a2,a3,a4,a5)
 * injective on C(a1).  Simulated annealing on (g1,g2,g3,g4);
 * score = sum over a1 of min over g5 of (codes in C(a1) - distinct signatures).
 * usage: q2 seed seconds
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define P 4
#define C 6
#define N 1296
#define NA 14
static unsigned char A[N][N];
static int dig[N][P];
static unsigned long long rs;
static unsigned rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static void init(void) {
    int amap[P + 1][P + 1], k = 0;
    for (int b = 0; b <= P; b++) for (int w = 0; w + b <= P; w++) { if (b == P - 1 && w == 1) { amap[b][w] = -1; continue; } amap[b][w] = k++; }
    for (int i = 0; i < N; i++) { int x = i; for (int p = P - 1; p >= 0; p--) { dig[i][p] = x % C; x /= C; } }
    for (int g = 0; g < N; g++) for (int c = 0; c < N; c++) {
        int b = 0, cg[C] = {0}, cc[C] = {0};
        for (int p = 0; p < P; p++) { if (dig[g][p] == dig[c][p]) b++; cg[dig[g][p]]++; cc[dig[c][p]]++; }
        int s = 0; for (int q = 0; q < C; q++) s += cg[q] < cc[q] ? cg[q] : cc[q];
        A[g][c] = (unsigned char)amap[b][s - b];
    }
}
static int best5[NA];  /* g5 chosen for each a1 (0 where any g5 will do) */
static int keyv[N];
static int cmpk(const void *a, const void *b) { int x = keyv[*(const int *)a], y = keyv[*(const int *)b]; return x < y ? -1 : x > y; }
static int eval(const int *g) {
    static int ord[N];
    for (int c = 0; c < N; c++) { keyv[c] = ((A[g[0]][c] * NA + A[g[1]][c]) * NA + A[g[2]][c]) * NA + A[g[3]][c]; ord[c] = c; }
    qsort(ord, N, sizeof(int), cmpk);
    /* groups of size>=2, per a1 */
    static int gc[N], gstart[N + 1], ga1[N]; int ng = 0, m = 0;
    for (int i = 0; i < N;) {
        int j = i; while (j < N && keyv[ord[j]] == keyv[ord[i]]) j++;
        if (j - i >= 2) { gstart[ng] = m; ga1[ng] = A[g[0]][ord[i]]; for (int k = i; k < j; k++) gc[m++] = ord[k]; ng++; }
        i = j;
    }
    gstart[ng] = m;
    int total = 0;
    for (int i = 0; i < ng;) {
        int j = i; while (j < ng && ga1[j] == ga1[i]) j++;
        int best = 1 << 30, bg = -1;
        for (int g5 = 0; g5 < N; g5++) {
            int coll = 0; const unsigned char *row = A[g5];
            for (int q = i; q < j && coll < best; q++) {
                unsigned mask = 0; int sz = gstart[q + 1] - gstart[q];
                for (int k = gstart[q]; k < gstart[q + 1]; k++) mask |= 1u << row[gc[k]];
                coll += sz - __builtin_popcount(mask);
            }
            if (coll < best) { best = coll; bg = g5; if (!best) break; }
        }
        best5[ga1[i]] = bg; total += best;
        i = j;
    }
    return total;
}
int main(int argc, char **argv) {
    rs = 88172645463325252ULL ^ ((unsigned long long)atoi(argv[1]) * 0x9E3779B97F4A7C15ULL);
    double secs = atof(argv[2]);
    init();
    time_t t0 = time(NULL);
    int g[4], best = 1 << 30; long it = 0;
    while (difftime(time(NULL), t0) < secs) {
        for (int i = 0; i < 4; i++) g[i] = rnd() % N;
        int cur = eval(g); double Tm = 3.0;
        for (int step = 0; step < 4000 && cur > 0; step++, it++) {
            int ng[4]; memcpy(ng, g, sizeof g);
            int i = rnd() % 4;
            if (rnd() % 3 == 0) ng[i] = rnd() % N;
            else { int p = rnd() % 4, pw = 1; for (int k = 0; k < 3 - p; k++) pw *= 6; int d = dig[ng[i]][p]; int nd = rnd() % 6; ng[i] += (nd - d) * pw; }
            int s = eval(ng);
            if (s <= cur || exp((cur - s) / Tm) * 4294967296.0 > (double)rnd()) { memcpy(g, ng, sizeof g); cur = s; }
            Tm *= 0.9985; if (Tm < 0.3) Tm = 0.3;
            if (cur < best) { best = cur; printf("seed %s it %ld best %d: %d %d %d %d\n", argv[1], it, best, g[0], g[1], g[2], g[3]); fflush(stdout); }
            if ((step & 63) == 0 && difftime(time(NULL), t0) >= secs) break;
        }
        if (cur == 0) {
            eval(g);
            printf("WITNESS g1..g4 = %d %d %d %d ; g5 by a1:", g[0], g[1], g[2], g[3]);
            for (int a = 0; a < NA; a++) printf(" %d", best5[a]);
            printf("\n"); fflush(stdout);
            return 0;
        }
    }
    printf("seed %s: no witness in %.0f s, best score %d, %ld evaluations\n", argv[1], secs, best, it);
    return 0;
}
