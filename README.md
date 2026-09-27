# El equilibrio se va haciendo

Animación vertical 2D (1080 × 1920, 30 fps) sobre la voz grabada de «narracion-corregida.srt».
Duración provisional de la pieza completa: 131.467 s (3944 fotogramas); se ajusta al conocer la duración real del audio.

**Estado: fase 1 (storyboard + piloto). Sincronización basada en transcripción; pendiente de comprobar con audio.**

## Contenido

| Ruta | Qué es |
|---|---|
| `guion/narracion-frases.tsv` | Transcripción vigente agrupada por frases (tiempos fuente desde t=0 de la grabación). Fuente verbal única. |
| `design/project/` | Copia del lienzo de Claude Design: storyboard de nueve cuadros + tarjeta del piloto (`canvas.json` + `*.dc.html`). |
| `piloto/piloto.html` | Composición HyperFrames autocontenida del piloto (18 s). SVG/CSS + línea temporal GSAP en pausa, registrada en `window.__timelines["main"]`. Fuente Literata (OFL) incrustada. |
| `piloto/vista-previa.html` | Reproductor para revisar el piloto (reproducir, barra, ±1 fotograma, zonas seguras, tiempo fuente). |

## Piloto

- Muestra A · El umbral: fuente 15.480–25.480 → piloto 0–10.
- Muestra B · La malla: fuente 86.780–94.780 → piloto 10–18.
- Los subtítulos guardan sus tiempos **fuente** en `data-src-start` / `data-src-end`; el script los traslada a tiempo de piloto. Solo existe un desfase por muestra; el 0.820 de la primera palabra no se vuelve a sumar.
- Corte provisional: la frase 86.780–91.280 no cabe en dos renglones y se reparte en dos subtítulos con corte en 89.660 (estimado por proporción de caracteres, sin audio).
- Audio: las etiquetas `<audio>` están comentadas en `piloto.html` con `data-media-start` 15.48 y 86.78. Descomentar al tener la grabación (archivo junto al HTML o URL pública absoluta).

## Comprobaciones hechas

- `@hyperframes/lint` 0.8.79: 0 errores, 2 avisos (`nested_structure_needs_subcomposition`: la estructura de escenas con `.scene-content` es la que pide la guía de Send to HyperFrames).
- Render en Chromium headless con el runtime de HyperFrames 0.8.79 y GSAP 3.14.2 locales: duración 18 s, navegación con `window.__player.seek`, fotogramas revisados en 0.6, 4, 8.5, 12.5, 16, 17.6 s.
- No comprobado: audio, mezcla, Send to HyperFrames, exportación MP4.

## Pendiente

1. Audio original → verificar tiempos, cortes provisionales y duración total.
2. Fase 2 (al decir «continúa»): pieza completa de 131.467 s reutilizando estos componentes.
3. Enviar a HyperFrames y exportar MP4 (paso manual fuera de este entorno).
