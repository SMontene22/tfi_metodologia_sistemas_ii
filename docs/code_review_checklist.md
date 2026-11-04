# Etapa 7 - Code review profesional

## Alcance y criterio de revisión

Se revisó la versión refactorizada y se leyeron los módulos de `solicitudes`, los puntos de entrada, las pruebas,
las herramientas y la documentación. Además, se ejecutaron las verificaciones de la
etapa 6 para respaldar las observaciones con resultados concretos.

La revisión se centró en que el código fuera entendible, mantuviera sus reglas y pudiera
modificarse sin mezclar responsabilidades. Para cada problema se registró qué ocurría,
por qué convenía corregirlo y qué acción se realizó.

## Checklist aplicado

| Control | Estado | Observación o evidencia |
|---|---|---|
| El código tiene sintaxis válida. | Cumple | `compileall` terminó con código 0. |
| Las pruebas automáticas pasan. | Cumple | 21 pruebas sin fallos ni errores. |
| Se conserva el resultado del escenario inicial. | Cumple | Mismo texto y mismos datos JSON; ver etapa 6. |
| Se prueban reglas principales y casos inválidos. | Cumple tras ampliar pruebas | Se agregaron casos de áreas, estados, vencimientos, búsquedas y persistencia. |
| Los nombres principales permiten entender las operaciones. | Cumple | `registrar`, `asignar_responsable` y `cambiar_estado` expresan su intención. |
| Las responsabilidades están separadas. | Cumple | El servicio coordina; el modelo aplica reglas; el repositorio guarda y el reporte genera texto. |
| Las reglas comunes tienen un lugar definido. | Cumple | Áreas, prioridades, plazos y transiciones están en `catalogos.py`. |
| La lógica puede probarse sin depender de archivos ni de la fecha real. | Cumple | Las pruebas usan `RepositorioMemoria` y `RelojFijo`. |
| La carga rechaza JSON roto o con estructura incorrecta. | Corregido | H1: se agregó validación de lista y objetos antes de convertir los registros. |
| La herramienta de cobertura informa un fallo con un código de salida distinto de cero. | Corregido | H2: antes devolvía 0 incluso con pruebas fallidas; ahora devuelve 1. |
| Las instrucciones de uso coinciden con el código actual. | Corregido | H3: el README ahora usa `main.py` y el paquete `solicitudes`. |
| El uso de IA está declarado según la intervención real. | Actualizado | H4: se registró la asistencia en pruebas, revisión y redacción. |
| Los datos de ejemplo son sintéticos. | Cumple en los archivos revisados | Las pruebas y la demo usan datos ficticios; el archivo de ejecución está ignorado por Git. |
| El costo de las operaciones es razonable para el caso pequeño del TP. | Adecuado al alcance | Se recorre la lista y se reescribe el JSON; no se hicieron pruebas de carga. |
| Los hitos de Git y la revisión entre compañeros quedan registrados. | Pendiente del equipo | Al revisar, solo estaban los tags `estado-inicial` y `etapa-diagnostico`. |

## Observaciones, feedback y correcciones

| Hallazgo | Ubicación | Feedback y motivo | Acción y comprobación |
|---|---|---|---|
| H1 - Prioridad media. Un JSON como `null` o `[null]` generaba errores sin convertirlos a `ErrorDePersistencia`; `{}` se aceptaba como repositorio vacío. | `solicitudes/repositorio.py`, `RepositorioJSON._cargar`. | Conviene validar la estructura antes de cargar los registros. Así se evita interpretar un archivo incorrecto como si no tuviera datos. | Se exige una lista de objetos. Los cinco subcasos de `test_json_invalido_informa_error_sin_sobrescribir` pasan y el archivo se conserva. |
| H2 - Prioridad media. La herramienta de cobertura terminaba con código 0 aunque hubiera pruebas fallidas. | `tools/cobertura.py`, cierre del programa. | El resultado debe servir tanto para leerlo en consola como para detectar automáticamente un fallo. | Se agregó el código de salida según el resultado de la suite y se cerró el recurso de salida con `with`. Una prueba fallida intencional confirmó el cambio de 0 a 1. |
| H3 - Prioridad baja. El README indicaba ejecutar `gestor.py`, eliminado en el refactoring. | `README.md`, uso y descripción. | Las instrucciones deben permitir que otro integrante ejecute la versión actual sin tener que adivinar el comando. | Se actualizaron descripción, requisitos, comandos y enlaces a pruebas y revisión. |
| H4 - Prioridad baja. La declaración de IA tenía una aclaración pendiente y no incluía esta asistencia. | `docs/declaracion_ia.md`. | El registro debe describir las herramientas usadas y el grado real de intervención. | Se agregó Codex, la finalidad de esta sesión y el prompt recibido. Falta adjuntar la conversación exportada en la entrega general. |

La secuencia de H1 queda registrada en
[pruebas_antes_correccion.txt](evidencias/pruebas_antes_correccion.txt) y
[pruebas_etapa_6.txt](evidencias/pruebas_etapa_6.txt). Para H2, el resultado está en
[code_review_verificacion.txt](evidencias/code_review_verificacion.txt): se sustituyó
temporalmente la carga de pruebas por una suite con un fallo intencional, solo en memoria.
No se agregó una prueba fallida permanente al proyecto.

## Criterios de aceptación técnica

Para dar por terminada la parte técnica se pidió que el código tuviera sintaxis válida,
que todas las pruebas pasaran y que el escenario mantuviera su salida y sus datos. Además,
los casos de JSON inválido debían informar el error sin sobrescribir el archivo, la
herramienta de cobertura debía devolver un código de fallo cuando correspondiera y los
comandos del README debían coincidir con la versión actual. Estos controles se cumplieron.

Como referencia del trabajo se tomó una cobertura total de líneas de al menos 80 %;
el resultado aproximado fue 97 %. Este valor ayuda a detectar partes sin recorrer,
pero por sí solo no demuestra que todas las decisiones del programa sean correctas.
Las correcciones se mantuvieron acotadas y no agregaron funcionalidades al sistema.
