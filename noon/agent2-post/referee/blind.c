/* Referee's blind program (written before reading anything of Noon's).
 * Mastermind P pegs, C colours.  Lag 1.
 * mode K: can 4 guesses always determine the code?
 *    g1,g2 blind; g3=g3(a1); g4=g4(a1,a2); need (a1,a2,a3,a4) injective.
 * mode W: can the code always have been sent among the first 6 guesses?
 *    g1,g2 blind; g3(a1); g4(a1,a2); g5(a1,a2,a3); g6(a1..a4).
 *    Reduces to: for each class E=(a1,a2,a3), g4 splits E into parts of
 *    size <=2 with at most one part of size 2 (g5 takes one code of the
 *    doubleton, g6 the code that is left).
 * usage: blind MODE part nparts [nosym]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef P
#define P 4
#endif
#ifndef C
#define C 6
#endif
#define MAXN 1296
#define MAXA 16
static int N, NA;
static unsigned char A[MAXN][MAXN];
static int dig[MAXN][P];
static int relaxed;

static void init(void) {
    int amap[P + 1][P + 1];
    N = 1; for (int p = 0; p < P; p++) N *= C;
    NA = 0;
    for (int b = 0; b <= P; b++) for (int w = 0; w + b <= P; w++) {
        if (b == P - 1 && w == 1) { amap[b][w] = -1; continue; }
        amap[b][w] = NA++;
    }
    for (int i = 0; i < N; i++) { int x = i; for (int p = P - 1; p >= 0; p--) { dig[i][p] = x % C; x /= C; } }
    for (int g = 0; g < N; g++) for (int c = 0; c < N; c++) {
        int b = 0, cg[C], cc[C];
        memset(cg, 0, sizeof cg); memset(cc, 0, sizeof cc);
        for (int p = 0; p < P; p++) { if (dig[g][p] == dig[c][p]) b++; cg[dig[g][p]]++; cc[dig[c][p]]++; }
        int s = 0; for (int q = 0; q < C; q++) s += cg[q] < cc[q] ? cg[q] : cc[q];
        A[g][c] = (unsigned char)amap[b][s - b];
    }
}

/* symmetry group images */
static unsigned short *img; static int NG;
static int next_perm(int *a, int n) {
    int i = n - 2; while (i >= 0 && a[i] > a[i + 1]) i--; if (i < 0) return 0;
    int j = n - 1; while (a[j] < a[i]) j--; int t = a[i]; a[i] = a[j]; a[j] = t;
    for (int l = i + 1, r = n - 1; l < r; l++, r--) { t = a[l]; a[l] = a[r]; a[r] = t; }
    return 1;
}
static void build_group(void) {
    int cf = 1, pf = 1; for (int i = 2; i <= C; i++) cf *= i; for (int i = 2; i <= P; i++) pf *= i;
    NG = cf * pf; img = malloc((size_t)NG * N * sizeof(unsigned short));
    int cp[C], pp[P]; int e = 0;
    for (int i = 0; i < C; i++) cp[i] = i;
    do {
        for (int i = 0; i < P; i++) pp[i] = i;
        do {
            for (int c = 0; c < N; c++) {
                int d[P]; for (int p = 0; p < P; p++) d[pp[p]] = cp[dig[c][p]];
                int x = 0; for (int p = 0; p < P; p++) x = x * C + d[p];
                img[(size_t)e * N + c] = (unsigned short)x;
            }
            e++;
        } while (next_perm(pp, P));
    } while (next_perm(cp, C));
}

static int cnt2[MAXA][MAXA];
static int stamp[MAXA * MAXA], dblst[MAXA], cntk[MAXA * MAXA], dbl[MAXA];
static int stampv = 0;
static long long nodes3 = 0, nodes4 = 0;

/* returns 1 if the opening (g1,g2) wins; else 0 and *fa1 = an a1 with no g3 */
static int try_pair(int g1, int g2, int *fa1) {
    int n1[MAXA]; memset(n1, 0, sizeof n1);
    for (int c = 0; c < N; c++) n1[A[g1][c]]++;
    int order[MAXA];
    for (int i = 0; i < NA; i++) order[i] = i;
    for (int i = 0; i < NA; i++) for (int j = i + 1; j < NA; j++) if (n1[order[j]] > n1[order[i]]) { int t = order[i]; order[i] = order[j]; order[j] = t; }
    static int L[MAXN], a2v[MAXN], a3v[MAXN];
    for (int oi = 0; oi < NA; oi++) {
        int a1 = order[oi]; if (n1[a1] <= 1) continue;
        /* bucket codes of C(a1) by a2 */
        int bs[MAXA + 1], bn[MAXA]; memset(bn, 0, sizeof bn);
        for (int c = 0; c < N; c++) if (A[g1][c] == a1) bn[A[g2][c]]++;
        bs[0] = 0; for (int a = 0; a < NA; a++) bs[a + 1] = bs[a] + bn[a];
        int fill[MAXA]; memcpy(fill, bs, sizeof(int) * NA);
        for (int c = 0; c < N; c++) if (A[g1][c] == a1) { int a = A[g2][c]; L[fill[a]] = c; a2v[fill[a]] = a; fill[a]++; }
        int n = bs[NA];
        int border[MAXA]; for (int i = 0; i < NA; i++) border[i] = i;
        for (int i = 0; i < NA; i++) for (int j = i + 1; j < NA; j++) if (bn[border[j]] > bn[border[i]]) { int t = border[i]; border[i] = border[j]; border[j] = t; }
        int found = 0;
        for (int g3 = 0; g3 < N && !found; g3++) {
            nodes3++;
            memset(cnt2, 0, sizeof cnt2);
            int ok = 1;
            for (int i = 0; i < n; i++) {
                int a3 = A[g3][L[i]]; a3v[i] = a3;
                if (++cnt2[a2v[i]][a3] > NA + relaxed) { ok = 0; break; }
            }
            if (!ok) continue;
            for (int bi = 0; bi < NA && ok; bi++) {
                int a2 = border[bi]; int m = bn[a2]; if (m <= 1) continue;
                int s = bs[a2];
                int exists = 0;
                for (int g4 = 0; g4 < N && !exists; g4++) {
                    nodes4++;
                    stampv++;
                    int good = 1;
                    for (int i = s; i < s + m; i++) {
                        int a3 = a3v[i];
                        int key = a3 * MAXA + A[g4][L[i]];
                        if (stamp[key] != stampv) { stamp[key] = stampv; cntk[key] = 0; }
                        if (dblst[a3] != stampv) { dblst[a3] = stampv; dbl[a3] = 0; }
                        int k = ++cntk[key];
                        if (k == 1) continue;
                        if (!relaxed) { good = 0; break; }
                        if (k >= 3) { good = 0; break; }
                        if (++dbl[a3] > 1) { good = 0; break; }
                    }
                    if (good) exists = 1;
                }
                if (!exists) ok = 0;
            }
            if (ok) found = 1;
        }
        if (!found) { *fa1 = a1; return 0; }
    }
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: blind K|W part nparts [nosym]\n"); return 2; }
    relaxed = (argv[1][0] == 'W');
    int part = atoi(argv[2]), nparts = atoi(argv[3]);
    int nosym = argc > 4;
    init();
    build_group();
    int npairs = 0, nyes = 0, nno = 0, idx = 0;
    int nrep = 0;
    static int stab[40320 * 2];
    for (int g1 = 0; g1 < N; g1++) {
        int ns = 0;
        if (!nosym) {
            int isrep = 1;
            for (int e = 0; e < NG; e++) { int x = img[(size_t)e * N + g1]; if (x < g1) { isrep = 0; break; } }
            if (!isrep) continue;
            for (int e = 0; e < NG; e++) if (img[(size_t)e * N + g1] == g1) stab[ns++] = e;
        }
        nrep++;
        for (int g2 = 0; g2 < N; g2++) {
            if (!nosym) {
                int canon = 1;
                for (int k = 0; k < ns; k++) if (img[(size_t)stab[k] * N + g2] < g2) { canon = 0; break; }
                if (!canon) continue;
            }
            npairs++;
            if ((idx++) % nparts != part) continue;
            int fa1 = -1;
            int r = try_pair(g1, g2, &fa1);
            if (r) { nyes++; printf("YES opening %d %d\n", g1, g2); fflush(stdout); }
            else nno++;
        }
    }
    printf("mode %s P=%d C=%d N=%d NA=%d sym=%d part %d/%d: g1 reps %d, ordered openings (all parts) %d, tried here %d, yes %d, no %d, g3 nodes %lld, g4 nodes %lld\n",
           relaxed ? "W(1)<=6" : "K(1)<=4", P, C, N, NA, !nosym, part, nparts, nrep, npairs, nyes + nno, nyes, nno, nodes3, nodes4);
    return 0;
}
