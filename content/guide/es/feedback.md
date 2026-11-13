# Enviar su opinión

## Para qué sirve

RockFace lo prueban colegas y estudiantes antes de que llegue a todos los usuarios. **Enviar opinión…** abre el
formulario de opinión de RockFace en su navegador, donde usted dice qué funciona, qué no y qué falta — sobre el
programa en general o sobre una función de esta guía. Las respuestas van al equipo de RockFace.

## Antes de empezar

* Un navegador y una conexión de red.
* El formulario es un Microsoft Forms del equipo de RockFace (Universidad de Brasilia). Mientras su dirección no esté
  definida, el botón lo avisa (abajo).

## Paso a paso

1. En RockFace Petro: **Ayuda → Enviar opinión…**. En RockFace Atlas, Explorer, Lab y MC: el botón **Enviar opinión…**
   de la barra de herramientas.
2. El navegador abre el formulario. Diga sobre qué programa y qué función escribe — la sección **Cobertura** al final
   de cada página de esta guía da los ítems de la función (por ejemplo *GT11*), que ayudan al equipo a encontrarla.
3. Describa lo que hizo, lo que esperaba y lo que pasó. Adjunte una captura de pantalla si ayuda; nunca adjunte datos
   confidenciales.
4. Envíe el formulario.

Cuando el formulario aún no está definido, RockFace muestra "El formulario de opinión aún no está definido." —
escriba entonces a la dirección de soporte de su equipo (**Ayuda → Soporte…** prepara las versiones a enviar).

## Opciones

| Dónde | Qué cambia |
|---|---|
| Preferencia `feedback/url` | La dirección del formulario (la fija el equipo cuando cambia el formulario). |
| Variable de entorno `ROCKFACE_FEEDBACK_URL` | Lo mismo, para una computadora o una sesión; prevalece sobre la preferencia. |

## Cómo funciona

RockFace solo abre la dirección del formulario en el navegador: el programa no envía nada, y ningún archivo, proyecto
o dato personal sale de la computadora. El texto de **Ayuda → Soporte…** (solo las versiones) puede pegarse en el
formulario.

## Desde un script

```python
print(rf.feedback_url())          # la dirección del formulario, o "" cuando aún no está definida
rf.send_feedback("lab")           # abre el formulario en el navegador; devuelve la dirección, o "" si no está definida
```

En una terminal: `rockface feedback` muestra la dirección del formulario (o que aún no está definida) y lo abre.

## Límites y problemas comunes

* "El formulario de opinión aún no está definido." — el equipo aún no fijó su dirección: use **Ayuda → Soporte…**.
* No se abre nada: ningún navegador está definido como predeterminado del sistema; copie la dirección que muestra
  `rockface feedback`.

## Cobertura

O2 (el formulario de opinión de los probadores en los programas, después de la 1.0 y del sitio).
