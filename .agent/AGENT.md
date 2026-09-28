# AGENT.md — Taller de LISTAS DOBLES: "MetroLine"

> Instrucciones para el agente (o desarrollador) que construirá el proyecto.
> Léelo completo antes de escribir código. Cada decisión de este documento existe para cumplir el enunciado del taller.

---

## 1. Enunciado del taller (fuente de verdad)

> *"Seleccione un caso de estudio de la vida real donde pueda aplicar el concepto y manejo de **LISTAS DOBLES**. El script debe ser realizado en **PYTHON** y debe tener **Frontend**."*

Requisitos derivados y verificables:

| # | Requisito | Cómo se cumple en este proyecto |
|---|-----------|--------------------------------|
| R1 | Caso de estudio de la vida real | Línea de metro / transporte masivo con estaciones y un tren que avanza y retrocede |
| R2 | Uso real de **listas dobles** | Estructura propia `DoublyLinkedList` con nodos `prev` / `next`, **sin usar `list` ni `deque` de Python para almacenar las estaciones** |
| R3 | Script en **Python** | Lógica y servidor en Python 3.10+ |
| R4 | **Frontend** | Página HTML con diseño claro, servida por Flask y conectada a la lógica por una API JSON |
| R5 | Código en inglés y **no avanzado** | Nombres en inglés, funciones cortas, sin decoradores propios, sin metaclases, sin genéricos complejos |
| R6 | No es un reproductor de música | El caso elegido es transporte público (los reproductores son el ejemplo más repetido; se evita a propósito) |

---

## 2. Caso de estudio: "MetroLine"

### 2.1 Descripción

Una línea de metro es una **secuencia ordenada de estaciones**. Un tren recorre la línea en ambos sentidos: puede ir a la **siguiente** estación o volver a la **anterior**. La administración puede **agregar** una estación nueva (al inicio, al final o entre dos estaciones existentes), **eliminar** una estación cerrada, **buscar** una estación y **invertir** el sentido completo de la línea.

### 2.2 ¿Por qué una lista doble es la estructura correcta?

- **Movimiento bidireccional natural.** Un tren necesita ir a `next` y volver a `prev` en O(1). Con una lista simple, retroceder obligaría a recorrer desde el inicio (O(n)).
- **Eliminación sencilla.** Si tenemos el nodo, conocemos a su vecino anterior sin buscarlo: `node.prev.next = node.next`.
- **Inserción intermedia.** Agregar una estación entre otras dos solo reasigna cuatro punteros.
- **Inversión de sentido.** Basta intercambiar `prev` y `next` en cada nodo (idea muy didáctica para explicar en la sustentación).

### 2.3 Complejidad esperada (incluir en el README de la sustentación)

| Operación | Complejidad |
|-----------|-------------|
| Agregar al inicio / al final | O(1) (se mantienen `head` y `tail`) |
| Insertar después de una estación dada | O(n) por la búsqueda, O(1) el reenlace |
| Eliminar una estación | O(n) por la búsqueda, O(1) el reenlace |
| Mover el tren siguiente / anterior | O(1) |
| Buscar por nombre | O(n) |
| Invertir la línea | O(n) |

---

## 3. Estructura del proyecto

```
metroline/
├── AGENT.md
├── requirements.txt          # solo: flask
├── app.py                    # servidor Flask + rutas de la API
├── linked_list.py            # Node y DoublyLinkedList (el corazón del taller)
├── seed_data.py              # estaciones de ejemplo para arrancar
├── test_linked_list.py       # pruebas simples con assert (sin frameworks)
├── templates/
│   └── index.html            # frontend
└── static/
    ├── style.css
    └── app.js
```

Ejecución esperada:

```bash
pip install -r requirements.txt
python app.py
# abrir http://127.0.0.1:5000
```

---

## 4. Reglas de código Python (nivel NO avanzado, en inglés)

1. **Todo en inglés**: nombres de variables, funciones, clases, comentarios, docstrings y mensajes de la API.
2. Nombres largos y descriptivos (`add_at_end`, no `ae`).
3. Funciones de máximo ~20 líneas. Una función, una tarea.
4. Usar solo: clases simples, `if/elif/else`, `while`, `for`, `return`, diccionarios y listas **únicamente para devolver datos** al frontend.
5. **Prohibido**: `lambda` complejas, comprensiones anidadas, decoradores propios, `__slots__`, `typing.Generic`, herencia múltiple, `deque`, `list.insert`, `list.remove` para guardar las estaciones.
6. Comentarios que expliquen el **porqué** de los pasos de punteros (es lo que se sustenta).
7. Cada método público lleva un docstring de una línea.
8. Manejar errores con valores de retorno claros (`True/False` o `None`), no con jerarquías de excepciones.

---

## 5. Especificación de `linked_list.py`

### 5.1 Nodo

```python
class Node:
    """One station of the metro line."""

    def __init__(self, name, zone):
        self.name = name        # station name, e.g. "Central Park"
        self.zone = zone        # fare zone: 1, 2 or 3
        self.prev = None        # link to the previous station
        self.next = None        # link to the next station
```

### 5.2 Lista doble

Atributos: `head`, `tail`, `current` (posición del tren), `size`.

| Método | Descripción | Devuelve |
|--------|-------------|----------|
| `add_at_start(name, zone)` | Nueva estación al inicio | `Node` |
| `add_at_end(name, zone)` | Nueva estación al final | `Node` |
| `add_after(target_name, name, zone)` | Inserta después de `target_name` | `Node` o `None` si no existe el objetivo |
| `remove(name)` | Elimina la estación | `True` / `False` |
| `find(name)` | Busca por nombre (ignorar mayúsculas) | `Node` o `None` |
| `move_next()` | Tren avanza | `Node` actual o `None` si ya está en `tail` |
| `move_previous()` | Tren retrocede | `Node` actual o `None` si ya está en `head` |
| `go_to(name)` | Coloca el tren en una estación | `True` / `False` |
| `reverse()` | Invierte el sentido de la línea | nada |
| `to_list_forward()` | Recorre de `head` a `tail` y devuelve datos | lista de dicts |
| `to_list_backward()` | Recorre de `tail` a `head` (demuestra `prev`) | lista de dicts |

Cada dict de estación debe tener: `name`, `zone`, `prev_name`, `next_name`, `is_current`, `index`.
Los campos `prev_name` y `next_name` (o `null`) alimentan el **panel de punteros** del frontend (sección 7.4).

### 5.3 Pasos de punteros que el agente DEBE implementar y comentar

**Insertar `new_node` después de `target`:**

```
1. new_node.prev = target
2. new_node.next = target.next
3. if target.next is not None: target.next.prev = new_node
   else: tail = new_node            # target was the last node
4. target.next = new_node
5. size += 1
```

**Eliminar `node`:**

```
1. if node.prev is not None: node.prev.next = node.next
   else: head = node.next           # node was the first
2. if node.next is not None: node.next.prev = node.prev
   else: tail = node.prev           # node was the last
3. if current is node: current = node.next or node.prev
4. size -= 1
```

**Invertir la línea:**

```
node = head
while node is not None:
    swap node.prev and node.next
    node = node.prev                # after the swap, the old "next" is now "prev"
swap head and tail
```

Casos borde obligatorios: lista vacía, un solo nodo, eliminar `head`, eliminar `tail`, eliminar el nodo donde está el tren, nombres duplicados (rechazar y devolver `None`).

---

## 6. API (`app.py`, Flask)

Una sola instancia global `metro_line = DoublyLinkedList()`, cargada con `seed_data.py` al iniciar. Todas las respuestas son JSON con esta forma:

```json
{ "ok": true, "message": "Station added", "line": { "size": 6, "current": "Central", "stations": [ ... ] } }
```

| Método | Ruta | Cuerpo | Acción |
|--------|------|--------|--------|
| GET | `/` | — | Sirve `index.html` |
| GET | `/api/line` | — | Estado completo de la línea |
| POST | `/api/stations` | `{name, zone, position: "start"\|"end"\|"after", after: "Name"}` | Agrega estación |
| DELETE | `/api/stations/<name>` | — | Elimina estación |
| GET | `/api/stations/search?name=` | — | Busca y devuelve la estación con sus vecinos |
| POST | `/api/train/next` | — | Avanza |
| POST | `/api/train/previous` | — | Retrocede |
| POST | `/api/train/goto` | `{name}` | Salta a una estación |
| POST | `/api/line/reverse` | — | Invierte la línea |
| GET | `/api/line/backward` | — | Recorrido en reversa (demuestra `prev`) |

Validaciones: nombre no vacío (máx. 30 caracteres), zona entre 1 y 3, nombre no duplicado. Ante error: `{"ok": false, "message": "..."}` con código HTTP 400 o 404.

`seed_data.py` — ejemplo de estaciones iniciales (en inglés): `North Terminal, University, Central Market, City Hall, Riverside, Airport Link`.

---

## 7. Especificación del Frontend

### 7.1 Filosofía de diseño

Claro, aireado y amigable, pero con una **estructura no convencional**: en lugar de la típica tabla + formulario, la línea de metro es el **eje visual de toda la pantalla**. La estructura de datos se *ve*, no solo se lista.

### 7.2 Paleta (colores claros) — definir como variables CSS

```css
:root {
  --bg:           #F6F9FC;   /* page background */
  --surface:      #FFFFFF;   /* cards */
  --ink:          #1F2A44;   /* main text */
  --ink-soft:     #6B7A99;   /* secondary text */
  --line-mint:    #7FE0C3;   /* metro line + primary accent */
  --line-sky:     #8EC5FF;   /* "next" pointers */
  --line-lilac:   #C3B1FF;   /* "prev" pointers */
  --line-peach:   #FFC9A8;   /* current station / train */
  --danger-soft:  #FFB3B3;   /* remove actions */
  --shadow:       0 10px 30px rgba(31, 42, 68, 0.08);
  --radius:       20px;
}
```

Reglas: fondo nunca oscuro, sombras suaves, bordes redondeados grandes, contraste de texto suficiente (texto `--ink` sobre fondos claros). Tipografía sugerida: *Poppins* o *Nunito* (Google Fonts) con `sans-serif` de respaldo, más *JetBrains Mono* para el panel de punteros.

### 7.3 Estructura de la pantalla (de arriba hacia abajo)

1. **Header**: nombre "MetroLine", subtítulo "Doubly linked list in action", contador de estaciones.
2. **La Línea (zona principal, ~50 % de la altura)**
   - Trazo horizontal grueso en `--line-mint` con estaciones como círculos grandes.
   - Cada estación muestra nombre y zona; la actual se resalta en `--line-peach` con un pequeño **tren** (emoji o SVG) encima que se desliza con `transition` al cambiar de estación.
   - Entre estaciones, dos flechas finas superpuestas: **azul →** (`next`) y **lila ←** (`prev`), para que la bidireccionalidad sea visible.
   - Si hay muchas estaciones, la línea hace scroll horizontal suave; en móvil se convierte en línea vertical.
3. **Mandos del tren (barra flotante centrada)**: `◀ Previous`, `Next ▶`, selector "Go to…" y botón `⇄ Reverse line`. Los botones se deshabilitan visualmente en los extremos (`head`/`tail`).
4. **Zona inferior en dos columnas**:
   - **Izquierda — "Line control"**: tarjeta con formulario para agregar estación (nombre, zona, posición: inicio / final / después de…) y buscador. Eliminar se hace con un botón `✕` en cada estación (con confirmación ligera).
   - **Derecha — "Memory view"** (el elemento innovador, ver 7.4).
5. **Toasts** (mensajes breves arriba a la derecha) para éxito y error, tomados del campo `message` de la API.

### 7.4 Panel "Memory view" (cumple el objetivo académico)

Muestra el **nodo seleccionado o actual** como una tarjeta que imita su representación en memoria:

```
┌─────────────────────────────────┐
│ prev ← "University"             │   (chip lila, clic = seleccionar ese nodo)
│ data   "Central Market" · zone 2│
│ next → "City Hall"              │   (chip azul, clic = seleccionar ese nodo)
└─────────────────────────────────┘
head: North Terminal    tail: Airport Link    size: 6
```

- Al pasar el cursor sobre una estación de la línea, el panel se actualiza con sus punteros.
- Debajo, dos pestañas: **Forward** y **Backward**, que muestran el recorrido `head → tail` y `tail → head` como listas de chips. La pestaña Backward existe para *demostrar* que el puntero `prev` funciona.
- Cuando `prev` o `next` son `None`, mostrar el chip `None` en gris.

### 7.5 Interacciones y microanimaciones

- Estación nueva: aparece con "pop" (escala 0.8 → 1) y un destello mint.
- Estación eliminada: se desvanece y la línea se cierra suavemente.
- Movimiento del tren: `transition: transform 0.6s ease`.
- Invertir línea: la línea hace un giro suave (flip horizontal de 0.5 s) antes de repintarse.
- Respetar `prefers-reduced-motion`: desactivar animaciones si el usuario lo pide.

### 7.6 Reglas técnicas del frontend

- HTML semántico (`header`, `main`, `section`, `button`), etiquetas `<label>` en formularios, `aria-label` en botones de solo icono.
- JavaScript **simple y sin frameworks**: `fetch`, `async/await` básico, una función `renderLine(data)` que repinta todo a partir del JSON. El estado vive en el servidor (Python); el frontend nunca reordena la lista por su cuenta.
- Sin librerías externas salvo Google Fonts. Debe abrir sin internet (con las fuentes de respaldo).
- Responsive: 360 px, 768 px y 1280 px como mínimo.

---

## 8. Pruebas (`test_linked_list.py`)

Pruebas con `assert`, ejecutables con `python test_linked_list.py`, que impriman `All tests passed`. Cubrir como mínimo:

1. Agregar al final varias estaciones y verificar el orden forward y backward.
2. Agregar al inicio y en medio; comprobar `size`, `head`, `tail`.
3. Eliminar `head`, `tail` y un nodo intermedio.
4. Eliminar la estación donde está el tren y verificar que `current` no queda apuntando a un nodo fuera de la lista.
5. `move_next()` en `tail` y `move_previous()` en `head` devuelven `None` sin romper nada.
6. `reverse()` dos veces devuelve el orden original.
7. Lista vacía: ninguna operación lanza error.
8. Nombre duplicado rechazado.

---

## 9. Orden de trabajo sugerido para el agente

1. Crear `linked_list.py` y sus pruebas; **no continuar hasta que todas pasen**.
2. Crear `seed_data.py` y `app.py` con la API; probar cada ruta con el navegador o `curl`.
3. Maquetar `index.html` + `style.css` con datos de ejemplo estáticos.
4. Conectar `app.js` con la API y añadir el panel "Memory view".
5. Pulir animaciones, estados vacíos y errores.
6. Revisar la lista de aceptación (sección 10).

---

## 10. Criterios de aceptación

- [ ] Las estaciones se guardan **únicamente** en nodos enlazados con `prev` y `next`.
- [ ] Todas las operaciones de la sección 5.2 funcionan y están probadas.
- [ ] El tren avanza y retrocede desde la interfaz; los extremos se manejan sin errores.
- [ ] Se puede agregar (inicio, final, intermedio), eliminar, buscar e invertir desde el frontend.
- [ ] El panel "Memory view" muestra `prev`, `data`, `next`, `head`, `tail` y `size` correctos tras cada acción.
- [ ] El recorrido Backward coincide exactamente con el Forward invertido.
- [ ] Código Python 100 % en inglés, sencillo y comentado (sección 4).
- [ ] Diseño claro, con la paleta de la sección 7.2 y sin desbordes en móvil.
- [ ] `python app.py` levanta el proyecto sin pasos adicionales tras `pip install -r requirements.txt`.

---

## 11. Guía para la sustentación (opcional, recomendado)

Preparar una explicación de 3 minutos:

1. **Problema**: un tren debe moverse en ambos sentidos.
2. **Estructura**: mostrar la clase `Node` y explicar `prev` / `next`.
3. **Demostración**: insertar una estación en medio y señalar en el "Memory view" cómo cambian cuatro punteros.
4. **Eliminación**: borrar un nodo intermedio y explicar por qué no hace falta recorrer desde el inicio.
5. **Comparación**: qué costaría hacer lo mismo con una lista simple.

---

## 12. Fuera de alcance

Base de datos, autenticación, múltiples usuarios, frameworks de frontend (React, Vue), mapas reales o cálculo de tarifas. El objetivo es **entender y demostrar las listas dobles**, no construir un sistema de producción.