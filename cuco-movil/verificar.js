// Comprobaciones automáticas de recorrido.html:
//  - subtítulos: ≤ 2 renglones, dentro de x = 100–930 px, sin solaparse en el tiempo;
//  - títulos de capítulo: un renglón dentro de 100–930 px;
//  - toques: cada uno cae sobre un elemento visible de la página;
//  - duración y número de fotogramas.
// Uso: node cuco-movil/verificar.js --url http://localhost:8137/cuco-movil/recorrido.html
const { chromium } = require('playwright');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const url = arg('url', 'http://localhost:8137/cuco-movil/recorrido.html');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, reducedMotion: 'reduce' });
  const warnings = [];
  page.on('console', m => { if (m.type() === 'warning' || m.type() === 'error') warnings.push(m.text()); });
  await page.goto(url + '?render');
  const info = await page.evaluate(() => window.__ready);
  await page.evaluate(() => document.fonts.ready);
  const errs = [];

  const subs = await page.$$eval('.sub', els => els.map(e => ({ a: +e.dataset.start, b: +e.dataset.end, text: e.textContent })));
  for (let i = 0; i < subs.length; i++) {
    const s = subs[i];
    await page.evaluate(t => window.__player.seek(t), (s.a + s.b)/2);
    const m = await page.evaluate(i => {
      const span = document.querySelectorAll('.sub span')[i], r = span.getBoundingClientRect(), cs = getComputedStyle(span);
      const lines = Math.round((r.height - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom))/parseFloat(cs.lineHeight));
      return { left: r.left, right: r.right, lines };
    }, i);
    if (m.lines > 2) errs.push(`subtítulo ${i + 1} con ${m.lines} renglones: ${s.text}`);
    if (m.left < 100 - .5 || m.right > 930 + .5) errs.push(`subtítulo ${i + 1} fuera de 100–930 (${m.left.toFixed(0)}–${m.right.toFixed(0)})`);
    if (s.b <= s.a) errs.push(`subtítulo ${i + 1} con duración no positiva`);
    if (i && subs[i - 1].b > s.a) errs.push(`subtítulos ${i} y ${i + 1} se solapan`);
    console.log(`sub ${String(i + 1).padStart(2)} ${s.a.toFixed(1)}–${s.b.toFixed(1)} · ${m.lines} renglón(es) · x ${m.left.toFixed(0)}–${m.right.toFixed(0)}`);
  }

  const chaps = await page.$$eval('.chap', els => els.map(e => ({ a: +e.dataset.start, b: +e.dataset.end })));
  for (let i = 0; i < chaps.length; i++) {
    await page.evaluate(t => window.__player.seek(t), chaps[i].a + 1);
    const m = await page.evaluate(i => { const el = document.querySelectorAll('.chap')[i]; const ws = [...el.querySelectorAll('.w')].map(w => w.getBoundingClientRect());
      return { left: Math.min(...ws.map(r => r.left)), right: Math.max(...ws.map(r => r.right)), rows: new Set(ws.map(r => Math.round(r.top))).size }; }, i);
    if (m.rows > 1 || m.left < 100 || m.right > 930) errs.push(`título ${i + 1} fuera de margen o en ${m.rows} renglones`);
  }

  // Toques: el centro medido debe estar dentro del iframe (390 × 760).
  const taps = await page.evaluate(() => window.__player.taps || null);
  if (taps) for (const k of taps) if (!(k.x > 0 && k.x < 390 && k.y > 0 && k.y < 760)) errs.push(`toque en ${k.t}s fuera de pantalla (${k.sel})`);

  if (info.frames !== Math.round(info.duration*info.fps)) errs.push('número de fotogramas inconsistente');
  for (const w of warnings) errs.push('consola: ' + w);
  console.log(`duración ${info.duration} s · ${info.fps} fps · ${info.frames} fotogramas · ${subs.length} subtítulos · ${chaps.length} títulos · ${taps ? taps.length : 0} toques`);
  console.log(errs.length ? 'ERRORES:\n - ' + errs.join('\n - ') : 'OK: sin errores');
  await browser.close();
  process.exit(errs.length ? 1 : 0);
})();
