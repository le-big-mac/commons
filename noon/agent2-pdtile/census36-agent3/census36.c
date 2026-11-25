/* Census of every subset of Z_36 that contains 0 (agent3 / Yonder): its size and which Phi_d divide its mask polynomial,
   d in {2, 4, 3, 9, 6, 12, 18, 36}, computed from residue-class counts in Z_4 x Z_9 (u = x mod 4, w = x mod 9):
     Phi_{2^i}       : for every class of u mod 2^{i-1}, its two halves mod 2^i have equal counts
     Phi_{3^j}       : for every class of w mod 3^{j-1}, its three thirds mod 3^j have equal counts
     Phi_{2^i 3^j}   : for every class of (u mod 2^{i-1}, w mod 3^{j-1}), the 2 x 3 array of counts of its subclasses is additive
   Output: "pattern size count"; pattern bits: 1 = Phi_2, 2 = Phi_4, 4 = Phi_3, 8 = Phi_9, 16 = Phi_6, 32 = Phi_12, 64 = Phi_18, 128 = Phi_36. */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>
#include <stdlib.h>
#define PC(x) __builtin_popcountll(x)
int main(int argc, char **argv) {
    int nth = argc > 1 ? atoi(argv[1]) : 8;
    uint64_t U2[2] = {0}, U4[4] = {0}, W3[3] = {0}, W9[9] = {0}, C[4][9];
    memset(C, 0, sizeof C);
    for (int x = 0; x < 36; x++) { U2[x % 2] |= 1ull << x; U4[x % 4] |= 1ull << x; W3[x % 3] |= 1ull << x; W9[x % 9] |= 1ull << x; C[x % 4][x % 9] |= 1ull << x; }
    /* masks for the arrays: A6[c][t] (u mod 2 = c, w mod 3 = t); A12[r][c][t] (u = r + 2c mod 4, w mod 3 = t); A18[s][c][t] (u mod 2 = c, w = s + 3t mod 9); A36[r][s][c][t] */
    uint64_t A6[2][3], A12[2][2][3], A18[3][2][3], A36[2][3][2][3];
    memset(A6, 0, sizeof A6); memset(A12, 0, sizeof A12); memset(A18, 0, sizeof A18); memset(A36, 0, sizeof A36);
    for (int u = 0; u < 4; u++) for (int w = 0; w < 9; w++) { uint64_t m = C[u][w];
        A6[u % 2][w % 3] |= m; A12[u % 2][u / 2][w % 3] |= m; A18[w % 3][u % 2][w / 3] |= m; A36[u % 2][w % 3][u / 2][w / 3] |= m; }
    static uint64_t cnt[256][37]; memset(cnt, 0, sizeof cnt);
    #pragma omp parallel num_threads(nth)
    { static __thread uint64_t loc[256][37]; memset(loc, 0, sizeof loc);
      #pragma omp for schedule(dynamic, 1 << 20)
      for (uint64_t m = 0; m < (1ull << 35); m++) {
        uint64_t A = (m << 1) | 1ull; int n = PC(A), pat = 0;
        if (PC(A & U2[0]) == PC(A & U2[1])) pat |= 1;
        if (PC(A & U4[0]) == PC(A & U4[2]) && PC(A & U4[1]) == PC(A & U4[3])) pat |= 2;
        { int a = PC(A & W3[0]); if (a == PC(A & W3[1]) && a == PC(A & W3[2])) pat |= 4; }
        { int ok = 1; for (int s = 0; s < 3 && ok; s++) { int a = PC(A & W9[s]); if (a != PC(A & W9[s + 3]) || a != PC(A & W9[s + 6])) ok = 0; } if (ok) pat |= 8; }
        #define ADD(M) (PC(A & M[0][0]) + PC(A & M[1][1]) == PC(A & M[0][1]) + PC(A & M[1][0]) && PC(A & M[0][0]) + PC(A & M[1][2]) == PC(A & M[0][2]) + PC(A & M[1][0]))
        if (ADD(A6)) pat |= 16;
        if (ADD(A12[0]) && ADD(A12[1])) pat |= 32;
        if (ADD(A18[0]) && ADD(A18[1]) && ADD(A18[2])) pat |= 64;
        { int ok = 1; for (int r = 0; r < 2 && ok; r++) for (int s = 0; s < 3 && ok; s++) if (!ADD(A36[r][s])) ok = 0; if (ok) pat |= 128; }
        loc[pat][n]++;
      }
      #pragma omp critical
      for (int p = 0; p < 256; p++) for (int n = 0; n < 37; n++) cnt[p][n] += loc[p][n];
    }
    for (int p = 0; p < 256; p++) for (int n = 0; n < 37; n++) if (cnt[p][n]) printf("%d %d %llu\n", p, n, (unsigned long long)cnt[p][n]);
    return 0;
}
