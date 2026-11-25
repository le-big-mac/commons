"""run.py: every text through cells.py, in Unified English Braille and in English Braille American Edition; one record a book.
    /usr/bin/python3 -I run.py ~/braille-data/texts OUTDIR [WORKERS] [story]      (with "story": each text cut to its story, by story.py)"""
import json, os, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cells, story
BOOKS = [  # (era, folder, title, year)
    (1, 'austen-pride-1813', 'Pride and Prejudice', 1813), (1, 'shelley-frankenstein-1818', 'Frankenstein', 1818), (1, 'bronte-jane-eyre-1847', 'Jane Eyre', 1847),
    (1, 'melville-moby-dick-1851', 'Moby-Dick', 1851), (1, 'dickens-great-1861', 'Great Expectations', 1861), (1, 'eliot-middlemarch-1871', 'Middlemarch', 1871),
    (2, 'conrad-lord-jim-1900', 'Lord Jim', 1900), (2, 'wharton-age-of-innocence-1920', 'The Age of Innocence', 1920), (2, 'christie-styles-1920', 'The Mysterious Affair at Styles', 1920),
    (2, 'lewis-babbitt-1922', 'Babbitt', 1922), (2, 'fitzgerald-gatsby-1925', 'The Great Gatsby', 1925), (2, 'hemingway-sun-1926', 'The Sun Also Rises', 1926),
    (3, 'hoover-daedalus-1991', 'Project Daedalus', 1991), (3, 'hoover-life-blood-2000', 'Life Blood', 2000), (3, 'hoover-syndrome-2003', 'Syndrome', 2003),
    (3, 'doctorow-down-and-out-2003', 'Down and Out in the Magic Kingdom', 2003), (3, 'doctorow-little-brother-2008', 'Little Brother', 2008), (3, 'doctorow-makers-2009', 'Makers', 2009),
    (0, 'kjv-1611', 'The King James Bible', 1611),
]
NEW = [   # the third sheet: two old novels in a colloquial voice (4) and two recent books of exposition by the author of three of the last six novels (5)
    (4, 'twain-huck-finn-1884', 'Adventures of Huckleberry Finn', 1884), (4, 'jerome-three-men-1889', 'Three Men in a Boat', 1889),
    (5, 'hoover-zen-culture-1977', 'Zen Culture', 1977), (5, 'hoover-zen-experience-1980', 'The Zen Experience', 1980),
]
def one(job):
    root, out, (era, folder, title, year), only = job
    trim = None if not only else story.trim(folder) if only != 'expand' else (lambda ps, f=folder: [story.expand(p) for p in story.trim(f)(ps)])
    d = os.path.join(root, folder); path = os.path.join(d, [f for f in os.listdir(d) if f.endswith('.txt')][0])
    rec = dict(era=era, folder=folder, title=title, year=year, ueb=cells.book(path, cells.UEB, cells.G1, trim), ebae=cells.book(path, cells.EBAE, cells.EBAE1, trim))
    json.dump(rec, open(os.path.join(out, folder + '.json'), 'w')); u = rec['ueb']
    return '%-36s %7d words  UEB %.2f%%  EBAE %.2f%%' % (title, u['words'], 100 * (u['U'] - u['C']) / u['U'], 100 * (rec['ebae']['U'] - rec['ebae']['C']) / rec['ebae']['U'])
if __name__ == '__main__':
    root, out = os.path.expanduser(sys.argv[1]), sys.argv[2]; os.makedirs(out, exist_ok=True); workers = int(sys.argv[3]) if len(sys.argv) > 3 else 6; only = sys.argv[4] if len(sys.argv) > 4 else ''          # '' the files as sent; 'story' the stories alone; 'expand' the stories with the shortened forms written out; 'new' the four added texts, stories alone
    with Pool(workers) as pool:
        for line in pool.imap(one, [(root, out, b, 'story' if only == 'new' else only) for b in (NEW if only == 'new' else BOOKS)]): print(line, flush=True)
