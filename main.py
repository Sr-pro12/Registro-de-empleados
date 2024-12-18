import tkinter as tk
from tkinter import ttk
import sqlite3
import csv
from modulos import es_telefono_valido, es_sueldo_valido, es_email_valido, leer_datos_db
from tkinter import messagebox

def crear_tabla():
    """Crea la tabla en la base de datos si no existe."""
    try:
        conexion = sqlite3.connect("empleados.db")
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                telefono TEXT,
                email TEXT,
                sueldo REAL,
                antiguedad INTEGER,
                direccion TEXT
            )
        """)
        conexion.commit()
        conexion.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al crear la tabla: {e}")

def agregar_empleado():
    """Agrega un nuevo empleado a la base de datos, validando los datos primero."""
    nombre = nombre_entry.get()
    telefono = telefono_entry.get()
    email = email_entry.get()
    sueldo = sueldo_entry.get()
    antiguedad = antiguedad_entry.get()
    direccion = direccion_entry.get()

    if not nombre or not telefono or not email or not sueldo or not antiguedad or not direccion:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        return

    if not es_sueldo_valido(sueldo):
        return
    if not es_telefono_valido(telefono):
        return
    if not es_email_valido(email):
        return
    try:
        conexion = sqlite3.connect("empleados.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO empleados (nombre, telefono, email, sueldo, antiguedad, direccion) VALUES (?, ?, ?, ?, ?, ?)",
                       (nombre_entry.get(), telefono_entry.get(), email_entry.get(), sueldo_entry.get(), antiguedad_entry.get(), direccion_entry.get()))
        conexion.commit()
        conexion.close()
        actualizar_treeview()
        limpiar_campos()
        messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error al agregar empleado: {error}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para Sueldo y Antigüedad.")

def actualizar_empleado():
    """Actualiza la información de un empleado existente."""
    try:
        seleccion = tree.selection()
        if seleccion:
            id_empleado = tree.item(seleccion)['values'][0]
            conexion = sqlite3.connect("empleados.db")
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE empleados SET nombre=?, telefono=?, email=?, sueldo=?, antiguedad=?, direccion=? WHERE id=?
            """, (nombre_entry.get(), telefono_entry.get(), email_entry.get(), sueldo_entry.get(), antiguedad_entry.get(), direccion_entry.get(), id_empleado))
            conexion.commit()
            conexion.close()
            actualizar_treeview()
            limpiar_campos()
            messagebox.showinfo("Éxito", "Empleado actualizado correctamente.")
        else:
             messagebox.showwarning("Advertencia", "Selecciona un empleado para actualizar.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al actualizar empleado: {e}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para Sueldo y Antigüedad.")

def eliminar_empleado():
    """Elimina un empleado de la base de datos."""
    seleccion = tree.selection()
    if seleccion:
        id_empleado = tree.item(seleccion)['values'][0]
        try:
            conexion = sqlite3.connect("empleados.db")
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM empleados WHERE id=?", (id_empleado,))
            conexion.commit()
            conexion.close()
            actualizar_treeview()
            limpiar_campos()
            messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar empleado: {e}")
    else:
        messagebox.showwarning("Advertencia", "Selecciona un empleado para eliminar.")

def exportar_csv():
    """Exporta los datos a un archivo CSV."""
    try:
        conexion = sqlite3.connect("empleados.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM empleados")
        datos = cursor.fetchall()
        conexion.close()

        with open("empleados.csv", "w", newline="", encoding="utf-8") as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow(["ID", "Nombre", "Teléfono", "Email", "Sueldo", "Antigüedad", "Dirección"])  # Encabezado
            escritor_csv.writerows(datos)

        messagebox.showinfo("Éxito", "Datos exportados a empleados.csv")
    except Exception as e:
         messagebox.showerror("Error", f"Error al exportar a CSV: {e}")

def actualizar_treeview():
    """Actualiza el Treeview con los datos de la base de datos."""
    datos = leer_datos_db("empleados.db")
    try:
        conexion = sqlite3.connect("empleados.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM empleados")
        datos = cursor.fetchall()
        conexion.close()

        tree.delete(*tree.get_children())

        # Configurar estilos para las filas alternadas
        tree.tag_configure('oddrow', background='white')  # Color para filas impares
        tree.tag_configure('evenrow', background='#e0c4f1')  # Color para filas pares (violeta claro)

        for i, fila in enumerate(datos):
            if i % 2 == 0:  # Si el índice es par
                tree.insert("", "end", values=fila, tags=('evenrow',))
            else:  # Si el índice es impar
                tree.insert("", "end", values=fila, tags=('oddrow',))
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error al actualizar Treeview: {error}")

def seleccionar_empleado(event):
    """Carga los datos del empleado seleccionado en los campos de entrada."""
    seleccion = tree.selection()
    if seleccion:
        item = tree.item(seleccion)
        valores = item['values']
        if valores: #verifica que valores no este vacio
            nombre_entry.delete(0, tk.END)
            nombre_entry.insert(0, valores[1])
            telefono_entry.delete(0, tk.END)
            telefono_entry.insert(0, valores[2])
            email_entry.delete(0, tk.END)
            email_entry.insert(0, valores[3])
            sueldo_entry.delete(0, tk.END)
            sueldo_entry.insert(0, valores[4])
            antiguedad_entry.delete(0, tk.END)
            antiguedad_entry.insert(0, valores[5])
            direccion_entry.delete(0, tk.END)
            direccion_entry.insert(0, valores[6])

def limpiar_campos():
    """Limpia los campos de entrada."""
    nombre_entry.delete(0, tk.END)
    telefono_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    sueldo_entry.delete(0, tk.END)
    antiguedad_entry.delete(0, tk.END)
    direccion_entry.delete(0, tk.END)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Empleados")
ventana.config(bg="#b289cd")
ventana.geometry("1458x550")
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("TLabel", font=("Arial", 10))
estilo.configure("TButton", padding=5)

# Frames para agrupar elementos
estilo = ttk.Style()
estilo.configure("MyFrame.TFrame", background="#b289cd")

frame_entradas = ttk.Frame(ventana, style="MyFrame.TFrame", padding=10)
frame_entradas.grid(row=0, column=0, sticky=(tk.W, tk.E))

frame_botones = ttk.Frame(ventana, style="MyFrame.TFrame", padding=10)
frame_botones.grid(row=1, column=0, sticky=(tk.W, tk.E))

frame_bd = ttk.Frame(ventana, style="MyFrame.TFrame", padding=10)
frame_bd.grid(row=2, column=0, sticky=(tk.W, tk.E))

# Creación de la base de datos y la tabla
crear_tabla()

# Etiquetas y campos de entrada
nombre_label = ttk.Label(frame_entradas, text="Nombre Completo:").grid(row=0, column=0, pady=5)
nombre_entry = ttk.Entry(frame_entradas)
nombre_entry.grid(row=0, column=1, pady=5)

telefono_label = ttk.Label(frame_entradas, text="Teléfono:").grid(row=1, column=0, pady=5)
telefono_entry = ttk.Entry(frame_entradas)
telefono_entry.grid(row=1, column=1, pady=5)

email_label = ttk.Label(frame_entradas, text="Email:").grid(row=2, column=0, pady=5)
email_entry = ttk.Entry(frame_entradas)
email_entry.grid(row=2, column=1, pady=5)

sueldo_label = ttk.Label(frame_entradas, text="Sueldo:").grid(row=3, column=0, pady=5)
sueldo_entry = ttk.Entry(frame_entradas)
sueldo_entry.grid(row=3, column=1, pady=5)

antiguedad_label = ttk.Label(frame_entradas, text="Años en la Empresa:").grid(row=4, column=0, pady=5)
antiguedad_entry = ttk.Entry(frame_entradas)
antiguedad_entry.grid(row=4, column=1, pady=5)

direccion_label = ttk.Label(frame_entradas, text="Dirección:").grid(row=5, column=0, pady=5)
direccion_entry = ttk.Entry(frame_entradas)
direccion_entry.grid(row=5, column=1, pady=5)

# Botones de acción
agregar_button = ttk.Button(frame_botones, text="Agregar", command=agregar_empleado).grid(row=0, column=0, pady=5)
actualizar_button = ttk.Button(frame_botones, text="Actualizar", command=actualizar_empleado).grid(row=0, column=1, pady=5)
eliminar_button = ttk.Button(frame_botones, text="Eliminar", command=eliminar_empleado).grid(row=0, column=2, pady=5)
exportar_button = ttk.Button(frame_botones, text="Exportar a CSV", command=exportar_csv).grid(row=0, column=3, pady=5)

# Treeview para mostrar los datos
tree = ttk.Treeview(frame_bd, columns=("ID", "Nombre", "Teléfono", "Email", "Sueldo", "Antigüedad", "Dirección"), show="headings")

tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Teléfono", text="Teléfono")
tree.heading("Email", text="Email")
tree.heading("Sueldo", text="Sueldo")
tree.heading("Antigüedad", text="Años")
tree.heading("Dirección", text="Dirección")
tree.grid(row=10, column=0, padx=10, pady=10)

# Barra de desplazamiento para el Treeview
tree_scrollbar_y = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
tree_scrollbar_y.grid(row=2, column=1, sticky='ns')
tree.configure(yscrollcommand=tree_scrollbar_y.set)

tree_scrollbar_x = ttk.Scrollbar(ventana, orient="horizontal", command=tree.xview)
tree_scrollbar_x.grid(row=11, column=0, columnspan=2, sticky='ew')
tree.configure(xscrollcommand=tree_scrollbar_x.set)

# Enlazar el evento de selección del Treeview
tree.bind("<<TreeviewSelect>>", seleccionar_empleado)

# Llenar el Treeview al iniciar la aplicación
actualizar_treeview()

ventana.mainloop()