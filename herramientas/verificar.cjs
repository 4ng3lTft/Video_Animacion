// Comprobaciones automáticas de una composición:
//  1. @hyperframes/lint (errores y avisos)
//  2. subtítulos: ≤ 2 renglones, dentro de 100–930 px, sin solaparse en el tiempo
//  3. duración de la línea de tiempo = data-duration; línea de tiempo en pausa
//  4. determinismo: el mismo instante, alcanzado por dos caminos distintos, da el mismo píxel
// Uso: NODE_PATH=... node herramientas/verificar.cjs <composicion.html>
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const html = path.resolve(process.argv[2]);
const local = (m) => {
  for (const p of (process.env.NODE_PATH || "").split(path.delimiter)) if (p && fs.existsSync(path.join(p, m))) return path.join(p, m);
  return require.resolve(m);
};

(async () => {
  let fallos = 0;
  // 1 · lint
  const { lintHyperframeHtml } = await import("file://" + local("@hyperframes/lint/dist/index.js"));
  const r = await lintHyperframeHtml(fs.readFileSync(html, "utf8"), { filePath: html });
  console.log(`lint: ${r.errorCount} errores, ${r.warningCount} avisos, ${r.infoCount} info`);
  for (const f of r.findings) console.log(`  [${f.severity}] ${f.code}: ${f.message.slice(0, 160)}`);
  fallos += r.errorCount;

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on("pageerror", (e) => { console.log("[pageerror]", e.message); fallos++; });
  await page.route(/cdn\.jsdelivr\.net\/npm\/gsap@3\.14\.2\/dist\/(.+)$/, (rt) =>
    rt.fulfill({ path: local("gsap/dist/" + rt.request().url().match(/dist\/(.+)$/)[1]), contentType: "application/javascript" }));
  await page.route(/cdn\.jsdelivr\.net\/npm\/@hyperframes\/core\/dist\/(.+)$/, (rt) =>
    rt.fulfill({ path: local("@hyperframes/core/dist/" + rt.request().url().match(/dist\/(.+)$/)[1]), contentType: "application/javascript" }));
  await page.goto("file://" + html);
  for (let i = 0; i < 300 && !(await page.evaluate(() => window.__playerReady === true)); i++) await page.waitForTimeout(100);
  await page.evaluate(() => document.fonts.ready);

  // 2 · subtítulos (se miden con la fuente real, uno por uno)
  const subs = await page.evaluate(() => {
    const out = [];
    for (const c of document.querySelectorAll("#subtitulos .cue")) {
      const ini = +c.dataset.srcStart, fin = +c.dataset.srcEnd;
      const lh = parseFloat(getComputedStyle(c).lineHeight);
      const rg = document.createRange(); rg.selectNodeContents(c);
      const rects = [...rg.getClientRects()];
      const L = Math.min(...rects.map((x) => x.left)), R = Math.max(...rects.map((x) => x.right));
      out.push({ texto: c.textContent, ini, fin, renglones: Math.round(c.getBoundingClientRect().height / lh), L: Math.round(L), R: Math.round(R) });
    }
    return out;
  });
  let prev = null;
  for (const s of subs) {
    const ok = s.renglones <= 2 && s.L >= 100 && s.R <= 930 && (!prev || s.ini >= prev.fin);
    if (!ok) fallos++;
    console.log(`${ok ? "ok " : "MAL"} ${s.ini.toFixed(2)}–${s.fin.toFixed(2)}  ${s.renglones} renglón(es)  x ${s.L}–${s.R}  «${s.texto}»`);
    prev = s;
  }

  // 3 · duración y pausa
  const d = await page.evaluate(() => {
    const tl = window.__timelines.main;
    return { tl: tl.duration(), attr: +document.querySelector("[data-composition-id=main]").dataset.duration, pausada: tl.paused() };
  });
  const okD = Math.abs(d.tl - d.attr) < 0.002 && d.pausada;
  if (!okD) fallos++;
  console.log(`${okD ? "ok " : "MAL"} duración línea de tiempo ${d.tl.toFixed(3)} s · data-duration ${d.attr} s · en pausa: ${d.pausada}`);

  // 4 · determinismo: t alcanzado hacia delante y hacia atrás. Se comparan píxeles decodificados
  //     (MotionPath deja ruido de 1e-5 px en coordenadas que no cambia la imagen de forma visible).
  const cmp = await browser.newPage();
  const diff = (a, b) => cmp.evaluate(async ([a, b]) => {
    const load = (s) => new Promise((r) => { const i = new Image(); i.onload = () => r(i); i.src = "data:image/png;base64," + s; });
    const [A, B] = await Promise.all([load(a), load(b)]);
    const c = document.createElement("canvas"); c.width = A.width; c.height = A.height; const x = c.getContext("2d");
    x.drawImage(A, 0, 0); const da = x.getImageData(0, 0, c.width, c.height).data;
    x.clearRect(0, 0, c.width, c.height); x.drawImage(B, 0, 0); const db = x.getImageData(0, 0, c.width, c.height).data;
    let n = 0, m = 0; for (let i = 0; i < da.length; i += 4) { const d = Math.max(Math.abs(da[i] - db[i]), Math.abs(da[i + 1] - db[i + 1]), Math.abs(da[i + 2] - db[i + 2])); if (d > 8) n++; if (d > m) m = d; }
    return { n, m };
  }, [a, b]);
  const shot = async () => (await page.screenshot({ type: "png" })).toString("base64");
  for (const t of [2.5, 5.4, 10.9, 15.5]) {
    await page.evaluate((x) => window.__player.seek(x), 0); await page.evaluate((x) => window.__player.seek(x), t);
    const a = await shot();
    await page.evaluate((x) => window.__player.seek(x), d.attr - 0.05); await page.evaluate((x) => window.__player.seek(x), t);
    const b = await shot();
    const r = await diff(a, b);
    const ok = r.n < 50;
    if (!ok) fallos++;
    console.log(`${ok ? "ok " : "MAL"} determinismo en t=${t}: ${r.n} px distintos (>8/255), diferencia máx ${r.m}`);
  }
  await browser.close();
  console.log(fallos ? `\n${fallos} fallo(s)` : "\ntodo en orden");
  process.exit(fallos ? 1 : 0);
})();
