# Print titles, links, scores from a Stack Exchange API search result (JSON file given as argument).
import sys, json, html
for path in sys.argv[1:]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as exc:
        print(path, "unreadable:", exc)
        continue
    items = data.get("items", [])
    print("==", path, "items:", len(items), "has_more:", data.get("has_more"), "quota:", data.get("quota_remaining"), data.get("error_message", ""))
    for it in items:
        print("  [%s] %s  (score %s, answers %s)" % (it.get("question_id"), html.unescape(str(it.get("title"))), it.get("score"), it.get("answer_count")))
        print("     ", it.get("link"))
