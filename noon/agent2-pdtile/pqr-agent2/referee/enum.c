// enum.c -- referee's independent exhaustive enumeration of all subsets A of Z_M containing 0,
// M = p0*p1*p2 squarefree with M <= 31 (intended: M = 30).
//
// For every subset it computes the pattern Z_A in TWO independent ways:
//   (R) exact cyclotomic division: A(X) mod Phi_d(X) over Z, for each d | M, d > 1;
//   (C) the coordinate criteria (F1), (F2), (F3) of the note (integer linear functionals of the counts).
// and compares.  It accumulates hist[mask][n] (mask = pattern, n = |A|), tests brute-force tiling for
// every subset whose size divides M, and tests the set-theoretic lemmas of the note on every subset
// that meets their premises.
//
// mask bits: 0,1,2 : p0,p1,p2 in Z_A (E);  3: p0p1, 4: p0p2, 5: p1p2 (P);  6: M (t).
//
// build: gcc -O2 -mavx2 -fopenmp -o enum enum.c
// run:   ./enum 2 3 5 out_prefix

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <immintrin.h>
#include <omp.h>

static int p[3], M;
static uint32_t FULL;
static int cx[32][3];            // coordinates of the elements
static int segoff[7], seglen[7]; // layout of the 7 segments in the 32-byte vectors
static uint32_t segbits[7];
static int divd[7];              // the divisor of each segment
static int PAIRBIT[3][3];

enum {
    C_TOTAL, C_MISMATCH,
    C_I4_PREM, C_I4_FAIL,
    C_L3_PREM, C_L3_FAIL, C_L3_A0POS, C_L3_A0POS_FAIL,
    C_L4A_PREM, C_L4A_FAIL, C_L4A_CONV_PREM, C_L4A_CONV_FAIL,
    C_L4B_PREM_P, C_L4B_PREM_EMPTY, C_L4B_PREM_BOTH, C_L4B_FAIL_T, C_L4B_FAIL_LINES,
    C_L4B_NOPREM, C_L4B_NOPREM_TNONZERO,
    C_I6_PREM, C_I6_FAIL,
    C_S5XY_PREM, C_S5XY_FAIL,
    C_S5ALL_PREM, C_S5ALL_A0POS, C_S5ALL_A0POS_FAIL, C_S5ALL_A0ZERO, C_S5ALL_A0ZERO_FAIL,
    C_L5_PREM, C_L5_FAIL, C_L5_TINT_FAIL,
    C_R1_PREM, C_R1_STEPFAIL, C_R1_ZNOTINE, C_R2_PREM, C_R2_STEPFAIL, C_R2_A0ZERO, C_R2_A0ZERO_STEPFAIL, C_R2_YZNOTINE,
    C_G1_PREM, C_G1_FAIL, C_G2_PREM, C_G2_FAIL,
    NCNT
};
static const char *CNAME[NCNT] = {
    "TOTAL", "MISMATCH_R_vs_C",
    "I4_PREM", "I4_FAIL",
    "L3_PREM", "L3_FAIL", "L3_A0POS", "L3_A0POS_FAIL",
    "L4A_PREM", "L4A_FAIL", "L4A_CONV_PREM", "L4A_CONV_FAIL",
    "L4B_PREM_P", "L4B_PREM_EMPTY", "L4B_PREM_BOTH", "L4B_FAIL_T", "L4B_FAIL_LINES",
    "L4B_NOPREM", "L4B_NOPREM_TNONZERO",
    "I6_PREM", "I6_FAIL",
    "S5XY_PREM", "S5XY_FAIL",
    "S5ALL_PREM", "S5ALL_A0POS", "S5ALL_A0POS_FAIL", "S5ALL_A0ZERO", "S5ALL_A0ZERO_FAIL",
    "L5_PREM", "L5_FAIL", "L5_TINT_FAIL",
    "R1_PREM", "R1_STEPFAIL", "R1_ZNOTINE_FAIL", "R2_PREM", "R2_STEPFAIL", "R2_A0ZERO", "R2_A0ZERO_STEPFAIL", "R2_YZNOTINE_FAIL",
    "G1_PREM", "G1_FAIL", "G2_PREM", "G2_FAIL",
};

typedef struct {
    uint64_t hist[128][33];
    uint64_t tile[128][33];
    uint32_t repmin[128][33], repmax[128][33], rephash[128][33], rephv[128][33];
    uint64_t cnt[NCNT];
    // per role (z = slicing coordinate) counts for Lemma 4(b)
    uint64_t l4b_prem_role[3], s5xy_prem_role[6], l3_prem_pair[3], l5_prem_pair[3];
    uint32_t firstfail[NCNT];
} acc_t;

// ---------- polynomials ----------
#define PL 80
static void cyclo(int n, int *out /*len PL*/, int *deg);
static int cyc_cache_deg[64];
static int cyc_cache[64][PL];
static int cyc_have[64];

static void cyclo(int n, int *out, int *deg) {
    if (cyc_have[n]) { memcpy(out, cyc_cache[n], sizeof(int) * PL); *deg = cyc_cache_deg[n]; return; }
    int num[PL]; memset(num, 0, sizeof num);
    num[n] = 1; num[0] = -1; int nd = n;      // X^n - 1
    for (int e = 1; e < n; e++) if (n % e == 0) {
        int q[PL], qd; cyclo(e, q, &qd);
        // exact division num / q (q monic)
        int quo[PL]; memset(quo, 0, sizeof quo);
        int r[PL]; memcpy(r, num, sizeof r);
        for (int k = nd; k >= qd; k--) {
            int c = r[k];
            if (c) { quo[k - qd] = c; for (int j = 0; j <= qd; j++) r[k - qd + j] -= c * q[j]; }
        }
        for (int k = 0; k < PL; k++) if (r[k]) { fprintf(stderr, "cyclo: inexact\n"); exit(1); }
        memcpy(num, quo, sizeof num); nd -= qd;
    }
    memcpy(cyc_cache[n], num, sizeof num); cyc_cache_deg[n] = nd; cyc_have[n] = 1;
    memcpy(out, num, sizeof(int) * PL); *deg = nd;
}

static int8_t vecR[32][32], vecC[32][32];

static void build_vectors(void) {
    // segment order: p0,p1,p2,p0p1,p0p2,p1p2,M
    divd[0] = p[0]; divd[1] = p[1]; divd[2] = p[2];
    divd[3] = p[0] * p[1]; divd[4] = p[0] * p[2]; divd[5] = p[1] * p[2]; divd[6] = M;
    int off = 0;
    memset(vecR, 0, sizeof vecR); memset(vecC, 0, sizeof vecC);
    for (int s = 0; s < 7; s++) {
        int phi[PL], deg; cyclo(divd[s], phi, &deg);
        segoff[s] = off; seglen[s] = deg;
        segbits[s] = 0; for (int k = 0; k < deg; k++) segbits[s] |= 1u << (off + k);
        // X^k mod Phi_d
        int cur[PL]; memset(cur, 0, sizeof cur); cur[0] = 1;
        for (int e = 0; e < M; e++) {
            for (int k = 0; k < deg; k++) {
                if (cur[k] < -3 || cur[k] > 3) { fprintf(stderr, "coefficient too large\n"); exit(1); }
                vecR[e][off + k] = (int8_t)cur[k];
            }
            // multiply by X and reduce
            for (int k = deg; k >= 1; k--) cur[k] = cur[k - 1];
            cur[0] = 0;
            int c = cur[deg];
            if (c) for (int k = 0; k <= deg; k++) cur[k] -= c * phi[k];
        }
        off += deg;
    }
    if (off != M - 1 || off > 32) { fprintf(stderr, "layout error %d\n", off); exit(1); }
    // counts functionals, same layout
    for (int e = 0; e < M; e++) {
        int o = 0;
        for (int x = 0; x < 3; x++)                       // F1: N_x(i) - N_x(0), i = 1..p_x-1
            for (int i = 1; i < p[x]; i++) vecC[e][o++] = (int8_t)((cx[e][x] == i) - (cx[e][x] == 0));
        for (int x = 0; x < 3; x++) for (int y = x + 1; y < 3; y++)   // F2: mixed second difference of N_xy
            for (int i = 1; i < p[x]; i++) for (int j = 1; j < p[y]; j++)
                vecC[e][o++] = (int8_t)(((cx[e][x] == i) - (cx[e][x] == 0)) * ((cx[e][y] == j) - (cx[e][y] == 0)));
        for (int i = 1; i < p[0]; i++) for (int j = 1; j < p[1]; j++) for (int k = 1; k < p[2]; k++)  // F3
            vecC[e][o++] = (int8_t)(((cx[e][0] == i) - (cx[e][0] == 0)) * ((cx[e][1] == j) - (cx[e][1] == 0)) *
                                    ((cx[e][2] == k) - (cx[e][2] == 0)));
        if (o != M - 1) { fprintf(stderr, "layout error C %d\n", o); exit(1); }
    }
    // the F2 segments are laid out in the order (0,1),(0,2),(1,2) = bits 3,4,5 : lengths must match phi
    {
        int o = 0, ok = 1;
        for (int x = 0; x < 3; x++) { ok &= (segoff[x] == o && seglen[x] == p[x] - 1); o += p[x] - 1; }
        int s = 3;
        for (int x = 0; x < 3; x++) for (int y = x + 1; y < 3; y++) {
            ok &= (segoff[s] == o && seglen[s] == (p[x] - 1) * (p[y] - 1)); o += (p[x] - 1) * (p[y] - 1); s++;
        }
        ok &= (segoff[6] == o);
        if (!ok) { fprintf(stderr, "segment layouts differ\n"); exit(1); }
    }
    // overflow guard for int8 sums
    for (int k = 0; k < 32; k++) {
        int sr = 0, sc = 0;
        for (int e = 0; e < M; e++) { sr += abs(vecR[e][k]); sc += abs(vecC[e][k]); }
        if (sr > 127 || sc > 127) { fprintf(stderr, "int8 overflow possible\n"); exit(1); }
    }
}

static inline int segmask(uint32_t nz) {
    int m = 0;
    for (int s = 0; s < 7; s++) m |= ((nz & segbits[s]) == 0) << s;
    return m;
}

// ---------- tiling by brute force ----------
static inline uint32_t rotl(uint32_t A, int b) { return ((A << b) | (A >> (M - b))) & FULL; }
static int cover(uint32_t A, uint32_t covered) {
    if (covered == FULL) return 1;
    int u = __builtin_ctz(~covered);
    uint32_t rem = A;
    while (rem) {
        int a = __builtin_ctz(rem); rem &= rem - 1;
        int b = u - a; if (b < 0) b += M;
        if (b == 0) continue;
        uint32_t T = rotl(A, b);
        if (!(T & covered) && cover(A, covered | T)) return 1;
    }
    return 0;
}

// ---------- structural checks ----------
static inline void fail(acc_t *acc, int c, uint32_t A) { if (!acc->cnt[c]) acc->firstfail[c] = A; acc->cnt[c]++; }

// N_xy as a p_x by p_y matrix
static void getN(uint32_t A, int x, int y, int N[8][8]) {
    for (int i = 0; i < p[x]; i++) for (int j = 0; j < p[y]; j++) N[i][j] = 0;
    uint32_t rem = A;
    while (rem) { int e = __builtin_ctz(rem); rem &= rem - 1; N[cx[e][x]][cx[e][y]]++; }
}
// normal form of an additive matrix; returns 1 if N == a0 + al_i + be_j
static int normal(int N[8][8], int px, int py, int *a0, int al[8], int be[8], int *Sa, int *Sb) {
    int mn = 1 << 30;
    for (int i = 0; i < px; i++) for (int j = 0; j < py; j++) if (N[i][j] < mn) mn = N[i][j];
    *a0 = mn; *Sa = 0; *Sb = 0;
    for (int i = 0; i < px; i++) { int m = 1 << 30; for (int j = 0; j < py; j++) if (N[i][j] < m) m = N[i][j]; al[i] = m - mn; *Sa += al[i]; }
    for (int j = 0; j < py; j++) { int m = 1 << 30; for (int i = 0; i < px; i++) if (N[i][j] < m) m = N[i][j]; be[j] = m - mn; *Sb += be[j]; }
    for (int i = 0; i < px; i++) for (int j = 0; j < py; j++) if (N[i][j] != mn + al[i] + be[j]) return 0;
    return 1;
}

static void slow(uint32_t A, int mask, int n, acc_t *acc) {
    int E[3] = { mask & 1, (mask >> 1) & 1, (mask >> 2) & 1 };
    int t = (mask >> 6) & 1;
    int nE = E[0] + E[1] + E[2];
    int nP = ((mask >> 3) & 1) + ((mask >> 4) & 1) + ((mask >> 5) & 1);
#define INP(x, y) ((mask >> PAIRBIT[x][y]) & 1)

    // (I4) and Lemma 3, for each pair in P
    int a0s[3] = { -1, -1, -1 };
    for (int x = 0; x < 3; x++) for (int y = x + 1; y < 3; y++) if (INP(x, y)) {
        int N[8][8], a0, al[8], be[8], Sa, Sb;
        getN(A, x, y, N);
        acc->cnt[C_I4_PREM]++;
        int ok = normal(N, p[x], p[y], &a0, al, be, &Sa, &Sb);
        if (!ok) fail(acc, C_I4_FAIL, A);
        else {
            if ((Sa == 0) != (E[x] != 0) || (Sb == 0) != (E[y] != 0)) fail(acc, C_I4_FAIL, A);
            if (n != p[x] * p[y] * a0 + p[y] * Sa + p[x] * Sb) fail(acc, C_I4_FAIL, A);
        }
        a0s[PAIRBIT[x][y] - 3] = a0;
        if (!E[x] && !E[y]) {
            acc->cnt[C_L3_PREM]++; acc->l3_prem_pair[PAIRBIT[x][y] - 3]++;
            if (!ok || Sa < 1 || Sb < 1 || n < p[x] + p[y]) fail(acc, C_L3_FAIL, A);
            if (a0 >= 1) { acc->cnt[C_L3_A0POS]++; if (n < p[x] * p[y] + p[x] + p[y]) fail(acc, C_L3_A0POS_FAIL, A); }
        }
    }

    // Lemma 5 (also taken from the histogram afterwards): |A| = p_x p_y, x,y in E, t = 1  =>  {x,y} in P
    if (t) for (int x = 0; x < 3; x++) for (int y = x + 1; y < 3; y++) if (E[x] && E[y] && n == p[x] * p[y]) {
        acc->cnt[C_L5_PREM]++; acc->l5_prem_pair[PAIRBIT[x][y] - 3]++;
        if (!INP(x, y)) fail(acc, C_L5_FAIL, A);
    }

    // Section 5, E = {x}, {y,z} in P, {x,y} in P : all six role assignments
    {
        static const int perm[6][3] = { {0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0} };
        for (int r = 0; r < 6; r++) {
            int x = perm[r][0], y = perm[r][1], z = perm[r][2];
            if (!(E[x] && !E[y] && !E[z] && INP(y, z) && INP(x, y))) continue;
            acc->cnt[C_S5XY_PREM]++; acc->s5xy_prem_role[r]++;
            int Nxy[8][8], Nyz[8][8], b0, al[8], be[8], Sa, Sb, bad = 0;
            getN(A, x, y, Nxy); getN(A, y, z, Nyz);
            for (int j = 0; j < p[y]; j++) {
                int Ny = 0;
                for (int i = 0; i < p[x]; i++) { if (Nxy[i][j] != Nxy[0][j]) bad = 1; Ny += Nxy[i][j]; }
                if (Ny % p[x]) bad = 1;
            }
            if (!normal(Nyz, p[y], p[z], &b0, al, be, &Sa, &Sb)) bad = 1;
            for (int j = 0; j < p[y]; j++) if (al[j] % p[x]) bad = 1;
            if (Sa < p[x]) bad = 1;
            if (n != p[y] * p[z] * b0 + p[z] * Sa + p[y] * Sb) bad = 1;
            if (n < p[z] * p[x] + p[y]) bad = 1;
            if (bad) fail(acc, C_S5XY_FAIL, A);
        }
    }

    // Section 5, E empty, P = all three pairs
    if (nE == 0 && nP == 3) {
        acc->cnt[C_S5ALL_PREM]++;
        int anypos = 0;
        for (int x = 0; x < 3; x++) for (int y = x + 1; y < 3; y++) if (a0s[PAIRBIT[x][y] - 3] >= 1) {
            anypos = 1;
            if (n < p[x] * p[y] + p[x] + p[y]) fail(acc, C_S5ALL_A0POS_FAIL, A);
        }
        if (anypos) acc->cnt[C_S5ALL_A0POS]++;
        else {
            acc->cnt[C_S5ALL_A0ZERO]++;
            static const int perm[6][3] = { {0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0} };
            int bad = 0;
            for (int r = 0; r < 6; r++) {
                int x = perm[r][0], y = perm[r][1], z = perm[r][2];
                int Nxy[8][8], Nxz[8][8], a0, a0p, al[8], be[8], alp[8], ga[8], Sa, Sb, Sap, Sg;
                getN(A, x, y, Nxy); getN(A, x, z, Nxz);
                if (!normal(Nxy, p[x], p[y], &a0, al, be, &Sa, &Sb)) bad = 1;
                if (!normal(Nxz, p[x], p[z], &a0p, alp, ga, &Sap, &Sg)) bad = 1;
                if (a0 || a0p) bad = 1;
                if (Sb != Sg) bad = 1;
                for (int i = 0; i < p[x]; i++) { if (p[y] * al[i] != p[z] * alp[i]) bad = 1; if (al[i] % p[z]) bad = 1; }
                if (Sa < p[z]) bad = 1;
                if (n != p[y] * Sa + p[x] * Sb) bad = 1;
                if (n < p[y] * p[z] + p[x]) bad = 1;
            }
            if (bad) fail(acc, C_S5ALL_A0ZERO_FAIL, A);
        }
    }

    // Lemma 4 (t = 1), and its converse direction on every set that reaches this function with t = 0
    for (int z = 0; z < 3; z++) {
        int x = (z == 0) ? 1 : 0, y = (z == 2) ? 1 : 2;       // x < y, the other two coordinates
        int px = p[x], py = p[y], pz = p[z];
        int sl[8][8][8]; memset(sl, 0, sizeof sl);
        uint32_t rem = A;
        while (rem) { int e = __builtin_ctz(rem); rem &= rem - 1; sl[cx[e][z]][cx[e][x]][cx[e][y]] = 1; }
        int T[8][8][8]; int allequal = 1, anyempty = 0, Tzero = 1, alllines = 1;
        for (int c = 0; c < pz; c++) {
            int R[8] = {0}, C[8] = {0}, S = 0;
            for (int i = 0; i < px; i++) for (int j = 0; j < py; j++) { R[i] += sl[c][i][j]; C[j] += sl[c][i][j]; S += sl[c][i][j]; }
            if (S == 0) anyempty = 1;
            int additive = 1;
            for (int i = 0; i < px; i++) for (int j = 0; j < py; j++) {
                T[c][i][j] = px * py * sl[c][i][j] - px * R[i] - py * C[j] + S;     // p_x p_y (A_c)°(i,j)
                if (T[c][i][j] != T[0][i][j]) allequal = 0;
                if (T[c][i][j]) { Tzero = 0; additive = 0; }
            }
            // union of full lines in the x-direction (depends on j only) or in the y-direction (on i only)?
            int depj = 1, depi = 1;
            for (int i = 0; i < px; i++) for (int j = 0; j < py; j++) {
                if (sl[c][i][j] != sl[c][0][j]) depj = 0;
                if (sl[c][i][j] != sl[c][i][0]) depi = 0;
            }
            if (!(depj || depi)) alllines = 0;
            // (I6): an additive 0/1 matrix is a union of full rows or of full columns
            if (additive) { acc->cnt[C_I6_PREM]++; if (!(depj || depi)) fail(acc, C_I6_FAIL, A); }
        }
        if (t) {
            acc->cnt[C_L4A_PREM]++;
            if (!allequal) fail(acc, C_L4A_FAIL, A);
            int premP = INP(x, y), premE = anyempty;
            if (premP || premE) {
                if (premP) acc->cnt[C_L4B_PREM_P]++;
                if (premE) acc->cnt[C_L4B_PREM_EMPTY]++;
                if (premP && premE) acc->cnt[C_L4B_PREM_BOTH]++;
                acc->l4b_prem_role[z]++;
                if (!Tzero) fail(acc, C_L4B_FAIL_T, A);
                if (!alllines) fail(acc, C_L4B_FAIL_LINES, A);
            } else {
                acc->cnt[C_L4B_NOPREM]++;
                if (!Tzero) acc->cnt[C_L4B_NOPREM_TNONZERO]++;   // shows the premise of (b) is not vacuous
            }
        } else {
            acc->cnt[C_L4A_CONV_PREM]++;
            if (allequal) fail(acc, C_L4A_CONV_FAIL, A);   // by (F3)+(I5), equal centred slices would force t = 1
        }
    }
    // ---- relaxed (non-vacuous) versions of the internal steps of Section 5, and the referee's sharper statements
    {
        static const int perm[6][3] = { {0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0} };
        for (int r = 0; r < 6; r++) {
            int x = perm[r][0], y = perm[r][1], z = perm[r][2];
            // R1: x in E, y not in E, {y,z} in P, {x,y} in P  (nothing assumed about z)
            if (E[x] && !E[y] && INP(y, z) && INP(x, y)) {
                acc->cnt[C_R1_PREM]++;
                int Nxy[8][8], Nyz[8][8], b0, al[8], be[8], Sa, Sb, bad = 0;
                getN(A, x, y, Nxy); getN(A, y, z, Nyz);
                for (int j = 0; j < p[y]; j++) {
                    int Ny = 0;
                    for (int i = 0; i < p[x]; i++) { if (Nxy[i][j] != Nxy[0][j]) bad = 1; Ny += Nxy[i][j]; }
                    if (Ny % p[x]) bad = 1;
                }
                if (!normal(Nyz, p[y], p[z], &b0, al, be, &Sa, &Sb)) bad = 1;
                for (int j = 0; j < p[y]; j++) if (al[j] % p[x]) bad = 1;
                if (Sa < p[x]) bad = 1;
                if (n < p[z] * p[x] + p[y] * Sb) bad = 1;
                if (bad) fail(acc, C_R1_STEPFAIL, A);
                if (!E[z]) fail(acc, C_R1_ZNOTINE, A);          // referee: z must then be in E
            }
            // R2: {x,y},{x,z} in P, x not in E (nothing assumed about y, z or {y,z})
            if (y < z && !E[x] && INP(x, y) && INP(x, z)) {
                acc->cnt[C_R2_PREM]++;
                int Nxy[8][8], Nxz[8][8], a0, a0p, al[8], be[8], alp[8], ga[8], Sa, Sb, Sap, Sg, bad = 0;
                getN(A, x, y, Nxy); getN(A, x, z, Nxz);
                if (!normal(Nxy, p[x], p[y], &a0, al, be, &Sa, &Sb)) bad = 1;
                if (!normal(Nxz, p[x], p[z], &a0p, alp, ga, &Sap, &Sg)) bad = 1;
                for (int i = 0; i < p[x]; i++) { if (p[y] * al[i] != p[z] * alp[i]) bad = 1; if (al[i] % p[z]) bad = 1; if (alp[i] % p[y]) bad = 1; }
                if (Sa < p[z] || Sap < p[y]) bad = 1;
                if (bad) fail(acc, C_R2_STEPFAIL, A);
                if (a0 == 0 && a0p == 0) {                       // the note's situation
                    acc->cnt[C_R2_A0ZERO]++;
                    if (Sb != Sg || n != p[y] * Sa + p[x] * Sb || n < p[y] * p[z] + p[x] * Sb) fail(acc, C_R2_A0ZERO_STEPFAIL, A);
                }
                if (!(E[y] && E[z])) fail(acc, C_R2_YZNOTINE, A);  // referee: y and z must then be in E
            }
        }
        // G1 (Lemma 5 without the hypothesis on |A|): x,y in E, t = 1  =>  {x,y} in P
        if (t) for (int x = 0; x < 3; x++) for (int y = x + 1; y < 3; y++) if (E[x] && E[y]) {
            acc->cnt[C_G1_PREM]++; if (!INP(x, y)) fail(acc, C_G1_FAIL, A);
        }
        // G2: x in E, {y,z} in P, t = 1  =>  y in E or z in E
        if (t) for (int x = 0; x < 3; x++) { int y = (x == 0) ? 1 : 0, z = (x == 2) ? 1 : 2;
            if (E[x] && INP(y, z)) { acc->cnt[C_G2_PREM]++; if (!(E[y] || E[z])) fail(acc, C_G2_FAIL, A); }
        }
    }
#undef INP
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: enum p0 p1 p2 outprefix\n"); return 1; }
    p[0] = atoi(argv[1]); p[1] = atoi(argv[2]); p[2] = atoi(argv[3]);
    M = p[0] * p[1] * p[2];
    if (M > 31) { fprintf(stderr, "M too large\n"); return 1; }
    FULL = (1u << M) - 1;
    for (int e = 0; e < M; e++) for (int w = 0; w < 3; w++) cx[e][w] = e % p[w];
    PAIRBIT[0][1] = PAIRBIT[1][0] = 3; PAIRBIT[0][2] = PAIRBIT[2][0] = 4; PAIRBIT[1][2] = PAIRBIT[2][1] = 5;
    build_vectors();

    int LOB = (M - 1) / 2, HB = M - 1 - LOB;   // element 0 fixed; elements 1..LOB low; LOB+1..M-1 high
    size_t nlo = (size_t)1 << LOB, nhi = (size_t)1 << HB;
    __m256i *TLR = aligned_alloc(32, nlo * 32), *TLC = aligned_alloc(32, nlo * 32);
    __m256i *THR = aligned_alloc(32, nhi * 32), *THC = aligned_alloc(32, nhi * 32);
    uint8_t *lopc = malloc(nlo);
    TLR[0] = _mm256_loadu_si256((const __m256i *)vecR[0]);
    TLC[0] = _mm256_loadu_si256((const __m256i *)vecC[0]);
    lopc[0] = 0;
    for (size_t s = 1; s < nlo; s++) {
        int b = __builtin_ctzl(s); size_t r = s & (s - 1);
        TLR[s] = _mm256_add_epi8(TLR[r], _mm256_loadu_si256((const __m256i *)vecR[1 + b]));
        TLC[s] = _mm256_add_epi8(TLC[r], _mm256_loadu_si256((const __m256i *)vecC[1 + b]));
        lopc[s] = lopc[r] + 1;
    }
    THR[0] = _mm256_setzero_si256(); THC[0] = _mm256_setzero_si256();
    for (size_t s = 1; s < nhi; s++) {
        int b = __builtin_ctzl(s); size_t r = s & (s - 1);
        THR[s] = _mm256_add_epi8(THR[r], _mm256_loadu_si256((const __m256i *)vecR[1 + LOB + b]));
        THC[s] = _mm256_add_epi8(THC[r], _mm256_loadu_si256((const __m256i *)vecC[1 + LOB + b]));
    }
    int divides[33]; for (int n = 0; n <= 32; n++) divides[n] = (n >= 1 && M % n == 0);

    acc_t *tot = calloc(1, sizeof(acc_t));
    for (int m = 0; m < 128; m++) for (int n = 0; n < 33; n++) { tot->repmin[m][n] = 0xffffffffu; tot->rephv[m][n] = 0xffffffffu; }
    const __m256i zero = _mm256_setzero_si256();

#pragma omp parallel
    {
        acc_t *acc = calloc(1, sizeof(acc_t));
        for (int m = 0; m < 128; m++) for (int n = 0; n < 33; n++) { acc->repmin[m][n] = 0xffffffffu; acc->rephv[m][n] = 0xffffffffu; }
#pragma omp for schedule(dynamic, 16)
        for (uint32_t hi = 0; hi < (uint32_t)nhi; hi++) {
            __m256i hr = THR[hi], hc = THC[hi];
            uint32_t hbits = hi << (LOB + 1);
            int hpc = __builtin_popcount(hi);
            for (uint32_t lo = 0; lo < (uint32_t)nlo; lo++) {
                __m256i r = _mm256_add_epi8(hr, TLR[lo]);
                __m256i c = _mm256_add_epi8(hc, TLC[lo]);
                uint32_t nzr = ~(uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(r, zero));
                uint32_t nzc = ~(uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(c, zero));
                int mr = segmask(nzr), mc = segmask(nzc);
                uint32_t A = hbits | (lo << 1) | 1u;
                int n = hpc + lopc[lo] + 1;
                acc->hist[mr][n]++;
                acc->cnt[C_TOTAL]++;
                if (mr != mc) fail(acc, C_MISMATCH, A);
                if (A < acc->repmin[mr][n]) acc->repmin[mr][n] = A;
                if (A > acc->repmax[mr][n]) acc->repmax[mr][n] = A;
                uint32_t hv = (A * 2654435761u) ^ (A >> 15);
                if (hv < acc->rephv[mr][n]) { acc->rephv[mr][n] = hv; acc->rephash[mr][n] = A; }
                if (divides[n] && cover(A, A)) acc->tile[mr][n]++;
                if (mr) slow(A, mr, n, acc);
                else if ((hv & 63u) == 0) slow(A, mr, n, acc);   // 1/64 sample of pattern-free sets, for the converse of L4(a)
            }
        }
#pragma omp critical
        {
            for (int m = 0; m < 128; m++) for (int n = 0; n < 33; n++) {
                tot->hist[m][n] += acc->hist[m][n]; tot->tile[m][n] += acc->tile[m][n];
                if (acc->repmin[m][n] < tot->repmin[m][n]) tot->repmin[m][n] = acc->repmin[m][n];
                if (acc->repmax[m][n] > tot->repmax[m][n]) tot->repmax[m][n] = acc->repmax[m][n];
                if (acc->rephv[m][n] < tot->rephv[m][n]) { tot->rephv[m][n] = acc->rephv[m][n]; tot->rephash[m][n] = acc->rephash[m][n]; }
            }
            for (int k = 0; k < NCNT; k++) { if (acc->cnt[k] && !tot->cnt[k]) tot->firstfail[k] = acc->firstfail[k]; tot->cnt[k] += acc->cnt[k]; }
            for (int k = 0; k < 3; k++) { tot->l4b_prem_role[k] += acc->l4b_prem_role[k]; tot->l3_prem_pair[k] += acc->l3_prem_pair[k]; tot->l5_prem_pair[k] += acc->l5_prem_pair[k]; }
            for (int k = 0; k < 6; k++) tot->s5xy_prem_role[k] += acc->s5xy_prem_role[k];
        }
        free(acc);
    }

    char fn[512];
    snprintf(fn, sizeof fn, "%s_hist.txt", argv[4]);
    FILE *f = fopen(fn, "w");
    fprintf(f, "# mask n count tilecount repmin repmax rephash   (M=%d, primes %d %d %d; subsets containing 0)\n", M, p[0], p[1], p[2]);
    for (int m = 0; m < 128; m++) for (int n = 0; n <= M; n++) if (tot->hist[m][n])
        fprintf(f, "%d %d %llu %llu %u %u %u\n", m, n, (unsigned long long)tot->hist[m][n], (unsigned long long)tot->tile[m][n],
                tot->repmin[m][n], tot->repmax[m][n], tot->rephash[m][n]);
    fclose(f);
    snprintf(fn, sizeof fn, "%s_counters.txt", argv[4]);
    f = fopen(fn, "w");
    for (int k = 0; k < NCNT; k++) {
        fprintf(f, "%-24s %llu", CNAME[k], (unsigned long long)tot->cnt[k]);
        if (strstr(CNAME[k], "FAIL") || strstr(CNAME[k], "MISMATCH")) { if (tot->cnt[k]) fprintf(f, "   first: %u", tot->firstfail[k]); }
        fprintf(f, "\n");
    }
    fprintf(f, "L4B premise by slicing coordinate z (p0,p1,p2): %llu %llu %llu\n",
            (unsigned long long)tot->l4b_prem_role[0], (unsigned long long)tot->l4b_prem_role[1], (unsigned long long)tot->l4b_prem_role[2]);
    fprintf(f, "L3 premise by pair (01,02,12): %llu %llu %llu\n",
            (unsigned long long)tot->l3_prem_pair[0], (unsigned long long)tot->l3_prem_pair[1], (unsigned long long)tot->l3_prem_pair[2]);
    fprintf(f, "L5 premise by pair (01,02,12): %llu %llu %llu\n",
            (unsigned long long)tot->l5_prem_pair[0], (unsigned long long)tot->l5_prem_pair[1], (unsigned long long)tot->l5_prem_pair[2]);
    fprintf(f, "S5XY premise by role (x,y,z)=(012,021,102,120,201,210): %llu %llu %llu %llu %llu %llu\n",
            (unsigned long long)tot->s5xy_prem_role[0], (unsigned long long)tot->s5xy_prem_role[1], (unsigned long long)tot->s5xy_prem_role[2],
            (unsigned long long)tot->s5xy_prem_role[3], (unsigned long long)tot->s5xy_prem_role[4], (unsigned long long)tot->s5xy_prem_role[5]);
    fclose(f);
    printf("done: %llu subsets\n", (unsigned long long)tot->cnt[C_TOTAL]);
    return 0;
}
