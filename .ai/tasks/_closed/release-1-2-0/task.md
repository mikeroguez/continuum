# Tarea: release-1-2-0

**Creada:** 2026-09-10 · **Tamaño:** medium · **Owner:** (sin asignar) · **Rol:** (sin asignar)

## Objetivo
Liberar Continuum 1.2.0 para publicar la capacidad de configurar la rama de
plantilla en `continuum sync`, ya integrada en `main`.

## Incluido en el alcance
- Actualizar la versión de la plantilla y de la copia autoalojada.
- Documentar el cambio y publicar tag, rama `export` y release.

## Explícitamente fuera de alcance
- Cambios de comportamiento adicionales.

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `template/tools/_continuum/__init__.py`
- `tools/_continuum/__init__.py`
- `CHANGELOG.md`, `README.en.md`
- `.ai/tasks/release-1-2-0/*`, `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- _(rutas específicas relevantes a esta tarea)_

## Contexto mínimo sugerido
Según el tamaño declarado arriba, no cargues más de lo necesario:

| Tamaño  | Techo de lectura inicial orientativo |
|---------|----------------------------------------|
| small   | 1-3 archivos concretos, sin explorar carpetas completas |
| medium  | 1 módulo/dominio, usar `rg`/`grep` para localizar antes de leer |
| large   | fragmentar con `continuum packetize`; considerar dividir en subtareas |
