"""Catalogos del dominio y sus reglas de negocio.

Reemplaza las cadenas magicas y las cadenas if/elif duplicadas de la version inicial por
datos declarativos: agregar un tipo de solicitud es agregar UNA entrada a REGLAS_POR_TIPO (OCP).
"""
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet

from .errores import ValidacionError


class _EnumTexto(str, Enum):
    @classmethod
    def desde_texto(cls, texto, campo):
        try:
            return cls(texto)
        except ValueError:
            validos = ", ".join(m.value for m in cls)
            raise ValidacionError(campo, "'%s' no es valido (opciones: %s)" % (texto, validos)) from None


class Prioridad(_EnumTexto):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"

    @property
    def orden(self):
        return list(Prioridad).index(self)


class Area(_EnumTexto):
    ALUMNADO = "ALUMNADO"
    SECRETARIA = "SECRETARIA"
    BEDELIA = "BEDELIA"


class Estado(_EnumTexto):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    RESUELTA = "RESUELTA"
    RECHAZADA = "RECHAZADA"

    @property
    def es_final(self):
        return not TRANSICIONES[self]

    def puede_pasar_a(self, nuevo):
        return nuevo in TRANSICIONES[self]


TRANSICIONES = {
    Estado.PENDIENTE: frozenset({Estado.EN_PROCESO, Estado.RECHAZADA}),
    Estado.EN_PROCESO: frozenset({Estado.RESUELTA, Estado.RECHAZADA}),
    Estado.RESUELTA: frozenset(),
    Estado.RECHAZADA: frozenset(),
}


@dataclass(frozen=True)
class ReglaTipo:
    prioridad_por_defecto: Prioridad
    areas_permitidas: FrozenSet[Area]
    sla_dias: int

    def acepta_area(self, area):
        return area in self.areas_permitidas


class TipoSolicitud(_EnumTexto):
    CERTIFICADO = "CERTIFICADO"
    EQUIVALENCIA = "EQUIVALENCIA"
    REINCORPORACION = "REINCORPORACION"
    BAJA = "BAJA"
    OTRO = "OTRO"

    @property
    def regla(self):
        return REGLAS_POR_TIPO[self]


REGLAS_POR_TIPO = {
    TipoSolicitud.CERTIFICADO: ReglaTipo(Prioridad.BAJA, frozenset({Area.ALUMNADO}), 5),
    TipoSolicitud.EQUIVALENCIA: ReglaTipo(Prioridad.MEDIA, frozenset({Area.SECRETARIA}), 30),
    TipoSolicitud.REINCORPORACION: ReglaTipo(Prioridad.ALTA, frozenset({Area.SECRETARIA}), 15),
    TipoSolicitud.BAJA: ReglaTipo(Prioridad.ALTA, frozenset({Area.ALUMNADO}), 10),
    TipoSolicitud.OTRO: ReglaTipo(Prioridad.MEDIA, frozenset(Area), 20),
}
