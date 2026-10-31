# Gestión de Solicitudes Académicas – sistema base

Trabajo Práctico Integrador de Metodología de Sistemas II.

Este repositorio contiene el **sistema base** (tag `estado-inicial`): un módulo pequeño que registra
solicitudes de estudiantes (certificados, equivalencias, reincorporaciones, bajas, otros), cambia su
estado, asigna responsables, busca y emite un reporte. Funciona correctamente, pero su estructura
interna no es buena: es el punto de partida para el diagnóstico y la mejora.

> El sistema base fue generado con ayuda de IA (Claude, Anthropic) y se declara en el informe.
> El diagnóstico, los refactorings, las pruebas y el code review los realiza el equipo.

## Uso
```bash
python gestor.py                          # demo mínima
python escenario.py                       # escenario completo (salida de referencia en docs/evidencias/)
python -m unittest discover -s tests -v   # prueba de caracterización
python tools/metricas.py gestor.py        # complejidad, parámetros y longitud por función
```

## Funcionalidades
Registrar solicitud · cambiar estado · asignar responsable · buscar/filtrar · reporte con marca de vencidas.
Persistencia en `solicitudes.json`. Todos los datos son sintéticos.

## Equipo
| Integrante | Usuario GitHub |
|---|---|
| Sergio Montenegro | smontene22 |
| Santiago Pace | santipace |
| Pedro Sota | dibaxu |
