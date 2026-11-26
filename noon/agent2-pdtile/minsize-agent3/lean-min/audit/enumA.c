/* Plain enumeration of every multiset on Z_M with at most S elements (no symmetry is used).
 *
 * A multiset is a nondecreasing sequence a_1 <= ... <= a_s of residues; the search tree has one node for each
 * multiset of size 0..S.  At each node the remainder of A(X) = sum X^{a_i} on division by Phi_d is kept for
 * every d | M, d > 1 (it is the sum of the remainders of the X^{a_i}, which were found by long division in
 * tables.py; division by a monic polynomial is linear).  The pattern is the set of d whose remainder is 0.
 *
 * Output (one file per worker): for each pattern mask reached, the number of multisets of each size with
 * exactly that pattern, and the first multiset of least size found.
 *
 * usage: enumA table S worker nworkers out
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXM 64
#define MAXL 64
#define MAXD 16
#define MAXS 64

static int M, ND, L, S;
static int dval[MAXD], dphi[MAXD], doff[MAXD];
static int16_t col[MAXM][MAXL] __attribute__((aligned(64)));
static int16_t rr[MAXS + 1][MAXL] __attribute__((aligned(64)));
static int cur[MAXS + 1];

static uint64_t *cnt;      /* cnt[mask*(S+1)+size] */
static int *best;          /* best[mask] */
static int *wit;           /* wit[mask*MAXS + i] */
static int NM;

static inline int mask_of(const int16_t *r) {
    int m = 0;
    for (int i = 0; i < ND; i++) {
        int z = 0;
        const int16_t *b = r + doff[i];
        for (int j = 0; j < dphi[i]; j++) z |= b[j];
        if (z == 0) m |= 1 << i;
    }
    return m;
}

static inline void record(int depth) {
    int m = mask_of(rr[depth]);
    cnt[(size_t)m * (S + 1) + depth]++;
    if (depth < best[m]) {
        best[m] = depth;
        for (int i = 0; i < depth; i++) wit[m * MAXS + i] = cur[i];
    }
}

static void rec(int depth, int last) {
    /* the node (multiset of size depth, elements cur[0..depth-1], remainder rr[depth]) is already recorded */
    if (depth == S) return;
    const int16_t *r = rr[depth];
    int16_t *r2 = rr[depth + 1];
    for (int a = last; a < M; a++) {
        const int16_t *c = col[a];
        for (int j = 0; j < L; j++) r2[j] = r[j] + c[j];
        cur[depth] = a;
        record(depth + 1);
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
    if (argc != 6) { fprintf(stderr, "usage: enumA table S worker nworkers out\n"); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("table"); return 2; }
    S = atoi(argv[2]);
    int worker = atoi(argv[3]), nworkers = atoi(argv[4]);
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
    NM = 1 << ND;
    cnt = calloc((size_t)NM * (S + 1), sizeof(uint64_t));
    best = malloc(NM * sizeof(int));
    wit = calloc((size_t)NM * MAXS, sizeof(int));
    for (int m = 0; m < NM; m++) best[m] = 1 << 30;
    memset(rr, 0, sizeof(rr));

    int PL = S < 3 ? S : 3;     /* prefix length used to share the work */
    /* nodes of depth < PL are recorded by worker 0; the subtree under each prefix of length PL by one worker */
    /* list the prefixes */
    int np = 0, cap = 1 << 16;
    Pref *pf = malloc(cap * sizeof(Pref));
    if (PL == 3) {
        for (int a = 0; a < M; a++) for (int b = a; b < M; b++) for (int c = b; c < M; c++) {
            if (np == cap) { cap *= 2; pf = realloc(pf, cap * sizeof(Pref)); }
            pf[np].a[0] = a; pf[np].a[1] = b; pf[np].a[2] = c;
            pf[np].size = binom(M - c + S - 3, S - 3);
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
    }
    if (PL < 3) {
        /* tiny case: worker 0 does everything */
        if (worker == 0) { record(0); rec(0, 0); }
    } else {
        if (worker == 0) {
            /* depths 0, 1, 2 */
            record(0);
            for (int a = 0; a < M; a++) {
                for (int j = 0; j < L; j++) rr[1][j] = col[a][j];
                cur[0] = a; record(1);
                for (int b = a; b < M; b++) {
                    for (int j = 0; j < L; j++) rr[2][j] = rr[1][j] + col[b][j];
                    cur[1] = b; record(2);
                }
            }
        }
        for (int i = 0; i < np; i++) if (pf[i].w == worker) {
            int a = pf[i].a[0], b = pf[i].a[1], c = pf[i].a[2];
            for (int j = 0; j < L; j++) rr[3][j] = col[a][j] + col[b][j] + col[c][j];
            cur[0] = a; cur[1] = b; cur[2] = c;
            record(3);
            rec(3, c);
        }
    }
    FILE *o = fopen(argv[5], "w");
    if (!o) { perror("out"); return 2; }
    fprintf(o, "M %d S %d ND %d worker %d of %d\n", M, S, ND, worker, nworkers);
    for (int m = 0; m < NM; m++) {
        int any = 0;
        for (int s = 0; s <= S; s++) if (cnt[(size_t)m * (S + 1) + s]) any = 1;
        if (!any) continue;
        fprintf(o, "mask %d best %d wit", m, best[m]);
        for (int i = 0; i < best[m]; i++) fprintf(o, " %d", wit[m * MAXS + i]);
        fprintf(o, " counts");
        for (int s = 0; s <= S; s++) fprintf(o, " %llu", (unsigned long long)cnt[(size_t)m * (S + 1) + s]);
        fprintf(o, "\n");
    }
    fclose(o);
    return 0;
}
