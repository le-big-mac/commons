/* peel.c: convex hull peeling of a cloud of points, exactly. Noon (agent2), 24 November 2026.

   usage: peel SHAPE N SEED [options]
     SHAPE   disc | square | triangle   N random points, uniform, independent (see gen())
             grid                       the N x N grid of whole numbers
             file:NAME                  points read from NAME, one "x y" per line (N is ignored)
     options -plain        the plain method: a hull of everything that is left, every layer
             -fast         the sector method (the default for disc, square, triangle)
             -both         run both and say whether every point got the same depth
             -vertices     a layer is the vertices of the hull only (plain method only)
                           default: a layer is every remaining point on the hull's boundary
             -mult F       sectors = F * N^(1/3)   (default 4)
             -sizes NAME   write the size of every layer
             -profile NAME write mean depth in 1000 rings of equal width
             -depths NAME  write "x y depth" for every point      (NAME may be - for the standard output)
             -affine       stretch and shear the cloud first: (x, y) -> (3x + y, y)   (needs -DWIDE)

   Coordinates are whole numbers below 2^29 in size (disc of radius R = 2^29; square and triangle of the
   same area, centred at 0), so that every "which side?" is exact in 64-bit whole numbers. Compile with
   -DWIDE for 128-bit products where coordinates are larger (the -affine option).

   One line of output, in JSON. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>

typedef int64_t i64;
#ifdef WIDE
typedef __int128 wide;
typedef int64_t coord;
#else
typedef int64_t wide;
typedef int32_t coord;
#endif

#define RAD ((i64)1 << 29)

static coord *X, *Y;
static int n;
static int *depth;                 /* 0 = not yet removed */

static inline int turn(int a, int b, int c) {      /* +1 if a,b,c turn left, -1 right, 0 in line */
    wide v = (wide)((i64)X[b] - X[a]) * ((i64)Y[c] - Y[a]) - (wide)((i64)Y[b] - Y[a]) * ((i64)X[c] - X[a]);
    return (v > 0) - (v < 0);
}

/* ---------- random numbers: xoshiro256** seeded by splitmix64 ---------- */
static uint64_t S[4];
static uint64_t splitmix(uint64_t *x) { uint64_t z = (*x += 0x9E3779B97F4A7C15ULL); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t next(void) {
    uint64_t r = rotl(S[1] * 5, 7) * 9, t = S[1] << 17;
    S[2] ^= S[0]; S[3] ^= S[1]; S[1] ^= S[2]; S[0] ^= S[3]; S[2] ^= t; S[3] = rotl(S[3], 45);
    return r;
}
static void seed(uint64_t s) { int i; for (i = 0; i < 4; i++) S[i] = splitmix(&s); }

/* the three shapes, all of area pi R^2, centred at 0 */
#define SQ_HALF 475789457LL          /* floor(R * sqrt(pi) / 2): half the side of the square */
#define TRI_HALFBASE 723043617LL     /* floor(R * sqrt(pi / sqrt(3))): half the side of the triangle */
#define TRI_TOP 834898854LL          /* two thirds of its height, 1252348281 */
#define TRI_BOT (-417449427LL)       /* minus a third of its height */
static void gen(const char *shape) {
    int i = 0; i64 x, y;
    if (!strcmp(shape, "disc")) {
        while (i < n) { x = (i64)(next() >> 34) - RAD; y = (i64)(next() >> 34) - RAD; if (x * x + y * y <= RAD * RAD) { X[i] = (coord)x; Y[i] = (coord)y; i++; } }
    } else if (!strcmp(shape, "square")) {
        while (i < n) { x = (i64)(next() >> 34) - RAD; y = (i64)(next() >> 34) - RAD; if (x >= -SQ_HALF && x <= SQ_HALF && y >= -SQ_HALF && y <= SQ_HALF) { X[i] = (coord)x; Y[i] = (coord)y; i++; } }
    } else if (!strcmp(shape, "triangle")) {
        /* corners (0, TOP), (-HB, BOT), (HB, BOT); inside if y >= BOT and on the inner side of both slanted edges */
        while (i < n) {
            x = (i64)(next() >> 33) - ((i64)1 << 30); y = (i64)(next() >> 33) - ((i64)1 << 30);
            if (y < TRI_BOT || y > TRI_TOP) continue;
            /* left edge from (-HB, BOT) to (0, TOP): inside if cross >= 0 with the point on its right ... use 128-bit */
            __int128 l = (__int128)(TRI_HALFBASE) * (y - TRI_BOT) - (__int128)(TRI_TOP - TRI_BOT) * (x + TRI_HALFBASE);     /* <= 0 inside */
            __int128 r = (__int128)(-TRI_HALFBASE) * (y - TRI_BOT) - (__int128)(TRI_TOP - TRI_BOT) * (x - TRI_HALFBASE);    /* >= 0 inside */
            if (l <= 0 && r >= 0) { X[i] = (coord)x; Y[i] = (coord)y; i++; }
        }
    } else { fprintf(stderr, "unknown shape %s\n", shape); exit(2); }
}

/* ---------- the plain method ---------- */
static int cmpxy(const void *a, const void *b) {
    int i = *(const int *)a, j = *(const int *)b;
    if (X[i] != X[j]) return X[i] < X[j] ? -1 : 1;
    if (Y[i] != Y[j]) return Y[i] < Y[j] ? -1 : 1;
    return (i > j) - (i < j);
}
/* One layer of the points cur[0..m), which are sorted by (x, y). Marks depth[] = layer for the points removed and
   returns how many. hull[] is scratch of size m + 1. */
static int oneLayer(int *cur, int m, int *hull, int layer, int verticesOnly) {
    int i, k = 0, t, removed = 0;
    if (m == 0) return 0;
    if (m == 1) { depth[cur[0]] = layer; return 1; }
    for (i = 0; i < m; i++) { while (k >= 2 && turn(hull[k - 2], hull[k - 1], cur[i]) <= 0) k--; hull[k++] = cur[i]; }
    for (i = m - 2, t = k + 1; i >= 0; i--) { while (k >= t && turn(hull[k - 2], hull[k - 1], cur[i]) <= 0) k--; hull[k++] = cur[i]; }
    k--;                                                    /* the last is the first again */
    if (k < 1) k = 1;
    if (verticesOnly) {
        for (i = 0; i < k; i++) if (depth[hull[i]] == 0) { depth[hull[i]] = layer; removed++; }
        return removed;
    }
    if (k <= 2) {                                           /* everything left is in one line (or one place) */
        for (i = 0; i < m; i++) { depth[cur[i]] = layer; }
        return m;
    }
    /* every point on the boundary. hull[] runs counter-clockwise from the leftmost-lowest point: the lower chain
       first (x rising), then the upper chain (x falling). */
    {
        int top = 0, lo, up;                                /* top: index in hull[] of the rightmost-highest vertex */
        for (i = 1; i < k; i++) if (cmpxy(&hull[i], &hull[top]) > 0) top = i;
        coord xmin = X[hull[0]], xmax = X[hull[top]];
        lo = 0; up = k;                                     /* lower edge hull[lo]..hull[lo+1]; upper edge hull[up-1]..hull[up % k], read leftwards */
        for (i = 0; i < m; i++) {
            int p = cur[i], on = 0;
            if (X[p] == xmin || X[p] == xmax) on = 1;       /* the two upright ends of the hull */
            else {
                while (lo + 1 < top && X[hull[lo + 1]] <= X[p]) lo++;
                if (turn(hull[lo], hull[lo + 1], p) == 0) on = 1;
                else {
                    while (up - 1 > top && X[hull[up - 1]] <= X[p]) up--;
                    if (turn(hull[up % k], hull[up - 1], p) == 0) on = 1;
                }
            }
            if (on) { depth[p] = layer; removed++; }
        }
    }
    return removed;
}
static int *sizes; static int nLayers;
static void pushSize(int s) { sizes[++nLayers] = s; }

/* peel the points cur[0..m) (sorted by (x, y)) to the end, starting at layer number `layer` + 1 */
static void plainFrom(int *cur, int m, int layer, int verticesOnly) {
    int *hull = malloc(sizeof(int) * (m + 2)), i, j, r;
    while (m > 0) {
        layer++;
        r = oneLayer(cur, m, hull, layer, verticesOnly);
        pushSize(r);
        for (i = 0, j = 0; i < m; i++) if (depth[cur[i]] == 0) cur[j++] = cur[i];
        m = j;
    }
    free(hull);
}
static void plain(int verticesOnly) {
    int *cur = malloc(sizeof(int) * n), i;
    for (i = 0; i < n; i++) cur[i] = i;
    qsort(cur, n, sizeof(int), cmpxy);
    plainFrom(cur, n, 0, verticesOnly);
    free(cur);
}

/* ---------- the sector method ----------
   The plane round 0 is cut into M sectors by M directions with whole-number components, so that "which sector"
   is exact. In each sector the points are kept in order of distance from 0, farthest first. For a layer:
     1. take the farthest remaining point of every sector; their hull H0 lies inside the hull of everything;
     2. a point strictly inside H0 is not on the hull, and in sector b every point nearer to 0 than the nearest
        line of H0 crossing that sector is strictly inside H0; so only the points at least that far are candidates;
     3. the layer is the boundary of the hull of the candidates, found by the plain method's oneLayer().
   When 0 is no longer strictly inside H0, or few points are left, the plain method finishes. */
typedef struct { i64 r2; int idx; } far_t;
static int cmpfar(const void *a, const void *b) {
    const far_t *p = a, *q = b;
    if (p->r2 != q->r2) return p->r2 > q->r2 ? -1 : 1;
    return (p->idx > q->idx) - (p->idx < q->idx);
}
static long long candTotal = 0; static int fastLayers = 0;
static void fast(double mult) {
    int M = (int)(mult * cbrt((double)n)), b, i, layer = 0, remaining = n;
    if (M < 16) M = 16;
    if (M > 200000) M = 200000;
    i64 *dx = malloc(sizeof(i64) * (M + 1)), *dy = malloc(sizeof(i64) * (M + 1));
    for (b = 0; b <= M; b++) { double th = 2 * M_PI * b / M; dx[b] = (i64)llround(1048576.0 * cos(th)); dy[b] = (i64)llround(1048576.0 * sin(th)); }
    dx[M] = dx[0]; dy[M] = dy[0];
    /* sector of each point: the b with direction b on or clockwise of the point and direction b + 1 strictly counter-clockwise */
    int *sec = malloc(sizeof(int) * n), *start = calloc(M + 1, sizeof(int));
    for (i = 0; i < n; i++) {
        double th = atan2((double)Y[i], (double)X[i]); if (th < 0) th += 2 * M_PI;
        b = (int)(th / (2 * M_PI) * M); if (b >= M) b = M - 1; if (b < 0) b = 0;
        if (X[i] == 0 && Y[i] == 0) b = 0;
        else {
            int guard = 0;
            for (;;) {
                i64 c0 = dx[b] * (i64)Y[i] - dy[b] * (i64)X[i], c1 = dx[b + 1] * (i64)Y[i] - dy[b + 1] * (i64)X[i];
                if (c0 < 0) b = (b + M - 1) % M; else if (c1 >= 0) b = (b + 1) % M; else break;
                if (++guard > 8) { fprintf(stderr, "sector not found\n"); exit(3); }
            }
        }
        sec[i] = b; start[b + 1]++;
    }
    for (b = 0; b < M; b++) start[b + 1] += start[b];
    far_t *list = malloc(sizeof(far_t) * n); int *fill = malloc(sizeof(int) * M);
    for (b = 0; b < M; b++) fill[b] = start[b];
    for (i = 0; i < n; i++) { far_t f; f.r2 = (i64)X[i] * X[i] + (i64)Y[i] * Y[i]; f.idx = i; list[fill[sec[i]]++] = f; }
    for (b = 0; b < M; b++) qsort(list + start[b], start[b + 1] - start[b], sizeof(far_t), cmpfar);
    free(fill); free(sec);
    int *top = malloc(sizeof(int) * M); for (b = 0; b < M; b++) top[b] = start[b];
    int *s0 = malloc(sizeof(int) * (M + 1)), *s0sec = malloc(sizeof(int) * (M + 1)), *h0 = malloc(sizeof(int) * (2 * M + 4)), *h0sec = malloc(sizeof(int) * (2 * M + 4));
    double *rho2 = malloc(sizeof(double) * M);
    int capC = 1 << 16, *cand = malloc(sizeof(int) * capC), *hull = malloc(sizeof(int) * (capC + 2));
    while (remaining > 2000) {
        /* 1. the farthest remaining point of each sector */
        int m0 = 0, k = 0, j, ok = 1, first = 0;
        for (b = 0; b < M; b++) {
            while (top[b] < start[b + 1] && depth[list[top[b]].idx] != 0) top[b]++;
            if (top[b] < start[b + 1]) { s0[m0] = list[top[b]].idx; s0sec[m0] = b; m0++; }
        }
        if (m0 < 3) break;
        /* their hull, by a scan in the order of the sectors, begun at the rightmost-highest of them, which is a vertex */
        for (j = 1; j < m0; j++) if (cmpxy(&s0[j], &s0[first]) > 0) first = j;
        for (j = 0; j <= m0; j++) {
            int q = (first + j) % m0, p = s0[q];
            if (j == m0) {                                   /* back at the start: only clean up, do not push */
                while (k >= 2 && turn(h0[k - 2], h0[k - 1], p) <= 0) k--;
                break;
            }
            while (k >= 2 && turn(h0[k - 2], h0[k - 1], p) <= 0) k--;
            h0[k] = p; h0sec[k] = s0sec[q]; k++;
        }
        if (k < 3) break;
        /* 2. for every sector, the least squared distance from 0 to a line of H0 that crosses it */
        for (b = 0; b < M; b++) rho2[b] = INFINITY;
        for (j = 0; j < k; j++) {
            int u = h0[j], v = h0[(j + 1) % k], bu = h0sec[j], bv = h0sec[(j + 1) % k];
            double cr = (double)X[u] * (double)Y[v] - (double)Y[u] * (double)X[v];
            wide exact = (wide)X[u] * Y[v] - (wide)Y[u] * X[v];
            if (exact <= 0) { ok = 0; break; }               /* 0 is not strictly inside H0 */
            double ex = (double)X[v] - X[u], ey = (double)Y[v] - Y[u], d2 = cr * cr / (ex * ex + ey * ey) * (1 - 1e-9);
            /* Within one sector the line of this edge is nearest to 0 at the foot of the perpendicular if that lies in
               the sector, and otherwise where it meets the nearer of the sector's two bounding rays. Along a straight
               side of a square this is much farther out than the perpendicular distance, and saves most candidates. */
            double t0 = -((double)X[u] * ex + (double)Y[u] * ey) / (ex * ex + ey * ey), fx = X[u] + t0 * ex, fy = Y[u] + t0 * ey, fr = sqrt(fx * fx + fy * fy) * 1048576.0;
            for (b = bu;; b = (b + 1) % M) {
                double lim = d2;
                double c0 = (double)dx[b] * fy - (double)dy[b] * fx, c1 = (double)dx[b + 1] * fy - (double)dy[b + 1] * fx;
                if (c0 < -1e-6 * fr || c1 > 1e-6 * fr) {            /* the foot is clearly outside this sector */
                    double q0 = (double)dx[b] * ey - (double)dy[b] * ex, q1 = (double)dx[b + 1] * ey - (double)dy[b + 1] * ex, s0v, s1v, m;
                    s0v = q0 > 0 ? cr / q0 : INFINITY; s1v = q1 > 0 ? cr / q1 : INFINITY;      /* in units of the direction's length, 2^20 or so */
                    m = s0v < s1v ? s0v : s1v;
                    if (m < INFINITY) {
                        double l0 = (double)dx[b] * dx[b] + (double)dy[b] * dy[b], l1 = (double)dx[b + 1] * dx[b + 1] + (double)dy[b + 1] * dy[b + 1];
                        double r2 = m * m * (s0v < s1v ? l0 : l1) * (1 - 1e-9);
                        if (r2 > lim) lim = r2;
                    }
                }
                if (lim < rho2[b]) rho2[b] = lim;
                if (b == bv) break;
            }
        }
        if (!ok) break;
        /* 3. the candidates, and the boundary of their hull */
        int mc = 0;
        for (b = 0; b < M; b++) {
            double lim = rho2[b];
            for (i = top[b]; i < start[b + 1]; i++) {
                if ((double)list[i].r2 < lim) break;
                if (depth[list[i].idx] == 0) {
                    if (mc == capC) { capC *= 2; cand = realloc(cand, sizeof(int) * capC); hull = realloc(hull, sizeof(int) * (capC + 2)); }
                    cand[mc++] = list[i].idx;
                }
            }
        }
        qsort(cand, mc, sizeof(int), cmpxy);
        layer++;
        int r = oneLayer(cand, mc, hull, layer, 0);
        pushSize(r); remaining -= r; candTotal += mc; fastLayers++;
    }
    /* the plain method for what is left */
    {
        int *cur = malloc(sizeof(int) * (remaining + 1)), m = 0;
        for (i = 0; i < n; i++) if (depth[i] == 0) cur[m++] = i;
        qsort(cur, m, sizeof(int), cmpxy);
        plainFrom(cur, m, layer, 0);
        free(cur);
    }
    free(dx); free(dy); free(start); free(list); free(top); free(s0); free(s0sec); free(h0); free(h0sec); free(rho2); free(cand); free(hull);
}

/* a file to write to; "-" is the standard output. A file that cannot be opened stops the program with a message. */
static FILE *openOut(const char *name) {
    FILE *f;
    if (!strcmp(name, "-")) return stdout;
    f = fopen(name, "w");
    if (!f) { fprintf(stderr, "cannot write to %s\n", name); exit(3); }
    return f;
}
static void closeOut(FILE *f) { if (f != stdout) fclose(f); else fflush(stdout); }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: peel SHAPE N SEED [options]\n"); return 2; }
    const char *shape = argv[1]; long long nn = atoll(argv[2]); uint64_t sd = strtoull(argv[3], NULL, 10);
    int usePlain = 0, useFast = 0, both = 0, verticesOnly = 0, affine = 0, i; double mult = 4;
    const char *fsizes = NULL, *fprofile = NULL, *fdepths = NULL;
    for (i = 4; i < argc; i++) {
        if (!strcmp(argv[i], "-plain")) usePlain = 1; else if (!strcmp(argv[i], "-fast")) useFast = 1; else if (!strcmp(argv[i], "-both")) both = 1;
        else if (!strcmp(argv[i], "-vertices")) verticesOnly = 1; else if (!strcmp(argv[i], "-affine")) affine = 1;
        else if (!strcmp(argv[i], "-mult") && i + 1 < argc) mult = atof(argv[++i]);
        else if (!strcmp(argv[i], "-sizes") && i + 1 < argc) fsizes = argv[++i];
        else if (!strcmp(argv[i], "-profile") && i + 1 < argc) fprofile = argv[++i];
        else if (!strcmp(argv[i], "-depths") && i + 1 < argc) fdepths = argv[++i];
        else { fprintf(stderr, "unknown option %s\n", argv[i]); return 2; }
    }
    int isGrid = !strcmp(shape, "grid"), isFile = !strncmp(shape, "file:", 5);
    if (isGrid) { if (nn < 1 || nn > 20000) { fprintf(stderr, "grid side out of range\n"); return 2; } n = (int)(nn * nn); }
    else if (isFile) {
        FILE *f = fopen(shape + 5, "r"); long long a, b2; if (!f) { fprintf(stderr, "cannot open %s\n", shape + 5); return 2; }
        n = 0; while (fscanf(f, "%lld %lld", &a, &b2) == 2) n++; fclose(f);
    } else { if (nn < 1 || nn > 400000000LL) { fprintf(stderr, "N out of range\n"); return 2; } n = (int)nn; }
    X = malloc(sizeof(coord) * n); Y = malloc(sizeof(coord) * n); depth = calloc(n, sizeof(int)); sizes = malloc(sizeof(int) * (n + 2));
    if (!X || !Y || !depth || !sizes) { fprintf(stderr, "no memory\n"); return 3; }
    if (isGrid) { int a, b2, k = 0; for (a = 0; a < nn; a++) for (b2 = 0; b2 < nn; b2++) { X[k] = a; Y[k] = b2; k++; } }
    else if (isFile) { FILE *f = fopen(shape + 5, "r"); long long a, b2; int k = 0; while (fscanf(f, "%lld %lld", &a, &b2) == 2) { X[k] = (coord)a; Y[k] = (coord)b2; k++; } fclose(f); }
    else { seed(sd); gen(shape); }
    if (affine) {
#ifdef WIDE
        for (i = 0; i < n; i++) X[i] = 3 * X[i] + Y[i];
#else
        fprintf(stderr, "-affine needs the -DWIDE build\n"); return 2;
#endif
    }
    if (!usePlain && !useFast && !both) { if (isGrid || isFile || verticesOnly) usePlain = 1; else useFast = 1; }
    if (verticesOnly && !usePlain) { fprintf(stderr, "-vertices goes with -plain\n"); return 2; }
    clock_t t0 = clock(); int same = -1;
    if (both) {
        int *d1 = malloc(sizeof(int) * n);
        nLayers = 0; plain(0); memcpy(d1, depth, sizeof(int) * n); memset(depth, 0, sizeof(int) * n);
        nLayers = 0; fast(mult);
        same = 1; for (i = 0; i < n; i++) if (d1[i] != depth[i]) { same = 0; break; }
        free(d1);
    } else if (usePlain) { nLayers = 0; plain(verticesOnly); }
    else { nLayers = 0; fast(mult); }
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    /* ---- what is measured ---- */
    int N = nLayers; double K = pow(n / M_PI, 2.0 / 3.0), n13 = cbrt((double)n);
    double su = 0, sd2 = 0, suu = 0, sud = 0; long long cnt = 0;
    static double pc[1000], ps[1000];
    int k1 = (int)floor(0.5 * N + 0.5), k2 = (int)floor(0.9 * N + 0.5); if (k1 < 1) k1 = 1; if (k2 < 1) k2 = 1;
    double mn1 = INFINITY, mx1 = 0, mn2 = INFINITY, mx2 = 0;
    for (i = 0; i < n; i++) {
        double r = sqrt((double)X[i] * X[i] + (double)Y[i] * Y[i]) / (double)RAD, u = 1 - pow(r, 4.0 / 3.0), d = depth[i];
        if (r >= 0.3 && r <= 0.9) { su += u; sd2 += d; suu += u * u; sud += u * d; cnt++; }
        int bin = (int)(r * 1000 / 1.6); if (bin >= 0 && bin < 1000) { pc[bin] += 1; ps[bin] += d; }
        if (depth[i] == k1) { if (r < mn1) mn1 = r; if (r > mx1) mx1 = r; }
        if (depth[i] == k2) { if (r < mn2) mn2 = r; if (r > mx2) mx2 = r; }
    }
    double slope = cnt > 2 ? (sud - su * sd2 / cnt) / (suu - su * su / cnt) : 0;
    double sw = 0, sww = 0; int k; for (k = 1; k <= N; k++) { double f = (double)k / N; if (f >= 0.1 && f <= 0.7) { double w = sqrt(1 - f); sw += sizes[k] * w; sww += w * w; } }
    double cfit = sww > 0 ? sw / sww : 0, mean2040 = 0; int c2040 = 0;
    for (k = 20; k <= 40 && k <= N; k++) { mean2040 += sizes[k]; c2040++; }
    if (c2040) mean2040 /= c2040;
    long long total = 0; for (k = 1; k <= N; k++) total += sizes[k];
    printf("{\"shape\":\"%s\",\"n\":%d,\"seed\":%llu,\"method\":\"%s\",\"layers\":%d,\"removed\":%lld,\"first\":%d,\"mean20to40\":%.4f,"
           "\"a_tot\":%.6f,\"slope\":%.6f,\"a_prof\":%.6f,\"cfit\":%.6f,\"a_size\":%.6f,\"ratio_half\":%.6f,\"ratio_ninetenths\":%.6f,"
           "\"same\":%d,\"fast_layers\":%d,\"candidates\":%lld,\"seconds\":%.2f}\n",
           shape, n, (unsigned long long)sd, both ? "both" : usePlain ? (verticesOnly ? "plain-vertices" : "plain") : "fast", N, total, N >= 1 ? sizes[1] : 0, mean2040,
           (4.0 / 3.0) * N / K, slope, (4.0 / 3.0) * slope / K, cfit, cfit > 0 ? 2 * pow(M_PI, 2.0 / 3.0) * n13 / cfit : 0,
           mn1 > 0 && mx1 > 0 ? mx1 / mn1 : 0, mn2 > 0 && mx2 > 0 ? mx2 / mn2 : 0, same, fastLayers, candTotal, secs);
    if (fsizes) { FILE *f = openOut(fsizes); for (k = 1; k <= N; k++) fprintf(f, "%d\n", sizes[k]); closeOut(f); }
    if (fprofile) { FILE *f = openOut(fprofile); for (k = 0; k < 1000; k++) if (pc[k] > 0) fprintf(f, "%.5f %.0f %.6f\n", (k + 0.5) * 1.6 / 1000, pc[k], ps[k] / pc[k]); closeOut(f); }
    if (fdepths) { FILE *f = openOut(fdepths); for (i = 0; i < n; i++) fprintf(f, "%lld %lld %d\n", (long long)X[i], (long long)Y[i], depth[i]); closeOut(f); }
    return 0;
}
