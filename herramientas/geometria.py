"""Geometría compartida por las pieles: personaje articulado, objetos del deseo y recortes.

Todo se genera con semillas fijas (determinista). Cada forma se define una sola vez como
polígono y se dibuja en dos pieles:
  - papel(...)  → recorte con borde rasgado, reborde blanco de fibra y sombra (collage).
  - linea(...)  → contorno fino con relleno del fondo (plano técnico).
Así el personaje y los objetos coinciden al milímetro cuando una piel se transforma en otra.
"""
import math
import random
import zlib


def semilla(*partes):
    """Semilla estable entre ejecuciones (hash() de Python cambia en cada proceso)."""
    return zlib.crc32("|".join(map(str, partes)).encode()) & 0xffff

# ---------------------------------------------------------------- primitivas

def circulo(cx, cy, r, n=36, a0=0.0):
    return [(cx + r * math.cos(a0 + 2 * math.pi * i / n), cy + r * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n)]


def rrect(x, y, w, h, r, n=6):
    """Rectángulo redondeado como polígono (sentido horario en pantalla)."""
    r = min(r, w / 2, h / 2)
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def capsula(x1, y1, x2, y2, w, n=8):
    """Cápsula (tubo con extremos redondos) entre dos puntos."""
    ang = math.atan2(y2 - y1, x2 - x1)
    r = w / 2
    pts = []
    for i in range(n + 1):
        a = ang - math.pi / 2 + math.pi * i / n
        pts.append((x2 + r * math.cos(a), y2 + r * math.sin(a)))
    for i in range(n + 1):
        a = ang + math.pi / 2 + math.pi * i / n
        pts.append((x1 + r * math.cos(a), y1 + r * math.sin(a)))
    return pts


def area(pts):
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return s / 2


def desplazar(pts, d):
    """Desplaza cada vértice d px hacia fuera (normal promedio de las aristas vecinas)."""
    sgn = 1 if area(pts) > 0 else -1
    out = []
    n = len(pts)
    for i in range(n):
        xp, yp = pts[i - 1]
        x, y = pts[i]
        xn, yn = pts[(i + 1) % n]
        nx = ny = 0.0
        for (ax, ay, bx, by) in ((xp, yp, x, y), (x, y, xn, yn)):
            dx, dy = bx - ax, by - ay
            L = math.hypot(dx, dy) or 1
            nx += -dy / L * sgn
            ny += dx / L * sgn
        L = math.hypot(nx, ny) or 1
        out.append((x + nx / L * d, y + ny / L * d))
    return out


def rasgar(pts, rng, paso=8.0, amp=2.0):
    """Subdivide las aristas y las desplaza al azar (semilla fija): borde de papel rasgado."""
    out = []
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        k = max(1, int(L / paso))
        nx, ny = (-dy / L, dx / L) if L else (0, 0)
        for j in range(k):
            t = j / k
            d = rng.uniform(-amp, amp)
            out.append((x1 + dx * t + nx * d, y1 + dy * t + ny * d))
    return out


def d(pts):
    return "M" + " L".join("%.1f %.1f" % p for p in pts) + " Z"


def mover(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


# ---------------------------------------------------------------- pieles

PAPEL_FIBRA = "#EDE3D2"
SOMBRA = "#120C14"
LINEA = "#EDE3D6"
FONDO_PLANO = "#1D1721"


def papel(pts, color, semilla, cls="", reborde=4.5, amp=1.4, sombra=True, extra=""):
    rng = random.Random(semilla)
    borde = rasgar(desplazar(pts, reborde), rng, paso=7, amp=reborde * 0.55)
    cuerpo = rasgar(pts, rng, paso=9, amp=amp)
    c = ' class="%s"' % cls if cls else ""
    s = []
    if sombra:
        s.append('<path d="%s" fill="%s" opacity="0.38" transform="translate(5 7)"/>' % (d(borde), SOMBRA))
    s.append('<path d="%s" fill="%s"/>' % (d(borde), PAPEL_FIBRA))
    s.append('<path d="%s" fill="%s"%s/>' % (d(cuerpo), color, extra))
    return "<g%s>%s</g>" % (c, "".join(s))


def linea(pts, cls="", ancho=2.6, color=LINEA, relleno=FONDO_PLANO, extra=""):
    c = ' class="%s"' % cls if cls else ""
    return '<path%s d="%s" fill="%s" stroke="%s" stroke-width="%.1f" stroke-linejoin="round"%s/>' % (
        c, d(pts), relleno, color, ancho, extra)


# ---------------------------------------------------------------- personaje
# Origen del rig: entre los pies. Arriba es y negativa. Cada articulación se dibuja
# relativa a su pivote para que GSAP la gire con svgOrigin "0 0" sin ambigüedad.
#   cadera (torso)   rig (0,-300)
#   hombros          torso (±86,-205)
#   codo             brazo (0,118)
#   mano             antebrazo (0,108..140)
#   cuello (cabeza)  torso (0,-240); centro de la cabeza en (0,-70), r 60

COL = {
    "camisa": "#8CAA9C", "pantalon": "#4A3A52", "piel": "#E6D2BF", "pelo": "#1F1722",
    "zapato": "#1F1722", "manga": "#7E9C8F",
}


def partes_rig():
    """Devuelve un dict de polígonos por articulación (coordenadas locales al pivote)."""
    P = {}
    P["piernas"] = [(-66, -302), (-76, -14), (-24, -14), (-2, -196), (2, -196), (24, -14), (76, -14), (66, -302)]
    P["zapatoI"] = rrect(-86, -22, 66, 24, 11)
    P["zapatoD"] = rrect(20, -22, 66, 24, 11)
    # torso relativo a la cadera
    P["torso"] = [(-96, -215), (-104, -120), (-88, -34), (-74, 2), (74, 2), (88, -34), (104, -120), (96, -215),
                  (62, -240), (-62, -240)]
    # cabeza relativa al cuello
    P["cuello"] = rrect(-16, -26, 32, 34, 8)
    P["cabeza"] = circulo(0, -70, 60, 40)
    pelo = [(0 + 66 * math.cos(math.radians(a)), -70 + 66 * math.sin(math.radians(a))) for a in range(118, 352, 9)]
    pelo += [(-6 + 50 * math.cos(math.radians(a)), -84 + 46 * math.sin(math.radians(a))) for a in range(345, 125, -12)]
    P["pelo"] = pelo
    # brazo relativo al hombro; antebrazo relativo al codo
    P["brazo"] = capsula(0, 0, 0, 118, 38)
    P["antebrazo"] = capsula(0, 0, 0, 104, 30)
    P["palma"] = rrect(-19, 100, 38, 40, 12)
    P["dedo"] = capsula(0, 0, 0, 30, 10, 6)      # relativo a su nudillo
    P["pulgar"] = capsula(0, 0, 13, 26, 11, 6)   # relativo a su base
    P["manoAtras"] = circulo(0, 122, 21, 24)
    return P


DEDOS_X = (-12.5, -4.2, 4.2, 12.5)


def rig(piel, pref):
    """Personaje completo en una piel ('papel' o 'linea'). Clases compartidas entre pieles."""
    P = partes_rig()
    s = [0]

    def pz(nombre, color, cls="", pts=None, reb=4.5):
        s[0] += 1
        pts = pts or P[nombre]
        if piel == "papel":
            return papel(pts, color, semilla(pref, nombre, s[0]), cls=cls, reborde=reb, sombra=(reb > 3))
        return linea(pts, cls=cls)

    def brazo(lado, frente):
        cl = "F" if frente else "B"
        mano = ""
        if frente:
            dedos = "".join(
                '<g transform="translate(%.1f 136)"><g class="r-f r-f%d">%s</g></g>' % (x, i, pz("dedo", COL["piel"], reb=2.2))
                for i, x in enumerate(DEDOS_X))
            mano = ('<g class="r-mano%s">%s<g transform="translate(15 108)"><g class="r-pulgar">%s</g></g>%s</g>' % (
                cl, dedos, pz("pulgar", COL["piel"], reb=2.2), pz("palma", COL["piel"], reb=2.6)))
        else:
            mano = pz("manoAtras", COL["piel"], reb=3)
        return ('<g transform="translate(%d -205)"><g class="r-brazo%s">%s'
                '<g transform="translate(0 118)"><g class="r-ante%s">%s%s</g></g></g></g>' % (
                    lado, cl, pz("brazo", COL["manga"]), cl, pz("antebrazo", COL["piel"]), mano))

    cabeza = ('<g transform="translate(0 -240)"><g class="r-cabeza">%s%s%s'
              '<circle class="r-ojo" cx="26" cy="-74" r="%s" fill="%s"/>'
              '<path class="r-ceja" d="M 14 -94 L 40 -92" stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none"/>'
              '</g></g>') % (
        pz("cuello", COL["piel"], reb=3), pz("cabeza", COL["piel"]), pz("pelo", COL["pelo"], reb=3),
        "6.5" if piel == "papel" else "5", COL["pelo"] if piel == "papel" else LINEA,
        COL["pelo"] if piel == "papel" else LINEA, "6" if piel == "papel" else "3")

    torso = ('<g transform="translate(0 -300)"><g class="r-torso">%s%s%s%s</g></g>' % (
        brazo(-86, False), pz("torso", COL["camisa"]), cabeza, brazo(86, True)))
    cuerpo = pz("piernas", COL["pantalon"]) + pz("zapatoI", COL["zapato"], reb=3) + pz("zapatoD", COL["zapato"], reb=3)
    return '<g class="r-rig" id="%s-rig">%s%s</g>' % (pref, cuerpo, torso)


# ---------------------------------------------------------------- objetos del deseo
# Centrados en el origen. HUESPED: punto donde la luz se aloja en cada objeto.

HUESPED = {"moto": (98, -30), "tel": (0, -8), "casa": (-38, 36)}


def obj_moto():
    return [
        ("rueda1", circulo(-82, 40, 50, 30), "#2E2433"),
        ("rueda2", circulo(82, 40, 50, 30), "#2E2433"),
        ("buje1", circulo(-82, 40, 16, 18), "#F0E8DF"),
        ("buje2", circulo(82, 40, 16, 18), "#F0E8DF"),
        ("cuerpo", [(-86, -6), (-40, -44), (30, -46), (70, -52), (104, -18), (86, 22), (-40, 30)], "#B4695E"),
        ("asiento", rrect(-92, -44, 74, 20, 9), "#2E2433"),
        ("manubrio", capsula(64, -50, 50, -96, 12), "#2E2433"),
        ("puño", capsula(38, -98, 78, -100, 12), "#2E2433"),
        ("faro", circulo(98, -30, 14, 16), "#3B2F40"),
    ]


def obj_tel():
    return [
        ("cuerpo", rrect(-64, -116, 128, 232, 22), "#3B2F40"),
        ("pantalla", rrect(-50, -94, 100, 176, 9), "#566A73"),
        ("boton", circulo(0, 100, 7, 12), "#F0E8DF"),
    ]


def obj_casa():
    return [
        ("techo", [(-118, -14), (0, -118), (118, -14)], "#6E4A63"),
        ("muro", rrect(-94, -22, 188, 136, 4), "#F0E8DF"),
        ("ventana", rrect(-64, 12, 52, 48, 3), "#3B2F40"),
        ("puerta", rrect(18, 30, 44, 84, 3), "#9C7F62"),
        ("chimenea", rrect(48, -104, 26, 56, 2), "#6E4A63"),
    ]


OBJETOS = {"moto": obj_moto, "tel": obj_tel, "casa": obj_casa}


def objeto(nombre, piel, pref):
    partes = OBJETOS[nombre]()
    orden = partes
    if nombre == "casa":  # la chimenea va detrás del techo
        orden = [partes[4]] + partes[:4]
    out = []
    for i, (k, pts, col) in enumerate(orden):
        if piel == "papel":
            out.append(papel(pts, col, semilla(pref, nombre, k), reborde=3.5 if i else 4.5, sombra=(i == 0)))
        else:
            out.append(linea(pts, ancho=2.4))
    hx, hy = HUESPED[nombre]
    brillo = ('<circle class="o-brillo o-brillo-%s" cx="%d" cy="%d" r="120" fill="url(#halo)" opacity="0"/>' % (nombre, hx, hy))
    return "".join(out) + brillo


# ---------------------------------------------------------------- desgarro entre pieles

def linea_desgarro(y0, semilla, x0=-400, x1=1480, paso=14):
    rng = random.Random(semilla)
    pts = []
    x = x0
    y = y0
    while x <= x1:
        y = y0 + rng.uniform(-18, 18) * 0.6 + (y - y0) * 0.4
        pts.append((x, y + rng.uniform(-3, 3)))
        x += paso * rng.uniform(0.6, 1.4)
    return pts


def mitades_desgarro(y0=700, semilla=11):
    tl = linea_desgarro(y0, semilla)
    arriba = [(-400, -900)] + tl + [(1480, -900)]
    abajo = [(-400, 2800)] + tl + [(1480, 2800)]
    # reborde de fibra blanca a cada lado del desgarro
    rng = random.Random(semilla + 1)
    fibra_arr = tl + [(x, y - 7 - rng.uniform(0, 7)) for x, y in reversed(tl)]
    fibra_ab = tl + [(x, y + 6 + rng.uniform(0, 8)) for x, y in reversed(tl)]
    return tl, arriba, abajo, fibra_arr, fibra_ab
