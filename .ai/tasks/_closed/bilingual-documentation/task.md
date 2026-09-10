# Tarea: bilingual-documentation

**Creada:** 2026-09-10 · **Tamaño:** large · **Owner:** (sin asignar) · **Rol:** (sin asignar)

## Objetivo
Establecer una documentación bilingüe sostenible: el español conserva la
autoridad editorial del proyecto inicial y el inglés permite a colaboradores
internacionales evaluar, instalar y contribuir sin depender de una traducción
informal.

## Incluido en el alcance
- Política explícita de idiomas y de sincronización de traducciones.
- Navegación y documentación de incorporación en inglés.
- Enlaces cruzados claros entre la documentación canónica en español y sus
  equivalentes o resúmenes en inglés.

## Explícitamente fuera de alcance
- Traducir resultados, hipótesis o material de una futura evaluación
  científica de Continuum.
- Cambiar comportamiento del CLI, protocolo, licencias o procesos de release.

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `README.md`, `README.en.md`
- `CONTRIBUTING.md`, `CONTRIBUTING.en.md`
- `docs/LANGUAGE_POLICY.md`, `docs/LANGUAGE_POLICY.en.md`, `docs/en/README.md`
- `.ai/tasks/bilingual-documentation/*`, `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`
- `docs/research-protocol.md`, `docs/ux-metrics-roadmap.md`

## Contexto mínimo sugerido
Según el tamaño declarado arriba, no cargues más de lo necesario:

| Tamaño  | Techo de lectura inicial orientativo |
|---------|----------------------------------------|
| small   | 1-3 archivos concretos, sin explorar carpetas completas |
| medium  | 1 módulo/dominio, usar `rg`/`grep` para localizar antes de leer |
| large   | fragmentar con `continuum packetize`; considerar dividir en subtareas |
