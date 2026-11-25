/* Referee's ruler: plain recursion from the definitions, any lag D, any T,
 * no symmetry, no bounds (one exception, marked), for small games.
 * usage: ruler K|W D T      (compile with -DP= -DC=)
 * State: about to send guess t; S = codes consistent with the answers that
 * have ARRIVED (answers to guesses 1..t-1-D); pend = guesses sent whose
 * answers have not arrived.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef P
#define P 2
#endif
#ifndef C
#define C 8
#endif
#define MAXN 1296
static int N, NA, D, T, modeW, FULL;
static unsigned char A[MAXN][MAXN];
static int dig[MAXN][P];
static long long calls = 0;

static void init(void) {
    int amap[P + 1][P + 1];
    N = 1; for (int p = 0; p < P; p++) N *= C;
    NA = 0;
    for (int b = 0; b <= P; b++) for (int w = 0; w + b <= P; w++) amap[b][w] = NA++;
    FULL = amap[P][0];
    for (int i = 0; i < N; i++) { int x = i; for (int p = 0; p < P; p++) { dig[i][p] = x % C; x /= C; } }
    for (int g = 0; g < N; g++) for (int c = 0; c < N; c++) {
        int b = 0, tot = 0;
        for (int p = 0; p < P; p++) if (dig[g][p] == dig[c][p]) b++;
        for (int q = 0; q < C; q++) {
            int x = 0, y = 0;
            for (int p = 0; p < P; p++) { x += dig[g][p] == q; y += dig[c][p] == q; }
            tot += x < y ? x : y;
        }
        A[g][c] = (unsigned char)amap[b][tot - b];
    }
}

static int win(int t, const int *S, int n, const int *pend, int np) {
    calls++;
    if (t > T) {
        if (!modeW) {
            for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) {
                int same = 1;
                for (int k = 0; k < np && same; k++) if (A[pend[k]][S[i]] != A[pend[k]][S[j]]) same = 0;
                if (same) return 0;
            }
            return 1;
        } else {
            for (int i = 0; i < n; i++) { int in = 0; for (int k = 0; k < np; k++) if (pend[k] == S[i]) in = 1; if (!in) return 0; }
            return 1;
        }
    }
    if (modeW && t == T) {
        /* the one shortcut: the last guess can add at most one code */
        int left = 0;
        for (int i = 0; i < n; i++) { int in = 0; for (int k = 0; k < np; k++) if (pend[k] == S[i]) in = 1; if (!in) left++; }
        return left <= 1;
    }
    int pend2[16]; memcpy(pend2, pend, sizeof(int) * np);
    int *buf = malloc(sizeof(int) * (n + 1));
    for (int g = 0; g < N; g++) {
        pend2[np] = g;
        int ok;
        if (np + 1 > D) {
            int g0 = pend2[0];
            ok = 1;
            for (int a = 0; a < NA && ok; a++) {
                int m = 0;
                for (int i = 0; i < n; i++) if (A[g0][S[i]] == a) buf[m++] = S[i];
                if (m == 0) continue;
                if (modeW && a == FULL) continue;
                if (!win(t + 1, buf, m, pend2 + 1, np)) ok = 0;
            }
        } else ok = win(t + 1, S, n, pend2, np + 1);
        if (ok) { free(buf); return 1; }
    }
    free(buf);
    return 0;
}

int main(int argc, char **argv) {
    modeW = argv[1][0] == 'W'; D = atoi(argv[2]); T = atoi(argv[3]);
    init();
    static int S[MAXN]; for (int i = 0; i < N; i++) S[i] = i;
    int pend[16];
    int r = win(1, S, N, pend, 0);
    printf("ruler P=%d C=%d %s lag=%d T=%d: %s (calls %lld)\n", P, C, modeW ? "W" : "K", D, T, r ? "YES" : "NO", calls);
    return 0;
}
