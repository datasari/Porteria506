import os
from datetime import datetime

from excepciones import ErrorPorteria
from paquetes import Caja, Sobre, Perecedero
from archivos import cargar_todo, guardar_todo

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def demo():
    unidad, entregados = cargar_todo("datos")
    print(f"{unidad.nombre}: {unidad.total_apartamentos()} apartamentos, "
          f"{unidad.total_pendientes()} paquetes pendientes")

    apto = unidad.apartamento(2, 1204)
    print(f"\nPendientes del {apto}:")
    print(apto.pendientes)

    unidad.descargar_camion(Caja("SV-500001", "Servientrega", datetime(2026, 10, 6, 8, 0)))
    unidad.descargar_camion(Perecedero("RP-20001", "Rappi", datetime(2026, 10, 6, 8, 0)))
    unidad.descargar_camion(Sobre("SV-448120", "Servientrega", datetime(2026, 10, 6, 8, 0)))
    print(f"\nLlegó el camión con {unidad.camion.cantidad()} paquetes")

    for bloque, numero in [(1, 101), (3, 1710), (2, 1204)]:
        paquete = unidad.siguiente_del_camion()
        try:
            destino = unidad.registrar_del_camion(bloque, numero)
            print(f"  {paquete.guia} -> {destino}")
        except ErrorPorteria as e:
            print(f"  {paquete.guia}: {e}")
            unidad.rechazar_del_camion()
    print(f"Quedan en el camión: {unidad.camion.cantidad()}")

    try:
        unidad.entregar(2, 1204, "99999")
    except ErrorPorteria as e:
        print(f"\n{e}")

    recibidos = unidad.entregar(2, 1204, "1037000112", datetime(2026, 10, 6, 18, 30))
    print(f"\nSe entregaron {recibidos.cantidad()} paquetes a Tomás:")
    print(recibidos)

    try:
        unidad.apartamento(2, 1513)
    except ErrorPorteria as e:
        print(f"\n{e}")

    actual = recibidos.cabeza
    while actual is not None:
        entregados.agregar(actual.dato)
        actual = actual.siguiente
    guardar_todo(unidad, "datos_guardados", entregados)
    otra, otros_entregados = cargar_todo("datos_guardados")
    print(f"\nGuardado y vuelto a cargar: {otra.total_pendientes()} pendientes, "
          f"{otros_entregados.cantidad()} entregados")


if __name__ == "__main__":
    demo()
