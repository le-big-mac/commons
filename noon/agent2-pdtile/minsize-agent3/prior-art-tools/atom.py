#!/usr/bin/env python
"""Print the entries of an arXiv API Atom file: id, dates, authors, title, first words of the abstract.

usage: python -I atom.py RESULT.xml [ABSTRACT_CHARS]
The file is parsed as data only (no entity expansion beyond the standard library's defaults).
"""
import sys
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}


def main():
    path = sys.argv[1]
    nchar = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    root = ET.parse(path).getroot()
    entries = root.findall("a:entry", NS)
    total = root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
    print("total results:", total.text if total is not None else "?", "| shown:", len(entries))
    for e in entries:
        ident = (e.findtext("a:id", default="", namespaces=NS) or "").rsplit("/abs/", 1)[-1]
        pub = (e.findtext("a:published", default="", namespaces=NS) or "")[:10]
        upd = (e.findtext("a:updated", default="", namespaces=NS) or "")[:10]
        title = " ".join((e.findtext("a:title", default="", namespaces=NS) or "").split())
        authors = ", ".join(a.findtext("a:name", default="", namespaces=NS) for a in e.findall("a:author", NS))
        summ = " ".join((e.findtext("a:summary", default="", namespaces=NS) or "").split())
        print("-" * 78)
        print(ident, "| published", pub, "| updated", upd)
        print(title)
        print(authors)
        if nchar > 0:
            print(summ[:nchar])


if __name__ == "__main__":
    main()
