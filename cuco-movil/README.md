# CUCO · recorrido de la versión móvil (vertical, 90 s)

Video vertical 1080 × 1920, 30 fps, 90.000 s (2700 fotogramas), sin audio, que recorre la versión móvil
de **CUCO · Cuenta Conmigo** (repo `4ng3lTft/CUCO`, `index.html` del commit `b48334c`, copiado en `sitio/index.html`).

Render: `exportes/cuco-recorrido-movil-90s.mp4` (H.264, CRF 18, yuv420p, faststart).

## Cómo está hecho

- La **página real** se carga en un iframe de 390 × 760 px CSS (ancho de un teléfono), así que aplica su propio
  diseño responsivo (`@media (max-width:650px)`). No es una imitación: son sus estilos, textos y estados.
- El iframe vive dentro de un teléfono que **nace del logo de CUCO** (el cuadro redondeado con la «C» se
  transforma en el teléfono) y al final **vuelve a ser el logo**. No hay fundidos a negro.
- El estado visible es **una función pura del tiempo**: `stateAt(t)` aplica en orden los eventos con `t_e ≤ t`
  (lista `EVENTS`), y las pistas continuas (scroll, cámara, diálogos) se interpolan con easing.
  Costo por fotograma: O(E + K) con E eventos y K keyframes (ambos < 30), así que el render completo es
  O(F·(E + K)) con F = 2700. Al ser puro, cualquier `seek(t)` da el mismo fotograma aunque se busque en desorden.
- `applyState` solo toca el DOM cuando un campo del estado cambia (comparación con el estado anterior), para no
  recalcular el diseño de la página en cada fotograma.
- Las transiciones propias de la página se apagan (`prefers-reduced-motion` + estilo inyectado) y el
  movimiento lo controla la línea de tiempo: diálogos que suben, cambio de pantalla con desplazamiento, rebote
  de los contadores del panel.

## Animatic (tomas)

| Tiempo | Toma |
|---|---|
| 0.0–3.0 | El logo de CUCO aparece con rebote; la «C» se dibuja y el punto salta. «cuco» sube letra por letra. Quietud breve. |
| 3.0–4.5 | Anticipación: el logo se encoge un poco y luego **crece hasta volverse el teléfono**; la pantalla de inicio aparece desde dentro. «cuco» se retira hacia abajo para no cruzar el logo; arriba entra la marca. |
| 4.6–11.9 | **Inicio.** La cámara se acerca a «¿Cómo estás, de verdad?», sostiene (lectura) y se abre. |
| 12.0–19.8 | **Hoy me siento…** Scroll a la tarjeta de ánimo, la cámara empuja, el dedo toca «Regular» y cambia el mensaje. |
| 20.0–24.6 | **Menú.** Toque en ☰, se abre la navegación, toque en «Cómo funciona» y la página viaja a la sección. |
| 24.8–34.4 | **Cómo funciona.** Lectura lenta de los tres pasos con un leve acercamiento; regreso al paso 01. |
| 34.6–48.3 | **Autoevaluación.** Toque en «Conocer la autoevaluación»: el diálogo sube. Privacidad → pregunta de ejemplo («Con altibajos») → orientación. |
| 48.4–56.5 | **Solicitud de apoyo.** El ticket DEMO-001 con datos ficticios. |
| 56.6–67.8 | **Vista de psicología.** Panel; la tabla se desliza; «Marcar como atendida» y la cámara se acerca a los contadores (2 → 1, 1 → 2, con rebote); filtro «Atendidas»; se cierra. |
| 67.9–76.8 | **Apoyo inmediato.** Toque en «Ayuda inmediata»; la cámara recorre Línea de la Vida (800 911 2000) y 911. |
| 77.0–84.6 | **Tus dudas.** Se abre «¿Se guardan mis respuestas?» y se baja al pie (ODS 3). |
| 84.6–90.0 | El teléfono **vuelve a ser el logo**; «cuco», «Un primer paso, a tu manera.» y créditos. Quietud final. |

Subtítulos y títulos están en capas HTML editables (`.sub` y `.chap` con `data-start` / `data-end`).

## Criterios del prompt maestro que se aplicaron

- Vertical 1080 × 1920, 30 fps; toma continua con transformación (logo ↔ teléfono), sin cortes a negro.
- Cámara con intención (acercamientos solo en lo importante y quietud para leer), dedo con anticipación,
  presión y onda; títulos que entran por máscara con rebote; atmósfera con brillo que deriva, órbita y grano.
- Subtítulos ≤ 2 renglones dentro de x = 100–930 px, sin solapes; títulos arriba.
- Revisión con tiras de 12 fotogramas consecutivos en los momentos clave (logo → teléfono, toque, apertura y
  cierre de diálogos), no solo capturas sueltas.

## Comprobado / no comprobado

- `verificar.js`: 19 subtítulos (≤ 2 renglones, dentro de 100–930 px, sin solapes), 9 títulos en un renglón,
  14 toques con objetivo dentro de la pantalla, 2700 fotogramas, sin avisos en consola.
- Tiras de fotogramas revisadas en 2.9, 3.4, 4.1, 14.6, 34.5, 67.7 s; capturas sueltas en 13 tiempos.
- No comprobado: reproducción en un teléfono real ni cómo lo recorta cada red social (zonas de interfaz).
- Sin audio: CUCO no tiene narración grabada. Si se agrega voz o música, hay que ajustar los tiempos a ese audio.
- Las fuentes del render son las del contenedor (Georgia y Segoe UI no están; se usan sustitutos con la misma
  pila de la página). En Windows la vista previa se verá con Georgia/Segoe UI.

## Reproducir

```bash
cd Video_Animacion
python3 -m http.server 8137          # el iframe necesita el mismo origen (no abrir con file://)
# vista previa: http://localhost:8137/cuco-movil/recorrido.html (▶︎ y barra de tiempo)
NODE_PATH=$(npm root -g) node cuco-movil/verificar.js
NODE_PATH=$(npm root -g) node cuco-movil/render.js --out exportes/cuco-recorrido-movil-90s.mp4
```

Requiere Playwright (Chromium) y ffmpeg con libx264.
