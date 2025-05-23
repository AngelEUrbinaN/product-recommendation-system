import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Menú Principal")
root.geometry("420x750")

# Datos de prueba
productos = [
    {
        "name": "Monitor Samsung 24” Curvo",
        "image": "https://m.media-amazon.com/images/I/81WSct4U7GL._AC_UL320_.jpg",
        "price": 2099.0,
        "actual_price": 2599.0
    },
    {
        "name": "Mouse Logitech Inalámbrico",
        "image": "https://m.media-amazon.com/images/I/61LtuGzXeaL._AC_UL320_.jpg",
        "price": 499.0,
        "actual_price": 699.0
    },
    {
        "name": "Teclado Mecánico Redragon",
        "image": "https://m.media-amazon.com/images/I/71cngYX2yaL._AC_UL320_.jpg",
        "price": 1299.0,
        "actual_price": 1599.0
    },
] * 7

frame_top = ctk.CTkFrame(root, height=50, fg_color="white")
frame_top.pack(fill="x")

entry_busqueda = ctk.CTkEntry(frame_top, placeholder_text="Buscar")
entry_busqueda.pack(padx=10, pady=10, fill="x")

frame_scroll = ctk.CTkScrollableFrame(root, fg_color="white", width=400, height=600)
frame_scroll.pack(fill="both", expand=True)

titulo = ctk.CTkLabel(frame_scroll, text="Productos recomendados para ti", font=ctk.CTkFont(size=18, weight="bold"))
titulo.grid(row=0, column=0, columnspan=2, pady=(10, 20), padx=10, sticky="w")

row = 1
col = 0

for producto in productos[:20]:
    card = ctk.CTkFrame(frame_scroll, width=180, height=230, fg_color="#f5f5f5", corner_radius=10)
    card.grid(row=row, column=col, padx=10, pady=10)
    card.grid_propagate(False)

    try:
        response = requests.get(producto["image"])
        img = Image.open(BytesIO(response.content)).resize((140, 100))
        img_tk = ImageTk.PhotoImage(img)
        lbl_img = tk.Label(card, image=img_tk)
        lbl_img.image = img_tk
        lbl_img.pack(pady=5)
    except:
        tk.Label(card, text="[Imagen]").pack()

    ctk.CTkLabel(card, text=producto["name"], font=ctk.CTkFont(size=12), wraplength=160).pack()

    precio_frame = tk.Frame(card, bg="#f5f5f5")
    precio_frame.pack(pady=5)
    tk.Label(precio_frame, text=f"${producto['price']:.2f}", font=("Arial", 12, "bold"), fg="green", bg="#f5f5f5").pack(side="left")
    tk.Label(precio_frame, text=f"${producto['actual_price']:.2f}", font=("Arial", 10, "overstrike"), fg="gray", bg="#f5f5f5", padx=5).pack(side="left")

    col += 1
    if col > 1:
        col = 0
        row += 1

frame_footer = ctk.CTkFrame(root, height=60, fg_color="#e6e6e6")
frame_footer.pack(fill="x")

ctk.CTkButton(frame_footer, text="Inicio").pack(side="left", expand=True, padx=10, pady=10)
ctk.CTkButton(frame_footer, text="Historial").pack(side="left", expand=True, padx=10, pady=10)
ctk.CTkButton(frame_footer, text="Logout").pack(side="left", expand=True, padx=10, pady=10)

root.mainloop()
