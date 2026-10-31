# Diagnóstico: calidad externa vs. interna y deuda técnica

## Calidad externa (lo que ve el usuario)

La versión inicial (`gestor.py`, tag `estado-inicial`) **funciona**: registra solicitudes,
valida datos, cambia estados respetando un flujo, asigna responsables según el área, busca
por cinco criterios, persiste en `solicitudes.json` y emite un reporte ordenado que marca
las solicitudes vencidas. El escenario `escenario.py` lo demuestra (`docs/evidencias/salida_inicial.txt`).

## Calidad interna (lo que ve quien mantiene el código)

| Atributo | Estado en la versión inicial | Consecuencia al evolucionar |
|---|---|---|
| Mantenibilidad | Un único módulo mezcla validación, reglas, persistencia y presentación. | Cualquier cambio de regla obliga a tocar funciones largas y propensas a error. |
| Legibilidad | Nombres crípticos (`reg`, `asig`, `p`, `t`, `s`, `e`), cadenas `if/elif` extensas. | Cuesta entender qué hace cada línea; el onboarding es lento. |
| Testabilidad | Estado global, archivo fijo, `date.today()` y `print` directos. | Para probar hubo que parchear módulos y capturar `stdout`. |
| Extensibilidad | Agregar un tipo de solicitud exige editar 4 lugares distintos. | Riesgo alto de olvidar uno (violación de OCP). |
| Robustez | Errores como códigos numéricos, `except:` vacío, archivos sin cerrar. | Fallos silenciosos y pérdida de información sobre la causa. |

Métricas de la versión inicial (`docs/evidencias/metricas_inicial.txt`): complejidad ciclomática
máxima **23** (`reg`), promedio **9,0**, función con **8 parámetros** y hasta **41 líneas**.

## Inventario de code smells (13)

Prioridad: **A** = alta (corregir primero), **M** = media, **B** = baja.

| # | Code smell / debilidad | Evidencia y ubicación (`gestor.py`) | Impacto | Riesgo de mantenimiento | Prio. |
|---|---|---|---|---|---|
| 1 | **Módulo Dios / violación de SRP** | Un archivo contiene validación (`reg`), reglas (`sla`, `asig`), persistencia (`cargar`, `guardar`) y presentación (`reporte`). | Cambios de un tema afectan a los demás. | Alto: alto acoplamiento y regresiones cruzadas. | A |
| 2 | **Long Method** | `reg` (líneas 29-69): 41 líneas, CC=23. | Difícil de leer y probar por partes. | Alto: es el punto con más probabilidad de bugs. | A |
| 3 | **Long Parameter List / Data Clump** | `reg(nom, leg, mail, t, desc, p, resp, f)` — 8 parámetros; `nom, leg, mail` viajan juntos. | Llamadas propensas a errores de orden. | Medio-alto. | A |
| 4 | **Switch Statements duplicados (viola OCP)** | La regla "según tipo" se repite en `reg` (prioridad, l.46-60), `asig` (área, l.78-90) y `sla` (l.142-152). | Un tipo nuevo requiere modificar 3 funciones. | Alto: olvidos silenciosos. | A |
| 5 | **Manejo de errores deficiente** | `reg` devuelve `-1..-6`; `asig`/`cambiar` devuelven `False` sin causa; mensajes por `print`. | El llamador no puede distinguir ni reaccionar a la causa. | Alto. | A |
| 6 | **Estado global mutable** | `lista`, `contador` y `global` en `cargar`/`reg` (l.8-10, 13, 30). | Acoplamiento oculto; imposible aislar pruebas. | Alto. | A |
| 7 | **Dependencia dura de infraestructura (viola DIP)** | `ARCHIVO` fijo y `open()` dentro de la lógica (l.7, 15, 24). | No se puede cambiar de JSON a BD ni usar memoria en tests. | Medio-alto. | M |
| 8 | **Primitive Obsession + Magic Strings** | Estados, tipos, prioridades y áreas son cadenas sueltas (`"EN_PROCESO"`, `"BAJA"`…); la solicitud es un `dict`. | Un typo no se detecta hasta ejecutar. | Medio-alto. | M |
| 9 | **Nombres poco expresivos** | `reg`, `asig`, `buscar(c, v)`, variables `s`, `t`, `p`, `e`, `o`. | Baja legibilidad. | Medio. | M |
| 10 | **Código duplicado (búsqueda por id)** | El bucle `for s in lista: if s["id"] == i` se repite en `asig` (l.72) y `cambiar` (l.99). | Correcciones repetidas. | Medio. | M |
| 11 | **Salida mezclada con la lógica / dependencia oculta del reloj** | `reporte` imprime con `print` y usa `date.today()` (l.167-186). | No se puede reutilizar ni probar sin parches. | Medio. | M |
| 12 | **Manejo de recursos y excepciones genéricas** | `except:` vacío (l.18) que oculta cualquier fallo; archivos abiertos sin `with` (l.15, 24). | Fallos silenciosos; posible pérdida de datos. | Medio. | M |
| 13 | **Código muerto / imports sin uso** | `exportar_csv` comentada (l.155-157), `viejo_buscar_por_id` sin uso (l.160), `import os`, `import sys`. | Ruido y confusión. | Bajo. | B |

## Relación entre los smells y la evolución futura

Agregar un nuevo tipo de solicitud ("PASANTIA", por ejemplo) hoy requiere editar `reg`, `asig` y
`sla`; agregar una regla de transición requiere editar `cambiar`; cambiar de JSON a una base de
datos requiere reescribir `cargar`, `guardar` y todas las funciones que usan `lista`. El costo del
cambio crece con cada requisito, que es precisamente la definición operativa de deuda técnica.