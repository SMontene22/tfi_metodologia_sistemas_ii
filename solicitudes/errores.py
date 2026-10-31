"""Errores del dominio: reemplazan los codigos numericos y los `print` de la version inicial."""


class ErrorDeDominio(Exception):
    """Base de todos los errores de negocio."""


class ValidacionError(ErrorDeDominio):
    """Un dato de entrada es invalido. `campo` indica cual (nombre, legajo, mail, ...)."""

    def __init__(self, campo, mensaje):
        super().__init__("%s invalido: %s" % (campo, mensaje))
        self.campo = campo


class SolicitudNoEncontrada(ErrorDeDominio):
    def __init__(self, id_solicitud):
        super().__init__("No existe la solicitud #%s" % id_solicitud)
        self.id_solicitud = id_solicitud


class TransicionInvalida(ErrorDeDominio):
    """El cambio de estado no esta permitido por el flujo de trabajo."""


class AsignacionInvalida(ErrorDeDominio):
    """No se puede asignar el responsable (solicitud cerrada o area no habilitada)."""


class ErrorDePersistencia(ErrorDeDominio):
    """El almacenamiento no pudo leerse o escribirse."""
