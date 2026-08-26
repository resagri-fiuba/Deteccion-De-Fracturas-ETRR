# Semana 1 — Poner la máquina en marcha

**31 de agosto al 6 de septiembre de 2026**

## Objetivo

Que el entorno ande en las dos máquinas y que hayamos mirado los datos con
nuestros propios ojos. Todavía no hay modelo.

## Tareas

- [ ] Crear el repositorio en GitHub y subir este esqueleto
- [ ] Abrir `notebooks/01_exploracion.ipynb` en Colab desde la pestaña GitHub
- [ ] Pedir GPU en Colab y verificar `nvidia-smi`
- [ ] Instalar el entorno en la PC con GPU y verificar `torch.cuda.is_available()`
- [ ] Descargar FracAtlas y correr el notebook completo
- [ ] Mirar la grilla de 20 radiografías y anotar observaciones en la bitácora
- [ ] Generar `docs/ficha-dataset.md` y subirlo
- [ ] Hacer al menos los ejercicios 1 y 2 del final del notebook

## Criterio de cierre

Se cierra la semana cuando **las cuatro** afirmaciones son verdaderas:

1. El notebook corre de principio a fin sin errores en Colab.
2. El notebook corre de principio a fin sin errores en la PC con GPU.
3. `torch.cuda.is_available()` devuelve `True` en la PC local.
4. `docs/ficha-dataset.md` está en el repositorio con los números reales.

## Conceptos que hay que poder explicar en voz alta

- Qué es un tensor y qué forma tiene un lote de radiografías.
- Por qué un modelo con 82,4% de accuracy en este dataset puede ser inútil.
- Por qué los datos no van al repositorio y el código sí.

## Números que salieron

_(completar al terminar)_

| | |
|---|---|
| Radiografías totales | |
| Proporción con fractura | |
| Accuracy del modelo trivial | |
| Tiempo de descarga en Colab | |
