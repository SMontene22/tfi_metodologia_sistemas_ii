"""Cobertura de lineas con la biblioteca estandar (`trace`). Uso: python tools/cobertura.py"""
import os
import sys
import trace
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

tracer = trace.Trace(count=1, trace=0)


def correr_pruebas():
    # La carga (import) de los modulos tambien debe ocurrir bajo el trazador.
    suite = unittest.defaultTestLoader.discover(os.path.join(RAIZ, "tests"))
    return unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, "w")).run(suite)


resultado = tracer.runfunc(correr_pruebas)
ejecutadas = {}
for (archivo, linea), _ in tracer.results().counts.items():
    ejecutadas.setdefault(os.path.abspath(archivo), set()).add(linea)

print("%-30s %6s %6s %6s" % ("modulo", "lineas", "cubiertas", "%"))
tot = cub = 0
carpeta = os.path.join(RAIZ, "solicitudes")
for nombre in sorted(os.listdir(carpeta)):
    if not nombre.endswith(".py"):
        continue
    ruta = os.path.join(carpeta, nombre)
    ejecutables = set(trace._find_executable_linenos(ruta))
    hechas = ejecutables & ejecutadas.get(ruta, set())
    tot += len(ejecutables)
    cub += len(hechas)
    print("%-30s %6d %6d %5.0f%%" % ("solicitudes/" + nombre, len(ejecutables), len(hechas),
                                      100.0 * len(hechas) / max(1, len(ejecutables))))
print("-" * 52)
print("%-30s %6d %6d %5.0f%%" % ("TOTAL", tot, cub, 100.0 * cub / max(1, tot)))
print("Pruebas: %d ejecutadas, %d fallos, %d errores" % (resultado.testsRun, len(resultado.failures), len(resultado.errors)))
