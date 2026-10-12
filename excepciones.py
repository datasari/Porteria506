class ErrorPorteria(Exception):
    pass

class ApartamentoInexistente(ErrorPorteria):
    def __init__(self,bloque,numero):
        super().__init__(f"El apartamento{numero} no existe en el bloque {bloque}")

class BloqueInexistente(ErrorPorteria):
    def __init__(self,bloque):
        super().__init__(f"El bloque {bloque} no existe")

class GuiaDuplicada(ErrorPorteria):
    def __init__(self,guia):
        super().__init__(f"La guia {guia} ya existe")

class SinPendientes(ErrorPorteria):
    def __init__(self, mensaje):
        super().__init__(mensaje)

class ResidenteNoAutorizado(ErrorPorteria):
     def __init__(self, documento, apartamento):
        super().__init__(f"El residente con documento {documento} no está autorizado para el apartamento {apartamento}")   

class ResidenteDuplicado(ErrorPorteria):
     def __init__(self, documento):
        super().__init__(f"El residente con documento {documento} ya existe")

class ArregloLleno(ErrorPorteria):
    def __init__(self,capacidad):
        super().__init__(f"El arreglo está lleno, la capacidad máxima es {capacidad}")

class PosicionInvalida(ErrorPorteria):
    def __init__(self,posicion):
        super().__init__(f"La posición {posicion} es inválida")

class TipoInvalido(ErrorPorteria):
    def __init__(self, dato):
        super().__init__(f"El dato de tipo {type(dato).__name__} es inválido")

class CamionVacio(ErrorPorteria):
    def __init__(self):
        super().__init__("El camión está vacío, no hay guías para entregar")  

class ArchivoInexistente(ErrorPorteria):
    def __init__ (self, ruta):
        super().__init__(f"El archivo no fue encontrado en la ruta {ruta}")

class ArchivoDanado(ErrorPorteria):
    def __init__(self, ruta,numero_linea):
        super().__init__(f"Error de formato en el archivo {ruta} en la línea {numero_linea}")                         