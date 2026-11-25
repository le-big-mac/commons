# The chronometers the French carried from Wha-Tonne to Saigon (Stephan's report, pp. 148-150, read from the page images): a check on their clock and their place.
# Chronometer 484, set to sidereal time, was +6h30m02.6s on Wha-Tonne's sidereal time and +6h57m50.25s on Saigon's, so Saigon is 27m47.6s of time east of Wha-Tonne.
# That difference rests on the French determination of local time at both places and on the chronometer, and not at all on anyone's tables of the Moon.
# A look made after the 10-second gap was known; not a sealed test.
paris = 2 + 20 / 60 + 14 / 3600; dl = (6 + 57 / 60 + 50.25 / 3600 - (6 + 30 / 60 + 2.6 / 3600)) * 15
print(f'Saigon minus Wha-Tonne by chronometer: {dl * 240:.2f} s of time = {dl:.4f} deg')
print(f'French figures: Wha-Tonne adopted {(6 + 29 / 60 + 47.5 / 3600) * 15 + paris:.4f} E; Saigon {(6 + 57 / 60 + 35.1 / 3600) * 15 + paris:.4f} E, {10 + 46 / 60 + 47.2 / 3600:.4f} N')
places = (('Ba Son, the old naval arsenal on the river (OpenStreetMap)', 106.7085), ('the river-front park at Bach Dang', 106.7066), ('the botanical garden', 106.7063))
print('modern longitudes on the Saigon river front: ' + '; '.join(f'{n} {l:.4f} E' for n, l in places))
for name, lon in (('at the memorial at Wa Ko', 99.7588), ("where Tisserand's contact times put it, were the French clock right", 99.7317)):
    s = lon + dl; print(f'if the camp was {name} ({lon:.4f} E): the Saigon observatory was at {s:.4f} E, {(s - 106.7085) * 240:+.1f} s of time ({(s - 106.7085) * 109.3:+.1f} km) from Ba Son')
print(f'the French Saigon longitude is {((6 + 57 / 60 + 35.1 / 3600) * 15 + paris - 106.7071) * 240:.1f} s of time east of 106.7071 E, as their Wha-Tonne one is {((6 + 29 / 60 + 47.5 / 3600) * 15 + paris - 99.7588) * 240:.1f} s east of the memorial (the same error carried over)')
