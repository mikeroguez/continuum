# Roadmap UX y métricas de Continuum

## Premisa

Continuum no debe depender de que el desarrollador recuerde un ritual. Su UX
debe convertir trabajos frecuentes en comandos idempotentes que detectan el
estado actual, reparan lo seguro y explican lo que requiere decisión humana.

El foco diferencial es reducir costo de contexto: cargar menos tokens,
persistir solo lo no inferible y evitar que la memoria crezca hasta volverse
otro problema.

Este diseño parte de hipótesis JTBD internas; falta validarlo con uso real,
entrevistas o diarios de trabajo.

## Contraste con evidencia

El plan es coherente con la evidencia revisada, pero requiere tres ajustes
para no introducir friccion nueva ni sesgos de medicion.

| Evidencia | Implicacion para Continuum | Ajuste al plan |
|---|---|---|
| Las heuristicas de Nielsen priorizan visibilidad del estado, prevencion de errores, reconocimiento sobre recuerdo, control del usuario y recuperacion clara. | `status`, `context`, `doctor --fix` y comandos idempotentes atacan problemas correctos. | Todo comando nuevo debe mostrar estado, impacto y siguiente accion; cualquier accion destructiva o remota requiere confirmacion. |
| SPACE advierte que productividad no se mide con una sola dimension. | Tokens por si solos no prueban mejora; pueden bajar mientras cae calidad o continuidad. | Medir siempre un conjunto minimo: tokens, continuidad, friccion, calidad y coordinacion. |
| DevEx estructura la experiencia en feedback loops, cognitive load y flow state. | Continuum debe reducir carga cognitiva y pasos recordados sin interrumpir el flujo. | Preferir medicion pasiva desde git/archivos/hooks; usar preguntas manuales solo como micro-check opcional. |
| DORA advierte contra convertir metricas en metas rigidas y recomienda empezar con baseline y conversaciones. | Metricas como "handoff <400 tokens" pueden volverse Goodhart si se usan como regla ciega. | Usar umbrales como guardrails, no objetivos absolutos; capturar excepciones justificadas. |
| La revision interna sobre `AGENTS.md` muestra que contenido inferible aumenta costo y puede empeorar resultados. | `context` no debe premiar archivos cortos sino informacion no inferible y pertinente. | Agregar clasificacion de contexto: obligatorio, recomendado, bajo demanda, evitar por ahora. |

Fuentes usadas para este contraste:

- Nielsen Norman Group, "10 Usability Heuristics for User Interface Design":
  https://www.nngroup.com/articles/ten-usability-heuristics/
- Forsgren et al., "The SPACE of Developer Productivity":
  https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/
- Noda, Storey, Forsgren y Greiler, "DevEx: What Actually Drives Productivity":
  https://doi.org/10.1145/3610285
- DORA, "Software delivery performance metrics":
  https://dora.dev/guides/dora-metrics/
- `docs/investigacion-2026.md`, especialmente la seccion sobre contenido
  inferible en `AGENTS.md`.

## Brechas y mitigacion de baja friccion

### Brecha 1 — Muchas metricas pueden volverse ceremonia

Riesgo: el desarrollador abandona Continuum si tiene que registrar eventos a
mano.

Mitigacion:

- Por defecto medir solo lo que ya existe en git y archivos: tamanos, tokens
  estimados, edad de handoff, tareas abiertas/cerradas, checks ejecutados,
  commits, tags y cambios fuera del write-set.
- Capturar eventos desde comandos que el usuario ya ejecuta (`doctor`,
  `session end`, `task close`, `sync`, `release`).
- Hacer cualquier input humano opcional y de una sola pregunta.

### Brecha 2 — Tokens bajos no garantizan mejor resultado

Riesgo: optimizar para menos tokens puede ocultar perdida de calidad.

Mitigacion:

- Medir tokens junto con validacion, rework y continuidad.
- Reportar "tokens ahorrados" solo si no suben tareas reabiertas, errores de
  contexto o cambios fuera de alcance.
- Mantener explicacion de excepciones cuando una tarea necesita mas contexto.

### Brecha 3 — Falta linea base antes de intervenir

Riesgo: no poder demostrar mejora porque las metricas empiezan despues de los
cambios UX.

Mitigacion:

- Mover `metrics snapshot` al Sprint 0.
- Capturar baseline del repo actual antes de implementar `context`, `tokens` o
  `doctor --fix`.
- Definir ventanas comparables: antes/despues por proyecto, no comparaciones
  entre proyectos distintos sin normalizar.

### Brecha 4 — Medicion puede afectar comportamiento

Riesgo: si las metricas se sienten evaluativas, el equipo las optimiza o las
  evita.

Mitigacion:

- Declarar que las metricas son para mejorar el sistema, no para evaluar
  personas.
- Anonimizar usuarios, rutas sensibles y remotos en exports.
- No versionar eventos crudos por defecto.

### Brecha 5 — `doctor --fix` puede erosionar control

Riesgo: una reparacion automatica toca archivos cuando el usuario no esperaba
  cambios.

Mitigacion:

- `--dry-run` por defecto para arreglos que modifican memoria o config.
- Auto-fix sin confirmacion solo para artefactos claramente derivados o
  faltantes seguros.
- Cada fix debe ser idempotente y reversible por git.

### Brecha 6 — Mezclar investigacion con uso diario

Riesgo: el producto se vuelve pesado si cada sesion pide datos para el estudio.

Mitigacion:

- Separar metricas en tres niveles:
  - automaticas: se capturan sin interrumpir el flujo;
  - opcionales: micro-check de una pregunta al cerrar sesion;
  - investigacion: diarios, entrevistas o encuestas solo en estudios
    declarados.
- El modo normal nunca bloquea por no responder una pregunta.
- `metrics report` debe funcionar con datos automaticos incompletos y marcar
  la confianza del resultado.

### Brecha 7 — Automatizar cuando hacia falta preguntar

Riesgo: por reducir friccion, la IA puede asumir decisiones que cambian
alcance, privacidad, riesgo o interpretacion del objetivo.

Mitigacion:

- Definir una politica de preguntas minimas: preguntar solo cuando la decision
  no sea inferible y afecte resultado, seguridad, privacidad, costo o alcance.
- Si la respuesta solo mejora marginalmente el resultado, asumir una opcion
  conservadora y registrar la suposicion.
- Cuando pregunte, hacer una sola pregunta concreta, con recomendacion por
  defecto y consecuencias claras.
- Permitir que los comandos impriman "necesita decision" en vez de fallar con
  errores genericos.

## Actores

- Desarrollador usuario: trabaja en un repo que usa Continuum.
- Agente IA: necesita contexto mínimo para actuar sin releer todo.
- Mantenedor de Continuum: publica versiones, regenera `export` y mantiene
  compatibilidad.
- Creador/investigador: mide si Continuum funciona y produce evidencia
  publicable.

## Jobs To Be Done

### Desarrollador usuario

1. Cuando abro un repo con Continuum, quiero saber el estado del proyecto y el
   siguiente paso sin leer todo el protocolo, para empezar en menos de un
   minuto.
2. Cuando empiezo una tarea, quiero que la estructura mínima se cree sola y con
   alcance claro, para no depender de memoria humana.
3. Cuando trabajo durante una sesión, quiero que el sistema detecte memoria
   obesa, handoff viejo, hooks faltantes o entrypoints divergentes, para no
   romper continuidad.
4. Cuando cierro o pauso una sesión, quiero guardar un handoff corto pero útil,
   para que otra IA o persona pueda retomar sin contexto del chat.
5. Cuando actualizo Continuum en un proyecto consumidor, quiero no recordar
   comandos de subtree, para evitar errores de sincronización.

### Agente IA

1. Cuando entra a una sesión nueva, quiere una lista exacta de archivos/rangos
   que leer y de archivos que no debe leer todavía, para gastar el mínimo de
   tokens.
2. Cuando detecta una inconsistencia reparable, quiere una acción segura e
   idempotente, para corregir sin pedir instrucciones innecesarias.
3. Cuando una tarea cruza dominios, quiere un índice de contexto por tema, para
   cargar detalle solo bajo demanda.

### Mantenedor de Continuum

1. Cuando hay cambios listos en `template/`, quiere publicar una versión sin
   recordar pasos manuales, para mantener `main`, `export`, changelog, version
   y tags consistentes.
2. Cuando protege el repositorio, quiere checks y reglas accionables, para
   evitar pushes accidentales y releases mal hechos.

### Creador/investigador

1. Cuando despliega Continuum en proyectos reales, quiere medir tokens,
   continuidad, fricción, calidad y coordinación, para validar si el protocolo
   mejora el trabajo con IA.
2. Cuando prepara una publicación científica, quiere exportar datos locales y
   anonimizables, para analizar resultados sin telemetría remota por defecto.

## Principios UX

- Visibilidad del estado: `status` responde "estoy listo o no" en segundos.
- Prevención de errores: `doctor` detecta problemas antes de commit, cierre de
  sesión o release.
- Reconocimiento sobre recuerdo: comandos por intención, no por implementación.
- Control y libertad: `--dry-run` antes de cambios; confirmación para acciones
  remotas o destructivas.
- Consistencia: todos los comandos distinguen `status/check/fix/apply` cuando
  aplique.
- Recuperación de errores: cada problema incluye impacto y siguiente comando.
- Ley de Hick: cada momento ofrece una acción principal, no una lista larga.
- Ley de Tesler: la complejidad de git, subtree y token budget vive en el CLI.

## Politica de preguntas de la IA

Continuum debe reducir memoria humana, no eliminar el juicio humano. La IA y
el CLI deben preguntar cuando sea necesario para afinar una decision que no se
puede recuperar con seguridad desde el repositorio.

### Preguntar siempre

- La accion modifica datos remotos, publica releases, fuerza ramas, borra o
  mueve informacion.
- Hay ambiguedad de alcance: dos interpretaciones producen write-sets
  distintos.
- La decision afecta privacidad, telemetria, anonimizado o exportacion de
  metricas.
- El sistema detecta conflicto entre instrucciones versionadas.
- Falta informacion no inferible que puede cambiar la solucion.

### No preguntar por defecto

- El repo da una respuesta clara.
- La accion es local, reversible por git e idempotente.
- La decision es de bajo riesgo y existe una convencion del proyecto.
- La pregunta solo ahorraria una lectura pequena o una preferencia estetica.

### Formato de pregunta

Cada pregunta debe minimizar carga cognitiva:

- una sola decision por pregunta;
- opcion recomendada primero;
- impacto de cada opcion en una frase;
- posibilidad de continuar con una suposicion conservadora si el usuario no
  responde.

Ejemplo:

```text
Necesito decidir si capturamos metricas opcionales en esta tarea.
Recomendado: no pedir preguntas al usuario y registrar solo metricas automaticas.
Alternativa: activar una pregunta opcional al cerrar sesion para medir calidad de continuidad.
```

## Comandos propuestos

### `continuum status`

Resumen humano de 10 segundos:

```text
Continuum: listo
Contexto inicial: ~2.7k tokens
Memoria: OK
Hooks: instalados
Tareas: 1 activa
Handoff: vigente
Export: sincronizada
Siguiente accion: continuum context
```

### `continuum context`

Lista minima de contexto para la IA:

- archivos obligatorios de arranque;
- temas recomendados segun tarea;
- archivos a evitar por ahora;
- costo estimado por bloque;
- `--why` para justificar cada inclusion.

### `continuum tokens`

Presupuesto de tokens:

- arranque obligatorio;
- handoff;
- indice;
- cada tema;
- crecimiento semanal si hay snapshots;
- advertencias de bloat.

### `continuum doctor --fix`

Repara solo lo seguro:

- instalar hooks faltantes;
- crear carpetas y `.gitkeep`;
- regenerar subagentes derivados;
- normalizar config incompleta;
- compactar temas solo con confirmacion o `--apply`.

No debe hacer automaticamente:

- push remoto;
- force-push;
- crear tags;
- borrar ramas;
- modificar proteccion de GitHub.

### `continuum session start/end`

`start` orienta lectura inicial. `end` escribe continuidad:

- objetivo;
- decisiones no inferibles;
- archivos tocados;
- validacion;
- riesgos;
- siguiente paso.

Debe advertir si el handoff repite README, diffs largos o informacion
inferible.

### `continuum sync`

Para proyectos consumidores:

- lee `.ai/config.json`;
- valida remoto, prefix y version;
- recomienda tag estable;
- ejecuta con `--apply` o imprime con `--dry-run`.

### `continuum release <version>`

Para meta-desarrollo:

- valida arbol limpio;
- corre `doctor` y tests;
- valida `CHANGELOG.md` y `__version__`;
- regenera `export`;
- crea o valida tag;
- publica con confirmacion.

Segunda ejecucion: "todo ya estaba listo".

### `continuum metrics`

Medicion local:

- `metrics snapshot`;
- `metrics report`;
- `metrics export --format csv|json`;
- `metrics anonymize`.

Eventos crudos deben quedar gitignored por defecto. Snapshots agregados pueden
versionarse si el equipo lo decide.

## Indicadores

Continuum mide para aprender y mejorar el sistema, no para evaluar personas.
Los reportes deben mostrar tendencias y tradeoffs, no rankings.

### Niveles de medicion

| Nivel | Ejemplos | Friccion permitida | Uso |
|---|---|---|---|
| Automatico | tokens estimados, edad de handoff, tareas abiertas, tests ejecutados, estado de hooks | cero preguntas | uso diario |
| Opcional | "La sesion fue facil de retomar? si/no", "falto contexto? si/no" | una pregunta al cierre, omitible | mejora continua |
| Investigacion | entrevista, diario de trabajo, encuesta DevEx, codificacion cualitativa | requiere consentimiento explicito | publicacion cientifica |

El reporte debe distinguir estos niveles para no presentar datos automaticos
como evidencia causal suficiente.

### Tokens

- tokens de arranque;
- tokens por handoff;
- tokens por tema;
- porcentaje de memoria inferible/redundante;
- crecimiento de `.ai/` por semana;
- numero de archivos leidos antes del primer cambio util.

Indicador primario: tokens de arranque obligatorios.

Indicadores de balance: validacion ejecutada, tareas reabiertas por contexto
insuficiente y cambios fuera de alcance.

### Continuidad

- edad de handoff;
- sesiones retomadas con handoff vigente;
- tareas abiertas sin handoff;
- tareas reabiertas por contexto insuficiente;
- tiempo estimado hasta primer cambio util.

### Friccion

- comandos manuales por flujo;
- comandos fallidos por configuracion;
- reparaciones aplicadas por `doctor --fix`;
- veces que hooks estaban faltantes;
- veces que el usuario debio consultar docs para operar.

Medicion de baja friccion: contar comandos ejecutados por Continuum y errores
detectados; no pedir al usuario que llene bitacoras manuales salvo en estudios
exploratorios.

### Calidad

- tests ejecutados por tarea;
- tareas cerradas con validacion;
- bugs reintroducidos;
- reverts;
- cambios fuera de write-set.

### Coordinacion

- tareas duplicadas;
- tareas sin owner;
- conflictos de git;
- sesiones concurrentes sin worktree;
- handoffs entre proveedores.

### Adopcion

- proyectos instalados;
- proyectos activos despues de N semanas;
- comandos mas usados;
- puntos de abandono del flujo.

## Privacidad y datos

- Sin telemetria remota por defecto.
- Eventos locales en `.ai/metrics/events.jsonl`, gitignored por defecto.
- Export explicito por comando.
- Anonimizacion de rutas, slugs, usuarios y remotos.
- Separar datos crudos de reportes agregados.
- Los reportes comparan proyectos contra su propia linea base; no rankean
  personas ni equipos.

## Esquema minimo de eventos

Los eventos crudos son opcionales y locales. Cada evento debe poder omitirse
sin romper el flujo principal.

```json
{"ts":"2026-09-09T20:00:00Z","event":"doctor_run","problems":0,"warnings":0,"startup_tokens":2723}
{"ts":"2026-09-09T20:05:00Z","event":"context_suggested","required_files":3,"recommended_files":1,"estimated_tokens":3100}
{"ts":"2026-09-09T20:30:00Z","event":"session_end","handoff_tokens":340,"validation":"passed"}
{"ts":"2026-09-09T21:00:00Z","event":"task_closed","slug_hash":"...","size":"medium","validation":"passed"}
```

Campos sensibles deben hashearse o omitirse en `metrics export --anonymize`.

## Sprints

El detalle operativo de cada sprint vive en `docs/ux-metrics-sprints.md`.
Esta seccion resume la secuencia y los criterios de salida.

### Sprint 0 — JTBD y metrica base

Entregables:

- Documento JTBD y metricas.
- Esquema inicial de eventos.
- Definicion de indicadores primarios.
- Criterios de privacidad.
- `metrics snapshot --dry-run` como baseline local sin telemetria remota.
- Checklist de evaluacion heuristica para comandos nuevos.

Criterio de salida:

- Cada comando propuesto mapea a un job real.
- Cada metrica responde a una hipotesis evaluable.
- Existe una linea base antes de implementar mejoras UX.

### Sprint 1 — Contexto y tokens

Entregables:

- `continuum context`.
- `continuum tokens`.
- `metrics snapshot` para capturar tokens y tamanos de memoria sin preguntas
  manuales.
- Reglas anti-bloat en `doctor`.
- Tests con fixtures de memoria pequena, obesa y redundante.

Criterio de salida:

- Una IA nueva sabe que leer y que no leer sin explorar todo el repo.
- Tokens de arranque se reportan en una sola pantalla.

### Sprint 2 — Status y reparacion segura

Entregables:

- `continuum status`.
- `doctor --fix`.
- `--dry-run` para reparaciones.
- Mensajes con problema, impacto y solucion.

Criterio de salida:

- Segunda ejecucion de `doctor --fix` no cambia nada y sale OK.

### Sprint 3 — Sesiones e handoff optimizado

Entregables:

- `continuum session start`.
- `continuum session end`.
- Validacion de handoff corto.
- Deteccion de informacion inferible.

Criterio de salida:

- Handoff recomendado menor a 400 tokens salvo excepcion justificada.

### Sprint 4 — Tareas guiadas

Entregables:

- `task current`.
- `task resume`.
- `task close` actualiza handoff general.
- Sugerencias de rol y tamano.

Criterio de salida:

- Crear, pausar, retomar y cerrar tarea no requiere recordar archivos internos.

### Sprint 5 — Sync para proyectos consumidores

Entregables:

- `continuum sync --check`.
- `continuum sync --dry-run`.
- `continuum sync --apply`.
- Validacion de remoto, prefix y tag.

Criterio de salida:

- Un proyecto consumidor puede actualizar Continuum sin recordar subtree.

### Sprint 6 — Release meta-Continuum

Entregables:

- `export status`.
- `export refresh`.
- `release <version>`.
- Validaciones de changelog, version, tag y export.

Criterio de salida:

- Release repetido es idempotente y no duplica tags ni ramas.

### Sprint 7 — GitHub y proteccion

Entregables:

- `github protect --print`.
- `github protect --apply` si hay `gh` o token.
- Reglas para `main`, `export` y tags `v*`.

Criterio de salida:

- Si no hay permisos, el usuario recibe pasos exactos; si hay permisos, se
  aplica automaticamente con confirmacion.

### Sprint 8 — Evidencia y publicacion

Entregables:

- `metrics report`.
- `metrics export`.
- `metrics compare --baseline <snapshot>`.
- Protocolo de evaluación y plan operativo prerregistrable.
- `docs/research-protocol.md` y `docs/evaluation-plan.md`.

Criterio de salida:

- Continuum puede producir datos locales suficientes para evaluar hipotesis.

## Hipótesis científicas

Las hipótesis, comparaciones, métricas y criterios de análisis canónicos viven
en `docs/research-protocol.md`. Esta hoja de ruta no afirma resultados: las
métricas de producto son señales operativas y no sustituyen una evaluación
controlada de continuidad entre sesiones.

## Metricas norte

- Tokens de arranque: menor a 3k.
- `estado-dev.md`: menor o igual a 80 lineas.
- Handoff normal: menor a 400 tokens.
- Tema individual: menor o igual a 300 lineas.
- Tiempo hasta siguiente accion clara: menor a 60 segundos.
- Tareas cerradas con validacion: tendencia creciente.
