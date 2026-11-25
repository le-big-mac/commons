import re, sys, html
t = open(sys.argv[1], encoding='utf-8', errors='replace').read()
t = re.sub(r'(?is)<(script|style).*?</\1>', ' ', t)
t = re.sub(r'(?s)<[^>]+>', ' ', t)
t = html.unescape(t); t = re.sub(r'\s+', ' ', t)
i = t.find('How Much of Humanity is on Your Side of World? Last Updated')
j = t.find('Comments Anthony')
print(t[i:j][:3500])
print('-----')
for w in ('LandScan', 'GPW', 'Gridded', 'census', 'data', 'Data', 'source', 'Source', '2005', '2010', '2012', '2013', '2014', '2015', 'Published', 'published'):
    print(w, len(re.findall(w, t[i:j])))
