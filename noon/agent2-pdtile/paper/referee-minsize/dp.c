/* Referee's exhaustive recursion over the tree of Section 2.
 *
 * usage: dp p q n B
 *
 * For every j = 0..n it computes the set of all quadruples
 *     (E(N), F(N), balanced?, |N|)
 * that occur for a class N with j levels below it and at most B elements
 * (equivalently: for the root of a multiset on Z_{p^j q} of size <= B).
 *
 * A class with j levels below it is described by its vector g in N^q and its pattern;
 * T[j][g] is the set of patterns (E, F) that classes with vector g can have.
 * A class with j >= 1 levels has p children c_0..c_{p-1}, each a class with j-1 levels:
 *   g(N) = sum g(c_i)
 *   1 in E(N)   iff the children have equal totals
 *   1 in F(N)   iff the children have equal shapes (vectors differing by constants)
 *   l+1 in E(N) iff l in E(c_i) for every i          (same for F)
 * (an empty class has every level in E and in F: this comes out of the recursion).
 * The children are added one at a time; after i children the state is the sum so far
 * together with "equal totals so far", "equal shapes so far" and the intersections so far.
 * With i children of equal totals the common total is |sum|/i, and with equal shapes
 * the next child v has the common shape iff i*v - sum is a constant vector.
 *
 * Pattern code for j levels: bits 0..j-1 = E (bit l-1 for own level l), bits j..2j-1 = F.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXQ 8
#define W 4            /* 256 bits: up to j = 4 */
typedef struct { uint64_t w[W]; } mask_t;

static int p, q, n, B;
static long nvec;
static int *vec;       /* nvec x q */
static int *tot;
static long *key;
static int *lookup;
static long *cnt_le;   /* number of vectors with total <= t (vectors are sorted by total) */

static inline int mask_empty(const mask_t *m) { return !(m->w[0] | m->w[1] | m->w[2] | m->w[3]); }
static inline void mask_set(mask_t *m, int b) { m->w[b >> 6] |= (uint64_t)1 << (b & 63); }
static inline int mask_get(const mask_t *m, int b) { return (m->w[b >> 6] >> (b & 63)) & 1; }

static int cmp_tot(const void *a, const void *b) {
    const int *x = a, *y = b; int sx = 0, sy = 0;
    for (int i = 0; i < q; i++) { sx += x[i]; sy += y[i]; }
    if (sx != sy) return sx - sy;
    for (int i = 0; i < q; i++) if (x[i] != y[i]) return x[i] - y[i];
    return 0;
}

static void gen(int pos, int left, int *cur, long *count, int *out) {
    if (pos == q) { if (out) memcpy(out + (*count) * q, cur, q * sizeof(int)); (*count)++; return; }
    for (int x = 0; x <= left; x++) { cur[pos] = x; gen(pos + 1, left - x, cur, count, out); }
}

int main(int argc, char **argv) {
    if (argc != 5) { fprintf(stderr, "usage: dp p q n B\n"); return 1; }
    p = atoi(argv[1]); q = atoi(argv[2]); n = atoi(argv[3]); B = atoi(argv[4]);
    if (q > MAXQ || n > 4) { fprintf(stderr, "q <= %d, n <= 4\n", MAXQ); return 1; }
    int cur[MAXQ]; long count = 0;
    gen(0, B, cur, &count, NULL);
    nvec = count;
    vec = malloc(sizeof(int) * nvec * q);
    count = 0; gen(0, B, cur, &count, vec);
    qsort(vec, nvec, q * sizeof(int), cmp_tot);
    long R = B + 1, tabsize = 1;
    for (int i = 0; i < q; i++) tabsize *= R;
    lookup = malloc(sizeof(int) * tabsize);
    for (long i = 0; i < tabsize; i++) lookup[i] = -1;
    tot = malloc(sizeof(int) * nvec); key = malloc(sizeof(long) * nvec);
    cnt_le = calloc(B + 2, sizeof(long));
    for (long i = 0; i < nvec; i++) {
        long k = 0, mul = 1; int s = 0;
        for (int w = 0; w < q; w++) { k += vec[i * q + w] * mul; mul *= R; s += vec[i * q + w]; }
        key[i] = k; tot[i] = s; lookup[k] = (int)i; cnt_le[s]++;
    }
    for (int t = 1; t <= B; t++) cnt_le[t] += cnt_le[t - 1];
    char *isbal = malloc(nvec);
    for (long i = 0; i < nvec; i++) {
        int c = 1; for (int w = 1; w < q; w++) if (vec[i * q + w] != vec[i * q]) c = 0;
        isbal[i] = c;
    }
    fprintf(stderr, "p=%d q=%d n=%d B=%d vectors=%ld\n", p, q, n, B, nvec);

    mask_t *T = calloc(nvec, sizeof(mask_t));      /* level j-1 */
    mask_t *P = calloc(nvec, sizeof(mask_t));      /* partial, i children */
    mask_t *P2 = calloc(nvec, sizeof(mask_t));
    for (long i = 0; i < nvec; i++) mask_set(&T[i], 0);     /* j = 0: the only pattern is the empty one */

    for (int j = 0; j <= n; j++) {
        if (j >= 1) {
            int nb = 1 << (2 * (j - 1));          /* number of child codes */
            int jm = j - 1;
            int childE_mask = (1 << jm) - 1;
            /* one child */
            memset(P, 0, nvec * sizeof(mask_t));
            for (long a = 0; a < nvec; a++)
                for (int b = 0; b < nb; b++) if (mask_get(&T[a], b)) {
                    int bE = b & childE_mask, bF = b >> jm;
                    int code = (1 | (bE << 1)) | ((1 | (bF << 1)) << j);
                    mask_set(&P[a], code);
                }
            int na = 1 << (2 * j);
            for (int i = 1; i < p; i++) {
                memset(P2, 0, nvec * sizeof(mask_t));
                long pairs = 0;
                for (long a = 0; a < nvec; a++) {
                    if (mask_empty(&P[a])) continue;
                    int alist[256], nal = 0;
                    for (int c = 0; c < na; c++) if (mask_get(&P[a], c)) alist[nal++] = c;
                    long lim = cnt_le[B - tot[a]];
                    const int *ga = vec + a * q;
                    for (long b = 0; b < lim; b++) {
                        if (mask_empty(&T[b])) continue;
                        pairs++;
                        const int *vb = vec + b * q;
                        int tflag = (i * tot[b] == tot[a]);
                        int sflag = 1; int d0 = i * vb[0] - ga[0];
                        for (int w = 1; w < q; w++) if (i * vb[w] - ga[w] != d0) { sflag = 0; break; }
                        long s = lookup[key[a] + key[b]];
                        mask_t *dst = &P2[s];
                        for (int bb = 0; bb < nb; bb++) if (mask_get(&T[b], bb)) {
                            int bE = bb & childE_mask, bF = bb >> jm;
                            for (int x = 0; x < nal; x++) {
                                int c = alist[x];
                                int aE = c & ((1 << j) - 1), aF = c >> j;
                                int nE = (((aE >> 1) & bE) << 1) | (aE & 1 & tflag);
                                int nF = (((aF >> 1) & bF) << 1) | (aF & 1 & sflag);
                                mask_set(dst, nE | (nF << j));
                            }
                        }
                    }
                }
                mask_t *tmp = P; P = P2; P2 = tmp;
                fprintf(stderr, "  level %d child %d: %ld pairs\n", j, i + 1, pairs);
            }
            memcpy(T, P, nvec * sizeof(mask_t));
        }
        /* output: for each code and balance, the set of totals */
        int nc = 1 << (2 * j);
        char *seen = calloc((size_t)nc * 2 * (B + 1), 1);
        for (long a = 0; a < nvec; a++)
            for (int c = 0; c < nc; c++) if (mask_get(&T[a], c))
                seen[((size_t)c * 2 + isbal[a]) * (B + 1) + tot[a]] = 1;
        for (int c = 0; c < nc; c++) for (int b = 0; b < 2; b++) {
            int any = 0;
            for (int t = 0; t <= B; t++) if (seen[((size_t)c * 2 + b) * (B + 1) + t]) any = 1;
            if (!any) continue;
            printf("%d %d %d %d", j, c & ((1 << j) - 1), c >> j, b);
            for (int t = 0; t <= B; t++) if (seen[((size_t)c * 2 + b) * (B + 1) + t]) printf(" %d", t);
            printf("\n");
        }
        free(seen);
    }
    return 0;
}
