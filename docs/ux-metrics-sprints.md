# Sprints detallados — UX y métricas de Continuum

## Criterios globales

Cada sprint debe preservar estas reglas:

- Cero telemetria remota por defecto.
- Toda accion local que modifique archivos debe ser reversible por git.
- Toda accion destructiva, remota o de privacidad requiere confirmacion.
- Cada comando nuevo debe ser idempotente: repetirlo no debe duplicar estado ni
  degradar memoria.
- Cada salida humana debe mostrar estado, impacto y siguiente accion.
- Los cambios de UX se validan contra JTBD, no contra preferencias internas.

## Sprint 0 — Baseline, JTBD y método de medición

### Objetivo

Fijar una linea base antes de modificar la experiencia. Este sprint evita que
la mejora se mida tarde o solo con intuicion.

### Jobs cubiertos

- Creador/investigador: medir si Continuum funciona.
- Desarrollador usuario: no cargar con rituales de investigacion durante el
  uso normal.

### Alcance

- Formalizar metricas primarias y de balance.
- Definir niveles de medicion: automatico, opcional, investigacion.
- Diseñar el primer snapshot local.
- Definir checklist heuristico para evaluar comandos nuevos.

### Entregables

- `docs/ux-metrics-roadmap.md` actualizado.
- `docs/ux-metrics-sprints.md`.
- Especificacion de `metrics snapshot --dry-run`.
- Esquema inicial de eventos locales.
- Checklist UX para comandos de Continuum.

### Tareas

- Definir schema de snapshot:
  - fecha;
  - commit;
  - rama;
  - tokens de arranque;
  - lineas por archivo de memoria;
  - tareas abiertas/cerradas;
  - edad de handoff;
  - estado de hooks;
  - checks conocidos.
- Definir schema de evento local:
  - `doctor_run`;
  - `context_suggested`;
  - `session_end`;
  - `task_started`;
  - `task_closed`;
  - `sync_checked`;
  - `release_checked`.
- Decidir archivo gitignored para eventos crudos:
  - `.ai/metrics/events.jsonl`.
- Decidir carpeta opcional de snapshots versionables:
  - `.ai/metrics/snapshots/`.
- Crear checklist heuristico:
  - visibilidad de estado;
  - lenguaje del usuario;
  - control/confirmacion;
  - prevencion de errores;
  - reconocimiento sobre recuerdo;
  - salida minima;
  - recuperacion accionable.

### Criterios de salida

- Existe baseline ejecutable sin pedir datos manuales.
- Cada metrica esta clasificada como automatica, opcional o investigacion.
- Ninguna metrica diaria exige responder preguntas.
- `tools/continuum doctor` sigue limpio.

### Riesgos

- Riesgo: sobre-disenar medicion antes de producto.
  Mitigacion: snapshot minimo, sin dashboard.
- Riesgo: sesgo por medir solo el meta-repo.
  Mitigacion: marcarlo como baseline de desarrollo, no evidencia general.

## Sprint 1 — Contexto y tokens

### Objetivo

Reducir carga inicial para IA y desarrollador: decir que leer, que no leer y
cuanto cuesta.

### Jobs cubiertos

- Agente IA: cargar contexto minimo.
- Desarrollador usuario: saber si el repo esta listo sin leer el protocolo.
- Creador/investigador: medir tokens antes/despues.

### Alcance

- `continuum context`.
- `continuum tokens`.
- `metrics snapshot` basico si no quedo en Sprint 0.
- Reglas anti-bloat en `doctor`.

### Entregables

- `tools/_continuum/context.py`.
- `tools/_continuum/metrics.py` con snapshot minimo.
- Nuevos subcomandos en `tools/_continuum/__main__.py`.
- Tests unitarios para seleccion de contexto y estimacion de tokens.
- Documentacion corta en README o tema de comandos.

### Tareas

- Implementar `context`:
  - lista archivos obligatorios;
  - lee `.ai/state/estado-dev.md`;
  - marca temas como bajo demanda;
  - soporta `--task <slug>`;
  - soporta `--why`;
  - soporta `--json`.
- Implementar categorias:
  - obligatorio;
  - recomendado;
  - bajo demanda;
  - evitar por ahora.
- Implementar `tokens`:
  - tokens de arranque;
  - tokens de handoff;
  - tokens de indice;
  - tokens por tema;
  - total estimado.
- Agregar warnings anti-bloat:
  - entrypoint demasiado largo;
  - indice con contenido que parece detalle;
  - handoff con bloque de diff largo;
  - tema sobre limite.
- Crear fixtures:
  - proyecto minimo;
  - memoria obesa;
  - tema recomendado por tarea;
  - repo sin `.ai`.

### Criterios de salida

- Una sesion nueva puede ejecutar `continuum context` y obtener menos de una
  pantalla de lectura recomendada.
- `continuum tokens` reporta el costo sin ejecutar acciones.
- `doctor` no duplica toda la salida de `tokens`; solo resume y remite.
- Tests cubren JSON y salida humana.

### Metricas

- Tokens de arranque.
- Numero de archivos obligatorios.
- Numero de temas recomendados.
- Tiempo estimado hasta siguiente accion clara.

### Riesgos

- Riesgo: `context` recomienda demasiado.
  Mitigacion: maximo por defecto de 3-6 entradas, resto bajo demanda.
- Riesgo: clasificacion incorrecta por heuristica simple.
  Mitigacion: `--why` y posibilidad de override futuro en config.

## Sprint 2 — Status y reparacion segura

### Objetivo

Convertir diagnostico en orientacion: una pantalla para saber estado y una ruta
segura para reparar lo obvio.

### Jobs cubiertos

- Desarrollador usuario: saber que hacer ahora.
- Agente IA: corregir inconsistencias locales sin pedir instrucciones de mas.

### Alcance

- `continuum status`.
- `doctor --fix`.
- `--dry-run` para fixes.
- Mensajes con problema, impacto y solucion.

### Entregables

- Modulo comun de checks reutilizable entre `doctor`, `status` y `--fix`.
- Salida compacta de `status`.
- Plan de fixes en dry-run.
- Tests de idempotencia.

### Tareas

- Extraer checks de `doctor` a estructuras con:
  - id;
  - severidad;
  - mensaje;
  - impacto;
  - solucion;
  - fix seguro opcional.
- Implementar `status`:
  - listo/no listo;
  - contexto inicial;
  - memoria;
  - hooks;
  - tareas;
  - handoff;
  - siguiente accion.
- Implementar `doctor --fix --dry-run`.
- Implementar fixes seguros:
  - crear carpetas faltantes;
  - crear `.gitkeep`;
  - instalar hooks;
  - regenerar roles de Claude si el pack esta activo;
  - normalizar config con defaults.
- Bloquear fixes no seguros:
  - compactar borrando detalle;
  - modificar ramas;
  - hacer push;
  - crear tags.

### Criterios de salida

- Segunda ejecucion de `doctor --fix` no produce diff.
- `status` cabe en una pantalla pequena.
- Cada problema tiene un comando de salida.
- No hay preguntas para reparaciones locales claramente seguras.

### Metricas

- Numero de problemas detectados.
- Numero de fixes aplicados.
- Numero de comandos necesarios para llegar a OK.
- Comandos fallidos por configuracion.

### Riesgos

- Riesgo: auto-fix sorprende al usuario.
  Mitigacion: dry-run por defecto para cambios de memoria/config no triviales.

## Sprint 3 — Sesiones e handoff optimizado

### Objetivo

Hacer que iniciar y cerrar sesiones preserve continuidad sin producir memoria
larga o redundante.

### Jobs cubiertos

- Desarrollador usuario: pausar sin perder contexto.
- Agente IA: retomar con lectura minima.
- Creador/investigador: medir continuidad.

### Alcance

- `continuum session start`.
- `continuum session end`.
- Validacion de handoff corto.
- Deteccion ligera de contenido inferible.

### Entregables

- Subcomando `session`.
- Plantilla de handoff optimizada.
- Reglas de lint para handoff.
- Evento local `session_end`.

### Tareas

- `session start`:
  - mostrar handoff vigente;
  - mostrar tareas activas;
  - sugerir `context`;
  - avisar si handoff esta viejo.
- `session end`:
  - aceptar `--message`;
  - registrar proveedor/rol si aplica;
  - resumir git status;
  - registrar validacion ejecutada;
  - pedir una sola pregunta opcional si modo metricas opcionales esta activo.
- Lint de handoff:
  - tokens aproximados;
  - campos vacios;
  - diff largo pegado;
  - frases genericas;
  - contenido que parece README.
- Permitir excepcion:
  - `--allow-long --reason "..."`

### Criterios de salida

- Handoff normal menor a 400 tokens o excepcion justificada.
- `session end` no bloquea si no hay respuesta a micro-check opcional.
- El siguiente paso queda visible.

### Metricas

- Edad de handoff.
- Tokens de handoff.
- Sesiones con handoff completo.
- Sesiones retomadas con contexto insuficiente.

### Riesgos

- Riesgo: detector de contenido inferible da falsos positivos.
  Mitigacion: warning no bloqueante en primera version.

## Sprint 4 — Tareas guiadas

### Objetivo

Reducir ceremonia de tareas medianas/grandes y evitar tareas abiertas sin
estado util.

### Jobs cubiertos

- Desarrollador usuario: crear, retomar y cerrar tarea sin recordar estructura.
- Agente IA: saber cual tarea esta activa y que contexto leer.

### Alcance

- `task current`.
- `task resume`.
- `task close` mas integrado.
- Sugerencias de rol y tamaño.

### Entregables

- Heuristica de tarea actual.
- Salida resumida de tareas.
- Integracion con `context --task`.
- Tests de lifecycle.

### Tareas

- Implementar `task current`:
  - si hay una tarea activa, mostrarla;
  - si hay varias, pedir decision;
  - si no hay, sugerir `task start`.
- Implementar `task resume <slug>`:
  - mostrar objetivo;
  - write-set;
  - siguiente paso;
  - contexto recomendado.
- Mejorar `task start`:
  - sugerir size por alcance si se pasa `--files`;
  - sugerir rol por dominio;
  - crear plan solo para medium/large.
- Mejorar `task close`:
  - validar handoff de tarea;
  - actualizar handoff general;
  - registrar validacion;
  - archivar.

### Criterios de salida

- Un usuario puede retomar una tarea con un comando.
- Tarea medium/large no puede cerrarse sin handoff util salvo `--force`.
- El write-set se muestra antes de editar.

### Metricas

- Tareas activas sin handoff.
- Tareas cerradas con validacion.
- Tareas reabiertas.
- Cambios fuera del write-set.

### Riesgos

- Riesgo: volver obligatorio el sistema de tareas para cambios pequenos.
  Mitigacion: mantener tareas opcionales en small.

## Sprint 5 — Sync para proyectos consumidores

### Objetivo

Actualizar Continuum en proyectos reales sin recordar `git subtree`.

### Jobs cubiertos

- Desarrollador usuario: traer nueva version sin romper el repo.
- Agente IA: detectar config incompleta y explicar.

### Alcance

- `continuum sync --check`.
- `continuum sync --dry-run`.
- `continuum sync --apply`.
- Validacion de config.

### Entregables

- Subcomando `sync` nuevo o reemplazo de `sync-template`.
- Validacion de `template_remote`, `template_prefix` y version.
- Mensajes de conflicto.
- Tests con repos temporales.

### Tareas

- Leer config:
  - remoto;
  - prefix;
  - canal: tag/export;
  - ultima version aplicada si existe.
- `--check`:
  - validar remoto configurado;
  - validar branch/tag existente si hay red;
  - detectar working tree sucio.
- `--dry-run`:
  - imprimir comando exacto;
  - explicar impacto.
- `--apply`:
  - confirmar si hay cambios remotos;
  - ejecutar subtree;
  - registrar evento.
- Mantener alias:
  - `sync-template` llama a `sync --dry-run` o queda deprecado con aviso.

### Criterios de salida

- Proyecto consumidor puede actualizar desde tag sin conocer subtree.
- Si falta config, el comando no falla opaco: muestra campos faltantes.
- No hace cambios con arbol sucio salvo confirmacion explicita.

### Metricas

- Syncs exitosos/fallidos.
- Causa de fallo.
- Version/canal usado.
- Conflictos detectados.

### Riesgos

- Riesgo: aplicar subtree en repo con cambios locales.
  Mitigacion: bloquear por defecto y explicar.

## Sprint 6 — Release meta-Continuum

### Objetivo

Automatizar el release del propio Continuum sin ocultar pasos peligrosos.

### Jobs cubiertos

- Mantenedor de Continuum: publicar version reproducible.

### Alcance

- `export status`.
- `export refresh`.
- `release <version>`.
- Validacion de changelog/version/tag/export.

### Entregables

- Subcomandos `export` y `release`.
- Checks de consistencia entre `template/`, `export`, tag y changelog.
- Flujo idempotente.
- Tests con repos git temporales.

### Tareas

- `export status`:
  - comparar `export` con `HEAD:template`;
  - mostrar commit local/remoto si hay red;
  - detectar si export falta.
- `export refresh`:
  - dry-run por defecto;
  - borrar/recrear local solo con confirmacion;
  - usar `git subtree split --prefix=template -b export`.
- `release <version>`:
  - validar SemVer;
  - validar `__version__`;
  - validar `CHANGELOG.md`;
  - correr `doctor`;
  - correr tests configurados;
  - regenerar export;
  - crear tag anotado en export;
  - pedir confirmacion para push.
- Idempotencia:
  - si tag existe y apunta correcto, OK;
  - si export ya coincide, OK;
  - si tag apunta a otro commit, bloquear.

### Criterios de salida

- Ejecutar release dos veces no cambia nada en la segunda.
- No se publica nada remoto sin confirmacion.
- Error de red deja instrucciones de continuacion.

### Metricas

- Releases preparados.
- Releases publicados.
- Fallos por changelog/version/export.
- Tiempo/pasos hasta release.

### Riesgos

- Riesgo: force-push equivocado.
  Mitigacion: usar `--force-with-lease` y mostrar remoto exacto.

## Sprint 7 — GitHub y proteccion

### Objetivo

Hacer accionable la proteccion de ramas sin depender de recordar settings de
GitHub.

### Jobs cubiertos

- Mantenedor de Continuum: proteger `main`, `export` y tags.

### Alcance

- `github protect --print`.
- `github protect --apply` si hay `gh` o token.
- Validacion no bloqueante en `doctor` si se puede consultar API.

### Entregables

- Instrucciones UI exactas.
- Payload/API opcional.
- Deteccion de herramientas disponibles.
- Tests unitarios de generacion de plan.

### Tareas

- Detectar:
  - remoto GitHub;
  - `gh`;
  - `GITHUB_TOKEN`/`GH_TOKEN`;
  - permisos disponibles si la API responde.
- `--print`:
  - reglas para `main`;
  - reglas para `export`;
  - reglas para tags `v*`.
- `--apply`:
  - pedir confirmacion;
  - aplicar rulesets si API disponible;
  - reportar lo que no se pudo aplicar.
- `doctor`:
  - warning opcional si no puede verificar proteccion;
  - no bloquear repos sin GitHub.

### Criterios de salida

- Sin credenciales, el usuario obtiene pasos UI suficientes.
- Con credenciales, el comando aplica o explica permisos faltantes.
- No se asume GitHub para repos con otro host.

### Metricas

- Protecciones detectadas.
- Protecciones faltantes.
- Aplicaciones exitosas/fallidas.

### Riesgos

- Riesgo: acoplar Continuum a GitHub.
  Mitigacion: comando opcional bajo namespace `github`.

## Sprint 8 — Evidencia y publicacion

### Objetivo

Convertir datos locales en evidencia util sin comprometer privacidad ni inflar
el uso diario.

### Jobs cubiertos

- Creador/investigador: preparar analisis publicable.
- Desarrollador usuario: conservar control sobre datos.

### Alcance

- `metrics report`.
- `metrics export`.
- `metrics compare`.
- Protocolo de estudio.

### Entregables

- `docs/research-protocol.md`.
- Export CSV/JSON anonimizado.
- Comparacion contra baseline.
- Reporte Markdown local.

### Tareas

- `metrics report`:
  - tendencias de tokens;
  - continuidad;
  - friccion;
  - calidad;
  - coordinacion;
  - confianza del reporte.
- `metrics compare --baseline`:
  - antes/despues por proyecto;
  - no comparar proyectos distintos sin normalizar.
- `metrics export`:
  - CSV;
  - JSON;
  - `--anonymize`;
  - excluir eventos crudos sensibles por defecto.
- `docs/research-protocol.md`:
  - hipotesis;
  - variables;
  - amenazas a validez;
  - consentimiento;
  - plan de analisis.

### Criterios de salida

- Se puede generar un reporte local sin datos manuales.
- Export anonimizado no incluye remotos, nombres de usuario ni rutas absolutas.
- El protocolo distingue evidencia descriptiva de causal.

### Metricas

- Cobertura de datos por periodo.
- Confianza del reporte.
- Hipotesis con datos suficientes.
- Hipotesis pendientes por falta de datos.

### Riesgos

- Riesgo: sobre-interpretar datos observacionales.
  Mitigacion: declarar amenazas a validez y evitar claims causales sin diseno
  adecuado.

## Secuencia recomendada de implementacion

1. Sprint 0: baseline y metodo.
2. Sprint 1: `context`, `tokens`, snapshot minimo.
3. Sprint 2: `status`, `doctor --fix`.
4. Sprint 3: `session start/end`.
5. Sprint 4: tareas guiadas.
6. Sprint 5: sync de consumidores.
7. Sprint 6: release del meta-repo.
8. Sprint 7: GitHub/proteccion.
9. Sprint 8: reporte y protocolo cientifico.

La razon del orden: primero medir y reducir tokens; luego bajar friccion diaria;
despues mejorar flujos menos frecuentes como sync, release y proteccion.
