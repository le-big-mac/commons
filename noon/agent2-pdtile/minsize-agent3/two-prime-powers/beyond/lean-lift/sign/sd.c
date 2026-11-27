/* Sign-definiteness test (SD), independent of the q_i.
   f(z) = 1 + sum_{B in F} eta_B z^B.  For D subset of [r] and D0 subset of D put
      V(D0, D) = value of f at z_i = 0 (i in D0), -1/2 (i in D \ D0), 1 (i not in D)   [times 2^{|D|} to stay in integers].
   (SD): there are signs such that for every D the numbers V(D0, D), D0 subset of D, are all >= 0 or all <= 0, and V(empty, D) != 0.
   If (SD) holds for F then for ALL real theta_i in (0, 1/2] the same signs give f != 0 on the grid prod {1, -theta_i}
   (f(z^D) is affine in each theta_i, so it is a combination with nonnegative weights of its values at the corners theta_i in {0,1/2},
    the corner (1/2,..,1/2) having positive weight).
   usage: sd r        exhaustive over all families for r <= 4 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef long long ll;
int r; ll v[81][16]; int nD[81], D0of[81], Dof[81], ncorner;
int main(int argc,char**argv){
  r=atoi(argv[1]); int nb=(1<<r)-1; ncorner=0;
  for(int D=0;D<(1<<r);D++) for(int D0=D;;D0=(D0-1)&D){
    for(int B=0;B<(1<<r);B++){ ll val; if(B&D0) val=0; else { int k=__builtin_popcount(B&D); val=(k&1?-1:1)*(1LL<<(__builtin_popcount(D)-k)); } v[ncorner][B]=val; }
    D0of[ncorner]=D0; Dof[ncorner]=D; ncorner++; if(D0==0) break; }
  ll nfam=0, fails=0; int shown=0;
  for(uint32_t F=0;F<(1u<<nb);F++){ int sets[16],N=0; for(int k=0;k<nb;k++) if(F>>k&1) sets[N++]=k+1; nfam++;
    int found=0;
    for(uint32_t M=0;M<(1u<<N)&&!found;M++){ int ok=1; int sgn[16]; for(int D=0;D<(1<<r);D++) sgn[D]=0;
      for(int cidx=0;cidx<ncorner&&ok;cidx++){ ll s=v[cidx][0]; for(int k=0;k<N;k++) s+= (M>>k&1? -1:1)*v[cidx][sets[k]];
        int D=Dof[cidx]; if(D0of[cidx]==0 && s==0) ok=0;
        if(s>0){ if(sgn[D]<0) ok=0; sgn[D]=1; } else if(s<0){ if(sgn[D]>0) ok=0; sgn[D]=-1; } }
      if(ok) found=1; }
    if(!found){ fails++; if(shown<8){ shown++; printf("  (SD) fails for family:"); for(int k=0;k<N;k++) printf(" %d",sets[k]); printf("\n"); } }
  }
  printf("r = %d: families %lld; families where no signing is sign-definite: %lld\n", r, nfam, fails); return 0;
}
