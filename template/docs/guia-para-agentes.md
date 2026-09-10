# Guía para Agentes (Continuum)

> [Read in English](guide-for-agents.md) · [Manual para Personas](como-usar-continuum.md) · [Protocolo Canónico](../AI_COLLABORATION.md)

> [!NOTE]
> `AI_COLLABORATION.md` es la fuente canónica e innegociable de reglas. Esta guía explica la aplicación práctica del protocolo para asistentes de IA.

---

## Objetivo Principal

Dejar el repositorio en un estado totalmente interpretable y verificable para cualquier sesión futura (humana o de IA). **El repositorio es la memoria; la conversación es solo el canal de ejecución.**

---

## Arranque Mínimo de Sesión

1. Leer [`AI_COLLABORATION.md`](../AI_COLLABORATION.md), [`.ai/HANDOFF.md`](../.ai/HANDOFF.md) y [`.ai/state/estado-dev.md`](../.ai/state/estado-dev.md).
2. Si la tarea existe, consultar su `task.md` y su plan.
3. Usar `tools/continuum context` para orientar la lectura inicial.
4. Consultar código, temas de memoria y documentación técnica **únicamente si responden a una necesidad concreta**.

---

## Elección de Flujo

- **Cambio pequeño/trivial**: Trabajar directamente sin abrir carpeta de tarea formal.
- **Cambio medio/complejo**: Crear o retomar una tarea formal (`tools/continuum task start <slug>`).
- **Cambio de arquitectura**: Usar un plan de ejecución (`execution-plan.md`) como lista persistente de pasos.

---

## Registro de Memoria e Handoffs

Registrar decisiones no inferibles: alternativas descartadas, límites de producto, riesgos, validaciones y siguiente paso.

> [!CAUTION]
> **Privacidad y Seguridad:**
> Nunca registrar secretos, credenciales, datos personales, rutas absolutas locales, transcripciones brutas de chat ni información confidencial en la memoria versionada.

Al interrumpirse o concluir una sesión:
- Actualizar `.ai/HANDOFF.md`.
- Completar el handoff de la tarea en `.ai/tasks/<slug>/handoff.md` antes de cerrarla.
- Listar las pruebas unitarias/integración ejecutadas y pendientes.

---

## Coordinación y Cierre

1. Ejecutar validaciones proporcionales al cambio realizado.
2. Revisar el diff (`git status`, `git diff`) y limpiar archivos no rastreados o temporales.
3. Ejecutar `tools/continuum doctor` si se modificó el protocolo, la memoria o la infraestructura `.ai/`.
4. Registrar resultados y riesgos pendientes en el handoff.
5. Dejar commits, merges y publicaciones a la persona autorizada (salvo permiso expreso).

---

<div align="center">

Continuum · [Licencia MIT](../LICENSE)

</div>
