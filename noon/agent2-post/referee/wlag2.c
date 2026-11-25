/* (wlag2.c, made from wquad.c) lag 2, 7 guesses: g1 g2 g3 blind, g4(a1) answered in time for g7 only; g5(a1,a2), g6(a1..a3), g7(a1..a4) can only name codes.
 * Works iff for every a1 there is a g4 with, for every a2: sum over a3 of max(0, [sum over a4 of max(0,n-1)] - 1) <= 1.
 * The header below is wquad.c's. */
/* Referee's own check of two W "no" rows on the classic board, with a formula worked by hand (not Noon's program).
 * Four blind guesses g1..g4 whose answers a1..a4 are seen one at a time by four later guesses that can only name codes:
 *   lag 3, 8 guesses: g5(a1) g6(a1,a2) g7(a1..a3) g8(a1..a4)                -> every code sent iff U = 0
 *   lag 4, 9 guesses: g5 blind and never answered in time (names one code), g6(a1) .. g9(a1..a4) -> iff U <= 1
 * U = least number of codes left unnamed = sum over a1 of u1, with (n = codes of the class not among g1..g4)
 *   u4 = max(0, n-1) per (a1..a4);  u3 = max(0, sum u4 - 1) per (a1,a2,a3);  u2 = max(0, sum u3 - 1);  u1 = max(0, sum u2 - 1).
 * Every ordered quad up to symmetry: 291 ordered pairs (g1,g2) x all g3 x all g4.  Triples are cut only by a bound that is certain:
 * a class of n3 codes under (a1,a2,a3) gives u3 >= n3 - 15 whatever g4 is.
 * usage: wquad part nparts */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 1296
static unsigned char A[N][N]; static int dig[N][4];
static unsigned short img[17280][N];
int main(int argc, char **argv) {
    int part = atoi(argv[1]), nparts = atoi(argv[2]);
    int amap[5][5], k = 0;
    for (int b = 0; b <= 4; b++) for (int w = 0; w + b <= 4; w++) amap[b][w] = k++;   /* 15 slots, (3,1) unused */
    for (int i = 0; i < N; i++) { int x = i; for (int p = 3; p >= 0; p--) { dig[i][p] = x % 6; x /= 6; } }
    for (int g = 0; g < N; g++) for (int c = 0; c < N; c++) {
        int b = 0, cg[6] = {0}, cc[6] = {0}, s = 0;
        for (int p = 0; p < 4; p++) { if (dig[g][p] == dig[c][p]) b++; cg[dig[g][p]]++; cc[dig[c][p]]++; }
        for (int q = 0; q < 6; q++) s += cg[q] < cc[q] ? cg[q] : cc[q];
        A[g][c] = (unsigned char)amap[b][s - b];
    }
    int ne = 0, cp[6], pp[4];
    for (int a = 0; a < 720; a++) { int used[6] = {0}, x = a, f[6] = {120, 24, 6, 2, 1, 1};
        for (int i = 0; i < 6; i++) { int r = x / f[i]; x %= f[i]; for (int j = 0; j < 6; j++) if (!used[j] && r-- == 0) { cp[i] = j; used[j] = 1; break; } }
        for (int b = 0; b < 24; b++) { int u4[4] = {0}, y = b, f4[4] = {6, 2, 1, 1};
            for (int i = 0; i < 4; i++) { int r = y / f4[i]; y %= f4[i]; for (int j = 0; j < 4; j++) if (!u4[j] && r-- == 0) { pp[i] = j; u4[j] = 1; break; } }
            for (int c = 0; c < N; c++) { int d[4]; for (int p = 0; p < 4; p++) d[pp[p]] = cp[dig[c][p]]; img[ne][c] = (unsigned short)(((d[0] * 6 + d[1]) * 6 + d[2]) * 6 + d[3]); }
            ne++; } }
    static int stab[17280]; static int cnt[3375], start[3376], ord[N], key3[N];
    long ntr = 0, nsurv = 0, nquad = 0, histU[8] = {0}; int minU = 1 << 30, bq[4] = {0}, npairs = 0, idx = 0;
    for (int g1 = 0; g1 < N; g1++) {
        int rep = 1, ns = 0; for (int e = 0; e < ne; e++) if (img[e][g1] < g1) { rep = 0; break; }
        if (!rep) continue;
        for (int e = 0; e < ne; e++) if (img[e][g1] == g1) stab[ns++] = e;
        for (int g2 = 0; g2 < N; g2++) {
            int can = 1; for (int i = 0; i < ns; i++) if (img[stab[i]][g2] < g2) { can = 0; break; }
            if (!can) continue; npairs++;
            if ((idx++) % nparts != part) continue;
            for (int g3 = 0; g3 < N; g3++) {
                ntr++;
                memset(cnt, 0, sizeof cnt);
                for (int c = 0; c < N; c++) { if (c == g1 || c == g2 || c == g3) { key3[c] = -1; continue; } key3[c] = (A[g1][c] * 15 + A[g2][c]) * 15 + A[g3][c]; cnt[key3[c]]++; }
                /* certain bound from the triple alone: g5 names one code per (a1,a2), so sum over a3 of max(0, n3-15) <= 1 */
                int dead = 0;
                for (int q = 0; q < 225 && !dead; q++) { int s3 = 0; const int *row = cnt + q * 15; for (int a3 = 0; a3 < 15; a3++) if (row[a3] > 15) s3 += row[a3] - 15; if (s3 > 1) dead = 1; }
                if (dead) continue;
                nsurv++;
                start[0] = 0; for (int q = 0; q < 3375; q++) start[q + 1] = start[q] + cnt[q];
                { static int fill[3375]; memcpy(fill, start, sizeof fill); for (int c = 0; c < N; c++) if (key3[c] >= 0) ord[fill[key3[c]]++] = c; }
                int allok = 1;
                for (int a1 = 0; a1 < 15 && allok; a1++) {
                    if (start[(a1 + 1) * 225] - start[a1 * 225] < 2) continue;
                    int found = 0;
                    for (int g4 = 0; g4 < N && !found; g4++) {
                        const unsigned char *row = A[g4]; int ok = 1; nquad++;
                        for (int a2 = 0; a2 < 15 && ok; a2++) { int s3 = 0; int base = (a1 * 15 + a2) * 15;
                            for (int a3 = 0; a3 < 15; a3++) { int lo = start[base + a3], hi = start[base + a3 + 1]; if (hi - lo < 2) continue;
                                unsigned mask = 0; int n = 0;
                                for (int i = lo; i < hi; i++) { int c = ord[i]; if (c == g4) continue; n++; mask |= 1u << row[c]; }
                                int s4 = n - __builtin_popcount(mask);
                                if (s4 > 1) { s3 += s4 - 1; if (s3 > 1) { ok = 0; break; } } }
                        }
                        if (ok) found = 1;
                    }
                    if (!found) allok = 0;
                }
                if (allok) { histU[0]++; printf("YES triple %d %d %d\n", g1, g2, g3); fflush(stdout); }
            }
        }
    }
    printf("lag 2, 7 guesses, W. part %d/%d: ordered pairs (all parts) %d; triples here %ld, not cut by the certain bound %ld; (a1, g4) tried %ld; triples that work: %ld\n", part, nparts, npairs, ntr, nsurv, nquad, histU[0]);
    return 0;
}
