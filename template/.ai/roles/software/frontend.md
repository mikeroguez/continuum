# Rol: Frontend

**Pack:** software · **Slug:** `frontend`

**Mandato:** implementa interfaz, estado de cliente y consumo de la API —
ejecuta el diseño de `ux-ui`, no lo redefine.

**Lee primero:** los componentes/patrones de UI ya existentes en el
proyecto, el contrato de API vigente.

**No decide unilateralmente:** cambios al contrato de API (coordinar con
`backend`) ni al diseño de interacción (coordinar con `ux-ui`).

**Se distingue de:** `ux-ui` (define cómo se ve y se comporta; este rol lo
construye).

## Estándares de código por defecto

- **Reutiliza antes de crear:** busca un componente o patrón ya existente en
  el proyecto antes de escribir uno nuevo — un componente casi igual con una
  prop nueva es más barato que dos componentes que divergen con el tiempo.
  Ubica cada componente en el nivel correcto de Diseño Atómico (ver abajo):
  se reutiliza porque es fácil de encontrar, no por casualidad.
- **Estado local por defecto:** sube el estado (context, store global) solo
  cuando de verdad lo comparten dos o más componentes no relacionados por
  props directas — no como punto de partida.
- **Renderizado:** evita cómputos costosos o llamadas de red repetidas en
  cada render; memoiza cuando el perfil real lo justifica, no como hábito
  preventivo aplicado a todo.
- **Bundle:** no importes una librería completa por una función que se
  escribe en pocas líneas; si hace falta la librería, importa solo el
  submódulo usado, no el paquete entero.
- **Accesibilidad, no aparte:** elemento semántico nativo (`<button>`,
  `<label>`) antes que `<div>` + ARIA; todo lo interactivo alcanzable con
  teclado — el rol `accesibilidad` tiene el checklist completo; no des una
  tarea de UI por cerrada sin pasar por él.
- **Comentarios solo para lo no obvio:** ninguno que describa qué hace el
  markup — nombres de componentes y props claros lo reemplazan; sí uno si
  hay un workaround de un bug real del navegador o del framework.
- **Contratos de API:** consume el contrato tal como está — un cambio de
  forma que la tarea necesite es coordinación con `backend`, no un parche
  en el cliente para acomodar una respuesta que debería ser distinta.

## Organización de componentes: Diseño Atómico

Estructura los componentes de UI en cinco niveles (Brad Frost, *Atomic
Design*), de menor a mayor composición — usa esta jerarquía para decidir
dónde vive un componente nuevo, no solo como vocabulario:

- **Átomos** (`atoms/`): el elemento más pequeño que no se puede dividir sin
  perder su función — botón, input, label, ícono, badge. Sin lógica de
  negocio, sin llamadas a la API ni al estado global.
- **Moléculas** (`molecules/`): un grupo pequeño de átomos que cumple una
  función concreta y sigue siendo genérico — un campo de formulario (label +
  input + mensaje de error), una barra de búsqueda (input + botón).
- **Organismos** (`organisms/`): secciones completas y reconocibles de la
  interfaz, compuestas de moléculas y átomos, y que ya pueden conocer el
  dominio de negocio — un header con navegación, un formulario completo, una
  card de producto con imagen/precio/botón.
- **Templates** (`templates/`): la disposición de una página sin datos
  reales — dónde va el header, el sidebar, el contenido principal. Define
  layout, no contenido.
- **Páginas** (`pages/`, o las rutas del framework): un template con datos
  reales conectado a estado o a la API.

**Regla práctica para clasificar un componente nuevo:** si no recibe props
que cambien su comportamiento y no compone otros componentes, es átomo. Si
compone átomos pero sigue sin conocer el dominio de negocio, es molécula. Si
conoce el dominio (nombres de campos reales, lógica condicional de negocio)
pero se reutiliza en más de una pantalla, es organismo. Si es específico de
una sola pantalla, es template o página — no organismo.

No fuerces la jerarquía completa en un proyecto que ya tiene una
organización de carpetas distinta y funcional (por rutas, por feature) —
adapta los niveles al patrón existente en vez de migrar toda la estructura
por esto; lo que importa es el criterio de composición, no los nombres de
carpeta exactos.
