# Revisión con asistentes de IA

Este repositorio define criterios comunes de revisión en
`AI_COLLABORATION.md` y expone el adaptador específico de GitHub Copilot en
`.github/copilot-instructions.md`. Las instrucciones del cliente son una
proyección: no sustituyen la revisión humana ni crean reglas de merge.

## Qué debe revisar el asistente

Prioriza hallazgos de alta confianza en este orden:

1. Corrección funcional y manejo explícito de errores.
2. Seguridad, secretos, validación de entradas y datos sensibles.
3. Pruebas ausentes o insuficientes para el comportamiento modificado.
4. Divergencia entre `AI_COLLABORATION.md` y sus entrypoints o proyecciones.
5. Cambios distribuibles que no se reflejan en `template/`.
6. Edición manual de archivos generados o drift detectable por `doctor`.

Cada comentario debe indicar archivo, ubicación, impacto y corrección
propuesta. No se deben reportar preferencias de estilo sin impacto funcional,
de seguridad o de mantenimiento.

## Flujo recomendado

1. Revisar el diff y confirmar el alcance de la tarea.
2. Solicitar la revisión del asistente desde el pull request.
3. Clasificar los comentarios y corregir solo los hallazgos confirmados.
4. Ejecutar nuevamente las validaciones del repositorio.
5. Solicitar una nueva revisión tras corregir el PR.
6. Obtener aprobación humana antes del merge.

No se habilitan aprobaciones automáticas ni se convierte la revisión del
asistente en requisito de protección de ramas.

## Fixture de validación

`evaluation/copilot-review/fixture.md` contiene un caso sintético no ejecutable
con cuatro defectos intencionados. Se usa únicamente para comprobar que una
revisión detecta:

- un fallo funcional;
- una prueba que no cubre el cambio;
- divergencia entre fuente canónica y proyección;
- un riesgo de seguridad o manejo de datos.

La evidencia de una revisión real debe registrarse sin tokens, credenciales,
datos personales ni transcripciones completas del chat.
