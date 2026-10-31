# Sistema de Gestion de Solicitudes Academicas - VERSION INICIAL
import json
import os
import sys
from datetime import date, datetime, timedelta

ARCHIVO = "solicitudes.json"
lista = []
contador = 1


def cargar():
    global lista, contador
    try:
        f = open(ARCHIVO)
        lista = json.load(f)
        contador = max([x["id"] for x in lista] + [0]) + 1
    except:
        lista = []
        contador = 1


def guardar():
    f = open(ARCHIVO, "w")
    json.dump(lista, f, indent=2)
    f.close()


def reg(nom, leg, mail, t, desc, p=None, resp=None, f=None):
    global contador
    if nom == None or nom.strip() == "":
        print("error nombre")
        return -1
    if leg == None or len(leg) < 5:
        print("error legajo")
        return -2
    if mail == None or "@" not in mail:
        print("error mail")
        return -3
    if t != "CERTIFICADO" and t != "EQUIVALENCIA" and t != "REINCORPORACION" and t != "BAJA" and t != "OTRO":
        print("error tipo")
        return -4
    if desc == None or desc.strip() == "":
        print("error descripcion")
        return -5
    if p == None:
        if t == "REINCORPORACION":
            p = "ALTA"
        elif t == "BAJA":
            p = "ALTA"
        elif t == "EQUIVALENCIA":
            p = "MEDIA"
        elif t == "CERTIFICADO":
            p = "BAJA"
        else:
            p = "MEDIA"
    else:
        if p != "BAJA" and p != "MEDIA" and p != "ALTA":
            print("error prioridad")
            return -6
    if f == None:
        f = date.today().strftime("%Y-%m-%d")
    s = {"id": contador, "nombre": nom, "legajo": leg, "mail": mail, "tipo": t,
         "desc": desc, "prio": p, "resp": resp, "area": None, "fecha": f,
         "estado": "PENDIENTE"}
    lista.append(s)
    contador = contador + 1
    guardar()
    return s["id"]


def asig(i, resp, area):
    for s in lista:
        if s["id"] == i:
            if s["estado"] == "RESUELTA" or s["estado"] == "RECHAZADA":
                print("no se puede asignar")
                return False
            t = s["tipo"]
            if t == "CERTIFICADO" or t == "BAJA":
                if area != "ALUMNADO":
                    print("area invalida")
                    return False
            elif t == "EQUIVALENCIA" or t == "REINCORPORACION":
                if area != "SECRETARIA":
                    print("area invalida")
                    return False
            else:
                if area != "ALUMNADO" and area != "SECRETARIA" and area != "BEDELIA":
                    print("area invalida")
                    return False
            s["resp"] = resp
            s["area"] = area
            guardar()
            return True
    print("no existe")
    return False


def cambiar(i, e):
    for s in lista:
        if s["id"] == i:
            a = s["estado"]
            ok = False
            if a == "PENDIENTE" and (e == "EN_PROCESO" or e == "RECHAZADA"):
                ok = True
            if a == "EN_PROCESO" and (e == "RESUELTA" or e == "RECHAZADA"):
                ok = True
            if ok == False:
                print("transicion invalida " + a + " -> " + e)
                return False
            if e == "EN_PROCESO" and s["resp"] == None:
                print("falta responsable")
                return False
            s["estado"] = e
            guardar()
            return True
    print("no existe")
    return False


def buscar(c, v):
    r = []
    for s in lista:
        if c == "estado":
            if s["estado"] == v:
                r.append(s)
        elif c == "tipo":
            if s["tipo"] == v:
                r.append(s)
        elif c == "prio":
            if s["prio"] == v:
                r.append(s)
        elif c == "legajo":
            if s["legajo"] == v:
                r.append(s)
        elif c == "texto":
            if v.lower() in s["desc"].lower():
                r.append(s)
    return r


def sla(t):
    if t == "CERTIFICADO":
        return 5
    elif t == "EQUIVALENCIA":
        return 30
    elif t == "REINCORPORACION":
        return 15
    elif t == "BAJA":
        return 10
    else:
        return 20


# def exportar_csv():
#     for s in lista:
#         print(s["id"], s["nombre"], s["estado"], sep=";")


def viejo_buscar_por_id(i):
    for s in lista:
        if s["id"] == i:
            return s
    return None


def reporte():
    hoy = date.today()
    print("=== REPORTE DE SOLICITUDES ===")
    print("Total: " + str(len(lista)))
    for e in ["PENDIENTE", "EN_PROCESO", "RESUELTA", "RECHAZADA"]:
        n = 0
        for s in lista:
            if s["estado"] == e:
                n = n + 1
        print(e + ": " + str(n))
    print("--- Detalle ---")
    o = {"ALTA": 0, "MEDIA": 1, "BAJA": 2}
    ordenada = sorted(lista, key=lambda s: (o[s["prio"]], s["fecha"], s["id"]))
    for s in ordenada:
        linea = "#" + str(s["id"]) + " [" + s["prio"] + "] " + s["tipo"] + " | " + s["nombre"] + " (" + s["legajo"] + ") | " + s["estado"] + " | resp: " + (s["resp"] if s["resp"] else "Sin asignar") + " | " + s["fecha"]
        if s["estado"] != "RESUELTA" and s["estado"] != "RECHAZADA":
            limite = datetime.strptime(s["fecha"], "%Y-%m-%d").date() + timedelta(days=sla(s["tipo"]))
            if limite < hoy:
                linea = linea + " VENCIDA"
        print(linea)


if __name__ == "__main__":
    cargar()
    reg("Ana Perez", "12345", "ana@mail.com", "CERTIFICADO", "Certificado de alumno regular")
    reporte()
