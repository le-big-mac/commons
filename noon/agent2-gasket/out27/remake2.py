"""Second stage of the gasket page's remake: the first screen and the words.   python -I out27/remake2.py   (run after remake.py)
After the plain reader's first visit (reader27/visit-1.md): the first screen was "all words" (a paragraph of fourteen lines and eight
of instruction, and no picture); the picture opened on a gasket in which nothing is lit ("The first thing a visitor sees shows an
absence"); "the test of remainders" was never explained; "(−3, 5, 8, 8)" was a name nobody had introduced; "the paper proves" came
before any paper was named; the third panel printed a list 1,861 px tall, spoke of a "sign" that nothing is done with, and its button
"Draw it above" drew the gasket last looked at, not the one typed.
What it changes:
  - the page opens with two sentences and the picture, on the gasket (−4, 5, 20, 21), in which squares are lit; under the picture a
    sentence and a button go to (−3, 5, 8, 8), in which none is, and back;
  - the buttons that magnify stand directly under the picture, the two menus after them;
  - what the picture is, how a gasket is named, the test with an example, and what was shown in 2023 come after, under "What is going on";
  - the sentence under the picture names the paper's authors where it said "the paper";
  - the third panel: the sign is not spoken of; the list of missing numbers is shown only when asked for; "Draw it above" reads the box."""
H = '/home/agent2/gasket/'
if __name__ == '__main__':
    s = open(H + 'page.src.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:110], s.count(a)); s = s.replace(a, b)
    # ---- the top of the page, as far as the second panel
    i = s.index('  <h1>A gasket with numbers missing</h1>'); j = s.index('    <h2>The numbers that never come</h2>')
    old = s[i:j]; assert 'id="pack"' in old and 'id="hi"' in old and 'id="gtab"' in old and 'id="g"' in old and 'id="gsay"' in old and 'id="gpick"' in old and 'id="gtable"' in old and old.count('<option') == 7, 'the top is not as expected'
    hi = old[old.index('<select id="hi">'):old.index('</select>', old.index('<select id="hi">')) + len('</select>')]
    canvas = old[old.index('<canvas id="g"'):old.index('</canvas>') + len('</canvas>')]
    new = '''  <h1>A gasket with numbers missing</h1>
  <p class="sub" id="lead">Each circle is marked with a whole number: the smaller the circle, the bigger its number. Squares are lit in orange.</p>

  <div class="viz-root">
    <figure id="gfig">
      ''' + canvas + '''
      <div class="tip" id="gtip"></div>
      <ul class="legend"><li><i style="background:var(--fam)"></i><b id="hiName">a square</b></li><li><i style="border:1px solid var(--muted);box-sizing:border-box"></i>any other number</li></ul>
      <p class="say" id="gstory"></p>
      <div class="controls"><button id="zin">Magnify ×2</button><button id="zout">Draw back ÷2</button><button id="home">The whole gasket</button></div>
      <p class="say" id="gpick" aria-live="polite"></p>
      <div class="controls">
        <label>The gasket begun from <select id="pack"></select></label>
        <label>Light up the numbers that are ''' + hi + '''</label>
        <button id="gtab" aria-pressed="false">Show the table</button>
      </div>
      <p class="say" id="gsay" aria-live="polite"></p>
      <p class="say" id="ghow">With fingers: pinch to magnify, drag sideways to move. With a mouse: scroll to magnify, drag to move. The numbers are worked out exactly, however far you magnify, as far as the page goes.</p>
      <div class="tables" id="gtable"></div>
    </figure>

    <h2>What is going on</h2>
    <div class="about" id="about">
      <p>Three circles that touch one another leave a gap, and exactly one circle fits the gap touching all three. Fill every gap, and every gap that leaves, for ever: that is an Apollonian gasket. A circle's number here is one over its radius, so small circles have big numbers; mathematicians call it the curvature. If the first four numbers are whole, every number in the gasket is.</p>
      <p>A gasket is named here by its four largest circles, as <b>(&minus;4, 5, 20, 21)</b>. The number with the minus is the circle round all the rest.</p>
      <p>Not every whole number can turn up. Divide a number by 24 and look at what is left over: in the two gaskets of the button above, only numbers that leave 0, 5, 8, 12, 20 or 21 are ever a circle's number. 36 leaves 12, so it passes that test, and in <b>(&minus;4, 5, 20, 21)</b> it is there.</p>
      <p>For twenty years the guess was that every number that passes the test turns up, once the numbers are large enough. In 2023 four mathematicians showed that the guess is false: in many gaskets a whole family of numbers that pass the test never appears. In <b>(&minus;3, 5, 8, 8)</b> it is the squares, and the numbers six times a square; in <b>(&minus;4, 5, 20, 21)</b> it is the numbers twice a square and three times a square.</p>
    </div>

'''
    s = s[:i] + new + s[j:]
    rep("  .nums { font-variant-numeric: tabular-nums;", "  .about p { margin: 0 0 10px; max-width: 760px; } #gstory { margin-bottom: 12px; } #gstory button { margin: 6px 0 0; } #gpick { margin: 10px 0 12px; } #ghow { color: var(--text-secondary); font-size: 13px; }\n  #tnums { display: none; } #tnums.on { display: block; }\n  .nums { font-variant-numeric: tabular-nums;")
    # ---- the gasket the page opens on, and the sentence with its button
    rep("  setPack(PRESETS[0]); chart(); look();", "  $('pack').value = '1'; setPack(PRESETS[1]); chart(); look();")
    rep("    if ($('gtable').classList.contains('on')) gtable();\n  }\n", """    story();
    if ($('gtable').classList.contains('on')) gtable();
  }
  // The sentence under the picture that goes with the two gaskets the page compares: one in which squares turn up, one in which none ever does.
  function story() { var key = pack.root.join(','), sq = $('hi').value === '1', h;
    if (key === '-4,5,20,21' && sq) h = 'In this gasket squares turn up: the two largest orange circles are marked 36, which is 6 \\u00d7 6. <button id="swap" data-to="0">Show a gasket with no square in it</button>';
    else if (key === '-3,5,8,8' && sq) h = 'In this gasket nothing is lit, and nothing will be, however far you magnify: no square is the number of any of its circles. That was proved in 2023, against what had been believed for twenty years. <button id="swap" data-to="1">Back to the gasket with squares</button>';
    else h = '<button id="swap" data-to="1">Back to the gasket with squares</button>';
    if ($('gstory').innerHTML !== h) $('gstory').innerHTML = h; }
  $('gstory').addEventListener('click', function (e) { var t = e.target; if (!t || t.id !== 'swap') return; $('hi').value = '1'; $('pack').value = t.getAttribute('data-to'); setPack(PRESETS[+t.getAttribute('data-to')]); });
""")
    # ---- the sentence under the picture: whose theorem
    rep("fams.length ? '; the paper proves it has no curvature of the form ' + fams.map(famName).join(' or ') : '; the paper\\u2019s theorem names no family of squares barred from it')",
        "fams.length ? '; it is proved (Haag, Kertzer, Rickards and Stange, 2023) that it has no number of the form ' + fams.map(famName).join(' or ') : '; the theorem of 2023 names no family of squares barred from it')")
    rep("' Its curvatures leave the remainders ' + t.res.join(', ') + ' on division by 24'", "' Its numbers leave ' + t.res.join(', ') + ' on division by 24'")
    # ---- the third panel
    rep("""    h += 'Its curvatures leave the remainders <b>' + t.res.join(', ') + '</b> on division by 24, and its sign (the paper’s χ<sub>2</sub>) is <b>' + (t.chi2 === null ? 'not found by the page' : t.chi2 > 0 ? '+1' : '−1') + '</b>. ';
    h += t.quad === null ? 'Without the sign the page cannot say which families are barred. '""", """    h += 'Its numbers leave <b>' + t.res.join(', ') + '</b> on division by 24. ';
    h += t.quad === null ? 'The page could not work out which families are barred from it. '""")
    rep("""$('tnums').innerHTML = miss.length ? 'Missing: ' + list + (miss.length > 600 ? ' … (' + group(miss.length - 600) + ' more)' : '') : '';""",
        """$('tnums').innerHTML = miss.length ? 'Missing: ' + list + (miss.length > 600 ? ' … (' + group(miss.length - 600) + ' more)' : '') : ''; $('tlist').hidden = !miss.length; $('tlist').textContent = ($('tnums').classList.contains('on') ? 'Hide' : 'Show') + ' the list of the missing numbers' + (miss.length > 600 ? ' (the first 600)' : '');""")
    rep("""      <p class="nums" id="tnums"></p>""", """      <button id="tlist" aria-pressed="false" hidden>Show the list of the missing numbers</button>
      <p class="nums" id="tnums"></p>""")
    rep("""    custom = rootq; $('show').disabled = false; }""", """    custom = rootq; $('show').disabled = false; return true; }
  $('tlist').addEventListener('click', function () { var on = $('tnums').classList.toggle('on'); this.setAttribute('aria-pressed', on); this.textContent = this.textContent.replace(on ? 'Show' : 'Hide', on ? 'Hide' : 'Show'); });""")
    rep("""  $('show').addEventListener('click', function () { if (!custom) return; fillPacks();""", """  $('show').addEventListener('click', function () { if (look() !== true || !custom) return; fillPacks();        /* the box is read again: the button used to draw the gasket last looked at, whatever had been typed since */""")
    open(H + 'page.src.html', 'w', encoding='utf8').write(s); print('gasket page: the first screen and the words (stage 2)')
