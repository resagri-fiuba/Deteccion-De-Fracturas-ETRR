# Chuleta de Git y GitHub

Versión corta y offline del manual, para tener dentro del propio repositorio.
El manual completo (con diagramas y explicaciones) está en la página del proyecto.

---

## Preparar la máquina (una sola vez)

```bash
git config --global user.name  "Nombre Apellido"
git config --global user.email "usuario@etrr.edu.ar"
git config --global init.defaultBranch main
```

Autenticación: la contraseña de GitHub **no** sirve para `git push`.
Lo más simple es instalar [GitHub CLI](https://cli.github.com) y correr:

```bash
gh auth login        # elegir "Login with a web browser"
```

---

## El ciclo diario

```bash
git pull                          # SIEMPRE al empezar
# ... editar archivos ...
git status                        # ¿qué cambió?
git diff                          # ¿qué cambió, línea por línea?
git add -A                        # preparar
git commit -m "Mensaje claro"     # sacar la foto
git push                          # subir
```

**Regla de oro:** `pull` antes de empezar, `push` antes de irse.

---

## Mensajes de commit

El mensaje tiene que completar la frase *"si aplico este commit, va a…"*.

| Mal | Bien |
|---|---|
| `cambios` | `Agrego la mediana al histograma` |
| `asd` | `Corrijo el error de rutas en Windows` |
| `subo todo` | `Semana 3: ResNet18, AUC 0.83 en validación` |

Si el commit resuelve un issue, agregá `closes #12` al final y se cierra solo.

---

## Ramas y pull requests

```bash
git switch main && git pull              # 1. partir de main actualizada
git switch -c joaco/histograma-mediana   # 2. crear la rama
# ... trabajar, add, commit ...
git push -u origin joaco/histograma-mediana   # 3. subir la rama
gh pr create --fill                      # 4. abrir el pull request
# 5. otro integrante revisa y aprueba → Merge
git switch main && git pull              # 6. volver
git branch -d joaco/histograma-mediana   # 7. limpiar
```

### Protocolo del equipo

- Nadie commitea directo en `main`. Nunca.
- Una rama por tarea, nombrada `quien/que-hace`.
- Todo entra a `main` por pull request, aprobado por otra persona.
- El que aprueba tiene que entender el cambio; si no, pregunta en el PR.
- `main` siempre tiene que andar.

---

## Conflictos

Git deja las dos versiones marcadas en el archivo:

```
<<<<<<< HEAD
lo que hay en tu rama actual
=======
lo que trae la otra rama
>>>>>>> nombre-de-la-otra-rama
```

1. Editar el archivo y dejar la versión correcta (borrando las tres líneas de marcas).
2. `git add archivo`
3. `git commit`

Para cancelar todo y volver atrás: `git merge --abort`.

> **Notebooks:** los `.ipynb` generan conflictos ilegibles porque guardan las salidas
> adentro. Por eso en este proyecto la lógica vive en `src/*.py` y el notebook solo llama
> a esas funciones.

---

## Cuando algo sale mal

| Situación | Comando |
|---|---|
| Descartar cambios de un archivo | `git restore archivo.py` |
| Sacar algo del área de preparación | `git restore --staged archivo.py` |
| Corregir el último commit (no subido) | `git commit --amend` |
| Deshacer el último commit local | `git reset --soft HEAD~1` |
| Anular un commit ya subido | `git revert <hash>` |
| Guardar cambios a medias | `git stash` … `git stash pop` |
| `! [rejected] non-fast-forward` | `git pull` y volver a pushear |
| `detached HEAD` | `git switch main` |
| Hice un desastre | `git reflog` y `git reset --hard <hash>` |

**Dos reglas:**

- Si todavía es local → `reset`. Si ya lo subiste → `revert`.
- `--hard` borra de verdad. Antes de escribirlo, `git status`.

`git reflog` guarda todos los movimientos de los últimos 90 días, incluso de
commits "borrados". Casi cualquier error se deshace desde ahí.

---

## Lo que nunca se sube

Ya está configurado en el `.gitignore` de este repositorio:

- Datos e imágenes del dataset (`datos/`)
- Modelos entrenados (`modelos/*.pt`)
- Contraseñas, tokens y claves (`.env`, `*.key`)
- Basura del lenguaje y del sistema (`__pycache__/`, `.venv/`, `.DS_Store`)

> Si alguna vez suben una contraseña, borrarla no alcanza: queda en la historia.
> Hay que **invalidar esa clave y generar una nueva**, inmediatamente.

---

## Equivalencias con interfaz gráfica

| Terminal | GitHub Desktop | VS Code |
|---|---|---|
| `git pull` | Botón "Pull origin" | Ícono de sincronizar |
| `git add` | Tildar la casilla del archivo | El `+` al lado del archivo |
| `git commit -m` | Escribir resumen + "Commit" | Mensaje + Ctrl+Enter |
| `git push` | Botón "Push origin" | Ícono de sincronizar |
| `git log` | Pestaña "History" | Extensión Git Graph |
