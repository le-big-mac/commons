import sys, json, html, re
# usage: python3 -I se_body.py FILE [MAXCHARS]
d = json.load(open(sys.argv[1], encoding="utf-8"))
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 1800
for it in d.get("items", []):
    b = html.unescape(re.sub(r"<[^>]+>", "", it.get("body", "")))
    print("##", it.get("question_id"), html.unescape(it.get("title", "")), "| score", it.get("score"), "| answers", it.get("answer_count"))
    print(re.sub(r"\s+", " ", b)[:mx]); print()
