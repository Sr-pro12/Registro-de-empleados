import re
from tkinter import messagebox
import sqlite3

def es_sueldo_valido(sueldo_str):
    """Verifica si el sueldo ingresado es válido."""
    try:
        sueldo = float(sueldo_str)  # Intenta convertir a float (permite decimales)
        if sueldo >= 0:
            return True
        else:
            messagebox.showwarning("Advertencia", "El sueldo debe ser un número positivo.")
            return False
    except ValueError:
        messagebox.showwarning("Advertencia", "Ingrese un valor numérico válido para el sueldo.")
        return False

def es_telefono_valido(telefono_str):
    """Verifica si el teléfono ingresado tiene un formato válido usando una expresión regular."""
    patron = r"^\+?[0-9]{11,}$"  # Acepta un signo + opcional al inicio y al menos 11 dígitos
    if re.match(patron, telefono_str):
        return True
    else:
        messagebox.showwarning("Advertencia", "Ingrese un número de teléfono válido (ej: (+58)4140000000 o 04140000000).")
        return False
    

def es_email_valido(email_str):
    """Verifica si el email ingresado tiene un formato válido usando una expresión regular."""
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(patron, email_str):
        return True
    else:
        messagebox.showwarning("Advertencia", "Ingrese un correo electrónico válido (ej: usuario@dominio.com).")
        return False
    
def leer_datos_db(nombre_db, tabla="empleados"):
    """Lee datos desde una base de datos SQLite y devuelve una lista de tuplas."""
    try:
        conexion = sqlite3.connect(nombre_db)
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM {tabla}")
        datos = cursor.fetchall()
        conexion.close()
        return datos
    except sqlite3.Error as e:
        print(f"Error al leer la base de datos: {e}")
        return None