// Referee's own convex peeling of uniform clouds in the unit disc.
// RNG: Lehmer 128-bit multiplicative generator (lehmer64), seeded by splitmix64.
// usage: peel n kind(0 fixed,1 poisson) nclouds seed [dump]
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static u128 st;
static uint64_t sm;
static uint64_t splitmix(void){ uint64_t z=(sm+=0x9e3779b97f4a7c15ULL); z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL; z=(z^(z>>27))*0x94d049bb133111ebULL; return z^(z>>31);}
static inline uint64_t rng(void){ st*=(u128)0xda942042e4dd58b5ULL; return (uint64_t)(st>>64);}
static inline double uni(void){ return ((double)(rng()>>11)+0.5)*(1.0/9007199254740992.0);}

typedef struct {double x,y;} pt;
static int cmp(const void*a,const void*b){ double d=((const pt*)a)->x-((const pt*)b)->x; return (d>0)-(d<0);}
static pt *P;
static inline double cross(int o,int a,int b){ return (P[a].x-P[o].x)*(P[b].y-P[o].y)-(P[a].y-P[o].y)*(P[b].x-P[o].x);}

static int peel(int N,int*depth,int*idx,int*hull,char*on){
  int m=N,layer=0,i,j,k;
  for(i=0;i<N;i++){idx[i]=i;on[i]=0;}
  while(m>0){
    layer++;
    if(m<=2){ for(i=0;i<m;i++) depth[idx[i]]=layer; break; }
    k=0;
    for(i=0;i<m;i++){ int p=idx[i]; while(k>=2 && cross(hull[k-2],hull[k-1],p)<=0) k--; hull[k++]=p; }
    for(i=0;i<k;i++) on[hull[i]]=1;
    k=0;
    for(i=m-1;i>=0;i--){ int p=idx[i]; while(k>=2 && cross(hull[k-2],hull[k-1],p)<=0) k--; hull[k++]=p; }
    for(i=0;i<k;i++) on[hull[i]]=1;
    j=0;
    for(i=0;i<m;i++){ int p=idx[i]; if(on[p]) depth[p]=layer; else idx[j++]=p; }
    m=j;
  }
  return layer;
}

#define NR 5
static const double RR[NR]={0.2,0.3,0.5,0.7,0.8};
#define HW 0.008

int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage\n");return 1;}
  int n=atoi(argv[1]),kind=atoi(argv[2]),nc=atoi(argv[3]); uint64_t seed=strtoull(argv[4],0,10);
  int dump=(argc>5);
  sm=seed*0x9E3779B97F4A7C15ULL+12345; st=(((u128)splitmix())<<64)|splitmix()|1; for(int i=0;i<8;i++)rng();
  double A=0.75*1.3259*pow(n/M_PI,2.0/3.0);
  int cap=n+20*(int)sqrt((double)n)+100;
  P=malloc(cap*sizeof(pt)); int*depth=malloc(cap*sizeof(int)),*idx=malloc(cap*sizeof(int)),*hull=malloc(cap*sizeof(int)); char*on=malloc(cap);
  for(int c=0;c<nc;c++){
    int N=n;
    if(kind==1){ // exact Poisson(n): count unit-rate arrivals before time n
      double s=0; N=0; for(;;){ s+=-log(uni()); if(s>n)break; N++; }
      if(N>cap)N=cap;
    }
    for(int i=0;i<N;i++){ double x,y; do{ x=2*uni()-1; y=2*uni()-1; }while(x*x+y*y>=1.0); P[i].x=x;P[i].y=y; }
    qsort(P,N,sizeof(pt),cmp);
    int L=peel(N,depth,idx,hull,on);
    if(dump){ for(int i=0;i<N;i++) printf("%.17g %.17g %d\n",P[i].x,P[i].y,depth[i]); printf("#\n"); continue; }
    double S[NR][16]; for(int a=0;a<NR;a++)for(int b=0;b<16;b++)S[a][b]=0;
    for(int i=0;i<N;i++){
      double x=P[i].x,y=P[i].y,rad=sqrt(x*x+y*y);
      for(int a=0;a<NR;a++){
        double u=rad-RR[a];
        if(fabs(u)<HW){
          double e=depth[i]-A*(1-pow(rad,4.0/3.0));
          double d=depth[i]-A*(1-pow(RR[a],4.0/3.0));
          double ct=x/rad,sn=y/rad;
          double c2=ct*ct-sn*sn,s2=2*ct*sn,c3=4*ct*ct*ct-3*ct,s3=3*sn-4*sn*sn*sn;
          double*s=S[a];
          s[0]+=1; s[1]+=e;
          s[2]+=ct; s[3]+=sn; s[4]+=c2; s[5]+=s2; s[6]+=c3; s[7]+=s3;
          s[8]+=e*ct; s[9]+=e*sn; s[10]+=e*c2; s[11]+=e*s2; s[12]+=e*c3; s[13]+=e*s3;
          // line fit sums in 2nd array below
        }
      }
    }
    // second pass for line fit (centred) for numerical safety
    double F[NR][5]; for(int a=0;a<NR;a++)for(int b=0;b<5;b++)F[a][b]=0;
    for(int i=0;i<N;i++){
      double x=P[i].x,y=P[i].y,rad=sqrt(x*x+y*y);
      for(int a=0;a<NR;a++){
        double u=rad-RR[a];
        if(fabs(u)<HW){ double d=depth[i]-A*(1-pow(RR[a],4.0/3.0)); double*f=F[a]; f[0]+=u; f[1]+=d; f[2]+=u*u; f[3]+=u*d; f[4]+=d*d; }
      }
    }
    printf("%d %d",N,L);
    for(int a=0;a<NR;a++){
      double*s=S[a],*f=F[a]; double np=s[0],M=s[1]/np;
      double suu=f[2]-f[0]*f[0]/np, sud=f[3]-f[0]*f[1]/np, sdd=f[4]-f[1]*f[1]/np;
      double vline=(sdd-sud*sud/suu)/(np-2);
      printf(" %d %.6f %.6f",(int)np,M,vline);
      for(int m=0;m<6;m++) printf(" %.6f",2*(s[8+m]/np-M*s[2+m]/np));
    }
    printf("\n");
  }
  return 0;
}
