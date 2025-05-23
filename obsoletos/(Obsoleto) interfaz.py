import tkinter as tk
from tkinter import messagebox
import requests

def obtener_recomendaciones():
    try:
        user_id = int(entry_usuario.get())
        url = f"http://localhost:5000/recommendations?user_id={user_id}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(response.json().get('error', 'Error desconocido'))

        productos = response.json()
        texto_resultado.delete("1.0", tk.END)

        if not productos:
            texto_resultado.insert(tk.END, "No se encontraron recomendaciones para este usuario.")
            return

        for p in productos:
            texto_resultado.insert(tk.END, f"{p['name']} - ${p['price']}\n{p['description']}\n\n")

    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce un ID válido.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener recomendaciones.\n{e}")

ventana = tk.Tk()
ventana.title("Sistema de Recomendación")
ventana.geometry("600x400")

tk.Label(ventana, text="ID de usuario:").pack(pady=10)
entry_usuario = tk.Entry(ventana)
entry_usuario.pack()

tk.Button(ventana, text="Obtener Recomendaciones", command=obtener_recomendaciones).pack(pady=10)

texto_resultado = tk.Text(ventana, wrap="word", height=15)
texto_resultado.pack(padx=10, pady=10, fill="both", expand=True)

ventana.mainloop()
