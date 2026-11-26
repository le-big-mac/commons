/* ref_dp.c -- referee's own recursion over the tree of classes (not the author's dp_sizes.c; written without
   reading it).

   A class with j levels below it has a state (g, E(N), F(N)): its vector g in N^q and its exact pattern on its
   own levels 1..j.  From the definitions of section 1 of proof-as-sent.md, for a class N with children N_0..N_(p-1):
       1 in E(N)  iff the children have equal totals;       1 in F(N) iff the children have equal shapes;
       l in E(N), l >= 2, iff l-1 in E(N_i) for every child i;   same for F
   (an empty child has every level in E and F: this comes out of the recursion itself, starting from depth-n
   classes, which have no levels).  So the set of states of level j is computed from the set of level j-1.

   usage: ref_dp p q n B Bfull out.bin
     levels 0..n-1: every state with total <= B
     level n      : every state with total <= Bfull, and every BALANCED state with total <= B
   output: records of int32: level, g[0..q-1], Ebits, Fbits   (level l <-> bit l-1)
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int p, q, n, B, Bfull;
static int nvec;
static int *vec;        /* nvec x q */
static int *tot;
static int *shapeid;    /* index of g - min(g) 1 */
static int *lookup;     /* mixed radix -> index */
static long radix[8];
static uint64_t *cmask; /* child level masks (child level jj <= 3): bit P, P = E | F << jj */
static uint8_t *present; /* parent level: nvec x npatparent */
static int jcur, npatpar;
static int Bcur;        /* bound on totals for the level being built */
static int balanced_only;

#define CACHE_BITS 22
typedef struct { uint64_t a, b, r; } centry;
static centry *cache;

static inline uint64_t inter(uint64_t a, uint64_t b) {
    if (a == b && (a & (a - 1)) == 0) return a;
    uint64_t h = (a * 0x9E3779B97F4A7C15ULL) ^ (b * 0xC2B2AE3D27D4EB4FULL);
    h ^= h >> 29;
    centry *c = &cache[h & ((1u << CACHE_BITS) - 1)];
    if (c->a == a && c->b == b && c->r) return c->r;
    uint64_t r = 0, x = a;
    while (x) {
        int i = __builtin_ctzll(x); x &= x - 1;
        uint64_t y = b;
        while (y) {
            int k = __builtin_ctzll(y); y &= y - 1;
            r |= 1ULL << (i & k);
        }
    }
    c->a = a; c->b = b; c->r = r;
    return r;
}

static long code_of(const int *g) {
    long c = 0;
    for (int w = 0; w < q; w++) c += g[w] * radix[w];
    return c;
}

static void emit(const int *sum, uint64_t clo, int eqT, int eqS) {
    int idx = lookup[code_of(sum)];
    int jj = jcur - 1;
    int cm = (1 << jj) - 1;
    uint8_t *row = present + (size_t)idx * npatpar;
    while (clo) {
        int P = __builtin_ctzll(clo); clo &= clo - 1;
        int E = P & cm, F = (P >> jj) & cm;
        int E2 = (E << 1) | eqT, F2 = (F << 1) | eqS;
        row[E2 | (F2 << jcur)] = 1;
    }
}

static void rec(int k, int start, int *sum, int sumtot, uint64_t clo, int eqT, int eqS, int tot0, int shape0) {
    if (k == p) { emit(sum, clo, eqT, eqS); return; }
    if (balanced_only && k == p - 1) {
        /* the last child is c*1 - sum */
        int mx = 0;
        for (int w = 0; w < q; w++) if (sum[w] > mx) mx = sum[w];
        for (int c = mx; (long)c * q <= Bcur; c++) {
            int g[8];
            for (int w = 0; w < q; w++) g[w] = c - sum[w];
            int i = lookup[code_of(g)];
            if (i < 0) continue;
            int s2[8];
            for (int w = 0; w < q; w++) s2[w] = c;
            uint64_t c2 = inter(clo, cmask[i]);
            emit(s2, c2, eqT && tot[i] == tot0, eqS && shapeid[i] == shape0);
        }
        return;
    }
    for (int i = start; i < nvec; i++) {
        if (sumtot + tot[i] > Bcur) break;      /* vectors are sorted by total */
        int s2[8];
        const int *g = vec + (size_t)i * q;
        for (int w = 0; w < q; w++) s2[w] = sum[w] + g[w];
        if (k == 0) rec(1, i, s2, tot[i], cmask[i], 1, 1, tot[i], shapeid[i]);
        else rec(k + 1, i, s2, sumtot + tot[i], inter(clo, cmask[i]), eqT && tot[i] == tot0, eqS && shapeid[i] == shape0, tot0, shape0);
    }
}

static int cmp_tot_then_code(const void *a, const void *b) {
    const int *x = a, *y = b;
    int tx = 0, ty = 0;
    for (int w = 0; w < q; w++) { tx += x[w]; ty += y[w]; }
    if (tx != ty) return tx - ty;
    for (int w = 0; w < q; w++) if (x[w] != y[w]) return x[w] - y[w];
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: ref_dp p q n B Bfull out.bin\n"); return 1; }
    p = atoi(argv[1]); q = atoi(argv[2]); n = atoi(argv[3]); B = atoi(argv[4]); Bfull = atoi(argv[5]);
    if (n > 4 || q > 7 || Bfull > B) { fprintf(stderr, "need n <= 4, q <= 7, Bfull <= B\n"); return 1; }
    radix[0] = 1;
    for (int w = 1; w <= q; w++) radix[w] = radix[w - 1] * (B + 1);
    long ncode = radix[q];
    lookup = malloc(sizeof(int) * ncode);
    for (long c = 0; c < ncode; c++) lookup[c] = -1;
    /* enumerate the vectors with total <= B */
    long cap = 1024; nvec = 0; vec = malloc(sizeof(int) * cap * q);
    {
        int g[8]; memset(g, 0, sizeof g);
        for (;;) {
            int t = 0; for (int w = 0; w < q; w++) t += g[w];
            if (t <= B) {
                if (nvec == cap) { cap *= 2; vec = realloc(vec, sizeof(int) * cap * q); }
                memcpy(vec + (size_t)nvec * q, g, sizeof(int) * q); nvec++;
            }
            int w = 0;
            while (w < q) { g[w]++; if (g[w] <= B) break; g[w] = 0; w++; }
            if (w == q) break;
        }
    }
    qsort(vec, nvec, sizeof(int) * q, cmp_tot_then_code);
    tot = malloc(sizeof(int) * nvec); shapeid = malloc(sizeof(int) * nvec);
    for (int i = 0; i < nvec; i++) {
        int t = 0; for (int w = 0; w < q; w++) t += vec[(size_t)i * q + w];
        tot[i] = t; lookup[code_of(vec + (size_t)i * q)] = i;
    }
    for (int i = 0; i < nvec; i++) {
        int g[8], mn = 1 << 30;
        for (int w = 0; w < q; w++) if (vec[(size_t)i * q + w] < mn) mn = vec[(size_t)i * q + w];
        for (int w = 0; w < q; w++) g[w] = vec[(size_t)i * q + w] - mn;
        shapeid[i] = lookup[code_of(g)];
    }
    cache = calloc((size_t)1 << CACHE_BITS, sizeof(centry));
    FILE *fo = fopen(argv[6], "wb");
    /* level 0: every vector, pattern (empty, empty) = pattern index 0 */
    cmask = malloc(sizeof(uint64_t) * nvec);
    for (int i = 0; i < nvec; i++) cmask[i] = 1ULL;
    long nrec = 0;
    for (int i = 0; i < nvec; i++) {
        if (n == 0 && tot[i] > Bfull) {
            int c = 1; for (int w = 1; w < q; w++) if (vec[(size_t)i*q+w] != vec[(size_t)i*q]) c = 0;
            if (!c) continue;
        }
        int32_t r[12]; r[0] = 0; for (int w = 0; w < q; w++) r[1 + w] = vec[(size_t)i * q + w]; r[1 + q] = 0; r[2 + q] = 0;
        fwrite(r, sizeof(int32_t), q + 3, fo); nrec++;
    }
    fprintf(stderr, "p=%d q=%d n=%d B=%d Bfull=%d: %d vectors\n", p, q, n, B, Bfull, nvec);
    for (jcur = 1; jcur <= n; jcur++) {
        npatpar = 1 << (2 * jcur);
        present = calloc((size_t)nvec * npatpar, 1);
        int sum[8]; memset(sum, 0, sizeof sum);
        memset(cache, 0, ((size_t)1 << CACHE_BITS) * sizeof(centry));
        if (jcur < n) {
            balanced_only = 0; Bcur = B;
            rec(0, 0, sum, 0, 0, 1, 1, 0, 0);
        } else {
            balanced_only = 0; Bcur = Bfull;
            rec(0, 0, sum, 0, 0, 1, 1, 0, 0);
            if (B > Bfull) {
                balanced_only = 1; Bcur = B;
                memset(sum, 0, sizeof sum);
                if (p == 1) return 1;
                rec(0, 0, sum, 0, 0, 1, 1, 0, 0);
            }
        }
        long cnt = 0;
        for (int i = 0; i < nvec; i++) {
            uint8_t *row = present + (size_t)i * npatpar;
            for (int P = 0; P < npatpar; P++) if (row[P]) {
                int32_t r[12]; r[0] = jcur; for (int w = 0; w < q; w++) r[1 + w] = vec[(size_t)i * q + w];
                r[1 + q] = P & ((1 << jcur) - 1); r[2 + q] = P >> jcur;
                fwrite(r, sizeof(int32_t), q + 3, fo); cnt++;
            }
        }
        nrec += cnt;
        fprintf(stderr, "level %d: %ld states\n", jcur, cnt);
        if (jcur < n) {
            if (jcur > 3) { fprintf(stderr, "child level too deep\n"); return 1; }
            for (int i = 0; i < nvec; i++) {
                uint64_t m = 0; uint8_t *row = present + (size_t)i * npatpar;
                for (int P = 0; P < npatpar; P++) if (row[P]) m |= 1ULL << P;
                cmask[i] = m;
            }
        }
        free(present);
    }
    fclose(fo);
    fprintf(stderr, "wrote %ld records\n", nrec);
    return 0;
}
