"""Contrast of a number in ink and in the paper's colour against each shade of the map (the usual ratio of relative luminances, 1 to 21)."""
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
SHADES = ['#113e79', '#1d5aa6', '#2e77d0', '#5297e8', '#84b5f0', '#b4d2f7', '#dcebfc']       # darkest first, as shading.py works them out from the program's colours
NAMES = ['under 0.01', '0.01 to 0.05', '0.05 to 0.1', '0.1 to 0.2', '0.2 to 0.4', '0.4 to 0.8', 'over 0.8']
print('shade (loss)            ink #0b0b0b   paper #fcfcfb')
for s, n in zip(SHADES, NAMES): print(f'{s} {n:14s}   {ratio(s, "#0b0b0b"):5.1f}         {ratio(s, "#fcfcfb"):5.1f}')
print('the number 0.01 stands between the first two shades, 0.05 between the second and third, 0.1 between the third and fourth')
