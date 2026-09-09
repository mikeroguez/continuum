# Protocolo de Investigación y Evidencia Local — Continuum

## 1. Declaración de Objetivo e Hipótesis

El protocolo Continuum investiga el impacto de persistir la memoria viva del desarrollo de software dentro del árbol de Git en lugar de depender exclusivamente del historial de contexto de chats de modelos de lenguaje (LLMs).

### Hipótesis Principal ($H_1$)
La estructuración de memoria de IA acotada mediante índices pequeños (`estado-dev.md`), temas bajo demanda y buzones de handoff cortos (`HANDOFF.md`) reduce el costo acumulado de tokens de arranque por sesión en al menos un **40%** sin degradar la precisión ni la continuidad entre sesiones.

## 2. Variables de Estudio

### Variables Independientes
- Mecanismo de persistencia (Continuum vs. Historial monolítico de conversación).
- Tamaño de tarea declarada (`small`, `medium`, `large`).

### Variables Dependientes
- **Presupuesto de arranque (tokens)**: Tokens consumidos antes de iniciar la primera iteración útil de código.
- **Continuidad operacional (0-1)**: Capacidad de retomar el trabajo tras una interrupción sin requerir aclaraciones adicionales del usuario.
- **Fricción de mantenimiento**: Frecuencia de intervenciones manuales necesarias para corregir estado o resolver duplicados.

## 3. Amenazas a la Validez

1. **Sesgo de Observación**: Evaluación realizada sobre repositorios de desarrollo propio.
2. **Variabilidad de Modelos**: Respuestas divergentes entre proveedores (Claude, Codex, Gemini).
3. **Control de Confidencialidad**: Anonimización estricta mediante `continuum metrics export --anonymize` para prevenir la divulgación de rutas locales, claves o identificadores privados.

## 4. Replicabilidad

Toda la recolección de métricas se ejecuta mediante scripts auditables en Python estándar (`tools/_continuum/metrics.py`) y pruebas automatizadas ejecutables localmente vía:

```bash
python3 tools/continuum metrics report
python3 tools/continuum metrics export --anonymize
python3 tools/continuum metrics compare
```

## 5. Consentimiento, Privacidad y Modelo Opt-In / Opt-Out

1. **Cero Telemetría Remota por Defecto**:
   Continuum es un protocolo 100% local. No existe envío automático de datos, métricas ni eventos a ningún servidor externo o servicio de analítica.

2. **Propiedad y Aislamiento de Datos**:
   - Los datos de rendimiento y métricas residen únicamente en el sistema de archivos local (`.ai/metrics/`).
   - Los eventos de sesión se guardan en `.ai/metrics/events.jsonl`, archivo incluido en `.gitignore` por defecto para impedir su publicación accidental.

3. **Consentimiento Explícito (Opt-In para Exportación/Estudios)**:
   - Los datos solo salen del entorno local cuando el usuario ejecuta **manualmente** un comando de exportación (`continuum metrics export`).
   - Toda exportación destinada a investigación o reporte público debe usar la bandera `--anonymize`, que ofusca identificadores de commit (hash de 7 caracteres sin retorno al repositorio), elimina nombres de ramas personales y omite nombres de usuario y rutas locales.

4. **Opción de No Participación (Opt-Out Total)**:
   - Un desarrollador o equipo que no desee recolectar métricas locales puede ignorar los comandos de `metrics` sin afectar ninguna funcionalidad principal de Continuum (`context`, `tokens`, `task`, `doctor`, `session`, etc. operan al 100% independientemente).
   - Para desactivar la creación de snapshots o eventos, basta con deshabilitar la opción en `config.json` o eliminar el directorio `.ai/metrics/`.
