"""Casos de uso. Orquesta validacion, reglas del modelo y persistencia (SRP)."""
from .errores import SolicitudNoEncontrada
from .modelos import FiltroSolicitudes, Solicitud
from .reporte import generar_reporte
from .validacion import validar_datos


class ServicioSolicitudes:
    def __init__(self, repositorio, reloj):
        self._repositorio = repositorio
        self._reloj = reloj

    def registrar(self, datos):
        estudiante, tipo, descripcion, prioridad, fecha = validar_datos(datos, self._reloj.hoy())
        solicitud = Solicitud(self._repositorio.siguiente_id(), estudiante, tipo, descripcion, prioridad, fecha)
        self._repositorio.guardar(solicitud)
        return solicitud

    def asignar_responsable(self, id_solicitud, responsable):
        solicitud = self._obtener(id_solicitud)
        solicitud.asignar(responsable)
        self._repositorio.guardar(solicitud)
        return solicitud

    def cambiar_estado(self, id_solicitud, nuevo_estado):
        solicitud = self._obtener(id_solicitud)
        solicitud.cambiar_estado(nuevo_estado)
        self._repositorio.guardar(solicitud)
        return solicitud

    def buscar(self, filtro=None):
        filtro = filtro or FiltroSolicitudes()
        return [s for s in self._repositorio.listar() if filtro.coincide(s)]

    def listar(self):
        return self._repositorio.listar()

    def reporte(self):
        return generar_reporte(self._repositorio.listar(), self._reloj.hoy())

    def _obtener(self, id_solicitud):
        solicitud = self._repositorio.obtener(id_solicitud)
        if solicitud is None:
            raise SolicitudNoEncontrada(id_solicitud)
        return solicitud
