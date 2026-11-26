/* Every multiset on Z_M with at most S elements whose mask polynomial is divisible by Phi_d for every d in a
 * target set P, found without listing the others.
 *
 * G = product of Phi_d over d in P (monic, degree D; the Phi_d are pairwise coprime, so G | A iff every
 * Phi_d, d in P, divides A).  Write A = A_low + A_high, A_low the part with exponents < D, A_high the part
 * with exponents D..M-1.  Then G | A iff A_low = -(A_high mod G), because deg A_low < D.  So: list every
 * multiset A_high on the exponents D..M-1 with at most S elements, take A_low = -(A_high mod G), and keep the
 * result when all coefficients of A_low are >= 0 and the whole has at most S elements (and at least one).
 * Each kept multiset gets its full pattern from the remainders modulo every Phi_d, d | M, d > 1, as in enumA.
 *
 * HMAX bounds the number of elements of A_high.  With HMAX = S nothing is left out.  With a smaller HMAX the
 * list is of those multisets (of at most S elements, G | A) that have at most HMAX elements at the exponents
 * D..M-1; the driver uses HMAX = floor(S (M-D) / M), which loses no pattern at any size <= S, because some
 * translate of a multiset of s elements has at least s D / M of them in a window of D consecutive residues,
 * and a translate has the same pattern.
 *
 * usage: enumB grouptable targettable S HMAX worker nworkers out
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXM 64
#define MAXL 64
#define MAXD 16
#define MAXS 80

static int M, ND, L, S, D, HMAX;
static int dval[MAXD], dphi[MAXD], doff[MAXD];
static int16_t col[MAXM][MAXL] __attribute__((aligned(64)));
static int16_t g[MAXM][MAXL] __attribute__((aligned(64)));
static int16_t rr[MAXS + 1][MAXL] __attribute__((aligned(64)));
static int16_t vv[MAXS + 1][MAXL] __attribute__((aligned(64)));
static int cur[MAXS + 1];

static uint64_t *cnt;      /* cnt[mask*(S+1)+size] */
static int *best;          /* best[mask] */
static int *wit;           /* wit[mask*MAXM + a] = multiplicity of a */
static int NM;
static uint64_t nodes = 0;

static inline int mask_of(const int32_t *r) {
    int m = 0;
    for (int i = 0; i < ND; i++) {
        int32_t z = 0;
        const int32_t *b = r + doff[i];
        for (int j = 0; j < dphi[i]; j++) z |= b[j];
        if (z == 0) m |= 1 << i;
    }
    return m;
}

static inline void visit(int depth) {
    nodes++;
    const int16_t *v = vv[depth];
    int tot = depth;
    int16_t pos = 0;
    for (int j = 0; j < D; j++) pos |= (v[j] > 0);
    if (pos) return;
    for (int j = 0; j < D; j++) tot -= v[j];
    if (tot < 1 || tot > S) return;
    int32_t full[MAXL];
    for (int j = 0; j < L; j++) full[j] = rr[depth][j];
    for (int a = 0; a < D; a++) if (v[a]) {
        int c = -v[a];
        for (int j = 0; j < L; j++) full[j] += c * col[a][j];
    }
    int m = mask_of(full);
    cnt[(size_t)m * (S + 1) + tot]++;
    if (tot < best[m]) {
        best[m] = tot;
        int *w = wit + (size_t)m * MAXM;
        for (int a = 0; a < M; a++) w[a] = 0;
        for (int a = 0; a < D; a++) w[a] = -v[a];
        for (int i = 0; i < depth; i++) w[cur[i]]++;
    }
}

static void rec(int depth, int last) {
    if (depth == HMAX) return;
    const int16_t *r = rr[depth], *v = vv[depth];
    int16_t *r2 = rr[depth + 1], *v2 = vv[depth + 1];
    for (int a = last; a < M; a++) {
        const int16_t *c = col[a], *gg = g[a];
        for (int j = 0; j < L; j++) r2[j] = r[j] + c[j];
        for (int j = 0; j < D; j++) v2[j] = v[j] + gg[j];
        cur[depth] = a;
        visit(depth + 1);
        rec(depth + 1, a);
    }
}

static double binom(int n, int k) {
    if (k < 0 || k > n) return 0;
    double r = 1;
    for (int i = 1; i <= k; i++) r = r * (n - k + i) / i;
    return r;
}

typedef struct { int a[3]; double size; int w; } Pref;
static int cmp_pref(const void *x, const void *y) {
    double a = ((const Pref *)x)->size, b = ((const Pref *)y)->size;
    return (a < b) - (a > b);
}

int main(int argc, char **argv) {
    if (argc != 8) { fprintf(stderr, "usage: enumB grouptable targettable S HMAX worker nworkers out\n"); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("table"); return 2; }
    S = atoi(argv[3]);
    HMAX = atoi(argv[4]);
    if (HMAX > S) HMAX = S;
    int worker = atoi(argv[5]), nworkers = atoi(argv[6]);
    if (fscanf(f, "%d %d", &M, &ND) != 2) return 2;
    if (M > MAXM || ND > MAXD || S > MAXS) { fprintf(stderr, "too large\n"); return 2; }
    L = 0;
    for (int i = 0; i < ND; i++) {
        if (fscanf(f, "%d %d", &dval[i], &dphi[i]) != 2) return 2;
        doff[i] = L;
        for (int a = 0; a < M; a++)
            for (int j = 0; j < dphi[i]; j++) {
                int v;
                if (fscanf(f, "%d", &v) != 1) return 2;
                col[a][L + j] = (int16_t)v;
            }
        L += dphi[i];
    }
    fclose(f);
    if (L != M - 1 || L > MAXL) { fprintf(stderr, "bad table\n"); return 2; }
    f = fopen(argv[2], "r");
    if (!f) { perror("target"); return 2; }
    if (fscanf(f, "%d", &D) != 1) return 2;
    if (D > MAXL || D >= M + 1) { fprintf(stderr, "bad target\n"); return 2; }
    for (int a = 0; a < M; a++)
        for (int j = 0; j < D; j++) {
            int v;
            if (fscanf(f, "%d", &v) != 1) return 2;
            g[a][j] = (int16_t)v;
        }
    fclose(f);
    /* the exponents below D must be their own remainders */
    for (int a = 0; a < D; a++)
        for (int j = 0; j < D; j++)
            if (g[a][j] != (a == j)) { fprintf(stderr, "target table: X^a mod G is not X^a for a < D\n"); return 2; }

    NM = 1 << ND;
    cnt = calloc((size_t)NM * (S + 1), sizeof(uint64_t));
    best = malloc(NM * sizeof(int));
    wit = calloc((size_t)NM * MAXM, sizeof(int));
    for (int m = 0; m < NM; m++) best[m] = 1 << 30;
    memset(rr, 0, sizeof(rr));
    memset(vv, 0, sizeof(vv));

    int R = M - D;              /* number of free exponents D..M-1 */
    int PL = (HMAX >= 3 && R >= 1) ? 3 : 0;
    if (PL == 0) {
        if (worker == 0) { visit(0); rec(0, D); }
    } else {
        int np = 0, cap = 1 << 16;
        Pref *pf = malloc(cap * sizeof(Pref));
        for (int a = D; a < M; a++) for (int b = a; b < M; b++) for (int c = b; c < M; c++) {
            if (np == cap) { cap *= 2; pf = realloc(pf, cap * sizeof(Pref)); }
            pf[np].a[0] = a; pf[np].a[1] = b; pf[np].a[2] = c;
            pf[np].size = binom(M - c + HMAX - 3, HMAX - 3);
            np++;
        }
        qsort(pf, np, sizeof(Pref), cmp_pref);
        double *load = calloc(nworkers, sizeof(double));
        for (int i = 0; i < np; i++) {
            int bw = 0;
            for (int w = 1; w < nworkers; w++) if (load[w] < load[bw]) bw = w;
            pf[i].w = bw; load[bw] += pf[i].size;
        }
        free(load);
        if (worker == 0) {
            visit(0);
            for (int a = D; a < M; a++) {
                for (int j = 0; j < L; j++) rr[1][j] = col[a][j];
                for (int j = 0; j < D; j++) vv[1][j] = g[a][j];
                cur[0] = a; visit(1);
                for (int b = a; b < M; b++) {
                    for (int j = 0; j < L; j++) rr[2][j] = rr[1][j] + col[b][j];
                    for (int j = 0; j < D; j++) vv[2][j] = vv[1][j] + g[b][j];
                    cur[1] = b; visit(2);
                }
            }
        }
        for (int i = 0; i < np; i++) if (pf[i].w == worker) {
            int a = pf[i].a[0], b = pf[i].a[1], c = pf[i].a[2];
            for (int j = 0; j < L; j++) rr[3][j] = col[a][j] + col[b][j] + col[c][j];
            for (int j = 0; j < D; j++) vv[3][j] = g[a][j] + g[b][j] + g[c][j];
            cur[0] = a; cur[1] = b; cur[2] = c;
            visit(3);
            rec(3, c);
        }
    }
    FILE *o = fopen(argv[7], "w");
    if (!o) { perror("out"); return 2; }
    fprintf(o, "M %d S %d HMAX %d ND %d D %d worker %d of %d nodes %llu\n", M, S, HMAX, ND, D, worker, nworkers,
            (unsigned long long)nodes);
    for (int m = 0; m < NM; m++) {
        int any = 0;
        for (int s = 0; s <= S; s++) if (cnt[(size_t)m * (S + 1) + s]) any = 1;
        if (!any) continue;
        fprintf(o, "mask %d best %d wit", m, best[m]);
        for (int a = 0; a < M; a++) fprintf(o, " %d", wit[(size_t)m * MAXM + a]);
        fprintf(o, " counts");
        for (int s = 0; s <= S; s++) fprintf(o, " %llu", (unsigned long long)cnt[(size_t)m * (S + 1) + s]);
        fprintf(o, "\n");
    }
    fclose(o);
    return 0;
}
