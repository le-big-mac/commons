/* "Tiny" cube test: for each nonempty set E (containing point 0) in a product of tree coordinates (see cubes.c for the format),
   is there a signing such that for EVERY level some cube has signed sum in {+-1, +-2} ?
   (Such a signing is good modulo every integer P >= 3 at every level.)
   Search: all signings if |E| <= 18, else flips of at most 3 points and 3000 random signings (then 'undecided' if none found).
   usage: cubes_tiny "3;5" */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
#define MAXC 200000
static u64 P[MAXC], M[MAXC]; static int lev_start[4096], nlev, ncube;
static int r, a[8], mod[8][8], sz[8], N;
static int coord(int x, int i){ for(int k=0;k<i;k++) x/=sz[k]; return x%sz[i]; }
static void build(void){
  int e[8]; int tot=1; for(int i=0;i<r;i++) tot*= (a[i]+1);
  nlev=0; ncube=0; static int pl[8][4096][2];
  for(int L=0;L<tot;L++){
    int t=L; for(int i=0;i<r;i++){ e[i]=t%(a[i]+1); t/=(a[i]+1); }
    lev_start[nlev++]=ncube; int idx[8], npairs[8];
    for(int i=0;i<r;i++){ npairs[i]=0; if(e[i]==0){ npairs[i]=1; continue; }
      int m=mod[i][e[i]], m0=mod[i][e[i]-1];
      for(int u=0;u<m;u++) for(int v=u+1;v<m;v++) if(u%m0==v%m0){ pl[i][npairs[i]][0]=u; pl[i][npairs[i]][1]=v; npairs[i]++; } }
    for(int i=0;i<r;i++) idx[i]=0;
    for(;;){ u64 p=0,mm=0;
      for(int x=0;x<N;x++){ int sgn=1, in=1;
        for(int i=0;i<r && in;i++){ if(e[i]==0) continue; int m=mod[i][e[i]]; int c=coord(x,i)%m;
          if(c==pl[i][idx[i]][0]) ; else if(c==pl[i][idx[i]][1]) sgn=-sgn; else in=0; }
        if(in){ if(sgn>0) p|=1ULL<<x; else mm|=1ULL<<x; } }
      P[ncube]=p; M[ncube]=mm; ncube++;
      int i=0; while(i<r){ idx[i]++; if(idx[i]<npairs[i]) break; idx[i]=0; i++; } if(i==r) break; }
  }
  lev_start[nlev]=ncube;
}
static inline int good(u64 E,u64 g){
  for(int L=0;L<nlev;L++){ int ok=0;
    for(int c=lev_start[L];c<lev_start[L+1];c++){
      int s=__builtin_popcountll(E&P[c])-__builtin_popcountll(E&M[c])-2*(__builtin_popcountll(g&P[c])-__builtin_popcountll(g&M[c]));
      if(s==1||s==-1||s==2||s==-2){ ok=1; break; } }
    if(!ok) return 0; }
  return 1;
}
int main(int argc,char**argv){
  char buf[256]; strcpy(buf,argv[1]);
  r=0; char*sv1; for(char*t=strtok_r(buf,";",&sv1); t; t=strtok_r(NULL,";",&sv1)){ char*sv2; a[r]=0; mod[r][0]=1;
    for(char*q=strtok_r(t,",",&sv2); q; q=strtok_r(NULL,",",&sv2)) mod[r][++a[r]]=atoi(q); sz[r]=mod[r][a[r]]; r++; }
  N=1; for(int i=0;i<r;i++) N*=sz[i]; build(); srandom(7);
  long long nsets=0, nfail=0, undec=0; int shown=0;
  for(u64 E=1; E<(1ULL<<N); E+=2){ nsets++;
    int pts[64], np=0; for(int x=0;x<N;x++) if(E>>x&1) pts[np++]=x;
    int found=0;
    if(np<=18){ u64 g=E; do{ if(good(E,g)){ found=1; break; } g=(g-1)&E; }while(g!=E);
      if(!found){ nfail++; if(shown<10){ shown++; printf("  NO tiny signing: E ="); for(int i=0;i<np;i++) printf(" %d",pts[i]); printf("\n"); } } }
    else { if(good(E,0)) found=1;
      for(int i=0;i<np&&!found;i++){ if(good(E,1ULL<<pts[i])) found=1; for(int j=i+1;j<np&&!found;j++){ if(good(E,(1ULL<<pts[i])|(1ULL<<pts[j]))) found=1; } }
      for(int t=0;t<3000&&!found;t++){ u64 g=(((u64)random()<<31)^random())&E; if(good(E,g)) found=1; }
      if(!found) undec++; }
  }
  printf("%s: N = %d, levels %d; sets containing 0: %lld; proven without tiny signing: %lld; undecided (large sets, sampled): %lld\n", argv[1],N,nlev,nsets,nfail,undec);
  return 0;
}
