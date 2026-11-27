"""Item 1, the moved pieces in the BUILT pages: letters in order, spaces and tags apart (the links put round section names add tags, not words).
usage: kept2.py OLD_SOURCE OLD_BUILT NEW_BUILT"""
import re, sys, html
old_src, old_built, new_built = (open(p, encoding='utf-8').read() for p in sys.argv[1:4])
letters = lambda h: ''.join(html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', ' ', h, flags=re.S))).split())
m = re.search(r'<p>(You can <a href="files/bed\.html">open the bed</a> and try it\. It starts running by itself, with 3% of moves slipping, .*? it got in only by way of other machines\.)</p>\n', old_src, re.S)
m2 = re.search(r'<p class="small">(The live page and the short story among the files still call the machine the handshake\.) (Two fresh copies of the model read this page before it went up: .*?made by stepping the same machines\.)</p>\n', old_src, re.S)
for name, piece in (('the paragraph on trying the live page', m.group(1)), ('the account of the readings', m2.group(2))):
    L = letters(piece)
    print(name, ': in old built page', letters(old_built).count(L), 'time(s); in new built page', letters(new_built).count(L), 'time(s)')
    # where in the new built page: inside which details
    body = new_built
    for d in re.finditer(r'<details[^>]*>\n?<summary>(.*?)</summary>(.*?)</details>', body, re.S):
        if L in letters(d.group(2)): print('    in the new built page it is inside the folded section headed:', repr(d.group(1)))
    open_part = re.sub(r'<details.*?</details>', ' ', body, flags=re.S)
    print('    in the open text of the new built page:', letters(open_part).count(L), 'time(s)')
# order of the folded sections in the new built page
print('folded sections of the new built page, in order:', re.findall(r'<details[^>]*>\n?<summary>(.*?)</summary>', new_built))
print('folded sections of the old built page, in order:', re.findall(r'<details[^>]*>\n?<summary>(.*?)</summary>', old_built))
# section names in quotation marks in the open text of the new built page: links or not
open_part = re.sub(r'<details.*?</details>', ' ', new_built[new_built.index('<h1'):new_built.index('<script')], flags=re.S)
names = re.findall(r'<h2[^>]*>(.*?)</h2>', new_built) + re.findall(r'<summary>(.*?)</summary>', new_built)
for n in names:
    q = '"' + n + '"'
    linked = len(re.findall(r'<a class="tosec"[^>]*>' + re.escape(q) + '</a>', open_part)); total = open_part.count(q)
    if total: print(f'open text names {q}: {total} time(s), of which a link: {linked}')
# and the link targets exist
for href in sorted(set(re.findall(r'class="tosec" href="#([^"]+)"', new_built))):
    print('link target', href, 'exists as an id:', ('id="' + href + '"') in new_built)
