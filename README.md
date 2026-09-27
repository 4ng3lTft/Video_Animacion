# El equilibrio se va haciendo

> **Versión 2 en curso:** ver `estado.md` (prueba de 20 s «collage → plano técnico», pendiente de revisión) y `guion/animatic.md`. Lo de abajo describe la versión 1.

Animación vertical 2D (1080 × 1920, 30 fps) sobre la voz grabada de «narracion-corregida.srt».
Duración provisional de la pieza completa: 131.467 s (3944 fotogramas); se ajusta al conocer la duración real del audio.

**Estado: fase 2 (pieza completa) lista para revisión.** Audio integrado (`pieza/narracion.mp3`, 130.94 s). Los tiempos del SRT coinciden con la grabación (voz desde 0.79 s, última palabra hasta 129.52 s, medido por detección de silencios; no escuchado).

## Contenido

| Ruta | Qué es |
|---|---|
| `guion/narracion-frases.tsv` | Transcripción vigente agrupada por frases (tiempos fuente desde t=0 de la grabación). Fuente verbal única. |
| `design/project/` | Copia del lienzo de Claude Design: storyboard de nueve cuadros + tarjeta del piloto (`canvas.json` + `*.dc.html`). |
| `pieza/pieza.html` | Composición HyperFrames completa: 9 capítulos, 131.467 s (3944 fotogramas), subtítulos editables con tiempos fuente, `<audio>` desde t=0. |
| `exportes/el-equilibrio-se-va-haciendo.mp4` | Render local de la pieza (H.264 + AAC), para revisión. |
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

## Pieza completa: notas

- Cortes internos provisionales, estimados con los silencios del audio: 89.950, 100.400, 105.910, 116.300.
- 125.400–129.440 («El equilibrio se va haciendo / en la medida de lo posible.») aparece como título en la zona alta, no como subtítulo.
- Validación: `@hyperframes/lint` 0 errores (avisos de tamaño/estructura); 35 subtítulos comprobados automáticamente (≤ 2 renglones, dentro de 100–930 px, sin solapes).
- Para Send to HyperFrames, el `<audio>` necesita una URL pública absoluta del mp3 (la ruta relativa no viaja).

## Pendiente

1. Revisión humana de la pieza con audio (sincronía fina, mezcla, lectura en teléfono).
2. Fase 3: recorte de 20 s. Fase 4: preguntas de prueba.
3. Enviar a HyperFrames (paso manual fuera de este entorno).
