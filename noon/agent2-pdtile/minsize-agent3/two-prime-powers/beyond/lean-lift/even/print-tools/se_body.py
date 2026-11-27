import sys, json, html, re
# usage: python3 -I se_body.py FILE...
for p in sys.argv[1:]:
    d = json.load(open(p, encoding="utf-8"))
    for it in d.get("items", []):
        print("==", it.get("question_id"), it.get("answer_id", ""), html.unescape(it.get("title", "")), "| score", it.get("score"), "| link", it.get("link", ""))
        body = html.unescape(re.sub(r"<[^>]+>", "", it.get("body", "")))
        print(body[:2500])
