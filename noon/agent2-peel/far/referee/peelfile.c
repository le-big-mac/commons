// Referee: peel the points dumped by cell2 (-check -dump) with my own chain, exact integer arithmetic.
// file: first line "period top", then "x y depth" in whole-number units (lift = y + x^2 exactly).
// usage: peelfile FILE [keepties]   (keepties=1: a point exactly on the parabola through its neighbours is taken too)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef __int128 wide; typedef int64_t i64;
typedef struct { i64 x, y; int d0, id; } P;
static int cmp(const void*a,const void*b){ const P*p=a,*q=b; if(p->x!=q->x) return p->x<q->x?-1:1; if(p->y!=q->y) return p->y<q->y?-1:1; return 0; }
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); int keepties = argc>2 ? atoi(argv[2]) : 0;
  long long per, top; if(fscanf(f,"%lld %lld",&per,&top)!=2) return 1;
  size_t cap=1<<20, N=0; P*p=malloc(cap*sizeof(P)); long long x,y; int d;
  while(fscanf(f,"%lld %lld %d",&x,&y,&d)==3){ if(N==cap){cap*=2;p=realloc(p,cap*sizeof(P));} p[N].x=x;p[N].y=y;p[N].d0=d;p[N].id=(int)N;N++; }
  qsort(p,N,sizeof(P),cmp);
  int *dep=calloc(N,sizeof(int)); P*w=malloc(N*sizeof(P)); for(size_t i=0;i<N;i++) w[i]=p[i];
  i64 *sx=malloc((N+2)*8), *sy=malloc((N+2)*8); int *sj=malloc((N+2)*4); char*mark=calloc(N+2,1);
  size_t n=N, i0=0; for(size_t i=1;i<n;i++) if(w[i].y<w[i0].y) i0=i;
  int layer=0; long ties=0;
  while(n>0){
    layer++; size_t tp=0;
    for(size_t t=0;t<=n;t++){
      size_t j=i0+t; i64 off=0; if(j>=n){j-=n; off=per;}
      i64 cx=w[j].x+off, cy=w[j].y;
      while(tp>=2){
        wide d1=sx[tp-1]-sx[tp-2], d2=cx-sx[tp-2], e1=sy[tp-1]-sy[tp-2], e2=cy-sy[tp-2];
        wide v=d1*e2-e1*d2+d1*d2*(d2-d1);
        if(v==0) ties++;
        if(v<0 || (v==0 && !keepties)) tp--; else break;
      }
      sx[tp]=cx; sy[tp]=cy; sj[tp]=(int)j; tp++;
    }
    for(size_t k=0;k<tp;k++){ mark[sj[k]]=1; dep[w[sj[k]].id]=layer; }
    size_t m=0; i0=0; i64 ymin=INT64_MAX;
    for(size_t i=0;i<n;i++){ if(mark[i]){mark[i]=0;continue;} w[m]=w[i]; if(w[m].y<ymin){ymin=w[m].y;i0=m;} m++; }
    n=m;
  }
  long below=0, mism=0, above=0, big=0; int maxd=0;
  for(size_t i=0;i<N;i++){ // p is sorted; dep indexed by id (= input order), p[i].id maps
    int mine=dep[p[i].id];
    if(p[i].d0>0){ below++; if(mine!=p[i].d0){ mism++; if(abs(mine-p[i].d0)>1) big++; } if(p[i].d0>maxd) maxd=p[i].d0; }
    else above++;
  }
  printf("%s: period %lld top %lld points %zu (finished %ld, above top %ld) my layers %d their max depth %d | depth mismatches %ld (by more than one: %ld) | exact ties met in chain %ld keepties=%d\n",
    argv[1],per,top,N,below,above,layer,maxd,mism,big,ties,keepties);
  return 0;
}
