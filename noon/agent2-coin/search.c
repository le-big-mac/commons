/* search.c: every set of D coins, scored. Noon (agent2), 24 November 2026.

   usage: search MODE D L M [FIRST]
     MODE  plain | greedy | both
     D     number of coins
     L     amounts 0..L-1 are scored
     M     largest coin allowed
     FIRST (optional, for sharing the work) only sets whose second-smallest coin
           (plain, greedy) or smallest coin (both) is FIRST

   plain, greedy: sets contain a coin of 1 (without it 1 cannot be made).
   both: any D distinct coins from 1..M; a set that cannot make every amount is skipped.

   Prints the least total, every set that reaches it, and the least worst case with the
   number of sets that reach it and the first of them. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXD 12
#define MAXL 2048
#define INF 1000000000
#define KEEP 200

static int D, L, M, FIRST = 0;
static int coin[MAXD];
static int tab[MAXD + 1][MAXL];
static long long nsets = 0;
static long long bestTotal = -1;
static int bestSets[KEEP][MAXD], nBest = 0;
static long long nBestAll = 0;
static int bestWorst = -1, worstSet[MAXD];
static long long nWorst = 0;

static void leaf(const int *t) {
    long long s = 0; int w = 0, a;
    for (a = 0; a < L; a++) { if (t[a] >= INF) return; s += t[a]; if (t[a] > w) w = t[a]; }
    nsets++;
    if (bestTotal < 0 || s < bestTotal) { bestTotal = s; nBest = 0; nBestAll = 0; }
    if (s == bestTotal) {
        if (nBest < KEEP) memcpy(bestSets[nBest++], coin, sizeof(int) * D);
        nBestAll++;
    }
    if (bestWorst < 0 || w < bestWorst) { bestWorst = w; nWorst = 0; memcpy(worstSet, coin, sizeof(int) * D); }
    if (w == bestWorst) nWorst++;
}

/* plain: add coins in rising order; the table after adding coin c is
   new[a] = min(old[a], new[a-c] + 1) */
static void recPlain(int d, int from) {
    int c, a; const int *old = tab[d]; int *nw = tab[d + 1];
    if (d == D) { leaf(old); return; }
    for (c = from; c <= M - (D - 1 - d); c++) {
        if (d == 1 && FIRST && c != FIRST) continue;
        coin[d] = c;
        for (a = 0; a < L; a++) {
            int v = old[a];
            if (a >= c && nw[a - c] + 1 < v) v = nw[a - c] + 1;
            nw[a] = v;
        }
        recPlain(d + 1, c + 1);
    }
}

/* greedy: add coins in rising order; with a new largest coin c,
   new[a] = a div c + old[a mod c] */
static void recGreedy(int d, int from) {
    int c, a; const int *old = tab[d]; int *nw = tab[d + 1];
    if (d == D) { leaf(old); return; }
    for (c = from; c <= M - (D - 1 - d); c++) {
        if (d == 1 && FIRST && c != FIRST) continue;
        coin[d] = c;
        for (a = 0; a < L; a++) nw[a] = a / c + old[a % c];
        recGreedy(d + 1, c + 1);
    }
}

/* both: breadth-first search from 0 with steps of plus or minus a coin, inside a
   window of one largest coin on each side of 0..L-1 */
static int dist[MAXL + 2 * 4096], queue[MAXL + 2 * 4096];
static void scoreBoth(void) {
    int cmax = coin[D - 1], lo = -(cmax - 1), size = (L - 1) + (cmax - 1) - lo + 1;
    int head = 0, tail = 0, i, x, y, d, t[MAXL], a;
    for (i = 0; i < size; i++) dist[i] = INF;
    dist[-lo] = 0; queue[tail++] = -lo;
    while (head < tail) {
        x = queue[head++]; d = dist[x] + 1;
        for (i = 0; i < D; i++) {
            y = x + coin[i]; if (y < size && dist[y] == INF) { dist[y] = d; queue[tail++] = y; }
            y = x - coin[i]; if (y >= 0 && dist[y] == INF) { dist[y] = d; queue[tail++] = y; }
        }
    }
    for (a = 0; a < L; a++) t[a] = dist[a - lo];
    leaf(t);
}
static void recBoth(int d, int from) {
    int c;
    if (d == D) { scoreBoth(); return; }
    for (c = from; c <= M - (D - 1 - d); c++) {
        if (d == 0 && FIRST && c != FIRST) continue;
        coin[d] = c;
        recBoth(d + 1, c + 1);
    }
}

int main(int argc, char **argv) {
    int a, i, j;
    if (argc < 5) { fprintf(stderr, "usage: search MODE D L M [FIRST]\n"); return 2; }
    D = atoi(argv[2]); L = atoi(argv[3]); M = atoi(argv[4]);
    if (argc > 5) FIRST = atoi(argv[5]);
    if (D < 1 || D > MAXD || L < 1 || L > MAXL || M < D || M > 4096) { fprintf(stderr, "out of range\n"); return 2; }
    if (!strcmp(argv[1], "plain") || !strcmp(argv[1], "greedy")) {
        coin[0] = 1;
        for (a = 0; a < L; a++) tab[1][a] = a;            /* with the coin of 1 alone */
        if (!strcmp(argv[1], "plain")) recPlain(1, 2); else recGreedy(1, 2);
    } else if (!strcmp(argv[1], "both")) {
        recBoth(0, 1);
    } else { fprintf(stderr, "unknown mode\n"); return 2; }
    printf("mode %s D %d L %d M %d first %d\n", argv[1], D, L, M, FIRST);
    printf("sets scored %lld\n", nsets);
    printf("least total %lld over %d amounts\n", bestTotal, L);
    printf("sets with the least total %lld\n", nBestAll);
    for (i = 0; i < nBest; i++) { printf("  best"); for (j = 0; j < D; j++) printf(" %d", bestSets[i][j]); printf("\n"); }
    printf("least worst case %d\n", bestWorst);
    printf("sets with the least worst case %lld\n", nWorst);
    printf("  first"); for (j = 0; j < D; j++) printf(" %d", worstSet[j]); printf("\n");
    return 0;
}
