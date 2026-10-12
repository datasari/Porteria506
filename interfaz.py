import tkinter as tk
from tkinter import ttk, messagebox

from paquetes import Sobre, Caja, Perecedero, Voluminoso
from recepcion import ListaPaquetes, Cola, SinPendientes, CamionVacio


class InterfazRecepcion:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Recepción de Paquetes")
        self.ventana.geometry("1150x680")
        self.ventana.minsize(900, 550)

        self.lista = ListaPaquetes()
        self.camion = Cola()

        self.guias_camion = []

        self.tipos = {
            "Sobre": Sobre,
            "Caja": Caja,
            "Perecedero": Perecedero,
            "Voluminoso": Voluminoso
        }

        self.crear_interfaz()
        self.actualizar_reloj()

    def crear_interfaz(self):

        titulo = ttk.Label(
            self.ventana,
            text="RECEPCIÓN Y DESPACHO DE PAQUETES",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=15)

        ttk.Label(
            self.ventana,
            text="Sistema de control de paquetes en portería"
        ).pack(pady=(0, 10))

        formulario = ttk.LabelFrame(
            self.ventana,
            text="Registrar paquete",
            padding=12
        )
        formulario.pack(fill="x", padx=20, pady=5)

        ttk.Label(
            formulario,
            text="Número de guía:"
        ).grid(row=0, column=0, padx=5, pady=7, sticky="w")

        self.entrada_guia = ttk.Entry(formulario, width=23)
        self.entrada_guia.grid(row=0, column=1, padx=5, pady=7)

        ttk.Label(
            formulario,
            text="Transportadora:"
        ).grid(row=0, column=2, padx=5, pady=7, sticky="w")

        self.entrada_transportadora = ttk.Entry(
            formulario, width=23
        )
        self.entrada_transportadora.grid(
            row=0, column=3, padx=5, pady=7
        )

        ttk.Label(
            formulario,
            text="Tipo de paquete:"
        ).grid(row=1, column=0, padx=5, pady=7, sticky="w")

        self.tipo = ttk.Combobox(
            formulario,
            values=list(self.tipos.keys()),
            state="readonly",
            width=20
        )
        self.tipo.grid(row=1, column=1, padx=5, pady=7)
        self.tipo.set("Sobre")

        ttk.Button(
            formulario,
            text="Registrar paquete",
            command=self.registrar
        ).grid(row=1, column=2, padx=5, pady=7)

        ttk.Button(
            formulario,
            text="Buscar paquete",
            command=self.buscar
        ).grid(row=1, column=3, padx=5, pady=7)

        marco_tabla = ttk.LabelFrame(
            self.ventana,
            text="Paquetes en recepción",
            padding=10
        )
        marco_tabla.pack(
            fill="both", expand=True, padx=20, pady=10
        )

        columnas = (
            "guia",
            "transportadora",
            "tipo",
            "estado",
            "dias",
            "limite",
            "vencimiento",
            "ubicacion"
        )

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings"
        )

        encabezados = {
            "guia": "Guía",
            "transportadora": "Transportadora",
            "tipo": "Tipo",
            "estado": "Estado",
            "dias": "Días en portería",
            "limite": "Máximo de días",
            "vencimiento": "Vencimiento",
            "ubicacion": "Ubicación"
        }

        anchos = {
            "guia": 100,
            "transportadora": 120,
            "tipo": 100,
            "estado": 125,
            "dias": 110,
            "limite": 105,
            "vencimiento": 100,
            "ubicacion": 200
        }

        for columna, texto in encabezados.items():
            self.tabla.heading(columna, text=texto)
            self.tabla.column(
                columna,
                width=anchos[columna],
                minwidth=70,
                anchor="center"
            )

        barra = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        barra_horizontal = ttk.Scrollbar(
            marco_tabla,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(
            yscrollcommand=barra.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabla.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        marco_tabla.rowconfigure(0, weight=1)
        marco_tabla.columnconfigure(0, weight=1)

        self.tabla.tag_configure(
            "vencido",
            background="#FFDADA"
        )

        self.tabla.tag_configure(
            "en_plazo",
            background="#DDF5E5"
        )

        self.tabla.tag_configure(
            "en_camion",
            background="#FFF0CC"
        )

        operaciones = ttk.LabelFrame(
            self.ventana,
            text="Operaciones",
            padding=10
        )
        operaciones.pack(fill="x", padx=20, pady=5)

        ttk.Button(
            operaciones,
            text="Agregar al camión",
            command=self.cargar_camion
        ).pack(side="left", padx=5)

        ttk.Button(
            operaciones,
            text="Ver frente de la cola",
            command=self.ver_frente
        ).pack(side="left", padx=5)

        ttk.Button(
            operaciones,
            text="Despachar paquete",
            command=self.despachar
        ).pack(side="left", padx=5)

        ttk.Button(
            operaciones,
            text="Actualizar tabla",
            command=self.actualizar_tabla
        ).pack(side="left", padx=5)

        marco_cola = ttk.LabelFrame(
            self.ventana,
            text="Estado del camión",
            padding=10
        )
        marco_cola.pack(fill="x", padx=20, pady=10)

        self.info_cola = ttk.Label(
            marco_cola,
            text="Paquetes en cola: 0 | Camión vacío"
        )
        self.info_cola.pack(anchor="w")

    def registrar(self):

        guia = self.entrada_guia.get().strip().upper()
        transportadora = (
            self.entrada_transportadora.get().strip()
        )
        tipo = self.tipo.get()

        if not guia or not transportadora or not tipo:
            messagebox.showwarning(
                "Datos incompletos",
                "Completa todos los campos."
            )
            return

        if self.lista.buscar(guia) is not None:
            messagebox.showerror(
                "Guía duplicada",
                "Ya existe un paquete con esa guía."
            )
            return

        paquete = self.tipos[tipo](guia, transportadora)

        self.lista.agregar(paquete)

        self.entrada_guia.delete(0, tk.END)
        self.entrada_transportadora.delete(0, tk.END)

        self.actualizar_tabla()

        messagebox.showinfo(
            "Registro exitoso",
            f"El paquete {guia} fue registrado."
        )

    def buscar(self):

        guia = self.entrada_guia.get().strip().upper()

        if not guia:
            seleccion = self.tabla.selection()

            if seleccion:
                guia = seleccion[0]
            else:
                messagebox.showwarning(
                    "Buscar paquete",
                    "Escribe una guía o selecciona un paquete."
                )
                return

        paquete = self.lista.buscar(guia)

        if paquete is None:
            messagebox.showinfo(
                "Resultado",
                f"No se encontró la guía {guia}."
            )
            return

        vencido = (
            "Sí" if paquete.esta_vencido() else "No"
        )

        messagebox.showinfo(
            "Información del paquete",
            f"Guía: {paquete.guia}\n"
            f"Transportadora: {paquete.transportadora}\n"
            f"Tipo: {paquete.tipo()}\n"
            f"Estado: {paquete.estado}\n"
            f"Días en portería: {paquete.dias_en_porteria()}\n"
            f"Máximo de días: {paquete.dias_maximos()}\n"
            f"¿Está vencido?: {vencido}\n"
            f"Ubicación: {paquete.ubicacion()}"
        )

        if self.tabla.exists(guia):
            self.tabla.selection_set(guia)
            self.tabla.focus(guia)
            self.tabla.see(guia)

    def cargar_camion(self):

        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selección requerida",
                "Selecciona un paquete de la tabla."
            )
            return

        guia = seleccion[0]
        paquete = self.lista.buscar(guia)

        if paquete is None:
            messagebox.showerror(
                "Error",
                "El paquete ya no está en recepción."
            )
            return

        if guia in self.guias_camion:
            messagebox.showwarning(
                "Paquete duplicado",
                "El paquete ya está en la cola del camión."
            )
            return

        if paquete.estado == "Entregado":
            messagebox.showwarning(
                "Paquete entregado",
                "No puedes cargar un paquete ya entregado."
            )
            return

        self.camion.encolar(paquete)
        self.guias_camion.append(guia)

        self.actualizar_tabla()
        self.actualizar_cola()

        messagebox.showinfo(
            "Camión",
            f"El paquete {guia} fue agregado a la cola."
        )

    def ver_frente(self):

        try:
            paquete = self.camion.ver_frente()

            messagebox.showinfo(
                "Frente de la cola",
                f"Guía: {paquete.guia}\n"
                f"Tipo: {paquete.tipo()}\n"
                f"Transportadora: {paquete.transportadora}\n"
                f"Días en portería: {paquete.dias_en_porteria()}"
            )

        except CamionVacio as error:
            messagebox.showwarning(
                "Camión vacío", str(error)
            )

    def despachar(self):

        try:
            paquete = self.camion.desencolar()

            self.lista.quitar(paquete.guia)
            self.guias_camion.remove(paquete.guia)

            self.actualizar_tabla()
            self.actualizar_cola()

            messagebox.showinfo(
                "Despacho exitoso",
                f"Se despachó el paquete {paquete.guia}.\n"
                f"Días que permaneció en portería: "
                f"{paquete.dias_en_porteria()}"
            )

        except CamionVacio as error:
            messagebox.showwarning(
                "No se puede despachar", str(error)
            )

        except SinPendientes as error:
            messagebox.showwarning(
                "Paquete no encontrado", str(error)
            )

    def actualizar_tabla(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        actual = self.lista.cabeza

        while actual is not None:

            paquete = actual.dato
            dias = paquete.dias_en_porteria()
            limite = paquete.dias_maximos()
            vencido = paquete.esta_vencido()

            if paquete.guia in self.guias_camion:
                estado = "En cola del camión"
                etiqueta = "en_camion"

            elif paquete.estado == "Entregado":
                estado = "Entregado"
                etiqueta = "en_plazo"

            elif vencido:
                estado = "Pendiente"
                etiqueta = "vencido"

            else:
                estado = "Pendiente"
                etiqueta = "en_plazo"

            texto_vencimiento = (
                "Vencido" if vencido else "En plazo"
            )

            self.tabla.insert(
                "",
                tk.END,
                iid=paquete.guia,
                values=(
                    paquete.guia,
                    paquete.transportadora,
                    paquete.tipo(),
                    estado,
                    dias,
                    limite,
                    texto_vencimiento,
                    paquete.ubicacion()
                ),
                tags=(etiqueta,)
            )

            actual = actual.siguiente

        self.actualizar_cola()

    def actualizar_cola(self):

        cantidad = self.camion.cantidad()

        if cantidad == 0:
            texto = "Paquetes en cola: 0 | Camión vacío"
        else:
            frente = self.camion.ver_frente()

            texto = (
                f"Paquetes en cola: {cantidad} | "
                f"Siguiente guía: {frente.guia}"
            )

        self.info_cola.config(text=texto)

    def actualizar_reloj(self):

        self.actualizar_tabla()

        self.ventana.after(60000, self.actualizar_reloj)

if __name__ == "__main__":

    ventana = tk.Tk()
    aplicacion = InterfazRecepcion(ventana)
    ventana.mainloop()