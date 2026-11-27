import sys, json, html
# usage: python3 -I se_ex_show.py FILE...
for p in sys.argv[1:]:
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(p, "unreadable", e); continue
    items = d.get("items", [])
    print("==", p, "items:", len(items), "quota:", d.get("quota_remaining"), d.get("error_message", ""))
    for it in items[:10]:
        print("  ", it.get("item_type"), it.get("question_id"), "|", html.unescape(it.get("title", ""))[:120], "| score", it.get("score"))
