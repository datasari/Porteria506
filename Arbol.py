class NodoArbol:
 def __init__(self, paquete):
  self.__paquete= paquete
  self.__izquierdo= None
  self.__derecho= None

 @property
 def paquete(self):
  return self.__paquete 
 
 @paquete.setter
 def paquete(self,paquete):
    self.__paquete = paquete

 @property
 def izquierdo(self):
  return self.__izquierdo
 
 @izquierdo.setter
 def izquierdo(self,nodo):
  self.__izquierdo = nodo

 @property
 def derecho(self):
    return self.__derecho
 @derecho.setter
 def derecho(self,nodo):
  self.__derecho = nodo 


class ArbolGuias:
  def __init__(self):
    self.__raiz = None
    self.__tamano = 0

  def esta_vacio(self):
    return self.__raiz is None
  
  def cantidad(self):
    return self.__tamano    

  def insertar(self,paquete):
    nuevo=NodoArbol(paquete)
    if self.esta_vacio():
      self.__raiz=nuevo
      self.__tamano +=1
      return
    actual=self.__raiz
    while True:
      if paquete.guia == actual.paquete.guia:
        actual.paquete = paquete
        return
      if paquete.guia < actual.paquete.guia:
        if actual.izquierdo is None:
          actual.izquierdo=nuevo
          break
        actual=actual.izquierdo
      else:
        if actual.derecho is None:
          actual.derecho=nuevo
          break
        actual=actual.derecho
    self.__tamano +=1   

  def buscar (self,guia):
    actual = self.__raiz
    while actual is not None:
      if guia == actual.paquete.guia:
        return actual.paquete
      if guia < actual.paquete.guia:
        actual = actual.izquierdo
      else:
        actual = actual.derecho
    return None

  def altura(self):
      return self.__altura(self.__raiz)

  def __altura(self,nodo):
      if nodo is None:
          return 0
      izquierda = self.__altura(nodo.izquierdo)
      derecha = self.__altura(nodo.derecho)
      return 1+max(izquierda,derecha)
  def en_orden(self):
    return self.__en_orden(self.__raiz).strip()

  def __en_orden(self,nodo):
    if nodo is None:
      return ""
    izquierda=self.__en_orden(nodo.izquierdo)
    derecha=self.__en_orden(nodo.derecho)
    return izquierda+ nodo.paquete.guia + " " + derecha 

