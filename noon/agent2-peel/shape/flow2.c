/* flow2.c: flow.c with one more option, made after the second sheet (flow.c itself is as sealed):
     -add M EPS DEG   add EPS cos(M (theta - DEG degrees)) to the support function (up to eight times); the shape must stay convex.
   With it a corner can be given a radius of curvature that varies across it, as the referee's lowest shape has.

   flow.c: the affine curve shortening flow of a convex shape in its support function, and, by one solve backward, how much the
   time the shape takes to vanish answers to a little area taken away at each place and moment. Noon (agent2), 25 November 2026.

   h(theta) is the support function (how far the shape reaches in direction theta); R = h + h'' is the radius of curvature of
   the point whose outward normal is theta, and ds = R dtheta. The flow (every point inward with the cube root of its
   curvature) is   dh/dt = -R^(-1/3).   On M equal angles, with R_k = h_k + (h_{k+1} - 2 h_k + h_{k-1}) / (2 - 2 cos dtheta)
   (that divisor, and not dtheta^2, so that moving the shape bodily leaves R alone), stepped implicitly:
        h' + dt R(h')^(-1/3) = h          (Newton; a cyclic tridiagonal solve each time).
   A corner has R = 0, where the flow is infinitely fast; every shape is first swollen by RHO0 (a disc of that radius added),
   and the first steps are tiny, growing by a twelfth each time. When the area is down to STOP of what it was, the time left
   is taken as an ellipse's, (3/4)(area/pi)^(2/3).

   The sensitivity. Let T be the time to vanish, as this program computes it from the shape at step n. If the curve at step n
   is pushed in by d at the node k, T falls by g_k d: g is the gradient of T. At the last step g_k = (dT/dA) R_k dtheta. And
   since one step is  h_n -> h_{n+1}  with  (1 - (dt/3) W L) dh_{n+1} = dh_n  to first order (W = diag R^(-4/3), L = 1 + d^2),
   the gradient one step earlier solves the transposed system  (1 - (dt/3) L W) g_n = g_{n+1}.  The time lost for a unit of
   area removed at node k is psi_k = g_k / (R_k dtheta). The program prints
        I = the integral of psi^2 over the shape (the sum over steps and nodes of psi^2 x the area swept there),
        the same integral of psi, which must be T, the least that I can be for the T found, T^2 / area, and the furthest
        that the integral of psi round one curve (which must be 1) is from 1 at any moment after t = 0.001;
        I_edge = (3/2) <g, L^(-1) g>, the same I from the starting curve's gradient alone (see the end of the program);
        shortfall = -(3/2) <z, L^(-1) z> with z = g - (2/3)(T/area) R, which is (4/3) T^2/area - I and is never negative;
        leak = how much of cos and sin there is in g (it must be nothing).

   The steps are governed by three numbers: none is longer than DTMAX (1e-4), none longer than a hundredth of the time left
   (as an ellipse of the same area would have it), and each is at most 13/12 of the one before. -q Q scales all three
   together (DTMAX = 1e-4 Q, a fraction 0.01 Q, growth 1 + Q/12), so that the error of the stepping is in proportion to Q
   and two runs at Q and Q/2 can be carried to the limit.

   usage: flow SHAPE M [-q Q] [-dt DTMAX] [-stop STOP] [-rho0 RHO0] [-map NAME EVERY] [-along NAME]
     SHAPE  disc | ellipse | square | rect | triangle | hexagon | halfdisc | quarter | rtriangle      (each of area pi)
            | poly:x1,y1,x2,y2,... (a convex polygon, corners in order) | cap:DEG (a disc cut by a chord) | wave:m:eps
     -map   write, for every EVERY-th step and every node: step, t, x, y, psi, R, the area swept there in that step
     -along write, for every step: step, t, the time left, the area, the affine length, the integral of psi^2 round the curve,
            and the integral of psi^2 over what the curve encloses
   One line of JSON. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static int M; static double dth, cdiv; static int nadd = 0; static double addm[8], adde[8], addp[8];
static double extra(double th) { double v = 0; int i; for (i = 0; i < nadd; i++) v += adde[i] * cos(addm[i] * (th - addp[i])); return v; }
static void applyL(const double *h, double *R) { int k; for (k = 0; k < M; k++) R[k] = h[k] + (h[(k + 1) % M] - 2 * h[k] + h[(k + M - 1) % M]) / cdiv; }
/* solve the cyclic tridiagonal system  a[k] x[k-1] + b[k] x[k] + c[k] x[k+1] = d[k]  (indices mod M) */
static void cyclic(const double *a, const double *b, const double *c, const double *d, double *x) {
    static double *bb, *u, *z, *cp, *dp, *up; static int cap = 0; int k; double gamma, fact;
    if (cap < M) { cap = M; bb = realloc(bb, sizeof(double) * M); u = realloc(u, sizeof(double) * M); z = realloc(z, sizeof(double) * M); cp = realloc(cp, sizeof(double) * M); dp = realloc(dp, sizeof(double) * M); up = realloc(up, sizeof(double) * M); }
    gamma = -b[0]; for (k = 0; k < M; k++) { bb[k] = b[k]; u[k] = 0; }
    bb[0] = b[0] - gamma; bb[M - 1] = b[M - 1] - a[0] * c[M - 1] / gamma; u[0] = gamma; u[M - 1] = c[M - 1];
    /* Thomas for bb with right sides d and u */
    cp[0] = c[0] / bb[0]; dp[0] = d[0] / bb[0]; up[0] = u[0] / bb[0];
    for (k = 1; k < M; k++) { double m = bb[k] - a[k] * cp[k - 1]; cp[k] = c[k] / m; dp[k] = (d[k] - a[k] * dp[k - 1]) / m; up[k] = (u[k] - a[k] * up[k - 1]) / m; }
    x[M - 1] = dp[M - 1]; z[M - 1] = up[M - 1];
    for (k = M - 2; k >= 0; k--) { x[k] = dp[k] - cp[k] * x[k + 1]; z[k] = up[k] - cp[k] * z[k + 1]; }
    fact = (x[0] + a[0] * x[M - 1] / gamma) / (1 + z[0] + a[0] * z[M - 1] / gamma);
    for (k = 0; k < M; k++) x[k] -= fact * z[k];
}
static double hshape(const char *name, double th) {
    double c = cos(th), s = sin(th), v, w;
    if (!strcmp(name, "disc")) return 1;
    if (!strcmp(name, "ellipse")) return sqrt(3 * c * c + s * s / 3);
    if (!strcmp(name, "square")) { w = sqrt(M_PI) / 2; return w * (fabs(c) + fabs(s)); }
    if (!strcmp(name, "rect")) { w = sqrt(3 * M_PI) / 2; return w * fabs(c) + (M_PI / (4 * w)) * fabs(s); }                    /* three times as long as wide */
    if (!strcmp(name, "triangle")) { double a = sqrt(4 * M_PI / sqrt(3.0)), ht = a * sqrt(3.0) / 2, m = -1e300; double vx[3] = {-a / 2, a / 2, 0}, vy[3] = {-ht / 3, -ht / 3, 2 * ht / 3}; int i; for (i = 0; i < 3; i++) { v = vx[i] * c + vy[i] * s; if (v > m) m = v; } return m; }
    if (!strcmp(name, "rtriangle")) { double rin = sqrt(M_PI / (4.5 * sqrt(3.0) + M_PI / 16)), rr = rin / 4, a = 2 * sqrt(3.0) * rin; double m = -1e300; double vx[3] = {-a / 2, a / 2, 0}, vy[3] = {-rin, -rin, 2 * rin}; int i; for (i = 0; i < 3; i++) { v = vx[i] * c + vy[i] * s; if (v > m) m = v; } return m + rr; }   /* an equilateral triangle swollen by a quarter of its inradius: round corners */
    if (!strcmp(name, "hexagon")) { double r = sqrt(2 * M_PI / (3 * sqrt(3.0))), m = -1e300; int i; for (i = 0; i < 6; i++) { v = r * (cos(M_PI * i / 3) * c + sin(M_PI * i / 3) * s); if (v > m) m = v; } return m; }
    if (!strcmp(name, "halfdisc")) { double r = sqrt(2.0); return s >= 0 ? r : r * fabs(c); }                 /* the arc above y = 0, the flat side on it */
    if (!strcmp(name, "quarter")) { double r = 2.0; if (c >= 0 && s >= 0) return r; v = r * c; w = r * s; return v > w ? (v > 0 ? v : 0) : (w > 0 ? w : 0); }
    if (!strncmp(name, "poly:", 5)) {                                    /* poly:x1,y1,x2,y2,...  any convex polygon, scaled to area pi */
        static double px[64], py[64], sc = 0; static int np = 0; int i; double m = -1e300;
        if (!np) { const char *q = name + 5; char *e; double a2 = 0; while (np < 64) { px[np] = strtod(q, &e); if (e == q || *e != ',') break; q = e + 1; py[np] = strtod(q, &e); if (e == q) break; np++; if (*e != ',') break; q = e + 1; }
            if (np < 3) { np = 0; return NAN; } for (i = 0; i < np; i++) a2 += px[i] * py[(i + 1) % np] - px[(i + 1) % np] * py[i]; sc = sqrt(2 * M_PI / fabs(a2)); }
        for (i = 0; i < np; i++) { v = sc * (px[i] * c + py[i] * s); if (v > m) m = v; } return m; }
    if (!strncmp(name, "cap:", 4)) {                                     /* cap:DEG  the piece of a disc cut off by a chord seen from the centre under 2 DEG degrees, area pi */
        double ph = atof(name + 4) * M_PI / 180, r; if (!(ph > 0.05 && ph < M_PI - 0.05)) return NAN; r = sqrt(M_PI / (ph - sin(ph) * cos(ph)));
        if (s >= cos(ph)) return r;
        return r * (sin(ph) * fabs(c) + cos(ph) * s); }
    if (!strncmp(name, "wave:", 5)) {                                    /* wave:m:eps  h = 1 + eps cos(m theta), scaled to area pi; needs eps (m^2 - 1) < 1 */
        int m = atoi(name + 5); const char *q = strchr(name + 5, ':'); double eps = q ? atof(q + 1) : -1; if (m < 2 || !(eps >= 0 && eps * (m * m - 1) < 1)) return NAN;
        return (1 + eps * cos(m * th)) / sqrt(1 - eps * eps * (m * m - 1) / 2); }
    return NAN;
}
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: flow SHAPE M [-q Q] [-dt DTMAX] [-stop STOP] [-rho0 RHO0] [-map NAME EVERY] [-along NAME]\n"); return 2; }
    const char *name = argv[1], *fmap = NULL, *falong = NULL; double dtmax = 1e-4, stop = 1e-3, rho0 = 1e-6, frac = 0.01, grow = 13.0 / 12.0; int every = 1, i, k, n;
    M = atoi(argv[2]);
    for (i = 3; i < argc; i++) {
        if (!strcmp(argv[i], "-dt") && i + 1 < argc) dtmax = atof(argv[++i]);
        else if (!strcmp(argv[i], "-stop") && i + 1 < argc) stop = atof(argv[++i]);
        else if (!strcmp(argv[i], "-q") && i + 1 < argc) { double q = atof(argv[++i]); if (!(q > 0 && q <= 4)) { fprintf(stderr, "-q must be above 0 and at most 4\n"); return 2; } dtmax = 1e-4 * q; frac = 0.01 * q; grow = 1 + q / 12; }
        else if (!strcmp(argv[i], "-rho0") && i + 1 < argc) rho0 = atof(argv[++i]);
        else if (!strcmp(argv[i], "-add") && i + 3 < argc && nadd < 8) { addm[nadd] = atof(argv[++i]); adde[nadd] = atof(argv[++i]); addp[nadd] = atof(argv[++i]) * M_PI / 180; nadd++; }
        else if (!strcmp(argv[i], "-map") && i + 2 < argc) { fmap = argv[++i]; every = atoi(argv[++i]); }
        else if (!strcmp(argv[i], "-along") && i + 1 < argc) falong = argv[++i];
        else { fprintf(stderr, "unknown option %s\n", argv[i]); return 2; }
    }
    if (isnan(hshape(name, 0)) || M < 64 || M > 65536 || !(dtmax > 0 && dtmax < 0.01) || !(stop > 0 && stop < 0.5) || !(rho0 > 0 && rho0 <= 4) || every < 1) { fprintf(stderr, "bad shape, M (64 to 65536), -dt (below 0.01), -stop (below 0.5), -rho0 (at most 4)\n"); return 2; }
    dth = 2 * M_PI / M; cdiv = 2 - 2 * cos(dth);
    double *h = malloc(sizeof(double) * M), *hn = malloc(sizeof(double) * M), *R = malloc(sizeof(double) * M), *F = malloc(sizeof(double) * M), *a = malloc(sizeof(double) * M), *b = malloc(sizeof(double) * M), *c = malloc(sizeof(double) * M), *dx = malloc(sizeof(double) * M), *tr = malloc(sizeof(double) * M);
    for (k = 0; k < M; k++) h[k] = hshape(name, k * dth) + rho0 + extra(k * dth);
    applyL(h, R);
    double A0 = 0, A, t = 0; for (k = 0; k < M; k++) A0 += 0.5 * h[k] * R[k] * dth;
    int cap = 4096, N = 0; double **Rs = malloc(sizeof(double *) * cap), **hs = malloc(sizeof(double *) * cap), *dts = malloc(sizeof(double) * cap), *ts = malloc(sizeof(double) * cap), *As = malloc(sizeof(double) * cap);
    double dt = 1e-10; A = A0; int fails = 0;
    while (A > stop * A0) {
        double rem = 0.75 * pow(A / M_PI, 2.0 / 3.0), lim = dtmax < frac * rem ? dtmax : frac * rem; int it, okstep = 0;
        if (dt > lim) dt = lim;
        while (!okstep) {
            memcpy(hn, h, sizeof(double) * M);                    /* first guess: the old curve */
            for (it = 0; it < 60; it++) {
                double worst = 0, lam = 1; int bad = 0;
                applyL(hn, R); for (k = 0; k < M; k++) if (!(R[k] > 0)) bad = 1;
                if (bad) break;
                for (k = 0; k < M; k++) { double w = pow(R[k], -4.0 / 3.0) * dt / 3; F[k] = hn[k] + dt * pow(R[k], -1.0 / 3.0) - h[k]; a[k] = -w / cdiv; c[k] = -w / cdiv; b[k] = 1 - w * (1 - 2 / cdiv); if (fabs(F[k]) > worst) worst = fabs(F[k]); }
                if (worst < 1e-13) { okstep = 1; break; }
                for (k = 0; k < M; k++) F[k] = -F[k];
                cyclic(a, b, c, F, dx);
                { double big = 0; for (k = 0; k < M; k++) if (fabs(dx[k]) > big) big = fabs(dx[k]); if (big < 1e-14 && worst < 1e-10) { okstep = 1; break; } }      /* the correction is down in the rounding: the step is done */
                for (;;) {                                        /* a shorter step if the full one would make some R negative */
                    for (k = 0; k < M; k++) tr[k] = hn[k] + lam * dx[k];
                    applyL(tr, R); bad = 0; for (k = 0; k < M; k++) if (!(R[k] > 0)) { bad = 1; break; }
                    if (!bad || lam < 1e-6) break;
                    lam /= 2;
                }
                if (bad) break;
                memcpy(hn, tr, sizeof(double) * M);
            }
            if (!okstep) { dt /= 4; fails++; if (dt < 1e-16) { fprintf(stderr, "the stepping failed at t = %g\n", t); return 4; } }
        }
        if (N == cap) { cap *= 2; Rs = realloc(Rs, sizeof(double *) * cap); hs = realloc(hs, sizeof(double *) * cap); dts = realloc(dts, sizeof(double) * cap); ts = realloc(ts, sizeof(double) * cap); As = realloc(As, sizeof(double) * cap); }
        applyL(hn, R); Rs[N] = malloc(sizeof(double) * M); memcpy(Rs[N], R, sizeof(double) * M); hs[N] = NULL; if (fmap && N % every == 0) { hs[N] = malloc(sizeof(double) * M); memcpy(hs[N], hn, sizeof(double) * M); } dts[N] = dt; t += dt; ts[N] = t; N++;
        memcpy(h, hn, sizeof(double) * M);
        A = 0; for (k = 0; k < M; k++) A += 0.5 * h[k] * R[k] * dth;
        As[N - 1] = A; dt *= grow;
    }
    double T = t + 0.75 * pow(A / M_PI, 2.0 / 3.0), dTdA = 0.5 * pow(A / M_PI, -1.0 / 3.0) / M_PI;
    /* backward: g_N = dT/dA R_N dtheta; (1 - (dt_n/3) L W_n) g_{n-1} = g_n, where step n took the curve n-1 to the curve n with W_n = R_n^(-4/3) */
    double *g = malloc(sizeof(double) * M), *g2 = malloc(sizeof(double) * M), I = 0, P1 = 0, lower = 0, worst = 0; FILE *fm = fmap ? fopen(fmap, "w") : NULL;
    double Irem = 3 * cbrt(A) / pow(8 * M_PI * M_PI, 2.0 / 3.0); FILE *fa = falong ? fopen(falong, "w") : NULL;
    for (k = 0; k < M; k++) g[k] = dTdA * Rs[N - 1][k] * dth;
    for (n = N - 1; n >= 0; n--) {
        double *Rn = Rs[n], s1 = 0, La = 0, s2 = 0;
        double wt = n + 1 < N ? (dts[n] + dts[n + 1]) / 2 : dts[n] / 2;      /* the trapezoid rule over the moments t_1 ... t_N (the first step of all is 1e-10 long and is left to the rule's end) */
        for (k = 0; k < M; k++) { double psi = g[k] / (Rn[k] * dth), sw = wt * pow(Rn[k], 2.0 / 3.0) * dth; I += psi * psi * sw; s1 += psi * sw; s2 += psi * psi * pow(Rn[k], 2.0 / 3.0) * dth; La += pow(Rn[k], 2.0 / 3.0) * dth;
            if (fm && n % every == 0) { double hp = (hs[n][(k + 1) % M] - hs[n][(k + M - 1) % M]) / (2 * sin(dth)), th = k * dth; fprintf(fm, "%d %.8f %.6f %.6f %.8f %.6e %.6e\n", n, ts[n], hs[n][k] * cos(th) - hp * sin(th), hs[n][k] * sin(th) + hp * cos(th), psi, Rn[k], sw); } }
        if (fa) fprintf(fa, "%d %.10f %.9f %.9f %.9f %.9f %.9f\n", n, ts[n], T - ts[n], As[n], La, s2, I + Irem - 0.5 * s2 * wt);   /* step, t, time left, area, affine length, the integral of psi^2 round the curve, the integral of psi^2 over what is inside it */
        P1 += s1; lower += wt / La; if (ts[n] > 1e-3 && fabs(s1 / wt - 1) > worst) worst = fabs(s1 / wt - 1);
        /* the transposed system: coefficient of g_{n-1}[k] in row k is 1 - (dt/3) w_k (1 - 2/cdiv); of g_{n-1}[k-1]: -(dt/3) w_{k-1} / cdiv; of g_{n-1}[k+1]: -(dt/3) w_{k+1} / cdiv */
        for (k = 0; k < M; k++) { double wk = pow(Rn[k], -4.0 / 3.0) * dts[n] / 3, wm = pow(Rn[(k + M - 1) % M], -4.0 / 3.0) * dts[n] / 3, wp = pow(Rn[(k + 1) % M], -4.0 / 3.0) * dts[n] / 3; a[k] = -wm / cdiv; c[k] = -wp / cdiv; b[k] = 1 - wk * (1 - 2 / cdiv); }
        cyclic(a, b, c, g, g2); memcpy(g, g2, sizeof(double) * M);
    }
    if (fm) fclose(fm);
    if (fa) fclose(fa);
    /* The same integral from the edge alone. With g the gradient of T at the starting curve (g is now that), and L = 1 + d^2/dtheta^2,
           I = (3/2) <g, L^(-1) g>,
       because d/dt of 3 <g, L^(-1) g> along the flow is -2 x (the integral of psi^2 round the curve), and both vanish at the end.
       L kills cos and sin, and g has none of either (moving the shape bodily does not change T). In the discrete scheme the mode m
       has the eigenvalue 1 - (2 - 2 cos(m dtheta)) / (2 - 2 cos(dtheta)). */
    double Iedge = 0, leak = 0, zLz = 0, cc = 2.0 / 3.0 * T / A0;
    { int m; double *hh = malloc(sizeof(double) * M), *R0 = malloc(sizeof(double) * M); for (k = 0; k < M; k++) hh[k] = hshape(name, k * dth) + rho0 + extra(k * dth); applyL(hh, R0);
      for (m = 0; m <= M / 2; m++) { double cr = 0, ci = 0, zr = 0, zi = 0, lam = 1 - (2 - 2 * cos(m * dth)) / cdiv, mult = (m == 0 || 2 * m == M) ? 1 : 2;
        for (k = 0; k < M; k++) { double an = dth * (double)(((long long)m * k) % M), z = g[k] - cc * R0[k] * dth; cr += g[k] * cos(an); ci += g[k] * sin(an); zr += z * cos(an); zi += z * sin(an); }
        if (m == 1) { leak = sqrt(cr * cr + ci * ci); continue; }
        Iedge += mult * (cr * cr + ci * ci) / lam; zLz += mult * (zr * zr + zi * zi) / lam; }
      Iedge *= 1.5 / (M * dth); zLz *= 1.5 / (M * dth); free(hh); free(R0); }
    printf("{\"shape\":\"%s\",\"M\":%d,\"dtmax\":%g,\"frac\":%g,\"grow\":%.6f,\"stop\":%g,\"rho0\":%g,\"area\":%.9f,\"steps\":%d,\"halvings\":%d,\"T\":%.9f,\"I\":%.9f,\"psi_integral\":%.9f,\"worst_step_check\":%.2e,\"lower_bound_affine\":%.9f,\"lower_bound_T2_over_A\":%.9f,\"I_edge\":%.9f,\"shortfall\":%.9f,\"leak\":%.2e}\n",
           name, M, dtmax, frac, grow, stop, rho0, A0, N, fails, T, I + Irem, P1 + 0.75 * pow(A / M_PI, 2.0 / 3.0), worst, lower + Irem, T * T / A0, Iedge, -zLz, leak);
    return 0;
}
