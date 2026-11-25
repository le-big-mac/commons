// orrery.c — barycentric N-body integration of the solar system.
// Units: au, day. Bodies: Sun Mercury Venus Earth Moon Mars Jup Sat Ura Nep Plu (barycenters for 4-9).
// Integrator: 3-stage Gauss-Legendre implicit Runge-Kutta (order 6, symplectic), fixed-point iteration.
// Relativity: optional 1PN Schwarzschild term from the Sun on every other body.
// usage: orrery ic.txt years dt gr(0/1) out_every_days mode
//   mode "state": prints jd body x y z vx vy vz ; mode "peri": prints t(yr) and Mercury varpi (arcsec), e, a
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define N 11
#define NS 3
static const double AU = 149597870.7, DAY = 86400.0, CKM = 299792.458;
static const double GMkm[N] = {132712440041.279419, 22031.868551, 324858.592, 398600.435507, 4902.800118,
  42828.375816, 126712764.1, 37940584.8418, 5794556.4, 6836527.10058, 975.5};
static double GM[N], c2; static int use_gr, use_j2; static double k2dt; static double tcur;
typedef struct { double x[N][3], v[N][3]; double th, om; double p[3]; } State;   // p: the Earth's pole (unit vector), a variable of the integration when POLE=1   // th, om: the Moon's rotation angle (longitude of its long axis) and rate, used when LFIG>=3
static double p_dot[3]; static int dynpole; static double hdyn = 0.0032737949;   // set by accel(): rate of change of the Earth's pole; H = (C-A)/C
static double th_acc; static int lfig;                              // set by accel(): angular acceleration of the Moon's rotation

static void accel(const State *s, double a[N][3]) {
  memset(a, 0, sizeof(double)*N*3);
  for (int i = 0; i < N; i++) for (int j = i+1; j < N; j++) {
    double d[3], r2 = 0;
    for (int k = 0; k < 3; k++) { d[k] = s->x[j][k]-s->x[i][k]; r2 += d[k]*d[k]; }
    double inv = 1.0/(r2*sqrt(r2));
    for (int k = 0; k < 3; k++) { a[i][k] += GM[j]*inv*d[k]; a[j][k] -= GM[i]*inv*d[k]; }
  }
  if (use_j2) { // Earth's oblateness acting on the Moon (and the reaction), precessing pole
    static double j2fac = -1; if (j2fac < 0) j2fac = getenv("J2FAC") ? atof(getenv("J2FAC")) : 1;      // J2FAC scales the Earth's oblateness (for measuring what it contributes)
    static double j2val = -1, j2dot = 0, j2t2 = 0;      // J2VAL, J2DOT (per year), J2T2 (per year^2): an oblateness that changes with time, as DE441's does (J2E, J2EDOT, J2ET2 in its header)
    if (j2val < 0) { j2val = getenv("J2VAL") ? atof(getenv("J2VAL")) : 1.0826359e-3; j2dot = getenv("J2DOT") ? atof(getenv("J2DOT")) : 0; j2t2 = getenv("J2T2") ? atof(getenv("J2T2")) : 0; }
    const double ty = tcur/365.25, J2 = (j2val + j2dot*ty + j2t2*ty*ty)*j2fac, Re = 6378.1366/149597870.7, eps = 23.4392911*M_PI/180;
    static double prec = -1; if (prec < 0) prec = getenv("PREC") ? atof(getenv("PREC")) : 50.2879;   // rate of the pole round the J2000 ecliptic pole, arcsec/yr. 50.2879 is the general precession; relative to the FIXED ecliptic it should be 50.3848 (PREC=50.38481507)
    double lam = M_PI/2 - (prec/206264.806247)*(tcur/365.25);
    double p[3] = {sin(eps)*cos(lam), sin(eps)*sin(lam), cos(eps)}, r[3], r2 = 0, z = 0;
    if (dynpole) { // the pole is carried by the integration: turned by every other body's pull on the Earth's bulge (precession and nutation come out by themselves)
      const double w = 7.292115e-5*86400.0; double pn = sqrt(s->p[0]*s->p[0]+s->p[1]*s->p[1]+s->p[2]*s->p[2]);
      for (int k = 0; k < 3; k++) { p[k] = s->p[k]/pn; p_dot[k] = 0; }
      for (int j = 0; j < N; j++) { if (j == 3) continue;
        double d[3], d2 = 0, dp = 0; for (int k = 0; k < 3; k++) { d[k] = s->x[j][k]-s->x[3][k]; d2 += d[k]*d[k]; dp += d[k]*p[k]; }
        double K = 3*GM[j]*hdyn/(w*d2*d2*sqrt(d2))*dp;            // 3 GM H (r.p) / (w r^5)
        p_dot[0] += K*(d[1]*p[2]-d[2]*p[1]); p_dot[1] += K*(d[2]*p[0]-d[0]*p[2]); p_dot[2] += K*(d[0]*p[1]-d[1]*p[0]); }
    }
    for (int k = 0; k < 3; k++) { r[k] = s->x[4][k]-s->x[3][k]; r2 += r[k]*r[k]; z += r[k]*p[k]; }
    double f = -1.5*J2*Re*Re/(r2*r2*sqrt(r2));
    for (int k = 0; k < 3; k++) { double g = f*((1-5*z*z/r2)*r[k] + 2*z*p[k]); a[4][k] += GM[3]*g; a[3][k] -= GM[4]*g; }
    if (getenv("LFIG")) { // Moon's figure, crude: synchronous Moon with long axis at Earth -> extra radial attraction
      static double lfac = -1; if (lfac < 0) lfac = getenv("LFAC") ? atof(getenv("LFAC")) : 1;   // LFAC scales the Moon's J2 and C22 in every term of its figure (for measuring what the figure contributes)
      double kf = lfac*(1.5*2.032e-4 + 9*2.24e-5)*pow(1737.4/149597870.7,2)/(r2*r2*sqrt(r2));
      for (int k = 0; k < 3; k++) { a[4][k] -= GM[3]*kf*r[k]; a[3][k] += GM[4]*kf*r[k]; }
    }
    if (getenv("LFIG") && atoi(getenv("LFIG")) >= 2) { // the part of the Moon's figure that depends on its spin axis: potential K (s.r)^2 / r^5,
      // K = G(M) Rm^2 (3/2 J2 + 3 C22); spin axis s in its Cassini state: 1.543 deg from the ecliptic pole, on the far side from the orbit normal
      static double lfac2 = -1; if (lfac2 < 0) lfac2 = getenv("LFAC") ? atof(getenv("LFAC")) : 1;
      double vv[3], nrm[3], I = 1.543*M_PI/180, K = lfac2*(1.5*2.032e-4 + 3*2.24e-5)*pow(1737.4/149597870.7,2);
      for (int k = 0; k < 3; k++) vv[k] = s->v[4][k]-s->v[3][k];
      nrm[0] = r[1]*vv[2]-r[2]*vv[1]; nrm[1] = r[2]*vv[0]-r[0]*vv[2]; nrm[2] = r[0]*vv[1]-r[1]*vv[0];
      double hp = sqrt(nrm[0]*nrm[0]+nrm[1]*nrm[1]), sp[3] = {-sin(I)*nrm[0]/hp, -sin(I)*nrm[1]/hp, cos(I)};
      static int cass = -1; if (cass < 0) cass = getenv("CASS") ? atoi(getenv("CASS")) : 0;
      if (cass) { // Cassini's laws refer to the ecliptic OF DATE: build the spin axis from the pole of the Earth-Moon barycentre's own orbit round the Sun, not from the J2000 ecliptic pole
        double re[3], ve[3], kk[3], hh[3], kn, hn, hk = 0, un = 0, u[3], f3 = GM[3]/(GM[3]+GM[4]), f4 = GM[4]/(GM[3]+GM[4]);
        for (int k = 0; k < 3; k++) { re[k] = f3*s->x[3][k]+f4*s->x[4][k]-s->x[0][k]; ve[k] = f3*s->v[3][k]+f4*s->v[4][k]-s->v[0][k]; }
        kk[0] = re[1]*ve[2]-re[2]*ve[1]; kk[1] = re[2]*ve[0]-re[0]*ve[2]; kk[2] = re[0]*ve[1]-re[1]*ve[0]; kn = sqrt(kk[0]*kk[0]+kk[1]*kk[1]+kk[2]*kk[2]);
        hn = sqrt(nrm[0]*nrm[0]+nrm[1]*nrm[1]+nrm[2]*nrm[2]);
        for (int k = 0; k < 3; k++) { kk[k] /= kn; hh[k] = nrm[k]/hn; hk += hh[k]*kk[k]; }
        for (int k = 0; k < 3; k++) { u[k] = hh[k]-hk*kk[k]; un += u[k]*u[k]; }
        un = sqrt(un); for (int k = 0; k < 3; k++) sp[k] = cos(I)*kk[k] - sin(I)*u[k]/un;
      }
      double sr = sp[0]*r[0]+sp[1]*r[1]+sp[2]*r[2], r5 = r2*r2*sqrt(r2);
      for (int k = 0; k < 3; k++) { double g = -K*(2*sr*sp[k]/r5 - 5*sr*sr*r[k]/(r5*r2)); a[4][k] += GM[3]*g; a[3][k] -= GM[4]*g; }
      if (lfig >= 3) { // Cassini's first law: the Moon turns at its own steady rate, so its long axis points at the MEAN Earth, not the true one.
        // LFIG=1,2 took the long axis A along the Earth line. With the true body axes the C22 potential -3 C22 Rm^2 [(r.A)^2-(r.B)^2]/r^5 differs from that
        // by +6 C22 Rm^2 (r.B)^2/r^5, B = S x A the equatorial axis at right angles to the long axis. The rotation angle th is integrated with the orbit:
        // th'' = (6 C22 / 0.3929) GM_earth * 2 (r.A)(r.B) / r^5   (the Earth's torque on the bulge; (B-A)/C = 4 C22/0.3929, free libration 2.9 yr).
        const double C22 = 2.24e-5*lfac2, K3 = 6*C22*pow(1737.4/149597870.7,2);
        double eth[3] = {cos(s->th), sin(s->th), 0}, es = eth[0]*sp[0]+eth[1]*sp[1]+eth[2]*sp[2], A[3], B[3], an = 0;
        for (int k = 0; k < 3; k++) { A[k] = eth[k]-es*sp[k]; an += A[k]*A[k]; }
        an = sqrt(an); for (int k = 0; k < 3; k++) A[k] /= an;
        B[0] = sp[1]*A[2]-sp[2]*A[1]; B[1] = sp[2]*A[0]-sp[0]*A[2]; B[2] = sp[0]*A[1]-sp[1]*A[0];
        double ra = r[0]*A[0]+r[1]*A[1]+r[2]*A[2], rb = r[0]*B[0]+r[1]*B[1]+r[2]*B[2];
        for (int k = 0; k < 3; k++) { double g = -K3*(2*rb*B[k]/r5 - 5*rb*rb*r[k]/(r5*r2)); a[4][k] += GM[3]*g; a[3][k] -= GM[4]*g; }
        th_acc = (6*C22/0.3929)*GM[3]*2*ra*rb/r5;
      }
    }
    { // the in-phase (elastic) tides: each body's bulge, raised by the other, pulls the other back along the line. K2E, K2M are the Love numbers (0 = off; about 0.30 and 0.024)
      static double k2e = -1, k2m = -1; if (k2e < 0) { k2e = getenv("K2E") ? atof(getenv("K2E")) : 0; k2m = getenv("K2M") ? atof(getenv("K2M")) : 0; }
      if (k2e > 0 || k2m > 0) { double Rm = 1737.4/149597870.7, r8 = r2*r2*r2*r2, ce = 3*k2e*pow(Re,5)/r8, cm = 3*k2m*pow(Rm,5)/r8;
        for (int k = 0; k < 3; k++) { a[4][k] -= (ce*GM[4] + cm*GM[3]*GM[3]/GM[4])*r[k]; a[3][k] += (ce*GM[4]*GM[4]/GM[3] + cm*GM[3])*r[k]; } }
    }
    if (k2dt > 0) { // dissipative tide raised on Earth by the Moon, constant time lag (Mignard 1979)
      double v[3], rv = 0, w = 7.292115e-5*86400.0, wxr[3];
      for (int k = 0; k < 3; k++) { v[k] = s->v[4][k]-s->v[3][k]; rv += r[k]*v[k]; }
      wxr[0] = w*(p[1]*r[2]-p[2]*r[1]); wxr[1] = w*(p[2]*r[0]-p[0]*r[2]); wxr[2] = w*(p[0]*r[1]-p[1]*r[0]);
      double c = -3*k2dt*pow(Re,5)/pow(r2,5);
      for (int k = 0; k < 3; k++) { double g = c*(2*r[k]*rv + r2*(v[k]-wxr[k])); a[4][k] += GM[4]*g; a[3][k] -= GM[4]*GM[4]/GM[3]*g; }
    }
  }
  if (use_gr == 2) { // full Einstein-Infeld-Hoffmann point-mass 1PN (beta = gamma = 1), as in the JPL DE ephemerides
    static double an[N][3]; double pot[N], v2[N], da[N][3];
    memcpy(an, a, sizeof an); // Newtonian (+J2) accelerations for the a_j terms
    for (int i = 0; i < N; i++) { pot[i] = 0; v2[i] = 0;
      for (int k = 0; k < 3; k++) v2[i] += s->v[i][k]*s->v[i][k];
      for (int j = 0; j < N; j++) if (j != i) { double r2 = 0; for (int k = 0; k < 3; k++) { double d = s->x[i][k]-s->x[j][k]; r2 += d*d; } pot[i] += GM[j]/sqrt(r2); } }
    for (int i = 0; i < N; i++) { da[i][0]=da[i][1]=da[i][2]=0;
      for (int j = 0; j < N; j++) if (j != i && GM[j] > 0) {
        double d[3], r2 = 0, vivj = 0, dvj = 0, daj = 0, dvv = 0;
        for (int k = 0; k < 3; k++) { d[k] = s->x[j][k]-s->x[i][k]; r2 += d[k]*d[k]; vivj += s->v[i][k]*s->v[j][k];
          dvj += d[k]*s->v[j][k]; daj += d[k]*an[j][k]; dvv += -d[k]*(4*s->v[i][k]-3*s->v[j][k]); }
        double r = sqrt(r2), g = GM[j]/(r2*r);
        double br = -4*pot[i] - pot[j] + v2[i] + 2*v2[j] - 4*vivj - 1.5*dvj*dvj/r2 + 0.5*daj;
        for (int k = 0; k < 3; k++) da[i][k] += (g*(br*d[k] + dvv*(s->v[i][k]-s->v[j][k])) + 3.5*GM[j]*an[j][k]/r)/c2;
      } }
    for (int i = 0; i < N; i++) for (int k = 0; k < 3; k++) a[i][k] += da[i][k];
  }
  if (use_gr == 1) for (int i = 1; i < N; i++) {
    double r[3], v[3], r2=0, v2=0, rv=0;
    for (int k = 0; k < 3; k++) { r[k]=s->x[i][k]-s->x[0][k]; v[k]=s->v[i][k]-s->v[0][k]; r2+=r[k]*r[k]; v2+=v[k]*v[k]; rv+=r[k]*v[k]; }
    double rr = sqrt(r2), f = GM[0]/(c2*r2*rr);
    for (int k = 0; k < 3; k++) a[i][k] += f*((4*GM[0]/rr - v2)*r[k] + 4*rv*v[k]);
  }
}

// Gauss-Legendre s=3 coefficients
static double A[NS][NS], B[NS];
static void gl_init(void) {
  double s15 = sqrt(15.0);
  double a[3][3] = {{5.0/36, 2.0/9 - s15/15, 5.0/36 - s15/30},
                    {5.0/36 + s15/24, 2.0/9, 5.0/36 - s15/24},
                    {5.0/36 + s15/30, 2.0/9 + s15/15, 5.0/36}};
  memcpy(A, a, sizeof a); B[0]=5.0/18; B[1]=4.0/9; B[2]=5.0/18;
}
static State comp; // Kahan compensation
static void step(State *s, double dt) {
  static double KX[NS][N][3], KV[NS][N][3]; // stage derivatives: dx = v, dv = a
  static double KT[NS], KO[NS];             // the same for the Moon's rotation: dth = om, dom = th_acc
  static double KP[NS][3];                  // and for the Earth's pole: dp = p_dot
  static int warm = 0;
  State Y; double a[N][3];
  if (!warm) { accel(s, a); for (int q=0;q<NS;q++) { memcpy(KX[q], s->v, sizeof s->v); memcpy(KV[q], a, sizeof a); KT[q] = s->om; KO[q] = th_acc; memcpy(KP[q], p_dot, sizeof p_dot); } warm = 1; }
  for (int it = 0; it < 12; it++) {
    static double NX[NS][N][3], NV[NS][N][3]; double diff = 0, NT[NS], NO[NS], NP[NS][3];
    for (int q = 0; q < NS; q++) {
      for (int i = 0; i < N; i++) for (int k = 0; k < 3; k++) {
        double sx = 0, sv = 0;
        for (int p = 0; p < NS; p++) { sx += A[q][p]*KX[p][i][k]; sv += A[q][p]*KV[p][i][k]; }
        Y.x[i][k] = s->x[i][k] + dt*sx; Y.v[i][k] = s->v[i][k] + dt*sv;
      }
      { double st = 0, so = 0; for (int p = 0; p < NS; p++) { st += A[q][p]*KT[p]; so += A[q][p]*KO[p]; } Y.th = s->th + dt*st; Y.om = s->om + dt*so;
        for (int k = 0; k < 3; k++) { double sp_ = 0; for (int p = 0; p < NS; p++) sp_ += A[q][p]*KP[p][k]; Y.p[k] = s->p[k] + dt*sp_; } }
      accel(&Y, NV[q]); memcpy(NX[q], Y.v, sizeof Y.v); NT[q] = Y.om; NO[q] = th_acc; memcpy(NP[q], p_dot, sizeof p_dot);
    }
    for (int q=0;q<NS;q++) for (int i=0;i<N;i++) for (int k=0;k<3;k++) { double d = fabs(NV[q][i][k]-KV[q][i][k]); if (d > diff) diff = d; }
    memcpy(KX, NX, sizeof NX); memcpy(KV, NV, sizeof NV); memcpy(KT, NT, sizeof NT); memcpy(KO, NO, sizeof NO); memcpy(KP, NP, sizeof NP);
    if (diff < 1e-19) break;
  }
  for (int i = 0; i < N; i++) for (int k = 0; k < 3; k++) {
    double dx = 0, dv = 0;
    for (int q = 0; q < NS; q++) { dx += B[q]*KX[q][i][k]; dv += B[q]*KV[q][i][k]; }
    double y = dt*dx - comp.x[i][k], t = s->x[i][k] + y; comp.x[i][k] = (t - s->x[i][k]) - y; s->x[i][k] = t;
    y = dt*dv - comp.v[i][k]; t = s->v[i][k] + y; comp.v[i][k] = (t - s->v[i][k]) - y; s->v[i][k] = t;
  }
  if (dynpole) for (int k = 0; k < 3; k++) { double dp = 0; for (int q = 0; q < NS; q++) dp += B[q]*KP[q][k];
    double y = dt*dp - comp.p[k], t = s->p[k] + y; comp.p[k] = (t - s->p[k]) - y; s->p[k] = t; }
  if (lfig >= 3) { double dth = 0, dom = 0; for (int q = 0; q < NS; q++) { dth += B[q]*KT[q]; dom += B[q]*KO[q]; }
    double y = dt*dth - comp.th, t = s->th + y; comp.th = (t - s->th) - y; s->th = t; y = dt*dom - comp.om; t = s->om + y; comp.om = (t - s->om) - y; s->om = t; }
}
static double energy(const State *s) { // Newtonian energy (units of GM)
  double e = 0;
  for (int i=0;i<N;i++) { double v2=0; for(int k=0;k<3;k++) v2+=s->v[i][k]*s->v[i][k]; e += 0.5*GM[i]*v2;
    for (int j=i+1;j<N;j++){ double r2=0; for(int k=0;k<3;k++){double d=s->x[i][k]-s->x[j][k]; r2+=d*d;} e -= GM[i]*GM[j]/sqrt(r2);} }
  return e;
}
static void peri(const State *s, double t) { // Mercury heliocentric osculating elements
  double r[3], v[3], h[3], e[3], mu = GM[0]+GM[1], rr=0, v2=0, rv=0;
  for (int k=0;k<3;k++){ r[k]=s->x[1][k]-s->x[0][k]; v[k]=s->v[1][k]-s->v[0][k]; rr+=r[k]*r[k]; v2+=v[k]*v[k]; rv+=r[k]*v[k]; }
  rr = sqrt(rr);
  h[0]=r[1]*v[2]-r[2]*v[1]; h[1]=r[2]*v[0]-r[0]*v[2]; h[2]=r[0]*v[1]-r[1]*v[0];
  for (int k=0;k<3;k++) e[k] = ((v2-mu/rr)*r[k]-rv*v[k])/mu;
  double ecc = sqrt(e[0]*e[0]+e[1]*e[1]+e[2]*e[2]);
  double nx=-h[1], ny=h[0], nn=sqrt(nx*nx+ny*ny);
  double Om = atan2(ny,nx);
  double cw = (nx*e[0]+ny*e[1])/(nn*ecc), w = acos(cw); if (e[2]<0) w = -w;
  double inc = acos(h[2]/sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2]));
  double a = 1.0/(2.0/rr - v2/mu);
  printf("%.6f %.6f %.12f %.12f %.6f %.6f\n", t/365.25, (Om+w)*206264.806247, ecc, a, Om*206264.806247, inc*206264.806247);
}
static double wlo[32], whi[32]; static int nwin = 0;     // OUTWINDOWS="lo:hi,lo:hi,..." in days since J2000: print only inside these
static int in_windows(double t) { if (!nwin) return 1; for (int i = 0; i < nwin; i++) if (t >= wlo[i] && t <= whi[i]) return 1; return 0; }
int main(int argc, char **argv) {
  if (argc < 7) { fprintf(stderr,"usage\n"); return 1; }
  State s; FILE *f = fopen(argv[1],"r");
  for (int i=0;i<N;i++) if (fscanf(f,"%lf %lf %lf %lf %lf %lf",&s.x[i][0],&s.x[i][1],&s.x[i][2],&s.v[i][0],&s.v[i][1],&s.v[i][2])!=6) return 2;
  double years=atof(argv[2]), dt=atof(argv[3]); use_gr=atoi(argv[4]); double every=atof(argv[5]); const char *mode=argv[6];
  for (int i=0;i<N;i++) GM[i]=GMkm[i]*DAY*DAY/(AU*AU*AU);
  if (getenv("NONEPTUNE")) GM[9]=0;
  if (getenv("GMFAC")) { char *p=getenv("GMFAC"); for (int i=0;i<N;i++) { GM[i]*=strtod(p,&p); if (*p==',') p++; } }
  use_j2 = getenv("J2")!=NULL; if (getenv("TIDE")) k2dt = atof(getenv("TIDE"))/86400.0;
  lfig = getenv("LFIG") ? atoi(getenv("LFIG")) : 0;
  dynpole = getenv("POLE") ? atoi(getenv("POLE")) : 0; if (getenv("HDYN")) hdyn = atof(getenv("HDYN"));
  { // the pole at J2000: obliquity 23.4392911 deg + DEPS0 arcsec, ecliptic longitude 90 deg - DPSI0 arcsec (DPSI0, DEPS0: the nutation at the epoch, so that the MEAN pole is where it should be)
    double e0 = 23.4392911*M_PI/180 + (getenv("DEPS0") ? atof(getenv("DEPS0")) : 0)/206264.806247, l0 = M_PI/2 - (getenv("DPSI0") ? atof(getenv("DPSI0")) : 0)/206264.806247;
    s.p[0] = sin(e0)*cos(l0); s.p[1] = sin(e0)*sin(l0); s.p[2] = cos(e0); }
  s.th = 218.326443502*M_PI/180; s.om = 481313.40834159*M_PI/180/36525.0;  // rotation angle and rate at J2000 (deg, deg/cy), tuned by src/lib_ic.py so that the free libration is not excited (mean longitude 218.3164477, mean motion 481266.48434638 plus the forced terms); TH0, OM0 override
  if (getenv("TH0")) s.th = atof(getenv("TH0"))*M_PI/180; if (getenv("OM0")) s.om = atof(getenv("OM0"))*M_PI/180/36525.0;
  FILE *lib = getenv("LIBOUT") ? fopen(getenv("LIBOUT"), "w") : NULL;     // days since J2000, rotation angle (rad), rate (rad/day), Moon's geocentric true longitude (rad)
  c2 = pow(CKM*DAY/AU,2); gl_init();
  long nsteps = lround(years*365.25/fabs(dt)), oe = lround(every/fabs(dt));
  double outfrom = getenv("OUTFROM") ? atof(getenv("OUTFROM")) : -1e300;
  if (getenv("OUTWINDOWS")) { char *p = getenv("OUTWINDOWS"); while (*p && nwin < 32) { wlo[nwin] = strtod(p, &p); if (*p == ':') p++; whi[nwin] = strtod(p, &p); nwin++; if (*p == ',') p++; } }   // only print from this many days after J2000
  if (getenv("ACCIN")) { // force check: read states (jd, 11 x (x y z vx vy vz), th, p[3]) one epoch per line and print what this model says the accelerations of the Earth and Moon are there
    FILE *fa = fopen(getenv("ACCIN"), "r"); double jd, acc[N][3];
    while (fa && fscanf(fa, "%lf", &jd) == 1) {
      for (int i = 0; i < N; i++) if (fscanf(fa, "%lf %lf %lf %lf %lf %lf", &s.x[i][0], &s.x[i][1], &s.x[i][2], &s.v[i][0], &s.v[i][1], &s.v[i][2]) != 6) return 3;
      if (fscanf(fa, "%lf %lf %lf %lf", &s.th, &s.p[0], &s.p[1], &s.p[2]) != 4) return 3;
      tcur = jd - 2451545.0; accel(&s, acc);
      printf("%.9f %.17e %.17e %.17e %.17e %.17e %.17e\n", jd, acc[3][0], acc[3][1], acc[3][2], acc[4][0], acc[4][1], acc[4][2]);
    }
    return 0;
  }
  double e0 = energy(&s);
  for (long n = 0; n <= nsteps; n++) {
    if (n % oe == 0 && n*dt >= outfrom && in_windows(n*dt)) {
      double t = n*dt;
      if (!strcmp(mode,"peri")) peri(&s,t);
      else for (int i=0;i<N;i++) printf("%.2f %d %.15e %.15e %.15e %.15e %.15e %.15e\n", 2451545.0+t, i, s.x[i][0],s.x[i][1],s.x[i][2],s.v[i][0],s.v[i][1],s.v[i][2]);
      if (lib) fprintf(lib, "%.2f %.12f %.15e %.12f %.15e %.15e %.15e\n", t, s.th, s.om, atan2(s.x[4][1]-s.x[3][1], s.x[4][0]-s.x[3][0]), s.p[0], s.p[1], s.p[2]);
    }
    tcur = n*dt; step(&s, dt);
  }
  fprintf(stderr,"dE/E = %.3e\n", (energy(&s)-e0)/fabs(e0));
  return 0;
}
