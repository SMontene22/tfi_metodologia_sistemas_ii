# Etapa 6 - Pruebas y verificación del comportamiento

## Objetivo y forma de trabajo

El objetivo fue comprobar que, después del refactoring, el sistema siguiera registrando,
asignando, cambiando estados, buscando y mostrando solicitudes como antes. Se partió de la prueba de caracterización que ya tenía el proyecto. Esta prueba ejecuta
un escenario completo y compara su salida con la guardada en la versión inicial.

Primero se volvió a ejecutar la prueba del tag `estado-inicial`. Luego se ejecutó el
escenario actual y se compararon tanto el texto generado como los datos guardados en
JSON. La versión revisada parte del commit `903a65c`, con los cambios locales de estas
etapas.

Además, se agregaron pruebas específicas con `unittest`, que viene con Python. Cada una
prepara los datos, ejecuta una operación y comprueba el resultado.

## Casos de prueba


| Caso | Datos o acción | Resultado esperado | Verificación |
|---|---|---|---|
| CP01 | Ejecutar el escenario completo en ambas versiones. | Mismos registros, rechazos, búsquedas, reporte y recarga. | `test_caracterizacion.py` y comparación antes/después. |
| CP02 | Registrar dos solicitudes válidas. | IDs 1 y 2, estado PENDIENTE y prioridad correspondiente al tipo. | `test_registrar_asigna_id_estado_y_prioridad`. |
| CP03 | Registrar con nombre vacío, legajo corto, mail sin @, tipo, descripción o prioridad inválidos. | Se rechaza el campo incorrecto, no se guarda ni se consume un ID. | `test_registrar_rechaza_datos_invalidos_sin_guardar`. |
| CP04 | Indicar prioridad y fecha; omitir la fecha; usar 2025-02-30. | Respeta los valores válidos, usa el reloj al omitir fecha y rechaza la fecha imposible. | Tres pruebas de registro y fecha. |
| CP05 | Registrar cada uno de los cinco tipos y probar sus áreas. | Prioridades y plazos correctos; solo acepta áreas habilitadas. | `test_todos_los_tipos_tienen_regla` y `test_asignacion_respeta_area_del_tipo`. |
| CP06 | Intentar pasar a EN_PROCESO sin responsable. | Rechaza el cambio y conserva PENDIENTE. | `test_no_permite_iniciar_sin_responsable`. |
| CP07 | Probar las 16 combinaciones entre los cuatro estados. | Acepta solo las cuatro transiciones permitidas; las demás conservan el estado anterior. | `test_transiciones_permitidas_y_rechazadas`. |
| CP08 | Asignar una solicitud cerrada u operar con ID 99 inexistente. | Informa el error y no realiza la operación. | Pruebas de solicitudes cerradas e ID inexistente. |
| CP09 | Buscar por tipo, estado, prioridad, legajo y texto, y combinar criterios. | Devuelve los IDs esperados, sin distinguir mayúsculas en el texto; sin coincidencias devuelve una lista vacía. | `test_buscar_por_criterios_y_combinaciones`. |
| CP10 | Consultar antes, durante y después del plazo de cada tipo. | Marca VENCIDA recién al día siguiente del límite; una solicitud cerrada no se marca vencida. | `test_reporte_usa_el_reloj_inyectado` y escenario completo. |
| CP11 | Generar un reporte vacío y otro con prioridades y fechas repetidas. | Totales en cero cuando no hay datos; orden por prioridad, fecha e ID cuando hay solicitudes. | Pruebas de reporte vacío y orden. |
| CP12 | Guardar, asignar, cambiar estado y volver a cargar. | Conserva todos los datos y el siguiente ID es 2. | `test_recarga_conserva_datos_y_siguiente_id`. |
| CP13 | Revisar el JSON guardado. | Conserva el formato inicial, sus campos y valores. | `test_guarda_formato_inicial` y comparación de los JSON de ambas versiones. |
| CP14 | Cargar JSON roto o con estructura incorrecta y simular un error de escritura. | Informa `ErrorDePersistencia`; al fallar la carga no sobrescribe el archivo. | Pruebas de JSON inválido y error de escritura. |
| CP15 | Ejecutar la demo con un archivo temporal. | Guarda una solicitud y muestra el reporte con Total: 1. | `test_demo_registra_y_muestra_reporte`. |

## Resultados y evidencias

| Verificación | Resultado obtenido | Evidencia |
|---|---|---|
| Prueba original del tag `estado-inicial`. | 1 prueba, sin fallos ni errores. | [pruebas_version_inicial.txt](evidencias/pruebas_version_inicial.txt) |
| Comparación del escenario antes y después. | Salidas idénticas y los mismos datos JSON de las 6 solicitudes. | [comparacion_antes_despues.txt](evidencias/comparacion_antes_despues.txt) |
| Suite actual. | 21 pruebas, sin fallos ni errores. | [pruebas_etapa_6.txt](evidencias/pruebas_etapa_6.txt) |
| Cobertura aproximada de líneas del paquete `solicitudes`. | 310 de 321 líneas, aproximadamente 97 %. | [cobertura_etapa_6.txt](evidencias/cobertura_etapa_6.txt) |
| Comprobación de sintaxis. | Sin errores en aplicación, pruebas y herramientas. | [compilacion_etapas_6_7.txt](evidencias/compilacion_etapas_6_7.txt) |

Se conservaron la [salida inicial reproducida](evidencias/salida_inicial_reproducida.txt)
y la [salida refactorizada](evidencias/salida_refactorizada.txt). El archivo de referencia
original no se modificó. Por ejemplo, en ambas versiones el intento de iniciar la
solicitud 1 sin responsable se rechaza, la búsqueda de pendientes devuelve `[4, 5, 6]`
y la recarga recupera las 6 solicitudes.


## Cómo repetir la verificación

Desde la carpeta principal del repositorio:

```bash
python -m unittest discover -s tests -v
python tools/verificar_antes_despues.py
python tools/cobertura.py
python -m compileall -q solicitudes tests tools main.py escenario.py
```

El segundo comando necesita Git y el tag `estado-inicial`, y actualiza los archivos de
comparación. El porcentaje de cobertura puede variar con la versión de Python; aquí se
usó Python 3.12.14.

## Qué se pudo concluir

No se observaron regresiones en las operaciones verificadas: el escenario de referencia
produjo el mismo resultado y se guardaron los mismos datos. Además, los casos específicos
permitieron comprobar reglas y situaciones límite que antes dependían de una sola prueba.

Esta conclusión se limita a los casos ejecutados. La interfaz de programación cambió:
antes se usaban funciones y códigos de error, mientras que ahora se usan un servicio,
objetos y excepciones. El escenario adapta esas llamadas para comparar los resultados
funcionales; por eso no demuestra compatibilidad con programas que importaban `gestor.py`.
Tampoco se afirma que el sistema esté libre de errores: se midieron líneas ejecutadas,
no cobertura de todas las ramas, ni se probaron grandes volúmenes o usuarios simultáneos.
