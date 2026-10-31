# Guía de trabajo del equipo

Esta guía organiza el trabajo; el contenido de cada etapa lo producen ustedes.

## Configurar Git (cada integrante, con su propio usuario)
```bash
git config user.name  "Nombre Apellido"
git config user.email "mail-asociado-a-su-GitHub"
```
Cada commit debe hacerlo quien realmente hizo el cambio. Un historial con varios autores es la evidencia de participación.

## Punto de partida
El tag `estado-inicial` ya existe. Antes de tocar nada, ejecuten `python escenario.py` y `python -m unittest discover -s tests`:
la prueba de caracterización es su red de seguridad. Si algo cambia en la salida, introdujeron una regresión.

## Etapas, producción esperada y tags
| Etapa | Qué hacer | Archivo sugerido | Tag al terminar |
|---|---|---|---|
| 1 | Describir dominio, alcance, actores, tecnología y evidencia de funcionamiento | `docs/sistema_base.md` | — |
| 2 | Calidad externa vs. interna, con ejemplos del código | `docs/calidad.md` | — |
| 3 | Diagnóstico: **mínimo 8 smells**, cada uno con evidencia, ubicación (archivo y línea), impacto, riesgo y prioridad | `docs/diagnostico.md` | `etapa-diagnostico` |
| 4 | SOLID y Clean Code: qué principio se viola y cómo se corrige | `docs/solid_clean_code.md` | — |
| 5 | **Mínimo 4 refactorings** (incluir Extract Method, Move Method e Introduce Parameter Object), con antes/después | `docs/refactorings.md` | `etapa-refactoring` |
| 6 | Pruebas: casos antes/después y cómo comprobaron que no hubo regresiones | `tests/`, `docs/pruebas.md` | `etapa-pruebas` |
| 7 | Checklist de code review aplicado al repo, con hallazgos y correcciones | `docs/code_review_checklist.md` | `etapa-docs` |
| 8 | Conclusiones: decisiones, dificultades, límites y mejoras pendientes | informe | `estado-refactorizado` |

Etapas 1 y 2 se documentan, pero no llevan tag propio; el tag `etapa-docs` va en el commit de documentación final.

## Cómo encarar el diagnóstico (etapa 3)
- Lean `gestor.py` completo antes de buscar problemas. Pregúntense: ¿qué cambios serían difíciles? ¿qué se repite? ¿qué no se puede probar?
- Midan: `python tools/metricas.py gestor.py` (complejidad, parámetros, líneas).
- Busquen en el catálogo de smells de la materia: Long Method, Long Parameter List, Duplicated Code, Switch Statements,
  Primitive Obsession, Magic Strings, Global State, nombres poco claros, manejo de errores, código muerto, etc.
- Para cada hallazgo anoten línea, por qué es un problema y qué pasaría al agregar un tipo de solicitud nuevo.

## Cómo encarar el refactoring (etapas 4 y 5)
1. Un refactoring por commit, con mensaje claro (`refactor: Extract Method en registrar`).
2. Después de cada commit corran la prueba de caracterización.
3. Documenten antes/después con fragmentos de código.
4. Pueden agregar pruebas unitarias nuevas a medida que el diseño lo permita.

## Reparto sugerido (ajústenlo como quieran)
| Integrante | Foco sugerido |
|---|---|
| Sergio Montenegro | Etapas 1-3: descripción, calidad y diagnóstico |
| Santiago Pace | Etapas 4-5: SOLID y refactorings |
| Pedro Sota | Etapas 6-7: pruebas y code review |
Todos participan en el video y en las conclusiones. Cada uno debe poder explicar cualquier parte del trabajo.

## Uso de IA
- Declárenlo en el informe: herramienta, finalidad y grado de intervención (el sistema base fue generado con IA).
- Registren cada prompt que usen con fecha y para qué, y adjunten la conversación exportada.
- Pidan a la IA explicaciones, revisiones o alternativas; las decisiones y la redacción final son de ustedes.

## Entrega
PDF único (estructura de la sección 11 de la consigna), repositorio GitHub con los tags, ZIP y video (10-15 min, todos con cámara y voz propia).
