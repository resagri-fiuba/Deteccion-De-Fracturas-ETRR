"""
config.py — Un solo lugar donde viven las rutas y las constantes del proyecto.

¿Por qué existe este archivo?
-----------------------------
Porque el proyecto va a correr en dos lugares distintos: en Google Colab y en
la PC con GPU. Si las rutas están escritas a mano en cada notebook, el día que
cambien de máquina hay que tocar veinte archivos. Acá se tocan una vez.

Regla del proyecto: ningún notebook escribe una ruta a mano. Todos importan
de acá.
"""

from pathlib import Path
import os
import random

import numpy as np

# ---------------------------------------------------------------------------
# 1. ¿Dónde estamos corriendo?
# ---------------------------------------------------------------------------
# Colab define una variable de entorno propia. La usamos para decidir dónde
# guardar los datos: en Colab conviene el disco temporal /content, en la PC
# local conviene la carpeta del repositorio.

def en_colab() -> bool:
    """Devuelve True si el código está corriendo dentro de Google Colab."""
    try:
        import google.colab  # noqa: F401
        return True
    except ImportError:
        return False


# ---------------------------------------------------------------------------
# 2. Rutas
# ---------------------------------------------------------------------------
# RAIZ apunta a la carpeta del repositorio (la que contiene src/, notebooks/...).
# Path(__file__) es la ruta de ESTE archivo; .parent sube un nivel.

RAIZ = Path(__file__).resolve().parent.parent

if en_colab():
    # En Colab el disco se borra al cerrar la sesión, pero es rápido.
    DATOS = Path("/content/datos")
else:
    DATOS = RAIZ / "datos"

MODELOS = RAIZ / "modelos"      # pesos entrenados (no van al repo)
SALIDAS = RAIZ / "salidas"      # gráficos, tablas, informes (no van al repo)
DOCS = RAIZ / "docs"            # bitácora y fichas (esto SÍ va al repo)

# Subcarpetas del dataset una vez descomprimido
FRACATLAS = DATOS / "FracAtlas"
FRACATLAS_IMGS = FRACATLAS / "images"
FRACATLAS_ANOT = FRACATLAS / "Annotations"


def crear_carpetas() -> None:
    """Crea todas las carpetas del proyecto si no existen. Es idempotente:
    llamarla diez veces tiene el mismo efecto que llamarla una."""
    for carpeta in (DATOS, MODELOS, SALIDAS, DOCS):
        carpeta.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 3. Reproducibilidad
# ---------------------------------------------------------------------------
# Un experimento que no se puede repetir no es un experimento. Fijar la semilla
# hace que todo lo "aleatorio" (mezclar el dataset, inicializar pesos) salga
# igual cada vez. Es la diferencia entre un resultado y una anécdota.

SEMILLA = 42


def fijar_semilla(semilla: int = SEMILLA) -> None:
    """Fija la semilla de todos los generadores de números aleatorios que
    usamos. Llamar SIEMPRE al principio de cada notebook."""
    random.seed(semilla)
    np.random.seed(semilla)
    os.environ["PYTHONHASHSEED"] = str(semilla)
    try:
        import torch
        torch.manual_seed(semilla)
        torch.cuda.manual_seed_all(semilla)
    except ImportError:
        # Todavía no instalamos torch (semana 1). No pasa nada.
        pass


# ---------------------------------------------------------------------------
# 4. Constantes del proyecto
# ---------------------------------------------------------------------------
# El descargo de responsabilidad va acá para que sea imposible olvidarlo:
# cualquier notebook, gráfico o demo lo importa de un único lugar.

DESCARGO = (
    "Herramienta educativa de asistencia. NO es un dispositivo médico y NO "
    "debe usarse para tomar decisiones clínicas. Proyecto escolar — ETRR."
)

if __name__ == "__main__":
    # Correr `python src/config.py` imprime el estado actual. Útil para
    # verificar que las rutas apuntan a donde uno cree.
    crear_carpetas()
    print(f"¿En Colab?      {en_colab()}")
    print(f"Raíz del repo:  {RAIZ}")
    print(f"Datos:          {DATOS}")
    print(f"Semilla:        {SEMILLA}")
