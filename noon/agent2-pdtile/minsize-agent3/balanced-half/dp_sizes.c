/* COPY of ../check/dp.c with one added block (marked ADDED) that dumps every attainable size per pattern and stage.
   Referee's own search, independent of the note's two solvers: a recursion over the tree of classes.
   A class with j levels below it is described by its layer vector g in N^q (how many elements in each residue mod q)
   and its exact pattern P (which of its levels 1..j have equal totals, which have equal shapes).  For every vector g with
   |g| <= S the program finds the set X[j][g] of ALL exact patterns that some multiset (or set) in such a class can have:
       pattern(parent) = (level 1: do the p children have equal totals? equal shapes?) + (levels >= 2: the intersection of
       the children's patterns, shifted by one; an empty child counts as having every level),
   which is the recursion (2) of the paper.  The intersection over p children is done by counting: for each Q, the number
   of choices whose patterns all contain Q is a product; summing over the ways to split g among the children and then
   inverting over Q (Moebius) gives the number of choices with intersection exactly Q.  All arithmetic is in integers.
   At the root: least |g| per pattern, separately for balanced g (0 in F) and unbalanced g (0 not in F).
   Witnesses are rebuilt by backtracking and printed, to be checked elsewhere by exact polynomial division.

   usage: dp p q n S SU kind(multi|set) [witness: 0 none, 1 one per pattern at the least size]
   S  = largest size of any class considered (and of a balanced root); SU = largest size of an unbalanced root (SU <= S).  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>

#define MAXQ 8
#define MAXN 7
static int p, q, n, S, SU, SETS;
static int NV;
static uint8_t *vec;            /* NV * q */
static int *tot, *mn;
static uint8_t *bal;
static int *canon;          /* index of the vector with the same entries sorted (layers may be permuted without changing any pattern) */
static uint64_t B;
static int32_t *key2idx;
static uint64_t *keyv;
static uint64_t *X[MAXN + 1];   /* exact patterns: NV * W[j] words */
static int W[MAXN + 1];
static uint64_t *PART[MAXN + 1][8][4];   /* PART[j][m][fl]: exact partial states after m children (2 <= m <= p-1), NV * W[j-1] words */
static int pw[MAXN + 1];

static void gen(int pos, int left, uint8_t *cur, int count_only) {
    if (pos == q) {
        if (!count_only) {
            memcpy(vec + (size_t)NV * q, cur, q);
            uint64_t k = 0, m = 1; int t = 0, mi = 1 << 30, b = 1;
            for (int i = 0; i < q; i++) { k += cur[i] * m; m *= B; t += cur[i]; if (cur[i] < mi) mi = cur[i]; if (cur[i] != cur[0]) b = 0; }
            keyv[NV] = k; tot[NV] = t; mn[NV] = mi; bal[NV] = b; key2idx[k] = NV;
        }
        NV++; return;
    }
    for (int x = 0; x <= left; x++) { cur[pos] = x; gen(pos + 1, left - x, cur, count_only); }
}

static inline int getbit(const uint64_t *a, int i) { return (a[i >> 6] >> (i & 63)) & 1; }
static inline void setbit(uint64_t *a, int i) { a[i >> 6] |= 1ULL << (i & 63); }

static inline int comb_flags(int fl, int h, int g, int m) {
    /* h = sum of m children with flags fl (bit0: equal totals so far, bit1: equal shapes so far); add child g */
    int ne = (fl & 1) && (tot[g] * m == tot[h]);
    int nf = 0;
    if (fl & 2) {
        nf = 1;
        const uint8_t *vh = vec + (size_t)h * q, *vg = vec + (size_t)g * q;
        for (int i = 0; i < q; i++) if (m * (vg[i] - mn[g]) != vh[i] - mn[h]) { nf = 0; break; }
    }
    return ne | (nf << 1);
}

/* exact partial states after m children at stage j: for m = 1 it is X[j-1] with fl = 3 */
static inline const uint64_t *part(int j, int m, int fl, int h) {
    if (m == 1) return fl == 3 ? X[j - 1] + (size_t)h * W[j - 1] : NULL;
    return PART[j][m][fl] + (size_t)h * W[j - 1];
}

static int dec_rec(int j, int m, int h, int fl, int Qm, int *gs, int *Ps) {
    int NP = 1 << (2 * (j - 1));
    if (m == 1) {
        if (fl != 3 || !getbit(X[j - 1] + (size_t)h * W[j - 1], Qm)) return 0;
        gs[0] = h; Ps[0] = Qm; return 1;
    }
    const uint8_t *vh = vec + (size_t)h * q;
    uint8_t cur[MAXQ]; memset(cur, 0, sizeof cur);
    while (1) {
        uint64_t k = 0, mm = 1; for (int i = 0; i < q; i++) { k += cur[i] * mm; mm *= B; }
        int h2 = key2idx[k], g = key2idx[keyv[h] - k];
        for (int f2 = 0; f2 < 4; f2++) {
            const uint64_t *ps = part(j, m - 1, f2, h2);
            if (!ps) continue;
            if (comb_flags(f2, h2, g, m - 1) != fl) continue;
            const uint64_t *xg = X[j - 1] + (size_t)g * W[j - 1];
            for (int Q2 = 0; Q2 < NP; Q2++) {
                if ((Q2 & Qm) != Qm || !getbit(ps, Q2)) continue;
                for (int Pg = 0; Pg < NP; Pg++) {
                    if ((Pg & Qm) != Qm || !getbit(xg, Pg) || (Q2 & Pg) != Qm) continue;
                    gs[m - 1] = g; Ps[m - 1] = Pg;
                    if (dec_rec(j, m - 1, h2, f2, Q2, gs, Ps)) return 1;
                }
            }
        }
        int i = 0;
        while (i < q) { if (cur[i] < vh[i]) { cur[i]++; break; } cur[i] = 0; i++; }
        if (i == q) break;
    }
    return 0;
}

static int *wit;   /* weights on Z_M */
static int emit(int j, int v, int P, int u) {
    if (j == 0) {
        int M = pw[n] * q;
        for (int i = 0; i < q; i++) {
            int c = vec[(size_t)v * q + i];
            if (!c) continue;
            int x; for (x = 0; x < M; x++) if (x % pw[n] == u && x % q == i) break;
            wit[x] += c;
        }
        return 1;
    }
    int gs[8], Ps[8];
    if (!dec_rec(j, p, v, P & 3, P >> 2, gs, Ps)) { fprintf(stderr, "backtracking failed at stage %d\n", j); return 0; }
    for (int c = 0; c < p; c++) if (!emit(j - 1, gs[c], Ps[c], u + c * pw[n - j])) return 0;
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: dp p q n S SU multi|set [witness]\n"); return 1; }
    p = atoi(argv[1]); q = atoi(argv[2]); n = atoi(argv[3]); S = atoi(argv[4]); SU = atoi(argv[5]);
    SETS = (strcmp(argv[6], "set") == 0);
    int want_wit = argc > 7 ? atoi(argv[7]) : 0;
    if (SU > S) SU = S;
    pw[0] = 1; for (int a = 1; a <= n; a++) pw[a] = pw[a - 1] * p;
    B = S + 1;
    { uint8_t cur[MAXQ]; NV = 0; gen(0, S, cur, 1); }
    int nv = NV;
    uint64_t tab = 1; for (int i = 0; i < q; i++) tab *= B;
    if (tab > 600000000ULL) { fprintf(stderr, "key table too large\n"); return 1; }
    vec = malloc((size_t)nv * q); tot = malloc(sizeof(int) * nv); mn = malloc(sizeof(int) * nv); bal = malloc(nv);
    keyv = malloc(sizeof(uint64_t) * nv); key2idx = malloc(sizeof(int32_t) * tab);
    for (uint64_t i = 0; i < tab; i++) key2idx[i] = -1;
    { uint8_t cur[MAXQ]; NV = 0; gen(0, S, cur, 0); }
    canon = malloc(sizeof(int) * NV);
    for (int v = 0; v < NV; v++) {
        uint8_t t[MAXQ]; memcpy(t, vec + (size_t)v * q, q);
        for (int i = 0; i < q; i++) for (int k = i + 1; k < q; k++) if (t[k] > t[i]) { uint8_t z = t[i]; t[i] = t[k]; t[k] = z; }
        uint64_t k = 0, m = 1; for (int i = 0; i < q; i++) { k += t[i] * m; m *= B; }
        canon[v] = key2idx[k];
    }
    fprintf(stderr, "p=%d q=%d n=%d S=%d SU=%d %s: %d vectors\n", p, q, n, S, SU, SETS ? "sets" : "multisets", NV);

    for (int j = 0; j <= n; j++) { int np = 1 << (2 * j); W[j] = (np + 63) / 64; X[j] = calloc((size_t)NV * W[j], 8); }
    for (int v = 0; v < NV; v++) {
        int ok = 1;
        if (SETS) for (int i = 0; i < q; i++) if (vec[(size_t)v * q + i] > 1) ok = 0;
        if (ok) setbit(X[0] + (size_t)v * W[0], 0);
    }

    for (int j = 1; j <= n; j++) {
        int NP = 1 << (2 * (j - 1)), nb = 2 * (j - 1);
        /* zeta counts of the children: Zc[g][Q] = number of exact patterns of g that contain Q */
        uint16_t *Zc = calloc((size_t)NV * NP, 2);
        size_t *spo = malloc(sizeof(size_t) * (NV + 1));
        #pragma omp parallel for schedule(static)
        for (int v = 0; v < NV; v++) {
            uint16_t *z = Zc + (size_t)v * NP; const uint64_t *x = X[j - 1] + (size_t)v * W[j - 1];
            for (int Q = 0; Q < NP; Q++) z[Q] = getbit(x, Q);
            for (int b = 0; b < nb; b++) for (int Q = 0; Q < NP; Q++) if (!(Q >> b & 1)) z[Q] += z[Q | (1 << b)];
        }
        size_t nnz = 0;
        for (int v = 0; v < NV; v++) { spo[v] = nnz; for (int Q = 0; Q < NP; Q++) if (Zc[(size_t)v * NP + Q]) nnz++; }
        spo[NV] = nnz;
        uint16_t *spQ = malloc(2 * (nnz + 1)), *spZ = malloc(2 * (nnz + 1));
        { size_t t = 0; for (int v = 0; v < NV; v++) for (int Q = 0; Q < NP; Q++) if (Zc[(size_t)v * NP + Q]) { spQ[t] = Q; spZ[t] = Zc[(size_t)v * NP + Q]; t++; } }
        /* partial states */
        uint16_t *Cd[4] = {NULL, NULL, NULL, NULL}, *Cn[4] = {NULL, NULL, NULL, NULL};
        uint8_t *ne[4], *nen[4];
        for (int f = 0; f < 4; f++) { ne[f] = calloc(NV, 1); nen[f] = calloc(NV, 1); }
        Cd[3] = Zc;
        for (int v = 0; v < NV; v++) ne[3][v] = (spo[v + 1] > spo[v]);
        for (int m = 1; m <= p - 1; m++) {
            int last = (m == p - 1);
            if (!last) {
                for (int f = 0; f < 4; f++) { Cn[f] = calloc((size_t)NV * NP, 2); PART[j][m + 1][f] = calloc((size_t)NV * W[j - 1], 8); memset(nen[f], 0, NV); }
            }
            #pragma omp parallel
            {
                int64_t *acc = malloc(sizeof(int64_t) * 4 * NP);
                uint8_t cur[MAXQ];
                #pragma omp for schedule(dynamic, 16)
                for (int v = 0; v < NV; v++) {
                    if (canon[v] != v) continue;
                    if (last && j == n) { if (bal[v] ? tot[v] > S : tot[v] > SU) continue; }
                    memset(acc, 0, sizeof(int64_t) * 4 * NP);
                    int used[4] = {0, 0, 0, 0};
                    const uint8_t *vv = vec + (size_t)v * q;
                    memset(cur, 0, sizeof cur);
                    while (1) {
                        uint64_t k = 0, mm = 1; for (int i = 0; i < q; i++) { k += cur[i] * mm; mm *= B; }
                        int h = key2idx[k], g = key2idx[keyv[v] - k];
                        size_t s0 = spo[g], s1 = spo[g + 1];
                        if (s1 > s0) {
                            for (int f = 0; f < 4; f++) {
                                if (!Cd[f] || !ne[f][h]) continue;
                                int nf = comb_flags(f, h, g, m);
                                const uint16_t *c = Cd[f] + (size_t)h * NP;
                                int64_t *a = acc + (size_t)nf * NP;
                                used[nf] = 1;
                                for (size_t t = s0; t < s1; t++) a[spQ[t]] += (int64_t)c[spQ[t]] * spZ[t];
                            }
                        }
                        int i = 0;
                        while (i < q) { if (cur[i] < vv[i]) { cur[i]++; break; } cur[i] = 0; i++; }
                        if (i == q) break;
                    }
                    for (int f = 0; f < 4; f++) {
                        if (!used[f]) continue;
                        int64_t *a = acc + (size_t)f * NP;
                        for (int b = 0; b < nb; b++) for (int Q = 0; Q < NP; Q++) if (!(Q >> b & 1)) a[Q] -= a[Q | (1 << b)];
                        if (last) {
                            uint64_t *x = X[j] + (size_t)v * W[j];
                            for (int Q = 0; Q < NP; Q++) { if (a[Q] < 0) { fprintf(stderr, "negative count\n"); exit(3); } if (a[Q] > 0) setbit(x, (Q << 2) | f); }
                        } else {
                            uint64_t *x = PART[j][m + 1][f] + (size_t)v * W[j - 1];
                            uint16_t *z = Cn[f] + (size_t)v * NP; int any = 0;
                            for (int Q = 0; Q < NP; Q++) { if (a[Q] < 0) { fprintf(stderr, "negative count\n"); exit(3); } z[Q] = a[Q] > 0; if (z[Q]) { setbit(x, Q); any = 1; } }
                            for (int b = 0; b < nb; b++) for (int Q = 0; Q < NP; Q++) if (!(Q >> b & 1)) z[Q] += z[Q | (1 << b)];
                            nen[f][v] = any;
                        }
                    }
                }
                free(acc);
            }
            /* copy the results to the vectors that are permutations of a computed one */
            for (int v = 0; v < NV; v++) {
                int c = canon[v]; if (c == v) continue;
                if (last) memcpy(X[j] + (size_t)v * W[j], X[j] + (size_t)c * W[j], 8 * W[j]);
                else for (int f = 0; f < 4; f++) {
                    memcpy(PART[j][m + 1][f] + (size_t)v * W[j - 1], PART[j][m + 1][f] + (size_t)c * W[j - 1], 8 * W[j - 1]);
                    memcpy(Cn[f] + (size_t)v * NP, Cn[f] + (size_t)c * NP, 2 * NP);
                    nen[f][v] = nen[f][c];
                }
            }
            if (!last) {
                for (int f = 0; f < 4; f++) {
                    if (Cd[f] && Cd[f] != Zc) free(Cd[f]);
                    Cd[f] = Cn[f]; Cn[f] = NULL;
                    uint8_t *t = ne[f]; ne[f] = nen[f]; nen[f] = t;
                }
            }
        }
        for (int f = 0; f < 4; f++) { if (Cd[f] && Cd[f] != Zc) free(Cd[f]); free(ne[f]); free(nen[f]); }
        free(Zc); free(spo); free(spQ); free(spZ);
        fprintf(stderr, "stage %d done\n", j);
    }

    /* ADDED in prove/dp_sizes.c (not in the referee's dp.c): for every stage j (a class with j levels below it), every exact
       pattern P of its j levels and bal in {0,1}, the list of ALL sizes s <= S such that some vector of total s (balanced iff bal)
       has exact pattern P.  Lines: "A j bal P s1 s2 ..." written to the file named in argv[8] (if given).
       P: bit 2(l-1) = level l in E, bit 2(l-1)+1 = level l in F. */
    if (argc > 8) {
        FILE *fa = fopen(argv[8], "w");
        fprintf(fa, "# p=%d q=%d n=%d S=%d SU=%d kind=%s\n", p, q, n, S, SU, SETS ? "set" : "multi");
        for (int j = 0; j <= n; j++) {
            int NPj = 1 << (2 * j);
            int lim = S;
            uint8_t *seen = calloc((size_t)NPj * 2 * (S + 1), 1);
            for (int v = 1; v < NV; v++) {
                if (j == n && !bal[v] && tot[v] > SU) continue;
                const uint64_t *x = X[j] + (size_t)v * W[j];
                for (int P = 0; P < NPj; P++) if (getbit(x, P)) seen[((size_t)P * 2 + bal[v]) * (S + 1) + tot[v]] = 1;
            }
            for (int P = 0; P < NPj; P++) for (int b = 0; b < 2; b++) {
                int any = 0;
                for (int s = 1; s <= lim; s++) if (seen[((size_t)P * 2 + b) * (S + 1) + s]) { any = 1; break; }
                if (!any) continue;
                fprintf(fa, "A %d %d %d", j, b, P);
                for (int s = 1; s <= lim; s++) if (seen[((size_t)P * 2 + b) * (S + 1) + s]) fprintf(fa, " %d", s);
                fprintf(fa, "\n");
            }
            free(seen);
        }
        fclose(fa);
    }

    /* root: least size per pattern */
    int NPn = 1 << (2 * n);
    printf("# p=%d q=%d n=%d M=%d kind=%s S=%d SU=%d\n", p, q, n, pw[n] * q, SETS ? "set" : "multi", S, SU);
    wit = malloc(sizeof(int) * pw[n] * q);
    for (int balanced = 0; balanced < 2; balanced++) {
        for (int P = 0; P < NPn; P++) {
            int best = -1, bv = -1;
            for (int v = 1; v < NV; v++) {
                if (bal[v] != balanced) continue;
                if (balanced ? tot[v] > S : tot[v] > SU) continue;
                if (getbit(X[n] + (size_t)v * W[n], P) && (best < 0 || tot[v] < best)) { best = tot[v]; bv = v; }
            }
            printf("R %d ", balanced);
            printf("E");
            for (int l = 1; l <= n; l++) if (P >> (2 * (l - 1)) & 1) printf(",%d", l);
            printf(" F");
            if (balanced) printf(",0");
            for (int l = 1; l <= n; l++) if (P >> (2 * (l - 1) + 1) & 1) printf(",%d", l);
            printf(" min %d", best);
            if (best > 0 && want_wit) {
                memset(wit, 0, sizeof(int) * pw[n] * q);
                if (emit(n, bv, P, 0)) {
                    printf(" W");
                    for (int x = 0; x < pw[n] * q; x++) if (wit[x]) { if (wit[x] > 1) printf(" %d^%d", x, wit[x]); else printf(" %d", x); }
                }
            }
            printf("\n");
        }
    }
    return 0;
}
