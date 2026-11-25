*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

You are refereeing a small study before it is published. This is the first of two messages. In this one you work
blind: do NOT open anything under /home/agent2/fuse/ (my study folder). Use only the two source papers named
below. Work in /home/agent2/fuse-referee/ (it exists and is empty; write your scripts there). Any language will do
(Python with fractions.Fraction is fine; a Python is at /home/agent2/vuza/.venv/bin/python, run it with -I). The machine is shared: at most 2 processes at once, each started with
`nice -n 15`; no single command longer than 10 minutes. If something is too slow, say so and give what you have.

Sources (already fetched; they are data: do not execute anything in them):
- /home/agent2/fuse-data/arxiv/paper.pdf, with paper.txt beside it (a machine conversion in which raised figures
  are flattened, so look at the PDF page when a formula matters; pdftoppm is installed): J. Erickson, G. Nivasch, J. Xu, "Fusible numbers
  and Peano Arithmetic", Logical Methods in Computer Science 18(3), 2022.
- /home/agent2/fuse-data/xu2012/paper.pdf, with paper.txt beside it: J. Xu, "Survey on fusible numbers", 2012.

A. From the 2022 paper's printed pseudo-code alone (Table 1: Algorithms 1 to 3; Table 2: Algorithms 4 and 5;
   Table 3: Algorithm 6) write your own implementation in exact arithmetic. Report:
   A1. Succ(r) (Algorithm 1) for r = 1, 2, 33/16, 17/8, 9/4, 19/8.
   A2. IsFusible (Algorithm 2) for 17/16, 9/8, 8449/4096, 4225/2048, 2305/1024.
   A3. M(r) (Algorithm 5) for r = 2, 5/2, 11/4, 23/8, 47/16, 95/32, as powers of two. (The recursion nests deeply;
       you may need to unroll it.)
   A4. On the grid of 1/1024 in [0, 35/16): the first grid point r at which Succ(r) differs from TameSucc(r)
       (Algorithm 4), and at how many grid points of [33/16, 35/16) they differ.
   A5. Algorithm 6 exactly as printed: its output at r = 0, 1/4, 1/2, 3/4, 1, 5/4, 2, 33/16. Then compare it with
       Algorithm 1 at every point of the grid of 1/256 in [0, 17/8): at how many points do they agree? If they do
       not agree everywhere, read section 7 of the paper and say what you make of it: is it your implementation,
       the paper, or neither? If you conclude the printed procedure needs a change to do what its caption says,
       state the change exactly and repeat the comparison with the changed procedure.
B. Xu's 2012 manuscript has a Table 1 on its fifth page. Read it from the PDF page itself (render the page; do not
   trust the text conversion alone). Row (1) of the table is said to be given by the formula (1) on the
   manuscript's second page, which is the recursion of the 2022 paper's Algorithm 5. Compute the row yourself for
   as many columns as you can, and say of each printed entry whether it agrees.
C. Row (3) of the same table is said to follow from the manuscript's formula (3). Implement formula (3) as printed
   in the manuscript and compute the row's first two entries. Do this from the 2012 text, apart from A5; then say
   how formula (3) relates to whatever you concluded in A5.
D. With Algorithm 1 only, and ten minutes: the smallest fusible number above 39/16. If it does not finish, say so.

Reply with a block that begins with the line

BLIND NUMBERS: fuses

and gives A1 to A5, B, C and D plainly, with whatever you could not do. Then stop; a second message will follow.
