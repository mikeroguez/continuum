# Tarea: manuals-and-minimal-protocol

**Creada:** 2026-09-10 · **Tamaño:** large · **Owner:** (sin asignar) · **Rol:** (sin asignar)

## Objetivo
Afinar el protocolo operativo de Continuum con base en evidencia sobre contexto
y crear guías bilingües separadas para personas y agentes.

## Incluido en el alcance
- Manuales instalables en `template/docs/` para personas y agentes.
- Ajustes al protocolo para privilegiar divulgación progresiva y verificaciones
  mecánicas sobre reglas extensas.
- Enlaces y política de idiomas actualizados.

## Explícitamente fuera de alcance
- Cambiar comportamiento del CLI, instrumentación experimental o recolección
  de datos.
- Publicar, versionar o liberar una nueva plantilla.

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `AI_COLLABORATION.md`, `template/AI_COLLABORATION.md`
- `README.md`, `README.en.md`, `docs/LANGUAGE_POLICY*.md`
- `template/docs/*`, `.ai/tasks/manuals-and-minimal-protocol/*`, `.ai/HANDOFF.md`

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
