from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.productos_archivo = ArchivoServicio(base_dir / "datos" / "productos.json")
        self.usuarios_archivo = ArchivoServicio(base_dir / "datos" / "usuarios.json")

    # ---------------- Usuarios ----------------
    def autenticar(self, usuario, password):
        usuarios = [Usuario.from_dict(x) for x in self.usuarios_archivo.leer()]
        for u in usuarios:
            if u.usuario == usuario and u.password == password:
                return u
        return None

    def listar_usuarios(self):
        return [Usuario.from_dict(x) for x in self.usuarios_archivo.leer()]

    # ---------------- Productos ----------------
    def listar_productos(self):
        return [Producto.from_dict(x) for x in self.productos_archivo.leer()]

    def buscar_producto(self, producto_id):
        producto_id = str(producto_id).strip()
        for producto in self.listar_productos():
            if producto.id == producto_id:
                return producto
        return None

    def registrar_producto(self, producto_id, nombre, precio, categoria):
        producto_id = str(producto_id).strip()
        nombre = str(nombre).strip()
        categoria = str(categoria).strip()

        if not producto_id or not nombre or not categoria:
            return False, "Todos los campos son obligatorios."

        try:
            precio = float(precio)
        except (TypeError, ValueError):
            return False, "El precio debe ser numérico."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

        if self.buscar_producto(producto_id):
            return False, "Ya existe un producto con ese identificador."

        productos = self.listar_productos()
        productos.append(Producto(producto_id, nombre, precio, categoria))
        self.productos_archivo.guardar([p.to_dict() for p in productos])
        return True, "Producto registrado correctamente."

    def actualizar_producto(self, producto_id, nombre, precio, categoria):
        producto_id = str(producto_id).strip()
        nombre = str(nombre).strip()
        categoria = str(categoria).strip()

        if not producto_id or not nombre or not categoria:
            return False, "Todos los campos son obligatorios."

        try:
            precio = float(precio)
        except (TypeError, ValueError):
            return False, "El precio debe ser numérico."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

        productos = self.listar_productos()
        encontrado = False
        for producto in productos:
            if producto.id == producto_id:
                producto.nombre = nombre
                producto.precio = precio
                producto.categoria = categoria
                encontrado = True
                break

        if not encontrado:
            return False, "No se encontró el producto."

        self.productos_archivo.guardar([p.to_dict() for p in productos])
        return True, "Producto actualizado correctamente."

    def eliminar_producto(self, producto_id):
        producto_id = str(producto_id).strip()
        productos = self.listar_productos()
        nuevos = [p for p in productos if p.id != producto_id]

        if len(nuevos) == len(productos):
            return False, "No se encontró el producto."

        self.productos_archivo.guardar([p.to_dict() for p in nuevos])
        return True, "Producto eliminado correctamente."
