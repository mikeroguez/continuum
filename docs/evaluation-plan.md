# Plan operativo para evaluar Continuum

Este documento convierte el [protocolo de evaluación](research-protocol.md) en
una secuencia ejecutable. Es un plan previo a datos: ningún paso autoriza
recolectar, compartir o interpretar resultados sin completar los controles de
privacidad y prerregistro.

## Fase 0 — Preparación y aprobación

- [ ] Confirmar que cada repositorio y tarea puede utilizarse para investigación.
- [ ] Obtener consentimiento explícito de cualquier persona o equipo externo.
- [ ] Obtener revisión ética o institucional cuando aplique.
- [ ] Escribir el manifiesto de tareas y congelarlo en un commit.
- [ ] Prerregistrar hipótesis, presupuesto, tamaño de muestra, exclusiones y
  análisis antes de la fase confirmatoria.

Un manifiesto debe contener, como mínimo:

```text
trial_id, repository_id, starting_commit, task_id, task_stratum,
predecessor_model, successor_model, condition, repetition,
interruption_rule, time_budget, token_budget, acceptance_command,
environment_hash, randomization_seed
```

`repository_id` y `task_id` deben ser pseudónimos si el repositorio no es
público. El manifiesto no incluye rutas locales, URLs privadas, prompts con
datos sensibles ni secretos.

## Fase 1 — Piloto de instrumentación

El piloto no prueba eficacia. Su objetivo es responder estas preguntas:

- ¿La restauración de un árbol parcial produce el mismo estado en cada ensayo?
- ¿El comando de aceptación distingue realmente una solución de un fallo?
- ¿La plataforma registra tokens y eventos con la precisión necesaria?
- ¿El punto de interrupción deja trabajo parcial útil, pero no una solución
  completa?
- ¿El exportado puede anonimizarse sin perder las variables analíticas?

Documentar cambios al protocolo provocados por el piloto. No unir sus ensayos a
la muestra confirmatoria.

## Fase 2 — Construir el harness

Antes de recolectar datos confirmatorios, el repositorio necesita scripts
versionados que hagan lo siguiente sin intervención manual:

1. Preparar un worktree limpio en el commit inicial de una tarea.
2. Lanzar el agente precursor con su configuración registrada.
3. Interrumpirlo usando la regla declarada y congelar el árbol parcial.
4. Crear el handoff de Continuum para la condición C.
5. Restaurar copias idénticas de ese árbol para A, B y C.
6. Ejecutar el sucesor bajo la condición asignada.
7. Ejecutar el comando de aceptación y registrar el resultado.
8. Guardar un registro de ensayo local y anonimizable.

El harness debe fallar de forma segura: no ejecutar comandos de producción,
no acceder a credenciales ni enviar datos. Debe borrar o aislar worktrees y
artefactos temporales después de verificar que la exportación requerida ya fue
creada.

## Fase 3 — Esquema de datos mínimo

Por cada ensayo se guarda un registro local estructurado con:

| Grupo | Campos permitidos |
| --- | --- |
| Identidad experimental | `trial_id`, condición, repetición, semilla, identificadores pseudónimos |
| Configuración | versión de Continuum, agente/modelo, fecha, presupuesto, hash de entorno |
| Ejecución | inicio/fin, tokens disponibles, eventos de herramienta, interrupciones, razón de término |
| Resultado | estado de pruebas de aceptación, duración, conteo de intervenciones y aclaraciones |
| Integridad | hash del árbol inicial, del estado congelado y del script de evaluación |

No guardar prompts completos, respuestas completas, código, diffs, rutas
locales, nombres de cuentas, URLs de remotos, claves ni contenido de handoffs
sin una revisión específica. Si un análisis requiere texto, usar una muestra
consentida, minimizada y revisada por separado.

## Fase 4 — Ejecución confirmatoria

- Ejecutar el orden de ensayos a partir de la semilla prerregistrada.
- Mantener inmutable el manifiesto; adendas nuevas reciben fecha y justificación.
- Correr cada condición con un worktree independiente y sin conversación
  previa del sucesor.
- Registrar fallas de infraestructura, pero no repetir selectivamente ensayos
  desfavorables.
- Mantener las pruebas de aceptación separadas de la información disponible al
  agente cuando sea viable.

## Fase 5 — Análisis y publicación

- Generar tablas y figuras solo mediante scripts versionados.
- Informar todos los ensayos, exclusiones y desviaciones del prerregistro.
- Reportar corrección y costo juntos: ahorrar tokens no compensa resolver menos
  tareas.
- Distinguir resultados exploratorios de confirmatorios.
- Publicar únicamente datos, scripts y artefactos que hayan pasado revisión de
  licencia, privacidad y consentimiento.

## Criterios para iniciar la fase confirmatoria

No se inicia hasta que se cumplan todos:

- [ ] Prerregistro fechado e inmutable.
- [ ] Harness reproducible y probado en un piloto.
- [ ] Comandos de aceptación válidos para cada tarea.
- [ ] Modelo de consentimiento y anonimización revisado.
- [ ] Plan de análisis y criterios de exclusión fijados.
- [ ] Revisión humana de los materiales que podrían hacerse públicos.
