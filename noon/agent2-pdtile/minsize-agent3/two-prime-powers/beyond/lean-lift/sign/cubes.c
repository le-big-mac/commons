/* Cube test, exhaustive, for a product of "tree" coordinates.
   A coordinate is a chain of moduli 1 = m_0 | m_1 | ... | m_a = size (e.g. "3" flat of size 3; "3,9" the tree of Z_9).
   A level is (e_1..e_r), 0 <= e_i <= a_i.  A cube at that level: for each i with e_i >= 1 two distinct classes mod m_{i,e_i}
   inside one class mod m_{i,e_i - 1}; for e_i = 0 no restriction.  Its function kappa is the product of (+1 on the first class, -1 on
   the second).  For a signing s (values +-1 on E, 0 off E) the cube sum is <kappa, s>.
   For cyclic groups (coprime prime-power sides) cube sum != 0 for some cube at level d  <=>  s(zeta_d) != 0.
   Checks for every set E containing the point 0 (translation invariance):
     D2(E) = levels where every cube meets E in an even number of points;
     mod-4 goodness of g (subset of E turned to -1): for every level some cube sum is not 0 mod 4 (only levels in D2 matter).
   Reports the least |g| found (0,1,2,3 by exhaustion; then all subsets of E), and any E with no g.
   usage: cubes "3,9;5"   (coordinates separated by ';', chain moduli by ',')   [maxsize: only sets up to that size, 0 = all] */
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
  nlev=0; ncube=0;
  for(int L=0;L<tot;L++){
    int t=L; for(int i=0;i<r;i++){ e[i]=t%(a[i]+1); t/=(a[i]+1); }
    lev_start[nlev++]=ncube;
    /* enumerate cubes: for each i with e_i>=1 choose classes c1<c2 mod m_{e_i} with same class mod m_{e_i-1} */
    int idx[8], c1[8], c2[8]; int npairs[8];
    /* list pairs per coordinate */
    static int pl[8][4096][2];
    for(int i=0;i<r;i++){ npairs[i]=0; if(e[i]==0){ npairs[i]=1; continue; }
      int m=mod[i][e[i]], m0=mod[i][e[i]-1];
      for(int u=0;u<m;u++) for(int v=u+1;v<m;v++) if(u%m0==v%m0){ pl[i][npairs[i]][0]=u; pl[i][npairs[i]][1]=v; npairs[i]++; } }
    for(int i=0;i<r;i++) idx[i]=0;
    for(;;){
      u64 p=0,mm=0;
      for(int x=0;x<N;x++){ int sgn=1, in=1;
        for(int i=0;i<r && in;i++){ if(e[i]==0) continue; int m=mod[i][e[i]]; int c=coord(x,i)%m;
          if(c==pl[i][idx[i]][0]) ; else if(c==pl[i][idx[i]][1]) sgn=-sgn; else in=0; }
        if(in){ if(sgn>0) p|=1ULL<<x; else mm|=1ULL<<x; } }
      if(ncube>=MAXC){ fprintf(stderr,"too many cubes\n"); exit(1);} P[ncube]=p; M[ncube]=mm; ncube++;
      int i=0; while(i<r){ idx[i]++; if(idx[i]<npairs[i]) break; idx[i]=0; i++; } if(i==r) break;
    }
  }
  lev_start[nlev]=ncube;
}
static int d2[4096], nd2;
static inline int good(u64 E,u64 g){
  for(int k=0;k<nd2;k++){ int L=d2[k], ok=0;
    for(int c=lev_start[L];c<lev_start[L+1];c++){
      int s=__builtin_popcountll(E&P[c])-__builtin_popcountll(E&M[c])-2*(__builtin_popcountll(g&P[c])-__builtin_popcountll(g&M[c]));
      if(s&3){ ok=1; break; } }
    if(!ok) return 0; }
  return 1;
}
int main(int argc,char**argv){
  char buf[256]; strcpy(buf,argv[1]); int maxsize = argc>2? atoi(argv[2]):0;
  r=0; char*sv1; for(char*t=strtok_r(buf,";",&sv1); t; t=strtok_r(NULL,";",&sv1)){ char*sv2; a[r]=0; mod[r][0]=1;
    for(char*q=strtok_r(t,",",&sv2); q; q=strtok_r(NULL,",",&sv2)) mod[r][++a[r]]=atoi(q);
    sz[r]=mod[r][a[r]]; r++; }
  N=1; for(int i=0;i<r;i++) N*=sz[i];
  if(N>40){ fprintf(stderr,"too large for exhaustion\n"); return 1; }
  build();
  long long cnt[8]={0}, nsets=0, nfail=0, d2empty=0; int shown=0;
  for(u64 E=1; E<(1ULL<<N); E+=2){
    int w=__builtin_popcountll(E); if(maxsize && w>maxsize) continue;
    nsets++; nd2=0;
    for(int L=0;L<nlev;L++){ int ev=1; for(int c=lev_start[L];c<lev_start[L+1];c++) if(__builtin_popcountll(E&(P[c]|M[c]))&1){ ev=0; break; } if(ev) d2[nd2++]=L; }
    if(!nd2){ d2empty++; continue; }
    int pts[64], np=0; for(int x=0;x<N;x++) if(E>>x&1) pts[np++]=x;
    int found=-1;
    if(good(E,0)) found=0;
    if(found<0) for(int i=0;i<np&&found<0;i++) if(good(E,1ULL<<pts[i])) found=1;
    if(found<0) for(int i=0;i<np&&found<0;i++) for(int j=i+1;j<np&&found<0;j++) if(good(E,(1ULL<<pts[i])|(1ULL<<pts[j]))) found=2;
    if(found<0) for(int i=0;i<np&&found<0;i++) for(int j=i+1;j<np&&found<0;j++) for(int k=j+1;k<np&&found<0;k++) if(good(E,(1ULL<<pts[i])|(1ULL<<pts[j])|(1ULL<<pts[k]))) found=3;
    if(found<0){ /* all subsets of E */ u64 g=E; do{ if(good(E,g)){ found=4; break; } g=(g-1)&E; }while(g!=E); }
    if(found<0){ nfail++; if(shown<10){ shown++; printf("  NO g: E ="); for(int i=0;i<np;i++) printf(" %d",pts[i]); printf("\n"); } }
    else cnt[found]++;
  }
  printf("%s: N = %d, levels %d, cubes %d; sets containing 0%s: %lld; D2 empty: %lld; least |g| = 0: %lld, 1: %lld, 2: %lld, 3: %lld, more: %lld; NO g at all: %lld\n",
     argv[1], N, nlev, ncube, maxsize? " (size-limited)":"", nsets, d2empty, cnt[0],cnt[1],cnt[2],cnt[3],cnt[4], nfail);
  return 0;
}
