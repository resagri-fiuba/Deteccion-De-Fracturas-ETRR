"""
datos.py — Descargar FracAtlas y armar una tabla con una fila por radiografía.

La idea de este módulo es que el notebook quede corto y legible. Todo lo feo
(descargar, descomprimir, buscar archivos) vive acá adentro.

FracAtlas: 4.083 radiografías de mano, pierna, cadera y hombro.
717 tienen fractura (922 instancias). Licencia CC BY 4.0 — hay que citarlo.
Paper: https://www.nature.com/articles/s41597-023-02432-4
"""

from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd
import requests
from tqdm.auto import tqdm

from . import config

# ---------------------------------------------------------------------------
# 1. Descarga
# ---------------------------------------------------------------------------
# Figshare sirve los archivos por un "ndownloader" con un ID numérico.
# Si algún día este ID cambia, la descarga va a fallar con un error claro.
# Para conseguir el ID actual: entrar a la página del dataset, botón derecho
# sobre "Download", "Copiar dirección del enlace".
FRACATLAS_URL = "https://figshare.com/ndownloader/files/43283628"
FRACATLAS_PAGINA = "https://figshare.com/articles/dataset/The_dataset/22363012"


def descargar(url: str, destino: Path, forzar: bool = False) -> Path:
    """Descarga un archivo mostrando una barra de progreso.

    Si el archivo ya existe no lo vuelve a bajar (salvo forzar=True). Esto
    importa: en Colab uno reinicia el entorno diez veces por día y bajar
    un giga cada vez es una pérdida de tiempo.
    """
    destino.parent.mkdir(parents=True, exist_ok=True)

    if destino.exists() and not forzar:
        mb = destino.stat().st_size / 1e6
        print(f"Ya estaba descargado: {destino.name} ({mb:.0f} MB)")
        return destino

    respuesta = requests.get(url, stream=True, timeout=60)
    respuesta.raise_for_status()          # corta acá si el servidor dice error

    total = int(respuesta.headers.get("content-length", 0))
    barra = tqdm(total=total, unit="B", unit_scale=True, desc=destino.name)

    with open(destino, "wb") as f:
        for bloque in respuesta.iter_content(chunk_size=1024 * 256):
            f.write(bloque)
            barra.update(len(bloque))
    barra.close()

    return destino


def descomprimir(zip_path: Path, destino: Path) -> Path:
    """Descomprime el .zip si todavía no fue descomprimido."""
    destino.mkdir(parents=True, exist_ok=True)

    if config.FRACATLAS_IMGS.exists():
        print("Ya estaba descomprimido.")
        return destino

    with zipfile.ZipFile(zip_path) as z:
        for miembro in tqdm(z.namelist(), desc="Descomprimiendo"):
            z.extract(miembro, destino)
    return destino


def preparar_fracatlas() -> Path:
    """Descarga + descomprime FracAtlas. Devuelve la carpeta del dataset.

    Es la única función que hay que llamar desde el notebook.
    """
    config.crear_carpetas()
    zip_path = config.DATOS / "FracAtlas.zip"

    try:
        descargar(FRACATLAS_URL, zip_path)
    except Exception as e:
        raise RuntimeError(
            f"No se pudo descargar FracAtlas ({e}).\n"
            f"Bajalo a mano desde {FRACATLAS_PAGINA} y subilo como "
            f"{zip_path}, después volvé a correr esta celda."
        ) from e

    descomprimir(zip_path, config.DATOS)

    if not config.FRACATLAS_IMGS.exists():
        # El zip puede traer una carpeta contenedora con otro nombre.
        candidatos = list(config.DATOS.glob("**/images"))
        if candidatos:
            print(f"Aviso: las imágenes están en {candidatos[0]}, no donde "
                  f"esperábamos. Ajustá config.FRACATLAS si hace falta.")
    return config.FRACATLAS


# ---------------------------------------------------------------------------
# 2. La tabla
# ---------------------------------------------------------------------------
# Antes de entrenar nada queremos UNA TABLA: una fila por imagen, con su ruta
# y su etiqueta. Todo lo que viene después (particiones, entrenamiento,
# evaluación) sale de esta tabla. Si la tabla está mal, todo está mal.

def tabla_imagenes() -> pd.DataFrame:
    """Devuelve un DataFrame con una fila por radiografía.

    Columnas garantizadas:
        archivo   nombre del archivo, ej. 'IMG0000001.jpg'
        ruta      ruta completa a la imagen
        fractura  1 si tiene fractura, 0 si no

    Si FracAtlas trae su dataset.csv, además vienen las columnas de parte del
    cuerpo (hand, leg, hip, shoulder) y de proyección (frontal, lateral...).
    """
    csv = config.FRACATLAS / "dataset.csv"

    if csv.exists():
        df = pd.read_csv(csv)
        # La columna de imagen se llama distinto según la versión del dataset.
        col_img = next(
            (c for c in ("image_id", "image", "filename") if c in df.columns),
            None,
        )
        col_frac = next(
            (c for c in ("fractured", "fracture", "label") if c in df.columns),
            None,
        )
        if col_img and col_frac:
            df = df.rename(columns={col_img: "archivo", col_frac: "fractura"})
            df["ruta"] = df["archivo"].apply(_buscar_imagen)
            df["fractura"] = df["fractura"].astype(int)
            return df.dropna(subset=["ruta"]).reset_index(drop=True)

    # Plan B: deducir la etiqueta de la carpeta donde está cada imagen.
    print("No encontré dataset.csv — deduzco la etiqueta de las carpetas.")
    filas = []
    for carpeta, etiqueta in (("Fractured", 1), ("Non_fractured", 0)):
        for p in (config.FRACATLAS_IMGS / carpeta).glob("*.jpg"):
            filas.append({"archivo": p.name, "ruta": p, "fractura": etiqueta})

    if not filas:
        raise FileNotFoundError(
            "No encontré imágenes. ¿Corriste preparar_fracatlas() primero?"
        )
    return pd.DataFrame(filas)


def _buscar_imagen(nombre: str) -> Path | None:
    """Busca una imagen por nombre en las subcarpetas de images/."""
    for sub in ("all", "Fractured", "Non_fractured", ""):
        p = config.FRACATLAS_IMGS / sub / nombre
        if p.exists():
            return p
    return None


def resumen(df: pd.DataFrame) -> None:
    """Imprime la ficha del dataset. Este texto va a la bitácora."""
    n = len(df)
    con = int(df["fractura"].sum())
    sin = n - con
    print(f"Radiografías totales : {n:,}")
    print(f"  con fractura       : {con:,}  ({con / n:.1%})")
    print(f"  sin fractura       : {sin:,}  ({sin / n:.1%})")
    print()
    print("Un modelo que SIEMPRE dijera 'sin fractura' acertaría el "
          f"{sin / n:.1%} de las veces.")
    print("Ese es el número a vencer. No el 50%.")

    partes = [c for c in ("hand", "leg", "hip", "shoulder") if c in df.columns]
    if partes:
        print("\nPor parte del cuerpo:")
        for p in partes:
            print(f"  {p:10s} {int(df[p].sum()):>6,}")
