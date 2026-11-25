// Referee: peel the author's points (integer coordinates) with my own method, exact arithmetic, and compare depths.
// usage: check < peel-output   (first line JSON, then "x y depth")
#include <stdio.h>
#include <stdlib.h>
typedef struct {long long x,y; int d;} pt;
static pt *P;
static int cmp(const void*a,const void*b){ const pt*p=a,*q=b; if(p->x!=q->x) return p->x<q->x?-1:1; if(p->y!=q->y) return p->y<q->y?-1:1; return 0;}
static inline __int128 cross(int o,int a,int b){ return (__int128)(P[a].x-P[o].x)*(P[b].y-P[o].y)-(__int128)(P[a].y-P[o].y)*(P[b].x-P[o].x);}
int main(void){
  static char line[8192]; if(!fgets(line,sizeof line,stdin)) return 1;
  int cap=1<<20,N=0; P=malloc(cap*sizeof(pt)); long long x,y; int d;
  while(scanf("%lld %lld %d",&x,&y,&d)==3){ if(N==cap){cap*=2;P=realloc(P,cap*sizeof(pt));} P[N].x=x;P[N].y=y;P[N].d=d;N++; }
  qsort(P,N,sizeof(pt),cmp);
  int dup=0,tiex=0; for(int i=1;i<N;i++){ if(P[i].x==P[i-1].x){tiex++; if(P[i].y==P[i-1].y)dup++;} }
  int*depth=malloc(N*sizeof(int)),*idx=malloc(N*sizeof(int)),*hull=malloc(N*sizeof(int)); char*on=calloc(N,1);
  int m=N,layer=0,i,j,k; long collinear=0;
  for(i=0;i<N;i++)idx[i]=i;
  while(m>0){
    layer++;
    if(m<=2){ for(i=0;i<m;i++) depth[idx[i]]=layer; break; }
    k=0; for(i=0;i<m;i++){ int p=idx[i]; while(k>=2){ __int128 c=cross(hull[k-2],hull[k-1],p); if(c==0)collinear++; if(c<=0)k--; else break;} hull[k++]=p; }
    for(i=0;i<k;i++) on[hull[i]]=1;
    k=0; for(i=m-1;i>=0;i--){ int p=idx[i]; while(k>=2){ __int128 c=cross(hull[k-2],hull[k-1],p); if(c==0)collinear++; if(c<=0)k--; else break;} hull[k++]=p; }
    for(i=0;i<k;i++) on[hull[i]]=1;
    j=0; for(i=0;i<m;i++){ int p=idx[i]; if(on[p]) depth[p]=layer; else idx[j++]=p; }
    m=j;
  }
  long bad=0; int maxd=0; for(i=0;i<N;i++){ if(depth[i]!=P[i].d) bad++; if(P[i].d>maxd)maxd=P[i].d; }
  printf("points %d  my layers %d  author's deepest %d  depth mismatches %ld  (ties in x %d, duplicate points %d, exactly collinear tests %ld)\n",N,layer,maxd,bad,tiex,dup,collinear);
  return 0;
}
