# Prompt maestro · «El equilibrio se va haciendo» (versión 2)

Copia todo lo que está debajo de la línea en un chat nuevo. Antes, llena la sección REFERENCIA VISUAL.

---

Actúa como director de animación y motion designer senior. Vamos a rehacer desde cero la animación de «El equilibrio se va haciendo». Ya existe un intento anterior que NO funcionó; aquí tienes lo aprendido para no repetirlo.

## Material disponible (repositorio 4ng3lTft/Video_Animacion, rama `claude/epic-heisenberg-lknc9k`)
- `pieza/narracion.mp3`: mi voz grabada, 130.94 s, mono. Es la única voz; no la generes, no la cortes, no la aceleres.
- `guion/narracion-frases.tsv`: transcripción vigente por frases, tiempos en segundos desde t=0 del audio. Coincide con el audio (voz desde 0.79 s, última palabra hasta 129.52 s). Transcripción íntegra al final de este prompt.
- `pieza/pieza.html`: versión anterior (HyperFrames + GSAP + SVG). Úsala solo como referencia técnica (contrato HyperFrames, subtítulos, fuente incrustada). No reutilices su estilo visual.
- Herramientas que ya funcionaron en el entorno: GSAP 3.14.2 y `@hyperframes/core` vía npm (jsdelivr está bloqueado en el contenedor), `@hyperframes/lint`, Playwright con Chromium en /opt/pw-browsers, ffmpeg con libx264 vía `pip install imageio-ffmpeg`. Render: `window.__player.seek(t)` por fotograma + captura + ffmpeg con el mp3.

## La idea (lo que alguien debe entender al terminar)
No hay vergüenza en desear. Lo importante son las iteraciones: reconocer la naturaleza misma del deseo (impulso, anticipación, satisfacción y también la negación, que al apretarlo lo intensifica) y reconocer nuestro lugar en la malla. El DESEO es el protagonista; la malla (comunidad) es el actor que le da sentido al deseo una vez analizado y diseccionado. El equilibrio no se alcanza: se va haciendo, en la medida de lo posible, con condiciones materiales reales y sin garantías.
- Es mi reflexión en español cercano de México, no una ley psicológica.
- El deseo no es villano ni el disfrute un engaño. Los vínculos son entre personas con autonomía.
- Ejemplos concretos de deseo, fáciles de reconocer: una casa, una moto, un teléfono, placeres (una comida compartida es un deseo que no es malo y el primero que incluye a otras personas).

## Por qué falló el intento anterior (no repetir)
1. Ilustraba frase por frase: la imagen repetía la voz en lugar de aportar.
2. Nueve escenas separadas con fundidos a negro: sin continuidad, sin arco.
3. Símbolos abstractos (hilos, nudos, cajas, siluetas genéricas) que obligaban a descifrar la metáfora.
4. Movimiento pobre: casi todo era aparecer / dibujar línea / desvanecer. Sin cámara, sin transformaciones, sin anticipación, sin rebote, sin movimiento secundario.
5. Se revisó con capturas fijas, así que el ritmo y la fluidez no se evaluaron.

## Dirección nueva
- Una sola toma continua o casi continua: la cámara viaja, las formas se transforman unas en otras (morph), no hay cortes a negro.
- Menos símbolos, más acción. La voz explica; la imagen muestra una transformación que suma.
- Personaje más expresivo aunque sea simple (postura, gesto, peso). El deseo debe verse como algo vivo y cálido, con pulso, de principio a fin.
- Principios de animación: anticipación, seguimiento/solapamiento, easing con intención, arcos, secundarios. Momentos de quietud deliberados.
- Tipografía cinética solo si ayuda; subtítulos completos en capa editable (máx. 2 renglones, margen seguro 100–930 px, abajo), títulos ocasionales arriba.
- Vertical 1080×1920, 30 fps, duración 131.467 s (termina ~2 s después de la última palabra).
- Paleta base (ajustable si la referencia lo pide): ciruela #241C27, ámbar #E3A04D, blanco cálido #F0E8DF, verde apagado #8CAA9C.
- Equipo del usuario para previsualizar: Windows 11, i7-1165G7, 12 GB RAM. Evitar 3D y físicas pesadas.

## REFERENCIA VISUAL (llena esto antes de pegar)
Enlace: https://x.com/VoidStateKate/status/2104041451084517742 (Claude no puede abrir X; describe lo que ves)
- Estilo (ilustración con personajes / formas abstractas que se transforman / tipografía / mezcla): …
- Ritmo (rápido con cortes / fluido y continuo): …
- Lo que más me gusta (colores, texturas, cámara, transiciones, sonido): …
- Qué NO quiero de esa referencia: …

## Proceso (cuidando tokens)
1. En máximo 150 palabras: tu lectura de la idea y la propuesta visual. Luego un animatic de texto por tomas con tiempos fuente.
2. Construye SOLO una prueba de 15 s: el momento de «reconocer el mecanismo» (fuente ~44.24–59.00, incluye impulso, anticipación, satisfacción y negación). Renderízala a MP4 con el audio de ese tramo y revisa el movimiento con tiras de fotogramas consecutivos (no solo capturas sueltas). Entrégala y DETENTE.
3. Si apruebo, construye la pieza completa reutilizando lo aprobado. Si no, propón cambiar de herramienta (After Effects, Rive u otra) y entrega un guion técnico toma por toma en lugar de seguir intentando.
4. Reporta breve: qué construiste, qué comprobaste, qué falta. Consumo de tokens: «no disponible» si la interfaz no lo expone. No inventes funciones ni resultados; si no sabes algo, dilo y remite a la documentación oficial.

## Transcripción vigente (inicio–fin en segundos | texto literal; no cambiar palabras)
0.820-2.600 | Como humanos tendemos a desear
3.800-6.840 | y ese deseo es como si fuera un combustible.
8.240-10.960 | Nos mueve, nos ayuda a imaginar,
11.320-13.700 | a buscar, a querer llegar a algo.
15.480-17.240 | Pensemos en un paquete,
18.860-20.300 | ya lo tenemos en nuestras manos,
21.620-24.320 | justo antes de abrirlo. Ese momento.
26.260-30.180 | Ahí, todavía cabe todo lo que esperas,
30.480-32.619 | todo lo que pienses que vas a obtener de él.
34.280-37.760 | Pero una vez que lo tienes, al consumarlo,
38.760-41.820 | a veces el deseo ya está buscando otro huésped.
44.240-46.270 | Podríamos argumentar que este equilibrio
47.020-50.300 | se va a obtener una vez que reconocemos los impulsos
51.020-54.820 | y escogemos qué deseos o ilusiones podemos alimentar.
56.220-57.840 | Dándole tiempo a la satisfacción,
58.820-60.710 | pudiendo disfrutar lo que sí nos sostiene,
61.500-63.760 | sin resignarnos a lo que nos lastima o nos falta.
64.819-66.140 | Porque tenemos que ser honestos,
66.880-70.740 | hay condiciones materiales, sí, limitantes,
71.560-74.040 | no todo lo podemos resolver desde lo individual.
75.240-77.400 | Por eso necesitamos formar comunidades,
78.200-79.990 | una malla entretejida que nos sostenga
80.300-83.680 | y que también podamos sostener, según nuestras posibilidades.
85.060-85.820 | Algo simbiótico,
86.780-91.280 | cuidarnos, permite cuidar y ser cuidados nos ayuda a estar bien,
92.140-94.620 | aunque también hay que escuchar a quien está cargando de más.
96.040-96.640 | No hay garantías,
97.780-102.280 | podemos comenzar en casa, en clase, en el espacio que permite el trabajo,
103.740-108.340 | reconocer el bienestar de nuestros vínculos, pero también poder cuestionarlos,
109.660-113.400 | Intentar, sentir, debatir y corregir juntos,
114.560-119.100 | no viéndolo como vergüenza, sino como una parte fundamental del proceso
120.240-124.020 | y que esa corrección cambie algo en cómo nos cuidamos.
125.400-126.930 | El equilibrio se va haciendo
127.660-129.440 | en la medida de lo posible.
