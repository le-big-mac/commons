/* enum.c -- every circle of an integral Apollonian packing with curvature at most N, by walking the Apollonian group
   from the root quadruple (Graham, Lagarias, Mallows, Wilks, Yan 2003, Theorem 3.3: each circle not in the root
   quadruple is the new, largest entry of S_in ... S_i1 v for exactly one reduced word).  S_i replaces the i-th
   curvature by twice the sum of the other three less itself.  Marks which curvatures occur.
   usage: enum a b c d N [out]     writes "out" (default: none) with one missing curvature a line: a positive integer n <= N
                                   whose residue modulo 24 occurs in the packing and which is not itself a curvature.
   With out = "-" nothing is listed, only the count of circles and the time.
   The strip packing (0,0,1,1) has infinitely many circles of curvature 1; there the two moves of the root that give
   another circle of curvature 1 are left out, which loses no curvature (the packing repeats along the strip). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
static int64_t N; static uint8_t *bits; static uint64_t circles = 0, maxdepth = 0;
static inline void mark(int64_t c) { if (c > 0 && c <= N) bits[c >> 3] |= (uint8_t)(1u << (c & 7)); }
static void walk(int64_t q0, int64_t q1, int64_t q2, int64_t q3, int last, uint64_t depth) {
  int64_t q[4] = { q0, q1, q2, q3 }, s = q0 + q1 + q2 + q3; if (depth > maxdepth) maxdepth = depth;
  for (int i = 0; i < 4; i++) { if (i == last) continue;
    int64_t nw = 2 * (s - q[i]) - q[i]; if (nw > N) continue;
    if (last < 0 && nw <= q[i] && q[i] == 1 && q0 == 0 && q1 == 0) continue;        /* the strip: a translate of a unit circle */
    circles++; mark(nw); int64_t old = q[i]; q[i] = nw; walk(q[0], q[1], q[2], q[3], i, depth + 1); q[i] = old; }
}
int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: enum a b c d N [out]\n"); return 2; }
  int64_t q[4]; for (int i = 0; i < 4; i++) q[i] = atoll(argv[1 + i]); N = atoll(argv[5]);
  int64_t s = q[0] + q[1] + q[2] + q[3], sq = q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3];
  if (s * s != 2 * sq || s <= 0) { fprintf(stderr, "not a Descartes quadruple\n"); return 2; }
  bits = calloc((size_t)(N >> 3) + 2, 1); clock_t t0 = clock();
  for (int i = 0; i < 4; i++) { mark(q[i]); circles++; }
  walk(q[0], q[1], q[2], q[3], -1, 0);
  double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
  int res[24] = { 0 }; int64_t present = 0; for (int64_t c = 1; c <= N; c++) if (bits[c >> 3] & (1u << (c & 7))) { res[c % 24] = 1; present++; }
  printf("packing (%lld, %lld, %lld, %lld), curvatures up to %lld: %llu circles, %lld different curvatures, deepest word %llu, %.1f s\n", (long long)q[0], (long long)q[1], (long long)q[2], (long long)q[3], (long long)N, (unsigned long long)circles, (long long)present, (unsigned long long)maxdepth, secs);
  printf("residues modulo 24 that occur:"); int nres = 0; for (int r = 0; r < 24; r++) if (res[r]) { printf(" %d", r); nres++; } printf("  (%d classes)\n", nres);
  if (argc > 6 && strcmp(argv[6], "-") != 0) { FILE *f = fopen(argv[6], "w"); int64_t miss = 0; int64_t per[24] = { 0 };
    for (int64_t c = 1; c <= N; c++) if (res[c % 24] && !(bits[c >> 3] & (1u << (c & 7)))) { fprintf(f, "%lld\n", (long long)c); miss++; per[c % 24]++; }
    fclose(f); printf("missing (admissible modulo 24 and absent): %lld, written to %s; by residue:", (long long)miss, argv[6]); for (int r = 0; r < 24; r++) if (res[r]) printf(" %d:%lld", r, (long long)per[r]); printf("\n"); }
  return 0;
}
