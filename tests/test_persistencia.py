"""Pruebas con archivos temporales, sin modificar los datos de la demo."""
from contextlib import redirect_stdout
from datetime import date
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from solicitudes.catalogos import Area, Estado
from solicitudes.cli import main
from solicitudes.errores import ErrorDePersistencia
from solicitudes.modelos import DatosSolicitud, Responsable
from solicitudes.reloj import RelojFijo
from solicitudes.repositorio import RepositorioJSON
from solicitudes.servicio import ServicioSolicitudes


class TestPersistencia(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        self.ruta = Path(temporal.name) / "solicitudes.json"
        self.reloj = RelojFijo(date(2025, 6, 30))
        self.datos = DatosSolicitud("Ana Perez", "12345", "ana@mail.com",
                                    "CERTIFICADO", "Certificado de alumno regular")

    def test_recarga_conserva_datos_y_siguiente_id(self):
        servicio = ServicioSolicitudes(RepositorioJSON(self.ruta), self.reloj)
        solicitud = servicio.registrar(self.datos)
        servicio.asignar_responsable(solicitud.id, Responsable("Carlos Ruiz", Area.ALUMNADO))
        servicio.cambiar_estado(solicitud.id, Estado.EN_PROCESO)
        recargado = ServicioSolicitudes(RepositorioJSON(self.ruta), self.reloj)
        self.assertEqual([solicitud], recargado.listar())
        self.assertEqual(2, recargado.registrar(self.datos).id)

    def test_guarda_formato_inicial(self):
        servicio = ServicioSolicitudes(RepositorioJSON(self.ruta), self.reloj)
        servicio.registrar(self.datos)
        filas = json.loads(self.ruta.read_text(encoding="utf-8"))
        self.assertEqual([{"id": 1, "nombre": "Ana Perez", "legajo": "12345",
                           "mail": "ana@mail.com", "tipo": "CERTIFICADO",
                           "desc": "Certificado de alumno regular", "prio": "BAJA",
                           "resp": None, "area": None, "fecha": "2025-06-30",
                           "estado": "PENDIENTE"}], filas)

    def test_json_invalido_informa_error_sin_sobrescribir(self):
        for contenido in ("{json roto", "null", "{}", "[null]", "[{}]"):
            with self.subTest(contenido=contenido):
                self.ruta.write_text(contenido, encoding="utf-8")
                with self.assertRaises(ErrorDePersistencia):
                    RepositorioJSON(self.ruta)
                self.assertEqual(contenido, self.ruta.read_text(encoding="utf-8"))

    def test_error_de_escritura_informa_causa(self):
        servicio = ServicioSolicitudes(RepositorioJSON(self.ruta), self.reloj)
        with patch("builtins.open", side_effect=OSError("sin permiso de escritura")):
            with self.assertRaises(ErrorDePersistencia) as error:
                servicio.registrar(self.datos)
        self.assertIsInstance(error.exception.__cause__, OSError)

    def test_demo_registra_y_muestra_reporte(self):
        salida = StringIO()
        with redirect_stdout(salida):
            main(self.ruta)
        self.assertIn("Total: 1", salida.getvalue())
        self.assertIn("Ana Perez", salida.getvalue())
        self.assertEqual(1, len(RepositorioJSON(self.ruta).listar()))


if __name__ == "__main__":
    unittest.main()
