import math
# 1. Brier
odds = dict(K1=.85,K2=.80,K3=.75,K4=.70,K5=.80,K6=.85,K7=.80,K8=.90,K9=.85,K10=.85,K11=.80,K12=.80,K13a=.80,K13b=.65,K14=.80,K15=.80,K16a=.70,K16b=.70,K17a=.70,K17b=.75,K18=.60,K19a=.45,K19b=.75,K20=.85)
failed = {'K11','K19b'}
b = sum(((1 if k not in failed else 0)-p)**2 for k,p in odds.items())/len(odds)
print('lines', len(odds), 'Brier %.4f' % b, 'always 50%% %.4f' % 0.25, 'always 90%% %.4f' % ((22*0.01+2*0.81)/24), 'always 22/24 %.4f' % ((22*(1-22/24)**2+2*(22/24)**2)/24))
# 2. rms now / floor
for p, now, fl in (('mercury',4.690,4.2271),('mars',11.669,9.5623),('jupiter',4.418,3.6651),('venus',10.437,1.4818),('saturn',9.260,4.9654)):
    print(p, 'worse by %.1f%%' % (100*(now/fl-1)))
# 3. Moon
print('360-262.154 =', 360-262.154)
# 4. Saturn columns
print('0.004208*442/427 = %.6f ; *(442/427)^2 = %.6f' % (0.004208*442/427, 0.004208*(442/427)**2))
for p,(n,y),ey,es in (('mercury',(1513,480),-0.005022,-0.001593),('venus',(289,462),0.008576,0.013710),('mars',(133,284),0.003089,0.006596),('jupiter',(315,344),0.000802,0.000876),('saturn',(427,442),0.004208,0.004509)):
    print('  %-8s e_y*y/n %.6f printed %.6f' % (p, ey*y/n, es))
# 5. implied synodic periods, sidereal year
Y = 365.256363
LR = {'mercury': 149472.67486623, 'venus': 58517.81560260, 'earth': 35999.37306329, 'mars': 19140.29934243, 'jupiter': 3034.90371757, 'saturn': 1222.11494724}
for p,(n,y),ey in (('mercury',(1513,480),-0.005022),('venus',(289,462),0.008576),('mars',(133,284),0.003089),('jupiter',(315,344),0.000802),('saturn',(427,442),0.004208)):
    s = n/y - ey/360
    jpl = 36525*360/abs(LR[p]-LR['earth'])
    print('  %-8s implied %.4f  (if error per Julian year: %.4f)   JPL %.4f' % (p, Y/s, Y/(n/y - ey/360*Y/365.25), jpl))
# 6. eclipse arithmetic
syn, dra = 29.530588853, 27.212220817
d = 223*syn - 242*dra
print('223 syn - 242 dra = %.5f d = %.4f deg; x123 = %.2f; x123.2 = %.2f; x122.7 %.2f, x123.7 %.2f' % (d, d/dra*360, d/dra*360*123, d/dra*360*123.2, d/dra*360*122.7, d/dra*360*123.7))
for k in (43, 125, 131, 178, 88, 135, 180):
    print('  %d lunations: %.2f deg mod 180' % (k, (k*syn/dra*360) % 180))
# with slowly changing months: mean of then and now? use Chapront-ish: synodic month at -200: 29.5305888-? skip
# 7. dial by the Sun
print('gears lunations S %.3f T %.3f; sky %.3f' % (2230.48955*235/19, 2230.57569*235/19, 814700.5/(0.5*(29.530589+29.530586))))
# 8. epicycle
print('0.64957/0.64325 = %.4f' % (0.64957/0.64325))
# 9. fraction of span after gears overtake
for nm, yv in (('venus',309.9),('saturn after.out',1122.0),('saturn check5',1117.5),('saturn README',1100)):
    print('  %s: gears larger for %.1f%% of 2230.5 y' % (nm, 100*(2230.5-yv)/2230.5))
# 10. precession
print('31.0103/2230.53*100 = %.4f deg per century' % (31.0103/2230.53*100))
# 11. Mercury sidereal check: 2 ppm of period -> deg
print('Mercury: turns in 2230.5 y %.1f; 2e-6 x that x 360 = %.2f deg' % (2230.5*365.25636/87.96926, 2e-6*2230.5*365.25636/87.96926*360))
