# RockFace Explorer: el panel de una colección

## Para qué sirve

La pestaña **Panel** muestra una colección de un vistazo: las muestras por facies, la porosidad frente a la
permeabilidad, la densidad de grano, las profundidades muestreadas en cada pozo, los tipos de muestra y galerías de
las imágenes (mosaicos PP y XP, láminas de escáner, fotos de detalle, mapas mineralógicos). Los filtros por campo,
formación, zona, pozo, facies y categoría de imagen estrechan todos los gráficos a la vez.

## Antes de empezar

Un proyecto con descripciones, de preferencia con petrofísica (pestaña Análisis, página [Análisis y solicitudes de análisis](analyses_requests.md)) e
imágenes (RockFace Atlas).

## Paso a paso

1. En RockFace Explorer, abra la pestaña **Panel**.
2. Los gráficos:
   * **Muestras por facies (clic para filtrar)** — un mapa de árbol; haga clic en una facies para quedarse solo con
     ella;
   * **Porosidad × permeabilidad (mD)** — un punto por muestra, coloreado por facies, permeabilidad en eje
     logarítmico;
   * **Densidad de grano** — un histograma;
   * **Profundidades por pozo** — las profundidades **Medida (tope)**, **Corregida** y **Ajustada** de las muestras de
     cada pozo;
   * **Tipos de muestra** — plugs, testigos enteros, testigos laterales, recortes de perforación, muestras de
     afloramiento.
3. **Filtros**: marque valores de **Campo**, **Formación**, **Zona**, **Pozo**, **Facies** y **Categoría de imagen**;
   todos los gráficos y galerías los siguen. "N de M muestras". **Limpiar filtros** los quita.
4. **Solo las descripciones de la consulta** limita el panel a las descripciones encontradas en la pestaña Consulta.
5. **Galerías**: **Mosaico PP**, **Mosaico XP**, **Escáner**, **Fotos de detalle**, **Mineralogía (mapas)**. Haga
   doble clic en una imagen para abrirla en RockFace Atlas.

## Opciones

| Opción | Qué cambia |
|---|---|
| Filtros | Todos los gráficos y galerías muestran solo las muestras que coinciden. |
| Solo las descripciones de la consulta | El panel del resultado de la consulta. |

## Cómo funciona

El panel lee los mismos hechos que las consultas: la petrofísica viene de los análisis de petrofísica convencional de
cada muestra; la facies, el campo, la formación, la zona y el pozo, de la identificación; las galerías, de las
imágenes Atlas de cada lámina (por categoría y luz). El mapa de árbol es "squarified" (el área de cada rectángulo es
el número de muestras).

## Desde un script

```python
board = prj.dashboard(field="Example Field A")
print(board.facies())                    # muestras por facies
for phi, k, facies, did in board.phi_k():
    print(phi, k, facies)
print(board.grain_density(10), board.depths(), board.sample_types())
print(board.gallery("mosaic_pp"))        # ids de las imágenes
```

## Límites y problemas comunes

* "Sin datos para las descripciones mostradas." — ninguna petrofísica o ninguna imagen entre las muestras filtradas.
* Una muestra sin facies aparece bajo "—".

## Cobertura

L1 (paneles), Q2 (conceptos de petrofísica en la colección).
