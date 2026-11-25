/* river.c -- the simplest physically based meander model (Ikeda, Parker and Sawai, 1981) with neck cutoffs.
 *
 * The river is its centre line, a chain of nodes on a valley that repeats along x with period LX.
 * Lengths are in units of D = H/(2 Cf) (depth over twice the friction factor) and times in units of
 * D^2/(E b U).  Each node moves along its left normal at the rate
 *
 *        V(s) = kappa(s) - P * I(s),     I(s) = integral_0^inf exp(-xi) kappa(s - xi) d xi,
 *
 * where kappa is the curvature (positive turning left) and s runs downstream.  For a long bend of even
 * curvature V = (1 - P) kappa: the bend moves outward when P > 1.  When two nodes that are not neighbours
 * along the stream come within DC of each other the loop between them is removed (a neck cutoff).
 *
 * With -f F0SQ the reach-wide values follow the river's length as they do for a fixed discharge on a fixed
 * valley slope: with tau = length / LX, the decay length becomes tau^(1/3), the speed tau^(-1/3) and
 * P = (F0SQ / tau + 2 P0 - F0SQ) / 2, where P0 is the P of the straight river.
 *
 * usage: river P DC LX T SEED [-ds DS] [-dt DT] [-out TOUT] [-snap TSNAP FILE] [-ox FILE] [-amin A]
 *              [-every M] [-f F0SQ] [-sine K AMP] [-nocut] [-smooth M] [-oxl FILE] [-start FILE]
 *              [-t0 T0 NCUT CUTLEN]   (with -start: go on from time T0, with the counts of loops as they stood)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define NMAX 400000
static double X[NMAX], Y[NMAX], X2[NMAX], Y2[NMAX];
static double L_[NMAX], K_[NMAX], I_[NMAX], V_[NMAX], S_[NMAX], NX[NMAX], NY[NMAX];
static int N;
static double P = 3, DC = 0.4, LX = 100, DS = 0.1, DT = -1, AMIN = -1;
static int EVERY = 5, NOCUT = 0, FEED = 0, SMOOTH = 0;
static double F0SQ = 0, P0;
static double length;          /* river length over one period */
static long ncut = 0;
static double cutlen = 0;      /* total length removed */
static FILE *oxf = NULL, *oxl = NULL;
static double now = 0;

/* a small generator of our own, so that the same seed gives the same river in every language */
static uint64_t rs;
static double rnd(void) {      /* uniform in [0,1): xorshift64* */
    rs ^= rs >> 12; rs ^= rs << 25; rs ^= rs >> 27;
    return (double)((rs * 2685821657736338717ULL) >> 11) / 9007199254740992.0;
}
static double gauss(void) {    /* Box-Muller */
    double u = rnd(), v = rnd();
    if (u < 1e-300) u = 1e-300;
    return sqrt(-2 * log(u)) * cos(2 * M_PI * v);
}

/* geometry: segment lengths, curvature, arc length, normals */
static void geometry(void) {
    int i;
    length = 0;
    for (i = 0; i < N; i++) {
        int j = i + 1 < N ? i + 1 : 0;
        double dx = X[j] - X[i] + (j == 0 ? LX : 0), dy = Y[j] - Y[i];
        L_[i] = sqrt(dx * dx + dy * dy);
        S_[i] = length; length += L_[i];
    }
    for (i = 0; i < N; i++) {
        int a = i > 0 ? i - 1 : N - 1, b = i + 1 < N ? i + 1 : 0;
        double ax = X[i] - X[a] + (i == 0 ? LX : 0), ay = Y[i] - Y[a];
        double bx = X[b] - X[i] + (b == 0 ? LX : 0), by = Y[b] - Y[i];
        double cx = ax + bx, cy = ay + by, c = sqrt(cx * cx + cy * cy);
        K_[i] = 2 * (ax * by - ay * bx) / (L_[a] * L_[i] * c);   /* the circle through three nodes */
        NX[i] = -cy / c; NY[i] = cx / c;                         /* left normal */
    }
}

/* the upstream integral, twice round the valley so that it has forgotten its start */
static void upstream(double dec) {     /* dec: decay length */
    int lap, i; double I = 0;
    for (lap = 0; lap < 2; lap++)
        for (i = 0; i < N; i++) {
            int a = i > 0 ? i - 1 : N - 1;
            double l = L_[a] / dec, E = exp(-l), c2 = (1 - E * (1 + l)) / l, c1 = 1 - E;
            I = E * I + K_[i] * (c1 - c2) + K_[a] * c2;
            I_[i] = I;
        }
}

static void step(void) {
    int i; double dec = 1, speed = 1, p = P;
    geometry();
    if (FEED) { double tau = length / LX; dec = cbrt(tau); speed = 1 / dec; p = (F0SQ / tau + 2 * P0 - F0SQ) / 2; }
    upstream(dec);
    for (i = 0; i < N; i++) V_[i] = speed * (K_[i] - p * I_[i]);
    for (i = 0; i < N; i++) { X[i] += DT * V_[i] * NX[i]; Y[i] += DT * V_[i] * NY[i]; }
}

/* keep the spacing between DS/2 and 3 DS/2 */
static void respace(void) {
    int i, m = 0, changed = 0;
    double lo = 0.5 * DS, hi = 1.5 * DS;
    for (i = 0; i < N; i++) {
        int j = i + 1 < N ? i + 1 : 0;
        double dx = X[j] - X[i] + (j == 0 ? LX : 0), dy = Y[j] - Y[i];
        if (dx * dx + dy * dy > hi * hi || dx * dx + dy * dy < lo * lo) { changed = 1; break; }
    }
    if (!changed) return;
    for (i = 0; i < N; i++) {
        int a = i > 0 ? i - 1 : N - 1, j = i + 1 < N ? i + 1 : 0, k = j + 1 < N ? j + 1 : 0;
        double xa = X[a] - (i == 0 ? LX : 0), ya = Y[a];
        double xi = X[i], yi = Y[i];
        double xj = X[j] + (j == 0 ? LX : 0), yj = Y[j];
        double xk = X[k] + ((j == 0 || k == 0) ? LX : 0), yk = Y[k];
        double dx = xj - xi, dy = yj - yi, d2 = dx * dx + dy * dy;
        if (m > 0 && i > 0) {       /* drop this node if it sits too close behind the last one kept */
            double ex = xi - X2[m - 1], ey = yi - Y2[m - 1];
            if (ex * ex + ey * ey < lo * lo) continue;
        }
        if (i == N - 1 && m > 1) {  /* and the last node, if it sits too close to the first one, a period on */
            double ex = X2[0] + LX - xi, ey = Y2[0] - yi;
            if (ex * ex + ey * ey < lo * lo) continue;
        }
        X2[m] = xi; Y2[m] = yi; m++;
        if (d2 > hi * hi) {         /* add nodes on a cubic through the four neighbours */
            int parts = (int)ceil(sqrt(d2) / DS), q;
            for (q = 1; q < parts; q++) {
                double t = (double)q / parts, t2 = t * t, t3 = t2 * t;
                double w0 = -0.5 * t3 + t2 - 0.5 * t, w1 = 1.5 * t3 - 2.5 * t2 + 1, w2 = -1.5 * t3 + 2 * t2 + 0.5 * t, w3 = 0.5 * t3 - 0.5 * t2;
                X2[m] = w0 * xa + w1 * xi + w2 * xj + w3 * xk; Y2[m] = w0 * ya + w1 * yi + w2 * yj + w3 * yk; m++;
                if (m >= NMAX - 2) { fprintf(stderr, "too many nodes\n"); exit(2); }
            }
        }
    }
    N = m; memcpy(X, X2, N * sizeof(double)); memcpy(Y, Y2, N * sizeof(double));
}

/* neck cutoffs.  Nodes are sorted into square cells of side DC; a pair in the same or touching cells, nearer
 * than DC and further apart than AMIN along the stream, closes a loop.  Returns 1 if a loop was removed. */
static int *head = NULL, *nxt = NULL, ncell = 0, gx, gy; static double gy0;
static int cutoff(void) {
    int i, c;
    double ymin = 1e300, ymax = -1e300;
    geometry();
    for (i = 0; i < N; i++) { if (Y[i] < ymin) ymin = Y[i]; if (Y[i] > ymax) ymax = Y[i]; }
    gx = (int)floor(LX / DC); if (gx < 3) gx = 3;
    double cw = LX / gx;                       /* cell width along x, a little over DC */
    gy0 = ymin - DC; gy = (int)ceil((ymax - ymin + 2 * DC) / DC) + 1;
    if (gx * gy > ncell) { ncell = gx * gy * 2; head = realloc(head, ncell * sizeof(int)); }
    if (!nxt) nxt = malloc(NMAX * sizeof(int));
    for (c = 0; c < gx * gy; c++) head[c] = -1;
    for (i = N - 1; i >= 0; i--) {             /* so that each cell lists its nodes in rising order */
        double xm = X[i] - LX * floor(X[i] / LX);
        int cx = (int)(xm / cw); if (cx >= gx) cx = gx - 1;
        int cy = (int)((Y[i] - gy0) / DC);
        c = cy * gx + cx; nxt[i] = head[c]; head[c] = i;
    }
    for (i = 0; i < N; i++) {
        double xm = X[i] - LX * floor(X[i] / LX);
        int cx = (int)(xm / cw); if (cx >= gx) cx = gx - 1;
        int cy = (int)((Y[i] - gy0) / DC), ax, ay, best = -1, bestk = 0; double besta = -1;
        for (ay = cy - 1; ay <= cy + 1; ay++) {
            if (ay < 0 || ay >= gy) continue;
            for (ax = cx - 1; ax <= cx + 1; ax++) {
                int bx = (ax + gx) % gx, j;
                for (j = head[ay * gx + bx]; j >= 0; j = nxt[j]) {
                    if (j <= i) continue;
                    double dx = X[j] - X[i], dy = Y[j] - Y[i];
                    double k = floor(dx / LX + 0.5); dx -= k * LX;
                    if (dx * dx + dy * dy >= DC * DC) continue;
                    double a1 = S_[j] - S_[i], arc;
                    if (k == 0) arc = a1; else if (k == 1) arc = length - a1; else { fprintf(stderr, "winding %g at t=%g\n", k, now); exit(3); }
                    if (arc <= AMIN) continue;
                    if (arc > besta) { besta = arc; best = j; bestk = (int)k; }
                }
            }
        }
        if (best >= 0) {
            int j = best, m = 0, q;
#ifdef COUNTSEAM
            if (bestk == 1) fprintf(stderr, "a loop across the seam at t = %.3f\n", now);   /* for seam.sh: how often the tests meet this branch */
#endif
            if (oxl) fprintf(oxl, "%.4f %.4f %d\n", now, besta, bestk == 0 ? j - i : N - (j - i));
            if (oxf) {      /* the loop that is left behind */
                fprintf(oxf, "%.4f %.4f", now, besta);
                if (bestk == 0) for (q = i; q <= j; q++) fprintf(oxf, " %.3f %.3f", X[q], Y[q]);
                else { for (q = j; q < N; q++) fprintf(oxf, " %.3f %.3f", X[q], Y[q]); for (q = 0; q <= i; q++) fprintf(oxf, " %.3f %.3f", X[q] + LX, Y[q]); }
                fprintf(oxf, "\n");
            }
            if (bestk == 0) { for (q = 0; q <= i; q++) { X2[m] = X[q]; Y2[m] = Y[q]; m++; } for (q = j; q < N; q++) { X2[m] = X[q]; Y2[m] = Y[q]; m++; } }
            else { for (q = i; q <= j; q++) { X2[m] = X[q]; Y2[m] = Y[q]; m++; } }
            if (bestk == 1) {   /* the kept arc runs from i to j, and j joins i one period on: shift so that it closes */
                double shift = LX * floor(X2[0] / LX);
                for (q = 0; q < m; q++) X2[q] -= shift;
            }
            N = m; memcpy(X, X2, N * sizeof(double)); memcpy(Y, Y2, N * sizeof(double));
            ncut++; cutlen += besta;
            if (SMOOTH > 0 && N > 4 * SMOOTH + 16) {   /* an option some authors use: drop SMOOTH nodes either side of the join, the two that met included */
                int at = bestk == 0 ? i : N - 1, r; m = 0;
                for (q = 0; q < N; q++) {
                    int drop = 0;
                    for (r = 0; r < SMOOTH; r++) if (q == ((at - r) % N + N) % N || q == (at + 1 + r) % N) drop = 1;
                    if (!drop) { X2[m] = X[q]; Y2[m] = Y[q]; m++; }
                }
                if (bestk == 1 || at - SMOOTH + 1 < 0 || at + SMOOTH >= N) { fprintf(stderr, "smoothing across the seam is not handled; left as it is\n"); }
                else { N = m; memcpy(X, X2, N * sizeof(double)); memcpy(Y, Y2, N * sizeof(double)); }
            }
            return 1;
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: river P DC LX T SEED [options]\n"); return 1; }
    P = atof(argv[1]); DC = atof(argv[2]); LX = atof(argv[3]); double T = atof(argv[4]); long seed = atol(argv[5]);
    double tout = 1, tsnap = -1, sinek = 0, sineamp = 0; const char *snapname = NULL, *startname = NULL; int a; double t0 = 0;
    for (a = 6; a < argc; a++) {
        if (!strcmp(argv[a], "-ds")) DS = atof(argv[++a]);
        else if (!strcmp(argv[a], "-dt")) DT = atof(argv[++a]);
        else if (!strcmp(argv[a], "-out")) tout = atof(argv[++a]);
        else if (!strcmp(argv[a], "-snap")) { tsnap = atof(argv[++a]); snapname = argv[++a]; }
        else if (!strcmp(argv[a], "-ox")) oxf = fopen(argv[++a], "w");
        else if (!strcmp(argv[a], "-oxl")) oxl = fopen(argv[++a], "w");
        else if (!strcmp(argv[a], "-amin")) AMIN = atof(argv[++a]);
        else if (!strcmp(argv[a], "-every")) EVERY = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-f")) { FEED = 1; F0SQ = atof(argv[++a]); }
        else if (!strcmp(argv[a], "-sine")) { sinek = atof(argv[++a]); sineamp = atof(argv[++a]); }
        else if (!strcmp(argv[a], "-nocut")) NOCUT = 1;
        else if (!strcmp(argv[a], "-start")) startname = argv[++a];
        else if (!strcmp(argv[a], "-t0")) { t0 = atof(argv[++a]); ncut = atol(argv[++a]); cutlen = atof(argv[++a]); }
        else if (!strcmp(argv[a], "-smooth")) SMOOTH = atoi(argv[++a]);
        else { fprintf(stderr, "unknown option %s\n", argv[a]); return 1; }
    }
    if (DT < 0) DT = 0.1 * DS * DS;
    if (AMIN < 0) AMIN = 3 * DC;
    P0 = P;
    N = (int)floor(LX / DS + 0.5);
    rs = 88172645463325252ULL ^ ((uint64_t)seed * 2654435761ULL); int i;
    for (i = 0; i < 20; i++) rnd();
    for (i = 0; i < N; i++) {
        X[i] = LX * i / N;
        Y[i] = sinek > 0 ? sineamp * sin(sinek * X[i]) : 0.01 * gauss();
    }
    if (startname) {    /* begin from a line of nodes written by -snap: t N x y x y ... */
        FILE *sf = fopen(startname, "r"); double t0; int n0;
        if (!sf || fscanf(sf, "%lf %d", &t0, &n0) != 2 || n0 >= NMAX) { fprintf(stderr, "cannot read %s\n", startname); return 1; }
        for (i = 0; i < n0; i++) if (fscanf(sf, "%lf %lf", &X[i], &Y[i]) != 2) { fprintf(stderr, "short file %s\n", startname); return 1; }
        N = n0; fclose(sf);
    }
    FILE *snap = snapname ? fopen(snapname, "w") : NULL;
    printf("# river P=%g DC=%g LX=%g T=%g seed=%ld DS=%g DT=%g AMIN=%g EVERY=%d FEED=%d F0SQ=%g SMOOTH=%d\n", P, DC, LX, T, seed, DS, DT, AMIN, EVERY, FEED, F0SQ, SMOOTH);
    printf("# t  nodes  length/LX  cutoffs  length_cut  mean|kappa|  max|kappa|  ymin  ymax  yrms  inflections  sum_of_chords_between_inflections\n");
    long nstep = 0; double nextout = 0, nextsnap = 0;
    if (t0 > 0) { nstep = (long)floor(t0 / DT + 0.5); now = nstep * DT; nextout = now; nextsnap = now + tsnap; }
    for (;;) {
        if (now >= nextout - 1e-9) {
            double mk = 0, xk = 0, ymin = 1e300, ymax = -1e300, ym = 0, y2 = 0;
            geometry();
            for (i = 0; i < N; i++) {
                double w = 0.5 * (L_[i] + L_[i > 0 ? i - 1 : N - 1]);
                mk += fabs(K_[i]) * w; if (fabs(K_[i]) > xk) xk = fabs(K_[i]);
                if (Y[i] < ymin) ymin = Y[i];
                if (Y[i] > ymax) ymax = Y[i];
                ym += Y[i] * w; y2 += Y[i] * Y[i] * w;
            }
            ym /= length; y2 = y2 / length - ym * ym;
            /* inflection points, by the rule of Howard and Hemberger (1991): the sign of K[i-1] + K[i] differs from
               that of K[i+1] + K[i+2]; the point is put midway between nodes i and i+1 */
            int ninf = 0, first = -1, last = -1; double chords = 0, fx = 0, fy = 0, lx = 0, ly = 0;
            for (i = 0; i < N; i++) {
                int a = i > 0 ? i - 1 : N - 1, b = i + 1 < N ? i + 1 : 0, b2 = b + 1 < N ? b + 1 : 0;
                double s1 = K_[a] + K_[i], s2 = K_[b] + K_[b2];
                if ((s1 > 0) != (s2 > 0)) {
                    double px = 0.5 * (X[i] + X[b] + (b == 0 ? LX : 0)), py = 0.5 * (Y[i] + Y[b]);
                    if (last == i - 1) { last = i; continue; }       /* the same crossing seen from the next node */
                    if (first < 0) { first = i; fx = px; fy = py; } else chords += sqrt((px - lx) * (px - lx) + (py - ly) * (py - ly));
                    lx = px; ly = py; last = i; ninf++;
                }
            }
            if (ninf > 1) chords += sqrt((fx + LX - lx) * (fx + LX - lx) + (fy - ly) * (fy - ly));
            printf("%.4f %d %.6f %ld %.4f %.6f %.4f %.4f %.4f %.4f %d %.4f\n", now, N, length / LX, ncut, cutlen, mk / length, xk, ymin, ymax, sqrt(y2 > 0 ? y2 : 0), ninf, chords);
            fflush(stdout);
            nextout += tout;
        }
        if (snap && now >= nextsnap - 1e-9) {
            fprintf(snap, "%.4f %d", now, N);
            for (i = 0; i < N; i++) fprintf(snap, " %.7f %.7f", X[i], Y[i]);
            fprintf(snap, "\n"); fflush(snap);
            nextsnap += tsnap;
        }
        if (now >= T - 1e-9) break;
        step(); nstep++; now = nstep * DT;
        respace();
        if (!NOCUT && nstep % EVERY == 0) { while (cutoff()) respace(); }
    }
    if (snap) fclose(snap);
    if (oxf) fclose(oxf);
    if (oxl) fclose(oxl);
    return 0;
}
