/* erode.c: the affine curve shortening flow of a convex shape, by affine erosion, and how much the time the shape takes to
   vanish answers to a little area taken away at each place. Noon (agent2), 24-25 November 2026.

   The flow: every point of the curve moves inward with the cube root of the curvature there (the limit of convex peeling;
   Calder and Smart 2020). Affine erosion (Moisan 1998, which I have not read; the step below is from a cap of a parabola,
   and is tried on a disc in stest.py): from each point of the curve draw the chord that cuts off a cap of area s; the
   midpoints of the chords are the new curve. One such step is the flow for a time w s^(2/3), w = (1/2)(3/2)^(2/3).
   Here the curve is a polygon of M points, s is a fixed part ETA of the area that is left, the points are spread evenly
   along the new curve after each step, and when the area has fallen to STOP of what it was the rest of the time is taken
   from the formula for an ellipse, (3/4)(area/pi)^(2/3), since by then the shape is one.

   usage: erode SHAPE M ETA STOP [-curves NAME EVERY]
     SHAPE  disc | ellipse | square | rect | triangle | hexagon | halfdisc | quarter | rtriangle (an equilateral triangle
            swollen by a quarter of its inradius) | file:NAME (a convex polygon, "x y" per line, counter-clockwise, taken as
            it is); every built-in shape has area pi
   One line of JSON: the time T to vanish, and "lower", the integral of dt over the affine length of the curve (the affine
   length being the area the curve loses in a unit of time), which is the least the integral I of flow.c can be.

   This program is the second witness for T: flow.c finds it another way. I first tried to get flow.c's sensitivity from
   this one too, by pushing a short stretch of the curve in a little and running on; that is wrong whenever the stretch is
   shorter than a chord (on a disc, where the answer is known, a push a tenth of the chord's width came out half as large
   again), because a step of erosion does not see a dent narrower than its chord as the flow does. It is taken out. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef struct { double x, y; } pt;
static const double OMEGA = 0.65518535034906170;      /* (1/2) (3/2)^(2/3) */
static double cross(pt a, pt b, pt c) { return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x); }
static double area(const pt *P, int M) { double s = 0; int i; for (i = 0; i < M; i++) { pt a = P[i], b = P[(i + 1) % M]; s += a.x * b.y - a.y * b.x; } return s / 2; }
/* M points evenly along the closed polygon P (N points), starting at P[0] */
static void spread(const pt *P, int N, pt *Q, int M) {
    double L = 0, acc = 0, step; int i, k = 0; double *len = malloc(sizeof(double) * N);
    for (i = 0; i < N; i++) { pt a = P[i], b = P[(i + 1) % N]; len[i] = hypot(b.x - a.x, b.y - a.y); L += len[i]; }
    step = L / M;
    for (i = 0; i < N && k < M; i++) {
        pt a = P[i], b = P[(i + 1) % N];
        while (k < M && k * step <= acc + len[i] + 1e-15 * L) { double t = len[i] > 0 ? (k * step - acc) / len[i] : 0; Q[k].x = a.x + t * (b.x - a.x); Q[k].y = a.y + t * (b.y - a.y); k++; }
        acc += len[i];
    }
    while (k < M) { Q[k] = P[0]; k++; }
    free(len);
}
/* one erosion: Q[i] = the midpoint of the chord from P[i] that cuts a cap of area s (the cap lies between the chord and the
   curve from P[i] onward, counter-clockwise); H[i] = the height of that cap taken as a parabola's, 3 s / (2 x chord); N[i] the
   inward normal of the chord. Returns 0 if a chord cannot be found. */
static int erode(const pt *P, int M, double s, pt *Q, double *H, pt *N) {
    int i, j = 1; double cap = 0;                               /* cap = area of the polygon P[i..j] */
    for (i = 0; i < M; i++) {
        if (j <= i) { j = i + 1; cap = 0; }
        for (;;) {
            double t = cross(P[i], P[j % M], P[(j + 1) % M]) / 2;
            if (cap + t >= s) {
                double f = t > 0 ? (s - cap) / t : 0; pt a = P[j % M], b = P[(j + 1) % M], B, c; double L;
                B.x = a.x + f * (b.x - a.x); B.y = a.y + f * (b.y - a.y); Q[i].x = (P[i].x + B.x) / 2; Q[i].y = (P[i].y + B.y) / 2;
                c.x = B.x - P[i].x; c.y = B.y - P[i].y; L = hypot(c.x, c.y); if (H) { H[i] = 1.5 * s / L; N[i].x = -c.y / L; N[i].y = c.x / L; }
                break;
            }
            cap += t; j++;
            if (j - i > M) return 0;
        }
        cap -= cross(P[i], P[(i + 1) % M], P[j % M]) / 2;      /* the cap from the next point: without the triangle at P[i] */
    }
    return 1;
}
static pt *shape(const char *name, int *n) {
    int i, K = 0; pt *V = malloc(sizeof(pt) * 4096);
    if (!strcmp(name, "disc") || !strcmp(name, "ellipse")) { double a = !strcmp(name, "disc") ? 1 : sqrt(3.0), b = 1 / a; K = 2880; for (i = 0; i < K; i++) { V[i].x = a * cos(2 * M_PI * i / K); V[i].y = b * sin(2 * M_PI * i / K); } }
    else if (!strcmp(name, "square") || !strcmp(name, "rect")) { double w = !strcmp(name, "square") ? sqrt(M_PI) : sqrt(3 * M_PI), h = M_PI / w; pt v[4] = {{-w / 2, -h / 2}, {w / 2, -h / 2}, {w / 2, h / 2}, {-w / 2, h / 2}}; K = 4; memcpy(V, v, sizeof v); }
    else if (!strcmp(name, "triangle")) { double a = sqrt(4 * M_PI / sqrt(3.0)), h = a * sqrt(3.0) / 2; pt v[3] = {{-a / 2, -h / 3}, {a / 2, -h / 3}, {0, 2 * h / 3}}; K = 3; memcpy(V, v, sizeof v); }
    else if (!strcmp(name, "rtriangle")) { double rin = sqrt(M_PI / (4.5 * sqrt(3.0) + M_PI / 16)), rr = rin / 4, a = 2 * sqrt(3.0) * rin; double vx[3] = {a / 2, 0, -a / 2}, vy[3] = {-rin, 2 * rin, -rin}; int j; K = 0;      /* each corner an arc of 120 degrees, a vertex every quarter of a degree */
        for (j = 0; j < 3; j++) for (i = 0; i <= 480; i++) { double th = (-90 + 120 * j + 0.25 * i) * M_PI / 180; V[K].x = vx[j] + rr * cos(th); V[K].y = vy[j] + rr * sin(th); K++; } }
    else if (!strcmp(name, "hexagon")) { double r = sqrt(2 * M_PI / (3 * sqrt(3.0))); K = 6; for (i = 0; i < K; i++) { V[i].x = r * cos(M_PI * i / 3); V[i].y = r * sin(M_PI * i / 3); } }
    else if (!strcmp(name, "halfdisc")) { double r = sqrt(2.0); K = 1441; for (i = 0; i < K; i++) { V[i].x = r * cos(M_PI * i / (K - 1)); V[i].y = r * sin(M_PI * i / (K - 1)); } }
    else if (!strcmp(name, "quarter")) { double r = 2.0; K = 0; V[K].x = 0; V[K].y = 0; K++; for (i = 0; i <= 720; i++) { V[K].x = r * cos(M_PI / 2 * i / 720); V[K].y = r * sin(M_PI / 2 * i / 720); K++; } }
    else if (!strncmp(name, "file:", 5)) { FILE *f = fopen(name + 5, "r"); double x, y; if (!f) return NULL; while (K < 4096 && fscanf(f, "%lf %lf", &x, &y) == 2) { V[K].x = x; V[K].y = y; K++; } fclose(f); }
    else return NULL;
    *n = K; return V;
}
typedef struct { double T, t, Afinal, lower; int steps; } res_t;
/* run the flow from P (M points) for at most maxsteps steps or until the area is below Astop; if pj >= 0, at step pj the new curve
   is pushed in by gamma x bump(i) x H; *eps gets the area so removed. Curves[j] (if not NULL) gets the curve before step j. */
static res_t run(const pt *P0, int M, double eta, double Astop, int maxsteps, int pj, int pi, int stride, double gamma, double *eps, pt **curves, double *dts) {
    pt *P = malloc(sizeof(pt) * M), *Q = malloc(sizeof(pt) * M), *N = malloc(sizeof(pt) * M); double *H = malloc(sizeof(double) * M); res_t r = {0, 0, 0, 0, 0}; int j, i;
    memcpy(P, P0, sizeof(pt) * M);
    for (j = 0; j < maxsteps; j++) {
        double A = area(P, M), s = eta * A, dt = OMEGA * pow(s, 2.0 / 3.0);
        if (A <= Astop) break;
        if (curves) { curves[j] = malloc(sizeof(pt) * M); memcpy(curves[j], P, sizeof(pt) * M); }
        if (dts) dts[j] = dt;
        if (!erode(P, M, s, Q, H, N)) break;
        if (j != pj) { double lost = A - area(Q, M); if (lost > 0) r.lower += dt * dt / lost; }      /* the affine length of the curve is the area it loses in a unit of time */
        if (j == pj) {
            double A1 = area(Q, M);
            for (i = -stride + 1; i < stride; i++) { int k = ((pi + i) % M + M) % M; double b = cos(M_PI * i / (2.0 * stride)); b *= b; Q[k].x += gamma * b * H[k] * N[k].x; Q[k].y += gamma * b * H[k] * N[k].y; }
            if (eps) *eps = A1 - area(Q, M);
        }
        spread(Q, M, P, M); r.t += dt; r.steps++;
    }
    r.Afinal = area(P, M); r.T = r.t + 0.75 * pow(r.Afinal / M_PI, 2.0 / 3.0);
    free(P); free(Q); free(N); free(H); return r;
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: erode SHAPE M ETA STOP [-curves NAME EVERY]\n"); return 2; }
    int M = atoi(argv[2]), K, i, j, every = 0; double eta = atof(argv[3]), stop = atof(argv[4]); const char *fcurves = NULL;
    for (i = 5; i < argc; i++) {
        if (!strcmp(argv[i], "-curves") && i + 2 < argc) { fcurves = argv[++i]; every = atoi(argv[++i]); }
        else { fprintf(stderr, "unknown option %s\n", argv[i]); return 2; }
    }
    pt *V = shape(argv[1], &K);
    if (!V || K < 3 || M < 64 || M > 100000 || !(eta > 0 && eta < 0.05) || !(stop > 0 && stop < 0.5)) { fprintf(stderr, "bad shape, M (64 to 100000), ETA (below 0.05) or STOP (below 0.5)\n"); return 2; }
    pt *P0 = malloc(sizeof(pt) * M); spread(V, K, P0, M);
    double A0 = area(P0, M); int maxsteps = 200000; pt **curves = calloc(maxsteps, sizeof(pt *)); double *dts = calloc(maxsteps, sizeof(double));
    res_t r = run(P0, M, eta, stop * A0, maxsteps, -1, 0, 1, 0, NULL, fcurves ? curves : NULL, dts);
    printf("{\"shape\":\"%s\",\"M\":%d,\"eta\":%g,\"stop\":%g,\"area\":%.9f,\"steps\":%d,\"T\":%.9f,\"time_run\":%.9f,\"area_left\":%.3e,\"lower\":%.9f", argv[1], M, eta, stop, A0, r.steps, r.T, r.t, r.Afinal, r.lower + 3 * cbrt(r.Afinal) / pow(8 * M_PI * M_PI, 2.0 / 3.0));
    if (fcurves) { FILE *f = fopen(fcurves, "w"); if (!f) return 3; for (j = 0; j < r.steps; j += every) { for (i = 0; i < M; i++) fprintf(f, "%.6f %.6f%s", curves[j][i].x, curves[j][i].y, i + 1 < M ? " " : "\n"); } fclose(f); }
    printf("}\n");
    return 0;
}
