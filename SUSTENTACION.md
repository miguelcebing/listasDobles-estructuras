# Guía de sustentación — MetroLine (3 minutos)

Un guion que puedes decir con tus propias palabras frente al docente. Reloj en mano: son unos 3 minutos.

---

## 1. El problema (20 segundos)

> "Mi caso de estudio es una **línea de metro**. El tren debe recorrer las estaciones **hacia adelante y hacia atrás**: ir a la siguiente estación o volver a la anterior. Además, la administración puede abrir estaciones nuevas (al inicio, al final o en medio de la línea), cerrar estaciones y hasta invertir el sentido de toda la línea.
>
> Eso es justamente lo que necesita una **lista doble**: moverse en ambos sentidos. Con una lista simple, para retroceder tendría que recorrer la lista desde el inicio cada vez."

## 2. La estructura: `Node`, `prev` y `next` (30 segundos)

> "Todo se guarda en la clase `Node`. Cada nodo tiene sus datos —`name` y `zone`— y **dos punteros**:
>
> - **`next`** apunta a la estación **siguiente**.
> - **`prev`** apunta a la estación **anterior**.
>
> La clase `DoublyLinkedList` mantiene tres referencias: **`head`** (primera estación), **`tail`** (última) y **`current`**, que es **dónde está el tren ahora**. Ojo: las estaciones se guardan **solo** como nodos enlazados, no uso `list` ni `deque` de Python."

*(Señala `linked_list.py` en pantalla.)*

## 3. Demostración: inserción en medio (50 segundos)

> "Voy a insertar una estación después de *Central Market*. Muestren el **Memory view** mientras hablas — aquí se ven los cuatro punteros que cambian, que es el corazón de la operación:
>
> 1. `new_node.prev = target` — el nodo nuevo **mira hacia atrás** a *Central Market*.
> 2. `new_node.next = target.next` — el nodo nuevo **mira hacia adelante** a lo que era el siguiente (*City Hall*).
> 3. `target.next.prev = new_node` — *City Hall* ahora **mira hacia atrás** al nodo nuevo.
> 4. `target.next = new_node` — *Central Market* ahora **mira hacia adelante** al nodo nuevo.
>
> Solo reasigné **cuatro punteros** y la estación quedó en su lugar. Si la lista tuviera mil estaciones, estos pasos serían igual de rápidos: la parte lenta es únicamente **buscar** el nodo, el reenlace es O(1)."

*(Hazlo en la interfaz: posiciones → "After…" → añade una estación y apunta a la tarjeta de memoria.)*

## 4. Eliminación de un nodo intermedio (40 segundos)

> "Ahora elimino una estación del medio. El nodo se 'salta' a sus dos lados:
>
> 1. `node.prev.next = node.next` — el anterior **atraviesa** el nodo eliminado hacia adelante.
> 2. `node.next.prev = node.prev` — el siguiente **atraviesa** el nodo eliminado hacia atrás.
>
> **No hace falta recorrer desde el inicio** para encontrar al anterior: ya lo tengo en `node.prev`. Esa es la ventaja que da el puntero `prev`.
>
> También hay dos detalles importantes: si la estación eliminada era `head` o `tail`, actualizo esos punteros; y si ahí estaba el tren, lo muevo a una estación vecina para que nunca quede apuntando a un nodo fuera de la lista."

## 5. Comparación con una lista simple (20 segundos)

> "Con una **lista simple**:
>
> - Retroceder obligaría a recorrer desde el inicio: **O(n)** en vez de **O(1)**.
> - Para eliminar un nodo del medio necesitaría buscar **antes** su predecesor; con lista doble, `prev` me lo da directo.
>
> La única operación cara en mi lista doble es **buscar por nombre** (O(n)), porque no tengo índice. Pero una vez encontrado el nodo, reenlazar es O(1)."

---

## Recorrido rápido de la interfaz (si te lo piden)

1. **Flechas ◀ ▶ / Go to…** → el tren se mueve; los botones se desactivan en `head` y `tail`.
2. **Line control** → agregar (inicio / final / después de…), buscar y eliminar (✕).
3. **Memory view** → pasa el cursor por una estación: se ven `prev`, `data`, `next`, y abajo `head`, `tail`, `size`.
4. **Pestaña Backward** → demuestra en pantalla que `prev` recorre la lista completa al revés.
5. **⇄ Reverse line** → se invierte la línea cambiando `prev`↔`next` en cada nodo.

## Respuestas a preguntas típicas

| Pregunta | Respuesta corta |
|----------|-----------------|
| ¿Por qué no usar `list.append`? | Porque la lista tendría que ser **nodos enlazados reales**; una `list` de Python haría trampa el taller y perdería los punteros `prev`/`next`. |
| ¿Qué pasa si la lista está vacía? | `head`, `tail` y `current` son `None`; todas las operaciones devuelven `None`/`False` sin lanzar errores (lo cubre la prueba de lista vacía). |
| ¿Y si elimino la estación donde está el tren? | El código reubica `current` en el siguiente o, si no hay, en el anterior. |
| ¿Cuánto cuesta `reverse()`? | O(n): recorre la lista una vez intercambiando `prev`↔`next` y luego cambia `head`↔`tail`. |
| ¿Y los nombres duplicados? | Se rechazan: `find()` antes de insertar y devuelve `None`. |
