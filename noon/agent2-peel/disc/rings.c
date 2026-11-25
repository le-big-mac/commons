/* rings.c: what is kept of one peeled disc, annulus by annulus. Noon (agent2), 24 November 2026.

   usage:  peel disc N SEED -depths - | rings N0 [HALF]
   Reads what peel writes: one line of JSON (its summary), then "x y depth" for every point, x and y in whole
   units of which the disc's radius is 2^29. N0 is the size the cloud is meant to have (for a cloud whose number
   of points is left to chance, the mean of that number): it sets the profile taken off, 0.75 x 1.3259 x
   (N0/pi)^(2/3) x (1 - rho^(4/3)). HALF is the half-width of an annulus (0.008 if not given).
   For each of the 19 annuli centred at rho = 0.05, 0.10, ..., 0.95 it keeps sums over the annulus's points,
   and writes one line of JSON: n0, n, seed and layers (from peel's line), half, and "rings": for each annulus
     [points, sum of (depth - profile), sum of depth, of depth^2, of rho, of rho^2, of rho x depth,
      then for m = 1, 2, 3, 4: sum of cos(m theta), of sin(m theta), of depth cos(m theta), of depth sin(m theta)].
   Nothing else is computed here; disc study scripts turn the sums into means and variances. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define NR 19
#define NS 23
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: peel disc N SEED -depths - | rings N0 [HALF]\n"); return 2; }
    double n0 = atof(argv[1]), half = argc > 2 ? atof(argv[2]) : 0.008, A0, R = 536870912.0;
    if (!(n0 >= 1) || !(half > 0 && half <= 0.025)) { fprintf(stderr, "N0 at least 1; HALF above 0 and at most 0.025\n"); return 2; }
    A0 = 0.75 * 1.3259 * pow(n0 / M_PI, 2.0 / 3.0);
    static double S[NR][NS]; static char line[4096]; long long x, y; int d; long n = 0, seed = -1, layers = -1, nsum = -1; int k, m;
    if (!fgets(line, sizeof line, stdin) || line[0] != '{') { fprintf(stderr, "the first line is not peel's summary\n"); return 3; }
    { char *p = strstr(line, "\"seed\":"); if (p) seed = atol(p + 7); p = strstr(line, "\"layers\":"); if (p) layers = atol(p + 9); p = strstr(line, "\"n\":"); if (p) nsum = atol(p + 4); }
    while (scanf("%lld %lld %d", &x, &y, &d) == 3) {
        double rho = sqrt((double)x * (double)x + (double)y * (double)y) / R, c1, s1, cm, sm, t;
        n++;
        k = (int)floor(rho / 0.05 + 0.5) - 1;                    /* the nearest centre: 0.05 (k = 0) to 0.95 (k = 18) */
        if (k < 0 || k >= NR || fabs(rho - 0.05 * (k + 1)) > half) continue;
        S[k][0] += 1; S[k][1] += d - A0 * (1 - pow(rho, 4.0 / 3.0)); S[k][2] += d; S[k][3] += (double)d * d; S[k][4] += rho; S[k][5] += rho * rho; S[k][6] += rho * d;
        c1 = x / (rho * R); s1 = y / (rho * R); cm = 1; sm = 0;
        for (m = 1; m <= 4; m++) { t = cm * c1 - sm * s1; sm = sm * c1 + cm * s1; cm = t; S[k][3 + 4 * m] += cm; S[k][4 + 4 * m] += sm; S[k][5 + 4 * m] += d * cm; S[k][6 + 4 * m] += d * sm; }
    }
    if (nsum >= 0 && nsum != n) { fprintf(stderr, "peel's summary says %ld points and %ld came\n", nsum, n); return 3; }
    printf("{\"n0\":%.0f,\"n\":%ld,\"seed\":%ld,\"layers\":%ld,\"half\":%g,\"rings\":[", n0, n, seed, layers, half);
    for (k = 0; k < NR; k++) { printf("%s[", k ? "," : ""); for (m = 0; m < NS; m++) printf("%s%.17g", m ? "," : "", S[k][m]); printf("]"); }
    printf("]}\n");
    return 0;
}
