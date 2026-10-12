import os
from datetime import datetime

from excepciones import ErrorPorteria, ArchivoDanado, ArchivoInexistente
from paquetes import TIPOS, FORMATO_FECHA
from recepcion import ListaPaquetes
from unidad import Unidad, Residente


def contar_lineas(ruta):
    total = 0
    with open(ruta, "r", encoding="utf-8") as f:
        f.readline()
        for linea in f:
            if linea.strip():
                total += 1
    return total


def leer_fecha(texto):
    texto = texto.strip()
    if not texto:
        return None
    return datetime.strptime(texto, FORMATO_FECHA)


def cargar_bloques(ruta, nombre_unidad):
    if not os.path.exists(ruta):
        raise ArchivoInexistente(ruta)
    unidad = Unidad(nombre_unidad, contar_lineas(ruta))
    with open(ruta, "r", encoding="utf-8") as f:
        f.readline()
        for numero_linea, linea in enumerate(f, start=2):
            if not linea.strip():
                continue
            try:
                d = linea.strip().split(",")
                unidad.agregar_bloque(d[0], int(d[1]), int(d[2]))
            except (ValueError, IndexError, ErrorPorteria):
                raise ArchivoDanado(ruta, numero_linea)
    return unidad


def cargar_residentes(unidad, ruta):
    cargados = 0
    if not os.path.exists(ruta):
        return cargados
    with open(ruta, "r", encoding="utf-8") as f:
        f.readline()
        for numero_linea, linea in enumerate(f, start=2):
            if not linea.strip():
                continue
            try:
                d = linea.strip().split(",")
                apartamento = unidad.apartamento(d[0], d[1])
                residente = Residente(d[2], d[3], d[4])
                apartamento.agregar_residente(residente)
                cargados += 1
            except (ValueError, IndexError, ErrorPorteria):
                raise ArchivoDanado(ruta, numero_linea)
    return cargados


def cargar_paquetes(unidad, ruta):
    entregados = ListaPaquetes()
    if not os.path.exists(ruta):
        return entregados
    with open(ruta, "r", encoding="utf-8") as f:
        f.readline()
        for numero_linea, linea in enumerate(f, start=2):
            if not linea.strip():
                continue
            try:
                d = linea.rstrip("\n").split(",")
                paquete = TIPOS[d[0]](d[1], d[2], leer_fecha(d[5]))
                if d[6] == "Pendiente":
                    unidad.registrar_llegada(d[3], d[4], paquete)
                elif d[6] == "Entregado":
                    destino = unidad.apartamento(d[3], d[4])
                    paquete.asignar_destino(destino)
                    paquete.marcar_entregado(d[8], leer_fecha(d[7]))
                    entregados.agregar(paquete)
                else:
                    raise ValueError(d[6])
            except (KeyError, ValueError, IndexError, ErrorPorteria):
                raise ArchivoDanado(ruta, numero_linea)
    return entregados


def cargar_todo(carpeta, nombre_unidad="Unidad 506"):
    bloques = os.path.join(carpeta, "bloques.csv")
    residentes = os.path.join(carpeta, "residentes.csv")
    paquetes = os.path.join(carpeta, "paquetes.csv")
    unidad = cargar_bloques(bloques, nombre_unidad)
    cargar_residentes(unidad, residentes)
    entregados = cargar_paquetes(unidad, paquetes)
    return unidad, entregados


def escribir_lista(f, lista):
    actual = lista.cabeza
    while actual is not None:
        f.write(actual.dato.a_fila() + "\n")
        actual = actual.siguiente


CABECERA_RESIDENTES = "bloque,apartamento,documento,nombre,telefono\n"
CABECERA_PAQUETES = ("tipo,guia,transportadora,bloque,apartamento,"
                     "llegada,estado,entregado_en,recibido_por\n")


def guardar_todo(unidad, carpeta, entregados=None):
    os.makedirs(carpeta, exist_ok=True)
    bloques = unidad.bloques
    ruta = os.path.join(carpeta, "bloques.csv")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("bloque,pisos,aptos_por_piso\n")
        for i in range(bloques.cantidad()):
            b = bloques.obtener(i)
            f.write(f"{b.nombre},{b.pisos},{b.aptos_por_piso}\n")
    ruta_r = os.path.join(carpeta, "residentes.csv")
    ruta_p = os.path.join(carpeta, "paquetes.csv")
    with open(ruta_r, "w", encoding="utf-8") as fr, \
         open(ruta_p, "w", encoding="utf-8") as fp:
        fr.write(CABECERA_RESIDENTES)
        fp.write(CABECERA_PAQUETES)
        for i in range(bloques.cantidad()):
            b = bloques.obtener(i)
            for fila in range(b.pisos):
                for columna in range(b.aptos_por_piso):
                    apto = b.apartamento_en(fila, columna)
                    for k in range(apto.residentes.cantidad()):
                        r = apto.residentes.obtener(k)
                        datos = f"{r.documento},{r.nombre},{r.telefono}"
                        fr.write(f"{b.nombre},{apto.numero},{datos}\n")
                    escribir_lista(fp, apto.pendientes)
        if entregados is not None:
            escribir_lista(fp, entregados)

