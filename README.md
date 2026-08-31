# Detección Automática de Fracturas Óseas mediante Inteligencia Artificial

Proyecto interdisciplinario — **Escuela Técnica Roberto Rocca**
Ramiro Sagripanti · Joaquín García (7mo TEL) · Ciclo lectivo 2026

> ⚠️ **Descargo de responsabilidad**
> Este es un **proyecto educativo**. El software de este repositorio **no es un
> dispositivo médico**, no está validado clínicamente y **no debe usarse para
> tomar decisiones sobre pacientes**. Su único propósito es el aprendizaje de
> técnicas de visión por computadora.

---

## Qué hace

Entrena y evalúa modelos de aprendizaje profundo que detectan fracturas en
radiografías digitalizadas, y muestra **dónde** mira el modelo mediante mapas
de calor (Grad-CAM).

## Estado

| Semana | Etapa | Estado |
|---|---|---|
| 1 | Entorno y exploración de datos | 🔨 en curso |
| 2 | Partición por paciente | ⬜ |
| 3 | Clasificador base | ⬜ |
| 4 | Evaluación y umbral operativo | ⬜ |
| 5 | Detección con caja (YOLO) | ⬜ |
| 6 | Experimentos | ⬜ |
| 7 | Explicabilidad (Grad-CAM) | ⬜ |
| 8 | Demo web | ⬜ |
| 9 | Validación externa e informe | ⬜ |
| 10 | Presentación | ⬜ |

---

## Cómo correrlo

### En Google Colab (recomendado para empezar)

1. Abrir [colab.research.google.com](https://colab.research.google.com)
2. Pestaña **GitHub** → pegar `resagri-fiuba/Deteccion-De-Fracturas-ETRR`
3. Elegir `notebooks/01_exploracion.ipynb`
4. `Entorno de ejecución` → `Cambiar tipo de entorno` → **GPU**

El notebook clona este repositorio solo, así que siempre corre con la última
versión del código.

### En la PC con GPU

```bash
git clone https://github.com/resagri-fiuba/Deteccion-De-Fracturas-ETRR.git
cd Deteccion-De-Fracturas-ETRR

python -m venv .venv
source .venv/bin/activate          # en Windows:  .venv\Scripts\activate
pip install -r requirements.txt

jupyter lab                        # y abrir notebooks/01_exploracion.ipynb
```

Verificar que la GPU se ve desde Python:

```python
import torch; print(torch.cuda.is_available())   # tiene que decir True
```

---

## Estructura

```
├── notebooks/          Un notebook por etapa. Son el hilo narrativo del proyecto.
│   └── 01_exploracion.ipynb
├── src/                El código de verdad. Los notebooks solo lo llaman.
│   ├── config.py       Rutas, semilla, descargo. Un solo lugar para todo.
│   ├── datos.py        Descargar FracAtlas y armar la tabla de imágenes.
│   └── visual.py       Grillas de radiografías e histogramas.
├── docs/               Bitácora, fichas, chuleta de Git. Esto SÍ se versiona.
├── datos/              Datasets descargados. Ignorado por git (pesa demasiado).
├── modelos/            Pesos entrenados. Ignorado por git.
└── salidas/            Gráficos e informes generados. Ignorado por git.
```

**Regla del proyecto:** al repositorio va el *código que genera* los datos y los
modelos, nunca los datos y los modelos. Si borrás `datos/` y `modelos/`, todo
se puede reconstruir corriendo los notebooks en orden.

---

## Datos

| Dataset | Qué es | Licencia |
|---|---|---|
| [FracAtlas](https://figshare.com/articles/dataset/The_dataset/22363012) | 4.083 radiografías (mano, pierna, cadera, hombro); 717 con fractura | CC BY 4.0 |
| [GRAZPEDWRI-DX](https://figshare.com/articles/dataset/GRAZPEDWRI-DX/14825193) | 20.327 radiografías de muñeca pediátrica con cajas | ver términos |

Las citas completas están en [`CITATION.md`](CITATION.md). Ningún dato de
pacientes reales de instituciones locales se usa en este proyecto.

---

## Licencia

**AGPL-3.0** — ver [`LICENSE`](LICENSE).

Elegimos AGPL porque a partir de la semana 5 el proyecto usa
[Ultralytics YOLO](https://github.com/ultralytics/ultralytics), que se
distribuye bajo esa licencia: cualquier trabajo derivado que se publique tiene
que ser abierto también. Es una restricción real, no un trámite, y forma parte
de lo que el proyecto documenta.
