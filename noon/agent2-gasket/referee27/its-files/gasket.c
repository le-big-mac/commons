/* Referee's own enumerator of an Apollonian gasket from the Descartes swap rule.
   usage: gasket a b c d N outfile
   Writes uint32 counts[0..N] : number of circles with each curvature k, 0<=k<=N.
   Prints the number of circles with negative curvature and the total.
   Each circle other than the four of the starting quadruple is created exactly once:
   by a swap that does not undo the swap that made the quadruple it is applied to. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t N;
static uint32_t *cnt;
static uint64_t total = 0;
static int maxdepth = 0;

/* d is the circle just created; never swap it back. */
static void rec(int64_t a, int64_t b, int64_t c, int64_t d, int depth) {
    int64_t s = a + b + c + d;
    int64_t n;
    if (depth > maxdepth) maxdepth = depth;
    n = 2 * (s - a) - a;
    if (n <= N && n > a) { cnt[n]++; total++; rec(b, c, d, n, depth + 1); }
    n = 2 * (s - b) - b;
    if (n <= N && n > b) { cnt[n]++; total++; rec(a, c, d, n, depth + 1); }
    n = 2 * (s - c) - c;
    if (n <= N && n > c) { cnt[n]++; total++; rec(a, b, d, n, depth + 1); }
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage\n"); return 2; }
    int64_t q[4];
    for (int i = 0; i < 4; i++) q[i] = atoll(argv[1 + i]);
    N = atoll(argv[5]);
    int64_t s = q[0] + q[1] + q[2] + q[3];
    if (s * s != 2 * (q[0]*q[0] + q[1]*q[1] + q[2]*q[2] + q[3]*q[3])) { fprintf(stderr, "not Descartes\n"); return 3; }
    cnt = calloc(N + 1, sizeof(uint32_t));
    uint64_t neg = 0;
    int strip = (q[0] == 0 && q[1] == 0) || (q[0]==0&&q[2]==0) || (q[0]==0&&q[3]==0) || (q[1]==0&&q[2]==0)||(q[1]==0&&q[3]==0)||(q[2]==0&&q[3]==0);
    for (int i = 0; i < 4; i++) {
        if (q[i] < 0) neg++;
        else if (q[i] <= N) { cnt[q[i]]++; }
        total++;
    }
    int eqroot = 0, notroot = 0;
    for (int i = 0; i < 4; i++) {
        int64_t n = 2 * (s - q[i]) - q[i];
        int64_t o[3]; int k = 0;
        for (int j = 0; j < 4; j++) if (j != i) o[k++] = q[j];
        if (n < q[i]) { notroot = 1; continue; }
        if (n == q[i]) {
            eqroot++;
            if (strip) continue;   /* strip packing: the equal swap is a translation, infinitely many; skip */
        }
        if (n <= N) { cnt[n]++; total++; rec(o[0], o[1], o[2], n, 1); }
    }
    FILE *f = fopen(argv[6], "wb");
    if (argc > 7) { /* byte mode: counts saturated at 255 */
        uint8_t *b = malloc(N + 1);
        for (int64_t i = 0; i <= N; i++) b[i] = cnt[i] > 255 ? 255 : cnt[i];
        fwrite(b, 1, N + 1, f);
    } else fwrite(cnt, sizeof(uint32_t), N + 1, f);
    fclose(f);
    printf("quad %lld %lld %lld %lld N %lld neg %llu total_circles %llu eqroot %d notroot %d strip %d maxdepth %d\n",
           (long long)q[0], (long long)q[1], (long long)q[2], (long long)q[3], (long long)N,
           (unsigned long long)neg, (unsigned long long)total, eqroot, notroot, strip, maxdepth);
    return 0;
}
