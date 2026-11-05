# Gestión de Solicitudes Académicas

Trabajo Práctico Integrador de Metodología de Sistemas II.

Este repositorio contiene un sistema pequeño que registra
solicitudes de estudiantes (certificados, equivalencias, reincorporaciones, bajas, otros), cambia su
estado, asigna responsables, busca y emite un reporte. La versión inicial se conserva en el tag
`estado-inicial`; la versión actual organiza el código en el paquete `solicitudes`.

> El sistema base fue generado con ayuda de IA (Claude, Anthropic) y se declara en el informe.
> El uso de IA en las distintas etapas se detalla en [la declaración](docs/declaracion_ia.md).

## Tecnología y requisitos

Python 3.9 o posterior y su biblioteca estándar. No requiere instalar paquetes.

## Uso
```bash
python main.py                            # demo mínima (crea solicitudes.json)
python escenario.py                       # escenario completo (salida de referencia en docs/evidencias/)
python -m unittest discover -s tests -v    # todas las pruebas
python tools/verificar_antes_despues.py    # compara salida y datos con estado-inicial
python tools/cobertura.py                 # cobertura aproximada de líneas
python tools/metricas.py solicitudes      # complejidad, parámetros y longitud por función
```

## Funcionalidades
Registrar solicitud · cambiar estado · asignar responsable · buscar/filtrar · reporte con marca de vencidas.
Persistencia en `solicitudes.json`. Todos los datos son sintéticos.
La demo agrega una solicitud cada vez que se ejecuta. Las pruebas usan archivos temporales.

## Estructura
```
solicitudes/   catalogos.py  modelos.py  validacion.py  servicio.py  repositorio.py  reporte.py  reloj.py  errores.py  cli.py
tests/         pruebas unitarias, de caracterización y de compatibilidad de datos
tools/         metricas.py, cobertura.py (solo biblioteca estándar)
docs/          diagnóstico, SOLID/Clean Code, refactorings, pruebas, code review, decisiones y evidencias
escenario.py   guion determinista usado como golden master
```
## Tags del repositorio
| Tag | Significado |
|---|---|
| `estado-inicial` | Sistema base con deuda técnica (`gestor.py`) |
| `etapa-diagnostico` | Diagnóstico de calidad y 13 code smells |
| `etapa-refactoring` | Refactorings aplicados; golden master idéntico |
| `etapa-pruebas` | Pruebas unitarias, compatibilidad y cobertura |
| `etapa-docs` | Code review y documentación final |


Para comparar: `git diff estado-inicial estado-refactorizado --stat`.

## Documentación
Ver [`docs/`](docs/): `diagnostico_code_smells.md`, `solid_clean_code.md`, `refactorings.md`, `pruebas.md`,
`code_review_checklist.md`, `decisiones_tecnicas.md`, `declaracion_ia.md` y `evidencias/`.

## Equipo
| Integrante | Usuario GitHub |
|---|---|
| Sergio Montenegro | smontene22 |
| Santiago Pace | santipace |
| Pedro Sota | dibaxu |

