# Plan de ejecución: catalogo-roles

- [x] 1. `.ai/roles/<pack>/<slug>.md` × 23 (comun=9, software=6, investigacion=3, contenido-educativo=5)
- [x] 2. `config.json`: campo `roles.packs`; `common.py` DEFAULT_CONFIG
- [x] 3. `roles.py`: descubrir roles activos, `list_roles`, `sync` (Claude Code subagents)
- [x] 4. `__main__.py`: subcomandos `roles list` / `roles sync`
- [x] 5. `tasks.py` + plantilla TASK.md: `--role` en `task start`
- [x] 6. `handoff.py` + plantilla HANDOFF.md: `--role` en `handoff`
- [x] 7. `doctor.py`: valida que los role_packs declarados existan
- [x] 8. Sincronizar copia autoalojada (raíz) desde `template/`
- [ ] 9. Docs: AI_COLLABORATION.md §9, ARCHITECTURE.md, decision-log.md ADR-009, README.md, CHANGELOG.md
- [x] 10. Tests: `test_roles.py` + extensiones a `test_tasks.py`/`test_handoff.py` (53/53 OK)
- [ ] 11. `continuum doctor` + suite completa en verde, cerrar tarea

## Estado actual
Paso 1 en curso.
