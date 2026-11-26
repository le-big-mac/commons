// Exhaustive enumeration of all multisets on Z_M that contain hour 0, of size <= S.
// (Any nonempty multiset is a turn of one containing hour 0, and turning does not change where it balances.)
// For each multiset the exact remainders of sum A(x) X^x modulo every Phi_d (d | M, d > 1) are kept as
// small integers; "balance at d" is "the remainder modulo Phi_d is zero". Records, for each pattern,
// the least size at which it occurs and one multiset of that size.
// usage: enum table.txt S job njobs
#include <immintrin.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static __m256i vec[32];
static uint32_t seg[8];
static int ndiv, M, S, job, njobs, dv[8];
static int best[256];
static uint8_t wit[256][40];
static uint8_t cur[64];
static unsigned long long nodes, counter;
#define SPLIT 6
static inline int pat_of(__m256i v) {
    uint32_t nz = ~(uint32_t)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v, _mm256_setzero_si256()));
    int pat = 0;
    for (int i = 0; i < ndiv; i++) if (!(nz & seg[i])) pat |= 1 << i;
    return pat;
}
static void dfs(__m256i v, int start, int depth) {
    for (int h = start; h < M; h++) {
        if (depth == SPLIT) { if ((counter++) % njobs != (unsigned long long)job) continue; }
        __m256i w = _mm256_add_epi8(v, vec[h]);
        int pat = pat_of(w);
        if (depth >= SPLIT || job == 0) nodes++;
        if (depth + 1 < best[pat]) { best[pat] = depth + 1; cur[depth] = h; memcpy(wit[pat], cur, depth + 1); }
        if (depth + 1 < S) { cur[depth] = h; dfs(w, h, depth + 1); }
    }
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); S = atoi(argv[2]); job = atoi(argv[3]); njobs = atoi(argv[4]);
    int mx; if (fscanf(f, "%d %d %d", &M, &ndiv, &mx) != 3) return 1;
    if (mx * S > 127 || M > 32 || ndiv > 8 || S > 40) { fprintf(stderr, "out of range\n"); return 1; }
    int pos = 0;
    for (int i = 0; i < ndiv; i++) { int phi; if (fscanf(f, "%d %d", &dv[i], &phi) != 2) return 1;
        seg[i] = 0; for (int j = 0; j < phi; j++) seg[i] |= 1u << (pos + j); pos += phi; }
    for (int h = 0; h < M; h++) { int8_t b[32]; memset(b, 0, 32);
        for (int j = 0; j < M - 1; j++) { int x; if (fscanf(f, "%d", &x) != 1) return 1; b[j] = (int8_t)x; }
        vec[h] = _mm256_loadu_si256((__m256i *)b); }
    for (int i = 0; i < 256; i++) best[i] = 1000;
    // first mark at hour 0
    __m256i v = vec[0]; cur[0] = 0; int pat = pat_of(v);
    if (job == 0) nodes++;
    best[pat] = 1; wit[pat][0] = 0;
    if (S > 1) dfs(v, 0, 1);
    printf("M %d S %d job %d/%d nodes %llu\n", M, S, job, njobs, nodes);
    for (int p = 0; p < (1 << ndiv); p++) if (best[p] < 1000) {
        printf("pat"); for (int i = 0; i < ndiv; i++) if (p >> i & 1) printf(" %d", dv[i]);
        printf(" | size %d | marks", best[p]); for (int j = 0; j < best[p]; j++) printf(" %d", wit[p][j]); printf("\n"); }
    return 0;
}
