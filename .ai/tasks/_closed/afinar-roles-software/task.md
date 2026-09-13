# Tarea: afinar-roles-software

**Creada:** 2026-09-12 · **Tamaño:** medium · **Owner:** mike · **Rol:** (sin asignar)

## Objetivo
Los roles del pack `software` que producen código (`backend`, `frontend`,
`devops-infraestructura`) son genéricos por diseño — deben servir para
cualquier producto de software que use Continuum, no solo para este
repositorio. El owner pidió reforzarlos para que, por defecto, generen
soluciones eficientes, código lo más corto posible sin sacrificar
claridad, y documentación mínima (no verbosa).

## Incluido en el alcance
- Sección nueva "Estándares de código por defecto" en `backend.md`,
  `frontend.md` y `devops-infraestructura.md`, con guías **concretas y
  accionables** por dominio (evitar N+1, evitar abstracción prematura,
  disciplina de comentarios, secretos, documentación mínima) — no
  consejos genéricos tipo "escribe código limpio", que la evidencia ya
  revisada en `docs/investigacion-2026.md` §4 muestra que empeora el
  resultado (contenido inferible/genérico aumenta costo y baja tasa de
  éxito) en vez de mejorarlo.
- Refuerzo corto en `qa.md` (pack `comun`): en software, "bien" incluye
  estos estándares, no solo que las pruebas pasen — cierra el ciclo entre
  quien escribe y quien audita.
- Sincronizar los mismos archivos en `template/.ai/roles/` (regla de doble
  copia raíz/`template/`, `arquitectura.md`).
- Regenerar `.claude/agents/*.md` con `continuum roles sync` para verificar
  que el contenido nuevo se propaga correctamente al subagente real
  (archivos gitignored, no se commitean, pero sí se valida el resultado).

## Explícitamente fuera de alcance
- `ux-ui`, `producto-jtbd`, `ux-research` — no producen código, "eficiente
  y corto" no aplica a su mandato. Si el owner quiere un refuerzo de
  concisión para sus entregables (documentos de investigación/producto),
  es una tarea aparte con un criterio distinto al de código.
- `seguridad`, `privacidad-datos`, `accesibilidad`, `iso-calidad`, `legal`,
  `design-thinking`, `gestion-proyecto`, `orquestador` (pack `comun`) — su
  mandato ya es específico y no se solapa con "código eficiente y
  documentación mínima"; tocarlos sería ceremonia sin un problema real
  identificado (`ARCHITECTURE.md` §2, principio 2).
- Ningún cambio al mecanismo de roles en sí (`tools/_continuum/roles.py`,
  `roles sync`, ADR-009) — es contenido de catálogo, no arquitectura del
  sistema de roles.

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `.ai/roles/software/backend.md` y `template/.ai/roles/software/backend.md`
- `.ai/roles/software/frontend.md` y `template/.ai/roles/software/frontend.md`
- `.ai/roles/software/devops-infraestructura.md` y
  `template/.ai/roles/software/devops-infraestructura.md`
- `.ai/roles/comun/qa.md` y `template/.ai/roles/comun/qa.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `.ai/roles/software/*.md`, `.ai/roles/comun/qa.md` (contenido actual)
- `.ai/roles/comun/accesibilidad.md` (precedente de rol "beefed up" con
  checklist concreto — el nivel de especificidad a igualar)
- `docs/investigacion-2026.md` §4 (por qué el contenido debe ser
  específico/no inferible, no genérico)
- `tools/_continuum/roles.py` (cómo `sync()` vuelca `role["text"]` completo
  al subagente generado — todo lo que no esté en el .md fuente no llega al
  subagente)

## Contexto mínimo sugerido
Según el tamaño declarado arriba, no cargues más de lo necesario:

| Tamaño  | Techo de lectura inicial orientativo |
|---------|----------------------------------------|
| small   | 1-3 archivos concretos, sin explorar carpetas completas |
| medium  | 1 módulo/dominio, usar `rg`/`grep` para localizar antes de leer |
| large   | fragmentar con `continuum packetize`; considerar dividir en subtareas |
