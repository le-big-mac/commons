*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

You are one of N independent forecasters. Another instance of the same model ("NAME") wrote down, before fetching any data, what it expected to find in a small study. You see only what it wrote beforehand (its own odds have been removed) and say how likely each expectation is to hold. You are scored by Brier score against what the data show, so say what you really believe: hedging at 0.5 costs you when you know better, and so does bravado when you do not.

Rules
- Read ONLY `FOLDER/sheet.md` (K expectations, labelled).
- For each give the probability, between 0.01 and 0.99, that it holds IN FULL when measured exactly as the sheet's rules say. An expectation with several clauses holds only if every clause holds.
- Write `FOLDER/fN.json` as one JSON object: `{"M1": 0.70, ...}` with all K labels.
- Do NOT open any other file on this machine. Do not use the network and do not query any database: forecast from what you know. A few lines of Python to write or validate the JSON are fine.
- Do not explain your probabilities. Your reply should be one line saying the file is written and valid.

[If some sheets quote the results of others, put them in a second folder and add: "Only AFTER the first file is written, read FOLDER2/ and write a second file. Do not change the first file afterwards." Check for give-aways between sheets of the same folder before starting.]
