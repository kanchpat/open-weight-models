/* OpenWeights course shell. Depends on course.js (CHAPTERS, LESSONS, LABS, ...) and SOURCES (injected by build.py). */
(function () {
  'use strict';
  const $ = (s, r) => (r || document).querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const md = (s) => esc(s)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
    .replace(/\*([^*]+)\*/g, '<i>$1</i>')
    .replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  const store = {
    get() { try { return JSON.parse(localStorage.getItem('ow2') || '{}'); } catch (e) { return {}; } },
    set(v) { try { localStorage.setItem('ow2', JSON.stringify(v)); } catch (e) { /* private mode */ } },
  };
  const saved = store.get();
  saved.done = saved.done || {};
  const I = {
    arrow: '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    back: '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
    replay: '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>',
    pause: '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M8 5v14M16 5v14"/></svg>',
    play: '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><path d="M7 5l12 7-12 7z"/></svg>',
    spark: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="4"/><path d="M12 7l1.4 3.6L17 12l-3.6 1.4L12 17l-1.4-3.6L7 12l3.6-1.4z"/></svg>',
    clock: '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    ext: '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
  };
  const folder = (c) => '<svg class="folder" viewBox="0 0 20 16"><path d="M1 3a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2z" fill="' + c + '" stroke="rgba(0,0,0,.35)" stroke-width="1"/></svg>';
  const byId = (id) => LESSONS.find((l) => l.id === id);
  const chapterOf = (l) => CHAPTERS.find((c) => c.id === l.ch);

  // ------------------------------------------------------------ routing
  function parse() {
    const p = location.hash.replace(/^#\/?/, '').split('/').filter(Boolean);
    if (p[0] === 'tools') return { tab: 'tools', tool: ['breakeven', 'license', 'router'].includes(p[1]) ? p[1] : 'breakeven' };
    if (p[0] === 'labs') return { tab: 'labs' };
    if (p[0] === 'cheatsheets') return { tab: 'cheatsheets' };
    const lesson = byId(p[1]) || byId(saved.last) || LESSONS[0];
    const step = Math.min(Math.max(parseInt(p[2], 10) || 1, 1), lesson.steps.length);
    return { tab: 'learn', lesson, step };
  }
  const go = (h) => { location.hash = h; };
  let prev = { lesson: null, step: 0 };
  let paused = false;

  // ------------------------------------------------------------ sidebar
  function sidebar(r) {
    const cur = r.tab === 'learn' ? r.lesson : null;
    const doneN = LESSONS.filter((l) => saved.done[l.id]).length;
    let h = '<div class="side-h"><span>Course outline</span><small>' + LESSONS.length + ' lessons</small></div><div class="tree">';
    CHAPTERS.forEach((c) => {
      const ls = LESSONS.filter((l) => l.ch === c.id);
      const open = cur ? cur.ch === c.id : c.id === '01';
      h += '<button class="ch' + (open ? ' open' : '') + '" data-ch="' + c.id + '"><span class="cv">›</span>' + '<span class="cb" style="background:' + c.color + '">' + c.id + '</span><span>' + esc(c.name) + '</span><span class="cnt">' +
        ls.filter((l) => saved.done[l.id]).length + '/' + ls.length + '</span></button><div class="lessons">';
      ls.forEach((l) => {
        h += '<a class="ls' + (cur === l ? ' on' : '') + (saved.done[l.id] ? ' done' : '') + '" href="#/learn/' + l.id + '/1"><i class="dot"></i>' + esc(l.title) + '</a>';
      });
      h += '</div>';
    });
    h += '</div><div class="card progress"><span>PROGRESS</span><span class="bar"><i style="width:' + Math.round(doneN / LESSONS.length * 100) + '%"></i></span><span>' + doneN + ' / ' + LESSONS.length + '</span></div>';
    return '<aside class="side">' + h + '</aside>';
  }

  // ------------------------------------------------------------ scenes
  const PAL = {
    sand: ['#F2ECE4', '#9E5A14'], green: ['#E3F0E8', '#2D6A4F'], blue: ['#E4ECF5', '#2F5D8A'],
    violet: ['#EEE4F2', '#4A235A'], orange: ['#FCEBD9', '#D9822B'], red: ['#FBE4DC', '#C85028'],
  };
  const NW = 152;
  const ctr = (n) => [n.x, n.y + 15 + (n.h || 46) / 2];
  const boxH = (label) => 36 + String(label).split('\n').length * 19;
  function nodeSvg(id, n, label, cls) {
    const p = PAL[n.c] || PAL.sand, lines = String(label).split('\n'), bh = boxH(label), c = ctr(n), x0 = c[0] - NW / 2, y0 = c[1] - bh / 2;
    let t = '';
    lines.forEach((ln, i) => { t += '<text x="' + c[0] + '" y="' + (c[1] - lines.length * 9.5 + 14.5 + i * 19).toFixed(1) + '">' + esc(ln) + '</text>'; });
    return '<g class="n ' + cls + '" data-n="' + id + '">' +
      '<rect x="' + x0 + '" y="' + y0 + '" width="' + NW + '" height="' + bh + '" rx="14" fill="' + p[0] + '" stroke="' + p[1] + '" stroke-width="1.6"/>' +
      '<rect x="' + (x0 + 18) + '" y="' + (y0 + bh - 2.5) + '" width="' + (NW - 36) + '" height="5" rx="2.5" fill="' + p[1] + '"/>' +
      (n.top ? '<rect x="' + (c[0] - 20) + '" y="' + (y0 - 13) + '" width="40" height="25" rx="12.5" fill="' + p[1] + '"/><text class="tp" x="' + c[0] + '" y="' + (y0 + 4.5) + '">' + esc(n.top) + '</text>' : '') + t + '</g>';
  }
  function isoScene(lesson, step, fresh) {
    const sc = lesson.scene, nodes = sc.nodes;
    const show = step.show || Object.keys(nodes);
    const hot = step.hot && step.hot.length ? step.hot : show;
    const lab = (id) => (step.labels && step.labels[id]) || nodes[id].label;
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    Object.keys(nodes).forEach((id) => { const c = ctr(nodes[id]); x0 = Math.min(x0, c[0] - NW / 2); x1 = Math.max(x1, c[0] + NW / 2); y0 = Math.min(y0, c[1] - 48); y1 = Math.max(y1, c[1] + 48); });
    y0 -= 44;
    (sc.texts || []).forEach((t) => { y0 = Math.min(y0, t.y - 16); y1 = Math.max(y1, t.y + 6); });
    const vb = [x0 - 26, y0 - 8, x1 - x0 + 52, y1 - y0 + 30].map((v) => Math.round(v));
    let s = '<svg viewBox="' + vb.join(' ') + '" preserveAspectRatio="xMidYMid meet"><defs>' +
      '<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="var(--line-2)" opacity=".7"/></pattern>' +
      '<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 1 L9 5 L0 9 Z" fill="var(--ink)"/></marker></defs>' +
      '<rect x="' + (vb[0] - 400) + '" y="' + (vb[1] - 400) + '" width="' + (vb[2] + 800) + '" height="' + (vb[3] + 800) + '" fill="url(#grid)"/>';
    (sc.texts || []).forEach((t) => { s += '<text class="axis" x="' + t.x + '" y="' + t.y + '"' + (t.a ? ' style="text-anchor:' + t.a + '"' : '') + '>' + esc(t.t) + '</text>'; });
    (step.edges || []).forEach((e) => {
      const a = ctr(nodes[e[0]]), b = ctr(nodes[e[1]]);
      const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
      const reach = (id) => Math.min((NW / 2 + 7) / (Math.abs(ux) || 1e-9), (boxH(lab(id)) / 2 + 9) / (Math.abs(uy) || 1e-9));
      const ta = reach(e[0]), tb = reach(e[1]) + 3;
      const d = 'M' + (a[0] + ux * ta).toFixed(1) + ',' + (a[1] + uy * ta).toFixed(1) + ' L' + (b[0] - ux * tb).toFixed(1) + ',' + (b[1] - uy * tb).toFixed(1);
      const fail = e[2] === 'fail';
      s += (fail ? '' : '<path class="flow' + (e[2] === 'slow' ? ' slow' : '') + '" d="' + d + '"/>') + '<path class="edge' + (fail ? ' fail' : '') + '" d="' + d + '" marker-end="url(#ah)"/>';
    });
    show.forEach((id) => { s += nodeSvg(id, nodes[id], lab(id), (hot.includes(id) ? '' : 'dim') + (fresh.includes(id) ? ' in' : '')); });
    if (step.bubble) {
      const n = nodes[step.bubble[0]], c = ctr(n), txt = step.bubble[1], w = txt.length * 8.2 + 30, by = c[1] - boxH(lab(step.bubble[0])) / 2 - (n.top ? 50 : 38);
      s += '<g class="bub"><rect x="' + (c[0] - w / 2) + '" y="' + by + '" width="' + w + '" height="28" rx="14"/><text x="' + c[0] + '" y="' + (by + 19) + '">' + esc(txt) + '</text></g>';
    }
    return s + '</svg>';
  }
  const BARC = { green: '#2D6A4F', red: '#C85028', orange: '#D9822B', sand: '#B9A98F', blue: '#2F5D8A', violet: '#4A235A' };
  function barsHtml(rows, max, unit) {
    if (!rows.length) return '<div class="bars"><div class="empty">?</div></div>';
    return '<div class="bars"><div class="unit">' + esc(unit) + '</div>' + rows.map((b) =>
      '<div class="bar-row' + (b.hot ? ' hot' : '') + '"><span>' + esc(b.l) + '</span><div class="tr"><div class="fl" data-w="' + Math.max(2, Math.min(100, b.v / max * 100)).toFixed(1) + '" style="background:' + (BARC[b.c] || BARC.sand) + '"></div></div><b>' + esc(b.t) + '</b></div>').join('') + '</div>';
  }
  function growBars(root) {
    requestAnimationFrame(() => requestAnimationFrame(() => root.querySelectorAll('.fl').forEach((f) => { f.style.width = f.dataset.w + '%'; })));
  }

  // ------------------------------------------------------------ learn view
  function learn(r) {
    const l = r.lesson, i = r.step - 1, st = l.steps[i], n = l.steps.length, ch = chapterOf(l);
    const sameLesson = prev.lesson === l;
    const before = sameLesson && prev.step >= 1 ? l.steps[prev.step - 1] : null;
    const idx = LESSONS.indexOf(l), nextL = LESSONS[idx + 1];
    const chLessons = LESSONS.filter((x) => x.ch === l.ch);
    if (r.step === n && !saved.done[l.id]) { saved.done[l.id] = true; }
    saved.last = l.id; store.set(saved);

    let chips = '';
    l.chips.forEach((c, k) => {
      const v = st.chips[k] == null ? '?' : st.chips[k];
      const isNew = before && before.chips[k] !== v && v !== '?';
      chips += '<div class="chip' + (isNew ? ' new' : '') + '"><small>' + esc(c) + '</small><b>' + esc(v) + '</b></div>';
    });
    let canvas;
    if (l.scene.type === 'bars') canvas = barsHtml(st.bars || [], l.scene.max, l.scene.unit);
    else {
      const was = before ? (before.show || []) : [];
      canvas = isoScene(l, st, (st.show || []).filter((id) => !was.includes(id)));
    }
    const brief = st.brief ? '<div class="brief"><h4>' + esc(st.brief.t) + '</h4><div>' + st.brief.l.map((x) => '<span>' + esc(x) + '</span>').join('') + '</div></div>' : '';
    const segs = l.steps.map((s, k) => '<button class="sg' + (k === i ? ' on' : k < i ? ' past' : '') + '" data-go="#/learn/' + l.id + '/' + (k + 1) + '" title="' + esc(s.title) + '"><i></i><span>' + (k + 1) + ' · ' + esc(s.rail) + '</span></button>').join('');
    const tagCls = st.tag.split(' ')[0];
    let extra = '';
    if (l.tool && (i === n - 1 || st.tag === 'FIX')) extra += '<a class="btn" href="#/tools/' + l.tool + '">' + I.ext + 'Open the ' + ({ license: 'License Triage', breakeven: 'Break-Even Calculator', router: 'Workload Router' })[l.tool] + '</a>';
    if (l.id === 'build-on-gcp' && i === n - 1) extra += '<a class="btn" href="#/labs">' + I.ext + 'Open Labs</a>';
    const nextHref = i < n - 1 ? '#/learn/' + l.id + '/' + (r.step + 1) : nextL ? '#/learn/' + nextL.id + '/1' : '#/labs';
    const nextLabel = i < n - 1 ? 'Next: ' + l.steps[i + 1].rail : nextL ? 'Next lesson: ' + nextL.title : 'Go to Labs';
    const L = l.learn.length;
    const learnList = l.learn.map((t, k) => {
      const ok = i >= Math.max(1, Math.round((k + 1) * (n - 1) / L));
      return '<li class="' + (ok ? 'ok' : '') + '"><i>' + (ok ? '✓' : '') + '</i>' + esc(t) + '</li>';
    }).join('');
    const head = '<header><div class="crumb">Chapter ' + ch.id + ' · ' + esc(ch.name) + ' &nbsp;/&nbsp; Lesson ' + (chLessons.indexOf(l) + 1) + ' of ' + chLessons.length + '</div>' +
      '<div class="lh"><div><h1>' + esc(l.title) + '</h1><p>' + esc(l.sub) + '</p></div><div class="pills"><span class="pill o">' + I.clock + l.mins + ' min</span><span class="pill g">' + esc(l.level) + '</span><span class="pill v">' + n + ' steps</span></div></div></header>';
    const narr = '<article class="card narr"><div class="step-h"><span>Step ' + r.step + ' of ' + n + '</span><span class="tag ' + tagCls + '">' + esc(st.tag) + '</span></div>' +
      '<h2>' + esc(st.title) + '</h2>' + st.body.map((p) => '<p>' + md(p) + '</p>').join('') +
      '<div class="key"><small>Key idea</small>' + md(st.key) + '</div>' + (extra ? '<div class="extra">' + extra + '</div>' : '') +
      '<div class="nav"><button class="btn ghost" data-go="#/learn/' + l.id + '/' + (r.step - 1) + '"' + (i === 0 ? ' disabled' : '') + '>' + I.back + 'Back</button>' +
      '<button class="btn pri" data-go="' + nextHref + '"><span>' + esc(nextLabel) + '</span>' + I.arrow + '</button></div></article>';
    const stage = '<div class="card stage"><div class="stage-top">' + chips + '<div class="ctl"><button class="btn" id="replay">' + I.replay + 'Replay</button>' +
      (l.scene.type === 'iso' ? '<button class="btn" id="pause">' + (paused ? I.play + 'Play' : I.pause + 'Pause') + '</button>' : '') + '</div></div>' +
      '<div class="canvas' + (paused ? ' paused' : '') + '" id="canvas">' + canvas + '</div>' + brief + '</div>';
    const strip = '<div class="card learn"><h3>You\'ll learn</h3><ul>' + learnList + '</ul>' +
      (l.source ? '<p><a href="' + l.source.url + '" target="_blank" rel="noopener">Source: ' + esc(l.source.label) + '</a></p>' : '') + '</div>';
    prev = { lesson: l, step: r.step };
    return '<section class="lesson">' + head + '<div class="steps">' + segs + '</div><div class="split">' + narr + stage + '</div>' + strip + '</section>';
  }

  // ------------------------------------------------------------ tools
  const money = (v) => '$' + Math.round(v).toLocaleString('en-US');
  function tools(r) {
    const tabs = [['breakeven', 'Break-Even Calculator'], ['license', 'License Triage'], ['router', 'Workload Router']];
    let h = '<section class="card page"><div class="crumb">Tools</div><h1>' + tabs.find((t) => t[0] === r.tool)[1] + '</h1>' +
      '<div class="pills" style="margin:10px 0 16px">' + tabs.map((t) => '<a class="pill ' + (t[0] === r.tool ? 'g' : '') + '" style="text-decoration:none" href="#/tools/' + t[0] + '">' + t[1] + '</a>').join('') + '</div>';
    if (r.tool === 'breakeven') {
      h += '<p class="sub">Serverless OpenMaaS vs. dedicated GPUs. Move the sliders to see where the 73% duty-cycle line falls for your volume. <a href="#/learn/duty-cycle-rule/1">Take the lesson</a>.</p>' +
        '<div class="grid" style="grid-template-columns:1fr 1fr;gap:18px"><label class="field"><span>Token volume: <b id="tv"></b></span><input type="range" id="tok" min="1" max="150" value="' + (saved.tok || 25) + '"></label>' +
        '<label class="field"><span>Hardware utilization: <b id="dv"></b></span><input type="range" id="duty" min="10" max="95" value="' + (saved.duty || 35) + '"></label></div>' +
        '<div class="stage" style="min-height:0;margin-top:14px"><div class="canvas" style="min-height:290px" id="be"></div></div><div id="verdict"></div>' +
        '<p class="sub" style="margin-top:12px">Planning model from the playbook: closed frontier API at $10.00 per 1M tokens, OpenMaaS PayGo at $0.907, dedicated cost scaled by 73% ÷ utilization, System 1 triage at $0.05. Illustrative, not a quote.</p>';
    } else if (r.tool === 'license') {
      const sel = (id, label, opts, def) => '<label class="field">' + label + '<select id="' + id + '">' + opts.map((o, k) => '<option value="' + (k + 1) + '"' + ((saved[id] || def) === k + 1 ? ' selected' : '') + '>' + esc(o) + '</option>').join('') + '</select></label>';
      h += '<p class="sub">Set your company profile to see which open-weight models are approved, conditional or restricted. Informational planning only, not legal advice. <a href="#/learn/license-triage/1">Take the lesson</a>.</p>' +
        '<div class="grid g4">' + sel('val', 'Company valuation', ['$50M growth', '$500M mid-market', '$2B late stage', '$10B enterprise gate', '$50B+ global Fortune 500'], 4) +
        sel('mau', 'Monthly active users', ['<1M users', '10M users', '50M users', '100M+ cap (Kimi / $20M rev)', '700M+ cap (Llama 4)'], 3) +
        sel('reg', 'Sovereignty policy', ['Global (any origin)', 'US / EU regulated only', 'Strict EU sovereign air-gap'], 1) +
        sel('aud', 'Data auditability', ['Level 1: weights only', 'Level 2: weights + open recipe', 'Level 3: full pre-training data (Tier 4)'], 1) + '</div>' +
        '<div class="sec" id="tally"></div><div id="lic"></div>';
    } else {
      h += '<p class="sub">Pick the quadrant that matches a workload to see its reference stack on Google Cloud. <a href="#/learn/workload-router/1">Take the lesson</a>.</p>' +
        '<div class="grid" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px"><div><div class="sec" style="margin-top:0">↑ SOVEREIGNTY / CUSTOMIZATION</div><div class="quad">' +
        ['2', '1', '3', '4'].map((q) => '<button class="qb" data-q="' + q + '"><b>QUADRANT ' + esc(QUADRANTS[q].name.toUpperCase()) + '</b><span>' + esc(QUADRANTS[q].head) + '</span><small>' + esc(QUADRANTS[q].sub) + '</small></button>').join('') +
        '</div><div class="sec" style="text-align:right">TOKEN VELOCITY / DUTY CYCLE →</div></div><div class="box" id="qd"></div></div>';
    }
    return h + '</section>';
  }
  function wireTools(r) {
    if (r.tool === 'breakeven') {
      const tok = $('#tok'), duty = $('#duty');
      const up = () => {
        const dailyM = +tok.value, d = +duty.value, monthlyM = dailyM * 30, maas = 0.907, ded = maas * (73 / d);
        const tc = monthlyM * 10, tm = monthlyM * maas, td = monthlyM * ded, ts = Math.max(45, monthlyM * 0.05), mx = Math.max(tc, td, tm);
        $('#tv').textContent = dailyM + 'M tokens/day (' + monthlyM.toLocaleString('en-US') + 'M/mo)';
        $('#dv').textContent = d + '% duty cycle';
        const rows = [{ l: 'Closed frontier API', v: tc, t: money(tc) + '/mo', c: 'orange' }, { l: 'Vertex AI OpenMaaS PayGo', v: tm, t: money(tm) + '/mo', c: 'green', hot: d < 73 },
          { l: 'Dedicated GPUs ($' + ded.toFixed(2) + '/1M)', v: td, t: money(td) + '/mo', c: d < 73 ? 'red' : 'green', hot: d >= 73 }, { l: 'System 1 triage heads', v: ts, t: money(ts) + '/mo', c: 'blue' }];
        const be = $('#be');
        if (!be.firstChild) { be.innerHTML = barsHtml(rows, mx, 'monthly cost'); be.querySelectorAll('.bar-row').forEach((x) => { x.style.gridTemplateColumns = '230px 1fr 120px'; }); }
        be.querySelectorAll('.bar-row').forEach((row, k) => {
          const b = rows[k];
          row.className = 'bar-row' + (b.hot ? ' hot' : '');
          row.children[0].textContent = b.l; row.children[2].textContent = b.t;
          const f = row.querySelector('.fl'); f.style.background = BARC[b.c]; f.style.width = Math.max(2, b.v / mx * 100).toFixed(1) + '%';
        });
        const save = Math.round((1 - Math.min(tm, td) / tc) * 100);
        let t, x, ok = false;
        if (dailyM < 8 && d < 73) { t = 'Pilot volume (<8M tokens/day): stay serverless'; x = 'At ' + dailyM + 'M tokens/day and ' + d + '% utilization, keep zero-ops endpoints on Vertex AI OpenMaaS PayGo (' + money(tm) + '/mo, $0 idle burn) or closed frontier APIs. Reserving 24/7 GPUs would cost ' + money(td) + '/mo, ' + (ded / maas).toFixed(2) + '× PayGo.'; }
        else if (d < 73) { t = 'Below 73% duty cycle: start serverless'; x = 'At ' + d + '% utilization, dedicated GPUs burn idle budget on nights and weekends (' + money(td) + '/mo, ' + (ded / maas).toFixed(2) + '× PayGo). Deploy on Vertex AI OpenMaaS (' + money(tm) + '/mo) or Cloud Run scale-to-zero vLLM GPUs until steady traffic clears 73% (series Parts 2 and 4).'; }
        else { ok = true; t = 'Above 73% duty cycle: a dedicated GPU cluster is justified'; x = 'At ' + d + '% sustained utilization, dedicated vLLM instances (' + money(td) + '/mo) clear the 73% line, saving ' + money(Math.max(0, tm - td)) + '/mo vs. PayGo and ' + save + '% vs. closed APIs. Pair with committed use discounts and System 1 triage heads (' + money(ts) + '/mo).'; }
        $('#verdict').innerHTML = '<div class="verdict' + (ok ? ' ok' : '') + '"><b>' + esc(t) + '</b>' + esc(x) + '</div>';
        saved.tok = dailyM; saved.duty = d; store.set(saved);
      };
      tok.oninput = up; duty.oninput = up; up();
    } else if (r.tool === 'license') {
      const ids = ['val', 'mau', 'reg', 'aud'];
      const up = () => {
        const [val, mau, reg, aud] = ids.map((id) => +$('#' + id).value);
        ids.forEach((id) => { saved[id] = +$('#' + id).value; }); store.set(saved);
        const cnt = { green: 0, amber: 0, red: 0 };
        $('#lic').innerHTML = LICENSE_MODELS.map((m) => {
          let s = 'green', badge = m.auditLevel === 3 ? 'Tier 4 approved' : 'Default approved';
          const why = [];
          if (m.ncAdapter) { s = 'red'; badge = 'Non-commercial adapter'; why.push('CC BY-NC 4.0 adapter prohibits commercial production use'); }
          if (val >= 4 && m.cap10b) { s = 'red'; badge = 'Hits $10B gate'; why.push('Exceeds $10B corporate valuation/revenue gate: requires a commercial deal'); }
          if (mau >= 4 && m.cap100m && s !== 'red') { s = 'amber'; badge = 'Hits 100M MAU cap'; why.push('Requires a custom commercial agreement above 100M MAU / $20M revenue'); }
          if (mau >= 5 && m.cap700m && !m.cap100m && s !== 'red') { s = 'amber'; badge = 'Hits 700M MAU cap'; why.push('Requires a custom commercial agreement above 700M MAU'); }
          if (reg === 2 && m.origin !== 'US' && m.origin !== 'EU') { s = 'red'; badge = 'Origin policy gate'; why.push('Blocked by US/EU-only origin filter (' + m.origin + ')'); }
          if (reg === 3 && m.origin !== 'EU') {
            if (m.origin === 'US' && s !== 'red') { s = 'amber'; badge = 'US origin (host in EU VPC)'; why.push('US-origin checkpoint: deploy inside an EU sovereign VPC perimeter'); }
            else { s = 'red'; badge = 'Non-EU origin'; why.push('Restricted under strict EU-origin sovereign policy (' + m.origin + ')'); }
          }
          if (aud > m.auditLevel) {
            if (s !== 'red') { s = 'amber'; badge = aud === 3 ? 'Weights only (not Tier 4)' : 'Recipe undisclosed'; }
            why.push(aud === 3 ? 'Pre-training data corpus not publicly auditable' : 'Post-training recipe not fully disclosed');
          }
          cnt[s]++;
          return '<div class="trow"><div><b>' + esc(m.name) + '</b><small>' + esc(m.note) + '</small>' + (why.length ? '<small class="why">' + esc(why.join(' · ')) + '</small>' : '') + '</div><span class="pill ' + ({ green: 'g', amber: 'o', red: 'r' })[s] + '">' + esc(badge) + '</span></div>';
        }).join('');
        $('#tally').textContent = cnt.green + ' APPROVED · ' + cnt.amber + ' CONDITIONAL · ' + cnt.red + ' RESTRICTED';
      };
      ids.forEach((id) => { $('#' + id).onchange = up; }); up();
    } else {
      const pick = (q) => {
        document.querySelectorAll('.qb').forEach((b) => b.classList.toggle('on', b.dataset.q === q));
        const d = QUADRANTS[q];
        $('#qd').innerHTML = '<div class="lab-top"><span class="pill v">Quadrant ' + esc(d.name) + '</span><span class="pill o">' + esc(d.parts) + '</span></div><h3>' + esc(d.head) + '</h3><p>' + esc(d.desc) + '</p><div class="sec">REFERENCE STACK</div><p>' + esc(d.stack) + '</p><div class="links"><a class="btn" href="#/labs">' + I.ext + 'See the matching lab</a></div>';
        saved.q = q; store.set(saved);
      };
      document.querySelectorAll('.qb').forEach((b) => { b.onclick = () => pick(b.dataset.q); });
      pick(saved.q || '2');
    }
  }

  // ------------------------------------------------------------ labs + cheatsheets
  function labs() {
    return '<section class="card page"><div class="crumb">Labs</div><h1>The 7-Part Code & Video Series</h1><p class="sub">Each part turns a layer of the playbook into runnable Google Cloud code, with a short video walkthrough.</p><div class="grid g3">' +
      LABS.map((p) => '<div class="box"><div class="lab-top"><span class="pill ' + (p.live ? 'g' : '') + '">Part ' + p.n + '</span><small>' + esc(p.date) + (p.live ? ' · live' : ' · coming soon') + '</small></div><h3>' + esc(p.title) + '</h3><p>' + esc(p.desc) + '</p><small>' + esc(p.stack) + '</small>' +
        (p.links.length ? '<div class="links">' + p.links.map((x) => '<a class="btn" href="' + x[1] + '" target="_blank" rel="noopener">' + I.ext + esc(x[0]) + '</a>').join('') + '</div>' : '') + '</div>').join('') + '</div></section>';
  }
  function cheats() {
    const tiers = byId('release-tiers').steps.slice(1, 5), risks = byId('watch-outs').steps.slice(1, 8), lic = byId('license-triage').steps.slice(1, 4);
    return '<section class="card page"><div class="crumb">Cheatsheets</div><h1>Numbers Worth Memorising</h1><p class="sub">The whole playbook on one page. Click a number to open its lesson.</p><div class="grid g4">' +
      KEY_NUMBERS.map((k) => '<a class="box" href="#/learn/' + k[2] + '/1"><span class="num">' + esc(k[0]) + '</span><small>' + esc(k[1]) + '</small></a>').join('') + '</div>' +
      '<div class="sec">RELEASE TIERS</div><div class="box"><table><tr><th>TIER</th><th>WEIGHTS</th><th>TRAINING DATA</th><th>CAPS</th><th>BEST FIT</th><th>EXAMPLES</th></tr>' +
      tiers.map((s) => '<tr><td><b>' + esc(s.title) + '</b></td>' + s.chips.map((c) => '<td>' + esc(c) + '</td>').join('') + '<td>' + esc(s.brief.l.join(' · ')) + '</td></tr>').join('') + '</table></div>' +
      '<div class="sec">LICENCE BUCKETS</div><div class="box"><table><tr><th>BUCKET</th><th>STATUS</th><th>WATCH FOR</th><th>EXAMPLES</th></tr>' +
      lic.map((s) => '<tr><td><b>' + esc(s.title) + '</b></td><td>' + esc(s.chips[1]) + '</td><td>' + esc(s.chips[2]) + '</td><td>' + esc(s.brief.l.join(' · ')) + '</td></tr>').join('') + '</table></div>' +
      '<div class="sec">SEVEN WATCH-OUTS</div><div class="box"><table><tr><th>#</th><th>RISK</th><th>MITIGATION</th></tr>' +
      risks.map((s, k) => '<tr><td>' + (k + 1) + '</td><td><b>' + esc(s.title) + '</b></td><td>' + esc(s.chips[1]) + '</td></tr>').join('') + '</table></div>' +
      '<div class="sec">PRIMARY SOURCES</div><div class="box"><ul class="src">' + SOURCES.map((s) => '<li>' + md(s) + '</li>').join('') + '</ul></div></section>';
  }

  // ------------------------------------------------------------ render
  function render() {
    const r = parse();
    document.querySelectorAll('.tab').forEach((t) => t.classList.toggle('on', t.dataset.tab === r.tab));
    const main = $('#main');
    main.className = 'main' + (r.tab === 'learn' ? '' : ' wide');
    const body = r.tab === 'learn' ? learn(r) : r.tab === 'tools' ? tools(r) : r.tab === 'labs' ? labs() : cheats();
    if (r.tab !== 'learn') prev = { lesson: null, step: 0 };
    main.innerHTML = sidebar(r) + body + '<div class="foot"><span>Unofficial practitioner guide by Kanchana Patlolla & Anusha Sabbineni. Not an official Google Cloud publication. Licensing notes are for planning, not legal advice.</span></div>';
    if (r.tab === 'tools') wireTools(r);
    if (r.tab === 'learn') {
      growBars(main);
      $('#replay').onclick = () => { prev = { lesson: null, step: 0 }; paused = false; render(); };
      const pb = $('#pause');
      if (pb) pb.onclick = () => { paused = !paused; render(); };
    }
    document.title = (r.tab === 'learn' ? r.lesson.title : r.tab[0].toUpperCase() + r.tab.slice(1)) + ' · Open Weights';
  }
  document.addEventListener('click', (e) => {
    const g = e.target.closest('[data-go]');
    if (g && !g.disabled) { go(g.dataset.go); return; }
    const c = e.target.closest('.ch');
    if (c) c.classList.toggle('open');
    if (!e.target.closest('.search')) $('#results').classList.remove('on');
  });
  document.addEventListener('keydown', (e) => {
    if (e.target.matches('input,select,textarea')) return;
    const r = parse();
    if (r.tab !== 'learn') return;
    if (e.key === 'ArrowRight' && r.step < r.lesson.steps.length) go('#/learn/' + r.lesson.id + '/' + (r.step + 1));
    if (e.key === 'ArrowLeft' && r.step > 1) go('#/learn/' + r.lesson.id + '/' + (r.step - 1));
  });

  // search
  const INDEX = [];
  LESSONS.forEach((l) => {
    INDEX.push({ t: l.title, s: chapterOf(l).name + ' · lesson', h: '#/learn/' + l.id + '/1', k: (l.title + ' ' + l.sub + ' ' + l.learn.join(' ')).toLowerCase() });
    l.steps.forEach((s, i) => INDEX.push({ t: s.title, s: l.title + ' · step ' + (i + 1), h: '#/learn/' + l.id + '/' + (i + 1), k: (s.title + ' ' + s.body.join(' ') + ' ' + s.key).toLowerCase() }));
  });
  LABS.forEach((p) => INDEX.push({ t: 'Part ' + p.n + ': ' + p.title, s: 'Labs', h: '#/labs', k: (p.title + ' ' + p.desc + ' ' + p.stack).toLowerCase() }));
  [['Break-Even Calculator', 'breakeven'], ['License Triage', 'license'], ['Workload Router', 'router']].forEach((t) => INDEX.push({ t: t[0], s: 'Tools', h: '#/tools/' + t[1], k: t[0].toLowerCase() + ' tool calculator' }));
  const q = $('#q'), res = $('#results');
  q.addEventListener('input', () => {
    const v = q.value.trim().toLowerCase();
    if (v.length < 2) { res.classList.remove('on'); return; }
    const hits = INDEX.filter((x) => x.k.includes(v)).slice(0, 8);
    res.innerHTML = hits.length ? hits.map((x) => '<a href="' + x.h + '">' + esc(x.t) + '<small>' + esc(x.s) + '</small></a>').join('') : '<a>No matches</a>';
    res.classList.add('on');
  });
  q.addEventListener('keydown', (e) => { if (e.key === 'Enter') { const a = res.querySelector('a[href]'); if (a) { go(a.getAttribute('href')); q.value = ''; res.classList.remove('on'); q.blur(); } } });
  res.addEventListener('click', () => { q.value = ''; res.classList.remove('on'); });

  // theme
  const setTheme = (t) => { document.documentElement.dataset.theme = t; saved.theme = t; store.set(saved); };
  if (saved.theme) document.documentElement.dataset.theme = saved.theme;
  $('#theme').onclick = () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');

  window.addEventListener('hashchange', () => { render(); window.scrollTo(0, 0); });
  render();
})();
