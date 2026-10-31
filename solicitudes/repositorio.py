"""Repositorios de solicitudes. El servicio depende de esta interfaz, no de un archivo (DIP)."""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Protocol

from .catalogos import Area, Estado, Prioridad, TipoSolicitud
from .errores import ErrorDePersistencia
from .modelos import Estudiante, Responsable, Solicitud


class RepositorioSolicitudes(Protocol):
    def siguiente_id(self) -> int: ...
    def guardar(self, solicitud: Solicitud) -> None: ...
    def obtener(self, id_solicitud: int) -> Optional[Solicitud]: ...
    def listar(self) -> List[Solicitud]: ...


class RepositorioMemoria:
    def __init__(self):
        self._items: Dict[int, Solicitud] = {}

    def siguiente_id(self):
        return max(self._items, default=0) + 1

    def guardar(self, solicitud):
        self._items[solicitud.id] = solicitud

    def obtener(self, id_solicitud):
        return self._items.get(id_solicitud)

    def listar(self):
        return list(self._items.values())


class RepositorioJSON(RepositorioMemoria):
    """Persiste en un archivo JSON con el MISMO formato que la version inicial."""

    def __init__(self, ruta):
        super().__init__()
        self._ruta = ruta
        self._cargar()

    def guardar(self, solicitud):
        super().guardar(solicitud)
        self._volcar()

    def _cargar(self):
        if not os.path.exists(self._ruta):
            return
        try:
            with open(self._ruta, encoding="utf-8") as f:
                for fila in json.load(f):
                    s = _desde_fila(fila)
                    self._items[s.id] = s
        except (OSError, ValueError, KeyError) as error:
            raise ErrorDePersistencia("No se pudo leer %s: %s" % (self._ruta, error)) from error

    def _volcar(self):
        try:
            with open(self._ruta, "w", encoding="utf-8") as f:
                json.dump([_a_fila(s) for s in self._items.values()], f, indent=2)
        except OSError as error:
            raise ErrorDePersistencia("No se pudo escribir %s: %s" % (self._ruta, error)) from error


def _a_fila(s):
    return {
        "id": s.id, "nombre": s.estudiante.nombre, "legajo": s.estudiante.legajo,
        "mail": s.estudiante.mail, "tipo": s.tipo.value, "desc": s.descripcion,
        "prio": s.prioridad.value, "resp": s.responsable.nombre if s.responsable else None,
        "area": s.responsable.area.value if s.responsable else None,
        "fecha": s.fecha.isoformat(), "estado": s.estado.value,
    }


def _desde_fila(f):
    responsable = Responsable(f["resp"], Area(f["area"])) if f.get("resp") and f.get("area") else None
    return Solicitud(
        id=f["id"], estudiante=Estudiante(f["nombre"], f["legajo"], f["mail"]),
        tipo=TipoSolicitud(f["tipo"]), descripcion=f["desc"], prioridad=Prioridad(f["prio"]),
        fecha=datetime.strptime(f["fecha"], "%Y-%m-%d").date(), estado=Estado(f["estado"]),
        responsable=responsable,
    )
