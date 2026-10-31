"""Generacion del reporte como texto puro (no imprime; el llamador decide donde mostrarlo)."""
from .catalogos import Estado


def _linea_detalle(s, hoy):
    responsable = s.responsable.nombre if s.responsable else "Sin asignar"
    linea = "#%d [%s] %s | %s (%s) | %s | resp: %s | %s" % (
        s.id, s.prioridad.value, s.tipo.value, s.estudiante.nombre, s.estudiante.legajo,
        s.estado.value, responsable, s.fecha.isoformat())
    return linea + " VENCIDA" if s.esta_vencida(hoy) else linea


def _resumen_por_estado(solicitudes):
    return ["%s: %d" % (e.value, sum(1 for s in solicitudes if s.estado is e)) for e in Estado]


def generar_reporte(solicitudes, hoy):
    solicitudes = list(solicitudes)
    ordenadas = sorted(solicitudes, key=lambda s: (s.prioridad.orden, s.fecha, s.id))
    lineas = ["=== REPORTE DE SOLICITUDES ===", "Total: %d" % len(solicitudes)]
    lineas += _resumen_por_estado(solicitudes)
    lineas.append("--- Detalle ---")
    lineas += [_linea_detalle(s, hoy) for s in ordenadas]
    return "\n".join(lineas)
