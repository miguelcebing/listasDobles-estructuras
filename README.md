# MetroLine 🚇 — Taller de Listas Dobles

Proyecto académico que aplica el concepto de **lista doblemente enlazada** (*doubly linked list*) a un caso de estudio de la vida real: **una línea de metro** con estaciones y un tren que avanza y retrocede.

> Enunciado: *"Seleccione un caso de estudio de la vida real donde pueda aplicar el concepto y manejo de LISTAS DOBLES. El script debe ser realizado en PYTHON y debe tener Frontend."*

## ¿Por qué una lista doble?

Una línea de metro es una secuencia ordenada de estaciones donde el tren necesita moverse en **ambos sentidos**:

- **Avanzar** (`next`) y **retroceder** (`prev`) en O(1). Con una lista simple, retroceder obligaría a recorrer desde el inicio.
- **Eliminar** una estación cerrada sin buscar al vecino: `node.prev.next = node.next`.
- **Insertar** una estación entre dos solo reasigna cuatro punteros.
- **Invertir** el sentido de la línea intercambiando `prev` y `next` en cada nodo.

```
 head                                              tail
  ▼                                                  ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  North   │  │University│  │ Central  │  │ Airport  │
│ Terminal │  │          │  │ Market   │  │  Link    │
│ prev:None │←→│prev:North│←→│prev:Univ │←→│prev:C.Mkt│
│ next:Univ │  │next:C.Mkt│  │next:Airp │  │next:None │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
      ▲                           ▲
      └── el tren (current) ──────┘
```

## Requisitos

- Python 3.10 o superior
- Flask (se instala con el comando de abajo)

## Instalación y ejecución

```bash
pip install -r requirements.txt
python app.py
```

Abre **http://127.0.0.1:5000** en tu navegador.

## Pruebas

```bash
python test_linked_list.py
```

Debe imprimir `All tests passed`. Las pruebas cubren inserciones, eliminaciones (head/tail/medio/nodo actual), extremos del tren, doble inversión, lista vacía, duplicados y la verificación de que el recorrido **backward es exactamente el forward invertido**.

## Estructura del proyecto

```
listasDobles-Estructuras/
├── requirements.txt          # solo: flask
├── app.py                    # servidor Flask + rutas de la API
├── linked_list.py            # Node y DoublyLinkedList (el corazón del taller)
├── seed_data.py              # estaciones de ejemplo para arrancar
├── test_linked_list.py       # pruebas con assert (sin frameworks)
├── templates/
│   └── index.html            # frontend
├── static/
│   ├── style.css             # diseño (paleta clara, responsive)
│   └── app.js                # conexión con la API + Memory view
├── SUSTENTACION.md           # guía de sustentación (3 minutos)
└── .agent/                   # especificaciones originales del taller
```

## Cómo funciona

### 1. El corazón: `linked_list.py`

- **`Node`**: cada estación guarda `name`, `zone` y dos punteros: `prev` (estación anterior) y `next` (siguiente).
- **`DoublyLinkedList`**: mantiene `head` (primera), `tail` (última), `current` (posición del tren) y `size`.

Las estaciones se guardan **únicamente** como nodos enlazados — no se usa `list` ni `deque` de Python para almacenarlas.

| Método | Qué hace | Devuelve |
|--------|----------|----------|
| `find(name)` | Busca por nombre (ignora mayúsculas) | `Node` o `None` |
| `add_at_start` / `add_at_end` | Agrega al inicio / final | `Node` o `None` (duplicado) |
| `add_after(target, ...)` | Inserta después de una estación | `Node` o `None` |
| `remove(name)` | Elimina una estación | `True` / `False` |
| `move_next` / `move_previous` | Mueve el tren | `Node` o `None` en los extremos |
| `go_to(name)` | Salta a una estación | `True` / `False` |
| `reverse()` | Invierte el sentido de la línea | — |
| `to_list_forward` / `to_list_backward` | Recorrido head→tail y tail→head | lista de diccionarios |

### 2. El servidor: `app.py` (Flask)

Una sola instancia global `metro_line` guarda todo el estado **en Python**. El frontend solo pinta lo que recibe.

| Método | Ruta | Acción |
|--------|------|--------|
| GET | `/` | Página del frontend |
| GET | `/api/line` | Estado completo de la línea |
| POST | `/api/stations` | Agrega estación (`start` / `end` / `after`) |
| DELETE | `/api/stations/<name>` | Elimina estación |
| GET | `/api/stations/search?name=` | Busca y devuelve la estación con sus vecinos |
| POST | `/api/train/next` · `/api/train/previous` | Avanza / retrocede el tren |
| POST | `/api/train/goto` | Salta a una estación |
| POST | `/api/line/reverse` | Invierte la línea |
| GET | `/api/line/backward` | Recorrido tail→head (demuestra que `prev` funciona) |

Toda respuesta tiene la forma:

```json
{ "ok": true, "message": "Station added", "line": { "size": 7, "current": "Central Market", "head": "North Terminal", "tail": "Airport Link", "stations": [] } }
```

Los errores responden `{"ok": false, "message": "..."}` con HTTP 400 o 404 (nombre vacío o >30 caracteres, zona fuera de 1–3, duplicados, estación inexistente).

### 3. El frontend

- **La línea** es el eje visual de la pantalla: estaciones como círculos, el tren sobre la actual, y flechas **azul → (`next`)** / **lila ← (`prev`)** entre estaciones para que la bidireccionalidad sea visible.
- **Memory view**: al pasar el cursor sobre una estación se muestra su nodo como si estuviera en memoria:

  ```
  prev ← "University"              (chip lila, clic = ir a ese nodo)
  data   "Central Market" · zone 2
  next → "City Hall"               (chip azul, clic = ir a ese nodo)
  head: North Terminal   tail: Airport Link   size: 7
  ```

  Con las pestañas **Forward** y **Backward** se comprueba que `prev` recorre la lista completa en sentido inverso.
- El estado **siempre vive en el servidor**: JavaScript nunca reordena la lista por su cuenta.

## Complejidad

| Operación | Costo |
|-----------|-------|
| Agregar al inicio o al final | O(1) gracias a `head` y `tail` |
| Insertar tras una estación / eliminar | O(n) la búsqueda, O(1) el reenlace |
| Mover el tren siguiente / anterior | O(1) |
| Buscar por nombre | O(n) |
| Invertir la línea | O(n) |

**La ventaja frente a una lista simple:** retroceder y eliminar un nodo conocido no requiere recorrer desde el inicio.

## Fuera de alcance

Bases de datos, autenticación, varios usuarios, frameworks de frontend (React, Vue), mapas reales o cálculo de tarifas. El objetivo es **entender y demostrar las listas dobles**.

## Sustentación

Prepara tu explicación de 3 minutos con la guía en **[SUSTENTACION.md](SUSTENTACION.md)**.
