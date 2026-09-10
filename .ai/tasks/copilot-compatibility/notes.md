# Notas del Sprint 0: compatibilidad con Copilot

## Decisiones

- Se adopta como baseline GitHub Copilot Coding Agent, Copilot Chat/Agent en
  VS Code y Copilot Code Review.
- GitHub.com Copilot Chat se considera una superficie esperada, pero se
  documentarán sus diferencias frente a las funciones del IDE.
- Otros IDEs quedan fuera del baseline hasta que exista una necesidad y una
  prueba específica.
- `AI_COLLABORATION.md` permanece como fuente canónica.
- Copilot se modelará como integración de GitHub basada en
  `.github/copilot-instructions.md`; no se inventará un `COPILOT.md`.
- Las instrucciones globales, instrucciones por ruta y agentes personalizados
  serán proyecciones verificables, no copias manuales independientes.
- El contrato común será agnóstico del modelo. Las capacidades específicas de
  cada cliente viven en sus adaptadores nativos, como
  `.github/copilot-instructions.md`, `.github/instructions/`,
  `.github/agents/` y `.claude/settings.json`.
- El handoff de Copilot será explícito y manual/CLI; no se presupone un hook de
  cierre equivalente al de Claude Code.

## Pendientes transferidos

- Sprint 1: smoke test real con Copilot Coding Agent; la integración global,
  configuración, `doctor`, handoff y pruebas ya están implementados.
- Sprint 2: prueba interactiva en VS Code; las instrucciones por ruta y la
  generación de `.github/agents/` ya están implementadas.
- Sprint 3: validación real de Code Review y segunda pasada sobre un PR; los
  criterios, documentación y fixture ya están implementados.
- Sprint 4: paridad de plantilla, CI, release y consumidor canary.

## Evidencia

- El baseline previo a la implementación específica de Copilot permanece
  limpio: 96 pruebas pasan y `doctor` reporta 0 problemas y 0 advertencias.
- La tarea activa y el archivo no trackeado de handoff preexistente aparecen en
  el working tree; no se mezclan con el contrato funcional de Copilot.
- Tras la implementación de Sprint 1, la suite tiene 99 pruebas y pasa. El
  `doctor` del checkout de trabajo seguirá señalando los nuevos archivos como
  no trackeados hasta que formen parte de un commit; en proyectos instalados o
  en CI, donde los archivos están trackeados, la validación es la relevante.
