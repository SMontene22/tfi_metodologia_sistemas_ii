"""Validaciones de entrada. Cada regla es una funcion pequena (Extract Method sobre `reg`).

El orden de `validar_datos` replica el de la version inicial: nombre, legajo, mail,
tipo, descripcion, prioridad (y fecha, nueva).
"""
from datetime import date, datetime

from .catalogos import Prioridad, TipoSolicitud
from .errores import ValidacionError
from .modelos import Estudiante

LONGITUD_MINIMA_LEGAJO = 5


def validar_estudiante(nombre, legajo, mail):
    if nombre is None or nombre.strip() == "":
        raise ValidacionError("nombre", "no puede estar vacio")
    if legajo is None or len(legajo) < LONGITUD_MINIMA_LEGAJO:
        raise ValidacionError("legajo", "debe tener al menos %d caracteres" % LONGITUD_MINIMA_LEGAJO)
    if mail is None or "@" not in mail:
        raise ValidacionError("mail", "debe contener '@'")
    return Estudiante(nombre, legajo, mail)


def validar_descripcion(descripcion):
    if descripcion is None or descripcion.strip() == "":
        raise ValidacionError("descripcion", "no puede estar vacia")
    return descripcion


def resolver_prioridad(tipo, prioridad):
    if prioridad is None:
        return tipo.regla.prioridad_por_defecto
    return Prioridad.desde_texto(prioridad, "prioridad")


def resolver_fecha(fecha, hoy):
    if fecha is None:
        return hoy
    if isinstance(fecha, date):
        return fecha
    try:
        return datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        raise ValidacionError("fecha", "formato esperado AAAA-MM-DD") from None


def validar_datos(datos, hoy):
    """Devuelve (estudiante, tipo, descripcion, prioridad, fecha) o lanza ValidacionError."""
    estudiante = validar_estudiante(datos.nombre, datos.legajo, datos.mail)
    tipo = TipoSolicitud.desde_texto(datos.tipo, "tipo")
    descripcion = validar_descripcion(datos.descripcion)
    prioridad = resolver_prioridad(tipo, datos.prioridad)
    fecha = resolver_fecha(datos.fecha, hoy)
    return estudiante, tipo, descripcion, prioridad, fecha
