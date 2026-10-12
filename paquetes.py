from abc import ABC, abstractmethod
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

class ErrorPorteria(Exception):
    pass

class ApartamenteInexistente(ErrorPorteria):
    def __init__(self, bloque, numero):
        super().__init__(f"El apartamento {numero} "
                         f"no existe en el bloque {bloque}")

class Paquete(ABC):
    def __init__(self, guia, transportadora, llegada=None):
        guia = str(guia).strip().upper()
        if not guia:
            raise ErrorPorteria("La guia no puede estar vacía")
        self.__guia = guia
        self.__transportadora = str(transportadora). strip()
        self.__llegada = llegada or datetime.now()
        self.__estado = "Pendiente"
        self.__entregado_en = None
        self.__recibido_por = None
        self.__destino = None

    @property
    def guia(self):
        return self.__guia

    @property
    def transportadora(self):
        return self.__transportadora

    @property
    def llegada(self):
        return self.__llegada

    @property
    def estado(self):
        return self.__estado

    @property
    def entrega_en(self):
        return self.__entregado_en

    @property
    def recibido_por(self):
        return self.__recibido_por

    def asignar_destino(self, apartamento):
        self.__destino = apartamento

    def marcar_entregado(self, recibido_por, momento = None):
        if self.__estado == "Entregado":
            raise ErrorPorteria(f"Guía {self.__guia} ya entregada")
        self.__estado = "Entregado"
        self.__entregado_en = momento or datetime.now()
        self.__recibido_por = recibido_por

    def devolver_a_pendiente(self):
        self.__estado = "Pendiente"
        self.__entregado_en = None
        self.__recibido_por = None

    def dias_en_porteria(self, ahora = None):
        fin = self.__entregado_en or ahora or datetime.now()
        return (fin - self.__llegada).days

    def esta_vencido(self, ahora = None):
        return self.dias_en_porteria(ahora) > self.dias_maximos()

    def tipo(self):
        return type(self).__name__

    @abstractmethod
    def dias_maximos(self):
        pass

    @abstractmethod
    def ubicacion(self):
        pass

    def a_fila(self): 
        bloque, numero = "", ""
        if self.__destino is not None:
            bloque = self.__destino.bloque.nombre
            numero = self.__destino.numero
        entregado = ""
        if self.__entregado_en is not None:
            entregado = self.__entregado_en.strftime(FORMATO_FECHA)
        llegada = self.__llegada.strftime(FORMATO_FECHA)
        recibio = self.__recibido_por or ""
        return (f"{self.tipo()},{self.__guia},{self.__transportadora},"
                f"{bloque},{numero},{llegada},{self.__estado},"
                f"{entregado},{recibio}")

    def __str__(self):
        return (f"{self.tipo()} {self.__guia} ({self.__transportadora})"
                f" -> {self.ubicacion()}")