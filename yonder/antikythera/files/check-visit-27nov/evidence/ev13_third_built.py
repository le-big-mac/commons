"""Third evidence reading: the third candidate as built (the file only; the builder is not loaded this time).
usage: python ev13_third_built.py SOURCE PREVIEW ; prints, writes nothing."""
import html, re, sys
src, pv = (open(p, encoding='utf-8').read() for p in sys.argv[1:3])
def letters(h):
    h = re.sub(r'<script>.*?</script>', ' ', h, flags=re.S)
    return ''.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())
body = pv[pv.index('<h1'):pv.index('<footer>')]
print('letters in order, source against the built body (full-size links apart):', letters(src) == letters(body).replace('Seethepictureatfullsize.', ''))
names = set(re.findall(r'<h2[^>]*>(.*?)</h2>', body)) | set(re.findall(r'<summary>(.*?)</summary>', body))
def where(i):
    stack = []
    for m in re.finditer(r'<details[^>]*>\n?<summary>(.*?)</summary>|</details>', body[:i], flags=re.S):
        if m.group(0).startswith('</'): stack.pop()
        else: stack.append(m.group(1))
    return ' > '.join(stack) or 'open text'
links = [(m.start(), m.group(1), m.group(2)) for m in re.finditer(r'<a class="tosec" href="#([^"]*)">(.*?)</a>', body)]
print(len(links), 'section links:')
for i, t, x in links:
    print(f'   {x:40s} target present: {bool(re.search(chr(34) + re.escape(t) + chr(34), body.replace("href=" + chr(34) + "#" + t + chr(34), "")))}; stands in: {where(i)}')
blank = re.sub(r'<a class="tosec".*?</a>', lambda m: ' ' * len(m.group(0)), body)
print('names of the page\'s own sections in quotation marks that are not links:')
for m in re.finditer(r'(?<!>)"([^"<>]{3,60})"', blank):
    if m.group(1) in names:
        print(f'   "{m.group(1)}" in: {where(m.start())}')
print('placeholders left:', re.findall(r'TODO[^.<;]*', body))
print('folds:', re.findall(r'<details class="([^"]*)" id="([^"]*)"', body))
