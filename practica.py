import json

class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return f"Producto: {self.nombre}, Precio: {self.precio}, Cantidad: {self.cantidad}"

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad,
        }

class ProductoElectronico(Producto):
    def __init__(self, nombre, precio, cantidad, garantia):
        super().__init__(nombre, precio, cantidad)
        self.garantia = garantia

    def __str__(self):
        return f"Electrónico - {super().__str__()}, Garantía: {self.garantia} meses"

    def to_dict(self):
        data = super().to_dict()
        data['garantia'] = self.garantia
        return data

class ProductoAlimenticio(Producto):
    def __init__(self, nombre, precio, cantidad, fecha_caducidad):
        super().__init__(nombre, precio, cantidad)
        self.fecha_caducidad = fecha_caducidad

    def __str__(self):
        return f"Alimenticio - {super().__str__()}, Fecha de caducidad: {self.fecha_caducidad}"

    def to_dict(self):
        data = super().to_dict()
        data['fecha_caducidad'] = self.fecha_caducidad
        return data

class Inventario:
    def __init__(self, archivo='inventario.json'):
        self.archivo = archivo
        self.productos = []
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
                for item in datos:
                    tipo = item.pop('tipo')
                    if tipo == 'ProductoElectronico':
                        self.productos.append(ProductoElectronico(**item))
                    elif tipo == 'ProductoAlimenticio':
                        self.productos.append(ProductoAlimenticio(**item))
        except FileNotFoundError:
            print("Archivo de inventario no encontrado, se creará uno nuevo.")
        except json.JSONDecodeError:
            print("Error al leer el archivo de inventario.")

    def guardar_datos(self):
        with open(self.archivo, 'w') as f:
            json.dump([{'tipo': p.__class__.__name__, **p.to_dict()} for p in self.productos], f)

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.guardar_datos()

    def eliminar_producto(self, nombre):
        self.productos = [p for p in self.productos if p.nombre != nombre]
        self.guardar_datos()

    def actualizar_producto(self, nombre, **kwargs):
        for p in self.productos:
            if p.nombre == nombre:
                p.__dict__.update(kwargs)
        self.guardar_datos()

    def listar_productos(self):
        for p in self.productos:
            print(p)

def agregar_producto_electronico(inventario):
    try:
        nombre = input("Nombre del producto electrónico: ")
        precio = float(input("Precio: "))
        cantidad = int(input("Cantidad: "))
        garantia = int(input("Garantía (meses): "))
        producto = ProductoElectronico(nombre, precio, cantidad, garantia)
        inventario.agregar_producto(producto)
        print("Producto electrónico agregado exitosamente.")
    except ValueError:
        print("Error: Entrada no válida, por favor intente de nuevo.")

def agregar_producto_alimenticio(inventario):
    try:
        nombre = input("Nombre del producto alimenticio: ")
        precio = float(input("Precio: "))
        cantidad = int(input("Cantidad: "))
        fecha_caducidad = input("Fecha de caducidad (YYYY-MM-DD): ")
        producto = ProductoAlimenticio(nombre, precio, cantidad, fecha_caducidad)
        inventario.agregar_producto(producto)
        print("Producto alimenticio agregado exitosamente.")
    except ValueError:
        print("Error: Entrada no válida, por favor intente de nuevo.")

def main():
    inventario = Inventario()

    while True:
        print("\nMenú de Inventario:")
        print("1. Agregar Producto Electrónico")
        print("2. Agregar Producto Alimenticio")
        print("3. Eliminar Producto")
        print("4. Actualizar Producto")
        print("5. Listar Productos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_producto_electronico(inventario)
        elif opcion == '2':
            agregar_producto_alimenticio(inventario)
        elif opcion == '3':
            nombre = input("Nombre del producto a eliminar: ")
            inventario.eliminar_producto(nombre)
        elif opcion == '4':
            nombre = input("Nombre del producto a actualizar: ")
            campo = input("Campo a actualizar (nombre, precio, cantidad, etc.): ")
            valor = input("Nuevo valor: ")
            inventario.actualizar_producto(nombre, **{campo: valor})
        elif opcion == '5':
            inventario.listar_productos()
        elif opcion == '6':
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

if __name__ == "__main__":
    main()
