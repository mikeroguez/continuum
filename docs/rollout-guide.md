# Guía de adopción en un proyecto existente

Procedimiento para incorporar Continuum en un proyecto que ya está en
desarrollo. Distingue tres puntos de partida distintos, observados en la
auditoría descrita en `ARCHITECTURE.md` §1 (referencias "Proyecto A–E" según
esa misma tabla). No sustituye a `README.md` — asume que la instalación
mecánica (`git subtree add`) ya se explicó ahí.

## Antes de empezar

```bash
tools/continuum doctor
```

Ejecutar primero sobre una copia de prueba de la plantilla, sin necesidad de
tenerla instalada aún en el proyecto destino. En el proyecto destino:
confirmar `git status` limpio y trabajar sobre una rama dedicada — la
instalación toca varios archivos de la raíz del repositorio.

## Caso 1 — Protocolo previo maduro (perfil del Proyecto A/E)

El proyecto ya tiene `AI_COLLABORATION.md`, `AGENTS.md`, `CLAUDE.md`,
`GEMINI.md`, un archivo de estado de desarrollo, `.ai/tasks/` con historial
real, y ADRs. Es una migración, no una instalación desde cero.

1. Comparar el `AI_COLLABORATION.md` existente contra
   `template/AI_COLLABORATION.md`: el contenido específico del proyecto
   (identificadores de requisitos, convenciones propias) se conserva dentro
   de la sección correspondiente de la plantilla; no se descarta.
2. Mover el archivo de estado de desarrollo existente a
   `.ai/state/estado-dev.md` y ejecutar `continuum memory-split-legacy` para
   dividirlo en índice más archivos de tema en `.ai/state/topics/`. Revisar
   el resultado: la migración fusiona en lugar de sobrescribir cuando ya
   existe un tema con el mismo nombre, y señala esos casos para revisión
   manual.
3. Revisar las tareas históricas en `.ai/tasks/`: cerrar con `continuum task
   close --force` las que ya estén resueltas en el código aunque no se haya
   escrito su handoff en su momento; conservar solo las genuinamente activas.
4. Eliminar directorios de configuración por proveedor que estén vacíos y
   sin control de versiones — no aportan soporte real (ver `ARCHITECTURE.md`
   §2, principio 5).
5. Ejecutar `tools/continuum install-hooks` y verificar que no entre en
   conflicto con scripts de verificación ya existentes en el proyecto; si
   los hay, conviene que el hook de pre-commit invoque ambos.

## Caso 2 — Protocolo declarado pero memoria desactualizada (perfil del Proyecto B/C)

El protocolo está declarado, pero el archivo de estado de desarrollo no
refleja el estado real del proyecto, y/o `.ai/tasks/` no tiene contenido
real o quedó con tareas sin retomar.

1. Antes de instalar nada, actualizar el archivo de estado de desarrollo a
   mano una vez más, para no migrar un snapshot que ya se sabe
   desactualizado. En el caso de un archivo de memoria muy grande (decenas
   de KB, siguiendo el perfil del Proyecto C), `continuum
   memory-split-legacy` va a generar varios temas extensos de una sola vez:
   es un resultado esperado — revisar y seguir dividiendo cualquier tema que
   supere las ~300 líneas que `continuum doctor` recomienda.
2. Eliminar cualquier duplicado obsoleto del archivo de estado detectado
   durante la migración, en el mismo commit que instala la plantilla.
3. Decidir el destino de cualquier herramienta de gestión de tareas previa
   sin uso reciente: si nadie la usa desde hace meses, retirarla en lugar de
   mantener dos herramientas equivalentes en paralelo.

## Caso 3 — Sin mecanismo previo (perfil del Proyecto D)

Instalación limpia, sin migración.

1. Instalar la plantilla completa según `README.md`.
2. Redactar `.ai/state/estado-dev.md` desde cero. Un archivo de registro de
   cambios orientado a usuario final (changelog de producto) puede servir
   como fuente para las secciones "Decisiones" y "Stack", pero no lo
   reemplaza: cumplen funciones distintas.
3. Si existe más de una copia de un mismo archivo de referencia (por
   ejemplo, un changelog duplicado entre la raíz y un subdirectorio de
   build), resolver esa divergencia antes de continuar y documentar la
   decisión como el primer ADR del proyecto.

## Después de instalar (los tres casos)

```bash
tools/continuum doctor
```

El resultado esperado es cero problemas críticos. Las advertencias son
normales en una adopción inicial (memoria más grande que el objetivo, tareas
antiguas pendientes de revisión); se registran como pendientes de limpieza
en el primer ciclo de trabajo, no se resuelven todas en el commit que
instala la plantilla.
