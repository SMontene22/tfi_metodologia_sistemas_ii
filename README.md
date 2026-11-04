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

## Equipo
| Integrante | Usuario GitHub |
|---|---|
| Sergio Montenegro | smontene22 |
| Santiago Pace | santipace |
| Pedro Sota | dibaxu |
