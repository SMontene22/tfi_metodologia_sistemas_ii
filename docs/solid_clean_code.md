# Aplicación de SOLID y Clean Code

## SOLID

| Principio | Problema en la versión inicial | Mejora aplicada | Evidencia |
|---|---|---|---|
| **SRP** (responsabilidad única) | `gestor.py` validaba, aplicaba reglas, persistía e imprimía. | Un módulo por responsabilidad: `validacion.py`, `catalogos.py` (reglas), `modelos.py` (entidades), `repositorio.py` (persistencia), `servicio.py` (casos de uso), `reporte.py` (presentación). | `docs/evidencias/metricas_final.txt`: ninguna función supera 10 líneas. |
| **OCP** (abierto/cerrado) | Un tipo nuevo obligaba a editar `reg`, `asig` y `sla`. | Las reglas por tipo son **datos** (`REGLAS_POR_TIPO`). Agregar `PASANTIA` = 1 valor en el enum + 1 entrada en la tabla; ninguna función cambia. | `catalogos.py`; prueba `test_todos_los_tipos_tienen_regla`. |
| **LSP** (sustitución de Liskov) | No había abstracciones que sustituir. | `RepositorioMemoria` y `RepositorioJSON` cumplen el mismo contrato (`RepositorioSolicitudes`) y el servicio funciona igual con ambos; `RelojSistema` y `RelojFijo` son intercambiables. | Las pruebas de servicio usan memoria; las de persistencia, JSON, con el mismo código de servicio. |
| **ISP** (segregación de interfaces) | — | Interfaces mínimas: el repositorio expone 4 operaciones; el reloj, 1 (`hoy`). Ningún cliente depende de métodos que no usa. | `repositorio.py`, `reloj.py`. |
| **DIP** (inversión de dependencias) | La lógica abría `solicitudes.json` y llamaba `date.today()` directamente. | `ServicioSolicitudes(repositorio, reloj)` recibe sus dependencias por constructor y depende de abstracciones. | `servicio.py`; `test_reporte_usa_el_reloj_inyectado`. |

## Clean Code

| Práctica | Antes | Después |
|---|---|---|
| **Nombres que revelan intención** | `reg`, `asig`, `buscar(c, v)`, `s`, `t`, `p`, `e` | `registrar`, `asignar_responsable`, `buscar(FiltroSolicitudes)`, `solicitud`, `tipo`, `prioridad`, `estado` |
| **Funciones pequeñas, un solo nivel de abstracción** | `reg`: 41 líneas, CC 23 | `registrar`: 5 líneas; `validar_datos` orquesta funciones de 4-9 líneas |
| **Pocos parámetros** | `reg` con 8 parámetros | `DatosSolicitud` (1 parámetro); máximo 3 en todo el código |
| **Sin números ni cadenas mágicas** | `"EN_PROCESO"`, `5`, `30`, `len(leg) < 5` | `Estado.EN_PROCESO`, `sla_dias`, `LONGITUD_MINIMA_LEGAJO` |
| **Manejo de errores con excepciones** | códigos `-1..-6`, `False`, `print`, `except:` | Jerarquía `ErrorDeDominio` con causa específica y `campo` |
| **Alta cohesión** | Todo mezclado | Cada módulo cambia por una sola razón |
| **Bajo acoplamiento y límites claros** | Estado global compartido | Dominio (`catalogos`, `modelos`) no conoce persistencia ni presentación; el servicio es la única frontera |
| **Sin código muerto ni comentarios obsoletos** | `exportar_csv` comentada, `viejo_buscar_por_id`, imports sin uso | Eliminados |
| **Recursos bien administrados** | `open()` sin cerrar | `with open(...)` |
