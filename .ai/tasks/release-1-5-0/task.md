# Tarea: release-1-5-0

**Creada:** 2026-09-13 · **Tamaño:** medium · **Owner:** mikeroguez · **Rol:** (sin asignar)

## Objetivo
Preparar y publicar la versión 1.5.0 con todos los cambios incorporados desde
v1.4.1, dejando documentado el proceso de revisión y protección de `main`.

## Incluido en el alcance
- Actualizar la versión en el CLI distribuible y el metarrepositorio.
- Registrar la nota de versión y actualizar referencias visibles.
- Definir CODEOWNERS y el acuerdo de votación entre mikeroguez y wada8a.
- Preparar el Pull Request y configurar la protección remota de `main`.

## Explícitamente fuera de alcance
- Cambios en la lógica funcional del CLI no relacionados con el release.
- Publicación de datos personales, secretos o transcripciones.

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors
oportunistas.

- `.ai/HANDOFF.md`
- `.ai/tasks/release-1-5-0/`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `CONTRIBUTING.en.md`
- `README.md`
- `README.en.md`
- `.github/CODEOWNERS`
- `tools/_continuum/__init__.py`
- `template/tools/_continuum/__init__.py`

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
