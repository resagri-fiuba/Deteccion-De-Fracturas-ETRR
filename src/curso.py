"""
curso.py — Funciones de apoyo para los notebooks del curso.

Los notebooks de `curso/` usan CIFAR-10 (gatos) para enseñar el mismo problema
que después vamos a resolver con radiografías. Este módulo tiene solo lo
repetitivo: descargar, graficar, medir. La lógica que hay que APRENDER está
escrita a la vista dentro de los notebooks, a propósito.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROJO = "#C8401F"     # la clase positiva (gato / fractura)
AZUL = "#1B6B87"     # la clase negativa
GRIS = "#6B7A87"

CLASES_CIFAR = ["avión", "auto", "pájaro", "gato", "ciervo",
                "perro", "rana", "caballo", "barco", "camión"]
GATO = 3             # índice de la clase "gato" en CIFAR-10


# ---------------------------------------------------------------------------
# 1. Datos
# ---------------------------------------------------------------------------

def cargar_cifar10(raiz: str | Path = "datos"):
    """Descarga CIFAR-10 y lo devuelve como arrays de numpy.

    Devuelve (X_ent, y_ent, X_test, y_test) donde X tiene forma
    (n, 32, 32, 3) con enteros 0–255, e y tiene los índices de clase 0–9.

    CIFAR-10: 60.000 fotos de 32x32 px, 10 clases, 6.000 por clase.
    Público, anónimo y liviano (~170 MB). Creado por Krizhevsky, Nair y Hinton.
    """
    from torchvision import datasets      # se importa acá para no exigirlo siempre

    raiz = Path(raiz)
    raiz.mkdir(parents=True, exist_ok=True)

    ent = datasets.CIFAR10(root=str(raiz), train=True, download=True)
    test = datasets.CIFAR10(root=str(raiz), train=False, download=True)

    return (np.array(ent.data), np.array(ent.targets),
            np.array(test.data), np.array(test.targets))


def a_binario(y: np.ndarray, clase: int = GATO) -> np.ndarray:
    """Convierte las 10 clases en un problema de sí/no: 1 = la clase elegida."""
    return (y == clase).astype(int)


def aplanar_y_normalizar(X: np.ndarray) -> np.ndarray:
    """De (n, 32, 32, 3) enteros 0–255 a (n, 3072) decimales 0–1.

    Es lo que necesitan los modelos clásicos de scikit-learn, que no entienden
    de imágenes: para ellos cada píxel es una columna más de una tabla.
    """
    return X.reshape(len(X), -1).astype("float32") / 255.0


# ---------------------------------------------------------------------------
# 2. Mirar
# ---------------------------------------------------------------------------

def grilla(X, y=None, filas=4, columnas=8, titulo=None, guardar=None):
    """Muestra imágenes en una grilla. Si y es binario, pinta el borde."""
    n = min(len(X), filas * columnas)
    fig, ejes = plt.subplots(filas, columnas, figsize=(columnas * 1.3, filas * 1.5))
    ejes = np.array(ejes).reshape(-1)

    for i, eje in enumerate(ejes):
        eje.set_xticks([]); eje.set_yticks([])
        if i >= n:
            eje.axis("off")
            continue
        eje.imshow(X[i])
        if y is not None:
            positivo = bool(y[i])
            color = ROJO if positivo else AZUL
            eje.set_title("GATO" if positivo else "no", fontsize=7,
                          color=color, pad=2)
            for lado in eje.spines.values():
                lado.set_color(color)
                lado.set_linewidth(1.8)

    if titulo:
        fig.suptitle(titulo, fontsize=12)
    fig.tight_layout()
    if guardar:
        Path(guardar).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(guardar, dpi=120, bbox_inches="tight")
    return fig


# ---------------------------------------------------------------------------
# 3. Medir
# ---------------------------------------------------------------------------

def matriz_confusion(y_real, y_pred, guardar=None):
    """Dibuja la matriz de confusión con los cuatro números y sus nombres."""
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y_real, y_pred)
    vn, fp, fn, vp = cm.ravel()

    fig, eje = plt.subplots(figsize=(4.6, 4.2))
    eje.imshow(cm, cmap="Blues", alpha=.65)

    etiquetas = [[f"Verdaderos\nnegativos\n{vn:,}", f"Falsos\npositivos\n{fp:,}"],
                 [f"Falsos\nnegativos\n{fn:,}", f"Verdaderos\npositivos\n{vp:,}"]]
    for i in range(2):
        for j in range(2):
            eje.text(j, i, etiquetas[i][j], ha="center", va="center", fontsize=10)

    eje.set_xticks([0, 1], ["dijo: no", "dijo: SÍ"])
    eje.set_yticks([0, 1], ["era: no", "era: SÍ"])
    eje.set_title("Matriz de confusión", fontsize=12)
    fig.tight_layout()
    if guardar:
        Path(guardar).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(guardar, dpi=120, bbox_inches="tight")
    return fig


def informe(y_real, y_pred, y_score=None, nombre="modelo") -> dict:
    """Imprime y devuelve las métricas que importan con clases desbalanceadas."""
    from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                                 f1_score, roc_auc_score, average_precision_score,
                                 confusion_matrix)

    vn, fp, fn, vp = confusion_matrix(y_real, y_pred).ravel()
    m = {
        "modelo": nombre,
        "accuracy": accuracy_score(y_real, y_pred),
        "precision": precision_score(y_real, y_pred, zero_division=0),
        "recall": recall_score(y_real, y_pred, zero_division=0),
        "f1": f1_score(y_real, y_pred, zero_division=0),
    }
    if y_score is not None:
        m["roc_auc"] = roc_auc_score(y_real, y_score)
        m["pr_auc"] = average_precision_score(y_real, y_score)

    print(f"── {nombre} " + "─" * max(0, 46 - len(nombre)))
    print(f"  Accuracy   {m['accuracy']:.3f}   de cada 100 imágenes, acierta {m['accuracy']*100:.0f}")
    print(f"  Recall     {m['recall']:.3f}   de cada 100 gatos REALES, encuentra {m['recall']*100:.0f}")
    print(f"  Precisión  {m['precision']:.3f}   de cada 100 veces que dice GATO, acierta {m['precision']*100:.0f}")
    print(f"  F1         {m['f1']:.3f}   el equilibrio entre las dos anteriores")
    if y_score is not None:
        print(f"  ROC-AUC    {m['roc_auc']:.3f}")
        print(f"  PR-AUC     {m['pr_auc']:.3f}   la métrica honesta cuando hay desbalance")
    print(f"  Se le escapan {fn:,} gatos y da {fp:,} falsas alarmas.")
    return m


def curvas(y_real, y_score, guardar=None):
    """Dibuja la curva ROC y la curva precisión-recall, una al lado de la otra."""
    from sklearn.metrics import (roc_curve, precision_recall_curve,
                                 roc_auc_score, average_precision_score)

    fpr, tpr, _ = roc_curve(y_real, y_score)
    prec, rec, _ = precision_recall_curve(y_real, y_score)
    base = float(np.mean(y_real))

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.3))

    a1.plot(fpr, tpr, color=AZUL, linewidth=2)
    a1.plot([0, 1], [0, 1], color=GRIS, linestyle="--", linewidth=1)
    a1.set_title(f"ROC — AUC {roc_auc_score(y_real, y_score):.3f}", fontsize=11)
    a1.set_xlabel("falsas alarmas (1 − especificidad)")
    a1.set_ylabel("gatos encontrados (recall)")

    a2.plot(rec, prec, color=ROJO, linewidth=2)
    a2.axhline(base, color=GRIS, linestyle="--", linewidth=1)
    a2.text(.02, base + .02, f"azar = {base:.2f}", color=GRIS, fontsize=9)
    a2.set_title(f"Precisión–Recall — AUC {average_precision_score(y_real, y_score):.3f}",
                 fontsize=11)
    a2.set_xlabel("recall")
    a2.set_ylabel("precisión")

    for a in (a1, a2):
        a.set_xlim(-.02, 1.02); a.set_ylim(-.02, 1.02)
        a.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    if guardar:
        Path(guardar).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(guardar, dpi=120, bbox_inches="tight")
    return fig


def umbral_para_recall(y_real, y_score, recall_minimo=0.90):
    """Devuelve el umbral más alto que todavía alcanza el recall pedido.

    En medicina esta es LA decisión: primero se fija cuántos casos positivos
    se está dispuesto a dejar pasar, y recién después se mira qué precisión
    queda. El umbral 0,5 que viene por omisión no tiene nada de especial.
    """
    from sklearn.metrics import precision_recall_curve

    prec, rec, umb = precision_recall_curve(y_real, y_score)
    # precision_recall_curve devuelve un umbral menos que puntos
    validos = [(u, p, r) for u, p, r in zip(umb, prec[:-1], rec[:-1])
               if r >= recall_minimo]
    if not validos:
        return 0.0, 0.0, 1.0
    u, p, r = max(validos, key=lambda t: t[0])
    print(f"Con umbral {u:.3f}: recall {r:.3f}, precisión {p:.3f}")
    return u, p, r


# ---------------------------------------------------------------------------
# 4. Redes neuronales (notebook curso/02)
# ---------------------------------------------------------------------------
# Estas funciones aparecen escritas a mano dentro del notebook 02 la primera
# vez, para que se entienda qué hace cada línea. Acá quedan empaquetadas para
# poder reusarlas sin repetir treinta líneas en cada experimento.

def dispositivo():
    """Devuelve la GPU si hay, y si no la CPU."""
    import torch
    d = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Usando: {d}" + (f"  ({torch.cuda.get_device_name(0)})" if d == "cuda" else ""))
    return torch.device(d)


def a_tensores(X, y, tamano_lote=128, mezclar=False):
    """De arrays de numpy a un DataLoader de PyTorch.

    Dos conversiones que hay que hacer sí o sí:
      - de (n, alto, ancho, canales) a (n, canales, alto, ancho), que es el
        orden que espera PyTorch;
      - de enteros 0–255 a decimales 0–1.
    """
    import torch
    from torch.utils.data import TensorDataset, DataLoader

    Xt = torch.tensor(X, dtype=torch.float32).permute(0, 3, 1, 2) / 255.0
    yt = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
    return DataLoader(TensorDataset(Xt, yt), batch_size=tamano_lote, shuffle=mezclar)


def entrenar(modelo, dl_ent, dl_val, epocas=8, lr=1e-3, peso_positivos=None,
             disp=None, verbose=True):
    """Entrena y devuelve el historial de pérdidas. Es el bucle de siempre.

    peso_positivos: cuánto pesa más un gato que un no-gato en la pérdida.
        Con 10% de positivos, un valor de 9 equilibra las clases. Es la forma
        más simple de que el modelo no se conforme con decir "no" a todo.
    """
    import torch
    from torch import nn

    disp = disp or dispositivo()
    modelo = modelo.to(disp)

    pw = None if peso_positivos is None else torch.tensor([peso_positivos], device=disp)
    criterio = nn.BCEWithLogitsLoss(pos_weight=pw)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=lr)

    historial = {"ent": [], "val": []}

    for ep in range(1, epocas + 1):
        # --- entrenamiento ---
        modelo.train()
        suma = 0.0
        for xb, yb in dl_ent:
            xb, yb = xb.to(disp), yb.to(disp)
            salida = modelo(xb)                 # 1. predecir
            perdida = criterio(salida, yb)      # 2. medir el error
            optimizador.zero_grad()             # 3. borrar gradientes viejos
            perdida.backward()                  # 4. calcular gradientes
            optimizador.step()                  # 5. corregir los pesos
            suma += perdida.item() * len(xb)
        historial["ent"].append(suma / len(dl_ent.dataset))

        # --- validación (sin aprender) ---
        modelo.eval()
        suma = 0.0
        with torch.no_grad():
            for xb, yb in dl_val:
                xb, yb = xb.to(disp), yb.to(disp)
                suma += criterio(modelo(xb), yb).item() * len(xb)
        historial["val"].append(suma / len(dl_val.dataset))

        if verbose:
            print(f"época {ep:>2}/{epocas}   "
                  f"pérdida entrenamiento {historial['ent'][-1]:.4f}   "
                  f"validación {historial['val'][-1]:.4f}")
    return historial


def predecir(modelo, dl, disp=None):
    """Devuelve (scores, etiquetas reales) como arrays de numpy."""
    import torch

    disp = disp or next(modelo.parameters()).device
    modelo.eval()
    scores, reales = [], []
    with torch.no_grad():
        for xb, yb in dl:
            s = torch.sigmoid(modelo(xb.to(disp)))   # de logit a probabilidad
            scores.append(s.cpu().numpy())
            reales.append(yb.numpy())
    return np.concatenate(scores).ravel(), np.concatenate(reales).ravel()


def curva_entrenamiento(historial, titulo="Curva de entrenamiento", guardar=None):
    """Grafica las dos pérdidas. Cuando la de validación sube y la de
    entrenamiento sigue bajando, el modelo empezó a memorizar."""
    fig, eje = plt.subplots(figsize=(6.4, 4))
    ep = range(1, len(historial["ent"]) + 1)
    eje.plot(ep, historial["ent"], color=AZUL, marker="o", ms=4, label="entrenamiento")
    eje.plot(ep, historial["val"], color=ROJO, marker="o", ms=4, label="validación")
    eje.set_xlabel("época"); eje.set_ylabel("pérdida")
    eje.set_title(titulo, fontsize=12); eje.legend()
    eje.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if guardar:
        Path(guardar).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(guardar, dpi=120, bbox_inches="tight")
    return fig
