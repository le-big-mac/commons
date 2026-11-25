// Referee, second step: the m-th parts measured two ways on the same clouds (raw depth as the sheet defines; profile taken off first),
// at several annulus widths. Same peeler and generator as peel.c.
// usage: peel2 n nclouds seed
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static u128 st; static uint64_t sm;
static uint64_t splitmix(void){ uint64_t z=(sm+=0x9e3779b97f4a7c15ULL); z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL; z=(z^(z>>27))*0x94d049bb133111ebULL; return z^(z>>31);}
static inline uint64_t rng(void){ st*=(u128)0xda942042e4dd58b5ULL; return (uint64_t)(st>>64);}
static inline double uni(void){ return ((double)(rng()>>11)+0.5)*(1.0/9007199254740992.0);}
typedef struct {double x,y;} pt;
static int cmp(const void*a,const void*b){ double d=((const pt*)a)->x-((const pt*)b)->x; return (d>0)-(d<0);}
static pt *P;
static inline double cross(int o,int a,int b){ return (P[a].x-P[o].x)*(P[b].y-P[o].y)-(P[a].y-P[o].y)*(P[b].x-P[o].x);}
static int peel(int N,int*depth,int*idx,int*hull,char*on){
  int m=N,layer=0,i,j,k; for(i=0;i<N;i++){idx[i]=i;on[i]=0;}
  while(m>0){ layer++; if(m<=2){ for(i=0;i<m;i++) depth[idx[i]]=layer; break; }
    k=0; for(i=0;i<m;i++){ int p=idx[i]; while(k>=2 && cross(hull[k-2],hull[k-1],p)<=0) k--; hull[k++]=p; } for(i=0;i<k;i++) on[hull[i]]=1;
    k=0; for(i=m-1;i>=0;i--){ int p=idx[i]; while(k>=2 && cross(hull[k-2],hull[k-1],p)<=0) k--; hull[k++]=p; } for(i=0;i<k;i++) on[hull[i]]=1;
    j=0; for(i=0;i<m;i++){ int p=idx[i]; if(on[p]) depth[p]=layer; else idx[j++]=p; } m=j; }
  return layer;
}
#define NR 3
#define NW 3
static const double RR[NR]={0.3,0.5,0.7};
static const double HW[NW]={0.004,0.008,0.016};
int main(int argc,char**argv){
  int n=atoi(argv[1]),nc=atoi(argv[2]); uint64_t seed=strtoull(argv[3],0,10);
  sm=seed*0x9E3779B97F4A7C15ULL+777; st=(((u128)splitmix())<<64)|splitmix()|1; for(int i=0;i<8;i++)rng();
  double A=0.75*1.3259*pow(n/M_PI,2.0/3.0);
  P=malloc(n*sizeof(pt)); int*depth=malloc(n*sizeof(int)),*idx=malloc(n*sizeof(int)),*hull=malloc(n*sizeof(int)); char*on=malloc(n);
  for(int c=0;c<nc;c++){
    int N=n;
    for(int i=0;i<N;i++){ double x,y; do{ x=2*uni()-1; y=2*uni()-1; }while(x*x+y*y>=1.0); P[i].x=x;P[i].y=y; }
    qsort(P,N,sizeof(pt),cmp);
    peel(N,depth,idx,hull,on);
    static double S[NR][NW][32];
    for(int a=0;a<NR;a++)for(int w=0;w<NW;w++)for(int b=0;b<32;b++)S[a][w][b]=0;
    for(int i=0;i<N;i++){
      double x=P[i].x,y=P[i].y,rad=sqrt(x*x+y*y);
      for(int a=0;a<NR;a++){
        double u=rad-RR[a]; if(fabs(u)>=HW[NW-1]) continue;
        double e=depth[i]-A*(1-pow(rad,4.0/3.0)), d=depth[i]-A*(1-pow(RR[a],4.0/3.0));
        double c1=x/rad,s1=y/rad,cm=1,sn=0,t;
        double cs[8]; for(int m=0;m<4;m++){ t=cm*c1-sn*s1; sn=sn*c1+cm*s1; cm=t; cs[2*m]=cm; cs[2*m+1]=sn; }
        for(int w=0;w<NW;w++){ if(fabs(u)>=HW[w]) continue; double*s=S[a][w];
          s[0]+=1; s[1]+=e; s[2]+=d; s[3]+=d*d; s[4]+=e*e;
          for(int q=0;q<8;q++){ s[5+q]+=cs[q]; s[13+q]+=e*cs[q]; s[21+q]+=d*cs[q]; } }
      }
    }
    for(int a=0;a<NR;a++)for(int w=0;w<NW;w++){ double*s=S[a][w]; double np=s[0],eb=s[1]/np,db=s[2]/np;
      printf("%d %.6f %.6f ",(int)np,s[3]/np-db*db,s[4]/np-eb*eb);
      for(int q=0;q<8;q++) printf("%.6f ",2*(s[13+q]/np-eb*s[5+q]/np));   // detrended c1 s1 c2 s2 ...
      for(int q=0;q<8;q++) printf("%.6f ",2*(s[21+q]/np-db*s[5+q]/np));   // raw (sheet's definition)
    }
    printf("\n");
  }
  return 0;
}
