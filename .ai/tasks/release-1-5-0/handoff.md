# Handoff — release-1-5-0

## Objetivo
Preparar la versión 1.5.0 desde v1.4.1, documentar los cambios y dejar
protegida la colaboración sobre `main`.

## Cambios realizados
- Versiones raíz y plantilla actualizadas a `1.5.0`.
- CHANGELOG y badges de README preparados para v1.5.0.
- CONTRIBUTING documenta revisión, votación entre mikeroguez y wada8a y
  publicación sin `--force`.
- Añadido `.github/CODEOWNERS` con ambos mantenedores.

## Validación
- `python3 -m unittest discover -s tests -t .` — OK, 113 tests.
- `python3 tools/continuum doctor` — OK.
- `python3 tools/continuum release v1.5.0 --dry-run` — OK.
- `git diff --check` — OK.

## Pendiente
- Commit, push de la rama, apertura del PR contra `main`.
- Aplicar protección remota de `main` después de verificar los nombres de
  checks de CI.
- Crear el tag y la publicación GitHub tras la aprobación y merge del PR.
