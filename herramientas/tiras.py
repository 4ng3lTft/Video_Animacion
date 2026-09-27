"""Hojas de contacto para revisar movimiento: fotogramas CONSECUTIVOS, no capturas sueltas.

Uso:
  python3 herramientas/tiras.py <carpeta_png> <salida.jpg> <desde> <hasta> [--paso 1] [--cols 6] [--t0 38.76] [--ancho 270]
Cada miniatura lleva el número de fotograma y el tiempo fuente (t0 + f/30).
"""
import argparse
import os

from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("carpeta")
ap.add_argument("salida")
ap.add_argument("desde", type=int)
ap.add_argument("hasta", type=int)
ap.add_argument("--paso", type=int, default=1)
ap.add_argument("--cols", type=int, default=6)
ap.add_argument("--t0", type=float, default=38.76)
ap.add_argument("--ancho", type=int, default=270)
a = ap.parse_args()

fr = list(range(a.desde, a.hasta + 1, a.paso))
w = a.ancho
h = int(w * 1920 / 1080)
filas = (len(fr) + a.cols - 1) // a.cols
hoja = Image.new("RGB", (a.cols * w, filas * (h + 22)), (12, 10, 14))
dr = ImageDraw.Draw(hoja)
for i, f in enumerate(fr):
    p = os.path.join(a.carpeta, "f%04d.png" % f)
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS)
    x, y = (i % a.cols) * w, (i // a.cols) * (h + 22)
    hoja.paste(im, (x, y + 22))
    dr.text((x + 4, y + 5), "f%d  %.2fs" % (f, a.t0 + f / 30), fill=(230, 220, 200))
hoja.save(a.salida, quality=88)
print(a.salida, hoja.size)
