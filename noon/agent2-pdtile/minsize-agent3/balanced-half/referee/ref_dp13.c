/* ref_dp13.c -- referee's recursion over the tree of classes, extended for Proposition 13:
   for every state (g, E(N), F(N)) of a class with j levels below it, the LEAST depth (counted from N, N itself = 0)
   of a nonempty fibre class contained in N, over all multisets with that state.

   A class is a fibre class iff every class inside it is balanced, i.e. iff it is balanced and each child is a
   fibre class (an empty class is a fibre class).  So with mind(N) = least relative depth of a NONEMPTY fibre class
   inside N (INF if none):
       mind(N) = 0                         if N is not empty, g(N) is constant and every child is empty or has mind 0;
       mind(N) = 1 + min over children     otherwise (INF stays INF).
   mind(N) is nondecreasing in each child's mind and the children can be chosen independently given their states,
   so the least value for a parent state is obtained from the least values of the child states.

   usage: ref_dp13 p q n B topall out.bin
     levels 0..n-1: every state with total <= B;  level n: balanced states with total <= B (topall = 0) or every
     state with total <= B (topall = 1)
   output: records of int32: level, g[0..q-1], Ebits, Fbits, mind (254 = no nonempty fibre class inside)
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define INF 254
#define NONE 255
static int p, q, n, B, topall;
static int nvec;
static int *vec, *tot, *shapeid, *isconst, *lookup;
static long radix[8];
/* child level: per vector a list of (pattern, mind) */
static int *cstart, *ccount;
static uint16_t *cpat;
static uint8_t *cmind;
static uint8_t *par;
static int jcur, npatpar, Bcur, balanced_only;
static int chosen[16];

static long code_of(const int *g) { long c = 0; for (int w = 0; w < q; w++) c += g[w] * radix[w]; return c; }

static void combine(const int *sum, int sumtot, int eqT, int eqS) {
    int idx = lookup[code_of(sum)];
    int jj = jcur - 1, cm = (1 << jj) - 1;
    int bal = isconst[idx];
    uint8_t *row = par + (size_t)idx * npatpar;
    /* iterate over the choices of one (pattern, mind) per child: odometer */
    int pos[16];
    for (int k = 0; k < p; k++) pos[k] = 0;
    for (;;) {
        int P = (1 << (2 * jj)) - 1, mn = INF, allfib = 1;
        for (int k = 0; k < p; k++) {
            int i = chosen[k];
            int s = cstart[i] + pos[k];
            P &= cpat[s];
            int m = cmind[s];
            if (m < mn) mn = m;
            if (!(tot[i] == 0 || m == 0)) allfib = 0;
        }
        int E = P & cm, F = (P >> jj) & cm;
        int E2 = (E << 1) | eqT, F2 = (F << 1) | eqS;
        int val;
        if (allfib && bal && sumtot > 0) val = 0;
        else val = (mn == INF) ? INF : mn + 1;
        uint8_t *cell = row + (E2 | (F2 << jcur));
        if (val < *cell) *cell = (uint8_t)val;
        int k = 0;
        while (k < p) { pos[k]++; if (pos[k] < ccount[chosen[k]]) break; pos[k] = 0; k++; }
        if (k == p) break;
    }
}

static void rec(int k, int start, int *sum, int sumtot, int eqT, int eqS, int tot0, int shape0) {
    if (k == p) { combine(sum, sumtot, eqT, eqS); return; }
    if (balanced_only && k == p - 1) {
        int mx = 0;
        for (int w = 0; w < q; w++) if (sum[w] > mx) mx = sum[w];
        for (int c = mx; (long)c * q <= Bcur; c++) {
            int g[8], s2[8];
            for (int w = 0; w < q; w++) { g[w] = c - sum[w]; s2[w] = c; }
            int i = lookup[code_of(g)];
            if (i < 0) continue;
            chosen[k] = i;
            combine(s2, c * q, eqT && tot[i] == tot0, eqS && shapeid[i] == shape0);
        }
        return;
    }
    for (int i = start; i < nvec; i++) {
        if (sumtot + tot[i] > Bcur) break;
        int s2[8];
        const int *g = vec + (size_t)i * q;
        for (int w = 0; w < q; w++) s2[w] = sum[w] + g[w];
        chosen[k] = i;
        if (k == 0) rec(1, i, s2, tot[i], 1, 1, tot[i], shapeid[i]);
        else rec(k + 1, i, s2, sumtot + tot[i], eqT && tot[i] == tot0, eqS && shapeid[i] == shape0, tot0, shape0);
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
    if (argc < 7) { fprintf(stderr, "usage: ref_dp13 p q n B topall out.bin\n"); return 1; }
    p = atoi(argv[1]); q = atoi(argv[2]); n = atoi(argv[3]); B = atoi(argv[4]); topall = atoi(argv[5]);
    if (n > 5 || q > 7 || p > 15) { fprintf(stderr, "need n <= 5, q <= 7, p <= 15\n"); return 1; }
    radix[0] = 1;
    for (int w = 1; w <= q; w++) radix[w] = radix[w - 1] * (B + 1);
    long ncode = radix[q];
    lookup = malloc(sizeof(int) * ncode);
    for (long c = 0; c < ncode; c++) lookup[c] = -1;
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
    tot = malloc(sizeof(int) * nvec); shapeid = malloc(sizeof(int) * nvec); isconst = malloc(sizeof(int) * nvec);
    for (int i = 0; i < nvec; i++) {
        int t = 0, c = 1;
        for (int w = 0; w < q; w++) { t += vec[(size_t)i * q + w]; if (vec[(size_t)i * q + w] != vec[(size_t)i * q]) c = 0; }
        tot[i] = t; isconst[i] = c; lookup[code_of(vec + (size_t)i * q)] = i;
    }
    for (int i = 0; i < nvec; i++) {
        int g[8], mn = 1 << 30;
        for (int w = 0; w < q; w++) if (vec[(size_t)i * q + w] < mn) mn = vec[(size_t)i * q + w];
        for (int w = 0; w < q; w++) g[w] = vec[(size_t)i * q + w] - mn;
        shapeid[i] = lookup[code_of(g)];
    }
    FILE *fo = fopen(argv[6], "wb");
    cstart = malloc(sizeof(int) * nvec); ccount = malloc(sizeof(int) * nvec);
    cpat = malloc(sizeof(uint16_t) * nvec); cmind = malloc(nvec);
    long nrec = 0;
    for (int i = 0; i < nvec; i++) {
        cstart[i] = i; ccount[i] = 1; cpat[i] = 0;
        cmind[i] = (isconst[i] && tot[i] > 0) ? 0 : INF;
        if (n == 0) {
            int32_t r[12]; r[0] = 0; for (int w = 0; w < q; w++) r[1 + w] = vec[(size_t)i * q + w];
            r[1 + q] = 0; r[2 + q] = 0; r[3 + q] = cmind[i];
            fwrite(r, sizeof(int32_t), q + 4, fo); nrec++;
        }
    }
    fprintf(stderr, "p=%d q=%d n=%d B=%d topall=%d: %d vectors\n", p, q, n, B, topall, nvec);
    for (jcur = 1; jcur <= n; jcur++) {
        npatpar = 1 << (2 * jcur);
        par = malloc((size_t)nvec * npatpar);
        memset(par, NONE, (size_t)nvec * npatpar);
        int sum[8]; memset(sum, 0, sizeof sum);
        Bcur = B;
        balanced_only = (jcur == n && !topall);
        rec(0, 0, sum, 0, 1, 1, 0, 0);
        long cnt = 0;
        for (size_t s = 0; s < (size_t)nvec * npatpar; s++) if (par[s] != NONE) cnt++;
        fprintf(stderr, "level %d: %ld states\n", jcur, cnt);
        if (jcur == n) {
            for (int i = 0; i < nvec; i++) {
                uint8_t *row = par + (size_t)i * npatpar;
                for (int P = 0; P < npatpar; P++) if (row[P] != NONE) {
                    int32_t r[12]; r[0] = jcur; for (int w = 0; w < q; w++) r[1 + w] = vec[(size_t)i * q + w];
                    r[1 + q] = P & ((1 << jcur) - 1); r[2 + q] = P >> jcur; r[3 + q] = row[P];
                    fwrite(r, sizeof(int32_t), q + 4, fo); nrec++;
                }
            }
        } else {
            free(cpat); free(cmind);
            cpat = malloc(sizeof(uint16_t) * cnt); cmind = malloc(cnt);
            long s = 0;
            for (int i = 0; i < nvec; i++) {
                uint8_t *row = par + (size_t)i * npatpar;
                cstart[i] = (int)s; ccount[i] = 0;
                for (int P = 0; P < npatpar; P++) if (row[P] != NONE) { cpat[s] = (uint16_t)P; cmind[s] = row[P]; s++; ccount[i]++; }
            }
        }
        free(par);
    }
    fclose(fo);
    fprintf(stderr, "wrote %ld records\n", nrec);
    return 0;
}
