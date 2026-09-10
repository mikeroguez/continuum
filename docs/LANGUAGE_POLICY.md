# Política de idiomas

Continuum nace de un equipo cuya lengua de trabajo es el español. Esa realidad
no se corrige sustituyendo el idioma del proyecto: se hace explícita y se
ofrece una ruta clara para que otras personas puedan usarlo y contribuir.

## Principio

El español es la fuente editorial canónica del proyecto. Cuando existe una
traducción al inglés, debe identificar su documento de origen y la versión que
representa. Ante cualquier diferencia, prevalece el texto en español hasta que
el mantenimiento resuelva la discrepancia.

No se mezclan idiomas dentro del cuerpo de un mismo documento, salvo nombres
propios, comandos, código, rutas y términos técnicos cuya traducción reduciría
la precisión.

## Qué debe existir en ambos idiomas

Las piezas que una persona necesita para evaluar y empezar a usar o contribuir
al proyecto deben estar disponibles en español e inglés:

- descripción, instalación y uso básico (`README.md` / `README.en.md`);
- guía de contribución (`CONTRIBUTING.md` / `CONTRIBUTING.en.md`);
- esta política y el índice de documentación en inglés (`docs/en/README.md`).

Los mensajes del CLI, nombres de archivos y ejemplos de configuración se
mantienen técnicos y estables. Localizarlos no forma parte de esta política;
solo se hará si puede mantenerse sin alterar scripts, automatizaciones o
salidas consumidas por otras herramientas.

## Documentación especializada

Los documentos de arquitectura, investigación, protocolo, métricas y planes de
producto permanecen inicialmente en español. `docs/en/README.md` explica su
propósito en inglés y apunta al original.

Una traducción completa de uno de estos documentos se añade cuando cumpla estas
dos condiciones:

1. el contenido está suficientemente estable para no crear dos fuentes que
   divergen; y
2. cualquier hipótesis, método, resultado o dato sensible ha superado la
   revisión científica, de privacidad y de publicación que corresponda.

Una traducción no debe adelantar resultados de investigación, métricas de uso
ni detalles que el proyecto haya reservado para un paper o evaluación futura.

## Convención de archivos y mantenimiento

- El original en español conserva su ruta actual.
- Su versión inglesa usa el mismo nombre con sufijo `.en.md` cuando vive en la
  raíz; para documentación especializada se agrupa bajo `docs/en/`.
- Las guías distribuidas dentro de `template/docs/` usan pares con títulos
  explícitos en ambos idiomas y se enlazan desde su propio índice.
- Toda traducción abre con un enlace al original y una línea `Source version:`
  que indique el tag o commit de origen.
- Quien cambie una pieza bilingüe revisa su equivalente en el mismo cambio. Si
  no puede actualizarlo, debe marcar la traducción como desactualizada y
  describir el desfase en el pull request o issue correspondiente.

No se automatizan traducciones en el proceso de release. Una traducción es una
decisión editorial: debe conservar significado, límites y tono, no solo
intercambiar palabras.

## Navegación

El README principal enlaza a su equivalente en inglés. El índice
`docs/en/README.md` ofrece a lectores internacionales una ruta hacia cada
documento especializado, aunque aún no tenga traducción completa.

Así el proyecto es accesible desde hoy sin ocultar cuál texto tiene autoridad
ni prometer paridad donde todavía no existe.
