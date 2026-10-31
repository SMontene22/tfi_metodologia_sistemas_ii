"""Escenario determinista usado como prueba de caracterizacion (golden master).

Registra SOLO resultados observables (ids, estados, texto del reporte), de modo que
el mismo escenario pueda ejecutarse contra la version inicial y la refactorizada.
"""
import contextlib
import io
import os
from datetime import date

import gestor

HOY = date(2025, 6, 30)
CODIGOS = {-1: "nombre", -2: "legajo", -3: "mail", -4: "tipo", -5: "descripcion", -6: "prioridad"}


class _FechaFija(date):
    @classmethod
    def today(cls):
        return HOY


def _silencioso(funcion, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return funcion(*args, **kwargs)


def ejecutar(directorio):
    gestor.ARCHIVO = os.path.join(directorio, "solicitudes.json")
    gestor.date = _FechaFija
    gestor.cargar()
    log = []

    def registrar(nom, leg, mail, t, desc, p=None, f=None):
        r = _silencioso(gestor.reg, nom, leg, mail, t, desc, p, None, f)
        res = "OK #%d" % r if r > 0 else "ERROR " + CODIGOS[r]
        log.append("REGISTRAR %s %s -> %s" % (nom, t, res))

    def asignar(i, resp, area):
        ok = _silencioso(gestor.asig, i, resp, area)
        log.append("ASIGNAR #%d %s/%s -> %s" % (i, resp, area, "OK" if ok else "RECHAZADO"))

    def cambiar(i, estado):
        ok = _silencioso(gestor.cambiar, i, estado)
        log.append("CAMBIAR #%d %s -> %s" % (i, estado, "OK" if ok else "RECHAZADO"))

    def buscar(campo, valor):
        ids = [s["id"] for s in gestor.buscar(campo, valor)]
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

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        gestor.reporte()
    log.append(buffer.getvalue().rstrip("\n"))

    gestor.cargar()
    log.append("RECARGA -> %d solicitudes persistidas" % len(gestor.lista))
    return "\n".join(log) + "\n"


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        print(ejecutar(d), end="")
