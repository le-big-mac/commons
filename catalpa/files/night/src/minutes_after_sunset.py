# How long after sunset (the Sun's upper edge on the horizon, altitude -0.833 degrees) the Sun is 3, 7 and 10 degrees
# down, at the latitudes of the southern places (21 to 41 south) at the solstices and equinoxes. Plain spherical
# astronomy; for the story's "a quarter of an hour", "half an hour" and "three quarters of an hour".
import math
def minutes(lat, dec, alt):
    f = lambda a: math.degrees(math.acos((math.sin(math.radians(a)) - math.sin(math.radians(lat)) * math.sin(math.radians(dec))) / (math.cos(math.radians(lat)) * math.cos(math.radians(dec)))))
    return (f(alt) - f(-0.833)) * 4.0
for alt in (-3.0, -7.0, -10.0):
    v = [minutes(lat, dec, alt) for lat in (-21.0, -31.0, -41.0) for dec in (-23.44, 0.0, 23.44)]
    print(f'the Sun {-alt:g} degrees down: {min(v):.0f} to {max(v):.0f} minutes after sunset (latitudes 21, 31 and 41 south; solstices and equinox); at 31 south at the equinox {minutes(-31.0, 0.0, alt):.0f}')
