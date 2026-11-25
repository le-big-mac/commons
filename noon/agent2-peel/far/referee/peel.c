// Convex (parabolic) peeling of a Poisson process, referee's own program.
// RNG: PCG-XSL-RR 128/64 (pcg64), NOT xoshiro.
// usage: peel W H seed periodic shear mode outfile
//   mode 0: write band statistics (band thickness 0.25): b n sum_y sum_d sum_d2 sum_d3
//   mode 1: dump points: x y depth
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
#include <string.h>
typedef __uint128_t u128;
static u128 st, inc;
static inline uint64_t pcg(void){
  const u128 MUL = (((u128)0x2360ED051FC65DA4ULL)<<64) | 0x4385DF649FCCF645ULL;
  st = st*MUL + inc;
  uint64_t hi = (uint64_t)(st>>64), lo = (uint64_t)st;
  uint64_t x = hi ^ lo; unsigned r = (unsigned)(hi>>58);
  return (x>>r) | (x<<((64-r)&63));
}
static inline double u01(void){ return ((double)(pcg()>>11)+0.5)*(1.0/9007199254740992.0); }
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  double W=atof(argv[1]), H=atof(argv[2]); uint64_t seed=strtoull(argv[3],0,10);
  int periodic=atoi(argv[4]); double shear=atof(argv[5]); int mode=atoi(argv[6]);
  inc = ((((u128)seed*2654435761ULL+12345)<<64) | (seed*0x9E3779B97F4A7C15ULL+777)) | 1;
  st = ((u128)(seed+0x853c49e6748fea9bULL)<<64) | (seed^0xda3e39cb94b95bdbULL);
  for(int i=0;i<20;i++) pcg();
  size_t cap=(size_t)(W*H*1.05+1000);
  double *x=malloc(cap*8), *y=malloc(cap*8), *wx=malloc(cap*8), *wy=malloc(cap*8);
  int *wid=malloc(cap*4), *dep=malloc(cap*4);
  size_t N=0; double xx=0;
  for(;;){
    xx += -log(u01())/H; if(xx>=W) break;
    if(N>=cap){fprintf(stderr,"cap\n");return 2;}
    x[N]=xx; y[N]=H*u01(); N++;
  }
  size_t n=N;
  for(size_t i=0;i<n;i++){wx[i]=x[i]; wy[i]=y[i]+shear*x[i]; wid[i]=(int)i;}
  double *sx=malloc((n+2)*8), *sy=malloc((n+2)*8); int *sj=malloc((n+2)*4);
  char *mark=calloc(n+2,1);
  int layer=0; size_t i0=0;
  if(periodic){ for(size_t i=1;i<n;i++) if(wy[i]<wy[i0]) i0=i; }
  while(n>0){
    layer++;
    size_t top=0, total = periodic? n+1 : n;
    for(size_t t=0;t<total;t++){
      size_t j=(periodic? i0:0)+t; double off=0; if(j>=n){j-=n; off=W;}
      double cx=wx[j]+off, cy=wy[j];
      while(top>=2){
        double dx1=sx[top-1]-sx[top-2], dx2=cx-sx[top-2];
        double dy1=sy[top-1]-sy[top-2], dy2=cy-sy[top-2];
        double cr=dx1*dy2-dy1*dx2+0.5*dx1*dx2*(dx2-dx1);
        if(cr<=0) top--; else break;
      }
      sx[top]=cx; sy[top]=cy; sj[top]=(int)j; top++;
    }
    for(size_t k=0;k<top;k++){ mark[sj[k]]=1; dep[wid[sj[k]]]=layer; }
    size_t m=0; i0=0; double ymin=1e300;
    for(size_t i=0;i<n;i++){
      if(mark[i]){mark[i]=0; continue;}
      wx[m]=wx[i]; wy[m]=wy[i]; wid[m]=wid[i];
      if(wy[m]<ymin){ymin=wy[m]; i0=m;}
      m++;
    }
    n=m;
  }
  FILE*f=fopen(argv[7],"w");
  if(mode==1){
    for(size_t i=0;i<N;i++) fprintf(f,"%.17g %.17g %d\n",x[i],y[i],dep[i]);
  } else {
    double dy=0.25; int nb=(int)ceil(H/dy)+1;
    double *a=calloc((size_t)nb*5,8);
    for(size_t i=0;i<N;i++){
      int b=(int)(y[i]/dy); double d=dep[i];
      a[5*b]+=1; a[5*b+1]+=y[i]; a[5*b+2]+=d; a[5*b+3]+=d*d; a[5*b+4]+=d*d*d;
    }
    for(int b=0;b<nb;b++) if(a[5*b]>0)
      fprintf(f,"%d %.0f %.10g %.0f %.0f %.0f\n",b,a[5*b],a[5*b+1],a[5*b+2],a[5*b+3],a[5*b+4]);
  }
  fclose(f);
  fprintf(stderr,"W=%g H=%g seed=%llu N=%zu layers=%d\n",W,H,(unsigned long long)seed,N,layer);
  return 0;
}
