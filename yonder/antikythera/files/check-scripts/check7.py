"""Jupiter and Saturn: arithmetic from JPL Table 2a rates plus the long-period terms of its Table 2b
(b T^2 + c cos(fT) + s sin(fT); coefficients typed from memory of that table), beside the measured drift."""
import math
LR = {'earth': 35999.37306329, 'jupiter': 3034.90371757, 'saturn': 1222.11494724}
T2B = {'jupiter': (-0.00012452, 0.06064060, -0.35635438, 38.35125), 'saturn': (0.00025899, -0.13434469, 0.87320147, 38.35125)}
G = {'jupiter': 315 / 344, 'saturn': 427 / 442}
TA, TB = 1646667.5, 2461368.0
Ta, Tb = (TA - 2451545.0) / 36525, (TB - 2451545.0) / 36525
turns = LR['earth'] * (Tb - Ta) / 360
print(f'T then {Ta:.4f}, now {Tb:.4f} centuries from J2000; turns of the Sun by the Table 2a rate {turns:.5f}')
for p in ('jupiter', 'saturn'):
    b, c, s, f = T2B[p]
    extra = lambda T: b * T * T + c * math.cos(math.radians(f * T)) + s * math.sin(math.radians(f * T))
    lin = LR[p] * (Tb - Ta)
    gear = 360 * (1 - G[p]) * turns
    print(f'{p}: gears {gear:.3f}; sky linear {lin:.3f} -> drift {gear - lin:+.3f}; long-period terms then {extra(Ta):+.4f}, now {extra(Tb):+.4f}; drift with them {gear - lin - (extra(Tb) - extra(Ta)):+.3f}')
