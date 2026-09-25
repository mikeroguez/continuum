# Matriz de compatibilidad: GitHub Copilot

**Sprint:** 0 · **Fecha:** 2026-09-10 · **Estado:** contrato aprobado

## Objetivo de validación

Continuum se considerará compatible con Copilot cuando las superficies
seleccionadas puedan descubrir instrucciones coherentes, ejecutar el flujo
operativo y dejar evidencia de continuidad sin crear una segunda fuente de
verdad.

## Superficies objetivo

| Superficie | Objetivo | Artefactos que debe descubrir | Criterio de aceptación |
|---|---|---|---|
| GitHub Copilot Coding Agent | Prioridad 1 | `.github/copilot-instructions.md`, `AGENTS.md` | Conoce el propósito, el protocolo, los comandos de validación y el handoff; abre un PR con las pruebas indicadas. |
| Copilot Chat/Agent en VS Code | Prioridad 1 | `.github/copilot-instructions.md`, `.github/instructions/`, `AGENTS.md` | Aplica las reglas globales y las específicas de la ruta activa; no contradice `AI_COLLABORATION.md`. |
| Copilot Code Review | Prioridad 1 | `.github/copilot-instructions.md`, instrucciones por ruta aplicables | Revisa corrección, pruebas, seguridad, consistencia canónica y paridad con `template/`; no sustituye la aprobación humana. |
| GitHub Copilot Chat en GitHub.com | Compatibilidad esperada | `.github/copilot-instructions.md`, `AGENTS.md` | Recibe las instrucciones globales; las reglas dependientes del IDE se documentan como limitación si no aplican. |
| JetBrains, Visual Studio, Eclipse, Xcode | Fuera del baseline | Depende del cliente | No se promete soporte equivalente sin una validación específica y evidencia del equipo que lo use. |

## Contrato de fuentes y proyecciones

| Artefacto | Tipo | Fuente | Requisito |
|---|---|---|---|
| `AI_COLLABORATION.md` | Fuente canónica | Mantenida manualmente | Contiene las reglas comunes; no se duplica por proveedor. |
| `AGENTS.md` | Entrypoint de agente | Proyección manual del protocolo | Debe remitir al protocolo canónico y conservarse compatible con agentes que reconocen `AGENTS.md`. |
| `.github/copilot-instructions.md` | Proyección Copilot global | Generada o validada desde el contrato de Continuum | Debe ser autocontenida para las reglas críticas, breve, determinista y detectable por `doctor`. |
| `.github/instructions/*.instructions.md` | Proyecciones por ruta | Derivadas de reglas canónicas | Solo contienen diferencias reales por ruta; no repiten el protocolo completo. |
| `.github/agents/*.agent.md` | Proyección de roles | `.ai/roles/<pack>/*.md` | Se genera de forma determinista; `.ai/roles/` sigue siendo la fuente única. |
| `.ai/HANDOFF.md` | Memoria de continuidad | CLI y sesión | Copilot puede escribirlo mediante `tools/continuum handoff --auto --provider copilot`; no se presupone un hook equivalente al de Claude. |

## Casos de aceptación

### Automáticos

1. `doctor` detecta que la integración Copilot está completa, ausente o
   desactualizada según la configuración.
2. La generación de instrucciones y agentes es determinista: dos ejecuciones
   consecutivas no producen diff.
3. La configuración raíz y `template/` conserva los artefactos obligatorios.
4. La suite existente y `doctor` permanecen limpios.
5. `copilot` es un valor válido para registrar el proveedor del handoff.

### Manuales

1. Coding Agent recibe una tarea pequeña y crea un PR que ejecuta las
   validaciones documentadas.
2. VS Code aplica una regla global y una regla por ruta en archivos distintos.
3. Code Review identifica defectos conocidos de corrección, pruebas o
   consistencia de arquitectura en un PR de prueba.
4. Después de corregir el PR, una nueva revisión refleja el estado corregido.

## Reglas de seguridad del contrato

- No se crean credenciales, tokens, servidores MCP ni permisos adicionales.
- No se activan aprobaciones automáticas ni se convierte Copilot Code Review en
  requisito de merge.
- No se registra contenido sensible en fixtures, handoffs ni evidencias.
- La compatibilidad se declara por superficie; no se extrapola desde una sola
  prueba.

## Baseline de Sprint 0

- Rama: `develop`.
- `python3 tools/continuum doctor`: 0 problemas críticos, 0 advertencias.
- `python3 -m unittest discover -s tests -t . -q`: 96 pruebas, todas pasan.
- El repositorio ya tiene `AGENTS.md`, por lo que existe compatibilidad básica
  con agentes que descubren ese archivo.
- No existen todavía `.github/copilot-instructions.md`,
  `.github/instructions/` ni `.github/agents/`; su implementación pertenece a
  los Sprints 1 y 2.
