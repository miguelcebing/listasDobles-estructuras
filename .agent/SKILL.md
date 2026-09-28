---
name: doubly-linked-list-workshop
description: Construye un taller completo de LISTAS DOBLES (doubly linked lists) en Python con frontend HTML, aplicado a un caso de estudio real; por defecto "MetroLine", una línea de metro con estaciones y un tren que avanza y retrocede. Genera la estructura propia con nodos prev/next, una API Flask, una interfaz clara e innovadora con panel de punteros, pruebas con assert y guía de sustentación. Usa esta skill siempre que el usuario mencione listas dobles, listas doblemente enlazadas, doubly linked list, taller de estructuras de datos, caso de estudio con Python y frontend, o pida un proyecto académico donde se vea una lista con puntero anterior y siguiente, incluso si no dice "skill" ni "metro". Also use it for any request to build a Python + HTML demo of a doubly linked list (undo/redo, browser history, route navigation, slideshow, etc.), but never a music player unless explicitly requested.
---

# Taller de listas dobles: Python + Frontend

Esta skill guía la construcción de un proyecto académico completo: una **lista doblemente enlazada** implementada a mano en Python, aplicada a un **caso de estudio de la vida real**, con un **frontend HTML** que hace visible la estructura de datos.

El enunciado que origina esta skill dice, en esencia: *"Seleccione un caso de estudio de la vida real donde pueda aplicar el concepto y manejo de listas dobles. El script debe ser realizado en Python y debe tener Frontend."* Todo lo que sigue existe para cumplir esa frase sin ambigüedad y para que el estudiante pueda **sustentarlo** (explicarlo en voz alta) con seguridad.

## Por qué esta skill es como es

Un taller de listas dobles se evalúa principalmente por tres cosas: que la estructura sea **realmente** una lista doble (no una `list` de Python disfrazada), que el caso de estudio **justifique** el uso de `prev` y `next`, y que el estudiante **entienda** el código. Por eso la skill insiste en código sencillo, comentarios que expliquen los punteros y una interfaz que muestre los punteros en pantalla. Un proyecto vistoso pero con una `list` por debajo, o con código que el estudiante no puede explicar, falla el objetivo aunque se vea bien.

## Cuándo aplicar cada decisión

- **Caso de estudio por defecto: MetroLine** (línea de metro). Encaja de forma natural: el tren avanza y retrocede (`next`/`prev`), se agregan y cierran estaciones, y se puede invertir el sentido de la línea.
- Si el usuario propone **otro caso** (historial del navegador, deshacer/rehacer de un editor, carrusel de diapositivas, ruta de un bus, galería de fotos), conserva la arquitectura completa y cambia solo el modelo de datos y el vocabulario. Ver la sección "Adaptar a otro caso".
- **Evita reproductores de música** salvo que el usuario los pida: es el ejemplo más repetido en este tipo de talleres y suele restar originalidad.
- Si el usuario no especifica idioma, escribe la **explicación en el idioma del usuario** y el **código (nombres, comentarios, docstrings, mensajes de la API) en inglés**.

## Flujo de trabajo

Sigue este orden; cada paso deja una base verificable para el siguiente.

1. **Confirmar el caso y el alcance en una línea.** Si el usuario ya eligió el caso, no lo cuestiones. Si no, propone MetroLine.
2. **Crear `linked_list.py` y `test_linked_list.py`.** Ejecutar las pruebas. No avanzar hasta que pasen: todo lo demás depende de que la lista sea correcta.
3. **Crear `seed_data.py` y `app.py`** con la API. Probar cada ruta.
4. **Crear el frontend** (`templates/index.html`, `static/style.css`, `static/app.js`) con la paleta y estructura descritas abajo.
5. **Conectar y pulir**: animaciones, estados vacíos, mensajes de error.
6. **Verificar contra la lista de aceptación** y entregar los archivos con `present_files`, junto con instrucciones de ejecución en pocas líneas.
7. **Ofrecer la guía de sustentación** (sección final), porque es lo que el estudiante realmente necesitará frente al docente.

Estructura de entrega:

```
metroline/
├── requirements.txt          # solo: flask
├── app.py                    # servidor Flask + rutas
├── linked_list.py            # Node y DoublyLinkedList (corazón del taller)
├── seed_data.py              # estaciones de ejemplo
├── test_linked_list.py       # pruebas con assert, sin frameworks
├── templates/index.html
└── static/
    ├── style.css
    └── app.js
```

Ejecución: `pip install -r requirements.txt`, luego `python app.py` y abrir `http://127.0.0.1:5000`.

## Reglas de código Python (nivel NO avanzado)

El estudiante debe poder leer y defender cada línea. Por eso:

- Todo en **inglés**: variables, funciones, clases, comentarios, docstrings, mensajes.
- Nombres largos y descriptivos (`add_at_end`, no `ae`).
- Funciones de unas 20 líneas como máximo; una función, una tarea.
- Herramientas permitidas: clases simples, `if/elif/else`, `while`, `for`, diccionarios y listas **solo para devolver datos** al frontend.
- Evitar: `lambda` complejas, comprensiones anidadas, decoradores propios, `__slots__`, genéricos, herencia múltiple, y especialmente `deque`, `list.insert` o `list.remove` para almacenar los nodos.
- Comentar el **porqué** de cada paso de punteros, porque eso es lo que se sustenta.
- Errores mediante valores de retorno claros (`None`, `True/False`), sin jerarquías de excepciones.

## Implementación de referencia: `linked_list.py`

Usa esta base (adáptala, no la copies a ciegas si el caso cambia). Los pasos de punteros son el núcleo académico: conserva sus comentarios.

```python
class Node:
    """One station of the metro line."""

    def __init__(self, name, zone):
        self.name = name      # station name, e.g. "Central Market"
        self.zone = zone      # fare zone: 1, 2 or 3
        self.prev = None      # link to the previous station
        self.next = None      # link to the next station


class DoublyLinkedList:
    """A metro line stored as a doubly linked list."""

    def __init__(self):
        self.head = None      # first station
        self.tail = None      # last station
        self.current = None   # where the train is now
        self.size = 0

    def find(self, name):
        """Return the node with this name (ignoring case) or None."""
        node = self.head
        while node is not None:
            if node.name.lower() == name.lower():
                return node
            node = node.next
        return None

    def add_at_start(self, name, zone):
        """Add a station before the head. Return the node or None if duplicated."""
        if self.find(name) is not None:
            return None
        new_node = Node(name, zone)
        if self.head is None:                 # empty line: node is head and tail
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.next = self.head         # new node points forward to old head
            self.head.prev = new_node         # old head points back to new node
            self.head = new_node
        self.size += 1
        return new_node

    def add_at_end(self, name, zone):
        """Add a station after the tail. Return the node or None if duplicated."""
        if self.find(name) is not None:
            return None
        new_node = Node(name, zone)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail         # new node points back to old tail
            self.tail.next = new_node         # old tail points forward to new node
            self.tail = new_node
        self.size += 1
        return new_node

    def add_after(self, target_name, name, zone):
        """Insert a station right after target_name. Return node or None."""
        target = self.find(target_name)
        if target is None or self.find(name) is not None:
            return None
        new_node = Node(name, zone)
        new_node.prev = target                # 1. new node looks back at target
        new_node.next = target.next           # 2. new node looks forward at target's old next
        if target.next is not None:
            target.next.prev = new_node       # 3. old next now looks back at new node
        else:
            self.tail = new_node              # target was the last station
        target.next = new_node                # 4. target now looks forward at new node
        self.size += 1
        return new_node

    def remove(self, name):
        """Remove a station. Return True if it existed."""
        node = self.find(name)
        if node is None:
            return False
        if node.prev is not None:
            node.prev.next = node.next        # skip over the removed node going forward
        else:
            self.head = node.next             # removed node was the head
        if node.next is not None:
            node.next.prev = node.prev        # skip over the removed node going backward
        else:
            self.tail = node.prev             # removed node was the tail
        if self.current is node:              # never leave the train on a deleted node
            self.current = node.next if node.next is not None else node.prev
        self.size -= 1
        return True

    def move_next(self):
        """Move the train forward. Return the new current node or None at the end."""
        if self.current is None or self.current.next is None:
            return None
        self.current = self.current.next
        return self.current

    def move_previous(self):
        """Move the train backward. Return the new current node or None at the start."""
        if self.current is None or self.current.prev is None:
            return None
        self.current = self.current.prev
        return self.current

    def go_to(self, name):
        """Place the train at a station. Return True if it exists."""
        node = self.find(name)
        if node is None:
            return False
        self.current = node
        return True

    def reverse(self):
        """Reverse the direction of the whole line by swapping prev and next."""
        node = self.head
        while node is not None:
            node.prev, node.next = node.next, node.prev
            node = node.prev                  # after the swap, the old "next" is now "prev"
        self.head, self.tail = self.tail, self.head

    def node_to_dict(self, node, index):
        """Convert a node into plain data for the frontend."""
        return {
            "name": node.name,
            "zone": node.zone,
            "prev_name": node.prev.name if node.prev is not None else None,
            "next_name": node.next.name if node.next is not None else None,
            "is_current": node is self.current,
            "index": index,
        }

    def to_list_forward(self):
        """Walk head -> tail using next."""
        result = []
        node = self.head
        index = 0
        while node is not None:
            result.append(self.node_to_dict(node, index))
            node = node.next
            index += 1
        return result

    def to_list_backward(self):
        """Walk tail -> head using prev (this proves prev works)."""
        result = []
        node = self.tail
        index = self.size - 1
        while node is not None:
            result.append(self.node_to_dict(node, index))
            node = node.prev
            index -= 1
        return result
```

Casos borde que siempre deben quedar cubiertos: lista vacía, un solo nodo, eliminar `head`, eliminar `tail`, eliminar el nodo donde está el tren, nombres duplicados, mover el tren en los extremos.

### Complejidad (incluirla en la explicación al estudiante)

| Operación | Costo |
|-----------|-------|
| Agregar al inicio o al final | O(1), gracias a `head` y `tail` |
| Insertar tras una estación dada / eliminar | O(n) por la búsqueda, O(1) el reenlace |
| Mover el tren siguiente / anterior | O(1) |
| Buscar por nombre | O(n) |
| Invertir la línea | O(n) |

La ventaja frente a una lista simple: retroceder y eliminar un nodo conocido no requiere recorrer desde el inicio.

## API (`app.py`, Flask)

Una sola instancia global `metro_line = DoublyLinkedList()`, cargada con `seed_data.py` (por ejemplo: North Terminal, University, Central Market, City Hall, Riverside, Airport Link). Toda respuesta es JSON con la forma:

```json
{ "ok": true, "message": "Station added", "line": { "size": 6, "current": "Central Market", "head": "North Terminal", "tail": "Airport Link", "stations": [] } }
```

| Método | Ruta | Cuerpo | Acción |
|--------|------|--------|--------|
| GET | `/` | — | Sirve `index.html` |
| GET | `/api/line` | — | Estado completo |
| POST | `/api/stations` | `{name, zone, position: "start"\|"end"\|"after", after}` | Agrega |
| DELETE | `/api/stations/<name>` | — | Elimina |
| GET | `/api/stations/search?name=` | — | Busca y devuelve vecinos |
| POST | `/api/train/next` · `/api/train/previous` | — | Mueve el tren |
| POST | `/api/train/goto` | `{name}` | Salta a una estación |
| POST | `/api/line/reverse` | — | Invierte la línea |
| GET | `/api/line/backward` | — | Recorrido tail → head |

Validaciones: nombre no vacío (máx. 30 caracteres), zona de 1 a 3, sin duplicados. Errores como `{"ok": false, "message": "..."}` con HTTP 400 o 404. **El estado vive en Python**; el frontend solo pinta lo que recibe, porque si JavaScript reordenara la lista por su cuenta, la lista doble dejaría de ser la protagonista.

## Frontend: claro, aireado y con estructura no convencional

La idea de diseño: en lugar de la típica tabla más formulario, **la línea de metro es el eje visual de toda la pantalla** y la estructura de datos se *ve*.

### Paleta (colores claros, variables CSS)

```css
:root {
  --bg:         #F6F9FC;  /* page background */
  --surface:    #FFFFFF;  /* cards */
  --ink:        #1F2A44;  /* main text */
  --ink-soft:   #6B7A99;  /* secondary text */
  --line-mint:  #7FE0C3;  /* metro line, primary accent */
  --line-sky:   #8EC5FF;  /* "next" pointers */
  --line-lilac: #C3B1FF;  /* "prev" pointers */
  --line-peach: #FFC9A8;  /* current station / train */
  --danger-soft:#FFB3B3;  /* remove actions */
  --shadow: 0 10px 30px rgba(31, 42, 68, 0.08);
  --radius: 20px;
}
```

Fondo nunca oscuro, sombras suaves, bordes muy redondeados, texto `--ink` sobre fondos claros para mantener buen contraste. Tipografía: Poppins o Nunito (Google Fonts) con `sans-serif` de respaldo, y JetBrains Mono para el panel de punteros. La página debe abrir bien sin internet.

### Estructura de la pantalla

1. **Header**: nombre, subtítulo ("Doubly linked list in action") y contador de estaciones.
2. **La Línea** (zona principal, cerca de la mitad de la altura): trazo horizontal grueso en `--line-mint`, estaciones como círculos con nombre y zona, la actual resaltada en `--line-peach` con un tren que se desliza con `transition`. Entre estaciones, dos flechas finas: **azul →** (`next`) y **lila ←** (`prev`). Scroll horizontal suave si hay muchas estaciones; en móvil la línea pasa a vertical.
3. **Mandos del tren** (barra flotante centrada): `◀ Previous`, `Next ▶`, selector "Go to…" y `⇄ Reverse line`. Los botones se atenúan en `head` y `tail`.
4. **Zona inferior en dos columnas**: a la izquierda "Line control" (formulario para agregar con posición inicio/final/después de…, buscador, y un botón `✕` por estación para eliminar); a la derecha "Memory view".
5. **Toasts** arriba a la derecha con el campo `message` de la API.

### Panel "Memory view" (lo que lo hace innovador y académico)

Muestra el nodo seleccionado o actual como si fuera su representación en memoria:

```
┌─────────────────────────────────┐
│ prev ← "University"             │  chip lila, clic = seleccionar ese nodo
│ data   "Central Market" · zone 2│
│ next → "City Hall"              │  chip azul, clic = seleccionar ese nodo
└─────────────────────────────────┘
head: North Terminal   tail: Airport Link   size: 6
```

Al pasar el cursor sobre una estación, el panel se actualiza. Debajo, pestañas **Forward** y **Backward** con el recorrido como chips; Backward existe para demostrar que `prev` funciona. Cuando un puntero es `None`, mostrar un chip gris "None". Este panel es lo que permite al estudiante señalar en pantalla cómo cambian los punteros durante una inserción.

### Animaciones y reglas técnicas

- Estación nueva: "pop" (escala 0.8 → 1) con destello mint. Eliminada: se desvanece y la línea se cierra. Tren: `transition: transform 0.6s ease`. Invertir: giro suave de 0.5 s antes de repintar.
- Respetar `prefers-reduced-motion`.
- HTML semántico, `<label>` en formularios, `aria-label` en botones de solo icono.
- JavaScript simple y sin frameworks: `fetch`, `async/await` básico y una función `renderLine(data)` que repinta todo desde el JSON.
- Sin librerías externas salvo Google Fonts. Responsive en 360, 768 y 1280 px como mínimo.

## Pruebas: `test_linked_list.py`

Con `assert`, ejecutable con `python test_linked_list.py`, que al final imprima `All tests passed`. Cubrir: orden forward y backward tras varias inserciones; inserción al inicio, al final y en medio con `size`, `head` y `tail` correctos; eliminación de `head`, `tail` y nodo intermedio; eliminación del nodo donde está el tren; movimiento en los extremos devolviendo `None`; `reverse()` aplicado dos veces recupera el orden original; lista vacía sin errores; duplicados rechazados. Una buena verificación adicional: el recorrido backward debe ser exactamente el forward invertido.

## Adaptar a otro caso de estudio

La arquitectura no cambia; cambian el modelo y el vocabulario. Guía rápida:

| Caso | Nodo guarda | `prev` / `next` significan | Acciones equivalentes |
|------|-------------|---------------------------|----------------------|
| Historial de navegador | URL, título | página anterior / siguiente | visitar (corta el futuro), atrás, adelante |
| Deshacer / rehacer | acción, texto | estado anterior / siguiente | ejecutar, undo, redo |
| Carrusel de diapositivas | título, imagen | diapositiva anterior / siguiente | insertar, mover, eliminar |
| Ruta de bus | parada, hora | parada anterior / siguiente | avanzar, retroceder, invertir sentido |

Al adaptar, justifica en una frase por qué el caso *necesita* recorrer en ambos sentidos; si no lo necesita, no es un buen caso para listas dobles.

## Lista de aceptación

Antes de entregar, confirma cada punto:

- [ ] Las estaciones existen **solo** como nodos enlazados con `prev` y `next`.
- [ ] Todas las operaciones del `DoublyLinkedList` funcionan y sus pruebas pasan.
- [ ] Desde el frontend se puede mover el tren, agregar (inicio, final, intermedio), eliminar, buscar e invertir.
- [ ] "Memory view" muestra `prev`, `data`, `next`, `head`, `tail` y `size` correctos tras cada acción.
- [ ] Código Python en inglés, sencillo y comentado.
- [ ] Diseño claro con la paleta indicada; sin desbordes en móvil.
- [ ] `pip install -r requirements.txt` + `python app.py` levantan el proyecto sin pasos extra.

## Guía de sustentación (entregar siempre al final)

Ofrece al estudiante un guion de unos 3 minutos: (1) el problema, un tren que se mueve en ambos sentidos; (2) la clase `Node` y qué significan `prev` y `next`; (3) demostración de una inserción en medio señalando en "Memory view" los cuatro punteros que cambian; (4) eliminación de un nodo intermedio y por qué no hace falta recorrer desde el inicio; (5) comparación con una lista simple. Redáctalo en el idioma del usuario y con lenguaje que pueda decir con sus propias palabras.

## Fuera de alcance

Bases de datos, autenticación, varios usuarios, frameworks de frontend (React, Vue), mapas reales o cálculo de tarifas. El objetivo es **entender y demostrar las listas dobles**, no construir un sistema de producción; añadir esas piezas solo distrae de lo que se evalúa.
