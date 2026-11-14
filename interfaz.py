import tkinter as tk
from tkinter import ttk, messagebox

from archivos import cargar_todo, guardar_todo
from excepciones import ErrorPorteria
from paquetes import Sobre, Caja, Perecedero, Voluminoso
from recepcion import CamionVacio

CARPETA_DATOS = "datos"
ERRORES = (ErrorPorteria, CamionVacio)

class InterfazRecepcion:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Recepción de Paquetes")
        self.ventana.geometry("1150x760")
        self.ventana.minsize(900, 600)

        self.unidad, _ = cargar_todo(CARPETA_DATOS)

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
            text="RECEPCIÓN Y ENTREGA DE PAQUETES",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=15)

        ttk.Label(
            self.ventana,
            text=f"{self.unidad.nombre}: "
                 f"{self.unidad.total_apartamentos()} apartamentos"
        ).pack(pady=(0, 10))

        formulario = ttk.LabelFrame(
            self.ventana,
            text="Paquete y apartamento",
            padding=12
        )
        formulario.pack(fill="x", padx=20, pady=5)

        ttk.Label(
            formulario, text="Número de guía:"
        ).grid(row=0, column=0, padx=5, pady=7, sticky="w")

        self.entrada_guia = ttk.Entry(formulario, width=23)
        self.entrada_guia.grid(row=0, column=1, padx=5, pady=7)

        ttk.Label(
            formulario, text="Transportadora:"
        ).grid(row=0, column=2, padx=5, pady=7, sticky="w")

        self.entrada_transportadora = ttk.Entry(formulario, width=23)
        self.entrada_transportadora.grid(
            row=0, column=3, padx=5, pady=7
        )

        ttk.Label(
            formulario, text="Tipo de paquete:"
        ).grid(row=0, column=4, padx=5, pady=7, sticky="w")

        self.tipo = ttk.Combobox(
            formulario,
            values=list(self.tipos.keys()),
            state="readonly",
            width=20
        )
        self.tipo.grid(row=0, column=5, padx=5, pady=7)
        self.tipo.set("Sobre")

        ttk.Label(
            formulario, text="Bloque:"
        ).grid(row=1, column=0, padx=5, pady=7, sticky="w")

        self.entrada_bloque = ttk.Entry(formulario, width=23)
        self.entrada_bloque.grid(row=1, column=1, padx=5, pady=7)

        ttk.Label(
            formulario, text="Apartamento:"
        ).grid(row=1, column=2, padx=5, pady=7, sticky="w")

        self.entrada_apto = ttk.Entry(formulario, width=23)
        self.entrada_apto.grid(row=1, column=3, padx=5, pady=7)

        ttk.Label(
            formulario, text="Documento:"
        ).grid(row=1, column=4, padx=5, pady=7, sticky="w")

        self.entrada_documento = ttk.Entry(formulario, width=23)
        self.entrada_documento.grid(row=1, column=5, padx=5, pady=7)

        ttk.Button(
            formulario,
            text="Bajar al camión",
            command=self.bajar_al_camion
        ).grid(row=2, column=1, padx=5, pady=7)

        ttk.Button(
            formulario,
            text="Buscar por guía",
            command=self.buscar
        ).grid(row=2, column=3, padx=5, pady=7)

        marco_tabla = ttk.LabelFrame(
            self.ventana,
            text="Paquetes pendientes en portería",
            padding=10
        )
        marco_tabla.pack(
            fill="both", expand=True, padx=20, pady=10
        )

        columnas = (
            "guia",
            "destino",
            "transportadora",
            "tipo",
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
            "destino": "Bloque-Apto",
            "transportadora": "Transportadora",
            "tipo": "Tipo",
            "dias": "Días en portería",
            "limite": "Máximo de días",
            "vencimiento": "Vencimiento",
            "ubicacion": "Ubicación"
        }

        anchos = {
            "guia": 100,
            "destino": 100,
            "transportadora": 120,
            "tipo": 100,
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

        self.tabla.tag_configure("vencido", background="#FFDADA")
        self.tabla.tag_configure("en_plazo", background="#DDF5E5")

        marco_cola = ttk.LabelFrame(
            self.ventana,
            text="Camión (cola de llegada)",
            padding=10
        )
        marco_cola.pack(fill="x", padx=20, pady=5)

        ttk.Button(
            marco_cola,
            text="Ver frente de la cola",
            command=self.ver_frente
        ).pack(side="left", padx=5)

        ttk.Button(
            marco_cola,
            text="Asignar al apartamento",
            command=self.asignar
        ).pack(side="left", padx=5)

        ttk.Button(
            marco_cola,
            text="Rechazar paquete",
            command=self.rechazar
        ).pack(side="left", padx=5)

        self.info_cola = ttk.Label(
            marco_cola,
            text="Paquetes en el camión: 0 | Camión vacío"
        )
        self.info_cola.pack(side="left", padx=15)

        entregas = ttk.LabelFrame(
            self.ventana,
            text="Entregas",
            padding=10
        )
        entregas.pack(fill="x", padx=20, pady=(5, 15))

        ttk.Button(
            entregas,
            text="Entregar todo al residente",
            command=self.entregar_todo
        ).pack(side="left", padx=5)

        ttk.Button(
            entregas,
            text="Entregar seleccionado",
            command=self.entregar_seleccionado
        ).pack(side="left", padx=5)

        ttk.Button(
            entregas,
            text="Deshacer última entrega",
            command=self.deshacer
        ).pack(side="left", padx=5)

        ttk.Button(
            entregas,
            text="Ver historial",
            command=self.ver_historial
        ).pack(side="left", padx=5)

        ttk.Button(
            entregas,
            text="Guardar cambios",
            command=self.guardar
        ).pack(side="left", padx=5)

    def bajar_al_camion(self):

        guia = self.entrada_guia.get().strip().upper()
        transportadora = self.entrada_transportadora.get().strip()
        tipo = self.tipo.get()

        if not guia or not transportadora or not tipo:
            messagebox.showwarning(
                "Datos incompletos",
                "Escribe la guía, la transportadora y el tipo."
            )
            return

        if self.unidad.buscar_pendiente(guia) is not None:
            messagebox.showerror(
                "Guía duplicada",
                "Ya existe un paquete pendiente con esa guía."
            )
            return

        paquete = self.tipos[tipo](guia, transportadora)
        self.unidad.descargar_camion(paquete)

        self.entrada_guia.delete(0, tk.END)
        self.entrada_transportadora.delete(0, tk.END)

        self.actualizar_cola()

        messagebox.showinfo(
            "Camión",
            f"El paquete {guia} entró a la cola del camión."
        )

    def ver_frente(self):

        try:
            paquete = self.unidad.siguiente_del_camion()
        except ERRORES as error:
            messagebox.showwarning("Camión vacío", str(error))
            return

        messagebox.showinfo(
            "Frente de la cola",
            f"Guía: {paquete.guia}\n"
            f"Tipo: {paquete.tipo()}\n"
            f"Transportadora: {paquete.transportadora}"
        )

    def asignar(self):

        bloque = self.entrada_bloque.get().strip()
        numero = self.entrada_apto.get().strip()

        if not bloque or not numero.isdigit():
            messagebox.showwarning(
                "Datos incompletos",
                "Escribe el bloque y el número del apartamento."
            )
            return

        try:
            paquete = self.unidad.siguiente_del_camion()
            destino = self.unidad.registrar_del_camion(bloque, numero)
        except ERRORES as error:
            messagebox.showerror("No se pudo asignar", str(error))
            return

        self.actualizar_tabla()

        messagebox.showinfo(
            "Paquete asignado",
            f"La guía {paquete.guia} quedó en el {destino}."
        )

    def rechazar(self):

        try:
            paquete = self.unidad.rechazar_del_camion()
        except ERRORES as error:
            messagebox.showwarning("No se puede rechazar", str(error))
            return

        self.actualizar_cola()

        messagebox.showinfo(
            "Paquete rechazado",
            f"La guía {paquete.guia} salió del camión sin registrarse."
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

        paquete = self.unidad.buscar_pendiente(guia)

        if paquete is None:
            messagebox.showinfo(
                "Resultado",
                f"No se encontró la guía {guia} entre los pendientes."
            )
            return

        vencido = "Sí" if paquete.esta_vencido() else "No"

        messagebox.showinfo(
            "Información del paquete",
            f"Guía: {paquete.guia}\n"
            f"Destino: {paquete.destino}\n"
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

    def entregar_todo(self):

        bloque = self.entrada_bloque.get().strip()
        numero = self.entrada_apto.get().strip()
        documento = self.entrada_documento.get().strip()

        try:
            entregados = self.unidad.entregar(bloque, numero, documento)
        except (ErrorPorteria, ValueError) as error:
            messagebox.showerror("No se pudo entregar", str(error))
            return

        self.actualizar_tabla()

        messagebox.showinfo(
            "Entrega exitosa",
            f"Se entregaron {entregados.cantidad()} paquetes:\n"
            f"{entregados}"
        )

    def entregar_seleccionado(self):

        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selección requerida",
                "Selecciona un paquete de la tabla."
            )
            return

        documento = self.entrada_documento.get().strip()

        if not documento:
            messagebox.showwarning(
                "Datos incompletos",
                "Escribe el documento de quien recibe."
            )
            return

        guia = seleccion[0]
        paquete = self.unidad.buscar_pendiente(guia)

        if paquete is None:
            messagebox.showerror(
                "Error",
                "El paquete ya no está pendiente."
            )
            return

        destino = paquete.destino

        try:
            entregado = self.unidad.entregar_guia(
                destino.bloque.nombre, destino.numero, guia, documento
            )
        except (ErrorPorteria, ValueError) as error:
            messagebox.showerror("No se pudo entregar", str(error))
            return

        self.actualizar_tabla()

        messagebox.showinfo(
            "Entrega exitosa",
            f"La guía {entregado.guia} fue entregada a "
            f"{entregado.recibido_por}."
        )

    def deshacer(self):

        try:
            paquete = self.unidad.deshacer_entrega()
        except ErrorPorteria as error:
            messagebox.showwarning("Deshacer", str(error))
            return

        self.actualizar_tabla()

        messagebox.showinfo(
            "Entrega deshecha",
            f"La guía {paquete.guia} volvió a pendientes del "
            f"{paquete.destino}."
        )

    def ver_historial(self):

        historial = self.unidad.historial

        if historial.esta_vacia():
            messagebox.showinfo("Historial", "Aún no hay entregas.")
            return

        messagebox.showinfo(
            "Últimas entregas",
            f"Total de entregas: {historial.cantidad()}\n\n"
            f"{historial.recientes(10)}"
        )

    def guardar(self):

        confirmar = messagebox.askyesno(
            "Guardar cambios",
            f"Esto reescribe los archivos de la carpeta "
            f"'{CARPETA_DATOS}'. ¿Continuar?"
        )

        if not confirmar:
            return

        try:
            guardar_todo(
                self.unidad, CARPETA_DATOS, self.unidad.historial
            )
        except OSError as error:
            messagebox.showerror("No se pudo guardar", str(error))
            return

        messagebox.showinfo("Guardado", "Los cambios quedaron guardados.")

    def actualizar_tabla(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        bloques = self.unidad.bloques

        for i in range(bloques.cantidad()):
            bloque = bloques.obtener(i)
            for fila in range(bloque.pisos):
                for columna in range(bloque.aptos_por_piso):
                    apto = bloque.apartamento_en(fila, columna)
                    actual = apto.pendientes.cabeza
                    while actual is not None:
                        self.agregar_fila(actual.dato)
                        actual = actual.siguiente

        self.actualizar_cola()

    def agregar_fila(self, paquete):

        vencido = paquete.esta_vencido()
        etiqueta = "vencido" if vencido else "en_plazo"
        destino = paquete.destino

        self.tabla.insert(
            "",
            tk.END,
            iid=paquete.guia,
            values=(
                paquete.guia,
                f"{destino.bloque.nombre}-{destino.numero}",
                paquete.transportadora,
                paquete.tipo(),
                paquete.dias_en_porteria(),
                paquete.dias_maximos(),
                "Vencido" if vencido else "En plazo",
                paquete.ubicacion()
            ),
            tags=(etiqueta,)
        )

    def actualizar_cola(self):

        cantidad = self.unidad.camion.cantidad()

        if cantidad == 0:
            texto = "Paquetes en el camión: 0 | Camión vacío"
        else:
            frente = self.unidad.siguiente_del_camion()
            texto = (
                f"Paquetes en el camión: {cantidad} | "
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