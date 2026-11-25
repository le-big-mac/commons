// page.js: the page's own script. The sums are core.js's (LANTERN); this draws them.
(function () {
  'use strict';
  var C = window.LANTERN, $ = function (id) { return document.getElementById(id); };
  function must(cond, what) { if (!cond) { window.FAULTS = (window.FAULTS || []).concat([what]); throw new Error('must: ' + what); } }
  var A_RODS = 11, OPENING = 0.25, FIGURE = 0.3, X0_SHADE = 0.833, F_MM = 200;       // rods of 11 f; the lens's opening f/4; the painted figure 0.3 f tall; the shade fitted for 1.5 to 10 times
  var MECH = {
    right: { name: 'the rods as they should be', make: function () { return C.rods({ a: A_RODS }); } },
    plate: { name: 'the rods as Young’s engraving has them', make: function () { return C.rods({ a: 3.73, a2: 3.67, b: 3.50, p: 1.84, e: 0 }); } },      // the bar's far face read as the screen: N at the screen, I 1.84 f before the slider
    words: { name: 'the rods as the Encyclopaedia Britannica’s seventh edition has them', make: function () { var b = Math.sqrt(A_RODS * A_RODS - 1); return C.rods({ a: A_RODS, a2: b, b: b }); } },      // "the rods KN and KL must be equal": KN = KL, and IK^2 - KL^2 = f^2
    nhigh: { name: 'the screen’s pivot N a tenth of a focal length too high', make: function () { return C.rods({ a: A_RODS, yN: 0.1 }); } },
    lhigh: { name: 'the lens’s pivot L a fiftieth of a focal length too high', make: function () { return C.rods({ a: A_RODS, yL: 0.02 }); } },
    none: { name: 'no rods: the lens left where it was sharp at five times', make: function () { return null; } }
  };
  var state = { m: 5, mech: 'right', shade: false };
  function solve(st) {                       // everything the page shows, from the state
    var D = C.DofM(st.m), want = C.focus(D)[0], r = MECH[st.mech].make(), s, jam = false;
    if (r) {
      s = r.lens(D);
      if (s === null || s <= 1) { jam = true; s = null; }
    } else s = C.focus(C.DofM(5))[0];
    var out = { m: st.m, D: D, want: want, s: s, jam: jam, rods: r, mech: st.mech, shade: st.shade };
    if (!jam) {
      out.patch = C.blur(D, s); out.size = (D - s) / s;                               // the size of the (blurred) image over the slider's, by the ray through the lens's middle
      out.light = C.light(st.m, s, st.shade ? X0_SHADE : undefined); out.light10 = out.light / C.light(10, C.focus(C.DofM(10))[0], st.shade ? X0_SHADE : undefined);
      out.K = r ? r.K(D) : null;
      if (st.mech === 'right') must(out.patch < 1e-9, 'the rods as they should be leave a patch of ' + out.patch);
    }
    return out;
  }
  // ---- the ghost: a shrouded figure, drawn here (no picture is loaded)
  function ghost(ctx, cx, cy, H, alpha) {
    var w = H * 0.46, top = cy - H / 2, g = ctx.createLinearGradient(0, top, 0, top + H);
    g.addColorStop(0, 'rgba(236,242,255,' + alpha + ')'); g.addColorStop(0.55, 'rgba(206,220,250,' + alpha + ')'); g.addColorStop(1, 'rgba(160,184,235,' + (alpha * 0.75) + ')');
    ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(cx - w * 0.5, top + H);
    ctx.bezierCurveTo(cx - w * 0.62, top + H * 0.62, cx - w * 0.5, top + H * 0.30, cx - w * 0.30, top + H * 0.17);
    ctx.bezierCurveTo(cx - w * 0.30, top + H * 0.02, cx + w * 0.30, top + H * 0.02, cx + w * 0.30, top + H * 0.17);
    ctx.bezierCurveTo(cx + w * 0.5, top + H * 0.30, cx + w * 0.62, top + H * 0.62, cx + w * 0.5, top + H);
    for (var i = 0; i < 4; i++) { var x1 = cx + w * 0.5 - (i + 0.5) * w / 4, x2 = cx + w * 0.5 - (i + 1) * w / 4; ctx.quadraticCurveTo(x1, top + H * (i % 2 ? 0.90 : 0.93), x2, top + H); }
    ctx.closePath(); ctx.fill();
    ctx.fillStyle = 'rgba(8,8,14,' + Math.min(1, alpha * 1.2) + ')';
    [-1, 1].forEach(function (k) { ctx.beginPath(); ctx.ellipse(cx + k * w * 0.13, top + H * 0.155, w * 0.055, H * 0.030, 0, 0, 6.2832); ctx.fill(); });
    ctx.beginPath(); ctx.ellipse(cx, top + H * 0.235, w * 0.05, H * 0.035, 0, 0, 6.2832); ctx.fill();
  }
  function drawSeen(o) {
    var cv = $('seen'), ctx = cv.getContext('2d'), W = cv.width, Hh = cv.height, k = 62;       // 62 pixels to a focal length: a ghost of 20 times is 372 pixels tall
    ctx.filter = 'none'; ctx.fillStyle = '#050507'; ctx.fillRect(0, 0, W, Hh);
    if (o.jam) return { H: 0, blurPx: 0, alpha: 0 };
    var H = o.size * FIGURE * k, blurPx = o.patch * OPENING * k / 2, alpha = Math.max(0.04, Math.min(1, Math.pow(o.light10, 1 / 2.2) * 0.62));
    blurPx = Math.min(blurPx, 60); H = Math.min(H, Hh - 24);
    ctx.save(); ctx.filter = blurPx > 0.15 ? 'blur(' + blurPx.toFixed(2) + 'px)' : 'none'; ghost(ctx, W / 2, Hh / 2, H, alpha); ctx.restore(); ctx.filter = 'none';
    return { H: H, blurPx: blurPx, alpha: alpha };
  }
  function drawBehind(o) {
    var cv = $('behind'), ctx = cv.getContext('2d'), W = cv.width, Hh = cv.height, k = 30, xs = W - 46, yp = Hh - 78, ya = yp - 1.25 * k;   // the screen's place; the pivots' line; the lens's axis
    ctx.fillStyle = '#0b0b10'; ctx.fillRect(0, 0, W, Hh);
    var X = function (u) { return xs - (o.D - u) * k; }, Y = function (v) { return yp - v * k; };      // u: distance from the slider; v: height above the pivots' line
    ctx.strokeStyle = '#3a3a44'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(0, Hh - 40); ctx.lineTo(W, Hh - 40); ctx.stroke();      // the floor
    ctx.strokeStyle = '#cfd6ea'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(xs, 20); ctx.lineTo(xs, Hh - 40); ctx.stroke();         // the screen
    var bx0 = X(-3.4), bx1 = X(0.25); ctx.fillStyle = '#23232c'; ctx.strokeStyle = '#8a8fa3'; ctx.lineWidth = 1.5;
    ctx.fillRect(bx0, ya - 0.95 * k, bx1 - bx0, (Hh - 62) - (ya - 0.95 * k)); ctx.strokeRect(bx0, ya - 0.95 * k, bx1 - bx0, (Hh - 62) - (ya - 0.95 * k));   // the box
    [bx0 + 0.7 * k, bx1 - 0.7 * k].forEach(function (wx) { ctx.beginPath(); ctx.arc(wx, Hh - 51, 11, 0, 6.2832); ctx.fillStyle = '#14141a'; ctx.fill(); ctx.stroke(); });
    var lamp = ctx.createRadialGradient(X(-2.3), ya, 2, X(-2.3), ya, 26); lamp.addColorStop(0, 'rgba(255,214,150,0.95)'); lamp.addColorStop(1, 'rgba(255,214,150,0)'); ctx.fillStyle = lamp; ctx.fillRect(X(-2.3) - 26, ya - 26, 52, 52);
    ctx.strokeStyle = '#e9c98a'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(X(0), ya - 0.28 * k); ctx.lineTo(X(0), ya + 0.28 * k); ctx.stroke();      // the painted slider
    var marks = { slider: [X(0), ya], screen: [xs, ya] };
    if (!o.jam) {
      var xl = X(o.s), half = o.size * FIGURE / 2 * k;
      ctx.fillStyle = 'rgba(214,226,255,0.10)'; ctx.beginPath(); ctx.moveTo(xl, ya); ctx.lineTo(xs, ya - half); ctx.lineTo(xs, ya + half); ctx.closePath(); ctx.fill();     // the light on its way to the screen
      ctx.strokeStyle = '#8a8fa3'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(bx1, ya + 0.62 * k); ctx.lineTo(xl + 1.02 * k, ya + 0.62 * k); ctx.stroke();               // the lens's bar
      ctx.strokeStyle = '#9fd0ff'; ctx.fillStyle = 'rgba(159,208,255,0.35)'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.ellipse(xl, ya, 0.07 * k, OPENING * k * 1.6, 0, 0, 6.2832); ctx.fill(); ctx.stroke();
      marks.lens = [xl, ya];
      if (o.rods && o.K) {
        var r = o.rods, I = [X(r.p), Y(r.yI)], L = [X(o.s + r.q), Y(r.yL)], N = [xs + r.e * k, Y(r.yN)], K = [X(o.K[0]), Y(o.K[1])];
        ctx.strokeStyle = '#8a8fa3'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(bx1, Hh - 70); ctx.lineTo(I[0], Hh - 70); ctx.lineTo(I[0], I[1]); ctx.stroke();           // the bracket that carries I
        ctx.beginPath(); ctx.moveTo(L[0], ya + 0.62 * k); ctx.lineTo(L[0], L[1]); ctx.stroke();                                                                            // the lens's bar turned down to L
        ctx.strokeStyle = '#eb6834'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(I[0], I[1]); ctx.lineTo(K[0], K[1]); ctx.lineTo(N[0], N[1]); ctx.stroke();
        ctx.strokeStyle = '#f0a37f'; ctx.beginPath(); ctx.moveTo(K[0], K[1]); ctx.lineTo(L[0], L[1]); ctx.stroke();
        ctx.fillStyle = '#f4f4f6'; [I, L, N, K].forEach(function (p) { ctx.beginPath(); ctx.arc(p[0], p[1], 3.5, 0, 6.2832); ctx.fill(); });
        ctx.font = '13px system-ui, sans-serif'; ctx.fillStyle = '#f4f4f6'; ctx.fillText('I', I[0] - 12, I[1] + 16); ctx.fillText('L', L[0] + 5, L[1] + 16); ctx.fillText('N', N[0] + 7, N[1] + 5); ctx.fillText('K', K[0] + 7, Math.max(K[1] - 4, 14));
        marks.I = I; marks.L = L; marks.N = N; marks.K = K;
      }
    }
    ctx.font = '12px system-ui, sans-serif'; ctx.fillStyle = '#9a9eb0'; ctx.fillText('the screen', xs - 64, 16); ctx.fillText('the lantern', Math.max(bx0 + 6, 4), ya - 0.95 * k - 6);
    return marks;
  }
  function fmt(x, d) { return x.toFixed(d); }
  function show() {
    var o = solve(state), seen = drawSeen(o), marks = drawBehind(o);
    var rr = MECH[state.mech].make(); $('cap-behind').textContent = 'To scale, in focal lengths of the lens. ' + (rr ? 'The rods IK and KN (orange) are ' + fmt(rr.a, 2) + ' and ' + fmt(rr.a2, 2) + ' focal lengths long; KL (paler), ' + fmt(rr.b, 2) + ', moves the lens. I is fixed to the lantern, N to the screen, L to the lens.' : 'No rods: the lens stays where it was put.');
    $('r-m').textContent = 'The lantern stands where a sharp ghost would be ' + fmt(state.m, 2) + ' times its painted figure.';
    if (o.jam) {
      $('r-lens').textContent = 'The rods jam: they cannot bring the lens to this place, or do not reach.'; $('r-patch').textContent = ''; $('r-light').textContent = '';
    } else {
      $('r-lens').textContent = 'The lens stands ' + fmt(o.s, 4) + ' focal lengths from the slider. A sharp image wants ' + fmt(o.want, 4) + '.';
      $('r-patch').textContent = 'One point of the figure makes a patch ' + fmt(o.patch, 4) + ' of the lens’s opening wide on the screen' + (o.patch < 5e-5 ? ': sharp.' : ' (' + fmt(o.patch * OPENING * F_MM, 1) + ' mm, with a lens of ' + F_MM + ' mm and an opening of ' + (OPENING * F_MM) + ' mm, on a ghost ' + fmt(o.size * FIGURE * F_MM, 0) + ' mm tall).');
      $('r-light').textContent = 'It is ' + (o.light10 >= 10 ? fmt(o.light10, 0) : fmt(o.light10, 2)) + ' times as bright as a sharp ghost of ten times ' + (state.shade ? 'under the same shade.' : 'with no shade.');
    }
    $('slider').value = String(Math.round(1000 * Math.log(state.m) / Math.log(20)));
    var rb = document.querySelector('input[name=mech][value=' + state.mech + ']'); if (rb) rb.checked = true; $('shade').checked = !!state.shade;      // the buttons kept in step with what is shown
    window.SHOWN = { caption: $('cap-behind').textContent, o: { m: o.m, D: o.D, s: o.s, want: o.want, jam: o.jam, patch: o.jam ? null : o.patch, size: o.jam ? null : o.size, light10: o.jam ? null : o.light10, K: o.K || null }, seen: seen, marks: marks };
  }
  function set(ch) { for (var k in ch) state[k] = ch[k]; state.m = Math.max(1, Math.min(20, state.m)); show(); }
  window.SET = set; window.STATE = function () { return JSON.parse(JSON.stringify(state)); };
  var timer = null;
  function advance() {
    if (timer) { clearInterval(timer); timer = null; $('go').textContent = 'Let it advance and retire'; return; }
    var t0 = performance.now(); $('go').textContent = 'Stop';
    timer = setInterval(function () {
      var t = (performance.now() - t0) / 1000, ph = (t % 16) / 16, u = ph < 0.5 ? ph * 2 : 2 - ph * 2;      // 8 seconds out, 8 back
      set({ m: Math.exp(Math.log(1.3) + u * (Math.log(18) - Math.log(1.3))) });
    }, 40);
  }
  window.addEventListener('DOMContentLoaded', function () {
    $('slider').addEventListener('input', function (e) { set({ m: Math.pow(20, Number(e.target.value) / 1000) }); });
    Array.prototype.forEach.call(document.querySelectorAll('input[name=mech]'), function (el) { el.addEventListener('change', function () { set({ mech: el.value }); }); });
    $('shade').addEventListener('change', function (e) { set({ shade: e.target.checked }); });
    $('go').addEventListener('click', advance);
    show();
  });
})();
