"""Escenario determinista usado como prueba de caracterizacion (golden master).

Version adaptada a la API refactorizada: ejecuta EXACTAMENTE los mismos pasos que la version
inicial y registra solo resultados observables. La salida debe ser identica a
docs/evidencias/salida_inicial.txt (capturada en el tag estado-inicial).
"""
import os
from datetime import date

from solicitudes.catalogos import Area, Estado, Prioridad, TipoSolicitud
from solicitudes.errores import ErrorDeDominio, ValidacionError
from solicitudes.modelos import DatosSolicitud, FiltroSolicitudes, Responsable
from solicitudes.reloj import RelojFijo
from solicitudes.repositorio import RepositorioJSON
from solicitudes.servicio import ServicioSolicitudes

HOY = date(2025, 6, 30)

# Nombre de criterio del escenario -> (campo de FiltroSolicitudes, conversor del valor)
_CRITERIOS = {
    "estado": ("estado", Estado),
    "tipo": ("tipo", TipoSolicitud),
    "prio": ("prioridad", Prioridad),
    "legajo": ("legajo", str),
    "texto": ("texto", str),
}


def ejecutar(directorio):
    ruta = os.path.join(directorio, "solicitudes.json")
    servicio = ServicioSolicitudes(RepositorioJSON(ruta), RelojFijo(HOY))
    log = []

    def registrar(nom, leg, mail, t, desc, p=None, f=None):
        try:
            res = "OK #%d" % servicio.registrar(DatosSolicitud(nom, leg, mail, t, desc, p, f)).id
        except ValidacionError as error:
            res = "ERROR " + error.campo
        log.append("REGISTRAR %s %s -> %s" % (nom, t, res))

    def asignar(i, resp, area):
        try:
            servicio.asignar_responsable(i, Responsable(resp, Area(area)))
            res = "OK"
        except ErrorDeDominio:
            res = "RECHAZADO"
        log.append("ASIGNAR #%d %s/%s -> %s" % (i, resp, area, res))

    def cambiar(i, estado):
        try:
            servicio.cambiar_estado(i, Estado(estado))
            res = "OK"
        except ErrorDeDominio:
            res = "RECHAZADO"
        log.append("CAMBIAR #%d %s -> %s" % (i, estado, res))

    def buscar(campo, valor):
        if campo in _CRITERIOS:
            nombre, convertir = _CRITERIOS[campo]
            ids = [s.id for s in servicio.buscar(FiltroSolicitudes(**{nombre: convertir(valor)}))]
        else:  # criterio inexistente: la API tipada ya no permite expresarlo
            ids = []
        log.append("BUSCAR %s=%s -> %s" % (campo, valor, ids))

    registrar("Ana Perez", "12345", "ana@mail.com", "CERTIFICADO", "Certificado de alumno regular", f="2025-06-20")
    registrar("Luis Gomez", "23456", "luis@mail.com", "EQUIVALENCIA", "Equivalencia de Algebra", f="2025-05-15")
    registrar("Marta Diaz", "34567", "marta@mail.com", "REINCORPORACION", "Reincorporacion 2025", f="2025-06-01")
    registrar("Raul Sosa", "45678", "raul@mail.com", "BAJA", "Baja de la carrera", f="2025-06-25")
    registrar("Eva Luna", "56789", "eva@mail.com", "OTRO", "Cambio de comision", p="ALTA", f="2025-06-05")
    registrar("Ana Perez", "12345", "ana@mail.com", "CERTIFICADO", "Certificado para beca", f="2025-06-29")
    registrar("", "12345", "a@mail.com", "BAJA", "x")
    registrar("Sin Legajo", "12", "a@mail.com", "BAJA", "x")
    registrar("Sin Mail", "12345", "sinarroba", "BAJA", "x")
    registrar("Tipo Malo", "12345", "a@mail.com", "VIAJE", "x")
    registrar("Sin Desc", "12345", "a@mail.com", "BAJA", "   ")
    registrar("Prio Mala", "12345", "a@mail.com", "BAJA", "x", p="URGENTE")

    cambiar(1, "EN_PROCESO")
    asignar(1, "Carlos Ruiz", "SECRETARIA")
    asignar(1, "Carlos Ruiz", "ALUMNADO")
    asignar(99, "Nadie", "ALUMNADO")
    asignar(5, "Sofia Paz", "BEDELIA")
    asignar(2, "Julia Vega", "SECRETARIA")
    cambiar(1, "EN_PROCESO")
    cambiar(1, "PENDIENTE")
    cambiar(1, "RESUELTA")
    cambiar(1, "RECHAZADA")
    asignar(1, "Otro Resp", "ALUMNADO")
    cambiar(2, "EN_PROCESO")
    cambiar(2, "RESUELTA")
    cambiar(3, "RECHAZADA")
    cambiar(5, "RESUELTA")
    cambiar(99, "EN_PROCESO")

    buscar("estado", "PENDIENTE")
    buscar("tipo", "CERTIFICADO")
    buscar("prio", "ALTA")
    buscar("legajo", "12345")
    buscar("texto", "ALGEBRA")
    buscar("color", "rojo")

    log.append(servicio.reporte())

    recargado = ServicioSolicitudes(RepositorioJSON(ruta), RelojFijo(HOY))
    log.append("RECARGA -> %d solicitudes persistidas" % len(recargado.listar()))
    return "\n".join(log) + "\n"


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        print(ejecutar(d), end="")
