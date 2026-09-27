# Prompt maestro · «El equilibrio se va haciendo» (versión 2)

Copia todo lo que está debajo de la línea en un chat nuevo. Antes, llena `<referencia_visual>`.
Estructura basada en la guía oficial de prompting de Anthropic
(https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices):
datos largos arriba, secciones en etiquetas XML, el porqué de cada regla, ejemplos y criterios de revisión concretos.

---

<transcripcion>
Formato: inicio–fin en segundos desde t=0 del audio | texto literal. No cambies palabras.
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
</transcripcion>

<contexto>
Soy estudiante de 4.º semestre de Ingeniería en Sistemas. Grabé una reflexión personal (español cercano de México) y quiero convertirla en una animación vertical para redes. Ya hubo un intento que no funcionó; esta es la segunda versión y quiero calidad de motion design, como las animaciones dinámicas que se ven en X.

Todo el material está en el repositorio 4ng3lTft/Video_Animacion, rama `claude/epic-heisenberg-lknc9k`. Lee el estado desde esos archivos al empezar; no necesitas la conversación anterior.
- `pieza/narracion.mp3`: mi voz, 130.94 s, mono. Es la única voz: no se genera, no se corta, no se acelera. La transcripción de arriba coincide con este audio (voz desde 0.79 s, última palabra hasta 129.52 s).
- `pieza/pieza.html`: el intento anterior (HyperFrames + GSAP + SVG). Sirve como referencia técnica (contrato HyperFrames, subtítulos editables, fuente incrustada), no de estilo.
- Herramientas que ya funcionaron en este contenedor: GSAP 3.14.2 y `@hyperframes/core` vía npm (jsdelivr está bloqueado), `@hyperframes/lint`, Playwright con Chromium en /opt/pw-browsers, ffmpeg con libx264 vía `pip install imageio-ffmpeg`. Render: `window.__player.seek(t)` por fotograma, captura y ffmpeg con el mp3.
- Guía de HyperFrames: https://github.com/heygen-com/hyperframes/blob/main/docs/guides/claude-design-send-to-hyperframes.md
</contexto>

<idea>
Lo que alguien debe entender al terminar: no hay vergüenza en desear. Lo importante son las iteraciones: reconocer la naturaleza misma del deseo (impulso, anticipación, satisfacción, y también la negación, que al apretar el deseo lo intensifica) y reconocer nuestro lugar en la malla.
- El DESEO es el protagonista de principio a fin. La malla (comunidad) es el actor que le da sentido al deseo una vez analizado y diseccionado.
- El equilibrio no se alcanza: se va haciendo, en la medida de lo posible, con condiciones materiales reales y sin garantías.
- Ejemplos de deseo fáciles de reconocer: una casa, una moto, un teléfono, placeres. La comida compartida es un deseo que no es malo y el primero que incluye a otras personas: sirve de puente hacia la malla.
- Es mi reflexión, no una ley psicológica. El deseo no es villano ni el disfrute un engaño. Los vínculos son entre personas con autonomía, no objetos.
</idea>

<lecciones_del_intento_anterior>
Estas fallas hicieron que la idea no se transmitiera; evítalas porque son la razón de rehacer todo:
1. Se ilustró frase por frase. La imagen repetía la voz en vez de sumarle algo, y el video parecía una presentación.
2. Nueve escenas sueltas con fundidos a negro. Sin continuidad no se percibía un arco.
3. Símbolos abstractos (hilos, nudos, cajas, siluetas genéricas) que el público tenía que descifrar mientras escuchaba un texto ya reflexivo.
4. Movimiento pobre: aparecer, dibujar una línea, desvanecer. Sin cámara, sin transformaciones, sin anticipación ni rebote.
5. Se revisó con capturas fijas, así que nunca se evaluó el ritmo ni la fluidez.
</lecciones_del_intento_anterior>

<direccion>
Tiendes a converger hacia resultados genéricos y «promedio»; aquí eso sería repetir el intento anterior. Busca una propuesta con carácter propio, pensada para esta idea.
- Continuidad: una toma continua o casi continua. La cámara viaja y las formas se transforman unas en otras (morph), para que el público sienta un solo recorrido del deseo.
- Menos símbolos, más acción: la voz explica y la imagen muestra una transformación que suma.
- Personaje expresivo aunque sea simple (postura, gesto, peso), porque la idea es humana y necesita empatía.
- Principios de animación: anticipación, seguimiento y solapamiento, arcos, easing con intención, movimiento secundario. Pocos momentos de gran impacto bien orquestados valen más que efectos dispersos. También debe haber quietud deliberada.
- Atmósfera y profundidad (capas, gradientes, textura ligera) en lugar de fondos planos.
- Subtítulos completos en capa editable: máximo 2 renglones, abajo, dentro de 100–930 px de ancho, sin cambiar palabras. Títulos ocasionales arriba.
- Formato: vertical 1080×1920, 30 fps, 131.467 s (termina unos 2 s después de la última palabra).
- Paleta base (cada piel la modula, ver `<estetica>`): ciruela #241C27, ámbar #E3A04D, blanco cálido #F0E8DF, verde apagado #8CAA9C.
- Equipo para previsualizar: Windows 11, i7-1165G7, 12 GB RAM. Evita 3D y físicas pesadas.
</direccion>

<estetica>
Concepto: «El deseo cambia de piel». La estética cambia con cada etapa porque así cambia nuestra forma de percibir el deseo en cada iteración. Una sola cosa nunca cambia: la luz ámbar del deseo (mismo color #E3A04D, mismo pulso), que atraviesa todos los estilos. Así la variedad atrae y la constante conserva el punto: el deseo es el protagonista y sigue vivo al final.

Cinco pieles, cada una con su textura, ritmo y cámara:
1. Luz líquida (0–34.28 · combustible y paquete). Partículas y luz ámbar fluida sobre ciruela profundo, grano fino. En el paquete: macro, papel kraft, desenfoque de capas y cámara casi quieta; «Ese momento» es un silencio visual.
2. Collage acelerado (34.28–44.24 · consumo y vueltas). Recortes con borde de papel rasgado (casa, moto, teléfono, comida), animación a pasos tipo stop-motion (12 fps), cortes por coincidencia de forma y cada vuelta más rápida. Es el único tramo frenético.
3. Plano técnico (44.24–64.82 · reconocer el mecanismo). Todo se congela. El mundo pasa a línea fina sobre fondo oscuro, como una lámina de anatomía del deseo, con rótulos a mano: impulso, anticipación, satisfacción, negación. En la negación, la mano aprieta y la luz ámbar se escapa entre los dedos.
4. Materia dura (64.82–75.24 · condiciones). Casi sin color, geometría rígida, texturas de concreto. El propio cuadro se estrecha con franjas que limitan el espacio. Movimiento pesado.
5. Textil y lápiz (75.24–final · malla, sin garantías, corregir, continuar). Vuelve el color: hilos con textura de estambre o bordado, manos, escenas de casa, clase y trabajo en recortes cálidos. Al corregir, el dibujo se ve a lápiz: se borra y se redibuja, con líneas que vibran a 8–12 fps (boiling). Corregir se ve como parte natural del dibujo, no como castigo.
Cierre: las cinco pieles conviven un instante en el mismo cuadro y la luz ámbar sigue pulsando.

Transiciones entre pieles: siempre por transformación (la luz ámbar se convierte en la siguiente textura, un recorte se desarma en líneas, una línea se vuelve hilo), nunca por fundido a negro.
Recursos viables en HTML/SVG/GSAP: grano y papel con filtros SVG (feTurbulence), bordes rasgados con trazos irregulares, animación a pasos con `steps()`, líneas que vibran con 2–3 variantes alternadas, franjas de encuadre con máscaras, tipografía cinética y morph de formas. Verifica en la documentación oficial de GSAP qué plugins están disponibles y bajo qué licencia antes de usarlos; no lo supongas. Sin fotos reales: los recortes son ilustrados con textura.
Sonido (opcional, evaluar con audio): una base mínima que cambie con cada piel y nunca tape la voz.
Riesgo que debes cuidar: la variedad no puede volverse ruido. Si en la prueba un cambio de piel distrae de la voz, simplifica esa piel antes que la idea.
</estetica>

<referencia_visual>
Enlace: https://x.com/VoidStateKate/status/2104041451084517742 (desde el contenedor no se puede abrir X; esta es mi descripción)
- Estilo (ilustración con personajes / formas abstractas que se transforman / tipografía / mezcla): …
- Ritmo (rápido con cortes / fluido y continuo): …
- Lo que más me gusta (colores, texturas, cámara, transiciones, sonido): …
- Qué no quiero de esa referencia: …
</referencia_visual>

<ejemplos_de_toma>
Así quiero que describas cada toma del animatic: acción y transformación, no el dibujo de la frase.

<example tipo="mal">
44.24–46.27 · Aparece una persona y su hilo. Subtítulo: «Podríamos argumentar que este equilibrio».
</example>

<example tipo="bien">
44.24–50.30 · La cámara sigue la estela del teléfono que se apaga y aterriza en las manos de la persona. Ella se detiene por primera vez; la luz que la movía se abre en cuatro corrientes que la rodean como si pudiera mirarlas desde fuera. Transformación: el objeto se disuelve en su propio mecanismo. Quietud de 0.8 s antes de «reconocemos los impulsos».
</example>
</ejemplos_de_toma>

<proceso>
1. En máximo 150 palabras: tu lectura de la idea y la propuesta visual (un solo concepto, sin variantes). Luego el animatic completo en texto, por tomas con tiempos fuente, con el formato de `<ejemplos_de_toma>`.
2. Construye solo una prueba de 20 s que cruce dos pieles: el final del collage acelerado y la transición al plano técnico de «reconocer el mecanismo» (fuente aprox. 38.76–58.80: vueltas, freno, impulso, anticipación, satisfacción y negación). Así se prueba a la vez la estética cambiante y la transición por transformación. Renderízala a MP4 con el audio de ese tramo. Entrégala y detente para que la revise.
3. Si la apruebo, construye la pieza completa reutilizando lo aprobado. Si no alcanza el nivel, propón cambiar de herramienta (After Effects, Rive u otra) y entrega un guion técnico toma por toma en lugar de seguir intentando a ciegas.
4. Guarda el avance en archivos del repositorio (animatic, estado.md con lo aprobado y lo pendiente) para poder continuar en otro chat sin repetir contexto.
</proceso>

<criterios_de_revision>
Antes de entregar cada render, compruébalo contra esto (con herramientas reales, sin suponer):
- Movimiento: revisa tiras de fotogramas consecutivos (por ejemplo 12 fotogramas seguidos en los momentos clave), no solo capturas sueltas. Busca saltos, elementos que aparecen de golpe, cosas que se enciman o se salen de cuadro.
- Continuidad: ningún corte a negro entre ideas, salvo que lo justifiques.
- Sincronía: las acciones clave caen en las palabras que las motivan (usa los tiempos de la transcripción y la detección de silencios del audio).
- Subtítulos: todos en ≤ 2 renglones, dentro del margen y sin solaparse (comprobación automática).
- Técnica: `@hyperframes/lint` sin errores; línea de tiempo pausada, determinista, duración exacta.
Reporta brevemente qué construiste, qué comprobaste y qué falta. Si algo no lo puedes comprobar (por ejemplo, oír la mezcla), dilo. Si no estás seguro de una librería o API, dilo y remite a la documentación oficial en lugar de inventar. Consumo de tokens: «no disponible» si la interfaz no lo expone.
</criterios_de_revision>
