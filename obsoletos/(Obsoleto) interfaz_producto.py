import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

producto = {
    "name": "Samsung LC24F390FHLXZ - Monitor Curvo, Negro, 23.5”",
    "image": "https://m.media-amazon.com/images/I/911TGUbnayL._AC_SL1500_.jpg",
    "rating": 4.5,
    "num_ratings": 8887,
    "price": 2099.00,
    "actual_price": 2999.00,
    "link": "https://www.amazon.com/dp/B0BHZJW94Y"
}

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Producto recomendado")
root.geometry("800x300")

frame = ctk.CTkFrame(root, width=780, height=280, corner_radius=10)
frame.pack(pady=10, padx=10, fill="both", expand=True)

try:
    response = requests.get(producto["image"])
    img_data = Image.open(BytesIO(response.content)).resize((150, 150))
    img_tk = ImageTk.PhotoImage(img_data)
    label_img = tk.Label(frame, image=img_tk)
    label_img.image = img_tk
    label_img.pack(side="left", padx=10, pady=10)
except:
    label_img = tk.Label(frame, text="[Imagen no disponible]")
    label_img.pack(side="left", padx=10, pady=10)

info_frame = ctk.CTkFrame(frame, fg_color="transparent")
info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

label_name = ctk.CTkLabel(info_frame, text=producto["name"], font=ctk.CTkFont(size=16, weight="bold"), wraplength=600, anchor="w", justify="left")
label_name.pack(anchor="w")

estrellas = "★" * int(producto["rating"]) + "☆" * (5 - int(producto["rating"]))
label_rating = ctk.CTkLabel(info_frame, text=f"{estrellas}  ({producto['num_ratings']} reseñas)", font=ctk.CTkFont(size=14))
label_rating.pack(anchor="w", pady=(5, 0))

label_price = ctk.CTkLabel(info_frame, text=f"$ {producto['price']:.2f}", font=ctk.CTkFont(size=16, weight="bold"))
label_price.pack(anchor="w", pady=(10, 0))

label_price_real = ctk.CTkLabel(info_frame, text=f"Precio real: $ {producto['actual_price']:.2f}", font=ctk.CTkFont(size=12, slant="italic"))
label_price_real.pack(anchor="w")

def abrir_enlace():
    webbrowser.open(producto["link"])

boton = ctk.CTkButton(info_frame, text="Ver producto", command=abrir_enlace)
boton.pack(anchor="w", pady=(15, 0))

root.mainloop()
