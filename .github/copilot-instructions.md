# Instrucciones del repositorio

Continuum es un protocolo y CLI de memoria persistente para equipos que
trabajan con varios asistentes de IA sobre el mismo repositorio.

## Integración específica de este cliente

- Este archivo es la instrucción global para GitHub Copilot; las reglas comunes
  siguen viviendo en `AI_COLLABORATION.md`.
- Cuando una tarea activa un archivo bajo `.github/instructions/`, aplica
  también su instrucción por ruta sin reemplazar el protocolo común.
- Los roles de `.ai/roles/` se proyectan a `.github/agents/*.agent.md` mediante
  `python3 tools/continuum roles sync --provider copilot`; no edites esos
  archivos generados directamente.
- Los agentes personalizados orientan la ejecución, pero no autorizan cambios
  fuera del alcance de la tarea ni sustituyen la revisión humana.

## Protocolo obligatorio

- Lee primero `.ai/HANDOFF.md`, `.ai/state/estado-dev.md` y la tarea relevante
  antes de cambiar archivos.
- `AI_COLLABORATION.md` es la fuente única de verdad. `AGENTS.md`, `CLAUDE.md`,
  `GEMINI.md` y este archivo no deben crear reglas divergentes.
- Conserva la separación entre la memoria versionada (`.ai/`) y el código.
- Para tareas medianas o grandes usa la carpeta de tarea correspondiente y
  deja un handoff antes de terminar o cuando el contexto se agote.
- No registres secretos, credenciales, datos personales ni transcripciones en
  archivos versionados.

## Validación de cambios

Ejecuta, cuando corresponda:

```bash
python3 -m unittest discover -s tests -t .
python3 tools/continuum doctor
```

Para cambios distribuibles, actualiza también `template/` y revisa que no haya
divergencia entre la raíz y la plantilla. No añadas dependencias externas sin
justificación explícita.

## Criterios para revisión de cambios

Cuando actúes como revisor, prioriza hallazgos de alta confianza sobre estilo:

- Corrección funcional y manejo explícito de errores.
- Pruebas suficientes para el comportamiento cambiado.
- Seguridad, secretos, validación de entradas y datos sensibles.
- Consistencia con `AI_COLLABORATION.md`, la configuración y el handoff.
- Paridad entre la implementación distribuible en `template/` y la raíz.
- Drift o archivos generados editados manualmente.

Describe el impacto, la ubicación y una corrección concreta. No marques como
defecto una preferencia de estilo sin impacto. La revisión de IA no sustituye
la aprobación humana ni cambia las reglas de protección de ramas.

## Continuidad

Antes de finalizar, actualiza `.ai/HANDOFF.md`. Si el cliente activo no ofrece
un hook de cierre, puedes generar el borrador con:

```bash
python3 tools/continuum handoff --auto --provider <proveedor>
```

Haz cambios quirúrgicos, ejecuta las validaciones disponibles y deja claros
los riesgos o pasos pendientes en el handoff.

<!-- Continuum source: AI_COLLABORATION.md sha256:63d9e776e4557c662ed423e18edef09d34e35a1f8358b095f814e7a8866372ec -->
