import os
import random
import time

from unidad import Unidad
from paquetes import Caja

os.chdir(os.path.dirname(os.path.abspath(__file__)))

TAMANOS = [500, 2000, 8000]
BUSQUEDAS = 1000


def armar_datos(n):
    random.seed(n)
    unidad = Unidad("Experimento")
    unidad.agregar_bloque(1, 14, 12)
    unidad.agregar_bloque(2, 14, 12)
    unidad.agregar_bloque(3, 17, 10)
    lista_fp = []
    guias = []
    for numero in random.sample(range(100000, 999999), n):
        guia = f"GU-{numero}"
        bloque = random.randint(1, 3)
        pisos = 17 if bloque == 3 else 14
        aptos = 10 if bloque == 3 else 12
        apto = random.randint(1, pisos) * 100 + random.randint(1, aptos)
        unidad.registrar_llegada(bloque, apto, Caja(guia, "X"))
        lista_fp.append({"guia": guia, "bloque": bloque,
                         "apartamento": apto, "estado": "Pendiente"})
        guias.append(guia)
    return unidad, lista_fp, guias


def buscar_fp(lista_fp, guia):
    for paquete in lista_fp:
        if paquete["guia"] == guia and paquete["estado"] == "Pendiente":
            return paquete
    return None


def medir(funcion, guias):
    inicio = time.perf_counter()
    for guia in guias:
        funcion(guia)
    total = time.perf_counter() - inicio
    return total / len(guias) * 1000000


def experimento():
    print(f"Tiempo promedio de {BUSQUEDAS} búsquedas por guía "
          "(microsegundos)\n")
    print(f"{'paquetes':>9} {'FP lista':>10} {'ED matriz':>10} "
          f"{'ED árbol':>9} {'altura':>7}")
    resultados = []
    for n in TAMANOS:
        unidad, lista_fp, guias = armar_datos(n)
        buscadas = random.choices(guias, k=BUSQUEDAS)
        fp = medir(lambda g: buscar_fp(lista_fp, g), buscadas)
        matriz = medir(unidad.buscar_pendiente_lineal, buscadas)
        arbol = medir(unidad.buscar_pendiente, buscadas)
        altura = unidad.guias.altura()
        resultados.append((n, fp, matriz, arbol))
        print(f"{n:>9} {fp:>10.1f} {matriz:>10.1f} {arbol:>9.1f} "
              f"{altura:>7}")
    return resultados


def graficar(resultados):
    import matplotlib.pyplot as plt
    tamanos = [r[0] for r in resultados]
    plt.plot(tamanos, [r[1] for r in resultados], "o-", label="FP: lista")
    plt.plot(tamanos, [r[2] for r in resultados], "s-", label="ED: matriz")
    plt.plot(tamanos, [r[3] for r in resultados], "^-", label="ED: árbol")
    plt.xlabel("Paquetes pendientes")
    plt.ylabel("Microsegundos por búsqueda")
    plt.yscale("log")
    plt.legend()
    plt.title("Búsqueda por número de guía")
    plt.savefig("experimento.png", dpi=150, bbox_inches="tight")
    print("\nGráfica guardada en experimento.png")


if __name__ == "__main__":
    resultados = experimento()
    graficar(resultados)
