/* open2.c -- second referee's program for the open reach, changed from the first referee's ref.c.
   V = (kappa - p*I)/c,  I(s) = (1/c) int_0^s exp(-xi/c) kappa(s-xi) dxi,
   tau = L/LX, c = tau^(1/3), p = (F/tau + 2 P0 - F)/2.  Neck cutoff at dc, min loop 3*dc.
   Open ends: node 0 never moves; node N-1 is free with kappa = 0.
   rule 0 (quiet): kappa[0] = 0, I[0] = 0.
   rule 1 (fed)  : kappa[0] = kappa[N-2] of the step before, I[0] = kappa[0]/p.
   usage: open2 rule seed [T h dt ncheck P0 F dc LX fixcp]
     fixcp = 1 : keep c = 1 and p = P0 (no tau dependence), for comparison only
   output: lines "t L dist L/dist N ncuts tau" every 0.5 time; last line "#MEAN ..."
*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>

#define NMAX 400000
static double X[NMAX], Y[NMAX], X2[NMAX], Y2[NMAX];
static double AX[NMAX], AY[NMAX], D[NMAX], K[NMAX], II[NMAX], CUM[NMAX + 1];
static int nxt[NMAX];
static int *head = NULL;
static long headcap = 0;
static int N;
static double LX, P0, F, dc, h, dt;
static int rule, fixcp;
static double kfeed = 0;
static double amp = 0;
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

/* segment i runs from node i-1 to node i, i = 1..N-1 */
static void segs(double *dmin, double *dmax) {
    double mn = 1e300, mx = 0;
    for (int i = 1; i < N; i++) {
        double ax = X[i] - X[i - 1], ay = Y[i] - Y[i - 1];
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
    return CUM[N - 1];
}

static int step(void) {
    double mn, mx;
    segs(&mn, &mx);
    double L = cum();
    double tau = L / LX;
    double c = fixcp ? 1.0 : cbrt(tau);
    double p = fixcp ? P0 : (F / tau + 2 * P0 - F) / 2;
    for (int i = 1; i < N - 1; i++) {
        double ax = AX[i], ay = AY[i], bx = AX[i + 1], by = AY[i + 1];
        double cr = ax * by - ay * bx;
        double cl = sqrt((ax + bx) * (ax + bx) + (ay + by) * (ay + by));
        K[i] = 2 * cr / (D[i] * D[i + 1] * cl);
    }
    K[N - 1] = 0;
    K[0] = rule == 1 ? kfeed : rule == 2 ? amp * grand() : 0.0;   /* rule 2 (added after blind.out): white noise of sd amp at the first node */
    double I = rule ? K[0] / p : 0.0;
    II[0] = I;
    for (int i = 1; i < N; i++) {
        double d = D[i] / c, e = exp(-d);
        I = e * I + K[i] * (1 - e) + (K[i - 1] - K[i]) * (1 - e * (1 + d)) / d;
        II[i] = I;
    }
    kfeed = K[N - 2];
    X2[0] = X[0]; Y2[0] = Y[0];
    for (int i = 1; i < N; i++) {
        double tx, ty;
        if (i < N - 1) {
            double da = D[i], db = D[i + 1];
            tx = AX[i] * db / da + AX[i + 1] * da / db;
            ty = AY[i] * db / da + AY[i + 1] * da / db;
        } else { tx = AX[i]; ty = AY[i]; }
        double tn = sqrt(tx * tx + ty * ty);
        double V = (K[i] - p * II[i]) / c;
        X2[i] = X[i] + dt * V * (-ty / tn);
        Y2[i] = Y[i] + dt * V * (tx / tn);
    }
    memcpy(X, X2, N * sizeof(double));
    memcpy(Y, Y2, N * sizeof(double));
    return (mn < 0.6 * h || mx > 1.4 * h);
}

/* resample uniformly in chord length with 4-point Lagrange interpolation; both end nodes kept */
static void regrid(void) {
    double mn, mx;
    segs(&mn, &mx);
    double L = cum();
    int Nn = (int)floor(L / h + 0.5) + 1;
    if (Nn >= NMAX) { fprintf(stderr, "too many nodes\n"); exit(1); }
    int j = 0;
    for (int m = 0; m < Nn; m++) {
        double s = m * L / (Nn - 1);
        while (j < N - 2 && s >= CUM[j + 1]) j++;
        int a = j - 1; if (a < 0) a = 0; if (a > N - 4) a = N - 4;
        double xs = 0, ys = 0;
        for (int q = 0; q < 4; q++) {
            double w = 1;
            for (int r = 0; r < 4; r++) if (r != q) w *= (s - CUM[a + r]) / (CUM[a + q] - CUM[a + r]);
            xs += w * X[a + q]; ys += w * Y[a + q];
        }
        X2[m] = xs; Y2[m] = ys;
    }
    X2[0] = X[0]; Y2[0] = Y[0];
    X2[Nn - 1] = X[N - 1]; Y2[Nn - 1] = Y[N - 1];
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
        cum();
        double ymin = 1e300, ymax = -1e300, xmin = 1e300, xmax = -1e300;
        for (int i = 0; i < N; i++) {
            if (Y[i] < ymin) ymin = Y[i]; if (Y[i] > ymax) ymax = Y[i];
            if (X[i] < xmin) xmin = X[i]; if (X[i] > xmax) xmax = X[i];
        }
        int ncx = (int)floor((xmax - xmin) / dc) + 1;
        int ncy = (int)floor((ymax - ymin) / dc) + 1;
        long nc = (long)ncx * ncy;
        if (nc > headcap) { free(head); head = malloc(nc * sizeof(int)); headcap = nc; }
        for (long c = 0; c < nc; c++) head[c] = -1;
        for (int i = 0; i < N; i++) {
            int cx = (int)((X[i] - xmin) / dc); if (cx >= ncx) cx = ncx - 1;
            int cy = (int)((Y[i] - ymin) / dc); if (cy >= ncy) cy = ncy - 1;
            long c = (long)cy * ncx + cx;
            nxt[i] = head[c]; head[c] = i;
        }
        double best = dc * dc; int bi = -1, bj = -1;
        for (int i = 0; i < N; i++) {
            int cx = (int)((X[i] - xmin) / dc); if (cx >= ncx) cx = ncx - 1;
            int cy = (int)((Y[i] - ymin) / dc); if (cy >= ncy) cy = ncy - 1;
            for (int oy = -1; oy <= 1; oy++) {
                int yy = cy + oy; if (yy < 0 || yy >= ncy) continue;
                for (int ox = -1; ox <= 1; ox++) {
                    int xx = cx + ox; if (xx < 0 || xx >= ncx) continue;
                    for (int j = head[(long)yy * ncx + xx]; j >= 0; j = nxt[j]) {
                        if (j <= i) continue;
                        double dx = X[j] - X[i], dy = Y[j] - Y[i];
                        double d2 = dx * dx + dy * dy;
                        if (d2 >= best) continue;
                        double arc = CUM[j] - CUM[i];
                        if (arc > 3 * dc) { best = d2; bi = i; bj = j; }
                    }
                }
            }
        }
        if (bi < 0) break;
        int n = 0;
        double arc = CUM[bj] - CUM[bi];
        double px = X[bi], py = Y[bi], qx = X[bj], qy = Y[bj];
        for (int i = 0; i <= bi; i++) { X2[n] = X[i]; Y2[n] = Y[i]; n++; }
        double g = sqrt((qx - px) * (qx - px) + (qy - py) * (qy - py));
        int nf = (int)ceil(g / h); if (nf < 1) nf = 1;
        for (int m = 1; m < nf; m++) { X2[n] = px + (qx - px) * m / nf; Y2[n] = py + (qy - py) * m / nf; n++; }
        for (int i = bj; i < N; i++) { X2[n] = X[i]; Y2[n] = Y[i]; n++; }
        N = n;
        memcpy(X, X2, N * sizeof(double));
        memcpy(Y, Y2, N * sizeof(double));
        ncuts++; cutlen += arc; made++;
        if (made > 100000) { fprintf(stderr, "runaway cutoffs\n"); exit(1); }
    }
    return made;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: open2 rule seed [T h dt ncheck P0 F dc LX fixcp dumpfile]\n"); return 1; }
    rule = atoi(argv[1]);
    long seed = atol(argv[2]);
    double T = argc > 3 ? atof(argv[3]) : 125.0;
    h = argc > 4 ? atof(argv[4]) : 0.1;
    dt = argc > 5 ? atof(argv[5]) : 0.1 * h * h;
    int ncheck = argc > 6 ? atoi(argv[6]) : 5;
    P0 = argc > 7 ? atof(argv[7]) : 6.43;
    F = argc > 8 ? atof(argv[8]) : 1.86;
    dc = argc > 9 ? atof(argv[9]) : 0.476;
    LX = argc > 10 ? atof(argv[10]) : 272.0;
    fixcp = argc > 11 ? atoi(argv[11]) : 0;
    const char *dump = argc > 12 ? argv[12] : NULL;
    amp = argc > 13 ? atof(argv[13]) : 0;
    rs = 0x1234567ULL + 7919ULL * (uint64_t)seed;
    N = (int)floor(LX / h + 0.5) + 1;
    for (int i = 0; i < N; i++) {
        X[i] = i * LX / (N - 1);
        Y[i] = 0.01 * grand();
    }
    long nsteps = (long)floor(T / dt + 0.5);
    long nout = (long)floor(0.5 / dt + 0.5); if (nout < 1) nout = 1;
    double sum = 0, sum2 = 0, sumtau = 0; long nsamp = 0;
    double sumA = 0, sumB = 0; long nA = 0, nB = 0;
    double dist = 0, rmax = 0, rmin = 1e300, distmin = 1e300, distmax = 0;
    for (long st = 1; st <= nsteps; st++) {
        int need = step();
        if (st % ncheck == 0) { if (cutoff()) need = 1; }
        if (need) regrid();
        if (st % nout == 0) {
            double mn, mx; segs(&mn, &mx); double L = cum();
            double t = st * dt;
            double dx = X[N - 1] - X[0], dy = Y[N - 1] - Y[0];
            dist = sqrt(dx * dx + dy * dy);
            double r = L / dist;
            printf("%.3f %.4f %.4f %.6f %d %ld %.6f %.3f %.3f\n", t, L, dist, r, N, ncuts, L / LX, X[N - 1], Y[N - 1]);
            if (t > 12.5 - 1e-9) {
                sum += r; sum2 += r * r; sumtau += L / LX; nsamp++;
                if (r > rmax) rmax = r; if (r < rmin) rmin = r;
                if (dist < distmin) distmin = dist; if (dist > distmax) distmax = dist;
                if (t <= 68.75) { sumA += r; nA++; } else { sumB += r; nB++; }
            }
        }
    }
    double m = sum / nsamp, sd = sqrt((sum2 - nsamp * m * m) / (nsamp - 1));
    printf("#MEAN rule=%s seed=%ld T=%g h=%g dt=%g P0=%g F=%g dc=%g LX=%g fixcp=%d  mean(L/dist; t=12.5..%g)=%.4f sd=%.4f min=%.3f max=%.3f n=%ld  halves=%.4f %.4f  mean(L/LX)=%.4f  dist_end=%.3f distmin=%.3f distmax=%.3f  end=(%.2f,%.2f) cuts=%ld cutlen=%.1f\n",
           rule == 1 ? "fed" : rule == 2 ? "noise-fed" : "quiet", seed, T, h, dt, P0, F, dc, LX, fixcp, T, m, sd, rmin, rmax, nsamp,
           sumA / (nA ? nA : 1), sumB / (nB ? nB : 1), sumtau / nsamp, dist, distmin, distmax, X[N - 1], Y[N - 1], ncuts, cutlen);
    if (dump) {
        FILE *f = fopen(dump, "w");
        for (int i = 0; i < N; i++) fprintf(f, "%.4f %.4f\n", X[i], Y[i]);
        fclose(f);
    }
    return 0;
}
