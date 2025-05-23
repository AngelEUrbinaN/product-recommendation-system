import customtkinter as ctk
from PIL import Image
import os
import requests
from tkinter import messagebox
import tkinter as tk  
from PIL import Image, ImageTk
from io import BytesIO

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AmazonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Amazon Recomendaciones")
        self.geometry("400x700")
        self.resizable(False, False)
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True)
        self.user_id = None
        
        # Iniciar con la pantalla de login
        self.show_login()
    
    def setup_main_layout(self):
        """Configura el layout principal con barra de búsqueda y footer"""
        # Limpiar el frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Barra superior de búsqueda
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="#232F3E", height=60)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        
        # Logo de Amazon
        logo_label = ctk.CTkLabel(self.header_frame, text="amazon", font=("Arial", 20, "bold"), text_color="white")
        logo_label.pack(side="left", padx=10)
        
        # Campo de búsqueda
        self.search_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Buscar", width=250, height=35)
        self.search_entry.pack(side="left", padx=10, pady=10)
        
        # Botón de búsqueda
        search_button = ctk.CTkButton(
            self.header_frame, 
            text="🔍", 
            width=35, 
            height=35, 
            fg_color="#FEBD69",
            hover_color="#F3A847",
            text_color="black",
            command=self.search_products
        )
        search_button.pack(side="left", padx=(0, 10), pady=10)
        
        # Contenedor para el contenido principal
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.content_frame.pack(fill="both", expand=True)
        
        # Footer
        self.footer_frame = ctk.CTkFrame(self.main_frame, fg_color="#232F3E", height=60)
        self.footer_frame.pack(fill="x", side="bottom")
        self.footer_frame.pack_propagate(False)
        
        # Botones del footer
        home_btn = ctk.CTkButton(
            self.footer_frame, 
            text="Inicio", 
            fg_color="transparent",
            hover_color="#37475A",
            text_color="white",
            command=self.show_home
        )
        home_btn.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        
        history_btn = ctk.CTkButton(
            self.footer_frame, 
            text="Historial", 
            fg_color="transparent",
            hover_color="#37475A",
            text_color="white",
            command=self.show_history
        )
        history_btn.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        
        logout_btn = ctk.CTkButton(
            self.footer_frame, 
            text="Logout", 
            fg_color="transparent",
            hover_color="#37475A",
            text_color="white",
            command=self.logout
        )
        logout_btn.pack(side="left", expand=True, fill="both", padx=2, pady=2)
    
    def show_login(self):
        # Limpiar el frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Frame para centrar el contenido
        login_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        login_frame.pack(pady=80, padx=40, fill="both", expand=True)
        
        # Logo de Amazon
        logo_label = ctk.CTkLabel(login_frame, text="AMAZON", font=("Arial", 36, "bold"), text_color="#232F3E")
        logo_label.pack(pady=(0, 40))
        
        # Entrada para el email
        email_label = ctk.CTkLabel(login_frame, text="Email:", font=("Arial", 14), text_color="#232F3E")
        email_label.pack(anchor="w", pady=(0, 5))
        
        self.email_entry = ctk.CTkEntry(login_frame, placeholder_text="Ingresa tu email", width=320, height=40)
        self.email_entry.pack(pady=(0, 15))
        
        # Entrada para la contraseña
        password_label = ctk.CTkLabel(login_frame, text="Contraseña:", font=("Arial", 14), text_color="#232F3E")
        password_label.pack(anchor="w", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Ingresa tu contraseña", show="•", width=320, height=40)
        self.password_entry.pack(pady=(0, 30))
        
        # Botón de login (amarillo como Amazon)
        login_button = ctk.CTkButton(
            login_frame, 
            text="Login", 
            font=("Arial", 16, "bold"),
            fg_color="#FFD814",
            hover_color="#F7CA00",
            text_color="#000000",
            width=320,
            height=45,
            corner_radius=8,
            command=self.login
        )
        login_button.pack(pady=(0, 20))

        register_button = ctk.CTkButton(
            login_frame, 
            text="Crear cuenta", 
            font=("Arial", 14),
            fg_color="#232F3E",
            hover_color="#37475A",
            text_color="white",
            width=320,
            height=35,
            corner_radius=8,
            command=self.show_register
        )
        register_button.pack(pady=(0, 10))
    
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        try:
            response = requests.post("http://localhost:5000/login", json={"email": email, "password": password})
            if response.status_code == 200:
                data = response.json()
                self.user_id = data["id"]
                self.show_home()
            else:
                messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas.")
        except Exception as e:
            messagebox.showerror("Error de red", f"No se pudo conectar al servidor:\n{e}")

    def show_register(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        register_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        register_frame.pack(pady=80, padx=40, fill="both", expand=True)

        ctk.CTkLabel(register_frame, text="Crear cuenta", font=("Arial", 28, "bold"), text_color="#232F3E").pack(pady=(0, 30))

        name = ctk.CTkEntry(register_frame, placeholder_text="Nombre", width=320, height=40)
        name.pack(pady=(0, 15))
        email = ctk.CTkEntry(register_frame, placeholder_text="Email", width=320, height=40)
        email.pack(pady=(0, 15))
        password = ctk.CTkEntry(register_frame, placeholder_text="Contraseña", show="•", width=320, height=40)
        password.pack(pady=(0, 30))

        def new_user():
            datos = {"name": name.get().strip(),"email": email.get().strip(), "password": password.get().strip()}
            try:
                response = requests.post("http://localhost:5000/registro", json=datos)
                if response.status_code == 200:
                    messagebox.showinfo("Registro exitoso", "Ahora puedes iniciar sesión.")
                    self.show_login()
                else:
                    raise Exception(response.text)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el usuario.\n{e}")

        ctk.CTkButton(
            register_frame,
            text="Registrar",
            fg_color="#FFD814",
            hover_color="#F7CA00",
            text_color="#000000",
            font=("Arial", 16, "bold"),
            width=320,
            height=45,
            command=new_user
        ).pack()

    def show_home(self):
        # Configurar el layout principal
        self.setup_main_layout()
        
        # Limpiar el frame de contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Título de productos recomendados
        title_label = ctk.CTkLabel(
            self.content_frame, 
            text="Productos recomendados para ti", 
            font=("Arial", 18, "bold"), 
            text_color="#232F3E"
        )
        title_label.pack(pady=(20, 15), padx=15, anchor="w")
        
        # Frame con scroll para los productos
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="white")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        try:
            response = requests.get(f"http://localhost:5000/recommendations?user_id={self.user_id}")
            productos = response.json()
            self.display_product_grid(scroll_frame, productos)
        except Exception as e:
            messagebox.showerror("Error de red", f"No se pudieron cargar los productos.\n{e}")
    
    def display_product_grid(self, parent_frame, productos):
        grid_frame = ctk.CTkFrame(parent_frame, fg_color="white")
        grid_frame.pack(fill="both", expand=True)

        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        for i, producto in enumerate(productos):
            row = i // 2
            col = i % 2

            frame = ctk.CTkFrame(grid_frame, fg_color="white", border_width=1, border_color="#DDDDDD", corner_radius=8)
            frame.grid(row=row, column=col, padx=5, pady=10, sticky="nsew")

            frame.bind("<Button-1>", lambda event, prod=producto: self.show_product_detail(prod))

            try:
                img_url = producto["image"]
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content)).resize((140, 140))
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=img_tk)
                img_label.image = img_tk
                img_label.pack()
                img_label.bind("<Button-1>", lambda event, prod=producto: self.show_product_detail(prod))
            except:
                img_label = ctk.CTkLabel(frame, text="Img")
                img_label.pack()
                img_label.bind("<Button-1>", lambda event, prod=producto: self.show_product_detail(prod))

            name_label = ctk.CTkLabel(frame, text=producto["name"], font=("Arial", 12), text_color="#0066C0", wraplength=150)
            name_label.pack(padx=5, anchor="w")
            name_label.bind("<Button-1>", lambda event, prod=producto: self.show_product_detail(prod))
            
            price_label = ctk.CTkLabel(frame, text=f"${producto['price']:.2f}", font=("Arial", 14, "bold"), text_color="#B12704")
            price_label.pack(anchor="w", padx=5)
            price_label.bind("<Button-1>", lambda event, prod=producto: self.show_product_detail(prod))
            
            if producto.get("actual_price"):
                actual_price_label = ctk.CTkLabel(frame, text=f"${producto['actual_price']:.2f}", font=("Arial", 10), text_color="#565959")
                actual_price_label.pack(anchor="w", padx=5)
                actual_price_label.bind("<Button-1>", lambda event, prod=producto: self.show_product_detail(prod))

    
    def show_history(self):
        self.setup_main_layout()

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.content_frame,
            text="Historial de productos vistos",
            font=("Arial", 18, "bold"),
            text_color="#232F3E"
        )
        title.pack(pady=(20, 15), padx=15, anchor="w")

        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="white")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        try:
            response = requests.get(f"http://localhost:5000/history?user_id={self.user_id}")
            productos = response.json()

            if isinstance(productos, dict) and productos.get("error"):
                raise Exception(productos["error"])

            self.display_search_results(scroll_frame, productos)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el historial.\n{e}")

    def search_products(self):
        query = self.search_entry.get().strip()
        if not query:
            return
        self.get_search_results(query)

    
    def get_search_results(self, query):
        # Configurar el layout principal
        self.setup_main_layout()
        
        # Limpiar el frame de contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Título de resultados de búsqueda
        title_label = ctk.CTkLabel(
            self.content_frame, 
            text=f'Resultados para "{query}"', 
            font=("Arial", 18, "bold"), 
            text_color="#232F3E"
        )
        title_label.pack(pady=(20, 15), padx=15, anchor="w")
        
        # Frame con scroll para los productos
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="white")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        try:
            response = requests.get(f"http://localhost:5000/search?query={query}")
            products = response.json()

            if isinstance(products, dict) and products.get("error"):
                raise Exception(products["error"])

            self.display_search_results(scroll_frame, products)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la búsqueda.\n{e}")
    
    def display_search_results(self, parent_frame, products):
        for product in products:
            card = ctk.CTkFrame(parent_frame, fg_color="white", border_width=1, border_color="#CCCCCC", corner_radius=8)
            card.pack(fill="x", padx=10, pady=10)
            card.bind("<Button-1>", lambda event, prod=product: self.show_product_detail(prod))

            content = ctk.CTkFrame(card, fg_color="white")
            content.pack(fill="x", padx=10, pady=10)
            content.bind("<Button-1>", lambda event, prod=product: self.show_product_detail(prod))

            # Imagen
            try:
                img_resp = requests.get(product["image"])
                img = Image.open(BytesIO(img_resp.content)).resize((100, 100))
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(content, image=img_tk)
                img_label.image = img_tk
                img_label.pack(side="left", padx=(0, 10))
                img_label.bind("<Button-1>", lambda event, prod=product: self.show_product_detail(prod))
            except:
                img_label = tk.Label(content, text="[Img]")
                img_label.pack(side="left", padx=(0, 10))
                img_label.bind("<Button-1>", lambda event, prod=product: self.show_product_detail(prod))

            # Info
            info = ctk.CTkFrame(content, fg_color="white")
            info.pack(side="left", fill="both", expand=True)
            info.bind("<Button-1>", lambda event, prod=product: self.show_product_detail(prod))

            name_label = ctk.CTkLabel(info, text=product["name"], font=("Arial", 12), text_color="#0066C0", wraplength=220)
            name_label.pack(anchor="w")
            name_label.bind("<Button-1>", lambda event, prod=product: self.show_product_detail(prod))

            # Rating
            estrellas = "★" * int(product.get("rating", 0)) + "☆" * (5 - int(product.get("rating", 0)))
            rating_label = ctk.CTkLabel(info, text=f"{estrellas}  ({product.get('num_ratings', 0)} reseñas)", font=("Arial", 10))
            rating_label.pack(anchor="w", pady=(5, 0))
            rating_label.bind("<Button-1>", lambda event, prod=product: self.show_product_detail(prod))

            # Precios
            price_label = ctk.CTkLabel(info, text=f"${product['price']:.2f}", font=("Arial", 13, "bold"), text_color="#B12704")
            price_label.pack(anchor="w", pady=(5, 0))
            price_label.bind("<Button-1>", lambda event, prod=product: self.show_product_detail(prod))
            
            if product.get("actual_price"):
                actual_price_label = ctk.CTkLabel(info, text=f"${product['actual_price']:.2f}", font=("Arial", 10), text_color="#565959")
                actual_price_label.pack(anchor="w")
                actual_price_label.bind("<Button-1>", lambda event, prod=product: self.show_product_detail(prod))

    
    def show_product_detail(self, producto):
        self.setup_main_layout()
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="white")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        detail_frame = ctk.CTkFrame(scroll_frame, fg_color="white")
        detail_frame.pack(fill="both", expand=True)

        # Nombre
        ctk.CTkLabel(
            detail_frame,
            text=producto["name"],
            font=("Arial", 18, "bold"),
            text_color="#0F1111",
            wraplength=350,
            justify="left"
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # Rating
        estrellas = "★" * int(producto.get("rating", 0)) + "☆" * (5 - int(producto.get("rating", 0)))
        ctk.CTkLabel(
            detail_frame,
            text=f"{estrellas}  ({producto.get('num_ratings', 0)} reseñas)",
            font=("Arial", 14),
            text_color="#FFA41C"
        ).pack(anchor="w", padx=10, pady=(0, 10))

        # Imagen
        try:
            img_resp = requests.get(producto["image"])
            img = Image.open(BytesIO(img_resp.content)).resize((320, 320))
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(detail_frame, image=img_tk)
            img_label.image = img_tk
            img_label.pack(pady=10)
        except:
            tk.Label(detail_frame, text="[Imagen no disponible]").pack()

        # Precio
        ctk.CTkLabel(
            detail_frame,
            text=f"${producto['price']:.2f}",
            font=("Arial", 24, "bold"),
            text_color="#B12704"
        ).pack(anchor="w", padx=10)
        
        if producto.get("actual_price"):
            ctk.CTkLabel(
                detail_frame,
                text=f"Precio de lista: ${producto['actual_price']:.2f}",
                font=("Arial", 14),
                text_color="#565959"
            ).pack(anchor="w", padx=10)

        buy_btn = ctk.CTkButton(
            detail_frame,
            text="Comprar",
            font=("Arial", 14, "bold"),
            fg_color="#FFD814",
            hover_color="#F7CA00",
            text_color="#000000",
            width=300,
            height=45,
            corner_radius=8,
            command=lambda: self.comprar_producto(producto["id"])
        )
        buy_btn.pack(pady=(20, 10))


        # Sección "Podría interesarte"
        ctk.CTkLabel(
            detail_frame,
            text="Podría interesarte...",
            font=("Arial", 16, "bold"),
            text_color="#0F1111"
        ).pack(anchor="w", padx=10, pady=(20, 10))

        try:
            response = requests.get(f"http://localhost:5000/recommendations_content?product_id={producto['id']}")
            similares = response.json()
            self.create_horizontal_product_ribbon(detail_frame, similares)
        except Exception as e:
            ctk.CTkLabel(detail_frame, text="No se pudieron cargar recomendaciones").pack()

        # Sección "Productos similares"
        ctk.CTkLabel(
            detail_frame,
            text="Productos similares",
            font=("Arial", 16, "bold"),
            text_color="#0F1111"
        ).pack(anchor="w", padx=10, pady=(20, 10))

        try:
            response = requests.get(f"http://localhost:5000/recommendations_image?product_id={producto['id']}")
            similares_imagen = response.json()
            self.create_horizontal_product_ribbon(detail_frame, similares_imagen)
        except Exception as e:
            ctk.CTkLabel(detail_frame, text="No se pudieron cargar similares por imagen").pack()


    def comprar_producto(self, product_id):
        try:
            response = requests.post("http://localhost:5000/compra", json={
                "user_id": self.user_id,
                "product_id": product_id
            })
            if response.status_code == 200:
                messagebox.showinfo("Compra realizada", "¡Producto comprado con éxito!")
            else:
                raise Exception(response.text)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la compra.\n{e}")
    
    def create_horizontal_product_ribbon(self, parent_frame, productos):
        """Crea una cinta horizontal con productos y scroll independiente"""
        # Frame contenedor principal
        container_frame = ctk.CTkFrame(parent_frame, fg_color="white")
        container_frame.pack(fill="x", padx=10, pady=10)

        # Canvas para el scroll
        scroll_canvas = tk.Canvas(container_frame, height=280, bg="white", highlightthickness=0)
        scroll_canvas.pack(fill="x", expand=True, pady=(0, 5))

        # Frame para los productos dentro del canvas
        ribbon_frame = ctk.CTkFrame(scroll_canvas, fg_color="white")
        scroll_window = scroll_canvas.create_window((0, 0), window=ribbon_frame, anchor="nw")

        # Mantener referencias a las imágenes
        if not hasattr(self, 'ribbon_image_refs'):
            self.ribbon_image_refs = []
        image_refs = []
        self.ribbon_image_refs.append(image_refs)

        # Crear tarjetas de productos
        for i, producto in enumerate(productos):
            frame = ctk.CTkFrame(ribbon_frame, fg_color="white", border_width=1,
                                border_color="#DDDDDD", corner_radius=8, width=170, height=260)
            frame.pack(side="left", padx=5, pady=10)
            frame.pack_propagate(False)
            frame.configure(cursor="hand2")

            # Imagen
            try:
                img_url = next((producto[k] for k in ["image", "image_url", "img", "url_image"]
                                if k in producto and producto[k]), None)
                if img_url:
                    img_resp = requests.get(img_url)
                    img = Image.open(BytesIO(img_resp.content)).resize((140, 120))
                    img_tk = ImageTk.PhotoImage(img)
                    image_refs.append(img_tk)
                    img_label = tk.Label(frame, image=img_tk, cursor="hand2", bg="white")
                    img_label.pack(pady=(5, 2))
                    img_label.bind("<Button-1>", lambda e, p=producto: self.show_product_detail(p))
                else:
                    raise ValueError("Sin URL")
            except Exception as e:
                print(f"Error imagen {i}: {e}")
                ctk.CTkLabel(frame, text="Img", width=140, height=120).pack(pady=(5, 2))

            # Nombre
            name = producto.get("name", "") or producto.get("title", "Producto")
            ctk.CTkLabel(
                frame,
                text=name[:25] + "..." if len(name) > 25 else name,
                font=("Arial", 10),
                text_color="#0066C0",
                wraplength=150
            ).pack(pady=(0, 2), padx=5, anchor="w")

            # Rating
            try:
                rating = int(float(producto.get("rating", 0)))
            except:
                rating = 0
            estrellas = "★" * rating + "☆" * (5 - rating)
            ctk.CTkLabel(frame, text=estrellas, font=("Arial", 10), text_color="#FFA41C")\
                .pack(pady=(0, 2), padx=5, anchor="w")

            # Número de reseñas
            try:
                num_ratings = int(producto.get("num_ratings", 0))
            except:
                num_ratings = 0
            ctk.CTkLabel(frame, text=f"({num_ratings})", font=("Arial", 8), text_color="#565959")\
                .pack(pady=(0, 2), padx=5, anchor="w")

            # Precio
            try:
                precio = float(producto.get("price", 0))
                ctk.CTkLabel(frame, text=f"${precio:.2f}", font=("Arial", 12, "bold"), text_color="#B12704")\
                    .pack(pady=(5, 5), padx=5, anchor="w")
            except:
                pass

            # Click en toda la tarjeta
            frame.bind("<Button-1>", lambda e, p=producto: self.show_product_detail(p))

        # Configurar el scroll
        ribbon_frame.update_idletasks()
        scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))
        scroll_canvas.bind("<MouseWheel>", lambda e: scroll_canvas.xview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Funciones de navegación
        def scroll_left():
            scroll_canvas.xview_scroll(-3, "units")

        def scroll_right():
            scroll_canvas.xview_scroll(3, "units")

        nav_frame = ctk.CTkFrame(container_frame, fg_color="white", height=40)
        nav_frame.pack(fill="x")
        
        # Botones para recorrer cintas
        left_btn = ctk.CTkButton(
            nav_frame, 
            text="<", 
            width=40, 
            height=30,
            fg_color="#E0E0E0",
            hover_color="#CCCCCC",
            text_color="black",
            corner_radius=15,
            command=scroll_left
        )
        left_btn.pack(side="left", padx=20)
        
        right_btn = ctk.CTkButton(
            nav_frame, 
            text=">", 
            width=40, 
            height=30,
            fg_color="#E0E0E0",
            hover_color="#CCCCCC",
            text_color="black",
            corner_radius=15,
            command=scroll_right
        )
        right_btn.pack(side="right", padx=20)
    
    def logout(self):
        print("Cerrando sesión...")
        self.show_login()

if __name__ == "__main__":
    app = AmazonApp()
    app.mainloop()