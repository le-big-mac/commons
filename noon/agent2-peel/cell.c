/* cell.c: the cell problem of Calder and Smart, by which their constant is defined. Noon (agent2), 24 November 2026.

   Points of unit density above a flat floor (the half-plane y > 0). A layer is the set of remaining points that a
   parabola y = c - (x - a)^2 / 2, opening downward, can touch from below with no remaining point under it
   ("semiconvex peeling"). Lift each point (x, y) to (x, y + x^2 / 2): the layer is then the lower convex hull of
   the lifted points. The depth of a point at height r grows like alpha * r.

   usage: cell W HD SEED [-plain] [-both] [-profile NAME] [-w WIDTH] [-margin F]
     W      width of the window (real units); HD its height; W * HD points, uniform and independent
     the peeling stops when every point of the middle of the window (a margin of 20 * sqrt(2 * HM) left out at each
     side) with height at most HM = HD / 1.25 has been removed. Only those points are measured.
   Whole-number coordinates: x in units of 2^-10, y in units of 2^-21, so that the lift y + x^2/2 is the whole
   number yu + xu^2 and every "which side?" is exact (128-bit products).

   Output: one line of JSON: the least-squares slope of depth against height over the measured points with
   0.2 HM <= y <= HM (the estimate of alpha), and the same over 0.5 HM <= y <= HM. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>
typedef int64_t i64; typedef __int128 wide;

static int n; static int32_t *XU; static i64 *YU; static int *depth;
static inline int turn(int a, int b, int c) {      /* of the lifted points */
    wide ax = XU[a], ay = (wide)YU[a] + (wide)XU[a] * XU[a], bx = XU[b], by = (wide)YU[b] + (wide)XU[b] * XU[b], cx = XU[c], cy = (wide)YU[c] + (wide)XU[c] * XU[c];
    wide v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax);
    return (v > 0) - (v < 0);
}
static uint64_t S[4];
static uint64_t splitmix(uint64_t *x) { uint64_t z = (*x += 0x9E3779B97F4A7C15ULL); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t next(void) { uint64_t r = rotl(S[1] * 5, 7) * 9, t = S[1] << 17; S[2] ^= S[0]; S[3] ^= S[1]; S[1] ^= S[2]; S[0] ^= S[3]; S[2] ^= t; S[3] = rotl(S[3], 45); return r; }
static void seed(uint64_t s) { int i; for (i = 0; i < 4; i++) S[i] = splitmix(&s); }
static uint64_t below(uint64_t m) { uint64_t lim = UINT64_MAX - UINT64_MAX % m, v; do v = next(); while (v >= lim); return v % m; }   /* uniform in 0..m-1 */

static int cmpx(const void *a, const void *b) {
    int i = *(const int *)a, j = *(const int *)b;
    if (XU[i] != XU[j]) return XU[i] < XU[j] ? -1 : 1;
    if (YU[i] != YU[j]) return YU[i] < YU[j] ? -1 : 1;
    return (i > j) - (i < j);
}
/* the lower hull of cur[0..m), sorted by x: marks its vertices with `layer`; returns how many */
static int lowerLayer(int *cur, int m, int *hull, int layer) {
    int i, k = 0;
    for (i = 0; i < m; i++) {
        if (k >= 1 && XU[hull[k - 1]] == XU[cur[i]]) continue;                 /* same x: the lower one came first */
        while (k >= 2 && turn(hull[k - 2], hull[k - 1], cur[i]) <= 0) k--;
        hull[k++] = cur[i];
    }
    for (i = 0; i < k; i++) depth[hull[i]] = layer;
    return k;
}
static long long left = 0; static i64 xlo, xhi, ymeas;
static inline int measured(int i) { return XU[i] >= xlo && XU[i] < xhi && YU[i] <= ymeas; }

static int plain(void) {
    int *cur = malloc(sizeof(int) * n), *hull = malloc(sizeof(int) * (n + 1)), m = n, i, j, layer = 0;
    for (i = 0; i < n; i++) cur[i] = i;
    qsort(cur, n, sizeof(int), cmpx);
    while (left > 0 && m > 0) {
        layer++;
        lowerLayer(cur, m, hull, layer);
        for (i = 0, j = 0; i < m; i++) { if (depth[cur[i]] == 0) cur[j++] = cur[i]; else if (measured(cur[i])) left--; }
        m = j;
    }
    free(cur); free(hull); return layer;
}
/* the column method: in each column of width w the points in order of height; for a layer, the lowest remaining
   point of each column, their lower hull H0 (which lies on or above the true one), and as candidates every point
   not above H0, generously: in column c, not above the greatest height H0 reaches over that column. */
typedef struct { i64 y; int idx; } low_t;
static int cmplow(const void *a, const void *b) { const low_t *p = a, *q = b; if (p->y != q->y) return p->y < q->y ? -1 : 1; return (p->idx > q->idx) - (p->idx < q->idx); }
static long long candTotal = 0;
static int columns(i64 WU, double wreal) {
    i64 wu = (i64)(wreal * 1024); int C = (int)((WU + wu - 1) / wu), c, i, layer = 0;
    int *start = calloc(C + 1, sizeof(int)); low_t *list = malloc(sizeof(low_t) * n); int *fill = malloc(sizeof(int) * C);
    for (i = 0; i < n; i++) start[XU[i] / wu + 1]++;
    for (c = 0; c < C; c++) start[c + 1] += start[c];
    for (c = 0; c < C; c++) fill[c] = start[c];
    for (i = 0; i < n; i++) { low_t f; f.y = YU[i]; f.idx = i; list[fill[XU[i] / wu]++] = f; }
    for (c = 0; c < C; c++) qsort(list + start[c], start[c + 1] - start[c], sizeof(low_t), cmplow);
    int *top = malloc(sizeof(int) * C), *s0 = malloc(sizeof(int) * C), *h0 = malloc(sizeof(int) * (C + 1));
    double *bound = malloc(sizeof(double) * C);
    int capC = 1 << 16, *cand = malloc(sizeof(int) * capC), *hull = malloc(sizeof(int) * (capC + 1));
    for (c = 0; c < C; c++) top[c] = start[c];
    double margin = (double)wu * (double)wu / 4.0 + 4.0;                       /* a parabola rises at most w^2/8 above its chord */
    while (left > 0) {
        int m0 = 0, k = 0, j, mc = 0;
        for (c = 0; c < C; c++) {
            while (top[c] < start[c + 1] && depth[list[top[c]].idx] != 0) top[c]++;
            if (top[c] < start[c + 1]) s0[m0++] = list[top[c]].idx;
        }
        if (m0 == 0) break;
        for (j = 0; j < m0; j++) {                                              /* s0 is in order of x: one per column */
            while (k >= 2 && turn(h0[k - 2], h0[k - 1], s0[j]) <= 0) k--;
            h0[k++] = s0[j];
        }
        for (c = 0; c < C; c++) bound[c] = -INFINITY;
        bound[XU[h0[0]] / wu] = (double)YU[h0[0]];
        for (j = 0; j + 1 < k; j++) {
            int u = h0[j], v = h0[j + 1]; double xu = XU[u], xv = XU[v], lu = (double)YU[u] + xu * xu, lv = (double)YU[v] + xv * xv;
            int cu = (int)(XU[u] / wu), cv = (int)(XU[v] / wu);
            for (c = cu; c <= cv; c++) {
                double a = (double)c * wu, b = a + wu, t, y; if (a < xu) a = xu; if (b > xv) b = xv;
                t = (a - xu) / (xv - xu); y = lu + (lv - lu) * t - a * a; if (y > bound[c]) bound[c] = y;
                t = (b - xu) / (xv - xu); y = lu + (lv - lu) * t - b * b; if (y > bound[c]) bound[c] = y;
            }
        }
        for (c = 0; c < C; c++) {
            if (bound[c] == -INFINITY) continue;
            double lim = bound[c] * (1 + 1e-9) + margin;
            int from = mc;
            for (i = top[c]; i < start[c + 1]; i++) {
                if ((double)list[i].y > lim) break;
                if (depth[list[i].idx] == 0) {
                    if (mc == capC) { capC *= 2; cand = realloc(cand, sizeof(int) * capC); hull = realloc(hull, sizeof(int) * (capC + 1)); }
                    cand[mc++] = list[i].idx;
                }
            }
            if (mc - from > 1) qsort(cand + from, mc - from, sizeof(int), cmpx);
        }
        layer++;
        lowerLayer(cand, mc, hull, layer);
        for (i = 0; i < mc; i++) if (depth[cand[i]] != 0 && measured(cand[i])) left--;
        candTotal += mc;
    }
    free(start); free(list); free(fill); free(top); free(s0); free(h0); free(bound); free(cand); free(hull);
    return layer;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: cell W HD SEED [-plain] [-both] [-profile NAME] [-w WIDTH] [-margin F]\n"); return 2; }
    double W = atof(argv[1]), HD = atof(argv[2]); uint64_t sd = strtoull(argv[3], NULL, 10);
    int usePlain = 0, both = 0, i; const char *fprofile = NULL; double wcol = 2.0, mfac = 20;
    for (i = 4; i < argc; i++) {
        if (!strcmp(argv[i], "-plain")) usePlain = 1; else if (!strcmp(argv[i], "-both")) both = 1;
        else if (!strcmp(argv[i], "-profile") && i + 1 < argc) fprofile = argv[++i];
        else if (!strcmp(argv[i], "-w") && i + 1 < argc) wcol = atof(argv[++i]);
        else if (!strcmp(argv[i], "-margin") && i + 1 < argc) mfac = atof(argv[++i]);
        else { fprintf(stderr, "unknown option %s\n", argv[i]); return 2; }
    }
    double HM = HD / 1.25, marg = mfac * sqrt(2 * HM);
    if (W <= 2 * marg + 1 || W > 2000000 || HD < 1 || HD > 100000 || W * HD > 4e8) { fprintf(stderr, "window out of range (the margin alone is %.0f a side)\n", marg); return 2; }
    n = (int)(W * HD + 0.5);
    i64 WU = (i64)(W * 1024), HU = (i64)(HD * 2097152.0);
    XU = malloc(sizeof(int32_t) * n); YU = malloc(sizeof(i64) * n); depth = calloc(n, sizeof(int));
    if (!XU || !YU || !depth) { fprintf(stderr, "no memory\n"); return 3; }
    seed(sd);
    for (i = 0; i < n; i++) { XU[i] = (int32_t)below((uint64_t)WU); YU[i] = 1 + (i64)below((uint64_t)HU); }
    xlo = (i64)(marg * 1024); xhi = WU - xlo; ymeas = (i64)(HM * 2097152.0);
    left = 0; for (i = 0; i < n; i++) if (measured(i)) left++;
    long long nMeasured = left; clock_t t0 = clock(); int layers, same = -1;
    if (both) {
        int *d1 = malloc(sizeof(int) * n); long long l0 = left;
        plain(); memcpy(d1, depth, sizeof(int) * n); memset(depth, 0, sizeof(int) * n); left = l0;
        layers = columns(WU, wcol);
        same = 1; for (i = 0; i < n; i++) if (measured(i) && d1[i] != depth[i]) { same = 0; break; }
        free(d1);
    } else if (usePlain) layers = plain(); else layers = columns(WU, wcol);
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    /* slopes of depth against height, and the spread of depth at each height */
    double a[2][5] = {{0}}; int nb = 400; double *bc = calloc(nb, sizeof(double)), *bs = calloc(nb, sizeof(double)), *bq = calloc(nb, sizeof(double)), *by = calloc(nb, sizeof(double));
    for (i = 0; i < n; i++) if (measured(i)) {
        double y = (double)YU[i] / 2097152.0, d = depth[i]; int q;
        for (q = 0; q < 2; q++) if (y >= (q ? 0.5 : 0.2) * HM) { a[q][0] += 1; a[q][1] += y; a[q][2] += d; a[q][3] += y * y; a[q][4] += y * d; }
        int b = (int)(y / HM * nb); if (b >= nb) b = nb - 1;
        bc[b] += 1; bs[b] += d; bq[b] += d * d; by[b] += y;
    }
    double sl[2]; for (i = 0; i < 2; i++) sl[i] = (a[i][4] - a[i][1] * a[i][2] / a[i][0]) / (a[i][3] - a[i][1] * a[i][1] / a[i][0]);
    printf("{\"W\":%.0f,\"HD\":%.0f,\"HM\":%.0f,\"margin\":%.0f,\"seed\":%llu,\"n\":%d,\"measured\":%lld,\"method\":\"%s\",\"layers\":%d,\"alpha_02\":%.6f,\"alpha_05\":%.6f,\"same\":%d,\"candidates\":%lld,\"seconds\":%.2f}\n",
           W, HD, HM, marg, (unsigned long long)sd, n, nMeasured, both ? "both" : usePlain ? "plain" : "columns", layers, sl[0], sl[1], same, candTotal, secs);
    if (fprofile) {       /* per band of height: mean height, points, mean depth, variance of depth within the band */
        FILE *f = fopen(fprofile, "w"); int b;
        for (b = 0; b < nb; b++) if (bc[b] > 1) { double mu = bs[b] / bc[b]; fprintf(f, "%.4f %.0f %.5f %.5f\n", by[b] / bc[b], bc[b], mu, bq[b] / bc[b] - mu * mu); }
        fclose(f);
    }
    return 0;
}
