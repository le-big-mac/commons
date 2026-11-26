"""Third check of the wikinotes page: the three paragraphs added to note 4 on 26 November 2026.

Writes changes.json (a list of {"id","old","new","why","must"}), checks that every "old" occurs exactly once
in README-proposed.md and that no two changes overlap, and writes two trial copies for reading:
README-after-all.md (every change applied) and README-after-must.md (only those marked must).

Run:  python3 -I make_changes.py
Nothing outside this directory is written.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'README-proposed.md')

C = []


def add(id_, old, new, why, must):
    C.append({"id": id_, "old": old, "new": new, "why": why, "must": must})


# ---------------------------------------------------------------- earlier text of note 4
add("c1-pointer",
    "request), so this is a question and not a correction.",
    "request), so this is a question and not a correction. (So it stood on 25 November, and I have left the "
    "note as it was written. The paper has since been read: see the paragraphs dated 26 November at the end of "
    "this note.)",
    "With the addition in place the page says in the present tense, in the first paragraph of note 4, \"None of "
    "us has read that paper\", and five paragraphs later that it has been read. An editor who stops at the first "
    "paragraph is told something no longer true. This leaves the earlier text standing and says so, as you "
    "prefer; it also covers the later sentence \"An editor with the 2021 paper to hand could see ...\".",
    True)

# ---------------------------------------------------------------- added paragraph 1
add("c2-opening",
    "A search for earlier work that Catalpa had made for its own page on this eclipse fetched the 2021 paper "
    "(from the Internet Archive's capture of the journal's open file, the journal's server having moved); "
    "Catalpa told me what it found, and I have searched the saved text myself.",
    "Catalpa had a fresh instance search for earlier work on this eclipse, and the search fetched the 2021 "
    "paper (from the Internet Archive's capture of the journal's own open file; the journal's old address no "
    "longer leads to it). Catalpa told me what it found, and I have searched the saved text myself.",
    "Plain words: \"earlier work that Catalpa had made\" reads at first as Catalpa's own earlier work. The "
    "search's report says the publisher's old address \"now leads to a general page of the institute's new "
    "site\", which is nearer \"no longer leads to it\" than \"the server having moved\". Nothing in the "
    "sentence is wrong.",
    False)

add("c3-one-sentence",
    "Its one sentence on how good the King's calculation was is a quotation from the booklet that",
    "Of the King's own calculation of this eclipse it has one sentence on how good it proved (the \"Thai solar "
    "eclipse calculation\" that a quotation on page 391 calls \"not particularly good\" is not said to be "
    "his), and that sentence is a quotation from the booklet that",
    "The count \"one sentence\" cannot be had from the paper as you word it. Its section 2.2, headed \"King "
    "Rama IV's Eclipse Calculations\", quotes Gislén and Eade (2021: 649): \"The Thai solar eclipse calculation "
    "above is not particularly good, it does not predict a total eclipse\". The paper does not say whose "
    "calculation \"above\" is (by the search's report of Gislén and Eade 2019 it is a traditional one, not the "
    "King's, but that is not in this paper). An editor who opens the paper will meet that sentence under that "
    "heading, so the note should have met it first. Your sentence is right about the King's own calculation of "
    "1868: Ord's is the only one. (The timeline on page 393 has \"10.06 am: This was first contact according to "
    "King Rama IV's calculation and prediction, but the sky was very cloudy and first contact could not be "
    "observed\", which says nothing of how good it was.)",
    True)

add("c4-gloss",
    "That is a guest's account of what was being said on the day. It gives no figure, and it is not an "
    "acknowledgement by the French; I found no sentence in the paper that says the French acknowledged anything.",
    "That is a guest's account of what was being said on the day: \"report\" names nobody, and it speaks of "
    "\"the European observers\", not of the French by name. It gives no figure, and it is not an "
    "acknowledgement by the French; neither I nor a fresh reader of mine who went through the whole text found "
    "a sentence in the paper that says the French acknowledged anything. For the French expedition the paper "
    "refers to its authors' chapter of 2017, which none of us has read.",
    "Improvement. Your gloss is fair: by the paper Ord was the King's guest (page 390, \"his most distinguished "
    "guest\"; page 396, houses built for his party), the visit was \"Late that same afternoon\", the mood and "
    "the calculations are the King's, and \"report\" is rumour. Two things an editor needs are not said: Ord "
    "has \"European observers\" where the article has \"French astronomers\", and the paper points elsewhere "
    "for the French side (page 390: \"It has been researched by Orchiston and Orchiston (2017)\"), so the "
    "absence here does not show the words are in nothing of Orchiston's.",
    False)

# ---------------------------------------------------------------- added paragraph 2
add("c5-two-bradleys",
    "says that the claim is usually taken from Dr Bradley, and quotes him (page 47, note 22: W. L. Bradley, "
    "*Siam Then*, 1981, page 149):",
    "says that writing which claims the King was the more accurate to the second usually takes it from the "
    "record of Dr Bradley, and quotes that from a book of 1981 by William Lee Bradley (page 47, note 22: *Siam "
    "Then: The Foreign Colony in Bangkok before and after Anna*, Pasadena, 1981, page 149):",
    "\"Dr Bradley, and quotes him (... W. L. Bradley ...)\" makes one man of two. Supavit's Thai is "
    "\"บันทึกของหมอบรัดเลย์\", the record of Mo (Doctor) Bradley, and on page 50 \"จดหมายเหตุของหมอบรัดเลย์\", "
    "Dr Bradley's journal; his note 22 cites William Lee Bradley's book of 1981. Catalpa's fifth reader made "
    "the same point (its A5: \"The book of 1981 is by W. L. Bradley, a different man\"). An editor needs to "
    "know which Bradley to cite and that the date of the sentence is unknown; the caution itself is in the "
    "next change.",
    True)

add("c6-supavit",
    "By Catalpa's reading of the Thai, Supavit remarks that this is hearsay by its own wording (\"It was "
    "reported\"), reports finding no document of the time that compares the two calculations in figures, and "
    "records a conjecture made by Loy Chunpongtong in a Thai book of 2019: that the figure grew out of the "
    "King's \"about only two or three seconds\" to Stephan, the sentence quoted above, which compares two "
    "places and not two calculations. I have seen neither Bradley's book nor Loy's.",
    "Supavit's \"Dr Bradley\" (in Thai, *Mo* Bradley) is, I take it, the missionary Dan Beach Bradley "
    "(1804–1873) of the Orchistons' page 390; the book of 1981 is by a later Bradley, and nothing I have read "
    "says whose sentence it is or when it was written. By Catalpa's reading of the Thai, which a fresh reader "
    "of mine checked against the page images and shares, Supavit remarks that this is hearsay by its own "
    "wording (\"It was reported\") and does not say which moment of the eclipse is meant. In the Thai "
    "documents of the time that he studied he has found no passage that praises the King's calculation as more "
    "accurate than the Westerners' (page 46), and the three foreign accounts he cites (Ord's, one cited by "
    "Cook, Stephan's) tell of the King's satisfaction and nowhere say that the calculations were compared in "
    "figures (page 47). He records, and calls reasonable, a conjecture made by Loy Chunpongtong "
    "(ลอย ชุนพงษ์ทอง) in a chapter of a Thai book of 2019: that Bradley may have got his figure from the King's "
    "\"about only 2 or 3 seconds\" in the letter to Stephan, by its content the sentence quoted above, which "
    "compares two places and not two calculations. I have seen neither Bradley's book nor Loy's chapter.",
    "Must, for the middle clause: \"reports finding no document of the time\" is wider than what Supavit "
    "says. Page 46: \"จากการศึกษาเอกสารร่วมสมัยในกลุ่มนี้ยังไม่พบข้อความใดที่สรรเสริญและเปรียบเทียบผลการคำนวณของรัชกาลที่ 4 "
    "ว่าแม่นยำเหนือกว่าฝรั่ง\" (from studying the contemporary documents in this group, no passage has yet been found "
    "that praises and compares Rama IV's calculation as more accurate than the Westerners'): \"this group\" is "
    "the Thai documents of his Table 1, and \"not yet\". Page 47, after Ord, a secondary document cited by Cook, "
    "and Stephan (the last through a Thai book of 2002): \"ทั้งหมดบันทึกอากัปกิริยาของรัชกาลที่ 4 ที่ทรงแสดงความพออกพอใจ "
    "แต่ไม่มีกรณีใดเลยที่ผู้บันทึกหลักฐานเหล่านั้นระบุถึงการนำผลคำนวณต่างกรณีกันมาเปรียบเทียบความแม่นยำในเชิงตัวเลข\" (all record "
    "the King's show of satisfaction, but in no case do the writers of those records say that separate "
    "calculations were brought together to compare accuracy in figures). So it is a statement about the "
    "documents he examined, not about every document of the time. The rest is improvement: the two Bradleys "
    "and the unknown date (see c5); Supavit's further remark, pages 47 to 48, that it is unclear whether the "
    "two seconds mean the start, the totality or the end; his verdict on Loy, \"ซึ่งผู้เขียนเห็นว่าข้อสันนิษฐานนี้"
    "สมเหตุสมผล\" (the present writer finds this conjecture reasonable), which your text left out; Supavit "
    "prints \"about only 2 or 3 seconds\" in figures, and it is Loy's conjecture as he reports it that Bradley "
    "\"อาจได้ตัวเลขมาจากพระราชหัตถเลขาของรัชกาลที่ 4 ที่ส่งให้สเตฟาน\" (may have got the figure from Rama IV's letter sent "
    "to Stephan); that this letter is the statement Stephan prints on his pages 128 and 129 is your "
    "identification, sound by its content, and is now marked as yours; Loy's piece is a chapter (note 23: "
    "pages 202-12 of the edited book of 2562 = 2019), and his name in Thai lets an editor find it, the Latin "
    "spelling being the search reader's.",
    True)

# ---------------------------------------------------------------- added paragraph 3
add("c7-where-to-look",
    "A source that has the two seconds is Bradley (1981, page 149, as Supavit quotes him), and has them as "
    "something reported.",
    "A source that has the two seconds is William Lee Bradley's book of 1981 (page 149, as Supavit quotes it), "
    "and it has them as something reported. The article already cites a web page that its citation calls a "
    "964-word excerpt from that book (the reference named \"Montes-Bradley\", on the sentence about the King's "
    "death); I have not opened it, and an editor could look there. Aubin's chapter of 2010, which the article "
    "also cites, may have the two seconds too: its draft, as Catalpa reports it, has them as the King's own "
    "boast (see the background paragraph above).",
    "Improvement, and a lead you may want to follow before posting. \"Him\" again leaves open which Bradley. "
    "And the wikitext you saved on 25 November (revision 1384898663) has, on the sentence \"He died a month and "
    "a half after the eclipse, on 1 October 1868\", a reference named Montes-Bradley: a web page of the Thomas "
    "Osgood Bradley Foundation by Saul M. Montes-Bradley and W. L. Bradley (author link \"William Lee "
    "Bradley\"), with format \"964-word excerpt from ''Siam then, the foreign colony in Bangkok before and "
    "after Anna'', Pasadena, California, 1981.\", an archive address, and the quotation \"King Mongkut's "
    "prediction surpassed those of European scientists. ...\". So the book that carries the two seconds is "
    "already among the article's references, two sentences after the claim, and the claim may have come from "
    "there. I could not open the page (no network). If you open it, replace \"I have not opened it\" with what "
    "you find. The Aubin clause only joins the addition to your own background paragraph, which already says "
    "this; the article cites Aubin (2010) after \"led by Pierre Janssen\" and after the sentence on diplomacy.",
    False)

add("c8-in-neither",
    "\"Who acknowledged his accuracy\" is in neither.",
    "\"Who acknowledged his accuracy\" is not in the paper, nor in Bradley's sentence as Supavit quotes it "
    "(the rest of Bradley's book I have not seen); the same goes for the lead's \"were acknowledged as more "
    "precise\".",
    "True as you mean it, but \"neither\" can be read as \"neither the paper nor Bradley's book\", and nobody "
    "here has seen the book: only one sentence of it, as quoted. Bradley's sentence has the King \"greatly "
    "gratified to find that he was more correct\", which is the King's satisfaction and no acknowledgement by "
    "anyone. The lead's wording (quoted in the first paragraph of note 4) has the same fault, and in the saved "
    "wikitext that sentence of the lead has no reference on it, so the editor should be told it falls with "
    "the other.",
    True)

add("c9-exactly-this-question",
    "Supavit's article is a published study of exactly this question and would be the place to start.",
    "Supavit's article is a research article on the Thai sources for this eclipse and on how its history has "
    "been written; it takes up exactly this question on pages 46 to 48 and would be the place to start. It is "
    "in Thai, with an English abstract.",
    "\"A published study of exactly this question\" says more than the article is. By its English abstract "
    "its question is the claim \"that King Rama IV had predicted the eclipse 2 years earlier\" and what the "
    "Thai primary sources show; the comparison with the French takes pages 46 to 48 of 24. Its first page is "
    "marked \"Research Article\" (received, revised and accepted dates given), which an editor weighing the "
    "source will want. (The search's report says it fetched \"the journal's own file\" from the journal's "
    "site; I could not test that, so it is not in the replacement.)",
    True)


def main():
    text = open(SRC, encoding='utf-8').read()
    spans = []
    ok = True
    for c in C:
        n = text.count(c["old"])
        if n != 1:
            print("NOT UNIQUE", c["id"], "occurs", n)
            ok = False
            continue
        i = text.index(c["old"])
        spans.append((i, i + len(c["old"]), c["id"]))
        if c["old"] == c["new"]:
            print("NO CHANGE", c["id"])
            ok = False
    spans.sort()
    for a, b in zip(spans, spans[1:]):
        if a[1] > b[0]:
            print("OVERLAP", a[2], b[2])
            ok = False
    ids = [c["id"] for c in C]
    if len(set(ids)) != len(ids):
        print("DUPLICATE ID")
        ok = False
    if not ok:
        sys.exit(1)

    with open(os.path.join(HERE, 'changes.json'), 'w', encoding='utf-8') as f:
        json.dump(C, f, ensure_ascii=False, indent=1)
        f.write('\n')

    def apply(only_must):
        t = text
        for c in C:
            if only_must and not c["must"]:
                continue
            assert t.count(c["old"]) == 1, c["id"]
            t = t.replace(c["old"], c["new"])
        return t

    allt = apply(False)
    mustt = apply(True)
    open(os.path.join(HERE, 'README-after-all.md'), 'w', encoding='utf-8').write(allt)
    open(os.path.join(HERE, 'README-after-must.md'), 'w', encoding='utf-8').write(mustt)

    def words(s):
        return len(s.split())

    print("changes:", len(C), " must:", sum(1 for c in C if c["must"]),
          " improvement only:", sum(1 for c in C if not c["must"]))
    for s in spans:
        print("  at char %6d  %s" % (s[0], s[2]))
    print("words: proposed %d, after must only %d, after all %d" % (words(text), words(mustt), words(allt)))
    a = text.index("**Added 26 November 2026")
    e = text.index("## What none of the notes covers")
    for name, t in (("proposed", text), ("after must only", mustt), ("after all", allt)):
        a2 = t.index("**Added 26 November 2026")
        e2 = t.index("## What none of the notes covers")
        print("  the three added paragraphs, %s: %d words" % (name, words(t[a2:e2])))


if __name__ == '__main__':
    main()
