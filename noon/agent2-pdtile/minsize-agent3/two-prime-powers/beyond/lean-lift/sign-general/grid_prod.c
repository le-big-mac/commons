// grid.c -- exhaustive test of the "grid statement" on a box X = [n_1] x ... x [n_k].
//
// A signing S : B -> {+1,-1} of a set of cells B is GOOD if for every subset P of the coordinates the
// P-interaction of the marginal of S on the coordinates in P is not zero, i.e. some "cube sum" at level P is
// not zero.  For prime sides and the cyclic group Z_{n_1...n_k} this is exactly: S(zeta) != 0 for every
// root of unity zeta of order dividing n_1...n_k.
//
// Coordinates: I(S)[j] for j = (j_1..j_k), 0 <= j_i < n_i, is the cube sum with corners 0 / j_i in the
// coordinates with j_i >= 1 (the others summed out).  Level of j = {i : j_i >= 1}.  S is good iff every
// level has a nonzero entry.  Exact integer arithmetic.
//
// usage: grid n_1 ... n_k  maxsize  [minsize]
//   all subsets B containing the cell 0 with minsize <= |B| <= maxsize; all signings with the first sign +.
// Output: number of sets, sets without a good signing, the least fraction of good signings and where,
//   and the largest "least number of signs turned from all +" (taken up to the global sign).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXK 6
#define MAXX 128
int k, n[MAXK], NX, NL;
int nw[MAXX];            // number of nonzero entries of w_x
int wj[MAXX][MAXX];      // their positions
signed char wv[MAXX][MAXX]; // their values
int levelof[MAXX];
int I[MAXX], nz[64];
int bad;
static inline void addw(int x, int c) {
    for (int t = 0; t < nw[x]; t++) {
        int j = wj[x][t]; int old = I[j]; int nu = old + c * wv[x][t];
        I[j] = nu;
        if (old == 0 && nu != 0) { if (nz[levelof[j]]++ == 0) bad--; }
        else if (old != 0 && nu == 0) { if (--nz[levelof[j]] == 0) bad++; }
    }
}
int B[MAXX], sz;
long long nsets = 0, nfail = 0;
double minfrac = 2.0; int minB[MAXX], minsz = 0; long long mingood = 0;
int maxflips = 0, maxflipB[MAXX], maxflipsz = 0;
long long histflips[MAXX];

static unsigned char *goodmap = 0;
long long pair_all = 0, pair_some = 0, pair_none = 0; int shown = 0, shown2 = 0;
void process(void) {
    memset(I, 0, sizeof(int) * NX); memset(nz, 0, sizeof(int) * NL); bad = NL;
    int sign[MAXX];
    if (!goodmap) goodmap = malloc(1u << 24);
    for (int i = 0; i < sz; i++) { sign[i] = 1; addw(B[i], 1); }
    unsigned long long total = 1ULL << sz, g = 0; long long good = 0;
    for (unsigned long long c = 0;; c++) {
        goodmap[g] = (bad == 0); good += (bad == 0);
        if (c + 1 == total) break;
        int b = __builtin_ctzll(c + 1);
        g ^= (1ULL << b);
        sign[b] = -sign[b];
        addw(B[b], 2 * sign[b]);
    }
    nsets++;
    if (good == 0) nfail++;
    double fr = (double)good / (double)total;
    if (fr < minfrac) { minfrac = fr; minsz = sz + 1; mingood = good; memcpy(minB, B, sizeof(int) * sz); }
    // product-form signings: S(x) = prod_i sigma_i(x_i)
    int tot = 0; for (int i = 0; i < k; i++) tot += n[i];
    int found = 0;
    for (unsigned long long sg = 0; sg < (1ULL << tot) && !found; sg++) {
        unsigned long long mask = 0;
        for (int e = 0; e < sz; e++) {
            int x = B[e], off = 0, par = 0;
            for (int i = 0; i < k; i++) { par ^= (sg >> (off + x % n[i])) & 1; off += n[i]; x /= n[i]; }
            if (par) mask |= 1ULL << e;
        }
        if (goodmap[mask]) found = 1;
    }
    if (found) pair_all++; else { pair_none++; if (shown++ < 5) { printf("NO PRODUCT-FORM GOOD SIGNING: "); for (int i = 0; i < sz; i++) printf("%d ", B[i]); printf("\n"); } }
}
void rec(int start, int want) {
    if (want == 0) { process(); return; }
    for (int x = start; x <= NX - want; x++) { B[sz++] = x; rec(x + 1, want - 1); sz--; }
}
void printcell(int x) {
    printf("(");
    for (int i = 0; i < k; i++) { printf("%d%s", x % n[i], i + 1 < k ? "," : ""); x /= n[i]; }
    printf(")");
}
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage\n"); return 1; }
    int maxsize, minsize = 1;
    // sides are all args but the last one or two; decide by a marker "--"
    int pos = 1; k = 0;
    while (pos < argc && strcmp(argv[pos], "--") != 0) n[k++] = atoi(argv[pos++]);
    pos++;
    maxsize = atoi(argv[pos++]); if (pos < argc) minsize = atoi(argv[pos++]);
    NX = 1; for (int i = 0; i < k; i++) NX *= n[i];
    NL = 1 << k;
    if (NX > MAXX) { fprintf(stderr, "too big\n"); return 1; }
    for (int j = 0; j < NX; j++) {
        int jj = j, lv = 0;
        for (int i = 0; i < k; i++) { if (jj % n[i]) lv |= 1 << i; jj /= n[i]; }
        levelof[j] = lv;
    }
    for (int x = 0; x < NX; x++) {
        nw[x] = 0;
        for (int j = 0; j < NX; j++) {
            int xx = x, jj = j, v = 1;
            for (int i = 0; i < k; i++) {
                int xi = xx % n[i], ji = jj % n[i]; xx /= n[i]; jj /= n[i];
                if (ji >= 1) { if (xi == ji) v *= 1; else if (xi == 0) v *= -1; else v = 0; }
            }
            if (v) { wj[x][nw[x]] = j; wv[x][nw[x]] = v; nw[x]++; }
        }
    }
    if (maxsize > NX) maxsize = NX;
    for (int s = minsize; s <= maxsize; s++) {
        long long before = nsets, bf = nfail;
        sz = 0; B[sz++] = 0; rec(1, s - 1);
        printf("size %d: %lld sets, %lld without a good signing\n", s, nsets - before, nfail - bf); fflush(stdout);
    }
    printf("box"); for (int i = 0; i < k; i++) printf(" %d", n[i]);
    printf(": sets (containing cell 0, sizes %d..%d): %lld; without a good signing: %lld\n", minsize, maxsize, nsets, nfail);
    printf("least fraction of good signings: %lld / 2^%d = %.6f at B =", mingood, minsz - 1, minfrac);
    for (int i = 0; i < minsz; i++) { printf(" "); printcell(minB[i]); } printf("\n");
    printf("a good signing of product form exists: %lld sets; does not exist: %lld\n", pair_all, pair_none); return 0;
    printf("least number of turned signs needed, histogram:");
    for (int i = 0; i <= maxflips; i++) printf(" %d:%lld", i, histflips[i]); printf("\n");
    printf("largest (%d) at B =", maxflips);
    for (int i = 0; i < maxflipsz; i++) { printf(" "); printcell(maxflipB[i]); } printf("\n");
    return 0;
}
