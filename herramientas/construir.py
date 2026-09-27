"""Ensambla una composición HyperFrames autocontenida a partir de su plantilla.

Uso:  python3 herramientas/construir.py prueba/prueba.fuente.html prueba/prueba.html

La plantilla contiene marcas {{NOMBRE}} que aquí se sustituyen por:
  - fuentes incrustadas (base64, OFL),
  - texturas PNG generadas con semilla fija (grano de película, fibra de papel),
  - marcado SVG generado por geometria.py (personaje y objetos en cada piel, desgarro),
  - constantes compartidas con la línea de tiempo (K), para que el dibujo y el movimiento
    usen exactamente las mismas posiciones.
"""
import base64
import io
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import geometria as g  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))


def b64(ruta):
    with open(ruta, "rb") as f:
        return base64.b64encode(f.read()).decode()


def png_b64(arr):
    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------- texturas

def textura_grano(n=256, semilla=7):
    rng = np.random.default_rng(semilla)
    v = rng.normal(0, 1, (n, n))
    # grano un poco agrupado: mezcla de ruido fino y ruido suavizado
    s = (v + np.roll(v, 1, 0) + np.roll(v, 1, 1) + np.roll(np.roll(v, 1, 0), 1, 1)) / 4
    m = 0.6 * v + 0.4 * s
    g8 = np.clip(128 + m * 46, 0, 255).astype(np.uint8)
    return png_b64(np.dstack([g8, g8, g8, np.full_like(g8, 255)]))


def textura_fibra(n=384, semilla=3):
    """Fibras y motas de papel sobre transparente, para superponer al mundo de recortes."""
    rng = random.Random(semilla)
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    px = img.load()
    for _ in range(900):  # motas
        x, y = rng.randrange(n), rng.randrange(n)
        claro = rng.random() < 0.55
        c = (255, 246, 230, rng.randrange(18, 46)) if claro else (20, 12, 20, rng.randrange(14, 36))
        px[x, y] = c
    for _ in range(140):  # fibras cortas y curvas
        x, y = rng.uniform(0, n), rng.uniform(0, n)
        a = rng.uniform(0, math.pi)
        largo = rng.randrange(8, 30)
        claro = rng.random() < 0.6
        for i in range(largo):
            a += rng.uniform(-0.18, 0.18)
            x = (x + math.cos(a)) % n
            y = (y + math.sin(a)) % n
            px[int(x), int(y)] = (255, 244, 226, 34) if claro else (18, 10, 18, 26)
    arr = np.array(img)
    # manchas amplias muy suaves (irregularidad del papel), periódicas para que el mosaico no se note
    yy, xx = np.mgrid[0:n, 0:n] / n * 2 * math.pi
    ondas = (np.sin(xx * 2 + 1.3) * np.cos(yy * 3 + 0.4) + np.sin(xx * 5 + yy * 2)) * 0.5
    alfa = np.clip(ondas * 14 + 10, 0, 40).astype(np.uint8)
    base = np.dstack([np.full((n, n), 250, np.uint8), np.full((n, n), 238, np.uint8),
                      np.full((n, n), 220, np.uint8), alfa])
    manchado = np.where(arr[..., 3:4] > 0, arr, base)
    return png_b64(manchado.astype(np.uint8))


# ---------------------------------------------------------------- constantes compartidas

K = {
    "T0": 38.76,               # tiempo fuente del fotograma 0 de la prueba
    "DUR": 20.04,              # 38.76–58.80
    "rig": {"x": 470, "y": 1290, "s": 1.25},
    # especímenes en el plano (misma posición final que en el collage congelado)
    "esp": {"casa": [250, 470, 0.8], "moto": [840, 430, 0.8], "tel": [880, 830, 0.78]},
    "flotar": [668, 742],      # la luz flota sobre la mano abierta
    "mano": [668, 800],        # objetivo de la mano al ofrecer / apretar
    "impulso": [806, 690],     # adonde tira el impulso
    "pecho": [497, 724],       # la luz en el pecho (pose neutra)
    "mesa": [790, 1150],       # centro del tablero de la mesa
    "olla": [760, 1098],       # donde la luz se asienta (satisfacción)
    "desgarroY": 700,
}


def huesped(nombre):
    x, y, s = K["esp"][nombre]
    hx, hy = g.HUESPED[nombre]
    return [x + hx * s, y + hy * s]


def arco(a, b, alto):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - alto
    return "M %.1f %.1f Q %.1f %.1f %.1f %.1f" % (a[0], a[1], mx, my, b[0], b[1])


def marcado_plano():
    """Piezas propias del plano técnico: arcos de anticipación, mesa, olla, rótulos."""
    f = K["flotar"]
    altos = (("casa", 150), ("moto", 190), ("tel", 110))
    K["arcos"] = {n: [f, huesped(n), a] for n, a in altos}
    puntos = "".join('<g id="arco-%s">%s</g>' % (n, puntos_arco(f, huesped(n), a, cls="pt pt-" + n)) for n, a in altos)
    impulso = puntos_arco(K["pecho"], K["impulso"], 24, paso=22, cls="pt-imp")
    mx, my = K["mesa"]
    L = g.LINEA
    mesa = [
        '<path class="m-traz" d="M %d %d L %d %d" stroke="%s" stroke-width="2.6" fill="none"/>' % (mx - 170, my, mx + 170, my, L),
        '<path class="m-traz" d="M %d %d L %d %d" stroke="%s" stroke-width="2.6" fill="none"/>' % (mx - 150, my, mx - 140, my + 150, L),
        '<path class="m-traz" d="M %d %d L %d %d" stroke="%s" stroke-width="2.6" fill="none"/>' % (mx + 150, my, mx + 140, my + 150, L),
        '<path class="m-traz" d="M %d %d L %d %d" stroke="%s" stroke-width="1.6" fill="none" opacity=".6"/>' % (mx - 170, my + 14, mx + 170, my + 14, L),
    ]
    ox, oy = K["olla"]
    olla = [
        # olla al centro, dos platos a los lados: la comida es para más de una persona
        '<path class="m-traz" d="M %d %d C %d %d %d %d %d %d" stroke="%s" stroke-width="2.6" fill="%s"/>' % (
            ox - 52, oy - 20, ox - 50, oy + 46, ox + 50, oy + 46, ox + 52, oy - 20, L, g.FONDO_PLANO),
        '<path class="m-traz" d="M %d %d L %d %d" stroke="%s" stroke-width="2.6" fill="none"/>' % (ox - 62, oy - 20, ox + 62, oy - 20, L),
        '<path class="m-traz" d="M %d %d q -14 0 -14 12 M %d %d q 14 0 14 12" stroke="%s" stroke-width="2.6" fill="none"/>' % (
            ox - 52, oy - 4, ox + 52, oy - 4, L),
        '<path class="m-traz" d="M %d %d Q %d %d %d %d" stroke="%s" stroke-width="2.4" fill="none"/>' % (
            mx - 150, my - 6, mx - 118, my + 14, mx - 86, my - 6, L),
        '<path class="m-traz" d="M %d %d L %d %d" stroke="%s" stroke-width="2.4" fill="none"/>' % (mx - 156, my - 6, mx - 80, my - 6, L),
        '<path class="m-traz" d="M %d %d Q %d %d %d %d" stroke="%s" stroke-width="2.4" fill="none"/>' % (
            mx + 78, my - 6, mx + 110, my + 14, mx + 142, my - 6, L),
        '<path class="m-traz" d="M %d %d L %d %d" stroke="%s" stroke-width="2.4" fill="none"/>' % (mx + 72, my - 6, mx + 148, my - 6, L),
    ]
    vapor = ''.join(
        '<path class="m-vapor" d="M %d %d c -14 -18 14 -30 0 -48 c -14 -18 14 -30 0 -48" stroke="%s" stroke-width="2.2" fill="none" stroke-linecap="round" opacity=".7"/>' % (
            ox + dx, oy - 34, L) for dx in (-18, 18))
    # anillo de tiempo alrededor de la olla (se dibuja despacio)
    tiempo = '<circle id="m-tiempo" cx="%d" cy="%d" r="92" fill="none" stroke="#8CAA9C" stroke-width="2.2" transform="rotate(-90 %d %d)"/>' % (
        ox, oy - 6, ox, oy - 6)
    return {"MESA": "".join(mesa + olla), "VAPOR": vapor, "TIEMPO": tiempo, "ARCOS": puntos, "IMPULSO": impulso}


def muestras():
    """Recortes grandes de fondo del collage (papel kraft, ciruela, blanco)."""
    specs = [("sw1", 1040, 820, "#9C7F62"), ("sw2", 600, 460, "#6E4A63"), ("sw3", 560, 700, "#3A2B40"),
             ("sw4", 380, 280, "#F0E8DF")]
    return "".join('<g id="%s">%s</g>' % (i, g.papel(g.rrect(-w / 2, -h / 2, w, h, 4), c, g.semilla(i), reborde=8, amp=2.6))
                   for i, w, h, c in specs)


def puntos_arco(a, b, alto, paso=20, cls=""):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - alto
    L = math.hypot(b[0] - a[0], b[1] - a[1]) + alto
    n = max(4, int(L / paso))
    out = []
    for i in range(1, n):
        t = i / n
        x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * mx + t * t * b[0]
        y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * my + t * t * b[1]
        out.append('<circle class="%s" cx="%.1f" cy="%.1f" r="3.2"/>' % (cls, x, y))
    return "".join(out)


def otra_mano():
    """Antebrazo y mano de otra persona que entra por la derecha (línea)."""
    ante = g.capsula(0, 0, 300, 0, 34)
    palma = g.rrect(-58, -20, 60, 40, 14)
    dedos = "".join(g.linea(g.capsula(-54, y, -86, y + 2, 11, 6)) for y in (-14, -4, 6, 15))
    return g.linea(ante) + dedos + g.linea(palma) + g.linea(g.capsula(-30, -18, -52, -36, 12, 6))


def main(fuente, salida):
    raiz = os.path.dirname(AQUI)
    html = open(os.path.join(raiz, fuente), encoding="utf-8").read()
    tl_des, arriba, abajo, fibra_arr, fibra_ab = g.mitades_desgarro(K["desgarroY"], 11)
    # grieta: se dibuja desde la luz hacia ambos lados antes de separar las mitades
    cx = 600
    izq = [p for p in tl_des if p[0] <= cx][::-1]
    der = [p for p in tl_des if p[0] >= cx]
    rep = {
        "FUENTE_LITERATA": b64(os.path.join(AQUI, "fuentes", "literata-latin-400-600.woff2")),
        "FUENTE_MANO": b64(os.path.join(AQUI, "fuentes", "architects-daughter-latin-400-normal.woff2")),
        "GRANO": textura_grano(),
        "FIBRA": textura_fibra(),
        "RIG_PAPEL": g.rig("papel", "c"),
        "RIG_LINEA": g.rig("linea", "p"),
        "CORTE_ARRIBA": g.d(arriba),
        "CORTE_ABAJO": g.d(abajo),
        "FIBRA_ARRIBA": g.d(fibra_arr),
        "FIBRA_ABAJO": g.d(fibra_ab),
        "GRIETA_IZQ": "M" + " L".join("%.1f %.1f" % p for p in izq),
        "GRIETA_DER": "M" + " L".join("%.1f %.1f" % p for p in der),
        "OTRA_MANO": otra_mano(),
    }
    for n in ("moto", "tel", "casa"):
        rep["OBJ_PAPEL_" + n.upper()] = g.objeto(n, "papel", "c")
        rep["OBJ_LINEA_" + n.upper()] = g.objeto(n, "linea", "p")
    rep.update(marcado_plano())
    rep["MUESTRAS"] = muestras()
    K["huesped"] = {n: list(g.HUESPED[n]) for n in g.HUESPED}
    rep["CONST"] = json.dumps(K, ensure_ascii=False)
    for k, v in rep.items():
        html = html.replace("{{%s}}" % k, v)
    faltan = [m for m in ("{{",) if m in html]
    if faltan:
        i = html.index("{{")
        raise SystemExit("Marca sin sustituir: " + html[i:i + 40])
    with open(os.path.join(raiz, salida), "w", encoding="utf-8") as f:
        f.write(html)
    print("escrito", salida, "%.1f KB" % (len(html.encode()) / 1024))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
