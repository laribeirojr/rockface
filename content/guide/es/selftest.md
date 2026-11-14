# Autoprueba de una instalación

## Para qué sirve

La autoprueba comprueba, en cerca de un minuto, que RockFace funciona en este equipo: lo que depende del equipo y no
del programa — las bibliotecas, los informes en todos los formatos, los archivos, las figuras, el procesamiento de
imágenes y volúmenes, los modelos de IA, Mio y las cinco ventanas en la pantalla real. Ejecútela después de instalar
y cada vez que algo se comporte de forma extraña; su informe es lo que el equipo de RockFace pide cuando usted
informa un problema.

## Antes de empezar

* Nada que preparar. La autoprueba crea sus propios datos ILUSTRATIVOS en una carpeta temporal y nunca abre, cambia
  ni guarda sus proyectos ni sus preferencias.

## Paso a paso

1. En RockFace Petro: **Ayuda → Ejecutar la autoprueba…**.
2. La ventana lista cada comprobación cuando termina. Los cinco programas se abren y cierran solos: no haga clic en
   ellos.
3. Al final, **Abrir el informe** muestra `report.html` en el navegador, con las imágenes que creó; **Abrir la
   carpeta** muestra la carpeta con `report.html`, `report.json` y `selftest.zip`.
4. Si una comprobación falló, envíe `selftest.zip` con su informe (vea [Enviar su opinión](feedback.md)).

## Opciones

| Dónde | Qué hace |
|---|---|
| `rockface selftest` | Las mismas comprobaciones desde una terminal, sin las ventanas |
| `--gui` | También abre y fotografía las cinco ventanas (Ayuda → Ejecutar la autoprueba… lo hace) |
| `--quick` | Solo el informe HTML entre los formatos de informe |
| `-o CARPETA` | La carpeta del informe (por defecto: una carpeta temporal nueva) |
| `--open` | Abre `report.html` al terminar |

## Cómo funciona

| Parte | Qué se comprueba |
|---|---|
| Instalación | Versión, sistema, edición (con o sin IA), los archivos de licencia |
| Numérica | numpy, SciPy, scikit-image y scikit-learn, con un umbral de respuesta conocida |
| Proyectos | El proyecto de ejemplo ILUSTRATIVO grabado, cerrado y abierto de nuevo; los totales y la clasificación de Folk (1980) |
| Informes | El informe de una descripción en HTML, Word, Excel y PDF |
| Intercambio | Las descripciones exportadas a un archivo `.rfx` e importadas en un proyecto nuevo |
| Figuras | Un diagrama ternario |
| Imágenes | Una lámina sintética con resina azul de porosidad conocida: filtro y segmentación; la porosidad hallada debe quedar a menos de 3 puntos de la dibujada |
| Volúmenes | Un volumen de microtomografía sintético de porosidad conocida: importación y segmentación de Otsu, a menos de 2 puntos |
| IA | El modelo de láminas incluido aplicado a la lámina sintética (edición AI; "no se aplica" en la otra), el dispositivo y si el entrenamiento está disponible |
| Mio | Una pregunta en lenguaje común leída por las reglas |
| Servidor | El controlador PostgreSQL del modo servidor |
| Interfaz | Las cinco ventanas, el tamaño y la escala de la pantalla |

Cada comprobación es independiente: un fallo nunca detiene las demás. Una comprobación que no se aplica a la
instalación (los modelos de IA en la edición sin IA) se marca "no se aplica", no como fallo.

## Desde un script

```python
import rockface.api as rf

res = rf.selftest(gui=False, quick=True)
print(res["summary"], res["folder"])     # {'passed': 13, 'skipped': 0, 'failed': 0} and the folder of report.html
```

## Límites y problemas comunes

* **La comprobación de las ventanas en un equipo sin pantalla.** Ejecute `rockface selftest` sin `--gui`, o defina
  `QT_QPA_PLATFORM=offscreen`.
* **La primera vez tarda más.** El sistema operativo y el antivirus revisan los archivos del programa en el primer
  inicio.

## Cobertura

1.0 (autoprueba de la instalación; ROADMAP).
