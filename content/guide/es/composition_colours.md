# Color de las líneas seleccionadas (composición)

## Para qué sirve

Counterledge permite al petrógrafo colorear líneas de la tabla de composición para encontrarlas rápido durante el
conteo. En RockFace las líneas seleccionadas reciben un color a través de su grupo.

## Paso a paso

1. **Petro → Composición**: seleccione una o más líneas.
2. **Color de las líneas seleccionadas…** y elija el color.

## Cómo funciona

Las líneas pasan a compartir un grupo (el que ya comparten, o uno nuevo) y el color del grupo las pinta; desagrupar lo
quita. El color se guarda con la composición.

## Desde un script

```python
d = prj["ILL-TS-001"]; d.composition.groups   # {"g1": {"name": …, "colour": "#123456"}}
```

## Cobertura

Counterledge C2 (Configure Selected Row Color).
