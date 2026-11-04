"""Pruebas de las reglas principales, con memoria y una fecha fija."""
from dataclasses import replace
from datetime import date, timedelta
import unittest

from solicitudes.catalogos import Area, Estado, Prioridad, TipoSolicitud
from solicitudes.errores import (
    AsignacionInvalida, SolicitudNoEncontrada, TransicionInvalida, ValidacionError,
)
from solicitudes.modelos import DatosSolicitud, FiltroSolicitudes, Responsable
from solicitudes.reloj import RelojFijo
from solicitudes.repositorio import RepositorioMemoria
from solicitudes.servicio import ServicioSolicitudes


HOY = date(2025, 6, 30)


class TestServicio(unittest.TestCase):
    def setUp(self):
        self.repositorio = RepositorioMemoria()
        self.servicio = ServicioSolicitudes(self.repositorio, RelojFijo(HOY))
        self.datos = DatosSolicitud("Ana Perez", "12345", "ana@mail.com",
                                    "CERTIFICADO", "Certificado de alumno regular")

    def test_registrar_asigna_id_estado_y_prioridad(self):
        # Preparar: setUp crea un servicio vacio y datos validos.
        # Ejecutar:
        primera = self.servicio.registrar(self.datos)
        segunda = self.servicio.registrar(self.datos)
        # Comprobar:
        self.assertEqual([1, 2], [primera.id, segunda.id])
        self.assertEqual(Estado.PENDIENTE, primera.estado)
        self.assertEqual(Prioridad.BAJA, primera.prioridad)
        self.assertEqual(self.datos.nombre, primera.estudiante.nombre)

    def test_registrar_rechaza_datos_invalidos_sin_guardar(self):
        casos = {"nombre": " ", "legajo": "1234", "mail": "sinarroba",
                 "tipo": "VIAJE", "descripcion": " ", "prioridad": "URGENTE"}
        for campo, valor in casos.items():
            with self.subTest(campo=campo):
                with self.assertRaises(ValidacionError) as error:
                    self.servicio.registrar(replace(self.datos, **{campo: valor}))
                self.assertEqual(campo, error.exception.campo)
                self.assertEqual([], self.servicio.listar())
        self.assertEqual(1, self.servicio.registrar(self.datos).id)

    def test_registrar_usa_prioridad_y_fecha_indicadas(self):
        solicitud = self.servicio.registrar(replace(
            self.datos, prioridad="ALTA", fecha="2025-06-20"))
        self.assertEqual(Prioridad.ALTA, solicitud.prioridad)
        self.assertEqual(date(2025, 6, 20), solicitud.fecha)

    def test_registrar_usa_fecha_del_reloj(self):
        solicitud = self.servicio.registrar(self.datos)
        self.assertEqual(HOY, solicitud.fecha)

    def test_fecha_invalida_no_se_guarda(self):
        with self.assertRaises(ValidacionError) as error:
            self.servicio.registrar(replace(self.datos, fecha="2025-02-30"))
        self.assertEqual("fecha", error.exception.campo)
        self.assertEqual([], self.servicio.listar())

    def test_todos_los_tipos_tienen_regla(self):
        esperadas = {"CERTIFICADO": ("BAJA", 5), "EQUIVALENCIA": ("MEDIA", 30),
                     "REINCORPORACION": ("ALTA", 15), "BAJA": ("ALTA", 10),
                     "OTRO": ("MEDIA", 20)}
        self.assertEqual(set(esperadas), {tipo.value for tipo in TipoSolicitud})
        for tipo, (prioridad, dias) in esperadas.items():
            with self.subTest(tipo=tipo):
                solicitud = self.servicio.registrar(replace(self.datos, tipo=tipo))
                self.assertEqual(prioridad, solicitud.prioridad.value)
                self.assertEqual(HOY + timedelta(days=dias), solicitud.fecha_limite())

    def test_asignacion_respeta_area_del_tipo(self):
        permitidas = {"CERTIFICADO": {"ALUMNADO"}, "EQUIVALENCIA": {"SECRETARIA"},
                      "REINCORPORACION": {"SECRETARIA"}, "BAJA": {"ALUMNADO"},
                      "OTRO": {"ALUMNADO", "SECRETARIA", "BEDELIA"}}
        for tipo, areas in permitidas.items():
            for area in Area:
                with self.subTest(tipo=tipo, area=area):
                    solicitud = self.servicio.registrar(replace(self.datos, tipo=tipo))
                    responsable = Responsable("Carlos Ruiz", area)
                    if area.value in areas:
                        self.servicio.asignar_responsable(solicitud.id, responsable)
                        self.assertEqual(responsable, solicitud.responsable)
                    else:
                        with self.assertRaises(AsignacionInvalida):
                            self.servicio.asignar_responsable(solicitud.id, responsable)
                        self.assertIsNone(solicitud.responsable)

    def test_no_permite_iniciar_sin_responsable(self):
        solicitud = self.servicio.registrar(self.datos)
        with self.assertRaises(TransicionInvalida):
            self.servicio.cambiar_estado(solicitud.id, Estado.EN_PROCESO)
        self.assertEqual(Estado.PENDIENTE, solicitud.estado)

    def test_transiciones_permitidas_y_rechazadas(self):
        permitidas = {("PENDIENTE", "EN_PROCESO"), ("PENDIENTE", "RECHAZADA"),
                      ("EN_PROCESO", "RESUELTA"), ("EN_PROCESO", "RECHAZADA")}
        for origen in Estado:
            for destino in Estado:
                with self.subTest(origen=origen, destino=destino):
                    solicitud = self.servicio.registrar(self.datos)
                    self.servicio.asignar_responsable(
                        solicitud.id, Responsable("Carlos Ruiz", Area.ALUMNADO))
                    solicitud.estado = origen  # Preparar cada estado de partida.
                    if (origen.value, destino.value) in permitidas:
                        self.servicio.cambiar_estado(solicitud.id, destino)
                        self.assertEqual(destino, solicitud.estado)
                    else:
                        with self.assertRaises(TransicionInvalida):
                            self.servicio.cambiar_estado(solicitud.id, destino)
                        self.assertEqual(origen, solicitud.estado)

    def test_no_asigna_a_solicitudes_cerradas(self):
        for estado in (Estado.RESUELTA, Estado.RECHAZADA):
            with self.subTest(estado=estado):
                solicitud = self.servicio.registrar(self.datos)
                solicitud.estado = estado
                with self.assertRaises(AsignacionInvalida):
                    self.servicio.asignar_responsable(
                        solicitud.id, Responsable("Carlos Ruiz", Area.ALUMNADO))
                self.assertIsNone(solicitud.responsable)

    def test_operaciones_sobre_id_inexistente(self):
        with self.assertRaises(SolicitudNoEncontrada):
            self.servicio.cambiar_estado(99, Estado.EN_PROCESO)
        with self.assertRaises(SolicitudNoEncontrada):
            self.servicio.asignar_responsable(99, Responsable("Carlos Ruiz", Area.ALUMNADO))

    def test_buscar_por_criterios_y_combinaciones(self):
        self.servicio.registrar(self.datos)
        self.servicio.registrar(replace(self.datos, nombre="Luis Gomez", legajo="23456",
                                       tipo="EQUIVALENCIA", descripcion="Equivalencia de Algebra"))
        tercera = self.servicio.registrar(replace(self.datos, tipo="BAJA"))
        self.servicio.cambiar_estado(tercera.id, Estado.RECHAZADA)
        casos = [(None, [1, 2, 3]), (FiltroSolicitudes(tipo=TipoSolicitud.CERTIFICADO), [1]),
                 (FiltroSolicitudes(estado=Estado.RECHAZADA), [3]),
                 (FiltroSolicitudes(prioridad=Prioridad.MEDIA), [2]),
                 (FiltroSolicitudes(legajo="12345"), [1, 3]),
                 (FiltroSolicitudes(texto="ALGEBRA"), [2]),
                 (FiltroSolicitudes(legajo="12345", estado=Estado.PENDIENTE), [1]),
                 (FiltroSolicitudes(texto="inexistente"), [])]
        for filtro, ids in casos:
            with self.subTest(filtro=filtro):
                self.assertEqual(ids, [s.id for s in self.servicio.buscar(filtro)])

    def test_reporte_usa_el_reloj_inyectado(self):
        for tipo, dias in [("CERTIFICADO", 5), ("EQUIVALENCIA", 30),
                           ("REINCORPORACION", 15), ("BAJA", 10), ("OTRO", 20)]:
            with self.subTest(tipo=tipo):
                repositorio = RepositorioMemoria()
                servicio = ServicioSolicitudes(repositorio, RelojFijo(HOY))
                solicitud = servicio.registrar(replace(self.datos, tipo=tipo))
                limite = HOY + timedelta(days=dias)
                for hoy, vencida in [(limite - timedelta(days=1), False),
                                     (limite, False), (limite + timedelta(days=1), True)]:
                    otro_reloj = ServicioSolicitudes(repositorio, RelojFijo(hoy))
                    self.assertEqual(vencida, "VENCIDA" in otro_reloj.reporte())
                servicio.cambiar_estado(solicitud.id, Estado.RECHAZADA)
                self.assertNotIn("VENCIDA", otro_reloj.reporte())

    def test_reporte_ordena_por_prioridad_fecha_e_id(self):
        for prioridad, fecha in [("BAJA", "2025-06-01"), ("ALTA", "2025-06-20"),
                                 ("ALTA", "2025-06-10"), ("ALTA", "2025-06-10")]:
            self.servicio.registrar(replace(self.datos, prioridad=prioridad, fecha=fecha))
        detalle = [linea.split()[0] for linea in self.servicio.reporte().splitlines()
                   if linea.startswith("#")]
        self.assertEqual(["#3", "#4", "#2", "#1"], detalle)

    def test_reporte_vacio(self):
        self.assertEqual("=== REPORTE DE SOLICITUDES ===\nTotal: 0\nPENDIENTE: 0\n"
                         "EN_PROCESO: 0\nRESUELTA: 0\nRECHAZADA: 0\n--- Detalle ---",
                         self.servicio.reporte())


if __name__ == "__main__":
    unittest.main()
