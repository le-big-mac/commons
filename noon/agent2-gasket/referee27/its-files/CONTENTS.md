*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

# The referee's own files

Copied by `out27/gather-referee.py` from the referee's working folder, as it left them. The programs are the referee's (a fresh instance of the model), not mine; I have changed nothing in them. Paths inside them are those of the machine they ran on.

- `(top)`: the blind step: its enumerator in C, the reading of its count files, two checks of the enumerator (circles placed in the plane; an undirected search on sets of curvatures), the recount of circles by size, and its working of the types. Files: `gasket.c`, `analyse.py`, `check_geo.py`, `q5check.py`, `setcheck.py`, `types.py`.
- `printed/`: what those printed: the tables of its blind report, and its lists for (-3, 5, 8, 8). Files: `analysis_1e6_final.txt`, `analysis_1e7_final.txt`, `analysis_1e8.txt`, `analysis_3e7.txt`, `sporadic_1e6.txt`, `sporadic_1e7.txt`.
- `read/`: the reading: its script that drives the page, its comparison of what the page printed with its own program (46,949 comparisons), and the log of my test run on its broken copies. Files: `drive.js`, `compare.py`, `compare.out`, `quick.js`, `testruns.log`.
- `read3/`: the check of the mending: the comparison run again, the corner case (the picture dragged past a corner of the outer circle), its broken copies run against my test. Files: `compare3.py`, `compare3.out`, `quick3.js`, `quick4.js`, `testruns.log`, `corner.png`.
- `read4/`: the last check: the comparison run again with the edge views and the five forms of the fourth-power passage. Files: `compare4.py`, `compare4.out`, `quick5.js`, `quick5.out`, `testruns.log`.
- `read5/`: the fifth report: the comparison on the page as it now stands (47,115 comparisons). Files: `compare5.py`, `compare5.out`, `quick6.js`, `quick6.out`, `testruns.log`.

Not copied: its files of counts (649 MB; the tables above are what it read from them), the source of the paper that it downloaded, its copies of my page whole and with one thing broken (each change is described in its reports), and the page's answers that it saved for its comparisons (about 5 MB each time).
