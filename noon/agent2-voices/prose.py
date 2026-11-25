"""Cleaning markdown (or plain text) into prose paragraphs and cutting it into pieces.  Shared by corpus.py and control.py."""
import re

WORD = re.compile(r"[A-Za-z][A-Za-z'’]*")


def nwords(t):
    return len(WORD.findall(t))


def clean(text):
    """markdown -> list of prose paragraphs (code, tables, headings, quotations, pictures removed)"""
    text = re.sub(r"```.*?```", "\n\n", text, flags=re.S)
    paras = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        if any(l.lstrip().startswith(("|", "#", ">", "![", "    ", "\t", "<")) for l in lines):
            lines = [l for l in lines if not l.lstrip().startswith(("|", "#", ">", "![", "<")) and not l.startswith(("    ", "\t"))]
        t = " ".join(l.strip() for l in lines)
        t = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", t)                  # a list marker at the start
        t = re.sub(r"\$\$.*?\$\$|\$[^$\n]{1,200}\$", " MATHS ", t)
        t = re.sub(r"`[^`\n]*`", " CODEREF ", t)
        t = re.sub(r"https?://\S+", " LINK ", t)
        t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
        toks = t.split()
        if nwords(t) >= 25 and nwords(t) >= 0.6 * len(toks):
            paras.append(t)
    return paras


def pieces(paras, size=300, least=150):
    out, cur = [], []
    for p in paras:
        cur.append(p)
        if nwords(" ".join(cur)) >= size:
            out.append(" ".join(cur))
            cur = []
    if cur and nwords(" ".join(cur)) >= least:
        out.append(" ".join(cur))
    return out


