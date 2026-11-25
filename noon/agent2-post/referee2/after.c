// Referee, after reading: checks on Noon's list of triples, on name.c's floor, and on the floor's soundness.
#define main blind_main
#include "blind.c"
#undef main
static int cmpll(const void *a, const void *b) { long long x = *(const long long *)a, y = *(const long long *)b; return x < y ? -1 : x > y; }
int main(int argc, char **argv) {
    init(); group();
    if (!strcmp(argv[1], "tri")) {
        // Burnside: orbits of ordered j-lists = sum_g fix(g)^j / |G|
        double s1 = 0, s2 = 0, s3 = 0;
        for (int g = 0; g < NG; g++) { long f = 0; for (int c = 0; c < N; c++) if (IMG[(size_t)g * N + c] == c) f++; s1 += f; s2 += (double)f * f; s3 += (double)f * f * f; }
        printf("Burnside: orbits of ordered singles %.0f, pairs %.0f, triples %.0f\n", s1 / NG, s2 / NG, s3 / NG);
        FILE *fp = fopen(argv[2], "r"); int a, b, c; long nt = 0; long long *canon = malloc(sizeof(long long) * 200000);
        long above25 = 0, above24 = 0, eq25 = 0, rep = 0;
        while (fscanf(fp, "%d %d %d", &a, &b, &c) == 3) {
            long long mn = -1;
            for (int g = 0; g < NG; g++) { const uint16_t *row = IMG + (size_t)g * N; long long v = ((long long)row[a] * N + row[b]) * N + row[c]; if (mn < 0 || v < mn) mn = v; }
            canon[nt++] = mn;
            int t = build3(a, b, c); int fl = t - 4 > 0 ? t - 4 : 0;   // name.c's floor_total for j = 4
            if (fl > 25) above25++; if (fl > 24) above24++; if (fl == 25) eq25++;
            if (a == b || a == c || b == c) rep++;
        }
        qsort(canon, nt, sizeof(long long), cmpll); long distinct = nt ? 1 : 0; for (long i = 1; i < nt; i++) if (canon[i] != canon[i - 1]) distinct++;
        printf("file %s: %ld triples, %ld distinct orbits of ordered triples; %ld have a repeated code\n", argv[2], nt, distinct, rep);
        printf("name.c's floor (recomputed here): above 25 for %ld triples, exactly 25 for %ld, above 24 for %ld\n", above25, eq25, above24);
        return 0;
    }
    if (!strcmp(argv[1], "sound")) {
        int r = atoi(argv[2]), k = atoi(argv[3]); long ntrip = 0, viol = 0, viol1 = 0, le25 = 0, le25skipped = 0; int best = 1 << 30, gap = 1 << 30;
        for (int i = 0; i < npairs; i++) { if (i % k != r) continue;
            for (int q3 = 0; q3 < N; q3++) {
                int t = build3(pr1[i], pr2[i], q3); int fl = t - 4 > 0 ? t - 4 : 0; int mn = 1 << 30;
                for (int q4 = 0; q4 < N; q4++) { int u = U4fast(q4, 1 << 30); if (u < mn) mn = u; }
                ntrip++; if (mn < fl) viol++; if (mn < t - 1) viol1++; if (mn - fl < gap) gap = mn - fl; if (mn < best) best = mn;
                if (mn <= 25) { le25++; if (fl > 25) le25skipped++; }
            } }
        printf("part %d of %d: %ld ordered triples; least over the fourth question below name.c's floor: %ld times (below the tighter t-1: %ld); smallest (least - floor) %d; triples whose best fourth gives 25 or less: %ld, of which with floor above 25: %ld; least %d\n", r, k, ntrip, viol, viol1, gap, le25, le25skipped, best);
        return 0;
    }
    return 1;
}
