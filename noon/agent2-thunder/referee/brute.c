/* Blind referee's own brute-force program: point emitters at midpoints of sub-pieces of length ~h.
   p[k] = sum_e (ds/r_e) N((k/fs - r_e/c)/T),  N(u)=1-2u on [0,1). */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
static const double c=343.0,T=0.005,fs=44100.0;
static double *p; static long np_; static double rmin,rmax; static long nem;
static void emit(double x,double z,double ds,double lx,double lz){
  double r=hypot(x-lx,z-lz),tau=r/c,amp=ds/r; long k=(long)ceil(tau*fs);
  if(r<rmin)rmin=r; if(r>rmax)rmax=r; nem++;
  for(;;k++){ double u=(k/fs-tau)/T; if(u>=1.0)break; if(u<0)continue; if(k>=np_){fprintf(stderr,"overflow\n");exit(1);} p[k]+=amp*(1-2*u);}
}
static void poly(const double *pts,int n,double h,double lx,double lz){
  for(int i=0;i+1<n;i++){ double x0=pts[2*i],z0=pts[2*i+1],x1=pts[2*i+2],z1=pts[2*i+3];
    double L=hypot(x1-x0,z1-z0); long m=(long)floor(L/h+0.5); if(m<1)m=1;
    for(long j=0;j<m;j++){ double f=(j+0.5)/m; emit(x0+(x1-x0)*f,z0+(z1-z0)*f,L/m,lx,lz);} }
}
static void arc(double R,double a0,double a1,double h,double lx,double lz){
  double L=R*(a1-a0); long m=(long)floor(L/h+0.5);
  for(long j=0;j<m;j++){ double a=a0+(a1-a0)*(j+0.5)/m; emit(R*cos(a),R*sin(a),L/m,lx,lz);} }
static void start(void){ memset(p,0,np_*sizeof(double)); rmin=1e300; rmax=0; nem=0; }
static void report(const char*name,int energy){
  long i=0,j=0,f=-1,l=-1; double e=0;
  for(long k=0;k<np_;k++){ if(p[k]>p[i])i=k; if(p[k]<p[j])j=k; if(p[k]!=0){ if(f<0)f=k; l=k;} e+=p[k]*p[k]; }
  printf("%s n=%ld max %.7g at %.6f | min %.7g at %.6f | first nonzero sample %.6f last %.6f | rmin/c %.6f rmax/c+T %.6f",
    name,nem,p[i],i/fs,p[j],j/fs,f/fs,l/fs,rmin/c,rmax/c+T);
  if(energy)printf(" | int p^2 dt %.7g",e/fs);
  printf("\n"); fflush(stdout);
}
int main(int argc,char**argv){
  np_=(long)(30*fs); p=malloc(np_*sizeof(double));
  double A[]={0,-3000,0,3000}; double C[]={0,5000,400,3800,-300,2500,200,1200,0,0};
  double hs[]={0.08,0.04,0.02,0.01,0.005,0.0025}; double d2r=acos(-1.0)/180;
  for(int q=0;q<6;q++){ double h=hs[q]; printf("spacing %g m\n",h);
    start(); poly(A,2,h,1000,0); report("A",0);
    start(); arc(2000,20*d2r,50*d2r,h,0,0); report("B",0);
    start(); poly(C,5,h,2000,0); report("C",1);
    if(argc>1 && q==5){ FILE*fp=fopen("C_fine.bin","wb"); fwrite(p,sizeof(double),np_,fp); fclose(fp);} }
  return 0;
}
