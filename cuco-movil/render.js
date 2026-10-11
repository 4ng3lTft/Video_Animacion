// Render determinista de recorrido.html: seek(t) por fotograma, captura PNG y ffmpeg (H.264).
// Uso (con la carpeta del repo servida por http, p. ej. `python3 -m http.server 8137`):
//   node cuco-movil/render.js --url http://localhost:8137/cuco-movil/recorrido.html --out exportes/cuco-recorrido-movil-90s.mp4
//   node cuco-movil/render.js --url ... --stills 0.5,6.6,15.2 --dir carpeta/   (capturas sueltas)
//   node cuco-movil/render.js --url ... --strip 15.0 --n 12 --dir carpeta/     (12 fotogramas seguidos desde t)
// Necesita Playwright (Chromium) y ffmpeg en el PATH.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const url = arg('url', 'http://localhost:8137/cuco-movil/recorrido.html');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
  page.on('console', m => { if (m.type() === 'warning' || m.type() === 'error') console.log('[página]', m.text()); });
  await page.goto(url + (url.includes('?') ? '&' : '?') + 'render');
  const info = await page.evaluate(() => window.__ready);
  await page.evaluate(() => document.fonts.ready);
  const shot = async t => { await page.evaluate(t => window.__player.seek(t), t); return page.screenshot({ type: 'png' }); };

  const dir = arg('dir');
  if (arg('stills') || arg('strip')) {
    fs.mkdirSync(dir, { recursive: true });
    let times = arg('stills') ? arg('stills').split(',').map(Number) : [];
    if (arg('strip')) { const f0 = Math.round(+arg('strip')*info.fps); times = Array.from({ length: +arg('n', 12) }, (_, i) => (f0 + i)/info.fps); }
    for (const t of times) fs.writeFileSync(path.join(dir, `t${t.toFixed(3).padStart(7, '0')}.png`), await shot(t));
    await browser.close();
    return;
  }

  const out = arg('out', 'exportes/cuco-recorrido-movil-90s.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(info.fps), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(info.fps), '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = 0; f < info.frames; f++) {
    const buf = await shot(f/info.fps);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`fotograma ${f}/${info.frames} · ${((Date.now() - t0)/1000).toFixed(0)} s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('listo:', out);
})();
