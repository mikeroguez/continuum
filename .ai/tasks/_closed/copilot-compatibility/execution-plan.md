# Plan de ejecución: copilot-compatibility

## Sprint 0 — Contrato y baseline

- [x] Aprobar superficies objetivo: Coding Agent, Chat/Agent en VS Code y Code Review.
- [x] Definir qué archivos son fuente, cuáles son proyecciones y cómo se detecta drift.
- [x] Definir casos de aceptación manual y automatizados por superficie.
- [x] Registrar el baseline: `doctor` limpio y 96 pruebas pasando.

**Salida:** matriz de compatibilidad y contrato de generación aprobados.

## Sprint 1 — Copilot Coding Agent

- [x] Añadir `.github/copilot-instructions.md` en raíz y `template/`.
- [x] Diseñar una proyección breve con huella verificable de `AI_COLLABORATION.md`.
- [x] Incorporar la integración Copilot a configuración y `continuum doctor`.
- [x] Aceptar y documentar `copilot` en `handoff` y ciclo de sesión.
- [x] Añadir pruebas de presencia, tracking y drift.
- [ ] Ejecutar un smoke test real con Copilot Coding Agent.

**Salida parcial:** Copilot tiene instrucciones globales distribuidas en raíz y
plantilla, validación de drift y handoff explícito. El smoke test real queda
pendiente de acceso a Copilot Coding Agent.

## Sprint 2 — IDE, Chat y agentes personalizados

- [x] Crear instrucciones por ruta para Python, memoria `.ai/` y documentación.
- [x] Extender `roles.sync` para generar `.github/agents/*.agent.md`.
- [x] Validar frontmatter, nombres y regeneración determinista.
- [x] Mantener el contenido de instrucciones agnóstico al modelo o proveedor.
- [ ] Probar Chat/Agent en VS Code y documentar límites de otras superficies
  (validación interactiva pendiente de acceso).

**Salida:** el repositorio y la plantilla contienen instrucciones por ruta y
agentes personalizados generables desde `.ai/roles/`, sin romper los agentes
de Claude. La validación interactiva queda registrada como pendiente externa,
igual que el smoke test de Coding Agent, y se ejecutará al final de todos los
sprints.

## Sprint 3 — Copilot Code Review

- [x] Añadir criterios de revisión de Continuum a la instrucción global.
- [x] Preparar un fixture seguro y no ejecutable con defectos conocidos.
- [ ] Solicitar revisión de Copilot y registrar evidencia sin datos sensibles.
- [ ] Verificar revisión inicial, corrección y nueva revisión.
- [x] Documentar que la revisión asistida no sustituye aprobación humana ni
  reglas de merge.

**Salida parcial:** están definidos los criterios, el flujo y el fixture
reproducible. La revisión real y la segunda pasada quedan aplazadas al cierre
de todos los sprints.

## Sprint 4 — Distribución, CI y rollout

- [x] Mantener paridad raíz/`template/` para configuración, proyecciones,
  agentes, CLI y documentación.
- [x] Añadir regresiones de CI para archivos obligatorios, frontmatter, drift y
  paridad de plantilla.
- [x] Actualizar README, guías, arquitectura y changelog.
- [x] Preparar la versión `v1.4.0` con SemVer minor.
- [x] Publicar la versión que contiene la integración (`v1.4.0`, `main`,
  `export` y tag publicados).
- [x] Validar un consumidor canary desde la rama `export` publicada.

**Salida parcial:** la compatibilidad queda distribuible y verificable; faltan
la publicación autorizada y la validación de un consumidor canary.

## Criterios de terminado globales

- [ ] `AI_COLLABORATION.md` sigue siendo la fuente canónica.
- [ ] No existen reglas contradictorias entre entrypoints o proyecciones.
- [ ] Los artefactos generados son reproducibles y detectan drift.
- [ ] La suite pasa con `python3 -m unittest discover -s tests -t .`.
- [ ] `python3 tools/continuum doctor` devuelve 0 problemas y 0 advertencias.
- [ ] Se validan manualmente las superficies disponibles o se documenta el
  bloqueo de acceso/licencia.
- [ ] El cambio distribuible existe también en `template/`.
- [ ] El handoff de esta tarea queda completo antes de cerrarla.

## Decisiones por defecto

- Declarar `copilot` como integración/proveedor soportado, pero mapearlo a
  `.github/copilot-instructions.md`, no crear `COPILOT.md`.
- Generar todos los roles activos en `.github/agents/` y conservar
  `.claude/agents/`.
- Priorizar GitHub.com y VS Code; tratar otros IDEs como objetivos condicionados.
- No activar aprobaciones automáticas ni hacer Code Review requisito de merge.
- No añadir `.github/prompts/` en el baseline inicial.

## Estado actual

La implementación local y la publicación de Sprint 4 están completadas.
`v1.4.0` está publicado en `main` y `export`, y el consumidor canary validó
`doctor` y la regeneración de agentes Copilot desde el artefacto exportado.
Siguen pendientes únicamente las validaciones externas que requieren acceso a
Copilot Coding Agent, VS Code Chat/Agent y Code Review.
