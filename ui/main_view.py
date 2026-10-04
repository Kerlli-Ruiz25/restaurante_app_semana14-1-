import tkinter as tk
from tkinter import ttk, messagebox

class MainView:
    def __init__(self, root, servicio, usuario):
        self.root = root
        self.servicio = servicio
        self.usuario = usuario

        self.root.title("Restaurante App - Gestión")
        self.root.geometry("1000x650")
        self.root.minsize(900, 600)

        self._crear_variables()
        self._crear_interfaz()
        self.mostrar_productos()

    def _crear_variables(self):
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.categoria_var = tk.StringVar()

    def _crear_interfaz(self):
        # Contenedor principal
        principal = ttk.Frame(self.root, padding=15)
        principal.pack(fill="both", expand=True)

        # Encabezado
        encabezado = ttk.Frame(principal)
        encabezado.pack(fill="x", pady=(0, 12))

        ttk.Label(encabezado, text="RESTAURANTE APP",
                  font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Label(encabezado, text=f"Usuario: {self.usuario.nombre or self.usuario.usuario}",
                  font=("Segoe UI", 10)).pack(side="right", pady=8)

        # Navegación
        navegacion = ttk.LabelFrame(principal, text="Navegación", padding=8)
        navegacion.pack(fill="x", pady=(0, 12))

        ttk.Button(navegacion, text="Usuarios",
                   command=self.mostrar_usuarios).pack(side="left", padx=5)
        ttk.Button(navegacion, text="Productos",
                   command=self.mostrar_productos).pack(side="left", padx=5)
        ttk.Button(navegacion, text="Limpiar formulario",
                   command=self.limpiar_formulario).pack(side="left", padx=5)
        ttk.Button(navegacion, text="Salir",
                   command=self.root.destroy).pack(side="right", padx=5)

        # Área de contenido
        self.contenido = ttk.Frame(principal)
        self.contenido.pack(fill="both", expand=True)

        self._crear_productos()

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def _crear_productos(self):
        self._limpiar_contenido()

        izquierda = ttk.Frame(self.contenido)
        izquierda.pack(side="left", fill="y", padx=(0, 12))

        derecha = ttk.Frame(self.contenido)
        derecha.pack(side="right", fill="both", expand=True)

        formulario = ttk.LabelFrame(izquierda, text="Formulario de producto", padding=15)
        formulario.pack(fill="x")

        campos = [
            ("ID:", self.id_var),
            ("Nombre:", self.nombre_var),
            ("Precio:", self.precio_var),
            ("Categoría:", self.categoria_var)
        ]

        for fila, (texto, variable) in enumerate(campos):
            ttk.Label(formulario, text=texto).grid(
                row=fila, column=0, sticky="w", pady=7
            )
            ttk.Entry(formulario, textvariable=variable, width=27).grid(
                row=fila, column=1, sticky="ew", padx=(8, 0), pady=7
            )

        formulario.columnconfigure(1, weight=1)

        acciones = ttk.LabelFrame(izquierda, text="Acciones", padding=12)
        acciones.pack(fill="x", pady=12)

        ttk.Button(acciones, text="Registrar",
                   command=self.registrar).pack(fill="x", pady=4)
        ttk.Button(acciones, text="Cargar / Consultar",
                   command=self.cargar).pack(fill="x", pady=4)
        ttk.Button(acciones, text="Actualizar",
                   command=self.actualizar).pack(fill="x", pady=4)
        ttk.Button(acciones, text="Eliminar",
                   command=self.eliminar).pack(fill="x", pady=4)

        listado = ttk.LabelFrame(derecha, text="Productos registrados", padding=10)
        listado.pack(fill="both", expand=True)

        tabla_frame = ttk.Frame(listado)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "precio", "categoria")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas,
                                  show="headings", height=16)

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("categoria", text="Categoría")

        self.tabla.column("id", width=90, anchor="center")
        self.tabla.column("nombre", width=230)
        self.tabla.column("precio", width=100, anchor="e")
        self.tabla.column("categoria", width=150)

        scroll = ttk.Scrollbar(tabla_frame, orient="vertical",
                               command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        ttk.Label(listado, text="Seleccione un producto para cargar sus datos.",
                  foreground="#555").pack(anchor="w", pady=(8, 0))

    def mostrar_productos(self):
        self._crear_productos()
        self._llenar_tabla()

    def _llenar_tabla(self):
        if not hasattr(self, "tabla"):
            return
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for producto in self.servicio.listar_productos():
            self.tabla.insert(
                "", "end",
                values=(producto.id, producto.nombre,
                        f"{producto.precio:.2f}", producto.categoria)
            )

    def _datos_formulario(self):
        return (
            self.id_var.get(),
            self.nombre_var.get(),
            self.precio_var.get(),
            self.categoria_var.get()
        )

    def registrar(self):
        resultado, mensaje = self.servicio.registrar_producto(*self._datos_formulario())
        if resultado:
            messagebox.showinfo("Registro", mensaje)
            self.mostrar_productos()
            self.limpiar_formulario()
        else:
            messagebox.showerror("No se pudo registrar", mensaje)

    def cargar(self):
        producto_id = self.id_var.get().strip()
        if not producto_id:
            seleccionado = self.tabla.selection()
            if seleccionado:
                valores = self.tabla.item(seleccionado[0], "values")
                producto_id = valores[0]
                self.id_var.set(producto_id)

        if not producto_id:
            messagebox.showwarning("Consulta", "Ingrese o seleccione un ID.")
            return

        producto = self.servicio.buscar_producto(producto_id)
        if not producto:
            messagebox.showerror("Consulta", "Producto no encontrado.")
            return

        self.nombre_var.set(producto.nombre)
        self.precio_var.set(f"{producto.precio:.2f}")
        self.categoria_var.set(producto.categoria)

    def actualizar(self):
        resultado, mensaje = self.servicio.actualizar_producto(*self._datos_formulario())
        if resultado:
            messagebox.showinfo("Actualización", mensaje)
            self.mostrar_productos()
        else:
            messagebox.showerror("No se pudo actualizar", mensaje)

    def eliminar(self):
        producto_id = self.id_var.get().strip()
        if not producto_id:
            seleccionado = self.tabla.selection()
            if seleccionado:
                producto_id = self.tabla.item(seleccionado[0], "values")[0]
                self.id_var.set(producto_id)

        if not producto_id:
            messagebox.showwarning("Eliminación", "Ingrese o seleccione un ID.")
            return

        producto = self.servicio.buscar_producto(producto_id)
        if not producto:
            messagebox.showerror("Eliminación", "Producto no encontrado.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar el producto '{producto.nombre}'?"
        )
        if not confirmar:
            return

        resultado, mensaje = self.servicio.eliminar_producto(producto_id)
        if resultado:
            messagebox.showinfo("Eliminación", mensaje)
            self.mostrar_productos()
            self.limpiar_formulario()
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    def mostrar_usuarios(self):
        self._limpiar_contenido()

        marco = ttk.LabelFrame(self.contenido, text="Usuarios registrados", padding=15)
        marco.pack(fill="both", expand=True)

        columnas = ("usuario", "nombre")
        tabla = ttk.Treeview(marco, columns=columnas,
                             show="headings", height=15)
        tabla.heading("usuario", text="Usuario")
        tabla.heading("nombre", text="Nombre")
        tabla.column("usuario", width=200)
        tabla.column("nombre", width=300)

        for usuario in self.servicio.listar_usuarios():
            tabla.insert("", "end", values=(usuario.usuario, usuario.nombre))

        tabla.pack(fill="both", expand=True)

        ttk.Button(self.contenido, text="Volver a Productos",
                   command=self.mostrar_productos).pack(pady=10)

    def limpiar_formulario(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.precio_var.set("")
        self.categoria_var.set("")
