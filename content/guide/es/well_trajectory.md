# Trayectoria del pozo

## Para qué sirve

En un pozo desviado, la muestra está a una profundidad medida (MD) que no es su profundidad vertical (TVD), ni queda
justo debajo de la boca del pozo. **Trayectoria del pozo** lee el levantamiento direccional y da a cada muestra su
TVD, su profundidad bajo el nivel del mar, sus desplazamientos norte y este, y su latitud y longitud.

## Antes de empezar

* El pozo en el proyecto (Identificación), con latitud y longitud de la boca para la posición geográfica.
* Un archivo de levantamiento: profundidad medida, inclinación y azimut (CSV, texto o LAS).

## Paso a paso

1. **Petro → Inicio → Trayectoria del pozo…**
2. Elija el pozo; escriba la elevación del datum de profundidad sobre el nivel del mar y la referencia del norte.
3. **Leer un levantamiento…** y elija el archivo. Las estaciones aparecen con TVD, norte, este y severidad del dogleg.
4. **Muestras**: cada muestra del pozo en la trayectoria. **Planta y sección**: la vista en planta y la sección
   vertical, con las muestras en rojo.

## Opciones

| Campo | Significado |
|---|---|
| Datum de profundidad | elevación del datum (mesa rotaria, kelly bushing) sobre el nivel del mar: TVDSS = TVD − datum |
| Referencia del norte | verdadero, de cuadrícula o magnético, como el levantamiento da los azimuts (registrado, no convertido) |
| Columnas | MD / Depth / Prof., Inc / Incl / Devi, Azi / Azim / Hazi, en cualquier orden; coma, punto y coma, tabulación o espacios |

## Cómo funciona

Mínima curvatura (Bourgoyne et al. 1986; Sawaryn & Thorogood 2005): entre dos estaciones el pozo sigue el arco de un
círculo; ΔN, ΔE y ΔTVD son las semisumas de los cosenos directores por ΔMD, por el factor RF = (2/β)·tan(β/2), β el
dogleg. Una muestra entre estaciones queda en el mismo arco. Latitud y longitud salen de la boca por los radios de
curvatura de WGS 84 (plano tangente local).

## Desde un script

```python
st = prj.survey("ILL-WELL-1", "levantamiento.csv", datum_elevation_m=25.0)
st[-1].tvd, st[-1].north, st[-1].east
rf.trajectory.sample_position(prj.raw, sample_id)     # {'tvd': …, 'tvdss': …, 'latitude': …, …}
```

## Límites y problemas comunes

* Por encima de la primera estación el pozo se toma como vertical; por debajo de la última, mantiene la última
  dirección (marcado como *extrapolado*).
* Los azimuts magnéticos no se corrigen por la declinación: conviértalos antes o elija la referencia que corresponde.

## Cobertura

P8 (ubicación de la muestra: posición geográfica, profundidad y trayectoria del pozo).
