import json
import os

class GestorJSON:
    @staticmethod
    def cargar_datos(archivo):
        try:
            print(f"\nIntentando abrir: {archivo}")
            print(f"Ruta absoluta: {os.path.abspath(archivo)}")
            print(f"¿Existe el archivo? {os.path.exists(archivo)}")
            
            with open(archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"Contenido cargado: {data[:50]}...")
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"¡Error cargando {archivo}! {str(e)}")
            # Retorna estructura vacía según el tipo de archivo
            if "inventario" in archivo:
                return {}
            return []

    @staticmethod
    def guardar_datos(archivo, datos):
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            print(f"Datos guardados correctamente en {archivo}")
        except Exception as e:
            print(f"Error guardando {archivo}: {str(e)}")

