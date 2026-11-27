/* (R**), r <= 4: for each nonempty family F of nonempty subsets of [r]: the set BAD of signings with some Psi_D = 0;
   is there B0 in F such that no two bad signings differ exactly at B0 (so: any signing, or its flip at B0, is good)?
   usage: rstar_flip q1 .. qr */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef long long ll;
int r,q[8]; ll c[16][16]; static unsigned char bad[1<<15];
int main(int argc,char**argv){
  r=argc-1; for(int i=0;i<r;i++) q[i]=atoi(argv[i+1]);
  for(int D=0;D<(1<<r);D++) for(int B=0;B<(1<<r);B++){ ll v=1; for(int i=0;i<r;i++) if(D>>i&1){ if(B>>i&1) v=-v; else v*=q[i]; } c[D][B]=v; }
  int nb=(1<<r)-1; ll nfam=0, none=0, minfails=0; double minfrac=2; uint32_t shown=0;
  for(uint32_t F=1;F<(1u<<nb);F++){ int sets[16],N=0; for(int k=0;k<nb;k++) if(F>>k&1) sets[N++]=k+1; nfam++;
    ll base[16]; for(int D=0;D<(1<<r);D++){ ll s=c[D][0]; for(int k=0;k<N;k++) s+=c[D][sets[k]]; base[D]=s; }
    ll nbad=0;
    for(uint32_t M=0;M<(1u<<N);M++){ int ok=1;
      for(int D=0;D<(1<<r)&&ok;D++){ ll s=base[D]; uint32_t m=M; while(m){ int k=__builtin_ctz(m); m&=m-1; s-=2*c[D][sets[k]]; } if(s==0) ok=0; }
      bad[M]=!ok; nbad+=!ok; }
    double fr=1.0-(double)nbad/(1u<<N); if(fr<minfrac) minfrac=fr;
    int any=0;
    for(int k=0;k<N;k++){ int w=1; for(uint32_t M=0;M<(1u<<N)&&w;M++) if(bad[M]&&bad[M^(1u<<k)]) w=0; if(w){ any=1; break; } }
    if(!any){ none++; if(shown<5){ shown++; printf("  no B0 for family:"); for(int k=0;k<N;k++) printf(" %d",sets[k]); printf("  (bad signings %lld of %u)\n",nbad,1u<<N); } }
  }
  printf("q ="); for(int i=0;i<r;i++) printf(" %d",q[i]);
  printf(": nonempty families %lld; least fraction of good signings %.4f; families with no universal flip B0: %lld\n",nfam,minfrac,none);
  return 0;
}
