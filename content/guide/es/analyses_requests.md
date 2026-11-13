# Análisis y solicitudes de análisis

## Para qué sirve

La pestaña **Análisis** guarda los resultados de laboratorio de la muestra — petrofísica, DRX, MEB, isótopos,
química, bioestratigrafía — con sus imágenes. La pestaña **Solicitudes** pide al laboratorio nuevos análisis y los
sigue hasta que están listos. Ambas pertenecen a la **muestra**: todas las descripciones de las láminas de la muestra
las muestran.

## Antes de empezar

Una descripción **guardada**: los análisis y solicitudes pertenecen a su muestra ("Guarde primero la descripción: los
análisis y solicitudes pertenecen a su muestra.").

## Paso a paso

### Añadir un análisis

1. Abra la pestaña **Análisis**. Su título nombra la muestra.
2. **Añadir análisis…**
3. Elija el **Análisis**: petrofísica convencional, petrofísica especial, DRX (roca total o fracción arcilla), MEB
   (electrones secundarios o retrodispersados), isótopos estables (C, O), isótopos de estroncio, química o
   bioestratigrafía.
4. Complete el **Laboratorio**, la **Fecha (aaaa-mm-dd)** y los resultados. Los campos siguen el tipo:
   * petrofísica convencional — **Porosidad** (%), **Permeabilidad** (mD), **Densidad de grano** (g/cm³);
   * isótopos estables — **δ13C** y **δ18O** (‰ VPDB); estroncio — **87Sr/86Sr**;
   * DRX — una tabla de **Mineral** y **%** (**Añadir fila**, **Quitar fila**);
   * química — una tabla de **Elemento o compuesto**, **Valor** y **Unidad**;
   * petrofísica especial — el **Método**; bioestratigrafía — **Biozona**, **Edad** y **Fósiles**;
   * **Notas** para lo demás.
5. En **Imágenes y archivos**, **Añadir imagen…** (imágenes de MEB, difractogramas, cromatogramas); **Exportar…**
   guarda una de vuelta en un archivo.
6. **Aceptar**. La lista muestra el tipo, el laboratorio, la fecha, un resumen de los resultados y el número de
   imágenes. **Editar…** y **Eliminar** actúan sobre el análisis seleccionado.

### Solicitar un análisis

1. Abra la pestaña **Solicitudes** y luego **Nueva solicitud…**
2. Elija el **Análisis**. La **Sugerencia** dice qué indica un buen objetivo para ese tipo.
3. Escriba el **Objetivo** (obligatorio): qué pregunta debe responder el análisis.
4. **Estado**: Solicitada, En curso, Concluida o Cancelada. Cámbielo a medida que avanza el trabajo.
5. **Notas** e imágenes (por ejemplo una foto del área a muestrear), y luego **Aceptar**.

La lista muestra el tipo, el objetivo, el estado, cuándo se solicitó y quién.

## Opciones

| Campo | Regla |
|---|---|
| Fecha | aaaa-mm-dd, aaaa-mm o aaaa. |
| Porosidad, permeabilidad, densidad de grano | 0–100 %, 0–100 000 mD, 1,5–5,0 g/cm³. |
| δ13C, δ18O | −50 a 50 ‰ VPDB; 87Sr/86Sr 0,69–0,80. |
| Filas de DRX | Cada mineral con nombre; los porcentajes deben sumar 100 (se guarda igual, con un aviso). |

## Cómo funciona

Los análisis y solicitudes se guardan con la muestra; así, la porosidad de un plug se escribe una vez y aparece en
todas las descripciones de ese plug. Entran en los informes, los archivos de intercambio, las consultas de Explorer
(petrofísica, isótopos, DRX) y su panel (porosidad × permeabilidad, densidad de grano). Las imágenes quedan dentro del
proyecto. Los análisis de rutina de testigo de un informe de laboratorio en PDF pueden leerse para las muestras de un
pozo por la profundidad (Inicio → **Importar informe de laboratorio (PDF)…**, página [Archivos de los programas de referencia](file_formats.md)).

## Desde un script

```python
d = prj["TS-9"]
d.add_analysis("conventional_petrophysics", laboratory="ILLUSTRATIVE lab", date="2026-03-02",
               values={"porosity": 18.2, "permeability": 245.0, "grain_density": 2.65})
d.add_analysis("xrd_whole_rock", rows=[{"mineral": "Cuarzo", "percent": 71}, {"mineral": "Calcita", "percent": 29}],
               pictures=["drx.png"])
d.add_request("stable_isotopes", "δ13C y δ18O del cemento de calcita, para fechar el agua que lo formó")
for a in d.analyses():
    print(a["kind"], a["values"], a["rows"])
print([r["status"] for r in d.requests()])
```

## Límites y problemas comunes

* "Elija el tipo de análisis." / "Indique el objetivo de la solicitud."
* "… debe estar entre … y …": un valor fuera del intervalo plausible de su tipo.
* "El análisis aún no tiene resultados." — un aviso: el análisis se guarda vacío.
* Se rechazan las imágenes más grandes que el límite de adjuntos del proyecto.

## Cobertura

P15 (análisis adicionales), P16 (solicitudes de análisis con imágenes).
