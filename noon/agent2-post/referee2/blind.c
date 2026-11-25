// Referee's blind program: Mastermind 4 pegs 6 colours, U of a list of blind questions.
// modes:
//   blind small           -> m(1), m(2), m(3) by complete search (ordered lists, up to symmetry)
//   blind four r k [B]    -> complete search of quadruples, pair-orbit index % k == r
//   blind list c1 c2 ...  -> U of a given list (digits 1..6)
//   blind check n         -> compare fast inner loop with plain recursion on n random quadruples
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 1296
static uint8_t A[N][N];
static int D[N][4];
static uint16_t *IMG; static int NG = 0;
static int reps[N], nreps = 0;
static int pr1[20000], pr2[20000], npairs = 0;

static void init(void) {
    int idx[5][5], k = 0;
    for (int b = 0; b <= 4; b++) for (int w = 0; w + b <= 4; w++) {
        if (b == 3 && w == 1) { idx[b][w] = -1; continue; }
        idx[b][w] = k++;
    }
    if (k != 14) { fprintf(stderr, "bad k\n"); exit(1); }
    for (int c = 0; c < N; c++) { int x = c; for (int p = 3; p >= 0; p--) { D[c][p] = x % 6; x /= 6; } }
    for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) {
        int bl = 0, ca[6] = {0}, cb[6] = {0}, tot = 0;
        for (int p = 0; p < 4; p++) { if (D[a][p] == D[b][p]) bl++; ca[D[a][p]]++; cb[D[b][p]]++; }
        for (int c = 0; c < 6; c++) tot += ca[c] < cb[c] ? ca[c] : cb[c];
        A[a][b] = (uint8_t)idx[bl][tot - bl];
    }
}
static int nextperm(int *a, int n) {
    int i = n - 2; while (i >= 0 && a[i] > a[i + 1]) i--;
    if (i < 0) return 0;
    int j = n - 1; while (a[j] < a[i]) j--;
    int t = a[i]; a[i] = a[j]; a[j] = t;
    for (int l = i + 1, r = n - 1; l < r; l++, r--) { t = a[l]; a[l] = a[r]; a[r] = t; }
    return 1;
}
static void group(void) {
    IMG = malloc((size_t)17280 * N * sizeof(uint16_t));
    int pp[4] = {0, 1, 2, 3};
    do {
        int cp[6] = {0, 1, 2, 3, 4, 5};
        do {
            uint16_t *row = IMG + (size_t)NG * N;
            for (int c = 0; c < N; c++) {
                int x = 0;
                for (int p = 0; p < 4; p++) x = x * 6 + cp[D[c][pp[p]]];
                row[c] = (uint16_t)x;
            }
            NG++;
        } while (nextperm(cp, 6));
    } while (nextperm(pp, 4));
    if (NG != 17280) { fprintf(stderr, "bad NG\n"); exit(1); }
    for (int c = 0; c < N; c++) {
        int mn = c;
        for (int g = 0; g < NG; g++) { int x = IMG[(size_t)g * N + c]; if (x < mn) mn = x; }
        if (mn == c) reps[nreps++] = c;
    }
    for (int i = 0; i < nreps; i++) {
        int q1 = reps[i];
        static int mn[N];
        for (int c = 0; c < N; c++) mn[c] = c;
        for (int g = 0; g < NG; g++) {
            uint16_t *row = IMG + (size_t)g * N;
            if (row[q1] != q1) continue;
            for (int c = 0; c < N; c++) if (row[c] < mn[c]) mn[c] = row[c];
        }
        for (int c = 0; c < N; c++) if (mn[c] == c) { pr1[npairs] = q1; pr2[npairs] = c; npairs++; }
    }
}
// plain recursion, straight from the definition
static int Urec(const int *codes, int n, const int *q, int j, int level) {
    if (level == j) return n > 0 ? n - 1 : 0;
    int cnt[14] = {0};
    int *buf = malloc(sizeof(int) * 14 * (size_t)n);
    const uint8_t *row = A[q[level]];
    for (int i = 0; i < n; i++) { int a = row[codes[i]]; buf[a * n + cnt[a]++] = codes[i]; }
    int sum = 0;
    for (int a = 0; a < 14; a++) if (cnt[a]) sum += Urec(buf + a * n, cnt[a], q, j, level + 1);
    free(buf);
    if (level == 0) return sum;
    return sum > 1 ? sum - 1 : 0;
}
static int Ulist(const int *q, int j) {
    // set the questions aside explicitly
    int codes[N], n = 0;
    for (int c = 0; c < N; c++) { int isq = 0; for (int i = 0; i < j; i++) if (q[i] == c) isq = 1; if (!isq) codes[n++] = c; }
    if (j == 0) return n;
    return Urec(codes, n, q, j, 0);
}
static void pr(int c, char *s) { for (int p = 0; p < 4; p++) s[p] = '1' + D[c][p]; s[4] = 0; }

// fast structure for a triple
static int L[N], cstart[N], csize[N], cend2[N], cend1[N], ncl;
static int build3(int q1, int q2, int q3) { // returns floor (lower bound over all q4)
    static int cnt[2744 + 1], key[N], pos[2744 + 1], ord[N];
    memset(cnt, 0, sizeof(cnt));
    for (int c = 0; c < N; c++) { key[c] = (A[q1][c] * 14 + A[q2][c]) * 14 + A[q3][c]; cnt[key[c]]++; }
    int s = 0; for (int k = 0; k < 2744; k++) { pos[k] = s; s += cnt[k]; }
    for (int c = 0; c < N; c++) ord[pos[key[c]]++] = c;
    ncl = 0; int nl = 0, at = 0, lastk = -1;
    int fl = 0, s2 = 0, s1 = 0;
    for (int k = 0; k < 2744; k++) {
        int sz = cnt[k];
        if (sz >= 3) {
            if (lastk >= 0) {
                cend2[ncl - 1] = (lastk / 14 != k / 14);
                cend1[ncl - 1] = (lastk / 196 != k / 196);
            }
            cstart[ncl] = nl; csize[ncl] = sz;
            for (int i = 0; i < sz; i++) L[nl++] = ord[at + i];
            ncl++; lastk = k;
        }
        at += sz;
    }
    if (ncl) { cend2[ncl - 1] = 1; cend1[ncl - 1] = 1; }
    for (int k = 0; k < ncl; k++) {
        int sz = csize[k]; int f3 = sz - (sz < 14 ? sz : 14) - 1; if (f3 > 0) s2 += f3;
        if (cend2[k]) { if (s2 > 1) s1 += s2 - 1; s2 = 0; }
        if (cend1[k]) { if (s1 > 1) fl += s1 - 1; s1 = 0; }
    }
    return fl;
}
static inline int U4fast(int q4, int cap) {
    const uint8_t *row = A[q4];
    int U = 0, s2 = 0, s1 = 0;
    for (int k = 0; k < ncl; k++) {
        unsigned mask = 0; const int *p = L + cstart[k]; int sz = csize[k];
        for (int i = 0; i < sz; i++) mask |= 1u << row[p[i]];
        int f3 = sz - __builtin_popcount(mask) - 1; if (f3 > 0) s2 += f3;
        if (cend2[k]) { if (s2 > 1) s1 += s2 - 1; s2 = 0; }
        if (cend1[k]) { if (s1 > 1) { U += s1 - 1; if (U > cap) return U; } s1 = 0; }
    }
    return U;
}
static int code_of(const char *s) { int x = 0; for (int p = 0; p < 4; p++) x = x * 6 + (s[p] - '1'); return x; }

int main(int argc, char **argv) {
    init();
    if (argc < 2) return 1;
    char s1[5], s2[5], s3[5], s4[5];
    if (!strcmp(argv[1], "list")) {
        int q[16], j = argc - 2;
        for (int i = 0; i < j; i++) q[i] = code_of(argv[2 + i]);
        for (int jj = 1; jj <= j; jj++) printf("U(first %d of the list) = %d\n", jj, Ulist(q, jj));
        return 0;
    }
    group();
    if (!strcmp(argv[1], "small")) {
        printf("group order %d, orbits of single codes %d, orbits of ordered pairs %d\n", NG, nreps, npairs);
        int best = 1 << 30, bq[3] = {0, 0, 0}; long nb = 0;
        for (int i = 0; i < nreps; i++) { int q[1] = {reps[i]}; int u = Ulist(q, 1); pr(q[0], s1); printf("  U(%s) = %d\n", s1, u); if (u < best) { best = u; bq[0] = q[0]; } }
        pr(bq[0], s1); printf("m(1) = %d  at %s  (complete: 5 orbit representatives)\n", best, s1);
        best = 1 << 30;
        for (int i = 0; i < npairs; i++) { int q[2] = {pr1[i], pr2[i]}; int u = Ulist(q, 2); if (u < best) { best = u; bq[0] = q[0]; bq[1] = q[1]; nb = 0; } if (u == best) nb++; }
        pr(bq[0], s1); pr(bq[1], s2); printf("m(2) = %d  at %s %s  (complete: %d orbits of ordered pairs; %ld orbits attain it)\n", best, s1, s2, npairs, nb);
        // cross-check m(2) without pair symmetry: 5 reps x all 1296
        int best2 = 1 << 30;
        for (int i = 0; i < nreps; i++) for (int c = 0; c < N; c++) { int q[2] = {reps[i], c}; int u = Ulist(q, 2); if (u < best2) best2 = u; }
        printf("   check, 5 x 1296 ordered pairs without the pair symmetry: min %d\n", best2);
        best = 1 << 30; nb = 0;
        for (int i = 0; i < npairs; i++) for (int c = 0; c < N; c++) { int q[3] = {pr1[i], pr2[i], c}; int u = Ulist(q, 3); if (u < best) { best = u; bq[0] = q[0]; bq[1] = q[1]; bq[2] = q[2]; nb = 0; } if (u == best) nb++; }
        pr(bq[0], s1); pr(bq[1], s2); pr(bq[2], s3);
        printf("m(3) = %d  at %s %s %s  (complete: %d pair orbits x 1296 third questions = %ld ordered triples; %ld of them attain it)\n", best, s1, s2, s3, npairs, (long)npairs * N, nb);
        return 0;
    }
    if (!strcmp(argv[1], "check")) {
        int n = atoi(argv[2]); srand(12345); int bad = 0;
        for (int t = 0; t < n; t++) {
            int q[4]; for (int i = 0; i < 4; i++) q[i] = rand() % N;
            if (t % 5 == 0) q[3] = q[rand() % 3];
            if (t % 7 == 0) q[1] = q[0];
            build3(q[0], q[1], q[2]);
            int a = U4fast(q[3], 1 << 30), b = Ulist(q, 4);
            if (a != b) { bad++; if (bad < 5) printf("MISMATCH %d %d\n", a, b); }
        }
        printf("fast inner loop against plain recursion on %d random quadruples: %d mismatches\n", n, bad);
        return 0;
    }
    if (!strcmp(argv[1], "four")) {
        int r = atoi(argv[2]), k = atoi(argv[3]);
        int usefloor = argc > 4 ? atoi(argv[4]) : 0;
        int best = 1 << 30, bq[4] = {0, 0, 0, 0}; long nb = 0, ntrip = 0, nskip = 0, nquad = 0;
        int minfloor = 1 << 30;
        for (int i = 0; i < npairs; i++) {
            if (i % k != r) continue;
            for (int q3 = 0; q3 < N; q3++) {
                int fl = build3(pr1[i], pr2[i], q3);
                ntrip++;
                if (fl < minfloor) minfloor = fl;
                if (usefloor && fl > best) { nskip++; continue; }
                for (int q4 = 0; q4 < N; q4++) {
                    int u = U4fast(q4, best);
                    nquad++;
                    if (u < best) { best = u; bq[0] = pr1[i]; bq[1] = pr2[i]; bq[2] = q3; bq[3] = q4; nb = 0; }
                    if (u == best) nb++;
                }
            }
        }
        pr(bq[0], s1); pr(bq[1], s2); pr(bq[2], s3); pr(bq[3], s4);
        printf("part %d of %d: min U = %d at %s %s %s %s ; %ld quadruples attain it in this part; triples %ld, skipped by floor %ld, quadruples evaluated %ld, least triple floor %d\n",
               r, k, best, s1, s2, s3, s4, nb, ntrip, nskip, nquad, minfloor);
        return 0;
    }
    return 1;
}
