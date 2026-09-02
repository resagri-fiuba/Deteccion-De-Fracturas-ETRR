# Curso — aprender con gatos antes de tocar radiografías

Estos dos notebooks no son parte del proyecto de detección de fracturas.
Son el ensayo general.

Resuelven un problema con **exactamente la misma forma** que el nuestro, pero con
datos públicos, livianos y sin implicancias médicas: CIFAR-10, distinguir gatos
del resto.

| | Curso (CIFAR-10) | Proyecto (FracAtlas) |
|---|---|---|
| Pregunta | ¿hay un gato? | ¿hay una fractura? |
| Imágenes | 60.000 de 32×32 px | 4.083 radiografías |
| Positivos | 10% | 17,6% |
| Modelo trivial acierta | 90% | 82,4% |
| Entrenar | segundos | minutos |

## Orden

1. **`01_datos_y_metricas.ipynb`** — sin redes neuronales todavía.
   Levantar un dataset, mirarlo, partirlo en entrenamiento/validación/test,
   entrenar un modelo simple, y descubrir por qué la accuracy engaña.
   Corre en CPU en pocos minutos.

2. **`02_redes_neuronales.ipynb`** — el bucle de entrenamiento escrito a mano,
   red densa, red convolucional y transfer learning, comparados con las mismas
   métricas. **Requiere GPU.**

## Cómo abrirlos

En [Colab](https://colab.research.google.com), pestaña **GitHub**, pegar
`resagri-fiuba/Deteccion-De-Fracturas-ETRR` y elegir el notebook.
Se clonan el repositorio solos, así que siempre corren con la última versión del código.

## Una diferencia de estilo, a propósito

En `curso/` el código está escrito **dentro** del notebook, a la vista: acá lo que se
mira es lo que hay que aprender. En `notebooks/` (el proyecto real) la lógica vive en
`src/` y el notebook solo la llama, que es como se trabaja de verdad.
