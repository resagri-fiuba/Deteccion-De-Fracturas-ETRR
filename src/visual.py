"""
visual.py — Mirar las imágenes antes de modelarlas.

Suena obvio y casi nadie lo hace: la primera obligación con un dataset nuevo
es abrirlo y mirarlo. La mitad de los problemas (imágenes rotadas, texto
quemado en la placa, estudios duplicados) se ven a ojo en cinco minutos y no
aparecen en ninguna métrica hasta que ya es tarde.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Paleta del proyecto. Tenerla en un solo lugar hace que todos los gráficos
# del informe final se vean como una familia y no como un collage.
ROJO = "#C8401F"     # fractura / atención
AZUL = "#1B6B87"     # normal / estructura
GRIS = "#6B7A87"


def cargar_gris(ruta: str | Path) -> np.ndarray:
    """Abre una imagen y la devuelve como matriz de grises (alto, ancho).

    Las radiografías ya son en escala de grises, pero muchos archivos vienen
    guardados como RGB con los tres canales iguales. Convertir a 'L' garantiza
    que siempre trabajemos con una matriz 2D.
    """
    return np.array(Image.open(ruta).convert("L"))


def grilla(rutas, etiquetas=None, filas: int = 4, columnas: int = 5,
           titulo: str | None = None, guardar: Path | None = None):
    """Muestra un puñado de radiografías en una grilla.

    rutas      lista de rutas a imágenes
    etiquetas  lista paralela de 0/1 (opcional). El borde se pinta rojo si es 1.
    """
    n = min(len(rutas), filas * columnas)
    fig, ejes = plt.subplots(filas, columnas, figsize=(columnas * 2.4, filas * 2.6))
    ejes = np.array(ejes).reshape(-1)

    for i, eje in enumerate(ejes):
        eje.axis("off")
        if i >= n:
            continue

        img = cargar_gris(rutas[i])
        eje.imshow(img, cmap="gray")

        if etiquetas is not None:
            tiene_fractura = bool(etiquetas[i])
            color = ROJO if tiene_fractura else AZUL
            eje.set_title(
                "FRACTURA" if tiene_fractura else "normal",
                fontsize=8, color=color, pad=4,
            )
            # El borde de color hace que el desbalance se vea de un vistazo.
            for lado in eje.spines.values():
                lado.set_visible(True)
                lado.set_color(color)
                lado.set_linewidth(2)
            eje.set_xticks([]); eje.set_yticks([]); eje.axis("on")

    if titulo:
        fig.suptitle(titulo, fontsize=13)
    fig.tight_layout()

    if guardar:
        guardar.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(guardar, dpi=120, bbox_inches="tight")
        print(f"Guardado en {guardar}")
    return fig


def histograma(ruta: str | Path, guardar: Path | None = None):
    """Muestra una radiografía al lado de su histograma de intensidades.

    ¿Para qué sirve el histograma? Para ver el CONTRASTE. Si todos los píxeles
    se amontonan en una franja angosta, la placa está lavada o quemada, y el
    modelo va a tener menos información con la que trabajar. Comparar
    histogramas entre imágenes también delata si vienen de equipos distintos.
    """
    img = cargar_gris(ruta)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4),
                                   gridspec_kw={"width_ratios": [1, 1.3]})

    ax1.imshow(img, cmap="gray")
    ax1.set_title(f"{Path(ruta).name}\n{img.shape[1]}×{img.shape[0]} px", fontsize=10)
    ax1.axis("off")

    ax2.hist(img.ravel(), bins=64, range=(0, 255), color=AZUL, alpha=.85)
    ax2.set_title("Distribución de intensidades", fontsize=10)
    ax2.set_xlabel("valor del píxel  (0 = negro, 255 = blanco)")
    ax2.set_ylabel("cantidad de píxeles")
    ax2.spines[["top", "right"]].set_visible(False)

    # Marcamos la media para tener una referencia visual del brillo global.
    ax2.axvline(img.mean(), color=ROJO, linestyle="--", linewidth=1.5)
    ax2.text(img.mean() + 5, ax2.get_ylim()[1] * .80,
             f"media {img.mean():.0f}", color=ROJO, fontsize=9,
             bbox=dict(facecolor="white", edgecolor="none", alpha=.75, pad=1.5))

    fig.tight_layout()
    if guardar:
        guardar.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(guardar, dpi=120, bbox_inches="tight")
        print(f"Guardado en {guardar}")
    return fig


def describir(ruta: str | Path) -> dict:
    """Devuelve las estadísticas básicas de una imagen, como diccionario."""
    img = cargar_gris(ruta)
    return {
        "archivo": Path(ruta).name,
        "alto": img.shape[0],
        "ancho": img.shape[1],
        "tipo_de_dato": str(img.dtype),
        "minimo": int(img.min()),
        "maximo": int(img.max()),
        "media": round(float(img.mean()), 1),
        "desvio": round(float(img.std()), 1),
    }
