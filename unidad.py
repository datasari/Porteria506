from arreglo import Arreglo
from recepcion import ListaPaquetes, Cola
from excepciones import (ErrorPorteria, ApartamentoInexistente,
                         BloqueInexistente, GuiaDuplicada, SinPendientes,
                         ResidenteNoAutorizado, ResidenteDuplicado)

MAX_RESIDENTES = 8


class Residente:
    def __init__(self, documento, nombre, telefono=""):
        documento = str(documento).strip()
        if not documento.isdigit():
            raise ErrorPorteria(f"Documento no numérico: {documento}")
        self.__documento = documento
        self.__nombre = str(nombre).strip()
        self.__telefono = str(telefono).strip()

    @property
    def documento(self):
        return self.__documento

    @property
    def nombre(self):
        return self.__nombre

    @property
    def telefono(self):
        return self.__telefono

    def __str__(self):
        return f"{self.__nombre} (CC {self.__documento})"


class ArregloResidentes(Arreglo):
    def validar_tipo(self, dato):
        return isinstance(dato, Residente)

    def buscar(self, documento):
        for i in range(self.cantidad()):
            residente = self.obtener(i)
            if residente.documento == str(documento).strip():
                return residente
        return None


class Apartamento:
    def __init__(self, numero, bloque):
        self.__numero = numero
        self.__bloque = bloque
        self.__residentes = ArregloResidentes(MAX_RESIDENTES)
        self.__pendientes = ListaPaquetes()

    @property
    def numero(self):
        return self.__numero

    @property
    def bloque(self):
        return self.__bloque

    @property
    def residentes(self):
        return self.__residentes

    @property
    def pendientes(self):
        return self.__pendientes

    def agregar_residente(self, residente):
        if self.__residentes.buscar(residente.documento) is not None:
            raise ResidenteDuplicado(residente.documento)
        self.__residentes.agregar(residente)

    def esta_autorizado(self, documento):
        return self.__residentes.buscar(documento) is not None

    def recibir(self, paquete):
        paquete.asignar_destino(self)
        self.__pendientes.agregar(paquete)

    def tiene_pendientes(self):
        return not self.__pendientes.esta_vacia()

    def __autorizado(self, documento):
        residente = self.__residentes.buscar(documento)
        if residente is None:
            raise ResidenteNoAutorizado(documento, self)
        return residente

    def entregar(self, guia, documento, momento=None):
        residente = self.__autorizado(documento)
        paquete = self.__pendientes.quitar(str(guia).strip().upper())
        paquete.marcar_entregado(residente.nombre, momento)
        return paquete

    def entregar_todos(self, documento, momento=None):
        residente = self.__autorizado(documento)
        if not self.tiene_pendientes():
            raise SinPendientes(f"el {self} no tiene paquetes")
        entregados = ListaPaquetes()
        while self.tiene_pendientes():
            paquete = self.__pendientes.quitar_primero()
            paquete.marcar_entregado(residente.nombre, momento)
            entregados.agregar(paquete)
        return entregados

    def __str__(self):
        bloque = self.__bloque.nombre
        return f"bloque {bloque}, apartamento {self.__numero}"


class ArregloApartamentos(Arreglo):
    def validar_tipo(self, dato):
        return isinstance(dato, Apartamento)


class ArregloPisos(Arreglo):
    def validar_tipo(self, dato):
        return isinstance(dato, ArregloApartamentos)


class Bloque:
    def __init__(self, nombre, pisos, aptos_por_piso):
        if pisos < 1 or not (1 <= aptos_por_piso <= 99):
            tamano = f"{pisos} x {aptos_por_piso}"
            raise ErrorPorteria(f"Bloque {nombre} inválido: {tamano}")
        self.__nombre = str(nombre).strip()
        self.__pisos = pisos
        self.__aptos_por_piso = aptos_por_piso
        self.__apartamentos = ArregloPisos(pisos)
        for piso in range(1, pisos + 1):
            fila = ArregloApartamentos(aptos_por_piso)
            for posicion in range(1, aptos_por_piso + 1):
                fila.agregar(Apartamento(piso * 100 + posicion, self))
            self.__apartamentos.agregar(fila)

    @property
    def nombre(self):
        return self.__nombre

    @property
    def pisos(self):
        return self.__pisos

    @property
    def aptos_por_piso(self):
        return self.__aptos_por_piso

    def total_apartamentos(self):
        return self.__pisos * self.__aptos_por_piso

    def obtener_apartamento(self, numero):
        piso, posicion = divmod(numero, 100)
        piso_ok = 1 <= piso <= self.__pisos
        posicion_ok = 1 <= posicion <= self.__aptos_por_piso
        if not (piso_ok and posicion_ok):
            raise ApartamentoInexistente(self.__nombre, numero)
        fila = self.__apartamentos.obtener(piso - 1)
        return fila.obtener(posicion - 1)

    def apartamento_en(self, fila, columna):
        return self.__apartamentos.obtener(fila).obtener(columna)

    def contar_pendientes(self):
        total = 0
        for fila in range(self.__pisos):
            for columna in range(self.__aptos_por_piso):
                apto = self.apartamento_en(fila, columna)
                total += apto.pendientes.cantidad()
        return total


class ArregloBloques(Arreglo):
    def validar_tipo(self, dato):
        return isinstance(dato, Bloque)

    def buscar(self, nombre):
        for i in range(self.cantidad()):
            bloque = self.obtener(i)
            if bloque.nombre == str(nombre).strip():
                return bloque
        return None


class Unidad:
    def __init__(self, nombre, cantidad_bloques=3):
        self.__nombre = nombre
        self.__bloques = ArregloBloques(cantidad_bloques)
        self.__camion = Cola()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def bloques(self):
        return self.__bloques

    @property
    def camion(self):
        return self.__camion

    def agregar_bloque(self, nombre, pisos, aptos_por_piso):
        if self.__bloques.buscar(nombre) is not None:
            raise ErrorPorteria(f"El bloque {nombre} ya existe")
        bloque = Bloque(nombre, pisos, aptos_por_piso)
        self.__bloques.agregar(bloque)
        return bloque

    def bloque(self, nombre):
        bloque = self.__bloques.buscar(nombre)
        if bloque is None:
            raise BloqueInexistente(nombre)
        return bloque

    def apartamento(self, bloque, numero):
        return self.bloque(bloque).obtener_apartamento(int(numero))

    def total_apartamentos(self):
        total = 0
        for i in range(self.__bloques.cantidad()):
            total += self.__bloques.obtener(i).total_apartamentos()
        return total

    def total_pendientes(self):
        total = 0
        for i in range(self.__bloques.cantidad()):
            total += self.__bloques.obtener(i).contar_pendientes()
        return total

    def buscar_pendiente(self, guia):
        guia = str(guia).strip().upper()
        for i in range(self.__bloques.cantidad()):
            bloque = self.__bloques.obtener(i)
            for fila in range(bloque.pisos):
                for columna in range(bloque.aptos_por_piso):
                    apto = bloque.apartamento_en(fila, columna)
                    paquete = apto.pendientes.buscar(guia)
                    if paquete is not None:
                        return paquete
        return None
    def entregar(self, bloque, numero, documento, momento=None):
        apto = self.apartamento(bloque, numero)
        return apto.entregar_todos(documento, momento)

    def entregar_guia(self, bloque, numero, guia, documento,
                      momento=None):
        apto = self.apartamento(bloque, numero)
        return apto.entregar(guia, documento, momento)

    def rechazar_del_camion(self):
        return self.__camion.desencolar()
        return apto.entregar(guia, documento, momento)
        apartamento = self.registrar_llegada(bloque, numero, paquete)
        self.__camion.desencolar()

    def registrar_del_camion(self, bloque, numero):
        paquete = self.__camion.ver_frente()

    def siguiente_del_camion(self):
        return self.__camion.ver_frente()

    def descargar_camion(self, paquete):
        self.__camion.encolar(paquete)