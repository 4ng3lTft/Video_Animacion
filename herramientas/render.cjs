// Render determinista de una composición HyperFrames: seek por fotograma + captura + ffmpeg.
//
// Uso:
//   NODE_PATH=<carpeta con node_modules de gsap, @hyperframes/core y playwright> \
//   node herramientas/render.cjs <composicion.html> <salida.mp4> [--audio narracion.mp3 --audio-desde 38.76]
//   node herramientas/render.cjs <composicion.html> <carpeta> --cuadros 330-341   (PNG sueltos para tiras)
//
// jsdelivr está bloqueado en este contenedor: las URL del CDN se sirven desde node_modules locales
// (gsap 3.14.2 y @hyperframes/core), que son las mismas versiones que la composición pide.
const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");
const { chromium } = require("playwright");

const args = process.argv.slice(2);
const html = path.resolve(args[0]);
const salida = path.resolve(args[1]);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const FPS = Number(opt("--fps", 30));
const cuadros = opt("--cuadros", null);
const audio = opt("--audio", null);
const audioDesde = Number(opt("--audio-desde", 0));
const ffmpeg = opt("--ffmpeg", process.env.FFMPEG || "ffmpeg");

function local(mod) {
  for (const p of (process.env.NODE_PATH || "").split(path.delimiter)) {
    const f = path.join(p, mod);
    if (p && fs.existsSync(f)) return f;
  }
  return require.resolve(mod);
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("[pageerror]", e.message));
  page.on("console", (m) => { if (m.type() === "error") console.error("[console]", m.text()); });
  await page.route(/cdn\.jsdelivr\.net\/npm\/gsap@3\.14\.2\/dist\/(.+)$/, (route) => {
    const f = route.request().url().match(/dist\/(.+)$/)[1];
    route.fulfill({ path: local("gsap/dist/" + f), contentType: "application/javascript" });
  });
  await page.route(/cdn\.jsdelivr\.net\/npm\/@hyperframes\/core\/dist\/(.+)$/, (route) => {
    const f = route.request().url().match(/dist\/(.+)$/)[1];
    route.fulfill({ path: local("@hyperframes/core/dist/" + f), contentType: "application/javascript" });
  });
  await page.goto("file://" + html);
  for (let i = 0; i < 300; i++) {
    const ok = await page.evaluate(() => window.__playerReady === true && !!(window.__timelines && window.__timelines.main));
    if (ok) break;
    if (i === 299) throw new Error("la composición no quedó lista (__playerReady)");
    await page.waitForTimeout(100);
  }
  await page.evaluate(() => document.fonts.ready);
  const dur = await page.evaluate(() => Number(document.querySelector("[data-composition-id=main]").getAttribute("data-duration")));
  const total = Math.round(dur * FPS);
  let desde = 0, hasta = total - 1;
  if (cuadros) { [desde, hasta] = cuadros.split("-").map(Number); fs.mkdirSync(salida, { recursive: true }); }
  console.error(`duración ${dur} s → ${total} fotogramas; render ${desde}–${hasta}`);

  let ff = null;
  if (!cuadros) {
    const a = ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-i", "-"];
    if (audio) a.push("-ss", String(audioDesde), "-t", String(dur), "-i", path.resolve(audio));
    a.push("-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", String(FPS));
    if (audio) a.push("-c:a", "aac", "-b:a", "192k", "-af", "apad", "-t", String(dur));
    a.push("-movflags", "+faststart", salida);
    ff = spawn(ffmpeg, a, { stdio: ["pipe", "inherit", "inherit"] });
  }
  const t0 = Date.now();
  for (let f = desde; f <= hasta; f++) {
    await page.evaluate((t) => window.__player.seek(t), f / FPS);
    const png = await page.screenshot({ type: "png" });
    if (ff) { if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once("drain", r)); }
    else fs.writeFileSync(path.join(salida, `f${String(f).padStart(4, "0")}.png`), png);
    if (f % 60 === 0) console.error(`  ${f}/${hasta}  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  }
  if (ff) { ff.stdin.end(); await new Promise((r) => ff.on("close", r)); }
  await browser.close();
  console.error("listo:", salida);
})().catch((e) => { console.error(e); process.exit(1); });
