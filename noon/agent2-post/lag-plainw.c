// lag-plainw.c: lag.c with the bounds and the pair bit sets taken out; in W a guess too late to be answered in time is still tried only
// if it may be the code. Made by plain.py from lag.c.
// Mastermind with late answers. The answer to guess i arrives only after guess i+d has been sent.
// Question K: can the codebreaker always determine the code with Q guesses, once all their answers are in?
// Question W: can the codebreaker always have sent the code itself among the first Q guesses?
//
// usage: lag n k d Q mode [options] < openings
//   mode K or W.  Each line of standard input is a blind opening: code numbers (from 0, base k, first peg most significant), possibly none.
//   options: -x E   extend each opening by E more blind guesses, tried as increasing sets (only valid when those guesses are interchangeable)
//            -a     do not stop at the first opening that works; report every opening
//            -s     print the strategy found for the first opening that works
//            -q     quiet: print only the openings that work, and the summary
// Output: one line per opening ("yes"/"no"), then a summary line beginning with '#'.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 1296
#define MAXQ 12
static int n, k, N, F, d, Q, quiet = 0, all = 0, show = 0, ext = 0;
static char mode;
static uint8_t fb[MAXN][MAXN];                       // fb[g][s]: the number of the answer to guess g when the code is s
static int fbB[32], fbW[32], black;                  // what answer number f means; the number of the all-black answer
static long long nodes = 0;
static long long capK[MAXQ + 1];                     // at most F^r codes can be told apart by r more answers
static long long capW[MAXQ + 1];                     // see quick()

static void maketable(void) {
  static int dig[MAXN][8]; int id[64]; memset(id, -1, sizeof id); F = 0;
  for (int c = 0; c < N; c++) { int v = c; for (int j = n - 1; j >= 0; j--) { dig[c][j] = v % k; v /= k; } }
  for (int g = 0; g < N; g++) for (int s = 0; s < N; s++) {
    int b = 0, cg[16] = {0}, cs[16] = {0}, tot = 0;
    for (int j = 0; j < n; j++) { if (dig[g][j] == dig[s][j]) b++; cg[dig[g][j]]++; cs[dig[s][j]]++; }
    for (int c = 0; c < k; c++) tot += cg[c] < cs[c] ? cg[c] : cs[c];
    int key = b * (n + 1) + (tot - b);
    if (id[key] < 0) { id[key] = F; fbB[F] = b; fbW[F] = tot - b; F++; }
    fb[g][s] = (uint8_t)id[key];
  }
  black = id[n * (n + 1)];
}

// ---- classes of a set under several answers, refined one answer at a time, so that keys stay below N*F ----
static int stampA[MAXN * 32 + 32], labelA[MAXN * 32 + 32], genA = 0;
// Writes each code's class number (0 .. c-1) under the answers to the guesses in P; returns c, the number of classes.
static int classes(const int16_t *S, int m, const int16_t *P, int p, int *id) {
  int c = m ? 1 : 0;
  for (int i = 0; i < m; i++) id[i] = 0;
  for (int j = 0; j < p; j++) {
    genA++; int c2 = 0; const uint8_t *row = fb[P[j]];
    for (int i = 0; i < m; i++) { int key = id[i] * F + row[S[i]]; if (stampA[key] != genA) { stampA[key] = genA; labelA[key] = c2++; } id[i] = labelA[key]; }
    c = c2;
  }
  return c;
}
static int apart(const int16_t *S, int m, const int16_t *P, int p) { int id[MAXN]; return classes(S, m, P, p, id) == m; }
static int largest(const int16_t *S, int m, const int16_t *P, int p) {
  int id[MAXN], cn[MAXN]; int c = classes(S, m, P, p, id), best = 0;
  for (int i = 0; i < c; i++) cn[i] = 0;
  for (int i = 0; i < m; i++) if (++cn[id[i]] > best) best = cn[id[i]];
  return best;
}

// ---- for the last guess in question K: which guesses give two codes different answers ----
static uint64_t *sep; static int WORDS;              // sep[(a*N + b)*WORDS ...], a < b: bit g set if guess g answers a and b differently
static void makesep(void) {
  WORDS = (N + 63) / 64; sep = calloc((size_t)N * N * WORDS, sizeof(uint64_t));
  static uint8_t col[MAXN][MAXN];
  for (int g = 0; g < N; g++) for (int c = 0; c < N; c++) col[c][g] = fb[g][c];
  for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) {
    uint64_t *w = sep + ((size_t)a * N + b) * WORDS; const uint8_t *x = col[a], *y = col[b];
    for (int g = 0; g < N; g++) if (x[g] != y[g]) w[g >> 6] |= 1ull << (g & 63);
  }
}
// One more guess, then every answer is in: is there a guess that, with the answers to P, tells all of S apart? Returns it, or -1.
static int lastK(const int16_t *S, int m, const int16_t *P, int p) {
  int id[MAXN], start[MAXN + 1], fill[MAXN], sorted[MAXN]; int c = classes(S, m, P, p, id);
  for (int i = 0; i <= c; i++) start[i] = 0;
  for (int i = 0; i < m; i++) start[id[i] + 1]++;
  for (int i = 0; i < c; i++) { if (start[i + 1] > F) return -1; start[i + 1] += start[i]; fill[i] = start[i]; }
  for (int i = 0; i < m; i++) sorted[fill[id[i]]++] = S[i];
  uint64_t acc[(MAXN + 63) / 64];
  for (int w = 0; w < WORDS; w++) acc[w] = ~0ull;
  if (N & 63) acc[WORDS - 1] = (1ull << (N & 63)) - 1;
  for (int q = 0; q < c; q++) for (int i = start[q]; i < start[q + 1]; i++) for (int j = i + 1; j < start[q + 1]; j++) {
    int a = sorted[i], b = sorted[j]; if (a > b) { int t = a; a = b; b = t; }
    const uint64_t *w = sep + ((size_t)a * N + b) * WORDS; uint64_t any = 0;
    for (int x = 0; x < WORDS; x++) { acc[x] &= w[x]; any |= acc[x]; }
    if (!any) return -1;
  }
  for (int x = 0; x < WORDS; x++) if (acc[x]) return x * 64 + __builtin_ctzll(acc[x]);
  return -1;
}

static int member(const int16_t *P, int p, int c) { for (int j = 0; j < p; j++) if (P[j] == c) return 1; return 0; }

// The state of play. S: the codes still possible given the answers that have arrived (in W, and not known to have been sent already).
// P: guesses sent whose answers have not arrived, oldest first. r: guesses still to send.

// In W, when every guess still to send comes too late for its answer to be used (r <= d+1), those guesses can only name codes.
// Each is decided in some state of knowledge and names one code there; the states refine as the answers in the post arrive.
// This returns the least number of codes of S that go unnamed: each state takes one code off the total of the states below it.
// A guess sent here is written -1: which code it names is left open, and its answer comes too late to matter.
static int unmetW(const int16_t *S, int m, const int16_t *P, int p, int r) {
  int out = 0;
  for (int i = 0; i < m; i++) if (!member(P, p, S[i])) out++;
  if (r == 0 || out == 0) return out;
  int16_t P2[MAXQ + 2]; memcpy(P2, P, p * sizeof(int16_t)); P2[p] = -1; int p2 = p + 1, t = 0;
  if (p2 <= d) t = unmetW(S, m, P2, p2, r - 1);                                        // no answer arrives
  else if (P2[0] < 0) t = unmetW(S, m, P2 + 1, p2 - 1, r - 1);                         // the answer to a naming guess: too late to be used
  else {
    int old = P2[0]; int16_t *T = malloc(m * sizeof(int16_t)); int cn[32] = {0}, at[33], fill[32];
    for (int i = 0; i < m; i++) cn[fb[old][S[i]]]++;
    at[0] = 0; for (int f = 0; f < F; f++) { at[f + 1] = at[f] + cn[f]; fill[f] = at[f]; }
    for (int i = 0; i < m; i++) T[fill[fb[old][S[i]]]++] = S[i];
    for (int f = 0; f < F; f++) if (cn[f] && f != black) t += unmetW(T + at[f], cn[f], P2 + 1, p2 - 1, r - 1);
    free(T);
  }
  return t > 0 ? t - 1 : 0;
}

// The cheap test: -1 the codebreaker cannot be sure, -2 nothing more is needed, 0 not settled.
static int quick(const int16_t *S, int m, const int16_t *P, int p, int r) {
  if (mode == 'K') {
    if (m <= 1) return -2;
    if (r == 0) return apart(S, m, P, p) ? -2 : -1;
    return apart(S, m, P, p) ? -2 : 0;
  }
  int out = 0;
  for (int i = 0; i < m; i++) if (!member(P, p, S[i])) out++;                           // codes not yet in the post
  if (out == 0) return -2;
  if (r == 0) return -1;
  return 0;
}

// The search: returns the guess to send (>= 0), -2 if nothing more is needed, -1 if the codebreaker cannot be sure.
static int solve(const int16_t *S, int m, const int16_t *P, int p, int r);

// The answer to the oldest guess in P2 arrives and splits S; every class must then come out right with r guesses left.
static int split(const int16_t *S, int m, const int16_t *P2, int p2, int r) {
  int old = P2[0]; int16_t *T = malloc(m * sizeof(int16_t)); int cn[32] = {0}, at[33], fill[32], todo[32], nt = 0, ok = 1;
  for (int i = 0; i < m; i++) cn[fb[old][S[i]]]++;
  at[0] = 0; for (int f = 0; f < F; f++) { at[f + 1] = at[f] + cn[f]; fill[f] = at[f]; }
  for (int i = 0; i < m; i++) T[fill[fb[old][S[i]]]++] = S[i];
  for (int f = 0; f < F && ok; f++) {                                                  // the cheap test on every class first
    if (!cn[f] || (mode == 'W' && f == black)) continue;                               // in W an all-black answer ends the game
    int q = quick(T + at[f], cn[f], P2 + 1, p2 - 1, r); if (q == -1) ok = 0; else if (q == 0) todo[nt++] = f;
  }
  for (int i = 1; i < nt; i++) { int f = todo[i], j = i - 1; while (j >= 0 && cn[todo[j]] < cn[f]) { todo[j + 1] = todo[j]; j--; } todo[j + 1] = f; }   // largest first
  for (int i = 0; i < nt && ok; i++) if (solve(T + at[todo[i]], cn[todo[i]], P2 + 1, p2 - 1, r) == -1) ok = 0;
  free(T); return ok;
}
// Does sending g now work?
static int after(const int16_t *S, int m, const int16_t *P, int p, int r, int g) {
  int16_t P2[MAXQ + 2]; memcpy(P2, P, p * sizeof(int16_t)); P2[p] = (int16_t)g; int p2 = p + 1;
  if (p2 <= d) return solve(S, m, P2, p2, r - 1) != -1;                                // no answer arrives yet
  return split(S, m, P2, p2, r - 1);
}
static int solve(const int16_t *S, int m, const int16_t *P, int p, int r) {
  nodes++;
  int q0 = quick(S, m, P, p, r); if (q0) return q0;
  // candidates, best first: the guess that, with the answers still in the post, leaves the smallest largest class
  int useful = (mode == 'K') || (r - 1 >= d + 1);                                      // in W an answer that never arrives in time tells nothing
  int *order = malloc(2 * MAXN * sizeof(int)), *score = order + MAXN, c = 0, found = -1;
  if (useful) {
    int base[MAXN]; classes(S, m, P, p, base);
    for (int g = 0; g < N; g++) {
      genA++; int mx = 0; const uint8_t *row = fb[g];
      for (int i = 0; i < m; i++) { int key = base[i] * F + row[S[i]]; if (stampA[key] != genA) { stampA[key] = genA; labelA[key] = 0; } if (++labelA[key] > mx) mx = labelA[key]; }
      score[g] = mx; order[c++] = g;
    }
    for (int i = 1; i < c; i++) { int g = order[i], j = i - 1; while (j >= 0 && score[order[j]] > score[g]) { order[j + 1] = order[j]; j--; } order[j + 1] = g; }   // stable
  } else { for (int i = 0; i < m; i++) if (!member(P, p, S[i])) order[c++] = S[i]; }
  for (int i = 0; i < c && found < 0; i++) if (after(S, m, P, p, r, order[i])) found = order[i];
  free(order); return found;
}

// ---- printing a strategy: "S t answers-known:guess" ----
static void codestr(int c, char *out) { for (int j = n - 1; j >= 0; j--) { out[j] = '1' + c % k; c /= k; } out[n] = 0; }
static void emit(const int16_t *S, int m, const int16_t *P, int p, int r, int t, const char *hist);
static void emitsplit(const int16_t *S, int m, const int16_t *P2, int p2, int r, int t, const char *hist) {
  int old = P2[0]; int16_t *T = malloc(m * sizeof(int16_t)); uint32_t seen = 0; char h2[256];
  for (int i = 0; i < m; i++) {
    int f = fb[old][S[i]]; if (seen >> f & 1) continue; seen |= 1u << f; if (mode == 'W' && f == black) continue;
    int tt = 0; for (int j = i; j < m; j++) if (fb[old][S[j]] == f) T[tt++] = S[j];
    snprintf(h2, sizeof h2, "%s%s%d%d", hist, hist[0] ? "," : "", fbB[f], fbW[f]);
    emit(T, tt, P2 + 1, p2 - 1, r, t, h2);
  }
  free(T);
}
static void emit(const int16_t *S, int m, const int16_t *P, int p, int r, int t, const char *hist) {
  int g = solve(S, m, P, p, r); if (g < 0) return;
  char cs[16]; codestr(g, cs); printf("S %d %s:%s\n", t, hist[0] ? hist : "-", cs);
  int16_t P2[MAXQ + 2]; memcpy(P2, P, p * sizeof(int16_t)); P2[p] = (int16_t)g; int p2 = p + 1;
  if (p2 <= d) emit(S, m, P2, p2, r - 1, t + 1, hist); else emitsplit(S, m, P2, p2, r - 1, t + 1, hist);
}

// ---- openings: guesses sent blind, in order ----
static int16_t ALL[MAXN];
static int forced(const int16_t *S, int m, const int16_t *P, int p, const int16_t *pre, int L, int at) {
  if (at == L) return solve(S, m, P, p, Q - L) != -1;
  int16_t P2[MAXQ + 2]; memcpy(P2, P, p * sizeof(int16_t)); P2[p] = pre[at]; int p2 = p + 1;
  if (p2 <= d) return forced(S, m, P2, p2, pre, L, at + 1);
  if (at + 1 == L) return split(S, m, P2, p2, Q - L);                                  // the opening is out: the search proper begins
  int old = P2[0]; int16_t *T = malloc(m * sizeof(int16_t)); int ok = 1; uint32_t seen = 0;
  for (int i = 0; i < m && ok; i++) {
    int f = fb[old][S[i]]; if (seen >> f & 1) continue; seen |= 1u << f; if (mode == 'W' && f == black) continue;
    int t = 0; for (int j = i; j < m; j++) if (fb[old][S[j]] == f) T[t++] = S[j];
    if (!forced(T, t, P2 + 1, p2 - 1, pre, L, at + 1)) ok = 0;
  }
  free(T); return ok;
}
static void emitforced(const int16_t *S, int m, const int16_t *P, int p, const int16_t *pre, int L, int at, const char *hist) {
  if (at == L) { emit(S, m, P, p, Q - L, L + 1, hist); return; }
  int16_t P2[MAXQ + 2]; memcpy(P2, P, p * sizeof(int16_t)); P2[p] = pre[at]; int p2 = p + 1;
  if (p2 <= d) { emitforced(S, m, P2, p2, pre, L, at + 1, hist); return; }
  int old = P2[0]; int16_t *T = malloc(m * sizeof(int16_t)); uint32_t seen = 0; char h2[256];
  for (int i = 0; i < m; i++) {
    int f = fb[old][S[i]]; if (seen >> f & 1) continue; seen |= 1u << f; if (mode == 'W' && f == black) continue;
    int t = 0; for (int j = i; j < m; j++) if (fb[old][S[j]] == f) T[t++] = S[j];
    snprintf(h2, sizeof h2, "%s%s%d%d", hist, hist[0] ? "," : "", fbB[f], fbW[f]);
    emitforced(T, t, P2 + 1, p2 - 1, pre, L, at + 1, h2);
  }
  free(T);
}

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: lag n k d Q mode [-x E] [-a] [-s] [-q] < openings\n"); return 2; }
  n = atoi(argv[1]); k = atoi(argv[2]); d = atoi(argv[3]); Q = atoi(argv[4]); mode = argv[5][0];
  for (int i = 6; i < argc; i++) { if (!strcmp(argv[i], "-x")) ext = atoi(argv[++i]); else if (!strcmp(argv[i], "-a")) all = 1; else if (!strcmp(argv[i], "-s")) show = 1; else if (!strcmp(argv[i], "-q")) quiet = 1; }
  N = 1; for (int j = 0; j < n; j++) N *= k;
  if (N > MAXN || Q > MAXQ || n > 7 || k > 9 || (mode != 'K' && mode != 'W')) { fprintf(stderr, "cannot do that board or mode\n"); return 2; }
  maketable(); for (int i = 0; i < N; i++) ALL[i] = (int16_t)i;
  if (mode == 'K') makesep();
  capK[0] = 1; for (int r = 1; r <= MAXQ; r++) capK[r] = capK[r - 1] * F > N ? N : capK[r - 1] * F;
  for (int r = 0; r <= MAXQ; r++) { long long tot = 0;
    for (int t = 1; t <= r; t++) { long long x = 1; for (int q = 0; q < t - 1 - d; q++) { x *= F - 1; if (x > N) { x = N; break; } } tot += x; }
    capW[r] = tot > N ? N : tot; }
  char line[4096]; long tried = 0, yes = 0; int done = 0;
  while (!done && fgets(line, sizeof line, stdin)) {
    int16_t pre[MAXQ + 2]; int L = 0; char *tok = strtok(line, " \t\r\n");
    while (tok && L < MAXQ) { pre[L++] = (int16_t)atoi(tok); tok = strtok(NULL, " \t\r\n"); }
    if (L + ext > Q || L + ext > d + 1) { fprintf(stderr, "an opening must be blind: at most d+1 guesses, and at most Q\n"); return 2; }
    int idx[MAXQ]; for (int e = 0; e < ext; e++) idx[e] = e;
    for (;;) {                                                                          // every increasing set of ext further blind guesses
      for (int e = 0; e < ext; e++) pre[L + e] = (int16_t)idx[e];
      int16_t P[MAXQ + 2]; int ok = forced(ALL, N, P, 0, pre, L + ext, 0); tried++; yes += ok;
      if (tried % 20000000 == 0) { fprintf(stderr, "%ld openings tried, %ld work\n", tried, yes); fflush(stderr); }
      if (!quiet || ok) { printf("%s", ok ? "yes" : "no"); for (int j = 0; j < L + ext; j++) { char cs[16]; codestr(pre[j], cs); printf(" %s", cs); } printf("\n"); fflush(stdout); }
      if (ok && show) {
        for (int j = 0; j < L + ext; j++) { char cs[16]; codestr(pre[j], cs); printf("S %d -:%s\n", j + 1, cs); }
        emitforced(ALL, N, P, 0, pre, L + ext, 0, ""); show = 0; fflush(stdout);
      }
      if (ok && !all) { done = 1; break; }
      if (!ext) break;
      int e = ext - 1; while (e >= 0 && idx[e] == N - ext + e) e--;
      if (e < 0) break;
      idx[e]++; for (int q = e + 1; q < ext; q++) idx[q] = idx[q - 1] + 1;
    }
  }
  printf("# n=%d k=%d d=%d Q=%d mode=%c: %ld openings tried, %ld work; answers %d; nodes %lld\n", n, k, d, Q, mode, tried, yes, F, nodes);
  return 0;
}
