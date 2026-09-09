# Notas de trabajo: ux-metricas-continuum

Bitácora libre mientras se trabaja la tarea. No es para lectores externos:
es memoria operativa de la propia sesión (hipótesis activas, callejones sin
salida, cosas por confirmar). Si algo aquí termina siendo una decisión firme,
pasa a `handoff.md` o a un ADR — este archivo se archiva junto con la tarea.

## Hipótesis activas
- La ventaja principal de Continuum no es "tener mas comandos", sino reducir
  memoria humana y tokens de arranque.
- Los comandos deben mapear a jobs reales; un comando sin job claro agrega
  friccion.
- La medicion debe ser local y explicita para no convertir Continuum en una
  herramienta de telemetria opaca.
- Para publicacion cientifica, las metricas deben existir antes del rollout en
  proyectos reales; agregarlas despues produciria datos incompletos.
- La IA debe preguntar cuando una decision no inferible afecta alcance, riesgo,
  privacidad, costo o resultado; automatizar esos casos baja friccion aparente
  pero aumenta riesgo real.

## Evidencia recopilada
- `tools/continuum doctor` ya estima tokens de arranque, lo que puede ser base
  de `continuum tokens`.
- El protocolo actual ya separa indice corto y temas, una base compatible con
  `continuum context`.
- El flujo de release manual reciente mostro friccion real: recordar `export`,
  tag, changelog, version y push remoto.
- Nielsen heuristics respalda `status`, `context`, error prevention,
  reconocimiento sobre recuerdo y recuperacion clara.
- SPACE/DORA respaldan medir multiples dimensiones y no usar una sola metrica
  como objetivo rigido.
- DevEx respalda ordenar mejoras por feedback loops, cognitive load y flow
  state; por eso la medicion manual debe ser minima.

## Callejones sin salida (para no repetirlos)
- No disenar comandos desde la implementacion (`git subtree`, ramas, tags) sin
  mapear primero el job del usuario.
- No usar telemetria remota por defecto.
- No convertir `AGENTS.md` o `estado-dev.md` en documentos largos; eso rompe el
  objetivo de optimizacion de tokens.
- No mezclar uso diario con estudio cientifico: la investigacion debe ser un
  modo explicito, no una carga permanente para el desarrollador.
- No confundir "baja friccion" con "cero preguntas": una pregunta bien puesta
  puede evitar retrabajo y gasto de tokens.

## Decisiones de desglose
- Mantener `docs/ux-metrics-roadmap.md` como documento estrategico corto y
  `docs/ux-metrics-sprints.md` como backlog detallado.
- Priorizar Sprint 0 y Sprint 1 porque crean baseline y reducen tokens antes
  de intervenir en otros flujos.
- Crear tareas separadas para Sprint 0 y Sprint 1 en vez de implementarlas
  dentro de la tarea paraguas, para mantener write-sets chicos y validacion
  independiente.
