"""The coin page made over for a visitor with a phone, 27 November 2026 (after a plain reader's visit, reader/visit-1.md).
It is made from the page as it stood (page.src.before-27nov.html), so that it can be run again.   python -I remake.py"""
import re
H = '/home/agent2/coin/'
if __name__ == '__main__':
    s = open(H + 'page.src.before-27nov.html', encoding='utf8').read()
    def rep(a, b, count=1):
        global s
        assert s.count(a) == count, (a[:90], s.count(a)); s = s.replace(a, b)
    def between(a, b, new):          # replace from the line that begins with a up to (not including) the line that begins with b
        global s
        i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]

    # ---------------- styles
    rep("  #best { min-width: 760px; }\n  .chartwrap { overflow-x: auto; } .chartwrap svg.chart { min-width: 620px; }\n",
        """  table.best { width: 100%; } table.best td.l { padding-right: 6px; } table.best .setbtn { white-space: normal; text-align: left; }
  @media (max-width: 520px) { table.best th, table.best td { padding-right: 8px; } }
  h3 { font-weight: normal; font-size: 16px; margin: 14px 0 4px; color: var(--text-primary); }
  .tile .k { align-items: flex-start; } .tile .k svg { flex: none; margin-top: 4px; }
  .tables th { position: sticky; top: 0; background: #1a1a19; }
  .grp { display: inline-flex; flex-wrap: wrap; align-items: center; gap: 4px 6px; }      /* "handed back" keeps with its coins */
  button.inline { font: inherit; font-style: italic; color: inherit; background: transparent; border: 0; border-bottom: 1px solid currentColor; border-radius: 0; padding: 2px 1px 1px; }
  @media (hover: hover) { button.inline:hover { background: #32322f; } }
  .setbtn { min-height: 32px; margin: 0 6px 6px 0; }
  input[type=range] { max-width: 100%; }
  html { overflow-anchor: none; }      /* the page itself keeps what is under the finger in its place (steady, in the script) */
""")
    rep("  .setbtn { margin: 0 6px 4px 0; padding: 2px 8px; font-variant-numeric: tabular-nums; white-space: nowrap; }", "  .setbtn { padding: 2px 8px; font-variant-numeric: tabular-nums; white-space: nowrap; }")
    rep("  button:hover, select:hover { background: #32322f; } button[aria-pressed=true]", "  @media (hover: hover) { button:hover, select:hover { background: #32322f; } } button[aria-pressed=true]")

    # ---------------- the page's words and their order
    between("<main>", "<script>\n/*CORE*/", """<main>
  <h1>Small change</h1>
  <p class="sub" id="lead">To pay 24 cents with American coins takes six coins; or two, if a 25 is handed over and a 1 is handed back. Choose some coins, or type your own, and pay an amount.</p>

  <figure class="viz-root" id="fig0">
    <div class="controls">
      <label>The coins of <select id="preset"></select></label>
      <label>or type your own <input type="text" id="coins" inputmode="numeric" autocomplete="off" spellcheck="false" aria-describedby="notice"></label>
      <label>Amounts from 0 to one less than <input type="number" id="L" min="2" max="1000" step="1"></label>
      <button id="apply">Count</button>
    </div>
    <p class="notice" id="notice" role="status"></p>
  </figure>

  <h2>Pay an amount</h2>
  <figure class="viz-root" id="fig3">
    <figcaption>A coin with a <b>solid ring</b> is handed over; a coin with a <b>dashed ring</b> is handed back.</figcaption>
    <div class="controls">
      <label>Amount <input type="number" id="amount" min="0" step="1" aria-describedby="amountSay"></label>
      <label><input type="range" id="amountR" min="0" step="1" aria-label="Amount"></label>
    </div>
    <p class="say" id="amountSay" role="status"></p>
    <div class="ways" id="ways"></div>
  </figure>

  <h2>On average</h2>
  <figure class="viz-root" id="fig1">
    <figcaption id="avgcap">Count every amount once, and take the average number of coins. With American coins it is 4.7. <button class="inline" data-set="1,5,18,25">Swap the 10 for an 18</button> and it is 3.89, if the coins are well chosen every time; a cashier, who takes the largest coin that fits, would need 4.58 with those coins.</figcaption>
    <div class="tiles">
      <div class="tile" id="tile-plain"><div class="k"><svg width="22" height="10" viewBox="0 0 22 10" aria-hidden="true"><line x1="1" y1="5" x2="21" y2="5" stroke="#3987e5" stroke-width="2.5"/></svg> <span><b>Fewest coins</b>: paid exactly, with as few coins as can be</span></div><div class="v"></div><div class="d"></div></div>
      <div class="tile" id="tile-greedy"><div class="k"><svg width="14" height="12" viewBox="0 0 14 12" aria-hidden="true"><circle cx="7" cy="6" r="4" fill="none" stroke="#f0efec" stroke-width="1.5"/></svg> <span><b>The cashier's way</b>: paid exactly, taking the largest coin that fits, again and again</span></div><div class="v"></div><div class="d"></div></div>
      <div class="tile" id="tile-both"><div class="k"><svg width="22" height="10" viewBox="0 0 22 10" aria-hidden="true"><line x1="1" y1="5" x2="21" y2="5" stroke="#d95926" stroke-width="2.5"/></svg> <span><b>With change</b>: coins may be handed back, and every coin that changes hands is counted</span></div><div class="v"></div><div class="d"></div></div>
    </div>
    <h3 id="capA">The coins for each amount</h3>
    <div class="chartwrap"><svg class="chart" id="chartA" viewBox="0 0 1000 300" role="img" aria-label="Number of coins for each amount, with the fewest coins and with change" tabindex="0"></svg></div>
    <div class="tip" id="tipA"></div>
    <ul class="legend" aria-label="Legend">
      <li><svg width="26" height="12" viewBox="0 0 26 12"><line x1="1" y1="6" x2="25" y2="6" stroke="#3987e5" stroke-width="4.5"/></svg> fewest coins (the wider line, so that it shows where the two run together)</li>
      <li><svg width="26" height="12" viewBox="0 0 26 12"><line x1="1" y1="6" x2="25" y2="6" stroke="#d95926" stroke-width="2.5"/></svg> with change</li>
      <li><svg width="14" height="12" viewBox="0 0 14 12"><circle cx="7" cy="6" r="4" fill="none" stroke="#f0efec" stroke-width="1.5"/></svg> where the cashier's way takes more than the fewest</li>
      <li><svg width="14" height="14" viewBox="0 0 14 14"><line x1="7" y1="0" x2="7" y2="14" stroke="#898781" stroke-width="1.5" stroke-dasharray="2 3"/></svg> the amount being paid above: tap the picture to change it</li>
    </ul>
    <p class="say" id="sayA" aria-live="polite"></p>
    <div class="controls"><button id="tA" aria-pressed="false" aria-controls="tabA">Show the table</button></div>
    <div class="tables" id="tabA"></div>
  </figure>

  <h2>One more coin</h2>
  <figure class="viz-root" id="fig2">
    <figcaption>If one more coin were added to these, which should it be? The picture gives the average with each new coin there could be; low is good. (With change, a coin larger than the amount can be handed over, so coins up to twice the largest amount are tried.)</figcaption>
    <div class="controls">
      <button id="addPlain">Add the best coin for the fewest coins</button>
      <button id="addBoth">Add the best coin for paying with change</button>
    </div>
    <p class="say" id="addedSay" role="status"></p>
    <div class="chartwrap"><svg class="chart" id="chartB" viewBox="0 0 1000 300" role="img" aria-label="The average with one more coin, against the value of the coin" tabindex="0"></svg></div>
    <div class="tip" id="tipB"></div>
    <ul class="legend" aria-label="Legend">
      <li><svg width="26" height="12" viewBox="0 0 26 12"><line x1="1" y1="6" x2="25" y2="6" stroke="#3987e5" stroke-width="2.5"/></svg> fewest coins</li>
      <li><svg width="26" height="12" viewBox="0 0 26 12"><line x1="1" y1="6" x2="25" y2="6" stroke="#d95926" stroke-width="2.5"/></svg> with change</li>
      <li><svg width="26" height="12" viewBox="0 0 26 12"><line x1="1" y1="6" x2="25" y2="6" stroke="#898781" stroke-width="1.5" stroke-dasharray="4 3"/></svg> the average now (the upper one is for the fewest coins)</li>
      <li><svg width="14" height="12" viewBox="0 0 14 12"><circle cx="7" cy="6" r="4.5" fill="none" stroke="#f0efec" stroke-width="1.5"/></svg> the best coin</li>
    </ul>
    <p class="say" id="sayB" aria-live="polite"></p>
    <div class="controls"><button id="tB" aria-pressed="false" aria-controls="tabB">Show the table</button></div>
    <div class="tables" id="tabB"></div>
  </figure>

  <h2>The best sets of coins for amounts below 100</h2>
  <figure class="viz-root" id="fig4">
    <figcaption>For each number of coins every set was tried (coins up to 99 for the fewest coins, up to 150 with change), and these have the lowest average. Press a set to try it at the top of the page. "Least possible" is what counting alone allows: no set of that many coins could do better.</figcaption>
    <h3>For the fewest coins</h3>
    <table class="best" id="best-plain"></table>
    <h3>With change</h3>
    <p class="say">From two coins up, <b>no best set has a coin of 1</b>. That comes of counting every amount once: count small amounts as likelier and the 1 comes back (the write-up has the figures).</p>
    <table class="best" id="best-both"></table>
  </figure>

  <p class="note">The sums are exact: each average is a whole number of coins divided by the number of amounts. Jeffrey Shallit asked in 2003 which coins make the average least, in a paper called "What this country needs is an 18¢ piece"; the best sets for the fewest coins are his, and are in the On-Line Encyclopedia of Integer Sequences as A366013. Those for paying with change I did not find in print. "Never more than the fewest, however large the amount" is decided by a test of D. Pearson's, as Shallit gives it. The study behind this page, with what was expected beforehand and what a referee changed, is in <a href="README.md">the write-up</a> beside it.</p>
</main>
""")
    open(H + 'out27/stage1.html', 'w', encoding='utf8').write(s); print('stage 1 (styles and words):', len(s), 'characters')
