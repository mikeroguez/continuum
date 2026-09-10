# Fixture sintético para revisar cambios

Este archivo es deliberadamente defectuoso y no forma parte de la aplicación.
No lo ejecutes ni copies sus patrones a código productivo. Sirve para validar
que una revisión identifica problemas conocidos sin depender de un proveedor
concreto.

## Caso A: fallo funcional

```python
def normalize_provider(value):
    return value.strip().lower() if value else "claude"
```

**Defecto esperado:** un valor vacío se convierte silenciosamente en un
proveedor válido en vez de señalar entrada inválida; eso puede ejecutar un
flujo distinto al solicitado.

## Caso B: cobertura insuficiente

```python
def test_normalize_provider():
    assert normalize_provider("Claude") == "claude"
```

**Defecto esperado:** falta cobertura para `None`, cadena vacía y proveedores
desconocidos; la prueba no demuestra el contrato completo.

## Caso C: divergencia de fuente canónica

```markdown
<!-- AI_COLLABORATION.md dice que el handoff es obligatorio -->
Este cliente puede omitir el handoff al terminar una tarea.
```

**Defecto esperado:** una instrucción específica contradice el protocolo
canónico y crea dos fuentes de verdad.

## Caso D: manejo inseguro de datos

```python
def debug_token(token):
    print(f"token={token}")
```

**Defecto esperado:** se expone un secreto en logs; el comentario debe pedir
eliminarlo o aplicar una técnica segura de redacción.

## Resultado esperado de la revisión

Un revisor útil debe reportar cada caso con ubicación, impacto y corrección,
sin convertir preferencias de estilo en hallazgos. Tras corregirlos, una nueva
revisión debe dejar de reportar esos cuatro defectos.
