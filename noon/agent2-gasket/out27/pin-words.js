// pin-words.js -- the gasket page's unchanging words, read off the page and written to tools/pinned-words.json, where the page test
// (tools/shot-gasket.js) holds the page to them word for word.  Run after a deliberate change of words, and read the file's diff by eye:
//      cd ~/web && node ~/gasket/out27/pin-words.js ~/gasket/gasket.html ~/gasket/tools/pinned-words.json
// The words that change with what the visitor does (the lines under the pictures, the first sentence's second half, the swap button
// and its sentence, the menu of gaskets when one has been added from the third panel) are not pinned: the test works those out.
const { chromium } = require('playwright'), fs = require('fs'), path = require('path');
const SELS = ['title', 'h1', 'h2', '#gmove button', '#ghow', '#about p', '#cfig figcaption', '#cfig .legend li', 'figure:not([id]) figcaption', 'p.note',
  '#hi option', '#upto option', '#pack option:not([value="c"])', '#cpack option', '#gtab', '#ctab', '#try', '#show', '#gfig .legend li:last-child'];
(async () => { const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1100, height: 1900 } }); await p.goto('file://' + path.resolve(process.argv[2])); await p.waitForTimeout(600);
  const words = await p.evaluate(sels => sels.map(q => [q, [...document.querySelectorAll(q)].map(e => e.textContent.replace(/\s+/g, ' ').trim())]), SELS);
  fs.writeFileSync(path.resolve(process.argv[3]), JSON.stringify(words, null, 1) + '\n'); console.log(words.length + ' kinds of piece, ' + words.reduce((a, x) => a + x[1].length, 0) + ' pieces, ' + words.reduce((a, x) => a + x[1].join('').length, 0) + ' characters'); await b.close(); })();
