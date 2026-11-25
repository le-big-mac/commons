// A second count of the openings that work at a lag of 3, written apart from lag.c: plain loops, no bit sets, no general search.
// For each blind pair (g1, g2) read from standard input and every two further blind guesses g3 < g4: is there, for each answer to g1,
// a fifth guess such that the answers to g2, g3, g4 and the fifth tell apart all the codes that give g1 that answer?
// usage: k3check < pairs      (code numbers from 0, base 6, first peg most significant)     Prints "yes g1 g2 g3 g4" for each that works.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 1296
static unsigned char fb[N][N]; static int F = 0;
static void table(void) {
  int dig[N][4], id[32]; memset(id, -1, sizeof id);
  for (int c = 0; c < N; c++) { int v = c; for (int j = 3; j >= 0; j--) { dig[c][j] = v % 6; v /= 6; } }
  for (int g = 0; g < N; g++) for (int s = 0; s < N; s++) {
    int b = 0, cg[6] = {0}, cs[6] = {0}, tot = 0;
    for (int j = 0; j < 4; j++) { if (dig[g][j] == dig[s][j]) b++; cg[dig[g][j]]++; cs[dig[s][j]]++; }
    for (int c = 0; c < 6; c++) tot += cg[c] < cs[c] ? cg[c] : cs[c];
    int key = b * 5 + (tot - b); if (id[key] < 0) id[key] = F++; fb[g][s] = (unsigned char)id[key];
  }
}
static void name(int c, char *o) { for (int j = 3; j >= 0; j--) { o[j] = '1' + c % 6; c /= 6; } o[4] = 0; }
int main(void) {
  table(); if (F != 14) return 3;
  static int stamp[14 * 14 * 14 * 14 * 14], gen = 0; static int cnt[14 * 14 * 14 * 14];
  int g1, g2; long tried = 0, yes = 0, passed = 0;
  while (scanf("%d %d", &g1, &g2) == 2) {
    int grp[14][N], gn[14] = {0}, order[14];
    for (int s = 0; s < N; s++) grp[fb[g1][s]][gn[fb[g1][s]]++] = s;                    // the codes by their answer to g1
    for (int f = 0; f < 14; f++) order[f] = f;
    for (int a = 0; a < 14; a++) for (int b = a + 1; b < 14; b++) if (gn[order[b]] > gn[order[a]]) { int t = order[a]; order[a] = order[b]; order[b] = t; }   // largest first
    for (int g3 = 0; g3 < N; g3++) for (int g4 = g3 + 1; g4 < N; g4++) {
      tried++;
      int k4[N], big = 0;                                                               // each code's answers to g1..g4 as one number
      for (int s = 0; s < N; s++) k4[s] = ((fb[g1][s] * 14 + fb[g2][s]) * 14 + fb[g3][s]) * 14 + fb[g4][s];
      for (int s = 0; s < N; s++) cnt[k4[s]] = 0;
      for (int s = 0; s < N; s++) if (++cnt[k4[s]] > 14) { big = 1; break; }            // a fifth answer has 14 values at most
      if (big) continue;
      passed++;
      int ok = 1;
      for (int a = 0; a < 14 && ok; a++) {
        int f = order[a], m = gn[f], found = 0; if (m <= 1) continue;
        for (int g5 = 0; g5 < N && !found; g5++) {
          gen++; int clash = 0;
          for (int i = 0; i < m && !clash; i++) { int s = grp[f][i], key = (k4[s] % 2744) * 14 + fb[g5][s]; if (stamp[key] == gen) clash = 1; else stamp[key] = gen; }
          if (!clash) found = 1;
        }
        if (!found) ok = 0;
      }
      if (ok) { char a[5], b[5], c[5], d[5]; name(g1, a); name(g2, b); name(g3, c); name(g4, d); printf("yes %s %s %s %s\n", a, b, c, d); fflush(stdout); yes++; }
    }
  }
  printf("# %ld openings tried, %ld with no set of more than 14 left by the four answers, %ld work\n", tried, passed, yes);
  return 0;
}
