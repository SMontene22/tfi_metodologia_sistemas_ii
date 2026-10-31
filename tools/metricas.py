"""Metricas simples de calidad interna (solo biblioteca estandar).

Uso: python tools/metricas.py archivo_o_carpeta [...]
Por funcion: lineas, parametros y complejidad ciclomatica aproximada
(1 + decisiones: if, for, while, except, and/or, if-expresion, filtros de comprension).
"""
import ast
import os
import sys


def complejidad(nodo):
    c = 1
    for n in ast.walk(nodo):
        if isinstance(n, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.IfExp)):
            c += 1
        elif isinstance(n, ast.BoolOp):
            c += len(n.values) - 1
        elif isinstance(n, ast.comprehension):
            c += len(n.ifs)
    return c


def archivos(rutas):
    for r in rutas:
        if os.path.isdir(r):
            for base, _, fs in os.walk(r):
                for f in sorted(fs):
                    if f.endswith(".py"):
                        yield os.path.join(base, f)
        else:
            yield r


def main(rutas):
    filas, total_loc = [], 0
    for ruta in archivos(rutas):
        with open(ruta, encoding="utf-8") as f:
            codigo = f.read()
        total_loc += sum(1 for l in codigo.splitlines() if l.strip() and not l.strip().startswith("#"))
        for n in ast.walk(ast.parse(codigo)):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                a = n.args
                params = len(a.args) + len(a.kwonlyargs) - (1 if a.args and a.args[0].arg in ("self", "cls") else 0)
                filas.append((ruta, n.name, n.end_lineno - n.lineno + 1, params, complejidad(n)))
    print("%-34s %-22s %5s %6s %5s" % ("archivo", "funcion", "lineas", "params", "CC"))
    for r in sorted(filas, key=lambda x: (x[0], -x[4])):
        print("%-34s %-22s %5d %6d %5d" % r)
    if filas:
        print("-" * 78)
        print("LOC (sin vacias/comentarios): %d | funciones: %d" % (total_loc, len(filas)))
        print("CC maxima: %d | CC promedio: %.2f | max parametros: %d | max lineas por funcion: %d" % (
            max(f[4] for f in filas), sum(f[4] for f in filas) / len(filas),
            max(f[3] for f in filas), max(f[2] for f in filas)))


if __name__ == "__main__":
    main(sys.argv[1:])
