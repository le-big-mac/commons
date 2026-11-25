// Binary necklaces of length M; keep those passing two necessary conditions for pd-tiling:
//  (a) number of Fourier zeros >= |A|-1      (b) |A-A| <= M - M/|A| + 1
// Usage: neck2 M worker nworkers  -> prints bitmasks
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int M, me, NW, D; int a[64]; double C[64][64], S[64][64]; int divs[64], phi[64], nd; long total=0, cand=0, sub=0;
static int gcd(int x,int y){ return y?gcd(y,x%y):x; }
void visit(void){
  total++; int w=0; unsigned long b=0; for(int i=1;i<=M;i++) if(a[i]){ w++; b|=1UL<<(i-1); }
  if(w<2||w>=M) return;
  int z=0;
  for(int j=0;j<nd;j++){ int k=M/divs[j]; double re=0,im=0; for(int i=0;i<M;i++) if(b>>i&1){ re+=C[k][i]; im+=S[k][i]; }
    if(re*re+im*im<1e-18) z+=phi[j]; }
  if(z<w-1) return;
  unsigned long full=(M==64)?~0UL:((1UL<<M)-1), diff=0;
  for(int i=0;i<M;i++) if(b>>i&1) diff|=((b>>i)|(b<<(M-i)))&full;   // {x-i : x in A}
  int nd2=__builtin_popcountl(diff);
  if((double)nd2 > M-(double)M/w+1+1e-9) return;
  printf("%lu\n",b); cand++;
}
void gen(int t,int p){
  if(t>M){ if(M%p==0) visit(); return; }
  if(t==D+1){ if((sub++)%NW!=me) return; }
  a[t]=a[t-p]; gen(t+1,p);
  for(int j=a[t-p]+1;j<=1;j++){ a[t]=j; gen(t+1,t); }
}
int main(int c,char**v){ M=atoi(v[1]); me=c>2?atoi(v[2]):0; NW=c>3?atoi(v[3]):1; D=M>24?18:1;
  for(int k=0;k<=M;k++) for(int i=0;i<M;i++){ C[k][i]=cos(2*M_PI*k*i/M); S[k][i]=sin(2*M_PI*k*i/M); }
  for(int d=2;d<=M;d++) if(M%d==0){ divs[nd]=d; int f=0; for(int x=1;x<=d;x++) if(gcd(x,d)==1) f++; phi[nd++]=f; }
  a[0]=0; gen(1,1); fprintf(stderr,"M %d worker %d/%d necklaces %ld candidates %ld\n",M,me,NW,total,cand); return 0; }
