// Enumerate binary necklaces of length M (FKM), print those whose mask polynomial vanishes at some M-th root of unity != 1.
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int M; int a[64]; double C[64][64], S[64][64]; long total=0, cand=0;
void visit(void){
  total++; int w=0; for(int i=1;i<=M;i++) w+=a[i];
  if(w<2||w>=M) return;
  for(int k=1;k<=M/2;k++){ double re=0,im=0; for(int i=1;i<=M;i++) if(a[i]){ re+=C[k][i-1]; im+=S[k][i-1]; }
    if(re*re+im*im<1e-18){ unsigned long b=0; for(int i=1;i<=M;i++) if(a[i]) b|=1UL<<(i-1); printf("%lu\n",b); cand++; return; } }
}
void gen(int t,int p){
  if(t>M){ if(M%p==0) visit(); return; }
  a[t]=a[t-p]; gen(t+1,p);
  for(int j=a[t-p]+1;j<=1;j++){ a[t]=j; gen(t+1,t); }
}
int main(int c,char**v){ M=atoi(v[1]);
  for(int k=0;k<=M;k++) for(int i=0;i<M;i++){ C[k][i]=cos(2*M_PI*k*i/M); S[k][i]=sin(2*M_PI*k*i/M); }
  a[0]=0; gen(1,1); fprintf(stderr,"necklaces %ld candidates %ld\n",total,cand); return 0; }
