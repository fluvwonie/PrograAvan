from datetime import datetime, timedelta

#Clase para gestionar el material de la biblioteca 
class Material:
    def __init__(self, titulo, estado='disponible'):
        self.titulo = titulo
        self.estado = estado

    def prestar(self):
        if self.estado == 'disponible':
            self.estado = 'prestado'
            return True
        return False

    def devolver(self):
        self.estado = 'disponible'

    def __str__(self):
        return f"{self.titulo} ({self.estado})"


class Libro(Material):
    def __init__(self, titulo, autor, genero):
        super().__init__(titulo)
        self.autor = autor
        self.genero = genero

    def __str__(self):
        return f"Libro: {self.titulo} por {self.autor} ({self.genero})"

class Revista(Material):
    def __init__(self, titulo, edicion, periodicidad):
        super().__init__(titulo)
        self.edicion = edicion
        self.periodicidad = periodicidad

    def __str__(self):
        return f"Revista: {self.titulo}, edicion: {self.edicion} ({self.periodicidad})"

class MaterialDigital(Material):
    def __init__(self, titulo, tipo_archivo, enlace):
        super().__init__(titulo)
        self.tipo_archivo = tipo_archivo
        self.enlace = enlace

    def __str__(self):
        return f"Material digital: {self.titulo} ({self.tipo_archivo}) enlace: {self.enlace}"



#Clase para gestionar al usuario y bibliotecario 
class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido


class Usuario(Persona):
    def __init__(self,nombre,apellido):
        super().__init__(nombre,apellido)
        self.materiales_prestados = []
        self.penalizaciones = 0

    def pedir_prestado(self,material,fecha_prestamo,dias_prestamo=7):
        if material.prestar():
            fecha_devolucion = fecha_prestamo + timedelta(days=dias_prestamo)
            self.materiales_prestados.append((material, fecha_prestamo, fecha_devolucion))
            print(f"{self.nombre} pidio prestado '{material.titulo}' el {fecha_prestamo.strftime('%Y-%m-%d')}, debe devolverlo antes del {fecha_devolucion.strftime('%Y-%m-%d')}")
            return True
        print(f"No se pudo prestar '{material.titulo}', no esta disponible.")
        return False

    def devolver_material(self, material):
        for i, (j, fecha_prestamo, fecha_devolucion) in enumerate(self.materiales_prestados):
            if j == material:
                if datetime.now() > fecha_devolucion:
                    dias_retraso = (datetime.now() - fecha_devolucion).days
                    self.penalizaciones += dias_retraso
                    print(f"{self.nombre} ha devuelto '{material.titulo}' con {dias_retraso} dias de retraso. Penalizaciones acumuladas: {self.penalizaciones}")
                else:
                    print(f"{self.nombre} ha devuelto '{material.titulo}' a tiempo.")
                material.devolver()
                self.materiales_prestados.pop(i)
                return True
        print(f"'{material.titulo}' no esta en la lista de materiales prestados de {self.nombre}.")
        return False




class Bibliotecario(Persona):
    def __init__(self,nombre,apellido, sucursal):
        super().__init__(nombre,apellido)
        self.sucursal = sucursal

    def agregar_material(self, material):
        self.sucursal.agregar_material(material)

    def transferir_material(self, material, otra_sucursal):
        if self.sucursal.eliminar_material(material):
            otra_sucursal.agregar_material(material)
            print(f'{self.nombre} transfirio "{material.titulo}" a "{otra_sucursal.nombre}')




#Clase para gestionar las sucursales
class Sucursal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = []

   
    def agregar_material(self, material):
        self.catalogo.append(material)
        print(f'{material.titulo} fue agregado a la biblioteca {self.nombre}') 


    def eliminar_material(self, material):
        if material in self.catalogo:
            self.catalogo.remove(material)
            print(f'El {material.titulo} fue eliminado de la biblioteca {self.nombre}')
            return True
        print(f'No se encontro {material.titulo} en {self.nombre}')
        return False 
    
    
    def mostrar_catalogo(self):
        print(f'Catalogo de la biblioteca "{self.nombre}":')
        if self.catalogo:
            for i, material in enumerate(self.catalogo, 1):
                print(f'{i}, {material}')
        else:
            print('La biblioteca no tiene materiales.') 

    

# Clase para gestionar penalizaciones
class Penalizacion:
    def __init__(self, usuario, dias_retraso):
        self.usuario = usuario
        self.dias_retraso = dias_retraso
        self.multa = dias_retraso * 1  # Multa de $1 por día de retraso

    def __str__(self):
        return f"Penalizacion para {self.usuario.nombre}: {self.dias_retraso} dias de retraso, multa de ${self.multa}"



libro1 = Libro("Cronicas del espacio", "Neil deGrasse Tyson", "Informativo")
revista1 = Revista("National Geographic", "Enero 2025", "Mensual")
digital1 = MaterialDigital("Data Sciencie for dummies", "PDF", "http://iakshs.com/python.pdf")


sucursal1 = Sucursal("Biblioteca Central")
sucursal2 = Sucursal("Biblioteca Sur")

usuario1 = Usuario("Pedro","Medina")
bibliotecario1 = Bibliotecario("Ana","Gonzalez", sucursal1)
penalizacion1 = Penalizacion(usuario1, 3)


#Agregar material
bibliotecario1.agregar_material(libro1)
bibliotecario1.agregar_material(revista1)
bibliotecario1.agregar_material(digital1)


#Hacer el prestamo con retraso 
fecha_prestamo = datetime.now() - timedelta(days=10)  # Simular un préstamo hace 10 dias
usuario1.pedir_prestado(libro1, fecha_prestamo)
print(penalizacion1)

#Devolver el material con retraso 
usuario1.devolver_material(libro1)

# Transferir material entre sucursales
bibliotecario1.transferir_material(revista1, sucursal2)

# Consultar catalogos
sucursal1.mostrar_catalogo()
sucursal2.mostrar_catalogo()