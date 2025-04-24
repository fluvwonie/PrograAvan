import json
import os
from gestor_json import GestorJSON


# Obtiene la ruta del directorio donde está el script actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_JSON = os.path.join(BASE_DIR, "users.json")
PRODUCTOS_JSON = os.path.join(BASE_DIR, "productos.json")
ORDERS_JSON = os.path.join(BASE_DIR, "orders.json")
INGREDIENTS_JSON = os.path.join(BASE_DIR, "inventario.json")



class GestorJSON:
    @staticmethod
    def cargar_datos(archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def guardar_datos(archivo, datos):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)


    @staticmethod
    def guardar_datos(archivo, datos):
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            print(f"Datos guardados correctamente en {archivo}")
        except Exception as e:
            print(f"Error guardando en {archivo}: {str(e)}")







class Persona:
    list_usuario = []

    def __init__(self, nombre, username, rol, password):
        self.nombre = nombre
        self.username = username
        self.rol = rol
        self.__pass = password
        Persona.list_usuario.append(self)

    @classmethod
    def iniciar_sesion(cls, username, password):
        for usuario in cls.list_usuario:
            if usuario.username == username and usuario._Persona__pass == password:
                return usuario
        return None

    @classmethod
    def cargar_usuarios(cls):
        cls.list_usuario = []
        data = GestorJSON.cargar_datos(USERS_JSON)
        for u in data:
            cls(
                nombre=u["nombre"],
                username=u["username"],
                rol=u["rol"],
                password=u["password"]
            )

    @classmethod
    def guardar_usuarios(cls):
        data = []
        for u in cls.list_usuario:
            data.append({
                "nombre": u.nombre,
                "username": u.username,
                "rol": u.rol,
                "password": u._Persona__pass
            })
        GestorJSON.guardar_datos(USERS_JSON, data)

class Inventario:
    ingredientes = {}

    @classmethod
    def cargar_ingredientes(cls):
        cls.ingredientes = GestorJSON.cargar_datos(INGREDIENTS_JSON)

    @classmethod
    def guardar_ingredientes(cls):
        GestorJSON.guardar_datos(INGREDIENTS_JSON, cls.ingredientes)

    @classmethod
    def descontar_ingredientes(cls, ingredientes_necesarios):
        for ing, cantidad in ingredientes_necesarios.items():
            if cls.ingredientes.get(ing, 0) < cantidad:
                return False
        for ing, cantidad in ingredientes_necesarios.items():
            cls.ingredientes[ing] -= cantidad
        cls.guardar_ingredientes()
        return True

class Producto:
    list_productos = []

    def __init__(self, nombre, precio, ingredientes):
        self.nombre = nombre
        self.precio = precio
        self.ingredientes = ingredientes
        Producto.list_productos.append(self)

    @classmethod
    def cargar_productos(cls):
        cls.list_productos = []
        data = GestorJSON.cargar_datos(PRODUCTOS_JSON)
        for p in data:
            cls(
                nombre=p["nombre"],
                precio=p["precio"],
                ingredientes=p["ingredientes"]
            )

    @classmethod
    def guardar_productos(cls):
        data = []
        for p in cls.list_productos:
            data.append({
                "nombre": p.nombre,
                "precio": p.precio,
                "ingredientes": p.ingredientes
            })
        GestorJSON.guardar_datos(PRODUCTOS_JSON, data)

class Pedido:
    list_pedidos = []

    def __init__(self, cliente, productos, estado="Pendiente"):
        self.cliente = cliente
        self.productos = productos  
        self.estado = estado
        Pedido.list_pedidos.append(self)

    


    def procesar_pedido(self):
        ingredientes_necesarios = {}
        for item in self.productos:
            producto = next((p for p in Producto.list_productos if p.nombre == item["producto"]), None)
            if producto:
                for ing in producto.ingredientes:
                    ingredientes_necesarios[ing] = ingredientes_necesarios.get(ing, 0) + 1
        if Inventario.descontar_ingredientes(ingredientes_necesarios):
            self.estado = "Completado"
            Pedido.guardar_pedidos()

    @classmethod
    def cargar_pedidos(cls):
        cls.list_pedidos = GestorJSON.cargar_datos(ORDERS_JSON)

    @classmethod
    def actualizar_estado_pedido(cls, pedido_id, nuevo_estado):
        
        estados_validos = {
            "pendiente": ["en_preparacion", "cancelado"],
            "en_preparacion": ["listo", "cancelado"],
            "listo": ["entregado"],
            "cancelado": [],
            "entregado": []
        }
        
        # Buscar el pedido en la lista
        pedido = next((p for p in cls.list_pedidos if p.get("id") == pedido_id), None)
        
        if not pedido:
            return False
            
        estado_actual = pedido.get("estado")
        
        # Validar transición de estado
        if nuevo_estado not in estados_validos.get(estado_actual, []):
            return False
        
        # Actualizar estado
        pedido["estado"] = nuevo_estado
        
        # Guardar cambios en el archivo
        try:
            GestorJSON.guardar_datos(ORDERS_JSON, cls.list_pedidos)
            return True
        except Exception as e:
            print(f"Error al guardar pedido actualizado: {e}")
            return False
           

    @classmethod
    def guardar_pedidos(cls):
        data = []
        for p in cls.list_pedidos:
            data.append({
                "cliente": p.cliente,
                "productos": p.productos,
                "estado": p.estado
            })
        GestorJSON.guardar_datos(ORDERS_JSON, data)


class Administrador(Persona):
    def __init__(self, nombre, username, password):
        super().__init__(nombre, username, "admin", password)

    def modificar_inventario(self, nombre, nueva_cantidad):
        Inventario.ingredientes[nombre] = nueva_cantidad
        Inventario.guardar_ingredientes()

    def ver_pedidos(self):
        for p in Pedido.list_pedidos:
            print(f"Cliente: {p.cliente}, Estado: {p.estado}, Productos: {[prod for prod in p.productos]}")

