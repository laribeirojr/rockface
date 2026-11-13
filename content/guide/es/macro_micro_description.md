# Descripción macroscópica y microscópica

## Para qué sirve

La pestaña **Macroscópica** registra lo que se ve en la muestra de mano o en el testigo: estructuras, textura, color
y fábrica. La pestaña **Microscópica** registra lo que se ve en la lámina: estructuras, el intervalo granulométrico y
sus modas, selección, forma de los granos, fábrica, los contactos intergranulares y el empaquetamiento. RockFace
comprueba cada valor con su escala, de modo que el texto y los números de una descripción nunca discrepan.

## Antes de empezar

Una descripción abierta (página [Proyectos y descripciones](projects_descriptions.md)). Las listas vienen de la base de conocimiento (página
[Nomenclatura, escalas y referencias (la base de conocimiento)](nomenclature_knowledge_base.md)).

## Paso a paso

### Macroscópica

1. Abra la pestaña **Macroscópica**.
2. **Estructuras** — hasta tres (**Estructura 1–3**), cada una con su **Extensión (%)** en la muestra.
3. **Textura** — **Tamaño de grano modal** (Udden–Wentworth), **Tamaño de cristal** (Folk 1962, para rocas
   cristalinas), **Selección**, **Redondez** (Powers) y **Esfericidad**.
4. **Color** — el **Código Munsell** (por ejemplo `5YR 6/4` o `N7`) y el **Nombre del color**.
5. **Fábrica** — **Orientación** y **Soporte**.
6. **Notas** y luego **Guardar** (Ctrl+S).

### Microscópica

1. Abra la pestaña **Microscópica**.
2. **Estructuras** — hasta tres, con su extensión.
3. **Tamaño de grano**
   * **Intervalo granulométrico**: la clase **Más fino** y la **Más grueso**.
   * **Modas**: la **Moda principal** y hasta tres más (**Segunda**, **Tercera**, **Cuarta moda**), cada una como clase
     o como tamaño en **mm**. Cuando se escribe un tamaño, su clase se completa.
   * **Grava (%)**, **Arena (%)** y **Lodo (%)**, con el total mostrado al lado.
4. **Selección y forma de los granos** — **Selección** como clase o como **σI (φ)** (Folk y Ward 1957); **Redondez**,
   el **Intervalo de redondez** y los **Modificadores de redondez**; **Esfericidad**; **Tamaño de cristal**;
   **Orientación** y **Soporte**.
5. **Contactos y empaquetamiento**
   * **Contactos, del más abundante (%)** — hasta cinco tipos de contacto (puntual, largo, cóncavo-convexo, suturado,
     flotante) con su porcentaje.
   * Para el empaquetamiento de Kahn (1956): cuente, a lo largo de una traversa, **Todos los contactos de la traversa**
     de los granos cruzados y cuántos son **Contactos grano–grano**; RockFace muestra la **Proximidad de
     empaquetamiento (Kahn)** y su clase (suelto, normal, cerrado). Mida los **Interceptos de granos (mm)** y la
     **Longitud de la traversa (mm)** para la **Densidad de empaquetamiento (Kahn)**.
   * **Ayuda de empaquetamiento…** abre la ayuda visual de las clases de empaquetamiento (página
     [McBride, Bramkamp & Powers y las clases de empaquetamiento](classifications_packing.md)).
6. **Notas** y luego **Guardar**.

## Opciones

| Campo | Regla |
|---|---|
| Estructuras | Como máximo tres, sin repetir; una extensión necesita una estructura; 0–100 %. |
| Modas | Como máximo cuatro; la moda principal primero; cada una dentro del intervalo granulométrico. |
| Intervalo granulométrico | El extremo más fino primero. |
| σI (φ), tamaños modales | Un número prevalece sobre la clase: cuando discrepan, la clase se actualiza, con un mensaje. |
| Grava + arena + lodo | Debe sumar 100 % (se guarda igual, con un aviso). |
| Contactos | Como máximo cinco, sin repetir, sumando como máximo 100 %. |
| Contactos grano–grano | No más que todos los contactos. |

## Cómo funciona

* La granulometría sigue la escala de Udden–Wentworth (Wentworth 1922) con el φ de Krumbein (1934); la selección, la
  desviación estándar gráfica inclusiva de Folk y Ward (1957); la redondez, las clases de Powers (1953); el tamaño de
  cristal, Folk (1962).
* "El número prevalece": un valor en milímetros o en φ es la medida, y la clase se deriva de él.
* Proximidad de empaquetamiento P = contactos grano–grano ÷ todos los contactos × 100; densidad de empaquetamiento =
  intercepto total de los granos ÷ longitud de la traversa × 100 (Kahn 1956). Clases: suelto por debajo de 40, normal
  de 40 a 55, cerrado por encima de 55.

## Desde un script

```python
d = prj["TS-9"]
d.micro.sorting_phi = 0.62               # σI de Folk y Ward; la clase sigue al guardar
d.micro.grain_contacts, d.micro.total_contacts = 38, 80
print(d.micro.packing_proximity, d.micro.packing_class)       # 47.5 normal
d.macro.colour_code = "5Y 7/2"
d.save()                                 # comprobado exactamente como en los formularios
```

## Límites y problemas comunes

* "«…» no está en notación Munsell (por ejemplo 5YR 6/4 o N7)."
* "Intervalo granulométrico: el primer extremo es mayor que el segundo."
* "Se indicaron modas secundarias sin la moda principal." / "… está fuera del intervalo indicado."
* "Tamaño de grano modal: 0,3 corresponde a arena media; el número prevalece y la clase se actualizó." — un mensaje, no
  un error.

## Cobertura

P11 (descripción macroscópica), P12 (estructuras y granulometría microscópicas), P13 (selección y forma), P14
(contactos y empaquetamiento).
