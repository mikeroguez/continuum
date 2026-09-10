# Guía para agentes que trabajan con Continuum

`AI_COLLABORATION.md` contiene las reglas obligatorias. Esta guía explica cómo aplicarlas. Si difieren, sigue el archivo canónico.

## Objetivo

Deja el repositorio en un estado que otra sesión pueda entender y verificar. No conserves información importante solo en la conversación.

## Arranque mínimo

1. Lee `AI_COLLABORATION.md`, `.ai/HANDOFF.md` y `.ai/state/estado-dev.md`.
2. Si la tarea existe, lee su `task.md` y su plan.
3. Usa `tools/continuum context --task <slug> --why` para orientar la lectura.
4. Abre temas, código y documentación adicional solo si responden a una necesidad concreta.

No cargues todos los temas ni repitas en el handoff lo que se verifica en el diff o las pruebas.

## Elegir el flujo

Un cambio claro y pequeño puede trabajarse sin carpeta de tarea. Si abarca un módulo, varios archivos, riesgo o ambigüedad, crea o retoma una tarea. Para trabajo grande, usa el plan de ejecución como cola persistente de pasos.

## Qué registrar

Registra decisiones no inferibles: alternativas descartadas, límites de producto, riesgos, validaciones y siguiente paso. No registres secretos, datos personales, rutas locales, transcripciones de chat, razonamiento interno ni información de terceros sin autorización.

Al interrumpirte o terminar:

- actualiza el handoff general;
- completa el handoff de una tarea formal antes de cerrarla; y
- nombra las validaciones ejecutadas y pendientes.

Un handoff breve y exacto es mejor que una crónica larga.

## Cómo usar reglas y documentación

- Trata `AI_COLLABORATION.md` como un mapa de reglas no negociables.
- Trata `estado-dev.md` como índice, no como historial.
- Trata los temas y `docs/` como fuentes bajo demanda.
- Si una regla es crítica y repetida, prefiere una prueba, linter, hook o CI antes que añadir texto al protocolo.

No inventes reglas para llenar vacíos. Pide dirección antes de cambiar alcance, publicar, borrar, revelar información o ejecutar acciones irreversibles.

## Coordinación y cierre

Declara la tarea y su responsable cuando haya más de una persona o agente. Usa un worktree o rama separada para trabajo concurrente. Un `claim` da visibilidad; no autoriza a sobrescribir trabajo ajeno.

Un rol es una lente de trabajo, no un subproceso concurrente. Consulta los packs activos con `tools/continuum roles list`; el rol puede registrarse al crear una tarea o handoff. `roles sync` genera artefactos locales para Claude Code y nunca deben editarse manualmente ni confirmarse en Git.

Antes de proponer que el trabajo terminó:

1. ejecuta validaciones proporcionales al cambio;
2. revisa el diff y archivos no rastreados;
3. ejecuta `tools/continuum doctor` si tocaste protocolo, memoria o tareas;
4. registra resultado y riesgos pendientes; y
5. deja commit, publicación, despliegue y acciones externas a quien tenga esa autorización.

## Señales para simplificar

Simplifica cuando el contexto de arranque crezca, una instrucción replique información del repositorio o una tarea pequeña genere demasiados archivos. Divide la memoria por tema y conserva en el protocolo solo hechos no inferibles y acciones necesarias.
