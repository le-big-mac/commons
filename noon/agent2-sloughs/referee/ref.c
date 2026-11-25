/* ref.c -- referee's own program for the model river (written blind).
   V = kappa - P*I,  I(s) = int_0^inf exp(-xi) kappa(s-xi) dxi, neck cutoff at dc, min loop 3*dc.
   usage: ref P dc T seed [h dt LX ncheck mode a]
     mode = 0 : noise start (sd 0.01 per node);  mode = m>0 : y = a*cos(2 pi m x / LX), no cutoffs (linear test)
   output: lines "t S N ncuts" every 0.1 time (stdout); summary on stderr and last line "#MEAN ..."
*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>

#define NMAX 400000
static double X[NMAX], Y[NMAX], X2[NMAX], Y2[NMAX];
static double AX[NMAX], AY[NMAX], D[NMAX], E[NMAX], K[NMAX], II[NMAX], CUM[NMAX + 1];
static int nxt[NMAX];
static int *head = NULL;
static long headcap = 0;
static int N;
static double LX, P, dc, h, dt;
static long ncuts = 0;
static double cutlen = 0;

static uint64_t rs;
static double urand(void) {
    rs += 0x9E3779B97F4A7C15ULL;
    uint64_t z = rs;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    z = z ^ (z >> 31);
    return ((z >> 11) + 0.5) / 9007199254740992.0;
}
static double grand(void) {
    double u = urand(), v = urand();
    return sqrt(-2 * log(u)) * cos(2 * M_PI * v);
}

/* segment i runs from node i-1 to node i (node -1 = node N-1 shifted by -LX) */
static void segs(double *dmin, double *dmax) {
    double mn = 1e300, mx = 0;
    for (int i = 0; i < N; i++) {
        double ax, ay;
        if (i == 0) { ax = X[0] - (X[N - 1] - LX); ay = Y[0] - Y[N - 1]; }
        else { ax = X[i] - X[i - 1]; ay = Y[i] - Y[i - 1]; }
        double d = sqrt(ax * ax + ay * ay);
        AX[i] = ax; AY[i] = ay; D[i] = d;
        if (d < mn) mn = d;
        if (d > mx) mx = d;
    }
    *dmin = mn; *dmax = mx;
}
static double cum(void) {
    CUM[0] = 0;
    for (int i = 1; i < N; i++) CUM[i] = CUM[i - 1] + D[i];
    CUM[N] = CUM[N - 1] + D[0];
    return CUM[N];
}

static int step(void) {
    double mn, mx;
    segs(&mn, &mx);
    for (int i = 0; i < N; i++) E[i] = exp(-D[i]);
    for (int i = 0; i < N; i++) {
        int ip = (i + 1 == N) ? 0 : i + 1;
        double ax = AX[i], ay = AY[i], bx = AX[ip], by = AY[ip];
        double cr = ax * by - ay * bx;
        double cl = sqrt((ax + bx) * (ax + bx) + (ay + by) * (ay + by));
        K[i] = 2 * cr / (D[i] * D[ip] * cl);
    }
    /* integral, exact for piecewise-linear kappa; warm-up over the last stretch, then once round */
    int i0 = N - 1200; if (i0 < 0) i0 = 0;
    double I = 0;
    for (int pass = 0; pass < 2; pass++) {
        int a = (pass == 0) ? i0 : 0;
        for (int i = a; i < N; i++) {
            int im = (i == 0) ? N - 1 : i - 1;
            if (pass == 0 && i == i0) { I = 0; continue; }
            double e = E[i], d = D[i];
            I = e * I + K[i] * (1 - e) + (K[im] - K[i]) * (1 - e * (1 + d)) / d;
            II[i] = I;
        }
    }
    for (int i = 0; i < N; i++) {
        int ip = (i + 1 == N) ? 0 : i + 1;
        double da = D[i], db = D[ip];
        double tx = AX[i] * db / da + AX[ip] * da / db;
        double ty = AY[i] * db / da + AY[ip] * da / db;
        double tn = sqrt(tx * tx + ty * ty);
        double V = K[i] - P * II[i];
        X2[i] = X[i] + dt * V * (-ty / tn);
        Y2[i] = Y[i] + dt * V * (tx / tn);
    }
    memcpy(X, X2, N * sizeof(double));
    memcpy(Y, Y2, N * sizeof(double));
    return (mn < 0.6 * h || mx > 1.4 * h);
}

static void getnode(int q, double L, double *x, double *y, double *c) {
    if (q < 0) { *x = X[q + N] - LX; *y = Y[q + N]; *c = CUM[q + N] - L; }
    else if (q >= N) { *x = X[q - N] + LX; *y = Y[q - N]; *c = CUM[q - N] + L; }
    else { *x = X[q]; *y = Y[q]; *c = CUM[q]; }
}
/* resample uniformly in chord length with 4-point Lagrange interpolation */
static void regrid(void) {
    double mn, mx;
    segs(&mn, &mx);
    double L = cum();
    int Nn = (int)floor(L / h + 0.5);
    if (Nn >= NMAX) { fprintf(stderr, "too many nodes\n"); exit(1); }
    int j = 0;
    for (int m = 0; m < Nn; m++) {
        double s = m * L / Nn;
        while (j < N - 1 && s >= CUM[j + 1]) j++;
        double x[4], y[4], c[4];
        for (int q = 0; q < 4; q++) getnode(j - 1 + q, L, &x[q], &y[q], &c[q]);
        double xs = 0, ys = 0;
        for (int q = 0; q < 4; q++) {
            double w = 1;
            for (int r = 0; r < 4; r++) if (r != q) w *= (s - c[r]) / (c[q] - c[r]);
            xs += w * x[q]; ys += w * y[q];
        }
        X2[m] = xs; Y2[m] = ys;
    }
    N = Nn;
    memcpy(X, X2, N * sizeof(double));
    memcpy(Y, Y2, N * sizeof(double));
}

/* find the closest qualifying pair; cut; repeat. returns number of cuts made */
static int cutoff(void) {
    int made = 0;
    for (;;) {
        double mn, mx;
        segs(&mn, &mx);
        double L = cum();
        double ymin = 1e300, ymax = -1e300;
        for (int i = 0; i < N; i++) { if (Y[i] < ymin) ymin = Y[i]; if (Y[i] > ymax) ymax = Y[i]; }
        int ncx = (int)floor(LX / dc); double cwx = LX / ncx;
        int ncy = (int)floor((ymax - ymin) / dc) + 1;
        long nc = (long)ncx * ncy;
        if (nc > headcap) { free(head); head = malloc(nc * sizeof(int)); headcap = nc; }
        for (long c = 0; c < nc; c++) head[c] = -1;
        for (int i = 0; i < N; i++) {
            double xr = X[i] - LX * floor(X[i] / LX);
            int cx = (int)(xr / cwx); if (cx >= ncx) cx = ncx - 1; if (cx < 0) cx = 0;
            int cy = (int)((Y[i] - ymin) / dc); if (cy >= ncy) cy = ncy - 1;
            long c = (long)cy * ncx + cx;
            nxt[i] = head[c]; head[c] = i;
        }
        double best = dc * dc; int bi = -1, bj = -1, bk = 0;
        for (int i = 0; i < N; i++) {
            double xr = X[i] - LX * floor(X[i] / LX);
            int cx = (int)(xr / cwx); if (cx >= ncx) cx = ncx - 1; if (cx < 0) cx = 0;
            int cy = (int)((Y[i] - ymin) / dc); if (cy >= ncy) cy = ncy - 1;
            for (int oy = -1; oy <= 1; oy++) {
                int yy = cy + oy; if (yy < 0 || yy >= ncy) continue;
                for (int ox = -1; ox <= 1; ox++) {
                    int xx = cx + ox; if (xx < 0) xx += ncx; if (xx >= ncx) xx -= ncx;
                    for (int j = head[(long)yy * ncx + xx]; j >= 0; j = nxt[j]) {
                        if (j == i) continue;
                        double dx = X[j] - X[i];
                        double kk = -floor(dx / LX + 0.5);
                        dx += kk * LX;
                        double dy = Y[j] - Y[i];
                        double d2 = dx * dx + dy * dy;
                        if (d2 >= best) continue;
                        double arc = CUM[j] - CUM[i] + kk * L;   /* downstream from i to image of j */
                        if (arc > 3 * dc && arc < 0.9 * L) { best = d2; bi = i; bj = j; bk = (int)kk; }
                    }
                }
            }
        }
        if (bi < 0) break;
        /* build new node list */
        int n = 0;
        double arc = CUM[bj] - CUM[bi] + bk * L;
        double px = X[bi], py = Y[bi], qx, qy;
        int seam = (bj < bi);
        if (!seam) {
            for (int i = 0; i <= bi; i++) { X2[n] = X[i]; Y2[n] = Y[i]; n++; }
            qx = X[bj] + bk * LX; qy = Y[bj];
        } else {
            for (int i = bj; i <= bi; i++) { X2[n] = X[i]; Y2[n] = Y[i]; n++; }
            qx = X[bj] + bk * LX; qy = Y[bj];
        }
        double g = sqrt((qx - px) * (qx - px) + (qy - py) * (qy - py));
        int nf = (int)ceil(g / h); if (nf < 1) nf = 1;
        for (int m = 1; m < nf; m++) { X2[n] = px + (qx - px) * m / nf; Y2[n] = py + (qy - py) * m / nf; n++; }
        if (!seam) {
            double sh = bk * LX;   /* should be 0 for a non-seam pair */
            for (int i = bj; i < N; i++) { X2[n] = X[i] + sh; Y2[n] = Y[i]; n++; }
        }
        N = n;
        memcpy(X, X2, N * sizeof(double));
        memcpy(Y, Y2, N * sizeof(double));
        ncuts++; cutlen += arc; made++;
        if (made > 100000) { fprintf(stderr, "runaway cutoffs\n"); exit(1); }
    }
    return made;
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: ref P dc T seed [h dt LX ncheck mode a]\n"); return 1; }
    P = atof(argv[1]); dc = atof(argv[2]);
    double T = atof(argv[3]); long seed = atol(argv[4]);
    h = argc > 5 ? atof(argv[5]) : 0.1;
    dt = argc > 6 ? atof(argv[6]) : 0.1 * h * h;
    LX = argc > 7 ? atof(argv[7]) : 200.0;
    int ncheck = argc > 8 ? atoi(argv[8]) : 5;
    int mode = argc > 9 ? atoi(argv[9]) : 0;
    double a = argc > 10 ? atof(argv[10]) : 1e-4;
    rs = 0x1234567ULL + 7919ULL * (uint64_t)seed;
    N = (int)floor(LX / h + 0.5);
    double k = 2 * M_PI * mode / LX;
    for (int i = 0; i < N; i++) {
        X[i] = i * LX / N;
        Y[i] = mode ? a * cos(k * X[i]) : 0.01 * grand();
    }
    long nsteps = (long)floor(T / dt + 0.5);
    long nout = (long)floor(0.1 / dt + 0.5); if (nout < 1) nout = 1;
    long nsamp = 0;
    double *Ss = malloc(sizeof(double) * (nsteps / nout + 2));
    for (long st = 1; st <= nsteps; st++) {
        int need = step();
        if (!mode && st % ncheck == 0) { if (cutoff()) need = 1; }
        if (need) regrid();
        if (st % nout == 0) {
            double mn, mx; segs(&mn, &mx); double L = cum();
            double t = st * dt;
            if (mode) {
                double cr = 0, ci = 0;
                for (int i = 0; i < N; i++) { cr += Y[i] * cos(k * X[i]); ci -= Y[i] * sin(k * X[i]); }
                cr *= 2.0 / N; ci *= 2.0 / N;
                printf("%.3f %.10g %.10g %.10g\n", t, sqrt(cr * cr + ci * ci), atan2(ci, cr), L / LX);
            } else {
                printf("%.3f %.6f %d %ld %.3f\n", t, L / LX, N, ncuts, cutlen);
            }
            Ss[nsamp++] = L / LX;
        }
    }
    if (!mode) {
        /* second-half mean and sd, and quarter means */
        double q[4] = {0, 0, 0, 0}; long qn[4] = {0, 0, 0, 0};
        double m = 0, v = 0; long nn = 0;
        for (long i = 0; i < nsamp; i++) {
            int qq = (int)(4.0 * i / nsamp); q[qq] += Ss[i]; qn[qq]++;
            if (i >= nsamp / 2) { m += Ss[i]; nn++; }
        }
        m /= nn;
        for (long i = nsamp / 2; i < nsamp; i++) v += (Ss[i] - m) * (Ss[i] - m);
        v = sqrt(v / (nn - 1));
        printf("#MEAN P=%g dc=%g T=%g seed=%ld h=%g dt=%g LX=%g  mean2ndhalf=%.4f sd=%.4f  quarters=%.4f %.4f %.4f %.4f  cuts=%ld cutlen=%.1f\n",
               P, dc, T, seed, h, dt, LX, m, v, q[0] / qn[0], q[1] / qn[1], q[2] / qn[2], q[3] / qn[3], ncuts, cutlen);
    }
    return 0;
}
