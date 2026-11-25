"""Put the rules (core.js) and the book (the strategies in the study's out/final/) inside the page.   usage (from play/): python -I build.py ..
Writes ../play.html and books.json. The book for each lag is the strategy that always has the code sent by letter W(lag)."""
import sys, json, os
study = sys.argv[1]; W = {0: 5, 1: 7, 2: 8, 3: 9, 4: 10}; books = {}
for d, T in W.items():
    b = {}
    for line in open(os.path.join(study, "out", "final", f"W-d{d}-Q{T}.out")):
        if line.startswith("S "):
            _, t, rest = line.split(); hist, guess = rest.split(":"); key = f"{t}|{'' if hist == '-' else hist}"; assert b.get(key, guess) == guess; b[key] = guess
    books[d] = b
json.dump(dict(W=W, books=books), open("books.json", "w"), separators=(",", ":"))
src = open("play.src.html").read(); core = open("core.js").read(); assert src.count("/*CORE*/") == 1 and src.count("/*BOOKS*/") == 1
page = os.path.join(study, "play.html"); open(page, "w").write(src.replace("/*CORE*/", core).replace("/*BOOKS*/", json.dumps(dict(W=W, books=books), separators=(",", ":"))))
print(page, os.path.getsize(page), "bytes;", {d: len(b) for d, b in books.items()}, "lines in the books")
