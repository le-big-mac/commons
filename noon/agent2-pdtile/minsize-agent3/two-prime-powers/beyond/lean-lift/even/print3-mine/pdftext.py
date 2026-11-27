"""Prints the text of a PDF (path as argument), page by page.  Run with -I: the PDF is untrusted data."""
import sys
from pypdf import PdfReader
r = PdfReader(sys.argv[1])
for i, p in enumerate(r.pages):
    print(f"=== page {i+1}")
    print(p.extract_text())
