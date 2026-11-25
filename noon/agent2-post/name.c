// Mastermind by post, the second sheet: after j blind questions, letters can only name codes, one for each state of knowledge.
// m(j) is the least number of codes left unnamed by the best tree of j rounds of naming (the first round knows answer 1, the
// last knows answers 1 to j), over every choice of the j questions; the questions' own codes count as sent.
// usage: name n k j [-b BEST] < prefixes      each line: j-1 codes (numbers from 0, base k); every code is tried as the j-th question.
//        name n k j -full < tuples            each line: j codes; just evaluate them.
//        name n k j -floors < prefixes        print the floor of each prefix (the bound by which it may be passed over) and nothing else.
// Output: a line for each prefix whose best beats or equals the best so far, then "# least ...".
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 1296
static int n, k, N, F, J;
static uint8_t fb[MAXN][MAXN];
static void maketable(void) {
  static int dig[MAXN][8]; int id[64]; memset(id, -1, sizeof id); F = 0;
  for (int c = 0; c < N; c++) { int v = c; for (int j = n - 1; j >= 0; j--) { dig[c][j] = v % k; v /= k; } }
  for (int g = 0; g < N; g++) for (int s = 0; s < N; s++) {
    int b = 0, cg[16] = {0}, cs[16] = {0}, tot = 0;
    for (int j = 0; j < n; j++) { if (dig[g][j] == dig[s][j]) b++; cg[dig[g][j]]++; cs[dig[s][j]]++; }
    for (int c = 0; c < k; c++) tot += cg[c] < cs[c] ? cg[c] : cs[c];
    int key = b * (n + 1) + (tot - b); if (id[key] < 0) id[key] = F++; fb[g][s] = (uint8_t)id[key];
  }
}
// The codes of S share the first `level` answers. One code is named here; then the next answer splits them.
// Returns how many of S are left unnamed in the end. `stop`: give up (return something large) once the count passes it.
static int unnamed(const int16_t *S, int m, const int16_t *g, int level, int j) {
  if (level == j) return m > 0 ? m - 1 : 0;
  int cn[32] = {0}, at[33], fill[32]; int16_t T[MAXN]; const uint8_t *row = fb[g[level]];
  for (int i = 0; i < m; i++) cn[row[S[i]]]++;
  at[0] = 0; for (int f = 0; f < F; f++) { at[f + 1] = at[f] + cn[f]; fill[f] = at[f]; }
  for (int i = 0; i < m; i++) T[fill[row[S[i]]]++] = S[i];
  int t = 0; for (int f = 0; f < F; f++) if (cn[f]) t += unnamed(T + at[f], cn[f], g, level + 1, j);
  return t > 0 ? t - 1 : 0;
}
// All the codes but the questions themselves, split by the first answer; the total left unnamed.
static int total(const int16_t *g, int j) {
  int16_t S[MAXN]; int m = 0;
  for (int c = 0; c < N; c++) { int is = 0; for (int i = 0; i < j; i++) if (g[i] == c) is = 1; if (!is) S[m++] = (int16_t)c; }
  int cn[32] = {0}, at[33], fill[32]; int16_t T[MAXN]; const uint8_t *row = fb[g[0]];
  for (int i = 0; i < m; i++) cn[row[S[i]]]++;
  at[0] = 0; for (int f = 0; f < F; f++) { at[f + 1] = at[f] + cn[f]; fill[f] = at[f]; }
  for (int i = 0; i < m; i++) T[fill[row[S[i]]]++] = S[i];
  int t = 0; for (int f = 0; f < F; f++) if (cn[f]) t += unnamed(T + at[f], cn[f], g, 1, j);
  return t;
}
// A floor on total() over every choice of the last question, from the first j-1 alone: a set of s codes that share j-1 answers
// is cut by one more answer into at most F parts, so at least s - F of them are left over before its own naming and the last round's.
static int floor_unnamed(const int16_t *S, int m, const int16_t *g, int level, int j) {
  if (level == j - 1) { int left = m - F; left = left > 0 ? left : 0; return left > 0 ? left - 1 : 0; }   // last round names up to F, this level 1
  int cn[32] = {0}, at[33], fill[32]; int16_t T[MAXN]; const uint8_t *row = fb[g[level]];
  for (int i = 0; i < m; i++) cn[row[S[i]]]++;
  at[0] = 0; for (int f = 0; f < F; f++) { at[f + 1] = at[f] + cn[f]; fill[f] = at[f]; }
  for (int i = 0; i < m; i++) T[fill[row[S[i]]]++] = S[i];
  int t = 0; for (int f = 0; f < F; f++) if (cn[f]) t += floor_unnamed(T + at[f], cn[f], g, level + 1, j);
  return t > 0 ? t - 1 : 0;
}
static int floor_total(const int16_t *g, int j) {
  int16_t S[MAXN]; int m = 0; for (int c = 0; c < N; c++) S[m++] = (int16_t)c;       // the questions themselves are left in: a floor may be loose
  if (j == 1) return 0;
  int cn[32] = {0}, at[33], fill[32]; int16_t T[MAXN]; const uint8_t *row = fb[g[0]];
  for (int i = 0; i < m; i++) cn[row[S[i]]]++;
  at[0] = 0; for (int f = 0; f < F; f++) { at[f + 1] = at[f] + cn[f]; fill[f] = at[f]; }
  for (int i = 0; i < m; i++) T[fill[row[S[i]]]++] = S[i];
  int t = 0; for (int f = 0; f < F; f++) if (cn[f]) t += floor_unnamed(T + at[f], cn[f], g, 1, j);
  return t - j > 0 ? t - j : 0;                                                       // at most j of those counted were questions
}
static void codestr(int c, char *out) { for (int j = n - 1; j >= 0; j--) { out[j] = '1' + c % k; c /= k; } out[n] = 0; }
int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: name n k j [-b BEST] [-full] < prefixes\n"); return 2; }
  n = atoi(argv[1]); k = atoi(argv[2]); J = atoi(argv[3]); int best = 1 << 30, full = 0, floors = 0;
  for (int i = 4; i < argc; i++) { if (!strcmp(argv[i], "-b")) best = atoi(argv[++i]); else if (!strcmp(argv[i], "-full")) full = 1; else if (!strcmp(argv[i], "-floors")) floors = 1; }
  N = 1; for (int j = 0; j < n; j++) N *= k; if (N > MAXN || J < 1 || J > 8) return 2;
  maketable();
  char line[4096]; long prefixes = 0, skipped = 0, tried = 0, atbest = 0; int16_t bestg[8] = {0}; int found = 0;
  while (fgets(line, sizeof line, stdin)) {
    int16_t g[8]; int L = 0; char *tok = strtok(line, " \t\r\n");
    while (tok && L < 8) { g[L++] = (int16_t)atoi(tok); tok = strtok(NULL, " \t\r\n"); }
    if (L != (full ? J : J - 1)) { fprintf(stderr, "a line with %d codes where %d are wanted\n", L, full ? J : J - 1); return 2; }
    prefixes++;
    if (floors) { printf("%d\n", floor_total(g, J)); continue; }                       // -floors: only print each prefix's floor
    if (!full && J > 1 && floor_total(g, J) > best) { skipped++; continue; }
    int lo = full ? g[J - 1] : 0, hi = full ? g[J - 1] : N - 1, mine = 1 << 30, arg = -1;
    for (int c = lo; c <= hi; c++) { g[J - 1] = (int16_t)c; int t = total(g, J); tried++; if (t < mine) { mine = t; arg = c; } if (t < best) atbest = 0; if (t <= best) { if (t < best) { best = t; } atbest++; memcpy(bestg, g, sizeof bestg); bestg[J - 1] = (int16_t)c; found = 1; } }
    if (mine <= best) { g[J - 1] = (int16_t)arg; printf("%d", mine); for (int i = 0; i < J; i++) { char cs[16]; codestr(g[i], cs); printf(" %s", cs); } printf("\n"); fflush(stdout); }
  }
  printf("# least %d", best); if (found) for (int i = 0; i < J; i++) { char cs[16]; codestr(bestg[i], cs); printf(" %s", cs); }
  printf(" ; questions j=%d; prefixes %ld, skipped by the floor %ld, lists tried %ld, lists at the least %ld\n", J, prefixes, skipped, tried, atbest);
  return 0;
}
