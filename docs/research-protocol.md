# Protocolo de evaluación de Continuum

**Estado:** diseño previo a la recolección de datos. Este documento no reporta
resultados ni afirma que Continuum mejore el desempeño de agentes.

**Propósito:** servir como base de prerregistro antes de ejecutar un estudio.
El plan operativo reproducible está en
[`evaluation-plan.md`](evaluation-plan.md). Si ambos documentos difieren, este
protocolo define las preguntas, comparaciones y análisis; el plan define cómo
se ejecuta cada ensayo.

## 1. Pregunta de investigación

Cuando una tarea de software queda interrumpida y la retoma una sesión nueva,
¿un handoff estructurado y memoria de proyecto bajo demanda reducen el costo de
retomar el trabajo sin empeorar su corrección?

La pregunta trata de **continuidad tras una interrupción**, no de si un archivo
de instrucciones hace a un modelo mejor programador en general. También separa
la guía mínima del mecanismo de handoff: son intervenciones distintas.

## 2. Diseño y condiciones

La unidad de análisis es una ejecución de relevo: un agente sucesor retoma un
estado de trabajo parcial congelado. Cada estado parcial se evalúa con una
condición elegida aleatoriamente y con repeticiones independientes.

| Código | Condición | El agente sucesor puede consultar |
| --- | --- | --- |
| A | Control | Estado parcial del repositorio, código y pruebas habituales. |
| B | Guía mínima | A + instrucciones breves con comandos, límites y rutas no inferibles. |
| C | Continuum | B + índice de memoria y handoff estructurado pertinente a la tarea. |

La comparación primaria es **C frente a A**. La comparación **B frente a A**
estima el efecto de la guía mínima; **C frente a B** estima el valor adicional
del estado y handoff. No se debe atribuir a Continuum un efecto que pertenezca
a cualquiera de esas dos capas sin reportar las tres comparaciones.

## 3. Hipótesis y resultados

No se fija un porcentaje de mejora antes de un piloto que permita estimar
varianza y un umbral de importancia práctica. El análisis debe informar tamaños
de efecto e intervalos de confianza, incluso si no hay diferencia concluyente.

- **H1 — eficiencia de relevo.** En C, el costo del sucesor hasta completar o
  agotar el presupuesto será menor que en A.
- **H2 — corrección.** C no tendrá una tasa de resolución materialmente menor
  que A. El margen de no inferioridad se definirá y justificará en el
  prerregistro final, después del piloto y antes de mirar datos confirmatorios.
- **H3 — mecanismo.** Si C supera a A, B permitirá distinguir cuánto corresponde
  a instrucciones mínimas y cuánto al handoff y memoria.

Los resultados primarios son:

1. **Resolución:** las pruebas de aceptación de la tarea pasan dentro del
   presupuesto asignado (sí/no).
2. **Costo de relevo:** tokens de entrada y salida, eventos de herramienta y
   tiempo de pared del agente sucesor hasta resolución o agotamiento.

Los resultados secundarios son número de solicitudes de aclaración, cambios
revertidos, ejecuciones de pruebas, intervenciones humanas y una evaluación
ciega de completitud del handoff. Ninguno se presentará como resultado primario
si no se declaró antes de ver los datos.

## 4. Tareas y estados de relevo

Cada tarea elegible debe:

- provenir de un repositorio propio o público con derecho explícito de uso;
- tener una versión fija de Git, descripción conservada y pruebas de aceptación
  ejecutables sin acceso a datos privados;
- poder completarse dentro de un presupuesto predefinido; y
- estar clasificada antes de correr el estudio por repositorio y complejidad.

Se excluyen tareas que dependan de secretos, servicios de pago, producción,
datos personales, decisiones irreversibles o revisión humana no disponible. La
lista de tareas, criterios de inclusión, presupuesto y reglas de exclusión se
congelan en un manifiesto versionado antes de la fase confirmatoria.

Para crear un estado de relevo, un agente precursor trabaja desde el mismo
commit de partida y se interrumpe en un punto determinista declarado en el
manifiesto —por ejemplo, tras un número fijo de eventos de herramienta y al
menos una modificación de archivo. Se congela el árbol de trabajo, incluidos
cambios no confirmados. El mismo estado congelado se reutiliza para A, B y C;
así la condición y no la calidad del trabajo precursor explica la diferencia.

En C, el precursor deja un handoff con la plantilla de Continuum después de la
interrupción. A y B no reciben ese handoff ni una transcripción de la sesión
anterior. Todos los sucesores reciben la misma descripción de tarea y el mismo
presupuesto.

## 5. Control de variables

El manifiesto registra para cada ensayo: identificador pseudónimo de tarea,
commit de partida, condición, agente/modelo y versión, fecha, sistema
operativo, presupuesto, punto de interrupción y hash del entorno. Se fija todo
lo que sea posible:

- misma tarea, árbol congelado y pruebas para sus tres condiciones;
- mismas herramientas, permisos, variables de entorno no sensibles y límite de
  tiempo; y
- mismo modelo por bloque de comparación.

Se prueban al menos dos modelos o proveedores cuando haya recursos. Las
condiciones se aleatorizan y se contrabalancean por tarea y modelo; las
repeticiones no comparten conversación, caché ni directorio de trabajo.

## 6. Análisis previsto

Antes de la recolección confirmatoria se publicarán la semilla de
aleatorización, el tamaño de muestra decidido mediante piloto o simulación, el
presupuesto y el código de análisis.

- Para resolución, se reportarán proporciones por condición y un modelo
  logístico con efectos por tarea, repositorio y modelo cuando el tamaño de la
  muestra lo permita.
- Para tokens, eventos y tiempo, se reportarán mediana, distribución e
  intervalos de confianza; un modelo de efectos mixtos sobre una transformación
  preespecificada será complementario, no sustituto de los datos descriptivos.
- Los ensayos agotados cuentan como no resueltos. Su costo se conserva; no se
  eliminan por ser altos.
- Un ensayo solo se excluye por fallas de infraestructura declaradas antes:
  entorno no arrancable, servicio externo caído o pruebas de aceptación
  inválidas. Toda exclusión se conserva en un registro con causa.

El piloto sirve para verificar la instrumentación, fijar presupuestos y estimar
la variabilidad. No se mezclará con la muestra confirmatoria ni se usará para
presentar eficacia.

## 7. Reproducibilidad

La publicación final debe incluir, según lo permitan licencias y privacidad:

- manifiesto de tareas y condiciones;
- scripts que preparan, interrumpen, restauran y evalúan cada ensayo;
- versiones de agentes, modelos, dependencias y entorno;
- datos anonimizados a nivel de ensayo;
- pruebas de aceptación y código que produce tablas y figuras; y
- una lista de desviaciones respecto al prerregistro.

El CLI actual ofrece snapshots y exportaciones locales, pero **todavía no es el
harness experimental**: no captura por sí solo la asignación aleatoria, los
estados congelados, eventos de relevo ni pruebas de aceptación por ensayo. Esas
capacidades deben implementarse y probarse antes de iniciar la fase
confirmatoria.

## 8. Privacidad, consentimiento y revisión ética

Continuum no debe enviar telemetría de forma remota. Los datos brutos viven
localmente y se excluyen de Git. Toda exportación de investigación se revisa
antes de salir del entorno y elimina rutas locales, nombres de personas,
remotos, prompts, contenido de código no autorizado y credenciales.

Si participan personas, equipos externos o repositorios privados, se requiere
consentimiento explícito y la aprobación institucional o ética aplicable antes
de recolectar datos. Un consentimiento para usar la herramienta no equivale a
consentimiento para investigar ni publicar datos derivados.

## 9. Evidencia que motiva el diseño

La literatura sobre archivos de instrucciones es mixta: una evaluación reporta
costos mayores y menor éxito con contexto innecesario, mientras otra encuentra
menor tiempo y menor consumo de tokens con `AGENTS.md`. Por eso este estudio
separa guía mínima, handoff y corrección, en vez de asumir que más instrucciones
son mejores.

Un trabajo reciente sobre relevo de agentes interrumpe sesiones, congela el
repositorio y compara qué ve el sucesor; ese patrón informa la unidad de
análisis de este protocolo. Las fuentes son preprints y motivan la evaluación,
no constituyen evidencia de que Continuum funcione.

- [Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents](https://arxiv.org/abs/2602.11988)
- [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents](https://arxiv.org/abs/2601.20404)
- [Handoff Debt: The Rediscovery Cost When Coding Agents Take Over Interrupted Tasks](https://arxiv.org/abs/2606.02875)
- [Guía de prerregistro de OSF](https://help.osf.io/article/330-welcome-to-registrations)
