# .githooks

Vacío a propósito en la plantilla. Se puebla al correr:

```bash
tools/continuum install-hooks
```

Eso escribe `.githooks/pre-commit` y apunta `core.hooksPath` a esta carpeta.
Si el proyecto ya usa otro `hooksPath` (p. ej. Husky), fusiona los hooks a
mano en vez de sobreescribir.
