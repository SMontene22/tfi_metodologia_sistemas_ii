"""Entidades y objetos de parametro del dominio."""
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional, Union

from .catalogos import Area, Estado, Prioridad, TipoSolicitud
from .errores import AsignacionInvalida, TransicionInvalida


@dataclass(frozen=True)
class Estudiante:
    nombre: str
    legajo: str
    mail: str


@dataclass(frozen=True)
class Responsable:
    nombre: str
    area: Area


@dataclass
class Solicitud:
    id: int
    estudiante: Estudiante
    tipo: TipoSolicitud
    descripcion: str
    prioridad: Prioridad
    fecha: date
    estado: Estado = Estado.PENDIENTE
    responsable: Optional[Responsable] = None

    @property
    def esta_cerrada(self):
        return self.estado.es_final

    def asignar(self, responsable):
        if self.esta_cerrada:
            raise AsignacionInvalida("La solicitud #%d esta %s" % (self.id, self.estado.value))
        if not self.tipo.regla.acepta_area(responsable.area):
            raise AsignacionInvalida("El area %s no atiende solicitudes %s" % (responsable.area.value, self.tipo.value))
        self.responsable = responsable

    def cambiar_estado(self, nuevo):
        if not self.estado.puede_pasar_a(nuevo):
            raise TransicionInvalida("No se puede pasar de %s a %s" % (self.estado.value, nuevo.value))
        if nuevo is Estado.EN_PROCESO and self.responsable is None:
            raise TransicionInvalida("Falta asignar un responsable antes de pasar a EN_PROCESO")
        self.estado = nuevo

    def fecha_limite(self):
        return self.fecha + timedelta(days=self.tipo.regla.sla_dias)

    def esta_vencida(self, hoy):
        return not self.esta_cerrada and self.fecha_limite() < hoy


@dataclass(frozen=True)
class DatosSolicitud:
    """Parameter Object: reemplaza la lista de 8 parametros de `reg`."""
    nombre: str
    legajo: str
    mail: str
    tipo: Union[TipoSolicitud, str]
    descripcion: str
    prioridad: Union[Prioridad, str, None] = None
    fecha: Union[date, str, None] = None


@dataclass(frozen=True)
class FiltroSolicitudes:
    """Parameter Object de busqueda; los criterios informados se combinan con AND."""
    estado: Optional[Estado] = None
    tipo: Optional[TipoSolicitud] = None
    prioridad: Optional[Prioridad] = None
    legajo: Optional[str] = None
    texto: Optional[str] = None

    def coincide(self, s):
        return (
            (self.estado is None or s.estado is self.estado)
            and (self.tipo is None or s.tipo is self.tipo)
            and (self.prioridad is None or s.prioridad is self.prioridad)
            and (self.legajo is None or s.estudiante.legajo == self.legajo)
            and (self.texto is None or self.texto.lower() in s.descripcion.lower())
        )
