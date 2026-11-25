/* cloud.c: N points thrown evenly and independently in a convex shape, as whole numbers for ../peel file:NAME.
   Noon (agent2), 25 November 2026.     usage: cloud SHAPE N SEED > NAME
   SHAPE  disc | ellipse | square | rect | triangle | hexagon | halfdisc | quarter | rtriangle (an equilateral triangle
   swollen by a quarter of its inradius, so that its corners are arcs). Every shape has area pi in units of
   2^28 (so that the largest coordinate stays under 2^29, which is what peel's exact arithmetic allows), and has its centre of
   area at the origin. A point is two whole numbers drawn evenly from the shape's bounding box, kept if it is in the shape.
   Random numbers: xoshiro256** started through splitmix64 from SEED and the shape's name. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
static uint64_t S[4];
static uint64_t splitmix(uint64_t *x) { uint64_t z = (*x += 0x9E3779B97F4A7C15ULL); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t next(void) { uint64_t r = rotl(S[1] * 5, 7) * 9, t = S[1] << 17; S[2] ^= S[0]; S[3] ^= S[1]; S[1] ^= S[2]; S[0] ^= S[3]; S[2] ^= t; S[3] = rotl(S[3], 45); return r; }
static double U01(void) { return ((double)(next() >> 11) + 0.5) / 9007199254740992.0; }
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: cloud SHAPE N SEED > NAME\n"); return 2; }
    const char *name = argv[1]; long n = atol(argv[2]), i; uint64_t sd = strtoull(argv[3], NULL, 10), z; const double UNIT = 268435456.0;
    double x0, x1, y0, y1; int kind;
    if (!strcmp(name, "disc")) { kind = 0; x0 = y0 = -1; x1 = y1 = 1; }
    else if (!strcmp(name, "ellipse")) { kind = 1; x0 = -sqrt(3.0); x1 = sqrt(3.0); y0 = -1 / sqrt(3.0); y1 = 1 / sqrt(3.0); }
    else if (!strcmp(name, "square")) { kind = 2; x1 = y1 = sqrt(M_PI) / 2; x0 = y0 = -x1; }
    else if (!strcmp(name, "rect")) { kind = 2; x1 = sqrt(3 * M_PI) / 2; x0 = -x1; y1 = M_PI / (4 * x1); y0 = -y1; }
    else if (!strcmp(name, "triangle")) { double a = sqrt(4 * M_PI / sqrt(3.0)), h = a * sqrt(3.0) / 2; kind = 3; x0 = -a / 2; x1 = a / 2; y0 = -h / 3; y1 = 2 * h / 3; }
    else if (!strcmp(name, "rtriangle")) { double rin = sqrt(M_PI / (4.5 * sqrt(3.0) + M_PI / 16)), rr = rin / 4, a = 2 * sqrt(3.0) * rin; kind = 7; x0 = -a / 2 - rr; x1 = a / 2 + rr; y0 = -rin - rr; y1 = 2 * rin + rr; }
    else if (!strcmp(name, "hexagon")) { double r = sqrt(2 * M_PI / (3 * sqrt(3.0))); kind = 4; x0 = -r; x1 = r; y1 = r * sqrt(3.0) / 2; y0 = -y1; }
    else if (!strcmp(name, "halfdisc")) { double r = sqrt(2.0), c = 4 * r / (3 * M_PI); kind = 5; x0 = -r; x1 = r; y0 = -c; y1 = r - c; }
    else if (!strcmp(name, "quarter")) { double r = 2.0, c = 4 * r / (3 * M_PI); kind = 6; x0 = y0 = -c; x1 = y1 = r - c; }
    else { fprintf(stderr, "unknown shape %s\n", name); return 2; }
    if (n < 1 || n > 100000000) { fprintf(stderr, "N from 1 to 100,000,000\n"); return 2; }
    z = sd * 0x100000001B3ULL; for (i = 0; name[i]; i++) z = z * 31 + (unsigned char)name[i];
    for (i = 0; i < 4; i++) S[i] = splitmix(&z);
    static char buf[1 << 16]; setvbuf(stdout, buf, _IOFBF, sizeof buf);
    for (i = 0; i < n; ) {
        double x = floor((x0 + (x1 - x0) * U01()) * UNIT), y = floor((y0 + (y1 - y0) * U01()) * UNIT), u = x / UNIT, v = y / UNIT; int in;
        switch (kind) {
            case 0: in = u * u + v * v <= 1; break;
            case 1: in = u * u / 3 + 3 * v * v <= 1; break;
            case 2: in = 1; break;
            case 3: { double a = sqrt(4 * M_PI / sqrt(3.0)), h = a * sqrt(3.0) / 2; in = v >= -h / 3 && fabs(u) * h <= (a / 2) * (2 * h / 3 - v); break; }
            case 4: { double r = sqrt(2 * M_PI / (3 * sqrt(3.0))), ap = r * sqrt(3.0) / 2; in = fabs(v) <= ap && fabs(sqrt(3.0) / 2 * u + v / 2) <= ap && fabs(sqrt(3.0) / 2 * u - v / 2) <= ap; break; }
            case 5: { double r = sqrt(2.0), c = 4 * r / (3 * M_PI); in = v + c >= 0 && u * u + (v + c) * (v + c) <= 2; break; }
            case 7: { double rin = sqrt(M_PI / (4.5 * sqrt(3.0) + M_PI / 16)), rr = rin / 4, a = 2 * sqrt(3.0) * rin; double vx[3] = {-a / 2, a / 2, 0}, vy[3] = {-rin, -rin, 2 * rin}; int j;      /* in the triangle, or within rr of one of its sides */
                      in = v >= -rin && fabs(u) * (3 * rin) <= (a / 2) * (2 * rin - v);
                      for (j = 0; j < 3 && !in; j++) { double px = vx[j], py = vy[j], qx = vx[(j + 1) % 3] - px, qy = vy[(j + 1) % 3] - py, t = ((u - px) * qx + (v - py) * qy) / (qx * qx + qy * qy), dx, dy; if (t < 0) t = 0; if (t > 1) t = 1; dx = u - px - t * qx; dy = v - py - t * qy; if (dx * dx + dy * dy <= rr * rr) in = 1; }
                      break; }
            default: { double r = 2.0, c = 4 * r / (3 * M_PI); in = u + c >= 0 && v + c >= 0 && (u + c) * (u + c) + (v + c) * (v + c) <= r * r; break; }
        }
        if (in) { printf("%.0f %.0f\n", x, y); i++; }
    }
    return 0;
}
