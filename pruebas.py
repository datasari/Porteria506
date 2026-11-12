import os
import shutil
import tempfile
from datetime import datetime, timedelta

from excepciones import (ErrorPorteria, ApartamentoInexistente, BloqueInexistente, GuiaDuplicada,
                         SinPendientes, ResidenteNoAutorizado, ResidenteDuplicado, ArregloLleno,
                         PosicionInvalida, TipoInvalido, CamionVacio, ArchivoDanado, ArchivoInexistente)
from arreglo import Arreglo
from paquetes import Paquete, Sobre, Caja, Perecedero, Voluminoso
from recepcion import ListaPaquetes, Cola
from unidad import Unidad, Residente, ArregloResidentes
from archivos import cargar_todo, guardar_todo
from Arbol import ArbolGuias

os.chdir(os.path.dirname(os.path.abspath(__file__)))

RESULTADOS = {"bien": 0, "mal": 0}
FECHA = datetime(2026, 10, 1, 9, 0)


def revisar(nombre, condicion):
    if condicion:
        RESULTADOS["bien"] += 1
    else:
        RESULTADOS["mal"] += 1
        print(f"  ❌ {nombre}")


def lanza(funcion, tipo):
    try:
        funcion()
    except tipo:
        return True
    except Exception:
        return False
    return False


def guias(lista):
    texto = ""
    actual = lista.cabeza
    while actual is not None:
        texto += actual.dato.guia + " "
        actual = actual.siguiente
    return texto.strip()


def unidad_de_prueba():
    u = Unidad("Prueba")
    u.agregar_bloque(1, 14, 12)
    u.agregar_bloque(2, 14, 12)
    u.agregar_bloque(3, 17, 10)
    u.apartamento(2, 1204).agregar_residente(Residente("111", "Sara"))
    return u


def probar_excepciones():
    def lanzar_hija():
        raise GuiaDuplicada("X")
    revisar("la madre atrapa a las hijas", lanza(lanzar_hija, ErrorPorteria))
    revisar("mensaje completo", str(ApartamentoInexistente(2, 9901)) == "El apartamento 9901 no existe en el bloque 2")


def probar_arreglo():
    a = ArregloResidentes(2)
    revisar("vacío", a.esta_vacio() and a.cantidad() == 0)
    a.agregar(Residente("1", "Ana"))
    revisar("rechaza otro tipo", lanza(lambda: a.agregar(Caja("C1", "X")), TipoInvalido))
    a.agregar(Residente("2", "Beto"))
    revisar("lleno", a.esta_lleno())
    revisar("agregar lleno", lanza(lambda: a.agregar(Residente("3", "Caro")), ArregloLleno))
    revisar("buscar", a.buscar("2").nombre == "Beto" and a.buscar("9") is None)
    revisar("obtener fuera de rango", lanza(lambda: a.obtener(2), PosicionInvalida))
    revisar("eliminar lleno", a.eliminar(0).nombre == "Ana" and a.obtener(0).nombre == "Beto")
    revisar("eliminar(-1)", lanza(lambda: a.eliminar(-1), PosicionInvalida))
    revisar("eliminar(cantidad)", lanza(lambda: a.eliminar(1), PosicionInvalida))
    b = Arreglo(1)
    revisar("Arreglo base acepta todo", b.validar_tipo("x") and b.capacidad() == 1)


def probar_paquetes():
    tipos = [Sobre("S", "X", FECHA), Caja("C", "X", FECHA), Perecedero("P", "X", FECHA), Voluminoso("V", "X", FECHA)]
    revisar("polimorfismo días", [p.dias_maximos() for p in tipos] == [30, 15, 1, 7])
    revisar("ubicaciones distintas", len({p.ubicacion() for p in tipos}) == 4)
    revisar("Paquete es abstracto", lanza(lambda: Paquete("X", "Y"), TypeError))
    p = Perecedero(" rp-1 ", "Rappi", FECHA)
    revisar("guía en mayúsculas sin espacios", p.guia == "RP-1")
    revisar("guía vacía", lanza(lambda: Caja("  ", "X"), ErrorPorteria))
    revisar("no vencido el mismo día", not p.esta_vencido(FECHA + timedelta(hours=5)))
    revisar("vencido a los 2 días", p.esta_vencido(FECHA + timedelta(days=2)))
    p.marcar_entregado("Sara", FECHA + timedelta(hours=3))
    revisar("estado entregado", p.estado == "Entregado" and p.recibido_por == "Sara")
    revisar("no se entrega dos veces", lanza(lambda: p.marcar_entregado("Otro"), ErrorPorteria))
    revisar("días cuentan hasta la entrega", p.dias_en_porteria(FECHA + timedelta(days=9)) == 0)
    p.devolver_a_pendiente()
    revisar("devolver a pendiente", p.estado == "Pendiente" and p.entregado_en is None)


def probar_lista():
    lista = ListaPaquetes()
    revisar("quitar en vacía", lanza(lambda: lista.quitar("X"), SinPendientes))
    revisar("quitar_primero en vacía", lanza(lambda: lista.quitar_primero(), SinPendientes))
    for g in ["A", "B", "C"]:
        lista.agregar(Caja(g, "X"))
    revisar("orden de llegada", guias(lista) == "A B C" and lista.cantidad() == 3)
    revisar("quitar el del medio", lista.quitar("B").guia == "B" and guias(lista) == "A C")
    revisar("quitar el primero", lista.quitar("A").guia == "A" and guias(lista) == "C")
    revisar("quitar inexistente", lanza(lambda: lista.quitar("Z"), SinPendientes) and lista.cantidad() == 1)
    revisar("quitar el único", lista.quitar("C").guia == "C" and lista.esta_vacia())
    lista.agregar(Caja("D", "X"))
    revisar("agregar después de vaciar", guias(lista) == "D")
    lista.agregar(Caja("E", "X"))
    lista.quitar("E")
    lista.agregar(Caja("F", "X"))
    revisar("quitar el último y seguir agregando", guias(lista) == "D F")
    revisar("buscar", lista.buscar("F").guia == "F" and lista.buscar("Z") is None)
    revisar("__str__ vacía", str(ListaPaquetes()) == "Sin paquetes")


def probar_cola():
    c = Cola()
    revisar("desencolar vacía", lanza(c.desencolar, CamionVacio) and lanza(c.ver_frente, CamionVacio))
    for x in [1, 2, 3]:
        c.encolar(x)
    revisar("FIFO", c.ver_frente() == 1 and c.desencolar() == 1 and c.desencolar() == 2)
    c.encolar(4)
    revisar("sigue en orden", c.desencolar() == 3 and c.desencolar() == 4 and c.esta_vacia())
    c.encolar(5)
    revisar("vaciar y volver a llenar", c.cantidad() == 1 and c.desencolar() == 5)


def probar_unidad():
    u = unidad_de_prueba()
    revisar("506 apartamentos", u.total_apartamentos() == 506)
    a = u.apartamento(2, 1204)
    revisar("acceso directo", a.numero == 1204 and a.bloque.nombre == "2")
    revisar("primero y último", u.apartamento(1, 101).numero == 101 and u.apartamento(3, 1710).numero == 1710)
    revisar("bloque inexistente", lanza(lambda: u.apartamento(4, 101), BloqueInexistente))
    for numero in [9901, 1213, 1500, 1200, 0, 99]:
        revisar(f"apto {numero} inexistente", lanza(lambda: u.apartamento(2, numero), ApartamentoInexistente))
    revisar("bloque repetido", lanza(lambda: u.agregar_bloque(1, 2, 2), ErrorPorteria))
    revisar("residente repetido", lanza(lambda: a.agregar_residente(Residente("111", "Otra")), ResidenteDuplicado))
    revisar("documento no numérico", lanza(lambda: Residente("abc", "X"), ErrorPorteria))
    u.registrar_llegada(2, 1204, Caja("G1", "X"))
    u.registrar_llegada(2, 1204, Sobre("G2", "X"))
    revisar("guía duplicada en otro apto", lanza(lambda: u.registrar_llegada(1, 101, Caja("g1", "X")), GuiaDuplicada))
    revisar("total pendientes", u.total_pendientes() == 2)
    revisar("no autorizado", lanza(lambda: u.entregar(2, 1204, "999"), ResidenteNoAutorizado))
    revisar("sigue con 2 tras el rechazo", a.pendientes.cantidad() == 2)
    p = u.entregar_guia(2, 1204, "g2", "111")
    revisar("entregar una guía", p.guia == "G2" and p.recibido_por == "Sara" and guias(a.pendientes) == "G1")
    entregados = u.entregar(2, 1204, "111")
    revisar("entregar todos", entregados.cantidad() == 1 and not a.tiene_pendientes())
    revisar("sin pendientes", lanza(lambda: u.entregar(2, 1204, "111"), SinPendientes))
    revisar("guía entregada se puede reutilizar", u.registrar_llegada(1, 101, Caja("G1", "X")).numero == 101)


def probar_camion():
    u = unidad_de_prueba()
    revisar("camión vacío", lanza(u.siguiente_del_camion, CamionVacio))
    for g in ["K1", "K2", "K3"]:
        u.descargar_camion(Caja(g, "X"))
    revisar("frente del camión", u.siguiente_del_camion().guia == "K1")
    revisar("apto inexistente no saca del camión",
            lanza(lambda: u.registrar_del_camion(2, 9999), ApartamentoInexistente) and u.camion.cantidad() == 3)
    u.registrar_del_camion(2, 1204)
    revisar("registrado y sacado", u.camion.cantidad() == 2 and u.apartamento(2, 1204).pendientes.buscar("K1") is not None)
    revisar("rechazar", u.rechazar_del_camion().guia == "K2" and u.siguiente_del_camion().guia == "K3")
    u.registrar_del_camion(1, 101)
    revisar("camión vacío al final", u.camion.esta_vacia())


def probar_archivos():
    revisar("sin bloques.csv", lanza(lambda: cargar_todo("no_existe"), ArchivoInexistente))
    u, entregados = cargar_todo("datos")
    revisar("carga ejemplo", u.total_apartamentos() == 506 and u.total_pendientes() == 3 and entregados.cantidad() == 1)
    revisar("residentes cargados", u.apartamento(2, 1204).esta_autorizado("1037000112"))
    revisar("fábrica de tipos", type(u.apartamento(3, 1710).pendientes.buscar("CO-55021")).__name__ == "Voluminoso")
    carpeta = tempfile.mkdtemp()
    try:
        guardar_todo(u, carpeta, entregados)
        u2, e2 = cargar_todo(carpeta)
        revisar("guardar y cargar", u2.total_pendientes() == 3 and e2.cantidad() == 1
                and e2.cabeza.dato.recibido_por == "Manuela Salazar")
        with open(os.path.join(carpeta, "paquetes.csv"), "a", encoding="utf-8") as f:
            f.write("Maleta,X-1,Y,1,101,2026-10-01 09:00,Pendiente,,\n")
        revisar("línea dañada", lanza(lambda: cargar_todo(carpeta), ArchivoDanado))
        try:
            cargar_todo(carpeta)
        except ArchivoDanado as e:
            revisar("dice la línea", "línea 6" in str(e))
    finally:
        shutil.rmtree(carpeta)


def probar_arbol():
    arbol = ArbolGuias()
    revisar("árbol vacío", arbol.esta_vacio() and arbol.buscar("X") is None)
    for g in ["M5", "C3", "T8", "A1", "E4", "Z9"]:
        arbol.insertar(Caja(g, "X"))
    revisar("cantidad del árbol", arbol.cantidad() == 6)
    revisar("en orden sale ordenado", arbol.en_orden() == "A1 C3 E4 M5 T8 Z9")
    revisar("buscar en el árbol", arbol.buscar("E4").guia == "E4" and arbol.buscar("B2") is None)
    revisar("altura", arbol.altura() == 3)
    arbol.insertar(Sobre("E4", "Y"))
    revisar("misma guía reemplaza", arbol.cantidad() == 6 and arbol.buscar("E4").tipo() == "Sobre")
    u = unidad_de_prueba()
    u.registrar_llegada(2, 1204, Caja("G1", "X"))
    revisar("unidad busca con el árbol", u.buscar_pendiente("g1") is u.buscar_pendiente_lineal("G1"))
    u.entregar(2, 1204, "111")
    revisar("entregado ya no es pendiente", u.buscar_pendiente("G1") is None and u.guias.buscar("G1") is not None)


if __name__ == "__main__":
    for nombre, prueba in [("Excepciones", probar_excepciones), ("Arreglo", probar_arreglo),
                           ("Paquetes", probar_paquetes), ("Lista de pendientes", probar_lista),
                           ("Cola", probar_cola), ("Unidad", probar_unidad),
                           ("Camión", probar_camion), ("Archivos", probar_archivos),
                           ("Árbol de guías", probar_arbol)]:
        antes = RESULTADOS["mal"]
        prueba()
        print(f"{'✅' if RESULTADOS['mal'] == antes else '❌'} {nombre}")
    print(f"\n{RESULTADOS['bien']} pruebas bien, {RESULTADOS['mal']} mal")
