import customtkinter as ctk

import customtkinter as ctk

class Simple(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg_color="white", fg_color="white")

        # Configuramos las columnas y filas para que se adapten al tamaño del formulario
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  # Columna 2 no se expande
        self.grid_columnconfigure(2, weight=0)  # Columna 3 no se expande

        # Establecer el ancho fijo para las columnas 2 y 3
        self.grid_columnconfigure(2, minsize=500)
        # Configurar las filas para que se expandan y establecer tamaños fijos
        self.grid_rowconfigure(0, minsize=50, weight=0)  # Header con tamaño fijo de 50 px
        self.grid_rowconfigure(1, minsize=120, weight=0)  # Fila 1 se expande
        self.grid_rowconfigure(2, weight=1)  # Fila 2 con tamaño fijo de 120 px
        self.grid_rowconfigure(3, minsize=80, weight=0)  # Fila 3 se expande
        self.grid_rowconfigure(4, minsize=50, weight=0)  # Footer con tamaño fijo de 50 px


        # Header (Fila 0, Columna 0 a 2)
        header_label = ctk.CTkLabel(self, text="Header")
        header_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Fila 1 (Columnas 0 a 2)
        label1 = ctk.CTkLabel(self, text="Label 1")
        label1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        label2 = ctk.CTkLabel(self, text="Label 2")
        label2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        label3 = ctk.CTkLabel(self, text="Label 3")
        label3.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # Fila 2 (Columna 0 a 1 Imagen, Columna 2 Labels)
        image_label = ctk.CTkLabel(self, text="Imagen")
        image_label.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        label4 = ctk.CTkLabel(self, text="Label 4")
        label4.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)

        # Fila 3 (Columnas 0 a 2)
        label5 = ctk.CTkLabel(self, text="Label 5")
        label5.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        label6 = ctk.CTkLabel(self, text="Label 6")
        label6.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
        label7 = ctk.CTkLabel(self, text="Label 7")
        label7.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)

        # Footer (Fila 4, Columna 0 a 2)
        footer_label = ctk.CTkLabel(self, text="Footer")
        footer_label.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
