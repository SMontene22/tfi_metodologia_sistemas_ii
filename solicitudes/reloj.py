"""Abstraccion del reloj: elimina la dependencia oculta de `date.today()`."""
from datetime import date


class RelojSistema:
    def hoy(self):
        return date.today()


class RelojFijo:
    def __init__(self, fecha):
        self._fecha = fecha

    def hoy(self):
        return self._fecha
