# Print question titles and bodies (HTML tags stripped) from a Stack Exchange API result file given as argument.
import sys, json, html, re
with open(sys.argv[1], "r", encoding="utf-8") as fh:
    data = json.load(fh)
for it in data.get("items", []):
    body = re.sub(r"<[^>]+>", "", it.get("body", ""))
    print("==", it.get("question_id"), html.unescape(it.get("title", "")))
    print(html.unescape(body)[:1500])
    print()
