/* cosines and sines of an array of angles; compiled apart with -ffast-math so that the compiler may use the vector
   library.  Nothing else is compiled that way: the sums in small.c are compensated and must not be reordered. */
#include <math.h>
void trig(const double *t, double *c, double *s, int n) {
  for (int i = 0; i < n; i++) { c[i] = cos(t[i]); s[i] = sin(t[i]); }
}
