import customtkinter as ctk
import mysql.connector
import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO
from tkinter import messagebox
import webbrowser

def abrir_vista_recomendaciones(user_id):
    ventana = ctk.CTk()
    ventana.title("Recomendaciones personalizadas")
    ventana.geometry("850x700")

    contenedor = ctk.CTkScrollableFrame(ventana, width=820, height=680)
    contenedor.pack(pady=10, padx=10)

    try:
        response = requests.get(f"http://localhost:5000/recommendations?user_id={user_id}")
        productos = response.json()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las recomendaciones.\n{e}")
        return

    for producto in productos:
        tarjeta = ctk.CTkFrame(contenedor, height=200)
        tarjeta.pack(padx=10, pady=10, fill="x")

        try:
            img_resp = requests.get(producto["image"])
            img = Image.open(BytesIO(img_resp.content)).resize((120, 120))
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(tarjeta, image=img_tk)
            img_label.image = img_tk
            img_label.pack(side="left", padx=10, pady=10)
        except:
            tk.Label(tarjeta, text="[Imagen no disponible]").pack(side="left", padx=10)

        info = ctk.CTkFrame(tarjeta, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(info, text=producto["name"], font=ctk.CTkFont(size=14, weight="bold"), wraplength=600, anchor="w", justify="left").pack(anchor="w")
        
        estrellas = "★" * int(producto.get("rating", 0)) + "☆" * (5 - int(producto.get("rating", 0)))
        reseñas = producto.get("num_ratings", 0)
        ctk.CTkLabel(info, text=f"{estrellas}  ({reseñas} reseñas)", font=ctk.CTkFont(size=12)).pack(anchor="w")

        ctk.CTkLabel(info, text=f"$ {producto['price']:.2f}", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(5, 0))
        ctk.CTkLabel(info, text=f"Precio real: $ {producto.get('actual_price', 0):.2f}", font=ctk.CTkFont(size=12)).pack(anchor="w")

        def abrir_enlace(url=producto["link"]):
            webbrowser.open(url)

        ctk.CTkButton(info, text="Ver producto", command=abrir_enlace).pack(anchor="w", pady=(10, 0))

    ventana.mainloop()

def verificar_credenciales():
    email = entrada_email.get().strip()
    password = entrada_password.get().strip()

    if not email or not password:
        messagebox.showwarning("Campos vacíos", "Por favor, completa ambos campos.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="tienda_online"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            messagebox.showinfo("Bienvenido", f"¡Hola, {usuario['name']}!")
            root.destroy()
            abrir_vista_recomendaciones(usuario['id'])
        else:
            messagebox.showerror("Acceso denegado", "Correo o contraseña incorrectos.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{e}")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Inicio de Sesión")
root.geometry("400x300")

frame = ctk.CTkFrame(root)
frame.pack(padx=40, pady=40, fill="both", expand=True)

ctk.CTkLabel(frame, text="Iniciar Sesión", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 20))
entrada_email = ctk.CTkEntry(frame, placeholder_text="Correo electrónico")
entrada_email.pack(pady=(0, 10), fill="x")
entrada_password = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*")
entrada_password.pack(pady=(0, 20), fill="x")
ctk.CTkButton(frame, text="Iniciar sesión", command=verificar_credenciales).pack()

root.mainloop()