import customtkinter as ctk
import tkinter as tk
import datetime
import os
from tkinter import messagebox 
from tkinter import simpledialog
from PIL import Image

import sys

# Ruta base para archivos empaquetados con PyInstaller
BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
def ruta_archivo(nombre):
    return os.path.join(BASE_PATH, nombre)

from caf_backend import *
from customtkinter import CTkImage


COLOR_FONDO = "#F9F6F1"
COLOR_PRINCIPAL = "#D2AB80"
COLOR_HOVER = "#B58F65"
COLOR_TEXTO = "#4A3F35"
COLOR_FRAME = "#FFF9F3"
COLOR_INPUT = "#FFF4E6"


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")



class StartWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bienvenido a LatteHaus")
        self.geometry("700x500")
        self.configure(bg="#f3f3f3")

        try:
            img=Image.open(ruta_archivo("C:/Users/fatis/Documents/ProyectoCafeteria/cafeteria/logo.png"))
            img=img.resize((250,250))
            self.bg_image=CTkImage(light_image=img, size=(250,250))
            ctk.CTkLabel(self, image=self.bg_image, text="").pack(pady=5)
        except:
            ctk.CTkLabel(self, text="Imagen de bienvenida").pack(pady=5)    
        
        ctk.CTkLabel(self, text="¡Bienvenido a LatteHaus!", font=("Century Gothic", 24,"bold"), text_color=COLOR_TEXTO).pack(pady=5)
        ctk.CTkLabel(self, text="Por favor identificate antes para continuar", font=("Century Gothic", 16), text_color=COLOR_TEXTO).pack(pady=5)


        ctk.CTkButton(self, text="Cliente", command=self.abrir_cliente, 
                        fg_color=COLOR_PRINCIPAL,
                        hover_color=COLOR_HOVER,
                        font=("Century Gothic", 14),
                        text_color="white",width=200).pack(pady=10)
        ctk.CTkButton(self, text="Empleado / Administrador", command=self.abrir_login,
                        fg_color=COLOR_PRINCIPAL,
                        hover_color=COLOR_HOVER,
                        font=("Century Gothic", 14)
                        , width=200).pack(pady=10)

    def abrir_cliente(self):
        self.withdraw()
        ClienteApp(self)

    def abrir_login(self):
        self.withdraw()
        LoginApp(self)


class ClienteApp(ctk.CTkToplevel):
    def __init__(self, ventana_anterior):
        super().__init__()
        self.ventana_anterior = ventana_anterior
        self.title("Menú de LatteHaus")
        self.geometry("1200x700")

        self.imagenes_cargadas=[]
        self.pedido_actual=[]
        self.pedido_id=None

        self.menu_frame = ctk.CTkScrollableFrame(self, fg_color=COLOR_FRAME, width=500)
        self.menu_frame.pack(side="left", fill="both", expand=False, padx=10, pady=10)

        self.pedido_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, width=300)
        self.pedido_frame.pack(side="right", fill="y", padx=10, pady=10)

        self.estado_frame=ctk.CTkFrame(self,fg_color=COLOR_FRAME, width=300)
        self.estado_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(self.pedido_frame, text="Tu pedido 🛒", font=("Century Gothic", 15), text_color=COLOR_TEXTO).pack(pady=10)

        self.lista_pedido= ctk.CTkTextbox(self.pedido_frame, height=350, state="disabled", wrap="word")
        self.lista_pedido.pack(pady=10)

        self.total_label=ctk.CTkLabel(self.pedido_frame, text="Total: $0", font=("Century Gothic", 14, "bold"), text_color=COLOR_TEXTO)
        self.total_label.pack(pady=10)

        ctk.CTkButton(self.pedido_frame, 
                      text="Confirmar pedido", 
                      fg_color=COLOR_PRINCIPAL,
                      hover_color=COLOR_HOVER,
                      text_color="white",
                      font=("Century Gothic", 14),
                      command=self.confirmar_pedido).pack(pady=10)
        
        ctk.CTkButton(self.pedido_frame,
                      text="Cancelar pedido",
                      fg_color=COLOR_PRINCIPAL,
                      hover_color=COLOR_HOVER,
                      text_color="white",
                      font=("Century Gothic", 14),
                      command=self.cancelar_pedido).pack(pady=5)
        
        ctk.CTkLabel(self.estado_frame, text="Estado de tu pedido", font=("Century Gothic", 15), text_color=COLOR_TEXTO).pack(pady=10)
        
        self.estado_pedido = ctk.CTkLabel(self.estado_frame, text="No hay pedido activo", font=("Arial", 12), text_color=COLOR_TEXTO)
        self.estado_pedido.pack(pady=10)
        
        self.tiempo_estimado = ctk.CTkLabel(self.estado_frame, text="Tiempo estimado: -", font=("Arial", 12), text_color=COLOR_TEXTO)
        self.tiempo_estimado.pack(pady=5)

        ctk.CTkButton(self.estado_frame, 
                     text="Actualizar estado", 
                     fg_color=COLOR_PRINCIPAL,
                     hover_color=COLOR_HOVER,
                     text_color="white",
                     font=("Century Gothic", 14),
                     command=self.actualizar_estado_pedido).pack(pady=10)
                      

    

        volver_btn = ctk.CTkButton(self, 
                                text="← Volver al inicio", 
                                command=self.volver,
                                fg_color=COLOR_PRINCIPAL,
                                hover_color=COLOR_HOVER,
                                text_color="white")
        volver_btn.pack(side="bottom",pady=10)

        self.cargar_productos()
        self.actualizar_total()


    def actualizar_total(self):
        total = 0
        for item in self.pedido_actual:
           
            precio_str = item.split(" - $")[-1].split("\n")[0]
            try:
                total += float(precio_str)
            except ValueError:
                pass
        self.total_label.configure(text=f"Total: ${total:.2f}")
        return total

    def cargar_productos(self):
        ruta_absoluta= os.path.join(os.path.dirname(__file__), "productos.json")
        with open(ruta_absoluta, "r", encoding="utf-8") as f:
            productos=json.load(f)

        for prod in productos:
            self.mostrar_producto(prod)

       
 
    
 

    def mostrar_producto(self, producto):
        frame=ctk.CTkFrame(self.menu_frame, fg_color=COLOR_FRAME)
        frame.pack(padx=10, pady=10, fill="x")

        try:
            img_path=os.path.join(os.path.dirname(__file__), producto.get("imagen","imagenes/default.jpg"))
            print("Ruta de imagen:", img_path)
            img= Image.open(img_path)
            img=img.resize((200,200))
            ct_img=ctk.CTkImage(light_image=img, size=(200,200))
            self.imagenes_cargadas.append(ct_img)
            ctk.CTkLabel(frame, image=ct_img, text="").pack(side="left", padx=10) 
        
        except Exception as e:
            print(f"Error al cargar imagen de {producto['nombre']}: {e}")
            ctk.CTkLabel(frame, text="[Imagen no encontrada]").pack(side="left", padx=10)

        content_frame=ctk.CTkFrame(frame, bg_color=COLOR_FRAME)
        content_frame.pack(side="left", fill="both",expand=False, padx=10) 

        ctk.CTkLabel(content_frame, text=f"{producto['nombre']} - ${producto['precio']}", font=("Arial", 16), text_color=COLOR_TEXTO).pack(anchor="w")         


        selecciones={
            "leche": "No aplica",
            "azucar": "No aplica",
            "extras": "No aplica"
        }

        opciones_widgets={}

        personalizaciones=producto.get("personalizaciones",{})

        if "leche" in personalizaciones:
            ctk.CTkLabel(content_frame, text="Tipo de leche:", font=("Century Gothic", 14), text_color=COLOR_TEXTO).pack(anchor="w")
            leche_opcion = ctk.CTkOptionMenu(content_frame, values=personalizaciones["leche"], 
                                              fg_color=COLOR_PRINCIPAL,
                                                button_color=COLOR_PRINCIPAL,
                                                button_hover_color=COLOR_HOVER,
                                                text_color="white",
                                                dropdown_fg_color=COLOR_FRAME,
                                                dropdown_hover_color=COLOR_HOVER,
                                                dropdown_text_color=COLOR_TEXTO,
                                                font=("Century Gothic", 13))
            leche_opcion.pack(anchor="w")
            opciones_widgets["leche"] = leche_opcion

        if "azucar" in personalizaciones:
            ctk.CTkLabel(content_frame, text="Azúcar:",font=("Century Gothic", 14)).pack(anchor="w")
            azucar_opcion = ctk.CTkOptionMenu(content_frame, values=personalizaciones["azucar"],
                                                fg_color=COLOR_PRINCIPAL,
                                               
                                                button_color=COLOR_PRINCIPAL,
                                                button_hover_color=COLOR_HOVER,
                                                text_color="white",
                                                dropdown_fg_color=COLOR_FRAME,
                                                dropdown_hover_color=COLOR_HOVER,
                                                dropdown_text_color=COLOR_TEXTO,
                                                font=("Century Gothic", 13))
            azucar_opcion.pack(anchor="w")
            opciones_widgets["azucar"] = azucar_opcion

        if "extras" in personalizaciones:
            ctk.CTkLabel(content_frame, text="Extras:", font=("Century Gothic", 14)).pack(anchor="w")
            extra_opcion = ctk.CTkOptionMenu(content_frame, values=personalizaciones["extras"], 
                                             fg_color=COLOR_PRINCIPAL,                            
                                             button_color=COLOR_PRINCIPAL,
                                             button_hover_color=COLOR_HOVER,
                                             text_color="white",
                                             dropdown_fg_color=COLOR_FRAME,
                                             dropdown_hover_color=COLOR_HOVER,
                                             dropdown_text_color=COLOR_TEXTO,
                                             font=("Century Gothic", 13))
            extra_opcion.pack(anchor="w")
            opciones_widgets["extras"] = extra_opcion

       
        if not personalizaciones:
            ctk.CTkLabel(content_frame, text="Este producto no tiene opciones de personalización").pack(anchor="w")

        
        ctk.CTkButton(
            content_frame,
            text="Agregar al pedido",
            command=lambda: self.agregar_al_pedido(
                producto,
                opciones_widgets.get("leche", "No aplica"),
                opciones_widgets.get("azucar", "No aplica"),
                opciones_widgets.get("extras", "No aplica")
            ),fg_color=COLOR_PRINCIPAL,
            hover_color=COLOR_HOVER,
            font=("Century Gothic",12)
        ).pack(pady=5)


       

    def agregar_al_pedido(self, producto, leche_widget, azucar_widget, extra_widget):
    
        leche = leche_widget.get() if hasattr(leche_widget, 'get') else leche_widget
        azucar = azucar_widget.get() if hasattr(azucar_widget, 'get') else azucar_widget
        extra = extra_widget.get() if hasattr(extra_widget, 'get') else extra_widget
        
        # Construir el texto del pedido mostrando solo las opciones aplicables
        texto = f"{producto['nombre']} - ${producto['precio']}"
        
        personalizaciones = producto.get("personalizaciones", {})
        detalles = []
        
        if "leche" in personalizaciones and leche != "No aplica":
            detalles.append(f"Leche: {leche}")
        
        if "azucar" in personalizaciones and azucar != "No aplica":
            detalles.append(f"Azúcar: {azucar}")
        
        if "extras" in personalizaciones and extra != "No aplica":
            detalles.append(f"Extra: {extra}")
        
        if detalles:
            texto += "\n > " + " | ".join(detalles)
        
     
        self.pedido_actual.append(texto)

        self.lista_pedido.configure(state="normal")
        self.lista_pedido.insert("end", texto + "\n\n")
        self.lista_pedido.configure(state="disabled")
        self.actualizar_total()

  

    def confirmar_pedido(self):
        if not self.pedido_actual:
            messagebox.showwarning("Pedido vacio", "No hay items en tu pedido")
            return

        nombre_cliente = simpledialog.askstring("Nombre", "Por favor ingresa tu nombre para el pedido:")
        if not nombre_cliente:
            return
        
        total = self.actualizar_total()
        
     
        self.pedido_id = int(datetime.datetime.now().timestamp())
        
        
        pedido_data = {
            "id": self.pedido_id,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cliente": nombre_cliente,
            "items": [item.split("\n")[0] for item in self.pedido_actual],
            "personalizaciones": [item.split("\n")[1][3:] for item in self.pedido_actual if "\n" in item],
            "total": total,
            "estado": "pendiente",
            "pago": False
        }
        
       
        try:
            ruta_ordenes=os.path.join(os.path.dirname(__file__), "orders.json")
            with open(ruta_ordenes, "r", encoding="utf-8") as f:
                pedidos = json.load(f)
        except FileNotFoundError:
            pedidos = []
        
        pedidos.append(pedido_data)
        
        with open(ruta_ordenes, "w", encoding="utf-8") as f:
            json.dump(pedidos, f, indent=2)
        
        
    
        
        
        messagebox.showinfo("Pedido confirmado", f"Pedido #{self.pedido_id} confirmado!\nTotal: ${total:.2f}")
        
       
        self.estado_pedido.configure(text=f"Pedido #{self.pedido_id}: Pendiente")
        self.tiempo_estimado.configure(text="Tiempo estimado: 15-20 min")
        
     
        self.pedido_actual.clear()
        self.lista_pedido.configure(state="normal")
        self.lista_pedido.delete("1.0", "end")
        self.lista_pedido.configure(state="disabled")
        self.actualizar_total()

    def cancelar_pedido(self):
        if not self.pedido_id:
            messagebox.showwarning("Sin pedido", "No hay un pedido activo para cancelar")
            return
        
        confirmacion = messagebox.askyesno(
            "Cancelar pedido", 
            f"¿Estás seguro de cancelar el pedido #{self.pedido_id}?"
        )
        
        if confirmacion:
           
            try:
                ruta_ordenes=os.path.join(os.path.dirname(__file__), "orders.json")
                with open(ruta_ordenes, "r", encoding="utf-8") as f:
                    pedidos = json.load(f)
                
                for pedido in pedidos:
                    if pedido["id"] == self.pedido_id:
                        pedido["estado"] = "cancelado"
                        break
        
                with open(ruta_ordenes, "w", encoding="utf-8") as f:
                    json.dump(pedidos, f, indent=2)
                
              
                self.estado_pedido.configure(text=f"Pedido #{self.pedido_id}: Cancelado")
                self.tiempo_estimado.configure(text="Tiempo estimado: -")
                self.pedido_id = None
                
                messagebox.showinfo("Pedido cancelado", "Tu pedido ha sido cancelado exitosamente")
                
            except FileNotFoundError:
                messagebox.showerror("Error", "No se pudo cancelar el pedido")    

    def cancelar_pedido_actual(self):
        if not self.pedido_id:
            messagebox.showinfo("Cancelar pedido", "No hay pedido activo para cancelar.")
            return

        confirm = messagebox.askyesno("Cancelar", "¿Seguro que deseas cancelar el pedido?")
        if not confirm:
            return

        # Cargar los pedidos
        try:
            ruta_orders=os.path.join(os.path.dirname(__file__), "orders.json")
            with open(ruta_orders, "r", encoding="utf-8") as f:
                pedidos = json.load(f)
        except FileNotFoundError:
            pedidos = []

        # Buscar el pedido por ID
        pedido_cancelado = None
        for p in pedidos:
            if p["id"] == self.pedido_id:
                pedido_cancelado = p
                break

        if not pedido_cancelado:
            messagebox.showerror("Error", "Pedido no encontrado.")
            return

        self.cancelar_pedido(pedido_cancelado)

        self.estado_pedido.configure(text="Pedido cancelado")
        self.tiempo_estimado.configure(text="Tiempo estimado: -")
        self.pedido_id = None


    def actualizar_estado_pedido(self):
        
        if not self.pedido_id:
            messagebox.showwarning("Sin pedido", "No hay un pedido activo")
            return
        
        try:
            ruta_ordenes=os.path.join(os.path.dirname(__file__), "orders.json")
            with open(ruta_ordenes, "r", encoding="utf-8") as f:
                pedidos = json.load(f)
            
            for pedido in pedidos:
                if pedido["id"] == self.pedido_id:
                    estado = pedido["estado"]
                    self.estado_pedido.configure(text=f"Estado: {estado.capitalize()}")
                    
                    # Mostrar acciones disponibles para cliente
                    if estado == "pendiente":
                        self.tiempo_estimado.configure(text="Puedes cancelar el pedido si lo deseas")
                    elif estado == "en_preparacion":
                        self.tiempo_estimado.configure(text="Tu pedido está en preparación")
                    
                    return
            
            messagebox.showerror("Error", "Pedido no encontrado")
        except FileNotFoundError:
            messagebox.showerror("Error", "No se pudo cargar el estado")

    def volver(self):
        self.destroy()
        self.ventana_anterior.deiconify()


class LoginApp(ctk.CTkToplevel):
    def __init__(self, ventana_anterior):
        super().__init__()
        self.ventana_anterior = ventana_anterior

        self.geometry("800x500")
        self.title("LatteHaus - Login")
        self.resizable(False, False)

       
        self.left_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, width=400)
        self.left_frame.pack(side="left", fill="both", expand=True)

       
        title = ctk.CTkLabel(self.left_frame, text="Bienvenido!", font=("Century Gothic", 24, "bold"), text_color=COLOR_TEXTO)
        title.pack(pady=(50, 10))

        subtitle = ctk.CTkLabel(self.left_frame, text="Inicia sesión para entrar a LatteHaus", font=("Century Gothic", 14), text_color=COLOR_TEXTO)
        subtitle.pack(pady=(0, 20))

        
        self.username_entry = ctk.CTkEntry(self.left_frame, placeholder_text="Usuario",
                                           fg_color=COLOR_INPUT,
                                           text_color=COLOR_TEXTO)
        self.username_entry.pack(pady=10, padx=40)

        self.password_entry = ctk.CTkEntry(self.left_frame, placeholder_text="Contraseña", show="*",
                                           fg_color=COLOR_INPUT,
                                           text_color=COLOR_TEXTO)
        self.password_entry.pack(pady=10, padx=40)

       
        login_btn = ctk.CTkButton(
            self.left_frame,
            text="Iniciar",
            command=self.login,
            fg_color=COLOR_PRINCIPAL,
            hover_color=COLOR_HOVER,
            text_color="white"
        )
        login_btn.pack(pady=20)

     
        volver_btn = ctk.CTkButton(
            self.left_frame, 
            text="← Volver", 
            command=self.volver,
            fg_color=COLOR_PRINCIPAL,
            hover_color=COLOR_HOVER,
            text_color="white")
        volver_btn.pack(pady=10)

       
        self.right_frame = ctk.CTkFrame(self,fg_color=COLOR_FRAME, width=400)
        self.right_frame.pack(side="right", fill="both", expand=False)

        img = Image.open(ruta_archivo("C:/Users/fatis/Documents/ProyectoCafeteria/cafeteria/cafeteria.jpg"))
        resized = img.resize((400, 500))

        self.bg_image = CTkImage(light_image=resized, size=(400, 500))
        image_label = ctk.CTkLabel(self.right_frame, image=self.bg_image, text="")
        image_label.pack()

    def login(self):
        usuario = self.username_entry.get()
        contraseña = self.password_entry.get()

        ruta_usuarios=os.path.join(os.path.dirname(__file__), "users.json")
        try:
           
            with open(ruta_usuarios,"r", encoding="utf-8") as f:
                usuarios = json.load(f)
        
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontro el archivo") 
            return

        
        for u in usuarios:
            if u["username"] == usuario and u["password"] == contraseña:
                messagebox.showinfo("Bienvenido", f"Hola {u["nombre"].capitalize()} ({u["rol"]})")
                self.destroy()
                if u["rol"] == "admin":
                    AdminApp(self.ventana_anterior)
                elif u["rol"] == "empleado":
                    EmpleadoApp(self.ventana_anterior)
                return 
            
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")    


    
    def volver(self):
        self.destroy()
        self.ventana_anterior.deiconify()


class AdminApp(ctk.CTkToplevel):
    def __init__(self, ventana_anterior):
        super().__init__()
        self.ventana_anterior = ventana_anterior
        self.title("Panel de Administración")
        self.geometry("1000x600")
        

        
        main_frame=ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkButton(main_frame, text="← Volver al inicio", command=self.volver,
                     fg_color=COLOR_PRINCIPAL, hover_color=COLOR_HOVER, text_color="white",font=("Century Gothic",12)).pack(pady=5)
        
        self.tab = ctk.CTkTabview(main_frame, width=900, height=500)
        self.tab.pack(pady=(0,10))

        
        self.tab_pedidos = self.tab.add("🧾 Pedidos")
        self.tab_inventario = self.tab.add("📦 Inventario")
        self.tab_historial = self.tab.add("📖 Historial")

        self.setup_pedidos()
        self.setup_inventario()
        self.mostrar_historial()
    
        
   
    
    def setup_pedidos(self):
        self.pedidos_frame = ctk.CTkScrollableFrame(self.tab_pedidos)
        self.pedidos_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.mostrar_pedidos()

    def setup_inventario(self):
        self.inventario_text = ctk.CTkTextbox(self.tab_inventario, height=300)
        self.inventario_text.pack(pady=10)    


    

        ctk.CTkButton(self.tab_inventario, text="Actualizar inventario", 
                      command=self.actualizar_inventario,
                      fg_color=COLOR_PRINCIPAL,
                        hover_color=COLOR_HOVER,
                        text_color="white",
                        font=("Century Gothic", 11)).pack(pady=5)
        ctk.CTkButton(self.tab_inventario,text="+ Agregar inventario", 
                      command=self.agregar_ingrediente,
                      fg_color=COLOR_PRINCIPAL,
                        hover_color=COLOR_HOVER,
                        text_color="white",
                        font=("Century Gothic", 11)).pack(pady=5)
        ctk.CTkButton(self.tab_inventario, text="- Eliminar inventario", 
                      command=self.eliminar_ingrediente,
                      fg_color=COLOR_PRINCIPAL,
                        hover_color=COLOR_HOVER,
                        text_color="white",
                        font=("Century Gothic", 11)).pack(pady=5)

        self.mostrar_inventario()

    def mostrar_pedidos(self):
        self.pedidos_frame._scrollbar.set(0, 0)
        for widget in self.pedidos_frame.winfo_children():
            widget.destroy()

        ruta = os.path.join(os.path.dirname(__file__), "orders.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                pedidos = json.load(f)
        except:
            pedidos = []

        for pedido in pedidos:
            frame = ctk.CTkFrame(self.pedidos_frame, fg_color=COLOR_FRAME)
            frame.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(frame, text=f"ID: {pedido['id']} | Cliente: {pedido['cliente']} | Estado: {pedido['estado']} | Total: ${pedido['total']}", font=("Arial", 14)).pack(anchor="w")
            ctk.CTkLabel(frame, text="Items: " + ", ".join(pedido["items"]), wraplength=600).pack(anchor="w")
            
            ctk.CTkButton(frame, text="Cambiar estado", command=lambda p=pedido: self.cambiar_estado(p)).pack(side="left", padx=5, pady=5)
            ctk.CTkButton(frame, text="Marcar como pagado", command=lambda p=pedido: self.marcar_pagado(p)).pack(side="left", padx=5, pady=5)
            ctk.CTkButton(frame, text="Cancelar pedido", command=lambda p=pedido: self.cancelar_pedido(p)).pack(side="left", padx=5, pady=5)


    def cambiar_estado(self, pedido):
        nuevo_estado = simpledialog.askstring("Estado", f"Nuevo estado para pedido #{pedido['id']}:")
        if not nuevo_estado:
            return

        ruta = os.path.join(os.path.dirname(__file__), "orders.json")
        with open(ruta, "r", encoding="utf-8") as f:
            pedidos = json.load(f)

        for p in pedidos:
            if p["id"] == pedido["id"]:
                p["estado"] = nuevo_estado
                break

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(pedidos, f, indent=2)

        self.mostrar_pedidos()

    def marcar_pagado(self, pedido):
        self.mover_historial(pedido, "pagado")
        messagebox.showinfo("Pago registrado", f"Pedido #{pedido["id"]} marcado como pagado")

    def cancelar_pedido(self,pedido):
        confirm=messagebox.askyesno("Cancelar", f"¿Cancelar el pedido #{pedido['id']}?")
        if confirm:
            self.mover_historial(pedido, "cancelado")
            messagebox.showinfo("Pedido cancelado", f"Pedido #{pedido['id']} ha sido cancelado.")
    
    
    def mostrar_inventario(self):
        self.inventario_text.configure(state="normal")
        self.inventario_text.delete("1.0", "end")
        ruta = os.path.join(os.path.dirname(__file__), "inventario.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                inventario = json.load(f)
        except:
            inventario = {}

        for ingrediente, cantidad in inventario.items():
            self.inventario_text.insert("end", f"{ingrediente}: {cantidad}\n")

        self.inventario_text.configure(state="disabled")

    def actualizar_inventario(self):
        nueva_cantidad = simpledialog.askstring("Actualizar", "Escribe 'ingrediente:cantidad' (ej. leche:10)")
        if not nueva_cantidad or ":" not in nueva_cantidad:
            return

        ing, cant = nueva_cantidad.split(":")
        ing = ing.strip().lower()
        try:
            cant = int(cant.strip())
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.")
            return

        ruta = os.path.join(os.path.dirname(__file__), "inventario.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                inventario = json.load(f)
        except:
            inventario = {}

        inventario[ing] = cant

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(inventario, f, indent=2)

        self.mostrar_inventario()
        messagebox.showinfo("Inventario actualizado", f"{ing} → {cant} unidades.")

        
    def agregar_ingrediente(self):
        nuevo = simpledialog.askstring("Nuevo ingrediente", "Escribe 'ingrediente:cantidad' (ej. miel:10)")
        if not nuevo or ":" not in nuevo:
            return

        nombre, cantidad = nuevo.split(":")
        nombre = nombre.strip().lower()
        try:
            cantidad = int(cantidad.strip())
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.")
            return

        ruta = os.path.join(os.path.dirname(__file__), "inventario.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                inventario = json.load(f)
        except:
            inventario = {}

        if nombre in inventario:
            messagebox.showwarning("Ya existe", f"El ingrediente '{nombre}' ya existe.")
            return

        inventario[nombre] = cantidad

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(inventario, f, indent=2)

        self.mostrar_inventario()
        messagebox.showinfo("Agregado", f"'{nombre}' fue agregado al inventario.")

    def eliminar_ingrediente(self):
        nombre = simpledialog.askstring("Eliminar", "¿Qué ingrediente deseas eliminar?")
        if not nombre:
            return

        nombre = nombre.strip().lower()

        ruta = os.path.join(os.path.dirname(__file__), "inventario.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                inventario = json.load(f)
        except:
            inventario = {}

        if nombre not in inventario:
            messagebox.showerror("No encontrado", f"'{nombre}' no está en el inventario.")
            return

        confirm = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar '{nombre}'?")
        if confirm:
            del inventario[nombre]
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(inventario, f, indent=2)
            self.mostrar_inventario()
            messagebox.showinfo("Eliminado", f"'{nombre}' fue eliminado del inventario.")

    def mover_historial(self, pedido, nuevo_estado):
        pedido["estado"] = nuevo_estado
        pedido["fecha_finalizacion"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ruta_historial = os.path.join(os.path.dirname(__file__), "historial.json")

        try:
            with open(ruta_historial, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except FileNotFoundError:
            historial = []

        historial.append(pedido)

        with open(ruta_historial, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=2)

        # Quitar de orders.json
        ruta_orders = os.path.join(os.path.dirname(__file__), "orders.json")
        with open(ruta_orders, "r", encoding="utf-8") as f:
            pedidos = json.load(f)

        pedidos = [p for p in pedidos if p["id"] != pedido["id"]]

        with open(ruta_orders, "w", encoding="utf-8") as f:
            json.dump(pedidos, f, indent=2)

        self.mostrar_pedidos()

    def mostrar_historial(self):
        for widget in self.tab_historial.winfo_children():
            widget.destroy()

        ruta_historial = os.path.join(os.path.dirname(__file__), "historial.json")

        try:
            with open(ruta_historial, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except FileNotFoundError:
            historial = []

        scroll = ctk.CTkScrollableFrame(self.tab_historial,fg_color=COLOR_FRAME)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        if not historial:
            ctk.CTkLabel(scroll, text="No hay pedidos en el historial.").pack(pady=20)
            return

        for pedido in historial:
            frame = ctk.CTkFrame(scroll)
            frame.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(frame, text=f"Pedido #{pedido['id']} - {pedido['estado']} - {pedido['fecha_finalizacion']}",
                        font=("Arial", 14)).pack(anchor="w")

            ctk.CTkLabel(frame, text="Items: " + ", ".join(pedido["items"]), wraplength=700).pack(anchor="w", padx=5)
    
    def volver(self):
        self.destroy()
        self.ventana_anterior.deiconify()   
        
   


class EmpleadoApp(ctk.CTkToplevel):
    def __init__(self, ventana_anterior):
        super().__init__()
        self.ventana_anterior = ventana_anterior
        self.title("Panel del Empleado - LatteHaus")
        self.geometry("1000x600")


        main_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.tabview = ctk.CTkTabview(main_frame, width=900, height=500)
        self.tabview.pack(pady=(0, 10))

        ctk.CTkButton(main_frame, text="← Volver al inicio", command=self.volver,
              fg_color=COLOR_PRINCIPAL, hover_color=COLOR_HOVER, text_color="white").pack(pady=5)

        
    

        self.tab_pedidos = self.tabview.add("🧾 Pedidos")
        self.tab_inventario = self.tabview.add("📦 Inventario")

        self.setup_pedidos()
        self.setup_inventario()

        ctk.CTkButton(self, text="← Volver al inicio", command=self.volver,
              fg_color=COLOR_PRINCIPAL, hover_color=COLOR_HOVER, text_color="white").pack(pady=10)  


    def setup_pedidos(self):
        self.pedidos_frame = ctk.CTkScrollableFrame(self.tab_pedidos, fg_color=COLOR_FRAME)
        self.pedidos_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.mostrar_pedidos()

    def mostrar_pedidos(self):
        for widget in self.pedidos_frame.winfo_children():
            widget.destroy()

        ruta = os.path.join(os.path.dirname(__file__), "orders.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                pedidos = json.load(f)
        except:
            pedidos = []

        for pedido in pedidos:
            frame = ctk.CTkFrame(self.pedidos_frame)
            frame.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(frame, text=f"ID: {pedido['id']} | Estado: {pedido['estado']} | Total: ${pedido['total']}", font=("Arial", 14)).pack(anchor="w")
            ctk.CTkLabel(frame, text="Items: " + ", ".join(pedido["items"]), wraplength=600).pack(anchor="w")

            ctk.CTkButton(frame, text="Marcar como pagado", command=lambda p=pedido: self.marcar_pagado(p)).pack(side="left", padx=5, pady=5)
            
   
    def marcar_pagado(self, pedido):
        pedido["estado"] = "pagado"
        pedido["fecha_finalizacion"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ruta_historial = os.path.join(os.path.dirname(__file__), "historial.json")

        try:
            with open(ruta_historial, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except:
            historial = []

        historial.append(pedido)

        with open(ruta_historial, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=2)

        
        ruta_orders = os.path.join(os.path.dirname(__file__), "orders.json")
        with open(ruta_orders, "r", encoding="utf-8") as f:
            pedidos = json.load(f)

        pedidos = [p for p in pedidos if p["id"] != pedido["id"]]

        with open(ruta_orders, "w", encoding="utf-8") as f:
            json.dump(pedidos, f, indent=2)

        self.mostrar_pedidos()
        messagebox.showinfo("Pedido pagado", f"Pedido #{pedido['id']} fue finalizado.")

    def setup_inventario(self):
        self.inventario_text = ctk.CTkTextbox(self.tab_inventario, height=400)
        self.inventario_text.pack(pady=10)

        ctk.CTkButton(self.tab_inventario, text="Actualizar cantidades", 
                      command=self.actualizar_inventario,
                      fg_color=COLOR_PRINCIPAL,
                    hover_color=COLOR_HOVER,
                    text_color="white",
                    font=("Century Gothic", 11)).pack(pady=5)
        self.mostrar_inventario()

    def mostrar_inventario(self):
        self.inventario_text.configure(state="normal")
        self.inventario_text.delete("1.0", "end")
        ruta = os.path.join(os.path.dirname(__file__), "inventario.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                inventario = json.load(f)
        except:
            inventario = {}

        for ingrediente, cantidad in inventario.items():
            self.inventario_text.insert("end", f"{ingrediente}: {cantidad}\n")

        self.inventario_text.configure(state="disabled")

    def actualizar_inventario(self):
        entrada = simpledialog.askstring("Actualizar", "Ingrediente:cantidad (ej. leche:10)")
        if not entrada or ":" not in entrada:
            return

        nombre, cantidad = entrada.split(":")
        nombre = nombre.strip().lower()
        try:
            cantidad = int(cantidad.strip())
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.")
            return

        ruta = os.path.join(os.path.dirname(__file__), "inventario.json")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                inventario = json.load(f)
        except:
            inventario = {}

        if nombre not in inventario:
            messagebox.showerror("No existe", f"'{nombre}' no está en el inventario.")
            return

        inventario[nombre] = cantidad

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(inventario, f, indent=2)

        self.mostrar_inventario()
        messagebox.showinfo("Inventario actualizado", f"{nombre}: {cantidad} unidades.")

    def volver(self):
        self.destroy()
        self.ventana_anterior.deiconify()

  


if __name__ == "__main__":
    app = StartWindow()
    app.mainloop()
