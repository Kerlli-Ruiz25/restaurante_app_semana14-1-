# restaurante_app - Semana 14

## Tema
**Componentes y contenedores con Tkinter/ttk**

## Propósito
Esta versión corresponde a la evolución del proyecto `restaurante_app` para la Semana 14 de Programación Orientada a Objetos. Se mantiene una arquitectura modular y se mejora principalmente la interfaz gráfica mediante componentes, contenedores y gestores de geometría.

## Estructura

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
└── main.py
```

## Componentes y contenedores utilizados

Se utilizaron componentes de Tkinter/ttk como `Frame`, `LabelFrame`, `Label`, `Entry`, `Button`, `Treeview` y `Scrollbar`.

Los contenedores permiten separar:
- Encabezado.
- Navegación.
- Formulario de productos.
- Acciones.
- Área de presentación de registros.
- Consulta de usuarios.

Para organizar los componentes se utilizaron principalmente los gestores `pack()` y `grid()`.

## Mejoras realizadas

- Se conserva el inicio de sesión.
- Se agregó una interfaz principal organizada por zonas.
- Se incorporó una sección de consulta de usuarios.
- Se implementó un formulario para productos.
- Se implementaron las operaciones de registrar, cargar/consultar, actualizar y eliminar.
- Los botones utilizan `command=`.
- La lógica de negocio permanece en `RestauranteServicio`.
- La interfaz no manipula directamente los archivos JSON.
- La información de productos se actualiza después de las operaciones.

## Persistencia

Los productos se almacenan en `datos/productos.json` y los usuarios en `datos/usuarios.json`.

La lectura y escritura de los archivos se realiza mediante `ArchivoServicio`.

## Credenciales de prueba

- Usuario: `admin`
- Contraseña: `1234`

También existe el usuario:
- Usuario: `cajero`
- Contraseña: `1234`

## Ejecución

1. Tener Python 3 instalado.
2. Abrir una terminal dentro de la carpeta del proyecto.
3. Ejecutar:

```bash
python main.py
```

No se requieren librerías externas, ya que se utiliza Tkinter/ttk incluido con Python.

## Funcionalidades comprobables

1. Inicio de sesión.
2. Consulta de usuarios.
3. Registro de productos.
4. Consulta/carga de productos.
5. Actualización de productos.
6. Eliminación de productos.
7. Persistencia de cambios en `productos.json`.

## Semana 14

La implementación se concentra en el tema de **Componentes y contenedores**, evitando funcionalidades avanzadas de eventos que no forman parte del objetivo de esta actividad.
