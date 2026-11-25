/* Exhaustive enumeration for Z_M (M = 36 by default) of all sets A containing 0 with A - A != Z_M.
   Rigorous facts used (independent of the scripts under review):
     (F1) if 1_A * f = 1, f >= 0, f(0) = 1 then f vanishes on (A - A) \ {0}   [evaluate at y in A]
          so if A - A = Z_M then f = delta_0 and A = Z_M.  Supersets of a set with full difference set have full difference set: prune.
     (F2) with T = Z_M \ (A - A): every y not in A needs (y - A) meeting T, i.e. the complement of A is inside A + T.
   Sets passing (F2) are written out (one per orbit of x -> u x + t: the member containing 0 with the smallest bit mask). */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#ifndef M
#define M 36
#endif
typedef uint64_t u64;
static const u64 FULL = (((u64)1) << M) - 1;
static int units[M], nunits = 0, mulperm[M][M];
static unsigned long long nodes = 0, pass2 = 0, canon = 0, bysize_nodes[M + 1], bysize_pass[M + 1], bysize_canon[M + 1];
static FILE *out;
static inline u64 rot(u64 a, int t) { return t ? (((a << t) | (a >> (M - t))) & FULL) : a; }
static int gcd(int a, int b) { return b ? gcd(b, a % b) : a; }
static int is_canonical(u64 A) {
    int el[M], k = 0;
    for (int x = 0; x < M; x++) if (A >> x & 1) el[k++] = x;
    for (int ui = 0; ui < nunits; ui++) {
        u64 B = 0;
        for (int i = 0; i < k; i++) B |= ((u64)1) << mulperm[ui][el[i]];
        /* translates of B containing 0: B - b for b in B */
        for (int i = 0; i < k; i++) {
            int b = mulperm[ui][el[i]];
            u64 C = rot(B, (M - b) % M);
            if (C < A) return 0;
        }
    }
    return 1;
}
static void dfs(u64 A, u64 D, int last, int k) {
    nodes++; bysize_nodes[k]++;
    if (k >= 2) {
        u64 T = ~D & FULL, S = 0, t = T;
        while (t) { int b = __builtin_ctzll(t); t &= t - 1; S |= rot(A, b); }
        if (((~A & FULL) & ~S) == 0) {
            pass2++; bysize_pass[k]++;
            if (is_canonical(A)) { canon++; bysize_canon[k]++; fprintf(out, "%llx\n", (unsigned long long)A); }
        }
    }
    for (int x = last + 1; x < M; x++) {
        u64 D2 = D, a = A;
        while (a) { int b = __builtin_ctzll(a); a &= a - 1; int d = x - b; D2 |= (((u64)1) << d) | (((u64)1) << (M - d)); }
        D2 &= FULL;
        if (D2 == FULL) continue;
        dfs(A | (((u64)1) << x), D2, x, k + 1);
    }
}
int main(int argc, char **argv) {
    for (int u = 1; u < M; u++) if (gcd(u, M) == 1) { for (int x = 0; x < M; x++) mulperm[nunits][x] = (u * x) % M; units[nunits++] = u; }
    out = fopen(argc > 1 ? argv[1] : "cand.txt", "w");
    dfs(1, 1, 0, 1);
    fclose(out);
    printf("M = %d: sets containing 0 with A - A != Z_M: %llu;  passing (F2): %llu;  affine-orbit representatives written: %llu\n", M, nodes, pass2, canon);
    for (int k = 1; k <= M; k++) if (bysize_nodes[k]) printf("  size %2d: %12llu sets, %10llu pass (F2), %8llu orbit representatives\n", k, bysize_nodes[k], bysize_pass[k], bysize_canon[k]);
    return 0;
}
