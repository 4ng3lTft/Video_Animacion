# Estado del proyecto · versión 2 («El deseo cambia de piel»)

Para continuar en otro chat: lee este archivo, `guion/animatic.md` y `prueba/prueba.fuente.html`.

## Fase actual: prueba de 20 s entregada, **pendiente de revisión**

| Archivo | Qué es |
|---|---|
| `guion/animatic.md` | Lectura de la idea + animatic completo por tomas (tiempos fuente). |
| `prueba/prueba.fuente.html` | **Plantilla editable** de la prueba (HTML + GSAP). Aquí se edita. |
| `prueba/prueba.html` | Composición HyperFrames autocontenida generada (fuentes y texturas incrustadas). No editar a mano. |
| `prueba/narracion.mp3` | Enlace simbólico a `../pieza/narracion.mp3` (el lint no admite rutas con `../`). |
| `exportes/prueba-20s-collage-a-plano.mp4` | Render de la prueba con la voz 38.76–58.80 (H.264 CRF 26 + AAC). |
| `herramientas/` | `construir.py` (ensambla), `geometria.py` (personaje, objetos, papel rasgado), `render.cjs` + `cuadros.sh` (render por fotograma), `tiras.py` (hojas de fotogramas consecutivos), `verificar.cjs` (lint, subtítulos, duración, determinismo), `fuentes/` (Literata y Architects Daughter, OFL). |

Versión anterior (referencia técnica, no de estilo): `pieza/pieza.html`, `exportes/el-equilibrio-se-va-haciendo.mp4`.

## Qué cubre la prueba (fuente 38.76–58.80 = 20.04 s, 601 fotogramas)
Final del collage a 12 fps (salto de la luz, corte por coincidencia pantalla → ventana, vueltas cada vez más rápidas,
congelado) → la luz quema y rasga el papel → plano técnico con impulso, anticipación, negación (puño con fugas de luz)
y satisfacción (mesa compartida, la mano de otra persona).

**Decisión a revisar:** en la voz, «negación» (la frase de 61.5 s) queda fuera de la ventana de 20 s. La puse en «podemos
alimentar» (53.78–54.88): escoger qué no alimentar = intentar apretarlo. En la pieza completa 61.5 s retoma el tema sin
apretar (acercar lo que falta, en vez de esconderlo).

## Comprobado (con herramientas, no a ojo)
- `@hyperframes/lint` 0.8.79: 0 errores; 2 avisos de tamaño/estructura (una sola toma continua, a propósito).
- Subtítulos (5): todos ≤ 2 renglones, dentro de 141–890 px (margen 100–930), sin solaparse.
- Línea de tiempo en pausa, duración 20.040 s = `data-duration`.
- Determinismo: el mismo instante alcanzado desde 0 o desde el final da el mismo píxel (0 px distintos).
- Movimiento: tiras de 24 fotogramas consecutivos en 38.76, 39.76, 41.56, 41.96, 44.09 (desgarro), 44.76, 49.76 (impulso),
  53.93 (puño) y 57.43 (satisfacción). Se corrigieron: luz que se quedaba atrás al abrazar la casa, moto invisible en el
  fotograma 0, objetos desplazados por `svgOrigin` repetido, `fromTo` que imponían su «from» al buscar hacia atrás.
- Sincronía: acciones puestas sobre silencios medidos (39.15–39.97, 41.87–44.04, 46.27–47.00, 49.18–49.49, 50.40–50.99,
  51.94–52.36, 54.88–56.14, 57.84–58.67).

## No comprobado
- **La mezcla y el ritmo con audio real**: no puedo oír. La voz está en el MP4 sin cambios; no hay música ni efectos.
- Reproducción en el equipo del usuario (i7-1165G7): el render es por fotograma, no en tiempo real.
- Send to HyperFrames: el `<audio>` necesita una URL pública absoluta del mp3.

## Aprendizajes técnicos (evitan repetir errores)
- No repetir `svgOrigin` en cada tween: se calcula con la matriz actual y desplaza el elemento. Fijarlo una vez al inicio.
  El origen por defecto en SVG ya es el (0,0) local.
- `tl.set` de duración cero y `fromTo` con `immediateRender` no se revierten bien al buscar: usar tweens de 1 ms
  (`fija`) y `defaults: { immediateRender: false }` en la línea de tiempo.
- Tweens encimados sobre la misma propiedad hacen que el resultado dependa del camino: evitarlos.
- Render: `NODE_PATH=<node_modules con gsap 3.14.2, @hyperframes/core, @hyperframes/lint, playwright> herramientas/cuadros.sh prueba/prueba.html <carpeta> 601`
  (4 procesos, ~2.5 min) y luego ffmpeg con el mp3 (`-ss 38.76 -t 20.04`).
- GSAP 3.14.2: MotionPath y DrawSVG están en el paquete npm con licencia «Standard no charge» (README del paquete:
  gratuito incluso para uso comercial). Condiciones: https://gsap.com/standard-license

## Pendiente
1. **Revisión de la prueba por el usuario** (ritmo, legibilidad, si el cambio de piel distrae de la voz).
2. Si se aprueba: pieles 1, 4 y 5 y el cierre, reutilizando rig, cámara, luz, `paso()` (12 fps) y el desgarro.
   Para el lápiz: 2–3 variantes de trazo alternadas a 10 fps.
3. Si no alcanza el nivel: proponer otra herramienta (After Effects/Rive) con guion técnico toma por toma.
4. Base sonora opcional por piel (no evaluada).
