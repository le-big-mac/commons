/* Referee's blind implementation of the braided-river cell model.
   usage: braid A seed nsteps report_every KL power inbed|- outprefix save_at [label_offset]
   power: 2.5 or 1.  inbed: binary file of NY*NX doubles, or "-" to start from slope+noise.
   Measures are taken on the bed after t steps and the water routed over that bed. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>
#define NY 256
#define NX 64
static double h[NY][NX], Q[NY][NX], dh[NY][NX], outs[NY][NX];
static const double S = 0.05, Cs = 0.05;
static uint64_t rs;
static double rnd(void) { /* splitmix64 -> [0,1) */
    uint64_t z = (rs += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    z ^= z >> 31;
    return (z >> 11) * (1.0 / 9007199254740992.0);
}

static void route(double KL, int p25) {
    memset(Q, 0, sizeof Q);
    memset(dh, 0, sizeof dh);
    memset(outs, 0, sizeof outs);
    for (int i = 0; i < NX; i++) Q[0][i] = 1.0;
    for (int j = 0; j < NY - 1; j++) {
        for (int i = 0; i < NX; i++) {
            double q = Q[j][i];
            if (q == 0.0) continue; /* no water: no shares, no sand */
            double s[3], w[3];
            int ex[3], any = 0;
            double hc = h[j][i];
            for (int k = 0; k < 3; k++) {
                int ii = i + k - 1;
                if (ii < 0 || ii >= NX) { ex[k] = 0; s[k] = 0; continue; }
                ex[k] = 1;
                s[k] = hc - h[j + 1][ii];
                if (k != 1) s[k] *= M_SQRT1_2;
                if (s[k] > 0) any = 1;
            }
            double sum = 0, qos;
            for (int k = 0; k < 3; k++) {
                if (!ex[k]) { w[k] = 0; continue; }
                if (any) w[k] = s[k] > 0 ? sqrt(s[k]) : 0.0;
                else w[k] = 1.0 / sqrt(fabs(s[k]) + 1e-12);
                sum += w[k];
            }
            qos = q / sum;
            for (int k = 0; k < 3; k++) {
                if (!ex[k] || w[k] == 0.0) continue;
                int ii = i + k - 1;
                double qk = w[k] * qos;
                Q[j + 1][ii] += qk;
                double g = s[k] + Cs;
                if (g > 0) {
                    double x = qk * g;
                    double qs = p25 ? x * x * sqrt(x) : x;
                    dh[j][i] -= qs;
                    dh[j + 1][ii] += qs;
                    outs[j][i] += qs;
                }
            }
        }
    }
    if (KL != 0.0)
        for (int j = 1; j < NY - 1; j++)
            for (int i = 0; i < NX; i++) {
                double o = outs[j][i];
                if (o == 0.0) continue;
                if (i > 0) {
                    double d = h[j][i - 1] - h[j][i];
                    if (d > 0) { double f = KL * d * o; dh[j][i - 1] -= f; dh[j][i] += f; }
                }
                if (i < NX - 1) {
                    double d = h[j][i + 1] - h[j][i];
                    if (d > 0) { double f = KL * d * o; dh[j][i + 1] -= f; dh[j][i] += f; }
                }
            }
}

static double update(void) {
    double m = 0;
    for (int j = 1; j < NY - 1; j++)
        for (int i = 0; i < NX; i++) { double a = fabs(dh[j][i]); if (a > m) m = a; }
    if (m <= 0) return 0;
    double f = 0.03 * S / m;
    for (int j = 1; j < NY - 1; j++)
        for (int i = 0; i < NX; i++) h[j][i] += f * dh[j][i];
    return f;
}

/* m[0]=threads m[1]=wet m[2]=rough(all cells) m[3]=max share m[4]=rough over wet cells only */
static void measure(double *m) {
    const double thr = 0.0035 * 64;
    double thsum = 0, wet = 0, r2 = 0, ms = 0, r2w = 0;
    for (int j = 64; j <= 191; j++) {
        double mean = 0, tot = 0, mx = 0;
        for (int i = 0; i < NX; i++) { mean += h[j][i]; tot += Q[j][i]; if (Q[j][i] > mx) mx = Q[j][i]; }
        mean /= NX;
        ms += mx / tot;
        int in = 0;
        for (int i = 0; i < NX; i++) {
            double d = h[j][i] - mean;
            r2 += d * d;
            if (Q[j][i] > thr) { wet += 1; r2w += d * d; if (!in) { thsum += 1; in = 1; } }
            else in = 0;
        }
    }
    m[0] = thsum / 128.0;
    m[1] = wet / (128.0 * NX);
    m[2] = sqrt(r2 / (128.0 * NX)) / S;
    m[3] = ms / 128.0;
    m[4] = wet > 0 ? sqrt(r2w / wet) / S : 0;
}

static void savebed(const char *prefix, long t) {
    char name[512];
    snprintf(name, sizeof name, "%s_bed_%ld.bin", prefix, t);
    FILE *f = fopen(name, "wb");
    fwrite(h, sizeof(double), NY * NX, f);
    fclose(f);
}

int main(int argc, char **argv) {
    if (argc < 10) { fprintf(stderr, "args\n"); return 1; }
    double A = atof(argv[1]);
    rs = strtoull(argv[2], 0, 10);
    long nsteps = atol(argv[3]), rep = atol(argv[4]);
    double KL = atof(argv[5]);
    int p25 = atof(argv[6]) > 1.5;
    const char *inbed = argv[7], *prefix = argv[8];
    long save_at = atol(argv[9]);
    long off = argc > 10 ? atol(argv[10]) : 0;
    if (strcmp(inbed, "-")) {
        FILE *f = fopen(inbed, "rb");
        if (!f || fread(h, sizeof(double), NY * NX, f) != NY * NX) { fprintf(stderr, "bad bed\n"); return 1; }
        fclose(f);
    } else {
        for (int j = 0; j < NY; j++)
            for (int i = 0; i < NX; i++) {
                double n = (j >= 1 && j <= NY - 2) ? (rnd() - 0.5) * A * S : 0.0;
                h[j][i] = S * (NY - 1 - j) + n;
            }
    }
    long W = rep < 10000 ? rep : 10000; /* window for the running mean (samples each 100 steps) */
    double acc[5] = {0, 0, 0, 0, 0};
    long nacc = 0;
    double tm = 0; /* model time: the sum of the steps' scale factors (K = 1) */
    printf("# A=%g seed=%s KL=%g power=%s inbed=%s\n", A, argv[2], KL, p25 ? "2.5" : "1", inbed);
    printf("# step threads wet rough maxshare rough_wetcells | means of the last %ld steps (every 100): threads wet rough maxshare\n", W);
    for (long t = 0; t <= nsteps; t++) {
        route(KL, p25);
        long nextrep = ((t + rep - 1) / rep) * rep; /* next report step >= t */
        if (t % 100 == 0 && t > nextrep - W && t > 0) {
            double m[5]; measure(m);
            for (int k = 0; k < 5; k++) acc[k] += m[k];
            nacc++;
        }
        if (t % rep == 0) {
            double m[5]; measure(m);
            printf("%ld %.3f %.4f %.4f %.4f %.4f | %.3f %.4f %.4f %.4f | time %.1f\n", t + off, m[0], m[1], m[2], m[3], m[4],
                   nacc ? acc[0] / nacc : m[0], nacc ? acc[1] / nacc : m[1], nacc ? acc[2] / nacc : m[2], nacc ? acc[3] / nacc : m[3], tm);
            fflush(stdout);
            for (int k = 0; k < 5; k++) acc[k] = 0;
            nacc = 0;
        }
        if (t + off == save_at) savebed(prefix, t + off);
        if (t == nsteps) break;
        tm += update();
    }
    savebed(prefix, nsteps + off);
    return 0;
}
