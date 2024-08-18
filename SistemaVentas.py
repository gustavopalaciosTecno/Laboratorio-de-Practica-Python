import json
from datetime import datetime

class Venta:
    def __init__(self, fecha, cliente, productos):
        self.fecha = fecha
        self.cliente = cliente
        self.productos = productos

    def to_dict(self):
        return {
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "cliente": self.cliente,
            "productos": self.productos
        }

class VentaOnline(Venta):
    def __init__(self, fecha, cliente, productos, plataforma):
        super().__init__(fecha, cliente, productos)
        self.plataforma = plataforma

    def to_dict(self):
        data = super().to_dict()
        data["plataforma"] = self.plataforma
        return data

class VentaLocal(Venta):
    def __init__(self, fecha, cliente, productos, sucursal):
        super().__init__(fecha, cliente, productos)
        self.sucursal = sucursal

    def to_dict(self):
        data = super().to_dict()
        data["sucursal"] = self.sucursal
        return data

class GestorVentas:
    def __init__(self):
        self.ventas = []

    def agregar_venta(self, venta):
        self.ventas.append(venta)

    def eliminar_venta(self, index):
        try:
            self.ventas.pop(index)
        except IndexError:
            print(f"No existe ninguna venta en el índice {index}.")

    def modificar_venta(self, index, nueva_venta):
        try:
            self.ventas[index] = nueva_venta
        except IndexError:
            print(f"No existe ninguna venta en el índice {index}.")

    def listar_ventas(self):
        return [venta.to_dict() for venta in self.ventas]

    def guardar_en_json(self, archivo):
        with open(archivo, 'w') as f:
            json.dump(self.listar_ventas(), f, indent=4)

    def cargar_de_json(self, archivo):
        try:
            with open(archivo, 'r') as f:
                ventas_data = json.load(f)
                for venta in ventas_data:
                    fecha = datetime.strptime(venta["fecha"], "%Y-%m-%d %H:%M:%S")
                    if "plataforma" in venta:
                        self.agregar_venta(VentaOnline(fecha, venta["cliente"], venta["productos"], venta["plataforma"]))
                    elif "sucursal" in venta:
                        self.agregar_venta(VentaLocal(fecha, venta["cliente"], venta["productos"], venta["sucursal"]))
        except FileNotFoundError:
            print(f"El archivo {archivo} no existe.")
        except json.JSONDecodeError:
            print("Error al decodificar el archivo JSON.")

def mostrar_menu():
    print("###################SISTEMA DE GESTIÓN DE VENTAS#############################")
    print("\nMenú de opciones:")
    print("1. Agregar Venta Online")
    print("2. Agregar Venta Local")
    print("3. Listar Ventas")
    print("4. Modificar Venta")
    print("5. Eliminar Venta")
    print("6. Guardar Ventas en JSON")
    print("7. Cargar Ventas desde JSON")
    print("8. Salir")

def obtener_venta_online():
    cliente = input("Ingresá el nombre del cliente: ")
    productos = input("Ingresá los productos vendidos separados por comas: ").split(',')
    plataforma = input("Ingresá la plataforma de venta: ")
    return VentaOnline(datetime.now(), cliente, productos, plataforma)

def obtener_venta_local():
    cliente = input("Ingresá el nombre del cliente: ")
    productos = input("Ingresá los productos vendidos separados por comas: ").split(',')
    sucursal = input("Ingresa la sucursal de venta: ")
    return VentaLocal(datetime.now(), cliente, productos, sucursal)

def main():
    gestor = GestorVentas()

    while True:
        mostrar_menu()
        opcion = input("Seleccioná una opción: ")

        if opcion == "1":
            venta = obtener_venta_online()
            gestor.agregar_venta(venta)
            print("Venta Online agregada exitosamente.")
        elif opcion == "2":
            venta = obtener_venta_local()
            gestor.agregar_venta(venta)
            print("Venta Local agregada exitosamente.")
        elif opcion == "3":
            ventas = gestor.listar_ventas()
            if ventas:
                for i, venta in enumerate(ventas):
                    print(f"{i}: {venta}")
            else:
                print("No hay ventas registradas.")
        elif opcion == "4":
            index = int(input("Ingresá el índice de la venta a modificar: "))
            tipo_venta = input("¿Es una venta online o local? (online/local): ").lower()
            if tipo_venta == "online":
                nueva_venta = obtener_venta_online()
            elif tipo_venta == "local":
                nueva_venta = obtener_venta_local()
            else:
                print("Tipo de venta no válida.")
                continue
            gestor.modificar_venta(index, nueva_venta)
            print("Venta modificada exitosamente.")
        elif opcion == "5":
            index = int(input("Ingresá el índice de la venta a eliminar: "))
            gestor.eliminar_venta(index)
            print("Venta eliminada exitosamente.")
        elif opcion == "6":
            archivo = input("Ingresá el nombre del archivo JSON: ")
            gestor.guardar_en_json(archivo)
            print(f"Ventas guardadas en {archivo} exitosamente.")
        elif opcion == "7":
            archivo = input("Ingresá el nombre del archivo JSON: ")
            gestor.cargar_de_json(archivo)
            print(f"Ventas cargadas desde {archivo} exitosamente.")
        elif opcion == "8":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, por favor intentá nuvamente.")

if __name__ == "__main__":
    main()
