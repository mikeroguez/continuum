<div align="center">

# ♾️ Continuum

**Protocolo y herramientas de memoria persistente para equipos que trabajan con múltiples asistentes de IA en Git.**

[![Version](https://img.shields.io/badge/version-v1.3.1-blue.svg)](CHANGELOG.md)
[![continuum doctor](https://github.com/mikeroguez/continuum/actions/workflows/continuum-doctor.yml/badge.svg?branch=main)](https://github.com/mikeroguez/continuum/actions/workflows/continuum-doctor.yml)
[![tests](https://github.com/mikeroguez/continuum/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/mikeroguez/continuum/actions/workflows/tests.yml)
[![Licencia MIT](https://img.shields.io/badge/licencia-MIT-green.svg)](LICENSE)

[🌐 Read in English](README.en.md) · [📜 Política de Idiomas](docs/LANGUAGE_POLICY.md) · [💬 GitHub Repository](https://github.com/mikeroguez/continuum)

---

### 📖 Guías Rápidas
[👥 Manual para Desarrolladores](template/docs/como-usar-continuum.md) · [🤖 Guía para Agentes IA](template/docs/guia-para-agentes.md) · [🗺️ Índice de Documentación](docs/README.md)

---

</div>

## 📌 ¿Qué es Continuum?

**Continuum** es un marco ligero e infraestructura basada en Git para **persistir el contexto vivo de un proyecto de software directamente en el repositorio**, eliminando la dependencia del historial volátil del chat con asistentes de IA.

```mermaid
flowchart LR
    A[👨‍💻 Desarrollador] -->|Sesión 1| B(Claude Code)
    B -->|Persiste en| C[(📁 .ai / Git Memory)]
    C -->|Carga contexto| D(Codex / Gemini)
    D -->|Sesión 2| E[🚀 Continuidad Perfecta]
```

### ✨ Principios Clave:
- 🔄 **Interoperabilidad Universal**: Compatible con la convención [`AGENTS.md`](https://agents.md) (Claude Code, Codex, Gemini CLI, Cursor, etc.) sin traducir ni duplicar contexto.
- ⚡ **Continuidad sin Pérdidas**: Las sesiones pueden interrumpirse por límite de tokens o rotación de proveedor sin perder el hilo de trabajo.
- 👥 **Colaboración Multi-Agente Segura**: Personas y asistentes trabajan en paralelo sobre el mismo repositorio sin sobrescribir ni pisar código.
- 📉 **Optimización de Contexto**: El arranque de cualquier sesión consume solo **~2.5k tokens** fijos frente a historiales inflados de decenas de miles de tokens.

---

## 🚀 Inicio Rápido

> [!TIP]
> **Instalación recomendada vía `git subtree`:**
> Se distribuye como plantilla base utilizando `git subtree` para mantener el proyecto limpio y sincronizable de forma permanente.

### 1️⃣ Instalar en un proyecto existente

```bash
# Agregar el remoto de Continuum (una sola vez)
git remote add continuum https://github.com/mikeroguez/continuum.git

# Montar la plantilla en la raíz usando la rama export
git subtree add --prefix=. continuum export --squash -m "chore: instala Continuum v1.3.1"
```

### 2️⃣ Configuración e Inicialización

```bash
# Configurar el archivo .ai/config.json con los datos del proyecto
$EDITOR .ai/config.json

# Instalar githooks locales y diagnosticar el estado del proyecto
tools/continuum install-hooks
tools/continuum doctor
```

---

## 🧩 Piezas Principales del Protocolo

| Componente | Archivo / Ruta | Propósito | Cuándo se lee |
| :--- | :--- | :--- | :--- |
| **Protocolo Canónico** | [`AI_COLLABORATION.md`](AI_COLLABORATION.md) | Reglas operativas únicas y obligatorias | En el arranque de cada sesión |
| **Continuidad Inmediata** | [`.ai/HANDOFF.md`](.ai/HANDOFF.md) | Resumen del último estado, pruebas y siguientes pasos | Al iniciar/retomar trabajo |
| **Índice de Memoria** | [`.ai/state/estado-dev.md`](.ai/state/estado-dev.md) | Mapa ligero de memoria del proyecto (<80 tokens) | Al arrancar |
| **Temas Específicos** | `.ai/state/topics/` | Desglose modular (arquitectura, decisiones, pendientes) | Bajo demanda |
| **Motor CLI** | [`tools/continuum`](tools/continuum) | Diagnóstico, tareas, sincronización y métricas | Vía terminal |

---

## 🛠️ Referencia Rápida del CLI (`tools/continuum`)

### 📋 Diagnóstico y Sesión
```bash
tools/continuum                        # doctor: Diagnóstico completo del estado del proyecto
tools/continuum session start          # Inicio de sesión: lee handoff, tareas y sugiere contexto
tools/continuum session end --auto     # Cierre de sesión asistido con validación de calidad
tools/continuum status                 # Estado compacto y siguiente acción recomendada
```

### 🎯 Gestión de Tareas (`task`)
```bash
tools/continuum task start <slug> --size small|medium|large   # Crear tarea acotada
tools/continuum task claim <slug> <responsable>              # Declarar ownership
tools/continuum task close <slug>                           # Cerrar y archivar tarea
```

### 🔄 Sincronización y Actualizaciones (`sync`)
```bash
tools/continuum sync --apply           # Sincronizar plantilla con el repositorio remoto
tools/continuum install-hooks          # Instalar pre-commit githook local
```

---

## 🛡️ Seguridad e Integridad en Git

> [!IMPORTANT]
> **Sin contaminación de historial**:
> Al usar `--squash`, `git subtree` añade **únicamente 1 commit** al historial del proyecto destino. Ningún historial extenso o commits individuales de Continuum se mezclan ni se transfieren a clones de red de otros miembros del equipo.

---

## 📖 Documentación Completa

- [👥 **Manual de Uso para Personas y Equipos**](template/docs/como-usar-continuum.md) — Incluye guía de adopción, casos de uso en equipo y plantillas de prompts.
- [🤖 **Guía de Conducta para Agentes IA**](template/docs/guia-para-agentes.md) — Directivas y límites operativos para asistentes.
- [🏛️ **Decisiones de Arquitectura (ADRs)**](docs/decision-log.md) — Historial de decisiones técnicas de Continuum.
- [🤝 **Guía de Contribución**](CONTRIBUTING.md) — Estándares de commits, Pull Requests y lanzamientos SemVer.

---

<div align="center">

**Continuum** está mantenido por [Mike Roguez](https://mikeroguez.me) bajo Licencia [MIT](LICENSE).

</div>
