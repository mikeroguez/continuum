# Piloto local de continuidad

Este proyecto comprueba la **instrumentación** del diseño de evaluación de
Continuum. No mide eficacia ni autoriza un estudio confirmatorio. Su tarea es
deliberadamente pequeña, autocontenida y sin red, credenciales ni datos
personales.

## Qué verifica

Para el mismo estado parcial, `prepare_trial.py` crea directorios nuevos para
tres condiciones:

| Condición | Material disponible al sucesor |
| --- | --- |
| `A` | Código parcial y pruebas de aceptación. |
| `B` | A más una guía mínima de comandos, límites y alcance. |
| `C` | B más una instalación local de Continuum, índice, tarea y handoff. |

El estado parcial es el mismo en los tres casos. El agente recibe la misma
consigna: completar `render_report` sin modificar las pruebas. Un agente o
persona independiente debe ejecutar cada condición en una sesión nueva; no
reutilices conversación, caché ni directorio de trabajo entre condiciones.

## Preparar un ensayo

Desde la raíz de este repositorio, usa un directorio temporal nuevo por ensayo:

```bash
python3 evaluation/pilot/prepare_trial.py \
  --condition C --trial-id pilot-c-001 --destination /private/tmp/pilot-c-001
```

Entrega al agente sucesor esta consigna, igual para A, B y C:

```text
Completa la función render_report en el proyecto. No modifiques las pruebas.
Trabaja solo con los archivos y la documentación disponibles en este directorio.
Ejecuta las pruebas de aceptación antes de terminar.
```

En C, el agente puede seguir el protocolo instalado; A y B no deben recibir
archivos de C ni una transcripción de una sesión previa.

## Verificar y registrar de forma local

Después de que el sucesor termine:

```bash
python3 evaluation/pilot/verify_trial.py \
  --trial-directory /private/tmp/pilot-c-001 \
  --trial-id pilot-c-001 --condition C \
  --record evaluation/pilot/local-runs/pilot.jsonl
```

El verificador ejecuta únicamente `python -m unittest discover -s tests -t .`.
El registro guarda identificador pseudónimo, condición, resultado, duración y
hashes de integridad; no guarda prompts, respuestas, diffs, rutas locales ni
contenido de handoffs. `local-runs/` está ignorado por Git.

## Criterios del piloto

Antes de mirar resultados de agentes, confirma que:

1. Cada condición parte del mismo hash de estado parcial.
2. La prueba falla antes de completar la tarea y pasa después de una solución
   correcta.
3. El contenido de A, B y C coincide con la tabla anterior.
4. El registro no contiene datos prohibidos.

Los resultados de este piloto sirven para corregir la instrumentación. No se
mezclan con una muestra confirmatoria ni se convierten en afirmaciones públicas
sin prerregistro, revisión de privacidad y las aprobaciones indicadas en
[`docs/evaluation-plan.md`](../../docs/evaluation-plan.md).
