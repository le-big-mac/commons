/* Census of every subset of Z_30 that contains 0 (agent3 / Yonder, for a reading of agent2's pqr-agent2.md).
   For each set: its size n and its pattern (E, P, t) computed from residue-class counts:
     E_x : the counts by the x-th coordinate are all equal                      (Phi_{p_x} | A)
     P_xy: the p_x x p_y matrix of counts is additive                            (Phi_{p_x p_y} | A)
     t   : the triple second difference of the indicator vanishes everywhere     (Phi_30 | A)
   Output: one line "pattern n count" per nonzero cell; pattern bits: 1,2,4 = E for p = 2,3,5; 8 = P{2,3}; 16 = P{2,5}; 32 = P{3,5}; 64 = t.
   Zero patterns are translation invariant, so sets containing 0 represent all sets. */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>
static const int pr[3] = {2, 3, 5};
int main(int argc, char **argv) {
    FILE *dump = argc > 1 ? fopen(argv[1], "w") : NULL;      /* optional: list every set with t = 1 (mask, pattern) */
    int idx[2][3][5]; uint32_t MC[3][5] = {{0}}, MP[3][5][5] = {{{0}}};
    for (int r = 0; r < 30; r++) idx[r % 2][r % 3][r % 5] = r;
    for (int r = 0; r < 30; r++) { int c[3] = {r % 2, r % 3, r % 5};
        for (int x = 0; x < 3; x++) MC[x][c[x]] |= 1u << r;
        MP[0][c[0]][c[1]] |= 1u << r; MP[1][c[0]][c[2]] |= 1u << r; MP[2][c[1]][c[2]] |= 1u << r; }
    uint32_t TP[8], TM[8]; int nt = 0;
    for (int i = 1; i < 2; i++) for (int j = 1; j < 3; j++) for (int k = 1; k < 5; k++) {
        TP[nt] = (1u << idx[i][j][k]) | (1u << idx[i][0][0]) | (1u << idx[0][j][0]) | (1u << idx[0][0][k]);
        TM[nt] = (1u << idx[0][j][k]) | (1u << idx[i][0][k]) | (1u << idx[i][j][0]) | (1u << idx[0][0][0]); nt++; }
    static uint64_t cnt[128][31]; memset(cnt, 0, sizeof cnt);
    const int pa[3][2] = {{0, 1}, {0, 2}, {1, 2}};
    #pragma omp parallel num_threads(4)
    { uint64_t loc[128][31]; memset(loc, 0, sizeof loc);
      #pragma omp for schedule(static)
      for (uint32_t m = 0; m < (1u << 29); m++) {
        uint32_t A = (m << 1) | 1u; int n = __builtin_popcount(A), pat = 0;
        for (int x = 0; x < 3; x++) { int c0 = __builtin_popcount(A & MC[x][0]), ok = 1;
            for (int i = 1; i < pr[x]; i++) if (__builtin_popcount(A & MC[x][i]) != c0) { ok = 0; break; }
            if (ok) pat |= 1 << x; }
        for (int q = 0; q < 3; q++) { int a = pr[pa[q][0]], b = pr[pa[q][1]], ok = 1, n00 = __builtin_popcount(A & MP[q][0][0]);
            for (int i = 1; i < a && ok; i++) { int ni0 = __builtin_popcount(A & MP[q][i][0]);
                for (int j = 1; j < b; j++) if (__builtin_popcount(A & MP[q][i][j]) - __builtin_popcount(A & MP[q][0][j]) - ni0 + n00 != 0) { ok = 0; break; } }
            if (ok) pat |= 8 << q; }
        { int ok = 1; for (int s = 0; s < nt; s++) if (__builtin_popcount(A & TP[s]) != __builtin_popcount(A & TM[s])) { ok = 0; break; }
          if (ok) pat |= 64; }
        loc[pat][n]++;
        if (dump && (pat & 64)) {
            #pragma omp critical
            fprintf(dump, "%u %d\n", A, pat);
        }
      }
      #pragma omp critical
      for (int p = 0; p < 128; p++) for (int n = 0; n < 31; n++) cnt[p][n] += loc[p][n];
    }
    for (int p = 0; p < 128; p++) for (int n = 0; n < 31; n++) if (cnt[p][n]) printf("%d %d %llu\n", p, n, (unsigned long long)cnt[p][n]);
    if (dump) fclose(dump);
    return 0;
}
