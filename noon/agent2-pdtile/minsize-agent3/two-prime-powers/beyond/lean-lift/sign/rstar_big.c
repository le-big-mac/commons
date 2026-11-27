/* (R**) for larger r: random families of nonempty subsets of [r], integers q_i = p_i - 1; search for signs with all
   Psi_D = q^D + sum_B eta_B (-1)^{|B cap D|} q^{D\B} != 0.   Exhaustive over signings when the family has at most 20 sets
   (so a reported failure is a true failure), random signings otherwise.
   usage: rstar_big nfam seed maxsets q1 ... qr */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef __int128 big; typedef long long ll;
int r,q[12]; static big c[1<<10][64]; int sets[64];
int main(int argc,char**argv){
  int nfam=atoi(argv[1]); srandom(atoi(argv[2])); int maxsets=atoi(argv[3]); r=argc-4; for(int i=0;i<r;i++) q[i]=atoi(argv[4+i]);
  int nD=1<<r; ll fails=0, undec=0;
  for(int t=0;t<nfam;t++){
    int N=1+random()%maxsets; int mode=random()%4;
    for(int k=0;k<N;k++){ int B;
      do{ if(mode==0) B=1+random()%(nD-1); else if(mode==1){ B=0; for(int i=0;i<r;i++) if(random()%3==0) B|=1<<i; }   /* small sets */
          else if(mode==2){ B=1<<(random()%r); if(random()%2) B|=1<<(random()%r); }                                   /* singletons and pairs */
          else { B=0; for(int i=0;i<r;i++) if(random()%3) B|=1<<i; } }                                                 /* large sets */
      while(B==0); int dup=0; for(int j=0;j<k;j++) if(sets[j]==B) dup=1; if(dup){ k--; if(N>nD-1) N=nD-1; continue; } sets[k]=B; }
    for(int D=0;D<nD;D++){ big v0=1; for(int i=0;i<r;i++) if(D>>i&1) v0*=q[i]; c[D][63]=v0;
      for(int k=0;k<N;k++){ big v=1; for(int i=0;i<r;i++) if(D>>i&1){ if(sets[k]>>i&1) v=-v; else v*=q[i]; } c[D][k]=v; } }
    int found=0;
    if(N<=20){ for(uint32_t M=0;M<(1u<<N)&&!found;M++){ int ok=1; for(int D=0;D<nD&&ok;D++){ big s=c[D][63]; for(int k=0;k<N;k++) s+= (M>>k&1)? -c[D][k]:c[D][k]; if(s==0) ok=0; } if(ok) found=1; }
      if(!found){ fails++; if(fails<=5){ printf("  FAIL: sets (bitmasks)"); for(int k=0;k<N;k++) printf(" %d",sets[k]); printf("\n"); } } }
    else { for(int it=0;it<20000&&!found;it++){ uint64_t M=((uint64_t)random()<<31)^random()^((uint64_t)random()<<50); int ok=1; for(int D=0;D<nD&&ok;D++){ big s=c[D][63]; for(int k=0;k<N;k++) s+= (M>>k&1)? -c[D][k]:c[D][k]; if(s==0) ok=0; } if(ok) found=1; }
      if(!found) undec++; }
  }
  printf("q ="); for(int i=0;i<r;i++) printf(" %d",q[i]); printf(": random families %d (up to %d sets): proven failures %lld, undecided %lld\n",nfam,maxsets,fails,undec);
  return 0;
}
