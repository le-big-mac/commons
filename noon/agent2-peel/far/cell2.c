/* cell2.c: the cell problem far up. Noon (agent2), 24 November 2026.

   Points of unit density above the floor y = 0; a layer is every remaining point that a downward parabola
   y = c - (x - a)^2 / 2 touches with no remaining point below it; lifted by (x, y) -> (x, y + x^2/2) a layer is the
   set of corners of the lower convex hull. (This is cell.c's problem; see that file and the README.)

   What is new here:
   - the window is joined end to end (period W), so there are no side walls and no margin to choose. The hull is taken
     over two copies of the window laid side by side, and a point is in the layer if its copy in the stretch from W/2
     to 3W/2 is a corner: a parabola that touches the front near there is far below the floor long before it reaches
     either end of the two copies;
   - the points of each column (a strip of width w) are made only when the peeling reaches them, lowest first, each
     column from its own random stream, so that the points do not depend on the order in which columns are asked;
   - nothing is kept of a point once it is removed but its part in the sums for its band of height (bands 1 high):
     how many, the sum of depths, the sum of squared depths.

   usage: cell2 C WCOL HM SEED [-profile NAME] [-snap NAME] [-check] [-dump NAME] [-seeding 1] [-floor A L] [-points NAME] [-margin F] [-sheartest S] [-bendtest K]
     C      number of columns; WCOL their width (real units); the period is W = C * WCOL
     HM     the peeling goes on until no point of height HM or less remains
     -snap NAME   write the front as it stands at chosen heights: for slabs 4 units thick whose lower edges are at
                  (HM - 4) / 2^(k/8), k = 0, 1, 2, ... (rounded; down to a height of 8; none overlapping), the mean
                  depth of the points of each column in the slab. The file is raw doubles, slab after slab from the
                  top one down, C numbers each (not-a-number where a column has no point in the slab); the lower edges
                  are listed in the JSON as snap_heights.
     -check       also peel the same points the plain way (all points made beforehand, every layer the hull of all
                  that is left, two copies) and say how many points of height <= HM got a different depth
     -dump NAME   with -check: write "x y depth" (whole-number units; the depth the streaming gave) for every point of
                  height <= HM, and "x y 0" for the points above it that the plain way was given, for an outside check
     -sheartest S no joining: the window with walls, peeled to the end the plain way, twice: as it is, and with every
                  point moved up by S/2048 times its x. Says how many points got a different depth.
     -bendtest K  the same, but every point is moved up by (K/2048) x^2/2 instead: no symmetry, a control. With K =
                  1024 the parabolas that peel are in effect half as curved, and nearly every depth must change.
     -seeding 1   start the columns' random streams as the first fifteen long windows did (see seedcol); without it,
                  the better way
     -floor A L   a rippled floor: only points above y = A (1 + cos(2 pi x / L)) are kept (A and L in real units; L
                  must divide the period). For measuring how fast a ripple of the front dies away with height.
     -points NAME no random points at all: read "x y" (whole numbers, in the units below) from the file, one point to a
                  line, peel them with walls to the end, and print each point's depth in the order given. For cases
                  worked by hand. (C, WCOL, HM and SEED must still be given, and are not used.)
     -margin F    for trying only: add F units of height to the limit below which the points of a column are taken
                  as candidates, in place of the margin that is proved enough. Cut far enough, -check must report
                  differences.
   Whole-number coordinates: x in units of 2^-10, y in units of 2^-21; the lift is then yu + xu^2, exactly.
   One line of JSON. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>
typedef int64_t i64; typedef __int128 wide;

typedef struct { i64 x, y; } pt;
static inline int turn(pt a, pt b, pt c) {                    /* of the lifted points (x, y + x^2) */
    /* The lift may be taken about a's own x instead of 0: (x - xa)^2 differs from x^2 by something straight in x,
       which no turn can feel. Then the numbers are small, and 64 bits hold them unless the points are far apart. */
    i64 d1 = b.x - a.x, d2 = c.x - a.x, e1 = b.y - a.y, e2 = c.y - a.y;
    if (d1 > -1048576 && d1 < 1048576 && d2 > -1048576 && d2 < 1048576 && e1 > -((i64)1 << 40) && e1 < ((i64)1 << 40) && e2 > -((i64)1 << 40) && e2 < ((i64)1 << 40)) {
        i64 v = d1 * (e2 + d2 * d2) - (e1 + d1 * d1) * d2;
        return (v > 0) - (v < 0);
    } else {
        wide v = (wide)d1 * ((wide)e2 + (wide)d2 * d2) - ((wide)e1 + (wide)d1 * d1) * (wide)d2;
        return (v > 0) - (v < 0);
    }
}
static uint64_t splitmix(uint64_t *x) { uint64_t z = (*x += 0x9E3779B97F4A7C15ULL); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }

typedef struct {
    uint64_t s[4];          /* this column's random stream */
    i64 ylast;              /* height of the last point made */
    long made;              /* how many points made so far */
    pt *p; unsigned char *gone; int head, size, cap; long seq0;      /* the points made and not yet dropped; seq0 = number of the one at index 0 */
} col_t;
static int C; static i64 WU, wu; static double wreal; static col_t *col;
static inline uint64_t nextc(col_t *q) { uint64_t *S = q->s, r = rotl(S[1] * 5, 7) * 9, t = S[1] << 17; S[2] ^= S[0]; S[3] ^= S[1]; S[1] ^= S[2]; S[0] ^= S[3]; S[2] ^= t; S[3] = rotl(S[3], 45); return r; }
static int seeding = 2;
/* Seeding 1 is how the first fifteen long windows were seeded: the four starting words of column c are splitmix outputs
   at z0 + (c+1)G ... z0 + (c+4)G, so neighbouring columns share three of their four words, shifted by one. I found no
   sign of it in the streams or the counts (README), but it is not how streams should be started. Seeding 2: each
   column starts its chain at a place hashed from the seed and the column, unrelated to its neighbours'. */
static void seedcol(int c, uint64_t seed) {
    uint64_t z; int i;
    if (seeding == 1) z = seed * 0x100000001B3ULL + (uint64_t)c * 0x9E3779B97F4A7C15ULL + 12345;
    else { uint64_t a = seed, b = (uint64_t)c * 0xD6E8FEB86659FD93ULL + 0x2545F4914F6CDD1DULL; z = splitmix(&a) ^ splitmix(&b); }
    for (i = 0; i < 4; i++) col[c].s[i] = splitmix(&z);
    col[c].ylast = 0; col[c].made = 0;
}
/* the next point of column c: a gap of height drawn from the exponential law of mean 1/w, a place across the column */
static double floorA = 0, floorL = 0;       /* -floor: amplitude and wavelength, real units; none if floorL is 0 */
static pt makept(int c) {
    col_t *q = &col[c]; pt r;
    for (;;) {
        double u = ((double)(nextc(q) >> 11) + 1.0) / 9007199254740992.0;
        q->ylast += (i64)(-log(u) / wreal * 2097152.0);
        r.y = q->ylast; r.x = (i64)c * wu + (i64)(((nextc(q) >> 32) * (uint64_t)wu) >> 32);
        if (floorL == 0 || (double)r.y >= floorA * 2097152.0 * (1.0 + cos(6.283185307179586 * (double)r.x / (floorL * 1024.0)))) break;
    }
    q->made++;
    return r;
}
static void pushpt(int c, pt r) {
    col_t *q = &col[c];
    if (q->head >= 256 && q->head * 2 >= q->size) {           /* drop what is gone from the front */
        memmove(q->p, q->p + q->head, sizeof(pt) * (q->size - q->head)); memmove(q->gone, q->gone + q->head, q->size - q->head);
        q->seq0 += q->head; q->size -= q->head; q->head = 0;
    }
    if (q->size == q->cap) { q->cap = q->cap ? q->cap * 2 : 64; q->p = realloc(q->p, sizeof(pt) * q->cap); q->gone = realloc(q->gone, q->cap); }
    q->p[q->size] = r; q->gone[q->size] = 0; q->size++;
}

/* sums by band of height */
static int NB; static double *bn, *bd, *bdd;
static int *snapOf, nSnap, snapH[1024], *snapCnt; static double *snapSum;     /* -snap: the slab of each band (or -1), the lower edges, and the sums by slab and column */
static int *dlog; static int dlogCap;  /* -check: the depth of point number j of column c, for j < dlogCap */
static void record(int c, long seq, i64 y, int layer) {
    i64 b = y >> 21;
    if (b >= 0 && b < NB) { bn[b] += 1; bd[b] += layer; bdd[b] += (double)layer * layer; }
    if (snapOf && b >= 0 && b < NB && snapOf[b] >= 0) { long idx = (long)snapOf[b] * C + c; snapSum[idx] += layer; snapCnt[idx]++; }
    if (dlog && seq < dlogCap) dlog[(long)c * dlogCap + seq] = layer;
}

/* the lower hull of P[0..m) (in order of x); writes the indices of its corners into h; returns how many */
static int lowerhull(const pt *P, int m, int *h) {
    int i, k = 0;
    for (i = 0; i < m; i++) {
        if (k >= 1 && P[h[k - 1]].x == P[i].x) { if (P[i].y >= P[h[k - 1]].y) continue; k--; }     /* same x: keep the lower */
        while (k >= 2 && turn(P[h[k - 2]], P[h[k - 1]], P[i]) <= 0) k--;
        h[k++] = i;
    }
    return k;
}
static int cmppt(const void *a, const void *b) { const pt *p = a, *q = b; if (p->x != q->x) return p->x < q->x ? -1 : 1; if (p->y != q->y) return p->y < q->y ? -1 : 1; return 0; }

static long long candTotal = 0, madeTotal = 0; static double marginGiven = 0; static int marginSet = 0;
static int stream(i64 HMU) {
    pt *S0 = malloc(sizeof(pt) * 2 * C); int *h = malloc(sizeof(int) * (2 * C + 4)); double *bound2 = malloc(sizeof(double) * 2 * C);
    int capC = 1 << 18; pt *cand = malloc(sizeof(pt) * capC); int *cc = malloc(sizeof(int) * capC), *ci = malloc(sizeof(int) * capC), *hc = malloc(sizeof(int) * (capC + 4));
    int layer = 0, c, i, k;
    double margin = marginSet ? marginGiven * 2097152.0 : (double)wu * (double)wu / 4.0 + 8.0;
    for (;;) {
        i64 lowest = INT64_MAX;
        for (c = 0; c < C; c++) {                              /* the lowest remaining point of each column */
            col_t *q = &col[c];
            while (q->head < q->size && q->gone[q->head]) q->head++;
            if (q->head == q->size) pushpt(c, makept(c));
            S0[c] = q->p[q->head]; S0[c + C] = S0[c]; S0[c + C].x += WU;
            if (S0[c].y < lowest) lowest = S0[c].y;
        }
        if (lowest > HMU) break;
        k = lowerhull(S0, 2 * C, h);
        for (i = 0; i < 2 * C; i++) bound2[i] = -INFINITY;
        for (i = 0; i + 1 < k; i++) {                          /* how high the inner hull reaches over each column */
            pt u = S0[h[i]], v = S0[h[i + 1]]; double m = (double)(v.y - u.y) / (double)(v.x - u.x); int j;
            for (j = h[i]; j <= h[i + 1]; j++) {               /* S0 holds one point for each column of the two copies, in order */
                double a = (double)j * wu, b = a + wu, y;
                if (a < (double)u.x) a = (double)u.x;
                if (b > (double)v.x) b = (double)v.x;
                y = (double)u.y + m * (a - u.x) + (a - u.x) * ((double)v.x - a); if (y > bound2[j]) bound2[j] = y;
                y = (double)u.y + m * (b - u.x) + (b - u.x) * ((double)v.x - b); if (y > bound2[j]) bound2[j] = y;
            }
        }
        int mc = 0;
        for (c = 0; c < C; c++) {                              /* candidates: every remaining point not above that, generously */
            col_t *q = &col[c]; double lim = bound2[c >= C / 2 ? c : c + C] + margin; int from = mc;
            while ((double)q->ylast <= lim) pushpt(c, makept(c));
            q = &col[c];
            for (i = q->head; i < q->size; i++) {
                if ((double)q->p[i].y > lim) break;
                if (!q->gone[i]) {
                    if (mc == capC) { capC *= 2; cand = realloc(cand, sizeof(pt) * capC); cc = realloc(cc, sizeof(int) * capC); ci = realloc(ci, sizeof(int) * capC); hc = realloc(hc, sizeof(int) * (capC + 4)); }
                    cand[mc] = q->p[i]; cc[mc] = c; ci[mc] = i; mc++;
                }
            }
            if (mc - from > 1) {                               /* within a column, into order of x (a few points: insertion) */
                int a, b;
                for (a = from + 1; a < mc; a++) { pt t = cand[a]; int tc = cc[a], ti = ci[a]; for (b = a - 1; b >= from && cmppt(&cand[b], &t) > 0; b--) { cand[b + 1] = cand[b]; cc[b + 1] = cc[b]; ci[b + 1] = ci[b]; } cand[b + 1] = t; cc[b + 1] = tc; ci[b + 1] = ti; }
            }
        }
        if (2 * mc > capC) { capC = 2 * mc + 16; cand = realloc(cand, sizeof(pt) * capC); cc = realloc(cc, sizeof(int) * capC); ci = realloc(ci, sizeof(int) * capC); hc = realloc(hc, sizeof(int) * (capC + 4)); }
        for (i = 0; i < mc; i++) { cand[mc + i] = cand[i]; cand[mc + i].x += WU; }
        k = lowerhull(cand, 2 * mc, hc);
        layer++; int took = 0;
        for (i = 0; i < k; i++) {
            pt v = cand[hc[i]]; int o = hc[i] % mc;
            if (v.x >= WU / 2 && v.x < WU / 2 + WU) {          /* the copy in the middle stretch speaks for the point */
                col_t *q = &col[cc[o]];
                if (!q->gone[ci[o]]) { q->gone[ci[o]] = 1; took++; record(cc[o], q->seq0 + ci[o], q->p[ci[o]].y, layer); }
            }
        }
        candTotal += mc;
        if (!took) { fprintf(stderr, "layer %d took no point: the margin is too small\n", layer); exit(4); }   /* cannot happen with the margin that is proved */
    }
    for (c = 0; c < C; c++) madeTotal += col[c].made;
    free(S0); free(h); free(bound2); free(cand); free(cc); free(ci); free(hc);
    return layer;
}

/* ---- the plain way, for checking: all points beforehand; every layer the hull of all that is left ---- */
typedef struct { pt p; int c; long seq; int depth; } full_t;
static int cmpfull(const void *a, const void *b) { const full_t *p = a, *q = b; int r = cmppt(&p->p, &q->p); if (r) return r; return (p->c > q->c) - (p->c < q->c); }
static full_t *F; static long nF;
static void makeall(uint64_t sd, i64 capU) {
    long cap = 1 << 20; int c; F = malloc(sizeof(full_t) * cap); nF = 0;
    for (c = 0; c < C; c++) { seedcol(c, sd); long j = 0; for (;;) { pt r = makept(c); if (r.y > capU) break; if (nF == cap) { cap *= 2; F = realloc(F, sizeof(full_t) * cap); } F[nF].p = r; F[nF].c = c; F[nF].seq = j++; F[nF].depth = 0; nF++; } }
    qsort(F, nF, sizeof(full_t), cmpfull);
}
/* periodic = 1: two copies, corners in the middle stretch; 0: walls, one copy. until = stop when no point of height <= until remains (or none at all) */
static int plain(int periodic, i64 until) {
    long m = nF, i, j; int layer = 0, k; long *cur = malloc(sizeof(long) * nF); pt *P = malloc(sizeof(pt) * 2 * nF); int *h = malloc(sizeof(int) * (2 * nF + 4));
    for (i = 0; i < nF; i++) cur[i] = i;
    for (;;) {
        int any = 0; for (i = 0; i < m; i++) if (F[cur[i]].p.y <= until) { any = 1; break; }
        if (!any || m == 0) break;
        for (i = 0; i < m; i++) { P[i] = F[cur[i]].p; if (periodic) { P[m + i] = P[i]; P[m + i].x += WU; } }
        k = lowerhull(P, periodic ? 2 * m : m, h);
        layer++;
        for (i = 0; i < k; i++) { pt v = P[h[i]]; long o = h[i] % m; if (!periodic || (v.x >= WU / 2 && v.x < WU / 2 + WU)) F[cur[o]].depth = layer; }
        for (i = 0, j = 0; i < m; i++) if (F[cur[i]].depth == 0) cur[j++] = cur[i];
        m = j;
    }
    free(cur); free(P); free(h); return layer;
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: cell2 C WCOL HM SEED [-profile NAME] [-snap NAME] [-check] [-dump NAME] [-seeding 1] [-floor A L] [-points NAME] [-margin F] [-sheartest S] [-bendtest K]\n"); return 2; }
    C = atoi(argv[1]); wreal = atof(argv[2]); double HM = atof(argv[3]); uint64_t sd = strtoull(argv[4], NULL, 10);
    const char *fprofile = NULL, *fdump = NULL, *fsnap = NULL, *fpoints = NULL; int check = 0, i; long shear = 0; int doShear = 0, doBend = 0;
    for (i = 5; i < argc; i++) {
        if (!strcmp(argv[i], "-profile") && i + 1 < argc) fprofile = argv[++i];
        else if (!strcmp(argv[i], "-snap") && i + 1 < argc) fsnap = argv[++i];
        else if (!strcmp(argv[i], "-check")) check = 1;
        else if (!strcmp(argv[i], "-dump") && i + 1 < argc) fdump = argv[++i];
        else if (!strcmp(argv[i], "-sheartest") && i + 1 < argc) { shear = atol(argv[++i]); doShear = 1; }
        else if (!strcmp(argv[i], "-bendtest") && i + 1 < argc) { shear = atol(argv[++i]); doShear = 1; doBend = 1; }
        else if (!strcmp(argv[i], "-seeding") && i + 1 < argc) { seeding = atoi(argv[++i]); if (seeding != 1 && seeding != 2) { fprintf(stderr, "-seeding 1 or 2\n"); return 2; } }
        else if (!strcmp(argv[i], "-floor") && i + 2 < argc) { floorA = atof(argv[++i]); floorL = atof(argv[++i]); if (!(floorA >= 0) || !(floorL > 0)) { fprintf(stderr, "-floor A L with A >= 0 and L > 0\n"); return 2; } }
        else if (!strcmp(argv[i], "-points") && i + 1 < argc) fpoints = argv[++i];
        else if (!strcmp(argv[i], "-margin") && i + 1 < argc) { marginGiven = atof(argv[++i]); marginSet = 1; }
        else { fprintf(stderr, "unknown option %s\n", argv[i]); return 2; }
    }
    if (fpoints) {                                             /* points given by hand, peeled with walls to the end */
        FILE *f = fopen(fpoints, "r"); long long x, y; long cap = 1024, j; int L, *out;
        if (!f) { fprintf(stderr, "cannot read %s\n", fpoints); return 3; }
        F = malloc(sizeof(full_t) * cap); nF = 0;
        while (fscanf(f, "%lld %lld", &x, &y) == 2) {
            if (x < -((i64)1 << 40) || x > ((i64)1 << 40) || y < -((i64)1 << 60) || y > ((i64)1 << 60)) { fprintf(stderr, "a point is out of range\n"); return 2; }
            if (nF == cap) { cap *= 2; F = realloc(F, sizeof(full_t) * cap); }
            F[nF].p.x = x; F[nF].p.y = y; F[nF].c = 0; F[nF].seq = nF; F[nF].depth = 0; nF++;
        }
        fclose(f); qsort(F, nF, sizeof(full_t), cmpfull); L = plain(0, INT64_MAX);
        out = malloc(sizeof(int) * (nF + 1)); for (j = 0; j < nF; j++) out[F[j].seq] = F[j].depth;
        printf("{\"mode\":\"points\",\"points\":%ld,\"layers\":%d,\"depths\":[", nF, L); for (j = 0; j < nF; j++) printf("%s%d", j ? "," : "", out[j]); printf("]}\n");
        return 0;
    }
    wu = (i64)(wreal * 1024 + 0.5); wreal = (double)wu / 1024.0; WU = (i64)C * wu;
    if (C < 8 || C % 2 || wu < 16 || WU >= ((i64)1 << 26) || HM < 1 || HM > 4000000) { fprintf(stderr, "out of range (C even, at least 8; the period below 65536; HM to 4,000,000)\n"); return 2; }
    if ((double)WU / 1024.0 < 40 * sqrt(2 * 40.0)) { fprintf(stderr, "the period must be at least 360\n"); return 2; }
    if (floorL > 0 && fabs((double)WU / 1024.0 / floorL - floor((double)WU / 1024.0 / floorL + 0.5)) > 1e-9) { fprintf(stderr, "the wavelength of the floor must divide the period\n"); return 2; }
    col = calloc(C, sizeof(col_t)); i64 HMU = (i64)(HM * 2097152.0);
    clock_t t0 = clock();
    if (doShear) {                                             /* the window with walls, as it is and sheared, peeled to the end */
        long differ = 0, moved = 0, j; int L1, L2;
        makeall(sd, HMU); L1 = plain(0, INT64_MAX);
        int *d1 = malloc(sizeof(int) * nF); for (j = 0; j < nF; j++) { i64 y0 = F[j].p.y; d1[j] = F[j].depth; F[j].depth = 0; F[j].p.y += doBend ? (i64)(((wide)shear * F[j].p.x * F[j].p.x) / 2048) : shear * F[j].p.x; if (F[j].p.y != y0) moved++; }
        L2 = plain(0, INT64_MAX);
        for (j = 0; j < nF; j++) if (d1[j] != F[j].depth) differ++;
        printf("{\"mode\":\"%s\",\"W\":%.3f,\"HM\":%.0f,\"seed\":%llu,\"points\":%ld,\"slope\":%.4f,\"layers\":%d,\"layers_sheared\":%d,\"moved\":%ld,\"differ\":%ld}\n", doBend ? "bendtest" : "sheartest", (double)WU / 1024, HM, (unsigned long long)sd, nF, (double)shear / 2048.0, L1, L2, moved, differ);
        return 0;
    }
    NB = (int)HM + 1; bn = calloc(NB, sizeof(double)); bd = calloc(NB, sizeof(double)); bdd = calloc(NB, sizeof(double));
    if (fsnap) {
        int prev = (int)HM + 4, k, b; snapOf = malloc(sizeof(int) * NB); for (b = 0; b < NB; b++) snapOf[b] = -1;
        for (k = 0; nSnap < 1024; k++) {
            int hk = (int)floor((HM - 4) * pow(2.0, -k / 8.0) + 0.5);
            if (hk < 8) break;
            if (hk + 4 > prev) continue;                       /* would overlap the slab above */
            snapH[nSnap] = hk; for (b = hk; b < hk + 4; b++) snapOf[b] = nSnap; prev = hk; nSnap++;
        }
        snapSum = calloc((size_t)nSnap * C, sizeof(double)); snapCnt = calloc((size_t)nSnap * C, sizeof(int));
        if (!snapSum || !snapCnt) { fprintf(stderr, "no memory for the slabs\n"); return 3; }
    }
    if (check) { dlogCap = (int)(HM * wreal * 1.6 + 400); dlog = calloc((long)C * dlogCap, sizeof(int)); if (!dlog) { fprintf(stderr, "no memory for the check\n"); return 3; } }
    for (i = 0; i < C; i++) seedcol(i, sd);
    int layers = stream(HMU);
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC; long differ = -1, compared = 0; int plainLayers = -1;
    if (check) {
        long j; makeall(sd, (i64)((HM * 1.5 + 200) * 2097152.0)); plainLayers = plain(1, HMU); differ = 0;
        for (j = 0; j < nF; j++) if (F[j].p.y <= HMU) { compared++; if (F[j].seq >= dlogCap || dlog[(long)F[j].c * dlogCap + F[j].seq] != F[j].depth) differ++; }
        if (fdump) {
            FILE *f = fopen(fdump, "w"); if (!f) { fprintf(stderr, "cannot write to %s\n", fdump); return 3; }
            fprintf(f, "%lld %lld\n", (long long)WU, (long long)HMU);
            for (j = 0; j < nF; j++) fprintf(f, "%lld %lld %d\n", (long long)F[j].p.x, (long long)F[j].p.y, F[j].p.y <= HMU && F[j].seq < dlogCap ? dlog[(long)F[j].c * dlogCap + F[j].seq] : 0);
            fclose(f);
        }
    }
    double n = 0, sy = 0, sdp = 0, syy = 0, syd = 0; int b;
    for (b = (int)(HM / 2); b < NB - 1; b++) { double y = b + 0.5, w = bn[b]; if (w > 0) { n += w; sy += w * y; sdp += bd[b]; syy += w * y * y; syd += y * bd[b]; } }
    double slope = n > 0 ? (syd - sy * sdp / n) / (syy - sy * sy / n) : 0;
    printf("{\"mode\":\"stream\",\"C\":%d,\"wcol\":%.4f,\"W\":%.3f,\"HM\":%.0f,\"seed\":%llu,\"layers\":%d,\"made\":%lld,\"candidates\":%lld,\"slope_upper_half\":%.6f,\"check_compared\":%ld,\"check_differ\":%ld,\"plain_layers\":%d,\"seconds\":%.1f%s",
           C, wreal, (double)WU / 1024, HM, (unsigned long long)sd, layers, madeTotal, candTotal, slope, compared, differ, plainLayers, secs, seeding == 2 ? ",\"seeding\":2" : "");
    if (fsnap) {
        FILE *f = fopen(fsnap, "wb"); long j, tot = (long)nSnap * C; if (!f) { fprintf(stderr, "cannot write to %s\n", fsnap); return 3; }
        for (j = 0; j < tot; j++) snapSum[j] = snapCnt[j] ? snapSum[j] / snapCnt[j] : NAN;
        if ((long)fwrite(snapSum, sizeof(double), tot, f) != tot) { fprintf(stderr, "cannot write to %s\n", fsnap); return 3; }
        fclose(f);
        printf(",\"snap_heights\":["); for (i = 0; i < nSnap; i++) printf("%s%d", i ? "," : "", snapH[i]); printf("]");
    }
    printf("}\n");
    if (fprofile) {
        FILE *f = fopen(fprofile, "w"); if (!f) { fprintf(stderr, "cannot write to %s\n", fprofile); return 3; }
        for (b = 0; b < NB - 1; b++) if (bn[b] > 1) { double mu = bd[b] / bn[b]; fprintf(f, "%d %.0f %.6f %.6f\n", b, bn[b], mu, bdd[b] / bn[b] - mu * mu); }
        fclose(f);
    }
    return 0;
}
