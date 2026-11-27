/* Independence test (IND').  Product of tree coordinates as in cubes.c.  For each set E containing 0:
   D2(E) = levels where every cube meets E evenly.  For each level L in D2 a cube kappa_L meeting E is to be chosen so that,
   among the chosen restricted functionals kappa_L|E (identified up to an overall sign), DISTINCT functionals have supports
   that are linearly independent over F_2.   (Then the system  <kappa_L, E - 2g> = 2 mod 4, L in D2,  is solvable for g subset of E:
   a mod-4-good signing.)   Backtracking search.  Reports sets for which no such choice exists.
   usage: indep "3;5" [step]     (step > 1: only every step-th set, for sampling) */
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
#define MAXK 600
static u64 cp[64][MAXK], cs[64][MAXK]; static int nc[64]; static int nd2;
static u64 chp[64], chs[64]; static int nch;         /* chosen distinct functionals: plus-part, support */
static u64 basis[64]; static int nbasis;
static int reduce_in(u64 v){ for(int i=0;i<nbasis;i++){ u64 t=v^basis[i]; if(t<v) v=t; } return v!=0; }
static int rec(int k){
  if(k==nd2) return 1;
  for(int j=0;j<nc[k];j++){ u64 p=cp[k][j], s=cs[k][j];
    int dup=0, clash=0; for(int i=0;i<nch;i++){ if(chs[i]==s){ if(chp[i]==p) dup=1; else clash=1; } }
    if(clash) continue;
    if(dup){ if(rec(k+1)) return 1; continue; }
    u64 v=s; for(int i=0;i<nbasis;i++){ u64 t=v^basis[i]; if(t<v) v=t; }
    if(!v) continue;
    int savb=nbasis, savc=nch; basis[nbasis++]=v;
    /* keep basis sorted by leading bit descending for the reduction to work */
    for(int i=nbasis-1;i>0 && basis[i]>basis[i-1];i--){ u64 t=basis[i]; basis[i]=basis[i-1]; basis[i-1]=t; }
    chp[nch]=p; chs[nch]=s; nch++;
    if(rec(k+1)) return 1;
    /* undo: remove v from basis */
    int pos=0; while(basis[pos]!=v) pos++; for(int i=pos;i<nbasis-1;i++) basis[i]=basis[i+1]; nbasis=savb; nch=savc;
  }
  return 0;
}
int main(int argc,char**argv){
  char buf[256]; strcpy(buf,argv[1]); long long step= argc>2? atoll(argv[2]):1;
  r=0; char*sv1; for(char*t=strtok_r(buf,";",&sv1); t; t=strtok_r(NULL,";",&sv1)){ char*sv2; a[r]=0; mod[r][0]=1;
    for(char*q=strtok_r(t,",",&sv2); q; q=strtok_r(NULL,",",&sv2)) mod[r][++a[r]]=atoi(q); sz[r]=mod[r][a[r]]; r++; }
  N=1; for(int i=0;i<r;i++) N*=sz[i]; build();
  long long nsets=0, nfail=0, withd2=0; int shown=0;
  for(u64 E=1; E<(1ULL<<N); E+=2*step){ nsets++; nd2=0;
    for(int L=0;L<nlev;L++){ int ev=1; for(int c=lev_start[L];c<lev_start[L+1];c++) if(__builtin_popcountll(E&(P[c]|M[c]))&1){ ev=0; break; }
      if(!ev) continue; int k=nd2++; nc[k]=0;
      for(int c=lev_start[L];c<lev_start[L+1];c++){ u64 p=E&P[c], m=E&M[c]; if(!(p|m)) continue; u64 s=p|m;
        if((m & (~m+1)) && ((s & (~s+1)) == (m & (~m+1)))){ u64 t=p; p=m; m=t; }       /* normalise: lowest point of the support is a plus */
        int dup=0; for(int j=0;j<nc[k];j++) if(cp[k][j]==p && cs[k][j]==s){ dup=1; break; }
        if(!dup && nc[k]<MAXK){ cp[k][nc[k]]=p; cs[k][nc[k]]=s; nc[k]++; } } }
    if(!nd2) continue; withd2++;
    /* order levels by number of candidates (fewest first) */
    for(int i=0;i<nd2;i++) for(int j=i+1;j<nd2;j++) if(nc[j]<nc[i]){ int t=nc[i]; nc[i]=nc[j]; nc[j]=t; for(int q=0;q<MAXK;q++){ u64 x=cp[i][q]; cp[i][q]=cp[j][q]; cp[j][q]=x; x=cs[i][q]; cs[i][q]=cs[j][q]; cs[j][q]=x; } }
    nch=0; nbasis=0;
    if(!rec(0)){ nfail++; if(shown<10){ shown++; printf("  no independent choice: E ="); for(int x=0;x<N;x++) if(E>>x&1) printf(" %d",x); printf("\n"); } }
  }
  printf("%s: N = %d; sets examined %lld (with D2 nonempty %lld); sets with NO independent choice of cubes: %lld\n", argv[1],N,nsets,withd2,nfail);
  return 0;
}
