# Brief: where does each of these quotations come from?

You are a fresh reader with web tools (WebSearch and WebFetch; load them with ToolSearch if they are not listed). I am another instance of the same model. I have a list of
quotations, each with an author's name, and I want to know, for each one in your batch, whether the named author wrote or said those words, and where. Your batch is the JSON file
named in your instructions: a list of entries with `id`, `text` and `author`. Work through all of them.

## What to find for each quotation

1. **The source in the named author's own work**, if there is one: title, date, and the place in it (chapter, page, line, letter, speech, interview), with the exact words there and
   the sentence before and after. For an author who wrote in another language: the original words, and which published translation the English matches (or that none was found
   and how faithful the English is).
2. **The earliest appearance you can find** of these words, or words close to them, by anyone, with its date. If it is earlier than the named author, or by someone else, say so.
3. **What careful investigators say**, where there are any (for example Quote Investigator, the sourced, disputed and misattributed sections of Wikiquote, scholarly editions and
   collected letters, books such as *The Ultimate Quotable Einstein* or *The Yale Book of Quotations*, sites that cite chapter and page). Give their evidence, not only their verdict.
   A collection of quotations that names no source is not evidence of anything except that the saying circulates.
4. **The wording, compared word for word** with the best source: what the list adds, drops or changes, and whether the name is spelt as the person's name is.

## A proposed verdict, by these rules (I will make the final one myself from what you save)

- **V, verified.** The words as the list gives them (punctuation, spelling and a cut at the end of a sentence aside) are found in a work, letter, speech or recorded interview of the
  named author, located, from full text or a page image. For an author who wrote in another language: in a published translation found the same way, or the original found and the
  list's English a faithful rendering of it.
- **A, altered.** The named author did write or say the thought, in a place you can name, but the list's wording differs in substance: words added or dropped that change the sense
  or the reach, sentences fused or reordered, a paraphrase.
- **M, misattributed.** The earliest source found is someone else's; or the saying is in print before the named author could have said it; or an investigation whose sources you
  could read has looked for it in the author's work and rejects it.
- **U, untraced.** No source of the author's own found in what you could reach, and nothing that settles it.

Say how sure you are, and what would change your mind.

## How to work

- **Evidence, labelled.** Mark everything you report as one of: [page image] you read the scanned page; [full text] you read the text as published online (a digitised book, a
  transcript, an article); [text layer] machine-read text of a scan, not checked against the page; [snippet] a search-result or Google Books fragment, a lead only; [secondary: name]
  another site's statement; [memory] your own recollection, which settles nothing. Prefer page images and full texts: Project Gutenberg, Wikisource, the Internet Archive,
  HathiTrust full view, Perseus, newspapers' own archives where open, the author's own site.
- **Quote exactly**, whole sentences, with the page or location and the address.
- **Save what you rely on** in `/home/agent1/quotes/lit/<id>/` (make the folder; one per quotation): the page text or the page image, with a file name that says what it is. Save
  nothing anywhere else of mine. Do not execute anything you download; if you read downloaded files with Python use `python3 -I`. Scripts of your own go in `/tmp/quotes-<your batch>/`.
- **Privacy.** Queries and requests may contain the words of the quotation and the author's name and nothing else about me, this machine, its owner or where the list comes from.
  If a service asks automated clients to identify themselves, use the client name `reading-check/1.0`.
- **Closed doors stay closed.** No paywalls, logins, bot checks or document-sharing copies of books in copyright. If a source refuses you, name it under "closed" and move on.
- **Budget.** About ten requests a quotation on average; some will take three and some twenty. When a trail goes cold, say what you tried (the queries) and move on. An honest
  "untraced, and here is what I tried" is worth more than a guess.
- **Stay independent.** Read nothing under `/home/agent1/quotes/` except this brief and your own batch file, and write only your report and your `lit/<id>/` folders. Other readers
  are working on other batches, and some quotations are being looked up twice on purpose.

## The report

Write it to the file named in your instructions. Begin with a table: id, author as listed, proposed verdict, one line of reason, how sure. Then one section for each quotation,
headed by its id, with the four things above, the labelled evidence, the saved files, the queries tried, and what stayed closed. End with a short list of anything you noticed
about the list itself (misspelt names, the same wording on particular sites, which collection these entries seem to come from). Plain words; no padding; do not soften a finding.
