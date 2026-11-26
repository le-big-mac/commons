/* Referee's exhaustive enumeration.  Every multiset (or set) on Z_M, M = p^n q, with 1 <= size <= S is visited once.
   For each one the exact pattern (E, F) is found by the remainder of A(X) on division by Phi_d(X): the remainder is the
   integer combination of the remainders of the monomials X^x, which were found by exact long division (pat.py) and are
   read from the input file.  Independently the pattern is found by the three translations of section 1 of the note
   (class counts on the tree) and the two are compared on every multiset visited; any disagreement stops the run.
   Output: for each pattern met, the number of multisets of each size.
   usage: brute INPUT S cap job njobs      (cap = largest weight allowed: 1 for sets, S for multisets)
   input file: M p q n ND, then for each of the ND divisors (E levels 1..n, then F levels 0..n): deg, and deg rows of M integers. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXM 64
#define MAXROWS 128
#define MAXN 6
static int M, p, q, n, ND, TOT, S, CAP;
static int col[MAXM][MAXROWS];
static int rowstart[2 * MAXN + 2], rowend[2 * MAXN + 2];
static int rem_[MAXROWS];
static int w[MAXM];
static int xu[MAXM], xl[MAXM];
static int pw[MAXN + 1];
static uint64_t *count;         /* count[pattern * (S+1) + size] */
static uint64_t visited = 0;
static int NPAT;

static int cntf[MAXN + 1][256 * 8];   /* cntf[a][c*q + j]: elements in class c mod p^a with residue j mod q */
static int par[MAXN + 1][256];        /* class c mod p^a lies in class par[a][c] mod p^(a-1) */
static int lidx[MAXM];                /* x -> (x mod p^n)*q + (x mod q) */

static int tree_pattern(void) {
    int a, c, j, i, x;
    for (x = 0; x < M; x++) cntf[n][lidx[x]] = w[x];
    for (a = n; a >= 1; a--) {
        memset(cntf[a - 1], 0, sizeof(int) * pw[a - 1] * q);
        for (c = 0; c < pw[a]; c++) {
            int *src = &cntf[a][c * q], *dst = &cntf[a - 1][par[a][c] * q];
            for (j = 0; j < q; j++) dst[j] += src[j];
        }
    }
    int bits = 0;
    /* level 0 in F: root balanced */
    { int ok = 1; for (j = 1; j < q; j++) if (cntf[0][j] != cntf[0][0]) ok = 0; if (ok) bits |= 1 << n; }
    for (a = 1; a <= n; a++) {
        int eqtot = 1, eqshape = 1;
        for (c = 0; c < pw[a - 1] && (eqtot || eqshape); c++) {
            int *k0 = &cntf[a][c * q];
            int t0 = 0; for (j = 0; j < q; j++) t0 += k0[j];
            for (i = 1; i < p; i++) {
                int *ki = &cntf[a][(c + i * pw[a - 1]) * q], ti = 0;
                for (j = 0; j < q; j++) ti += ki[j];
                if (ti != t0) eqtot = 0;
                int d0 = ki[0] - k0[0];
                for (j = 1; j < q; j++) if (ki[j] - k0[j] != d0) eqshape = 0;
            }
        }
        if (eqtot) bits |= 1 << (a - 1);
        if (eqshape) bits |= 1 << (n + a);
    }
    return bits;
}

static inline void evaluate(int size) {
    if (size == 0) return;
    int bits = 0, d, r;
    for (d = 0; d < ND; d++) {
        int z = 1;
        for (r = rowstart[d]; r < rowend[d]; r++) if (rem_[r]) { z = 0; break; }
        if (z) bits |= 1 << d;
    }
    int tb = tree_pattern();
    if (tb != bits) {
        fprintf(stderr, "MISMATCH division %d tree %d weights:", bits, tb);
        for (int x = 0; x < M; x++) fprintf(stderr, " %d", w[x]);
        fprintf(stderr, "\n"); exit(2);
    }
    count[(size_t)bits * (S + 1) + size]++;
    visited++;
}

static void rec(int pos, int used) {
    int lim = S - used, wt, r;
    if (lim > CAP) lim = CAP;
    if (pos == M - 1) {
        for (wt = 0; wt <= lim; wt++) {
            w[pos] = wt;
            evaluate(used + wt);
            for (r = 0; r < TOT; r++) rem_[r] += col[pos][r];
        }
        for (r = 0; r < TOT; r++) rem_[r] -= (lim + 1) * col[pos][r];
        w[pos] = 0;
        return;
    }
    for (wt = 0; wt <= lim; wt++) {
        w[pos] = wt;
        rec(pos + 1, used + wt);
        for (r = 0; r < TOT; r++) rem_[r] += col[pos][r];
    }
    for (r = 0; r < TOT; r++) rem_[r] -= (lim + 1) * col[pos][r];
    w[pos] = 0;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
    FILE *f = fopen(argv[1], "r");
    S = atoi(argv[2]); CAP = atoi(argv[3]);
    int job = atoi(argv[4]), njobs = atoi(argv[5]);
    if (fscanf(f, "%d %d %d %d %d", &M, &p, &q, &n, &ND) != 5) return 1;
    TOT = 0;
    for (int d = 0; d < ND; d++) {
        int deg; if (fscanf(f, "%d", &deg) != 1) return 1;
        rowstart[d] = TOT; rowend[d] = TOT + deg;
        for (int r = 0; r < deg; r++) for (int x = 0; x < M; x++) { if (fscanf(f, "%d", &col[x][TOT + r]) != 1) return 1; }
        TOT += deg;
    }
    fclose(f);
    pw[0] = 1; for (int a = 1; a <= n; a++) pw[a] = pw[a - 1] * p;
    for (int x = 0; x < M; x++) { xu[x] = x % pw[n]; xl[x] = x % q; lidx[x] = xu[x] * q + xl[x]; }
    for (int a = 1; a <= n; a++) for (int c = 0; c < pw[a]; c++) par[a][c] = c % pw[a - 1];
    NPAT = 1 << ND;
    count = calloc((size_t)NPAT * (S + 1), sizeof(uint64_t));
    /* split the work by the weights of positions 0 and 1 */
    int idx = 0;
    int lim0 = S < CAP ? S : CAP;
    for (int w0 = 0; w0 <= lim0; w0++) {
        int lim1 = S - w0; if (lim1 > CAP) lim1 = CAP;
        for (int w1 = 0; w1 <= lim1; w1++, idx++) {
            if (idx % njobs != job) continue;
            memset(rem_, 0, sizeof rem_); memset(w, 0, sizeof w);
            w[0] = w0; w[1] = w1;
            for (int r = 0; r < TOT; r++) rem_[r] = w0 * col[0][r] + w1 * col[1][r];
            rec(2, w0 + w1);
        }
    }
    printf("# M=%d p=%d q=%d n=%d S=%d cap=%d job=%d/%d visited=%llu\n", M, p, q, n, S, CAP, job, njobs, (unsigned long long)visited);
    for (int b = 0; b < NPAT; b++) {
        int any = 0;
        for (int s = 1; s <= S; s++) if (count[(size_t)b * (S + 1) + s]) any = 1;
        if (!any) continue;
        printf("%d", b);
        for (int s = 1; s <= S; s++) if (count[(size_t)b * (S + 1) + s]) printf(" %d:%llu", s, (unsigned long long)count[(size_t)b * (S + 1) + s]);
        printf("\n");
    }
    return 0;
}
