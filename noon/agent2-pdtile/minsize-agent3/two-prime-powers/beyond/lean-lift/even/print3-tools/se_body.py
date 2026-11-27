import sys, json, html, re
# usage: python3 -I se_body.py FILE [maxchars]
d = json.load(open(sys.argv[1], encoding="utf-8"))
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
for it in d.get("items", []):
    body = re.sub(r"<[^>]+>", "", html.unescape(it.get("body", "")))
    print("--- answer", it.get("answer_id"), "score", it.get("score"), "owner", (it.get("owner") or {}).get("display_name"))
    print(body[:mx])
