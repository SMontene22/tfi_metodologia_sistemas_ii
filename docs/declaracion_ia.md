# Declaración de uso de inteligencia artificial

| Campo | Detalle |
|---|---|
| Herramientas | Claude (Anthropic) y Codex (OpenAI) |
| Finalidad | Claude: generar el sistema base con problemas de diseño (`estado-inicial`) y asistir con dudas. Codex: ayudar con el código python de la etapas 6. |
| Grado de intervención | Medio-Alto en la creación del sistema base. En las etapas 6, Codex revisó y modificó los test para hacer la verificación del antes y después. |

## Registro de prompts
| N.º | Fecha | Integrante | Prompt | Finalidad | Resultado |
|---|---|---|---|---|---|
| 1 | 26/10/2026 | `Sergio Montenegro` | "tenemos que resolver el tp integrador" (con la consigna adjunta). Generar un sistema base de gestión de solicitudes académicas con deuda técnica y code smells intencionales  | Generar el caso de trabajo | Sistema base con tag `estado-inicial` |
| 2 | 26/10/2026 | `Equipo` | Analizar el código y verificar la presencia de los siguientes 10 code smells... | Validar el diagnóstico técnico. | Se obtuvo un informe indicando cuáles smells estaban presentes y evidencias de cada uno. |
| 3 | 27/10/2026 | `Santiago Pace` | Sugerir refactorings aplicables respetando principios SOLID | Identificar oportunidades de mejora. | Se propusieron alternativas de refactoring y reorganización de responsabilidades. |
| 4 | 03/11/2026 | `Pedro Sota` | Solicitud de revisión y correción sobre el código. | Corregir pruebas y code review. | comparación antes/después, evidencias y correcciones. |
