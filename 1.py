import tkinter as tk
from tkinter import messagebox
import os

DATA_FILE = "inventario URIBE.txt"

def cargar_datos():
    datos = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            for line in file:
                try:
                    producto, cantidad = line.strip().split(":")
                    datos[producto.strip()] = int(cantidad.strip())
                except ValueError:
                    pass
    return datos

def guardar_datos(datos):
    with open(DATA_FILE, "w") as file:
        for producto, cantidad in datos.items():
            file.write(f"{producto}:{cantidad}\n")

def actualizar_inventario(nombre_producto, cantidad, operacion):
    datos = cargar_datos()
    if operacion == "compra":
        datos[nombre_producto] = datos.get(nombre_producto, 0) + cantidad
    elif operacion == "venta":
        if nombre_producto in datos:
            if cantidad > datos[nombre_producto]:
                messagebox.showerror("Error", "Cantidad de venta mayor que el inventario disponible.")
                return
            datos[nombre_producto] -= cantidad
            if datos[nombre_producto] <= 0:
                del datos[nombre_producto]
        else:
            messagebox.showerror("Error", "El producto no está en el inventario.")
            return
    guardar_datos(datos)
    messagebox.showinfo("Éxito", f"{operacion.capitalize()} realizada correctamente.")

def mostrar_inventario():
    datos = cargar_datos()
    inventario = "\n".join(f"{producto}: {cantidad}" for producto, cantidad in datos.items())
    if not inventario:
        inventario = "El inventario está vacío."
    messagebox.showinfo("Inventario", inventario)

def manejar_accion(accion):
    nombre_producto = entry_producto.get().strip()
    try:
        cantidad = int(entry_cantidad.get().strip())
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Cantidad no válida. Debe ser un número entero positivo.")
        return
    actualizar_inventario(nombre_producto, cantidad, accion)
    entry_producto.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)

root = tk.Tk()
root.title("Gestión de Inventario")
root.geometry("500x300")  
root.minsize(500, 300)  
frame = tk.Frame(root, bg="#e6e6fa", padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)  

tk.Label(frame, text="Nombre del Producto", bg="#e6e6fa", font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky="e")
entry_producto = tk.Entry(frame, font=("Arial", 12))
entry_producto.grid(row=0, column=1, pady=5, padx=10, sticky="ew")

tk.Label(frame, text="Cantidad", bg="#e6e6fa", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="e")
entry_cantidad = tk.Entry(frame, font=("Arial", 12))
entry_cantidad.grid(row=1, column=1, pady=5, padx=10, sticky="ew")


btn_agregar_compra = tk.Button(frame, text="Agregar Compra", command=lambda: manejar_accion('compra'), font=("Arial", 12), bg="#98c6e4", padx=10, pady=5)
btn_agregar_compra.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

btn_agregar_venta = tk.Button(frame, text="Agregar Venta", command=lambda: manejar_accion('venta'), font=("Arial", 12), bg="#98c6e4", padx=10, pady=5)
btn_agregar_venta.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

btn_mostrar_inventario = tk.Button(frame, text="Mostrar Inventario", command=mostrar_inventario, font=("Arial", 12), bg="#98c6e4", padx=10, pady=5)
btn_mostrar_inventario.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

frame.columnconfigure(1, weight=1)

root.mainloop()
