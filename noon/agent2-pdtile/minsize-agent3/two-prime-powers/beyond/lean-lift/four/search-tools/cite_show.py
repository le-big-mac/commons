# Print citation lists saved from Semantic Scholar (citations endpoint) or OpenAlex (works endpoint).
# Usage: cite_show.py FILE [FILE ...]
import sys, json
for path in sys.argv[1:]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as exc:
        print("==", path, "unreadable:", exc); continue
    if "data" in data:  # Semantic Scholar
        rows = data.get("data") or []
        print("==", path, "Semantic Scholar rows:", len(rows), "next:", data.get("next"))
        for r in rows:
            p = r.get("citingPaper") or r.get("citedPaper") or {}
            ids = p.get("externalIds") or {}
            au = ", ".join(a.get("name", "") for a in (p.get("authors") or [])[:4])
            print("  %s | %s | %s | arXiv:%s doi:%s | %s" % (p.get("year"), p.get("title"), au, ids.get("ArXiv"), ids.get("DOI"), p.get("venue")))
    elif "results" in data:  # OpenAlex
        rows = data.get("results") or []
        meta = data.get("meta") or {}
        print("==", path, "OpenAlex rows:", len(rows), "count:", meta.get("count"))
        for w in rows:
            au = ", ".join((a.get("author") or {}).get("display_name", "") for a in (w.get("authorships") or [])[:4])
            loc = (w.get("primary_location") or {})
            src = (loc.get("source") or {}).get("display_name")
            print("  %s | %s | %s | %s | doi:%s | cited_by:%s | %s | %s" % (w.get("publication_year"), w.get("id"), w.get("display_name"), au, w.get("doi"), w.get("cited_by_count"), src, loc.get("landing_page_url")))
    else:
        print("==", path, "unrecognised:", str(data)[:300])
