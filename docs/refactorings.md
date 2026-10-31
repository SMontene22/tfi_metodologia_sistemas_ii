# Refactorings aplicados (antes / después)

Técnica de trabajo: protección con una prueba de caracterización (golden master). Primero se capturó la salida de la versión inicial (docs/evidencias/salida_inicial.txt); luego se construyó la estructura nueva, se migró el escenario y se eliminó gestor.py. La salida del escenario refactorizado es idéntica a la inicial y la prueba automática termina en OK.

## R1 – Extract Method (sobre reg)
Smells atacados: #2 Long Method, #10 duplicación.

Antes (gestor.py, reg, 41 líneas, CC 23):

```python
def reg(nom, leg, mail, t, desc, p=None, resp=None, f=None):
    if nom == None or nom.strip() == "":
        print("error nombre")
        return -1
    if leg == None or len(leg) < 5:
        print("error legajo")
        return -2
    ...
    if t != "CERTIFICADO" and t != "EQUIVALENCIA" and t != "REINCORPORACION" and t != "BAJA" and t != "OTRO":
```

Después (validacion.py):

```python
def validar_datos(datos, hoy):
    estudiante = validar_estudiante(datos.nombre, datos.legajo, datos.mail)
    tipo = TipoSolicitud.desde_texto(datos.tipo, "tipo")
    descripcion = validar_descripcion(datos.descripcion)
    prioridad = resolver_prioridad(tipo, datos.prioridad)
    fecha = resolver_fecha(datos.fecha, hoy)
    return estudiante, tipo, descripcion, prioridad, fecha
```

Resultado: CC máxima 23 → 10; función más larga 41 → 10 líneas. También se extrajo la búsqueda por id (ServicioSolicitudes._obtener), que estaba duplicada en asig y cambiar.

## R2 – Move Method / reubicación de responsabilidad
Smells: #1 módulo Dios, #4 switch duplicado, #11 envidia de funcionalidad.

Antes: las reglas de transición, de asignación y de vencimiento vivían en funciones sueltas que manipulaban diccionarios ajenos (cambiar, asig, reporte+sla).

Después: el comportamiento vive junto a los datos que usa:

```python
class Solicitud:
    def asignar(self, responsable): ...         # valida estado cerrado y área habilitada
    def cambiar_estado(self, nuevo): ...        # valida transición y responsable
    def esta_vencida(self, hoy): ...            # usa fecha_limite() y la regla SLA del tipo
```

Y sla(), la prioridad por defecto y las áreas permitidas se movieron a ReglaTipo (catalogos.py).

## R3 – Introduce Parameter Object
Smells: #3 Long Parameter List / Data Clump.

Antes: reg(nom, leg, mail, t, desc, p, resp, f) y buscar(c, v).

Después:

```python
servicio.registrar(DatosSolicitud(nombre, legajo, mail, tipo, descripcion, prioridad, fecha))
servicio.buscar(FiltroSolicitudes(tipo=TipoSolicitud.BAJA, texto="carrera"))
```

Estudiante(nombre, legajo, mail) agrupa además el data clump que viajaba junto.

## R4 – Replace Magic String with Enum / Replace Conditional with Table
Smells: #4, #8.

Antes (sla): if t == "CERTIFICADO": return 5 elif ... (y dos cadenas más con el mismo patrón).

Después: REGLAS_POR_TIPO = {TipoSolicitud.CERTIFICADO: ReglaTipo(Prioridad.BAJA, {Area.ALUMNADO}, 5), ...}. Los valores inválidos fallan al convertirse (desde_texto), no en algún punto lejano.

## R5 – Replace Error Code with Exception
Smells: #5, #12.

Antes: return -1 + print("error nombre"); return False sin causa.

Después: raise ValidacionError("nombre", "no puede estar vacio"), TransicionInvalida, AsignacionInvalida, SolicitudNoEncontrada, ErrorDePersistencia. El llamador distingue la causa y decide cómo informarla.

## R6 – Extract Interface + Dependency Injection (repositorio y reloj)
Smells: #6 estado global, #7 dependencia dura, #11 date.today().

Antes: lista/contador globales, open(ARCHIVO) y date.today() dentro de la lógica.

Después: ServicioSolicitudes(repositorio, reloj) con RepositorioMemoria, RepositorioJSON, RelojSistema, RelojFijo.

## R7 – Rename y R8 – Remove Dead Code
Smells: #9, #13. Rename: reg → registrar, asig → asignar_responsable, cambiar → cambiar_estado, etc. Se eliminaron exportar_csv (comentada), viejo_buscar_por_id y los imports os/sys.

## Métricas antes / después

| Métrica | Versión inicial | Versión refactorizada |
|---|---|---|
| Complejidad ciclomática máxima | 23 (reg) | 10 (FiltroSolicitudes.coincide) |
| Complejidad ciclomática promedio | 9,00 | 1,86 |
| Parámetros máximos por función | 8 | 3 |
| Líneas máximas por función | 41 | 10 |
| Estado global mutable | 2 variables | 0 |
| Módulos con una responsabilidad | 1 módulo con 4 | 9 módulos |
| Pruebas automáticas | 1 (golden master) | 1 (golden master), 89 % de líneas cubiertas |

Fuente: tools/metricas.py y tools/cobertura.py; salidas completas en docs/evidencias/metricas_final.txt y docs/evidencias/cobertura_final.txt.