// mitm.c -- referee's independent exact count, by meet in the middle, of the subsets A of Z_M (ALL subsets,
// not only those containing 0), M = p0*p1*p2 <= 42, by (pattern Z_A, size).
//
// For each S subset of the seven divisors d > 1 of M, count_S[n] = #{A : |A| = n, Phi_d | A for all d in S}
// is obtained by splitting Z_M in two halves, computing A(X) mod Phi_d exactly for both halves, sorting, and
// joining on (residue of low half) = -(residue of high half) on the segments of S.  The exact pattern counts
// follow by Moebius inversion over S.  Keys are compared exactly (no hashing).
//
// Optionally, for patterns S given on the command line, the join is enumerated explicitly and the structural
// checks of the note (Lemma 3, Lemma 4, (I6), the internal steps of Section 5) are run on every set with
// Z_A containing S.
//
// mask bits: 0,1,2 : p0,p1,p2 ;  3: p0p1, 4: p0p2, 5: p1p2 ;  6: M.
// build: gcc -O2 -fopenmp -o mitm mitm.c
// run:   ./mitm 2 3 7 out_prefix [S1 S2 ...]

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>

typedef uint64_t set_t;
static int p[3], M;
static int cx[64][3];
static int segoff[7], seglen[7], divd[7];
static int PAIRBIT[3][3];
#define KL 48
static int8_t vecR[64][KL];

#define PL 100
static int cyc_cache_deg[64];
static int cyc_cache[64][PL];
static int cyc_have[64];
static void cyclo(int n, int *out, int *deg) {
    if (cyc_have[n]) { memcpy(out, cyc_cache[n], sizeof(int) * PL); *deg = cyc_cache_deg[n]; return; }
    int num[PL]; memset(num, 0, sizeof num);
    num[n] = 1; num[0] = -1; int nd = n;
    for (int e = 1; e < n; e++) if (n % e == 0) {
        int q[PL], qd; cyclo(e, q, &qd);
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

static void build_vectors(void) {
    divd[0] = p[0]; divd[1] = p[1]; divd[2] = p[2];
    divd[3] = p[0] * p[1]; divd[4] = p[0] * p[2]; divd[5] = p[1] * p[2]; divd[6] = M;
    int off = 0;
    memset(vecR, 0, sizeof vecR);
    for (int s = 0; s < 7; s++) {
        int phi[PL], deg; cyclo(divd[s], phi, &deg);
        segoff[s] = off; seglen[s] = deg;
        int cur[PL]; memset(cur, 0, sizeof cur); cur[0] = 1;
        for (int e = 0; e < M; e++) {
            for (int k = 0; k < deg; k++) {
                if (cur[k] < -3 || cur[k] > 3) { fprintf(stderr, "coefficient too large\n"); exit(1); }
                vecR[e][off + k] = (int8_t)cur[k];
            }
            for (int k = deg; k >= 1; k--) cur[k] = cur[k - 1];
            cur[0] = 0;
            int c = cur[deg];
            if (c) for (int k = 0; k <= deg; k++) cur[k] -= c * phi[k];
        }
        off += deg;
    }
    if (off != M - 1 || off > KL) { fprintf(stderr, "layout error %d\n", off); exit(1); }
    for (int k = 0; k < KL; k++) {
        int sr = 0;
        for (int e = 0; e < M; e++) sr += abs(vecR[e][k]);
        if (sr > 127) { fprintf(stderr, "int8 overflow possible\n"); exit(1); }
    }
}

// ------------------------------------------------------------------ structural checks (as in enum.c)
enum {
    C_TOTAL,
    C_I4_PREM, C_I4_FAIL,
    C_L3_PREM, C_L3_FAIL, C_L3_A0POS, C_L3_A0POS_FAIL,
    C_L4A_PREM, C_L4A_FAIL, C_L4A_CONV_PREM, C_L4A_CONV_FAIL,
    C_L4B_PREM_P, C_L4B_PREM_EMPTY, C_L4B_PREM_BOTH, C_L4B_FAIL_T, C_L4B_FAIL_LINES,
    C_L4B_NOPREM, C_L4B_NOPREM_TNONZERO,
    C_I6_PREM, C_I6_FAIL,
    C_S5XY_PREM, C_S5XY_FAIL,
    C_S5ALL_PREM, C_S5ALL_A0POS, C_S5ALL_A0POS_FAIL, C_S5ALL_A0ZERO, C_S5ALL_A0ZERO_FAIL,
    C_L5_PREM, C_L5_FAIL,
    NCNT
};
static const char *CNAME[NCNT] = {
    "TOTAL",
    "I4_PREM", "I4_FAIL",
    "L3_PREM", "L3_FAIL", "L3_A0POS", "L3_A0POS_FAIL",
    "L4A_PREM", "L4A_FAIL", "L4A_CONV_PREM", "L4A_CONV_FAIL",
    "L4B_PREM_P", "L4B_PREM_EMPTY", "L4B_PREM_BOTH", "L4B_FAIL_T", "L4B_FAIL_LINES",
    "L4B_NOPREM", "L4B_NOPREM_TNONZERO",
    "I6_PREM", "I6_FAIL",
    "S5XY_PREM", "S5XY_FAIL",
    "S5ALL_PREM", "S5ALL_A0POS", "S5ALL_A0POS_FAIL", "S5ALL_A0ZERO", "S5ALL_A0ZERO_FAIL",
    "L5_PREM", "L5_FAIL",
};
typedef struct {
    uint64_t cnt[NCNT];
    uint64_t l4b_prem_role[3], s5xy_prem_role[6], l3_prem_pair[3];
    set_t firstfail[NCNT];
    set_t example_s5xy[6], example_s5all;
    int have_s5xy[6], have_s5all;
} acc_t;
static inline void fail(acc_t *acc, int c, set_t A) { if (!acc->cnt[c]) acc->firstfail[c] = A; acc->cnt[c]++; }

static void getN(set_t A, int x, int y, int N[8][8]) {
    for (int i = 0; i < p[x]; i++) for (int j = 0; j < p[y]; j++) N[i][j] = 0;
    set_t rem = A;
    while (rem) { int e = __builtin_ctzll(rem); rem &= rem - 1; N[cx[e][x]][cx[e][y]]++; }
}
static int normal(int N[8][8], int px, int py, int *a0, int al[8], int be[8], int *Sa, int *Sb) {
    int mn = 1 << 30;
    for (int i = 0; i < px; i++) for (int j = 0; j < py; j++) if (N[i][j] < mn) mn = N[i][j];
    *a0 = mn; *Sa = 0; *Sb = 0;
    for (int i = 0; i < px; i++) { int m = 1 << 30; for (int j = 0; j < py; j++) if (N[i][j] < m) m = N[i][j]; al[i] = m - mn; *Sa += al[i]; }
    for (int j = 0; j < py; j++) { int m = 1 << 30; for (int i = 0; i < px; i++) if (N[i][j] < m) m = N[i][j]; be[j] = m - mn; *Sb += be[j]; }
    for (int i = 0; i < px; i++) for (int j = 0; j < py; j++) if (N[i][j] != mn + al[i] + be[j]) return 0;
    return 1;
}

static void slow(set_t A, int mask, int n, acc_t *acc) {
    int E[3] = { mask & 1, (mask >> 1) & 1, (mask >> 2) & 1 };
    int t = (mask >> 6) & 1;
    int nE = E[0] + E[1] + E[2];
    int nP = ((mask >> 3) & 1) + ((mask >> 4) & 1) + ((mask >> 5) & 1);
#define INP(x, y) ((mask >> PAIRBIT[x][y]) & 1)
    acc->cnt[C_TOTAL]++;
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
    if (t) for (int x = 0; x < 3; x++) for (int y = x + 1; y < 3; y++) if (E[x] && E[y] && n == p[x] * p[y]) {
        acc->cnt[C_L5_PREM]++;
        if (!INP(x, y)) fail(acc, C_L5_FAIL, A);
    }
    {
        static const int perm[6][3] = { {0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0} };
        for (int r = 0; r < 6; r++) {
            int x = perm[r][0], y = perm[r][1], z = perm[r][2];
            if (!(E[x] && !E[y] && !E[z] && INP(y, z) && INP(x, y))) continue;
            acc->cnt[C_S5XY_PREM]++; acc->s5xy_prem_role[r]++;
            if (!acc->have_s5xy[r]) { acc->have_s5xy[r] = 1; acc->example_s5xy[r] = A; }
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
    if (nE == 0 && nP == 3) {
        acc->cnt[C_S5ALL_PREM]++;
        if (!acc->have_s5all) { acc->have_s5all = 1; acc->example_s5all = A; }
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
    for (int z = 0; z < 3; z++) {
        int x = (z == 0) ? 1 : 0, y = (z == 2) ? 1 : 2;
        int px = p[x], py = p[y], pz = p[z];
        int sl[8][8][8]; memset(sl, 0, sizeof sl);
        set_t rem = A;
        while (rem) { int e = __builtin_ctzll(rem); rem &= rem - 1; sl[cx[e][z]][cx[e][x]][cx[e][y]] = 1; }
        int T[8][8][8]; int allequal = 1, anyempty = 0, Tzero = 1, alllines = 1;
        for (int c = 0; c < pz; c++) {
            int R[8] = {0}, C[8] = {0}, S = 0;
            for (int i = 0; i < px; i++) for (int j = 0; j < py; j++) { R[i] += sl[c][i][j]; C[j] += sl[c][i][j]; S += sl[c][i][j]; }
            if (S == 0) anyempty = 1;
            int additive = 1;
            for (int i = 0; i < px; i++) for (int j = 0; j < py; j++) {
                T[c][i][j] = px * py * sl[c][i][j] - px * R[i] - py * C[j] + S;
                if (T[c][i][j] != T[0][i][j]) allequal = 0;
                if (T[c][i][j]) { Tzero = 0; additive = 0; }
            }
            int depj = 1, depi = 1;
            for (int i = 0; i < px; i++) for (int j = 0; j < py; j++) {
                if (sl[c][i][j] != sl[c][0][j]) depj = 0;
                if (sl[c][i][j] != sl[c][i][0]) depi = 0;
            }
            if (!(depj || depi)) alllines = 0;
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
                if (!Tzero) acc->cnt[C_L4B_NOPREM_TNONZERO]++;
            }
        } else {
            acc->cnt[C_L4A_CONV_PREM]++;
            if (allequal) fail(acc, C_L4A_CONV_FAIL, A);
        }
    }
#undef INP
}

// ------------------------------------------------------------------ meet in the middle
typedef struct { uint8_t key[KL]; uint32_t idx; uint32_t pc; } rec_t;
static int cmprec(const void *a, const void *b) {
    int c = memcmp(((const rec_t *)a)->key, ((const rec_t *)b)->key, KL);
    if (c) return c;
    return (int)((const rec_t *)a)->pc - (int)((const rec_t *)b)->pc;
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: mitm p0 p1 p2 outprefix [S ...]\n"); return 1; }
    p[0] = atoi(argv[1]); p[1] = atoi(argv[2]); p[2] = atoi(argv[3]);
    M = p[0] * p[1] * p[2];
    if (M > 42 || p[0] > 7 || p[1] > 7 || p[2] > 7) { fprintf(stderr, "M too large\n"); return 1; }
    for (int e = 0; e < M; e++) for (int w = 0; w < 3; w++) cx[e][w] = e % p[w];
    PAIRBIT[0][1] = PAIRBIT[1][0] = 3; PAIRBIT[0][2] = PAIRBIT[2][0] = 4; PAIRBIT[1][2] = PAIRBIT[2][1] = 5;
    build_vectors();
    int h1 = M / 2, h2 = M - h1;
    size_t n1 = (size_t)1 << h1, n2 = (size_t)1 << h2;
    int8_t (*R1)[KL] = malloc(n1 * KL), (*R2)[KL] = malloc(n2 * KL);
    memset(R1[0], 0, KL); memset(R2[0], 0, KL);
    for (size_t s = 1; s < n1; s++) { int b = __builtin_ctzl(s); size_t r = s & (s - 1); for (int k = 0; k < KL; k++) R1[s][k] = R1[r][k] + vecR[b][k]; }
    for (size_t s = 1; s < n2; s++) { int b = __builtin_ctzl(s); size_t r = s & (s - 1); for (int k = 0; k < KL; k++) R2[s][k] = R2[r][k] + vecR[h1 + b][k]; }

    static uint64_t cntS[128][64];
    memset(cntS, 0, sizeof cntS);
    int nenum = argc - 5; int enumS[128];
    for (int i = 0; i < nenum; i++) enumS[i] = atoi(argv[5 + i]);
    acc_t *accs = calloc(nenum > 0 ? nenum : 1, sizeof(acc_t));
    uint64_t enumcount[128]; memset(enumcount, 0, sizeof enumcount);

    // job list: 128 counting jobs (S = 0 done directly), plus enumeration is done inside the job for S when asked
#pragma omp parallel
    {
        rec_t *a = malloc(n1 * sizeof(rec_t)), *b = malloc(n2 * sizeof(rec_t));
#pragma omp for schedule(dynamic, 1)
        for (int S = 127; S >= 1; S--) {
            int en = -1; for (int i = 0; i < nenum; i++) if (enumS[i] == S) en = i;
            uint8_t sel[KL]; memset(sel, 0, KL);
            for (int s = 0; s < 7; s++) if (S >> s & 1) for (int k = 0; k < seglen[s]; k++) sel[segoff[s] + k] = 1;
            for (size_t i = 0; i < n1; i++) {
                for (int k = 0; k < KL; k++) a[i].key[k] = sel[k] ? (uint8_t)(R1[i][k]) : 0;
                a[i].idx = (uint32_t)i; a[i].pc = __builtin_popcountl(i);
            }
            for (size_t i = 0; i < n2; i++) {
                for (int k = 0; k < KL; k++) b[i].key[k] = sel[k] ? (uint8_t)(-R2[i][k]) : 0;
                b[i].idx = (uint32_t)i; b[i].pc = __builtin_popcountl(i);
            }
            qsort(a, n1, sizeof(rec_t), cmprec); qsort(b, n2, sizeof(rec_t), cmprec);
            uint64_t loc[64]; memset(loc, 0, sizeof loc);
            size_t i = 0, j = 0;
            while (i < n1 && j < n2) {
                int c = memcmp(a[i].key, b[j].key, KL);
                if (c < 0) { i++; continue; }
                if (c > 0) { j++; continue; }
                size_t i2 = i, j2 = j;
                uint64_t hl[32] = {0}, hh[32] = {0};
                while (i2 < n1 && memcmp(a[i2].key, a[i].key, KL) == 0) { hl[a[i2].pc]++; i2++; }
                while (j2 < n2 && memcmp(b[j2].key, b[j].key, KL) == 0) { hh[b[j2].pc]++; j2++; }
                for (int u = 0; u <= h1; u++) if (hl[u]) for (int v = 0; v <= h2; v++) if (hh[v]) loc[u + v] += hl[u] * hh[v];
                if (en >= 0) {
                    for (size_t ii = i; ii < i2; ii++) for (size_t jj = j; jj < j2; jj++) {
                        set_t A = (set_t)a[ii].idx | ((set_t)b[jj].idx << h1);
                        if (!A) continue;
                        // exact pattern from the full residues
                        int mask = 0;
                        for (int s = 0; s < 7; s++) {
                            int z = 1;
                            for (int k = 0; k < seglen[s]; k++) if ((int8_t)(R1[a[ii].idx][segoff[s] + k] + R2[b[jj].idx][segoff[s] + k])) { z = 0; break; }
                            mask |= z << s;
                        }
                        if ((mask & S) != S) { fprintf(stderr, "join inconsistency\n"); exit(1); }
                        slow(A, mask, (int)(a[ii].pc + b[jj].pc), &accs[en]);
                        enumcount[en]++;
                    }
                }
                i = i2; j = j2;
            }
            memcpy(cntS[S], loc, sizeof loc);
        }
        free(a); free(b);
    }
    // S = 0: binomials
    {
        static uint64_t C[64][64];
        for (int n = 0; n <= M; n++) { C[n][0] = 1; for (int k = 1; k <= n; k++) C[n][k] = C[n - 1][k - 1] + (k <= n - 1 ? C[n - 1][k] : 0); }
        for (int n = 0; n <= M; n++) cntS[0][n] = C[M][n];
    }
    // Moebius inversion: exact[mask] = sum_{S superset of mask} (-1)^{|S - mask|} cntS[S]
    char fn[512];
    snprintf(fn, sizeof fn, "%s_hist.txt", argv[4]);
    FILE *f = fopen(fn, "w");
    fprintf(f, "# mask n count   (M=%d, primes %d %d %d; ALL subsets, by meet in the middle)\n", M, p[0], p[1], p[2]);
    for (int mask = 0; mask < 128; mask++) for (int n = 1; n <= M; n++) {
        __int128 v = 0;
        for (int S = 0; S < 128; S++) if ((S & mask) == mask) {
            int sg = __builtin_popcount(S ^ mask) & 1;
            if (sg) v -= cntS[S][n]; else v += cntS[S][n];
        }
        if (v < 0) { fprintf(stderr, "negative count: mask %d n %d\n", mask, n); return 1; }
        if (v > 0) fprintf(f, "%d %d %llu\n", mask, n, (unsigned long long)v);
    }
    fclose(f);
    snprintf(fn, sizeof fn, "%s_super.txt", argv[4]);
    f = fopen(fn, "w");
    fprintf(f, "# S total(count of nonempty-or-empty sets with Z_A superset of S)\n");
    for (int S = 0; S < 128; S++) { unsigned long long tt = 0; for (int n = 0; n <= M; n++) tt += cntS[S][n]; fprintf(f, "%d %llu\n", S, tt); }
    fclose(f);
    for (int i = 0; i < nenum; i++) {
        snprintf(fn, sizeof fn, "%s_enum_S%d.txt", argv[4], enumS[i]);
        f = fopen(fn, "w");
        fprintf(f, "enumerated sets with Z_A superset of S=%d: %llu\n", enumS[i], (unsigned long long)enumcount[i]);
        for (int k = 0; k < NCNT; k++) {
            fprintf(f, "%-24s %llu", CNAME[k], (unsigned long long)accs[i].cnt[k]);
            if (strstr(CNAME[k], "FAIL") && accs[i].cnt[k]) fprintf(f, "   first: %llu", (unsigned long long)accs[i].firstfail[k]);
            fprintf(f, "\n");
        }
        fprintf(f, "L4B premise by slicing coordinate z (p0,p1,p2): %llu %llu %llu\n",
                (unsigned long long)accs[i].l4b_prem_role[0], (unsigned long long)accs[i].l4b_prem_role[1], (unsigned long long)accs[i].l4b_prem_role[2]);
        fprintf(f, "L3 premise by pair (01,02,12): %llu %llu %llu\n",
                (unsigned long long)accs[i].l3_prem_pair[0], (unsigned long long)accs[i].l3_prem_pair[1], (unsigned long long)accs[i].l3_prem_pair[2]);
        fprintf(f, "S5XY premise by role (x,y,z)=(012,021,102,120,201,210): %llu %llu %llu %llu %llu %llu\n",
                (unsigned long long)accs[i].s5xy_prem_role[0], (unsigned long long)accs[i].s5xy_prem_role[1], (unsigned long long)accs[i].s5xy_prem_role[2],
                (unsigned long long)accs[i].s5xy_prem_role[3], (unsigned long long)accs[i].s5xy_prem_role[4], (unsigned long long)accs[i].s5xy_prem_role[5]);
        for (int r = 0; r < 6; r++) if (accs[i].have_s5xy[r]) fprintf(f, "example S5XY role %d: %llu\n", r, (unsigned long long)accs[i].example_s5xy[r]);
        if (accs[i].have_s5all) fprintf(f, "example S5ALL: %llu\n", (unsigned long long)accs[i].example_s5all);
        fclose(f);
    }
    printf("done\n");
    return 0;
}
