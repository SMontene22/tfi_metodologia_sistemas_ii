"""Compara el tag inicial con el codigo actual sin cambiar de rama.

Uso: python tools/verificar_antes_despues.py
Guarda las salidas y la comparacion en docs/evidencias/.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from escenario import ejecutar  # noqa: E402


def main():
    evidencias = RAIZ / "docs" / "evidencias"
    with tempfile.TemporaryDirectory() as temporal:
        base = Path(temporal) / "inicial"
        archivos = ["gestor.py", "escenario.py", "tests/test_caracterizacion.py",
                    "docs/evidencias/salida_inicial.txt"]
        for nombre in archivos:
            contenido = subprocess.check_output(
                ["git", "show", "estado-inicial:" + nombre], cwd=RAIZ)
            destino = base / nombre
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_bytes(contenido)

        prueba_inicial = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=base, capture_output=True, text=True)
        (evidencias / "pruebas_version_inicial.txt").write_text(
            "Version: estado-inicial\n" + prueba_inicial.stdout + prueba_inicial.stderr,
            encoding="utf-8")
        if prueba_inicial.returncode:
            print("Fallo la prueba inicial; consultar pruebas_version_inicial.txt")
            return 1

        datos_iniciales = base / "datos"
        datos_actuales = Path(temporal) / "actual"
        datos_iniciales.mkdir()
        datos_actuales.mkdir()
        salida_inicial = subprocess.check_output(
            [sys.executable, "-c",
             "from escenario import ejecutar; print(ejecutar('datos'), end='')"],
            cwd=base, text=True)
        salida_actual = ejecutar(str(datos_actuales))
        referencia = (evidencias / "salida_inicial.txt").read_text(encoding="utf-8")
        json_inicial = json.loads((datos_iniciales / "solicitudes.json").read_text(encoding="utf-8"))
        json_actual = json.loads((datos_actuales / "solicitudes.json").read_text(encoding="utf-8"))

    (evidencias / "salida_inicial_reproducida.txt").write_text(salida_inicial, encoding="utf-8")
    (evidencias / "salida_refactorizada.txt").write_text(salida_actual, encoding="utf-8")
    controles = {
        "Prueba de caracterizacion del tag inicial": prueba_inicial.returncode == 0,
        "Salida inicial reproducida igual a la referencia": salida_inicial == referencia,
        "Salida refactorizada igual a la inicial": salida_actual == salida_inicial,
        "Datos JSON finales iguales en ambas versiones": json_actual == json_inicial,
    }
    commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=RAIZ, text=True).strip()
    resumen = ["Comparacion antes/despues", "Base: tag estado-inicial",
               "Version actual: " + commit + " + cambios locales si los hay",
               "Fecha simulada del escenario: 2025-06-30"]
    resumen += [nombre + ": " + ("OK" if ok else "FALLO") for nombre, ok in controles.items()]
    resumen += ["SHA-256 salida inicial (texto UTF-8 con saltos LF): " +
                hashlib.sha256(salida_inicial.encode("utf-8")).hexdigest(),
                "SHA-256 salida refactorizada (texto UTF-8 con saltos LF): " +
                hashlib.sha256(salida_actual.encode("utf-8")).hexdigest(),
                "Solicitudes persistidas: " + str(len(json_actual))]
    texto = "\n".join(resumen) + "\n"
    (evidencias / "comparacion_antes_despues.txt").write_text(texto, encoding="utf-8")
    print(texto, end="")
    return 0 if all(controles.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
