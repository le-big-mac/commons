/* Referee: every ordered triple of blind guesses up to symmetry (291 ordered pairs x 1296 thirds, a superset of the 151,235 classes):
 * the largest class its three answers leave, counting only codes not among the three guesses.  Used for the W "no" rows:
 * at lag 3 with 8 guesses a class may hold at most 17 such codes (g4, g5, g6, g7 name one each, g8 one per answer to g4 other than all black). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define P 4
#define C 6
#define N 1296
static unsigned char A[N][N]; static int dig[N][P];
int main(void) {
    int amap[5][5], k = 0;
    for (int b = 0; b <= 4; b++) for (int w = 0; w + b <= 4; w++) amap[b][w] = k++;
    for (int i = 0; i < N; i++) { int x = i; for (int p = 3; p >= 0; p--) { dig[i][p] = x % 6; x /= 6; } }
    for (int g = 0; g < N; g++) for (int c = 0; c < N; c++) {
        int b = 0, cg[6] = {0}, cc[6] = {0}, s = 0;
        for (int p = 0; p < 4; p++) { if (dig[g][p] == dig[c][p]) b++; cg[dig[g][p]]++; cc[dig[c][p]]++; }
        for (int q = 0; q < 6; q++) s += cg[q] < cc[q] ? cg[q] : cc[q];
        A[g][c] = (unsigned char)amap[b][s - b];
    }
    /* group */
    static unsigned short img[17280][N]; int ne = 0;
    int cp[6], pp[4];
    for (int a = 0; a < 720; a++) { int used[6] = {0}, x = a, f[6] = {120, 24, 6, 2, 1, 1};
        for (int i = 0; i < 6; i++) { int r = x / f[i]; x %= f[i]; for (int j = 0; j < 6; j++) if (!used[j] && r-- == 0) { cp[i] = j; used[j] = 1; break; } }
        for (int b = 0; b < 24; b++) { int u4[4] = {0}, y = b, f4[4] = {6, 2, 1, 1};
            for (int i = 0; i < 4; i++) { int r = y / f4[i]; y %= f4[i]; for (int j = 0; j < 4; j++) if (!u4[j] && r-- == 0) { pp[i] = j; u4[j] = 1; break; } }
            for (int c = 0; c < N; c++) { int d[4]; for (int p = 0; p < 4; p++) d[pp[p]] = cp[dig[c][p]]; img[ne][c] = (unsigned short)(((d[0] * 6 + d[1]) * 6 + d[2]) * 6 + d[3]); }
            ne++; } }
    static int cnt[15 * 15 * 15]; long hist[1300]; memset(hist, 0, sizeof hist); long ntr = 0; int npairs = 0, best = N, bg[3] = {0, 0, 0};
    static int stab[17280];
    for (int g1 = 0; g1 < N; g1++) {
        int rep = 1, ns = 0; for (int e = 0; e < ne; e++) if (img[e][g1] < g1) { rep = 0; break; }
        if (!rep) continue;
        for (int e = 0; e < ne; e++) if (img[e][g1] == g1) stab[ns++] = e;
        for (int g2 = 0; g2 < N; g2++) {
            int can = 1; for (int i = 0; i < ns; i++) if (img[stab[i]][g2] < g2) { can = 0; break; }
            if (!can) continue; npairs++;
            for (int g3 = 0; g3 < N; g3++) {
                memset(cnt, 0, sizeof cnt); int mx = 0;
                for (int c = 0; c < N; c++) { if (c == g1 || c == g2 || c == g3) continue; int key = (A[g1][c] * 15 + A[g2][c]) * 15 + A[g3][c]; if (++cnt[key] > mx) mx = cnt[key]; }
                hist[mx]++; ntr++; if (mx < best) { best = mx; bg[0] = g1; bg[1] = g2; bg[2] = g3; }
            }
        }
    }
    long le16 = 0, le17 = 0, le18 = 0; for (int i = 0; i <= 18; i++) { if (i <= 16) le16 += hist[i]; if (i <= 17) le17 += hist[i]; le18 += hist[i]; }
    printf("ordered pairs %d, triples %ld; smallest largest-class (codes not among the three guesses) %d, at codes %d %d %d\n", npairs, ntr, best, bg[0], bg[1], bg[2]);
    printf("triples whose largest class is <=16: %ld, <=17: %ld, <=18: %ld\n", le16, le17, le18);
    for (int i = best; i < best + 8; i++) printf("  largest class %d: %ld triples\n", i, hist[i]);
    return 0;
}
