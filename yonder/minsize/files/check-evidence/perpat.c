// Per-pattern exhaustive search. For a pattern P on Z_M: every multiset A with Phi_d | A(X) for all d in P
// is A = G*C with G = prod_{d in P} Phi_d (monic, degree D) and C an integer polynomial of degree < f = M - D,
// and its top f coefficients A_D..A_{M-1} determine C. So: enumerate all nonnegative top parts with sum <= B,
// compute the forced low coefficients, keep A if all are >= 0 and the size is <= B, and test exactly whether
// any Phi_d with d not in P divides (remainders supplied as a table). Prints the least size with EXACT pattern P.
// input (stdin): M D f B ; g_0..g_D ; nother ; for each other d: phi_d, then M rows of phi_d ints (X^h mod Phi_d)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int M, D, f, B, g[64], nother, phi[8], rem[8][32][16];
static long long c[32], A[32];
static int best = 1 << 30; static long long bestA[32]; static unsigned long long leaves;
static void leaf(void) {
    leaves++;
    long long tot = 0;
    for (int j = 0; j < M; j++) { long long s = 0;
        for (int i = (j - D > 0 ? j - D : 0); i <= j && i < f; i++) s += g[j - i] * c[i];
        if (s < 0) return; A[j] = s; tot += s; if (tot > B) return; }
    if (tot == 0 || tot >= best) return;
    for (int o = 0; o < nother; o++) { int zero = 1;
        for (int t = 0; t < phi[o] && zero; t++) { long long s = 0; for (int h = 0; h < M; h++) s += A[h] * rem[o][h][t]; if (s) zero = 0; }
        if (zero) return; }   // some Phi_d outside P divides: pattern not exact
    best = (int)tot; memcpy(bestA, A, sizeof A);
}
static void dfs(int i, int used) {
    if (i < 0) { leaf(); return; }
    long long s = 0; for (int i2 = i + 1; i2 < f && i2 - i <= D; i2++) s += g[D + i - i2] * c[i2];
    for (int h = 0; used + h <= B; h++) { c[i] = h - s; dfs(i - 1, used + h); }
}
int main(void) {
    if (scanf("%d %d %d %d", &M, &D, &f, &B) != 4) return 1;
    for (int i = 0; i <= D; i++) if (scanf("%d", &g[i]) != 1) return 1;
    if (scanf("%d", &nother) != 1) return 1;
    for (int o = 0; o < nother; o++) { if (scanf("%d", &phi[o]) != 1) return 1;
        for (int h = 0; h < M; h++) for (int t = 0; t < phi[o]; t++) if (scanf("%d", &rem[o][h][t]) != 1) return 1; }
    dfs(f - 1, 0);
    if (best == 1 << 30) printf("none leaves %llu\n", leaves);
    else { printf("least %d leaves %llu marks", best, leaves); for (int h = 0; h < M; h++) for (long long r = 0; r < bestA[h]; r++) printf(" %d", h); printf("\n"); }
    return 0;
}
