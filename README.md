# Portería 506

Sistema de gestión de paquetes para la portería de una unidad residencial de **3 bloques y 506 apartamentos**.
Proyecto integrador de Estructuras de Datos (ITM, 2026-2).

En la versión de Fundamentos de Programación los paquetes se guardaban en una lista de diccionarios, y para
encontrar una guía había que recorrerla toda. En esta versión cada tarea de la portería tiene su propia
estructura de datos, programada desde cero (sin usar `list` ni `dict` de Python para guardar los datos).

## Qué hace

1. **Llega el camión:** los paquetes se descargan en una **cola** y se atienden en el orden de llegada.
2. **Se registra cada paquete** en su apartamento. El apartamento se encuentra directo en la **matriz** del bloque.
   El paquete queda en la **lista** de pendientes del apartamento y en el **árbol** de guías.
3. **Buscar por guía:** el árbol baja comparando guías, sin recorrer los 506 apartamentos.
4. **Entregar:** solo a un residente autorizado del apartamento. Cada entrega queda en el **historial** (lista doble)
   y en la **pila** de deshacer.
5. **Deshacer:** la última entrega vuelve a pendientes y sale del historial.
6. **Guardar y cargar** todo en archivos CSV.

## Estructuras

| Estructura | Archivo | Para qué se usa | Costo de la operación principal |
|---|---|---|---|
| `Arreglo` (desde cero) | `arreglo.py` | Base de los arreglos de residentes, pisos y bloques | Acceso por posición O(1) |
| Matriz de apartamentos | `unidad.py` | Llegar a un apartamento por su número: `divmod(1204, 100) = (12, 4)` | O(1) |
| Lista enlazada | `recepcion.py` | Paquetes pendientes de cada apartamento | Agregar al final O(1) |
| Cola | `recepcion.py` | El camión: primero en llegar, primero en registrarse | Encolar y desencolar O(1) |
| Árbol binario de búsqueda | `Arbol.py` | Buscar un paquete por número de guía | O(altura) ≈ O(log n) |
| Lista doblemente enlazada | `historial.py` | Historial de entregas, recorrible en los dos sentidos | Agregar y quitar el último O(1) |
| Pila | `deshacer.py` | Deshacer la última entrega | Apilar y desapilar O(1) |

Además hay 4 tipos de paquete con herencia y una clase abstracta (`paquetes.py`), una jerarquía de excepciones
propias (`excepciones.py`) y la lectura y escritura de CSV (`archivos.py`).

## Cómo correrlo

Usa solo la librería estándar de Python. La gráfica del experimento necesita matplotlib, que ya viene con Spyder.

```bash
python interfaz.py     # ventana de la portería (tkinter)
python demo.py         # recorrido por consola
python pruebas.py      # 94 pruebas automáticas
python experimento.py  # comparación de búsquedas por guía
```

Los datos de ejemplo están en `datos/` (`bloques.csv`, `residentes.csv` y `paquetes.csv`). Al guardar desde la
interfaz se escribe en `datos/`; el demo guarda en `datos_guardados/`.

## Pruebas

`pruebas.py` revisa cada parte por separado: excepciones, arreglo, paquetes, lista de pendientes, cola, unidad,
camión, archivos, árbol, historial y deshacer. Debe terminar en **94 pruebas bien, 0 mal**.

## Experimento

`experimento.py` mide el tiempo promedio de 1000 búsquedas por guía con 500, 2000 y 8000 paquetes pendientes
repartidos al azar, de tres formas:

- **FP (lista de diccionarios):** recorre la lista completa.
- **ED (matriz):** recorre los 506 apartamentos y la lista de cada uno.
- **ED (árbol):** baja por el árbol comparando guías.

Resultado de una corrida (microsegundos; cambian según el computador):

| Paquetes | FP lista | ED matriz | ED árbol | Altura del árbol |
|---|---|---|---|---|
| 500 | 30,2 | 360,1 | 6,7 | 19 |
| 2000 | 107,3 | 614,8 | 8,3 | 26 |
| 8000 | 430,4 | 2304,5 | 10,3 | 32 |

Con 16 veces más paquetes, el árbol solo tarda 1,5 veces más, porque su altura crece como un logaritmo. La matriz
es la más lenta para buscar por guía porque recorre todo, pero es la mejor para llegar a un apartamento.
La gráfica queda en `experimento.png`.

## Equipo

| Integrante | Parte |
|---|---|
| Sara Gaviria Giraldo | Árbol binario de búsqueda por guía (`Arbol.py`), arreglo y excepciones |
| Verónica Roca Moreno | Historial con lista doblemente enlazada (`historial.py`) y su conexión con la unidad y los archivos |
| Valentina Castaño Saldarriaga | Paquetes y recepción, pila para deshacer (`deshacer.py`) e interfaz gráfica (`interfaz.py`) |
| Enrique Almanza Saucedo | Integración de las partes, reparación, pruebas, experimento y documentación |
