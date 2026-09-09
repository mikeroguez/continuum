# Tarea: suite-de-pruebas

**Creada:** 2026-09-09 · **Tamaño:** medium · **Owner:** claude

## Objetivo
Suite de tests automatizada (stdlib `unittest`, sin dependencias nuevas)
para `template/tools/_continuum/`, que hasta ahora solo se había validado
con smoke tests manuales en `/tmp`.

## Incluido en el alcance
- Tests unitarios/integración para common, doctor, tasks, handoff, memory,
  packets, bootstrap.
- Tests de regresión específicos para los dos bugs reales ya encontrados y
  corregidos a mano: colisión de nombres en `memory-split-legacy`, y ruta
  relativa sin resolver en `packetize`.
- Workflow de CI que corra la suite (solo en este meta-repo, no en `template/`).

## Explícitamente fuera de alcance
- No se toca la lógica de `template/tools/_continuum/` salvo que un test
  revele un bug real (en cuyo caso se documenta aparte, no se mezcla).
- No se agrega pytest ni ninguna dependencia externa — sigue siendo
  Python estándar únicamente.

## Write-set (archivos que se espera tocar)
- `tests/` (nuevo)
- `.github/workflows/tests.yml` (nuevo, solo en la raíz del meta-repo)
- `CONTRIBUTING.md` (agregar cómo correr los tests)

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
