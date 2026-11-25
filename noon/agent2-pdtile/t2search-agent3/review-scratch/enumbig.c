/* As enum36.c but for M up to 127 (128-bit masks) and with a size cap KMAX: all sets A containing 0 with |A| <= KMAX and A - A != Z_M
   that pass (F2) [the complement of A is inside A + T, T = Z_M \ (A - A)], one representative per affine orbit (smallest mask containing 0).
   (F2) is evaluated as:  the set { y : y - A inside D } = intersection over x in A of (D + x) must be inside A.   usage: enumbig KMAX outfile */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#ifndef M
#define M 72
#endif
typedef unsigned __int128 u128;
static u128 FULL;
static int nunits = 0, mulperm[M][M], KMAX;
static unsigned long long nodes = 0, pass2 = 0, canon = 0, bysize_nodes[M + 1], bysize_pass[M + 1], bysize_canon[M + 1];
static FILE *out;
static inline u128 rot(u128 a, int t) { return t ? (((a << t) | (a >> (M - t))) & FULL) : a; }
static int gcd(int a, int b) { return b ? gcd(b, a % b) : a; }
static int is_canonical(u128 A, int *el, int k) {
    for (int ui = 0; ui < nunits; ui++) {
        u128 B = 0;
        for (int i = 0; i < k; i++) B |= ((u128)1) << mulperm[ui][el[i]];
        for (int i = 0; i < k; i++) {
            int b = mulperm[ui][el[i]];
            u128 C = rot(B, (M - b) % M);
            if (C < A) return 0;
        }
    }
    return 1;
}
static int el[M];
static void dfs(u128 A, u128 D, int last, int k) {
    nodes++; bysize_nodes[k]++;
    if (k >= 2) {
        u128 I = FULL;
        for (int i = 0; i < k; i++) I &= rot(D, el[i]);
        if ((I & ~A) == 0) {
            pass2++; bysize_pass[k]++;
            if (is_canonical(A, el, k)) { canon++; bysize_canon[k]++; fprintf(out, "%llx%016llx\n", (unsigned long long)(A >> 64), (unsigned long long)A); }
        }
    }
    if (k == KMAX) return;
    for (int x = last + 1; x < M; x++) {
        u128 D2 = D;
        for (int i = 0; i < k; i++) { int d = x - el[i]; D2 |= (((u128)1) << d) | (((u128)1) << (M - d)); }
        D2 &= FULL;
        if (D2 == FULL) continue;
        el[k] = x;
        dfs(A | (((u128)1) << x), D2, x, k + 1);
    }
}
int main(int argc, char **argv) {
    FULL = (((u128)1) << M) - 1;
    KMAX = atoi(argv[1]);
    for (int u = 1; u < M; u++) if (gcd(u, M) == 1) { for (int x = 0; x < M; x++) mulperm[nunits][x] = (u * x) % M; nunits++; }
    out = fopen(argv[2], "w");
    el[0] = 0;
    dfs(1, 1, 0, 1);
    fclose(out);
    printf("M = %d, sizes <= %d: sets containing 0 with A - A != Z_M: %llu;  passing (F2): %llu;  affine-orbit representatives written: %llu\n", M, KMAX, nodes, pass2, canon);
    for (int k = 1; k <= M; k++) if (bysize_nodes[k]) printf("  size %2d: %14llu sets, %10llu pass (F2), %8llu orbit representatives\n", k, bysize_nodes[k], bysize_pass[k], bysize_canon[k]);
    return 0;
}
