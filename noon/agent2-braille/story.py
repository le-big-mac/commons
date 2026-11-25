"""story.py: the story alone. For each text, where the story begins and where it ends, found by reading the head and foot
of each cleaned file after the referee's blind step showed how much else the files hold: a preface of 1894 in Pride and
Prejudice, an author's note of 1917 in Lord Jim, publishers' pages, blurbs, lists of other books, licences, afterwords
by other hands, acknowledgements. The sealed design cut only Project Gutenberg's own head and foot.
    trim(folder)(paragraphs) -> the paragraphs from the first that matches the start to the one before the last that
    matches the end, less paragraphs with no letter in them (rules, "* * *", "#"), less Little Brother's dedications
    of each chapter to a bookshop and the shop's address after each (paragraphs in double square brackets; the
    referee found that I had first cut only the dedications), and with the rules of = taken off Down and Out's headings."""
import re
STORY = {   # folder: (the story's first paragraph, the first paragraph after the story or None if it runs to the end)
    'austen-pride-1813': (r'^It is a truth universally acknowledged', r'^CHISWICK PRESS'),
    'shelley-frankenstein-1818': (r'^Letter 1$', None),
    'bronte-jane-eyre-1847': (r'^CHAPTER I$', None),
    'melville-moby-dick-1851': (r'^Call me Ishmael', None),
    'dickens-great-1861': (r"^My father's family name being Pirrip", None),
    'eliot-middlemarch-1871': (r'^Who that cares much to know the history of man', r'^THE END$'),
    'conrad-lord-jim-1900': (r'^He was an inch, perhaps two, under six feet', r'^September 1899'),
    'wharton-age-of-innocence-1920': (r'^On a January evening of the early seventies', r'^A Note on the Text'),
    'christie-styles-1920': (r'^The intense interest aroused in the public', r'^THE END$'),
    'lewis-babbitt-1922': (r'^The towers of Zenith aspired', None),
    'fitzgerald-gatsby-1925': (r'^In my younger and more vulnerable years', None),
    'hemingway-sun-1926': (r'^Robert Cohn was once middleweight boxing champion', r'^THE END$'),
    'hoover-daedalus-1991': (r'^PROLOGUE$', r'^BOOKS BY THOMAS HOOVER'),
    'hoover-life-blood-2000': (r'^Chapter One$', r'^BOOKS BY THOMAS HOOVER'),
    'hoover-syndrome-2003': (r'^Chapter 1$', r'^Afterword$'),
    'doctorow-down-and-out-2003': (r'^=+ PROLOGUE =+$', r'^=+ Acknowledgements'),
    'doctorow-little-brother-2008': (r'^Chapter 1$', r'^Afterword by Bruce Schneier'),
    'doctorow-makers-2009': (r'^PART I$', r'^Acknowledgements:'),
    'kjv-1611': (r'^1:1 In the beginning God created', None),
    # four texts added for the third sheet; their boundaries were set from their heads and feet before any was translated
    'twain-huck-finn-1884': (r'^CHAPTER I\.$', r'^THE END\. YOURS TRULY'),
    'jerome-three-men-1889': (r'^CHAPTER I\.$', r'^Footnotes\.$'),
    'hoover-zen-culture-1977': (r'^CHAPTER ONE$', r'^References$'),
    'hoover-zen-experience-1980': (r'^PREFACE TO ZEN$', r'^NOTES$'),
}
SHORT = [(r"\bcan't\b", 'cannot'), (r"\bwon't\b", 'will not'), (r"\bshan't\b", 'shall not'), (r"n't\b", ' not'), (r"'ll\b", ' will'), (r"'ve\b", ' have'), (r"'re\b", ' are'),
         (r"'d\b", ' would'), (r"\bI'm\b", 'I am')]
def expand(par):
    """the shortened forms of speech written out, crudely (the referee's experiment): 'd is always would, ain't becomes ai not, and 's is left alone"""
    for a, b in SHORT: par = re.sub(a, lambda m, b=b: b.capitalize() if m.group(0)[0].isupper() and b[0] != ' ' else b, par, flags=re.I)
    return par
def short_forms(vocab):
    """how many of a book's words are such shortened forms (from its vocabulary count)"""
    return sum(n for w, n in vocab.items() if re.search(r"(n't|'ll|'ve|'re|'d|'m)$", w))
def trim(folder):
    start, end = STORY[folder]
    def f(paras):
        a = [i for i, p in enumerate(paras) if re.search(start, p)]; assert a, ('the story\'s first paragraph is not found', folder)
        if end is None: b = len(paras)
        else:
            hits = [i for i, p in enumerate(paras) if re.search(end, p) and i > a[0]]; assert hits, ('the paragraph after the story is not found', folder); b = hits[-1]
        return [re.sub(r'^=+ (.*?) =+$', r'\1', p) for p in paras[a[0]:b] if any(ch.isalpha() for ch in p) and not p.startswith('[[')]
    return f
