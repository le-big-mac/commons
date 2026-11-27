/* (R**): for a family F of nonempty subsets B of [r] and integers q_i >= 2, are there signs eta_B with
      Psi_D = q^D + sum_{B in F} eta_B (-1)^{|B cap D|} q^{D \ B}   != 0   for every D subset of [r] ?
   (Psi_D / q^D = 1 + sum eta_B prod_{i in B cap D} (-1/q_i) is the value of f(z) = 1 + sum eta_B z^B at z_i = -1/q_i (i in D), 1 (else).)
   Exhaustive over all families for r <= 4; random families for r = 5 (then: argument nrand).
   usage: rstar q1 ... qr [nrand] */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef long long ll;
int r, q[8]; ll c[32][32]; /* c[D][B] */
static int solve(int *sets, int N){
  /* try all sign patterns (first sign may be fixed? no: constant term breaks the symmetry) */
  ll base[32];
  for(int D=0; D<(1<<r); D++){ ll s=c[D][0]; for(int k=0;k<N;k++) s+=c[D][sets[k]]; base[D]=s; }
  if(N<=22){
    for(uint32_t M=0; M<(1u<<N); M++){ int ok=1;
      for(int D=0; D<(1<<r) && ok; D++){ ll s=base[D]; uint32_t m=M; while(m){ int k=__builtin_ctz(m); m&=m-1; s-=2*c[D][sets[k]]; } if(s==0) ok=0; }
      if(ok) return 1; }
    return 0; }
  for(int t=0;t<200000;t++){ uint32_t M=(uint32_t)random() ^ ((uint32_t)random()<<16); int ok=1;
    for(int D=0; D<(1<<r) && ok; D++){ ll s=base[D]; for(int k=0;k<N;k++) if(M>>k&1) s-=2*c[D][sets[k]]; if(s==0) ok=0; }
    if(ok) return 1; }
  return -1;
}
int main(int argc,char**argv){
  r=0; int nrand=0; for(int i=1;i<argc;i++){ if(r<5 && (i<argc-1 || argc-1<=5)) q[r++]=atoi(argv[i]); else nrand=atoi(argv[i]); }
  if(argc-1==6){ r=5; nrand=atoi(argv[6]); }
  for(int D=0;D<(1<<r);D++) for(int B=0;B<(1<<r);B++){ ll v=1; for(int i=0;i<r;i++) if(D>>i&1){ if(B>>i&1) v=-v; else v*=q[i]; } c[D][B]=v; }
  int nb=(1<<r)-1; ll fails=0, total=0, unknown=0; int sets[32];
  if(r<=4){
    for(uint32_t F=0; F<(1u<<nb); F++){ int N=0; for(int b=0;b<nb;b++) if(F>>b&1) sets[N++]=b+1; total++;
      int res=solve(sets,N); if(res==0){ fails++; if(fails<=5){ printf("  FAIL family:"); for(int k=0;k<N;k++) printf(" %d",sets[k]); printf("\n"); } } }
  } else {
    srandom(12345);
    for(int t=0;t<nrand;t++){ int N=0; int dens=1+random()%9; for(int b=0;b<nb;b++) if(random()%10<dens) sets[N++]=b+1; total++;
      int res=solve(sets,N); if(res==0){ fails++; if(fails<=5){ printf("  FAIL family:"); for(int k=0;k<N;k++) printf(" %d",sets[k]); printf("\n"); } } else if(res<0) unknown++; }
  }
  printf("q ="); for(int i=0;i<r;i++) printf(" %d",q[i]);
  printf(": families %lld, with no good signs %lld, undecided (random search only) %lld\n", total, fails, unknown);
  return 0;
}
