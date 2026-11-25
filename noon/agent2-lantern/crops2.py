"""crops2.py: the crops of the scans that the second sheet rests on, each with a ruler in the scan's own pixels and my reading of each
pivot marked (the places are after2.py's).      python -I crops2.py ~/lantern-data  ->  afterlife-crops/*.png
The scans: the Britannica's seventh edition, vol. 16, leaf 523 (p. 514) and leaf 824 (Plate CCCLXXXVI); the eighth edition, vol. 16,
leaf 704 (p. 697); Brewster's Letters on Natural Magic (1832), leaf 103 (p. 83); Hutton's Dictionary (1815), vol. 2, leaf 189 (p. 182). All from the Internet Archive (sources.md)."""
import os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import after2
OUT = os.path.join(HERE, 'afterlife-crops')
SCANS = {'hutton': 'hutton-page/leaf-0189.jp2', 'eb7-page': 'eb7/leaf-0523.jp2', 'eb7-plate': 'eb7/leaf-0824.jp2', 'eb8-page': 'eb8-pages/leaf-0704.jp2', 'brewster-1832': 'brewster-1832/leaf-0103.jp2'}
PLACES = {'eb7-plate': "the Britannica's plate, seventh edition (Plate CCCLXXXVI, Fig. 110)", 'eb8-page': "the Britannica's woodcut, eighth edition (vol. 16, p. 697, Fig. 282)",
          'brewster-1832': "Brewster's woodcut, 1832 (Letters on Natural Magic, p. 83, Fig. 6)"}
CROPS = [   # (scan, name, box, magnification, ruler step or None)
    ('hutton', 'hutton-1815-p182', (0, 0, 2500, 3328), 0.36, None),
    ('hutton', 'hutton-1815-must-be-equal', (360, 1590, 1260, 1770), 2, None),
    ('eb7-page', 'eb7-p514', (0, 0, 3045, 4274), 0.25, None),
    ('eb7-page', 'eb7-p514-must-be-equal', (1640, 960, 3020, 1240), 1, None),
    ('eb7-plate', 'eb7-plate', (0, 0, 3284, 4311), 0.25, None),
    ('eb7-plate', 'eb7-fig110', (240, 3180, 3000, 4080), 0.5, None),
    ('eb7-plate', 'eb7-fig110-IL', (780, 3610, 1040, 3790), 4, 50),
    ('eb7-plate', 'eb7-fig110-K', (2150, 3220, 2400, 3400), 4, 50),
    ('eb7-plate', 'eb7-fig110-N', (2680, 3690, 2900, 3850), 4, 50),
    ('eb8-page', 'eb8-p697', (0, 0, 3274, 4284), 0.25, None),
    ('eb8-page', 'eb8-p697-must-be-equal', (230, 3330, 1520, 3500), 1, None),
    ('eb8-page', 'eb8-fig282', (200, 880, 2800, 1760), 0.5, None),
    ('eb8-page', 'eb8-fig282-IL', (740, 1340, 940, 1480), 5, 20),
    ('eb8-page', 'eb8-fig282-K', (2040, 940, 2240, 1080), 5, 20),
    ('eb8-page', 'eb8-fig282-N', (2600, 1410, 2780, 1540), 5, 20),
    ('brewster-1832', 'brewster-1832-p83', (0, 0, 2038, 3480), 1 / 3.0, None),
    ('brewster-1832', 'brewster-1832-fig6', (100, 1000, 1900, 1900), 0.6, None),
    ('brewster-1832', 'brewster-1832-fig6-K', (1060, 1040, 1260, 1200), 5, 20),
    ('brewster-1832', 'brewster-1832-fig6-IL', (860, 1540, 1060, 1700), 5, 20),
    ('brewster-1832', 'brewster-1832-fig6-N', (1260, 1540, 1440, 1680), 5, 20),
]
if __name__ == '__main__':
    root = sys.argv[1]; os.makedirs(OUT, exist_ok=True); cache = {}
    for scan, name, box, k, step in CROPS:
        im = cache.setdefault(scan, Image.open(os.path.join(root, SCANS[scan])).convert('L'))
        c = im.crop(box).resize((int(round((box[2] - box[0]) * k)), int(round((box[3] - box[1]) * k))), Image.LANCZOS).convert('RGB'); d = ImageDraw.Draw(c)
        if step:
            for x in range(box[0] - box[0] % step + step, box[2], step): d.line([((x - box[0]) * k, 0), ((x - box[0]) * k, 10)], fill=(200, 0, 0)); d.text(((x - box[0]) * k + 2, 10), str(x), fill=(200, 0, 0))
            for y in range(box[1] - box[1] % step + step, box[3], step): d.line([(0, (y - box[1]) * k), (10, (y - box[1]) * k)], fill=(200, 0, 0)); d.text((12, (y - box[1]) * k - 5), str(y), fill=(200, 0, 0))
        if scan in PLACES and (step or 'fig' in name):
            P = after2.DRAWINGS[PLACES[scan]]
            for lab in 'ILKN':
                px, py = P[lab]
                if box[0] <= px <= box[2] and box[1] <= py <= box[3]:
                    X, Y = (px - box[0]) * k, (py - box[1]) * k; r = 9 if step else 5
                    d.line([(X - r, Y), (X + r, Y)], fill=(235, 104, 52), width=2); d.line([(X, Y - r), (X, Y + r)], fill=(235, 104, 52), width=2)
        c.save(os.path.join(OUT, name + '.png')); print(name, c.size)
