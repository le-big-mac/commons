/* (R**) with rational grid values: z_i in {1, -a_i/b}.  For every family F of nonempty subsets of [r] (r <= 4):
   are there signs with  b^{|D|} f(z^D) = b^{|D|} + sum_B eta_B prod_{i in D}( i in B ? -a_i : b ) != 0 for all D ?
   Scans all (a_1..a_r) with 1 <= a_i <= amax, and reports the failing (a, family) with the smallest max a_i/b.
   usage: rstar_real r b amax */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef long long ll;
int r, a[8], b; ll c[16][16];
static int solve(int *sets,int N){
  ll base[16];
  for(int D=0;D<(1<<r);D++){ ll s=c[D][0]; for(int k=0;k<N;k++) s+=c[D][sets[k]]; base[D]=s; }
  for(uint32_t M=0;M<(1u<<N);M++){ int ok=1;
    for(int D=0;D<(1<<r)&&ok;D++){ ll s=base[D]; uint32_t m=M; while(m){ int k=__builtin_ctz(m); m&=m-1; s-=2*c[D][sets[k]]; } if(s==0) ok=0; }
    if(ok) return 1; }
  return 0;
}
int main(int argc,char**argv){
  r=atoi(argv[1]); b=atoi(argv[2]); int amax=atoi(argv[3]); int nb=(1<<r)-1; ll fails=0,total=0; int best=1<<30; int bestA[8]; uint32_t bestF=0;
  int idx[8]; for(int i=0;i<r;i++) idx[i]=1;
  for(;;){
    int nondecr=1; for(int i=1;i<r;i++) if(idx[i]<idx[i-1]) nondecr=0;   /* symmetry: a_1 <= a_2 <= ... */
    if(nondecr){
      for(int i=0;i<r;i++) a[i]=idx[i];
      for(int D=0;D<(1<<r);D++) for(int B=0;B<(1<<r);B++){ ll v=1; for(int i=0;i<r;i++) if(D>>i&1){ if(B>>i&1) v*=-a[i]; else v*=b; } c[D][B]=v; }
      for(uint32_t F=0;F<(1u<<nb);F++){ int sets[16],N=0; for(int k=0;k<nb;k++) if(F>>k&1) sets[N++]=k+1; total++;
        if(!solve(sets,N)){ fails++; int mx=0; for(int i=0;i<r;i++) if(a[i]>mx) mx=a[i]; if(mx<best){ best=mx; bestF=F; for(int i=0;i<r;i++) bestA[i]=a[i]; } } }
    }
    int i=0; while(i<r){ idx[i]++; if(idx[i]<=amax) break; idx[i]=1; i++; } if(i==r) break;
  }
  printf("r = %d, grid values -a/%d with a <= %d: (a, family) pairs %lld, failures %lld", r,b,amax,total,fails);
  if(fails){ printf("; failure with least max a: a ="); for(int i=0;i<r;i++) printf(" %d",bestA[i]); printf(", family (bitmask of subsets 1..%d) %u",nb,bestF); }
  printf("\n"); return 0;
}
