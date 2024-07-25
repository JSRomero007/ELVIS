import customtkinter as ctk

class InnerTab5Content(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="white")

        # Fila 1: Columna 1 a 3 expandida label (header)
        header_label = ctk.CTkLabel(self, text="Header", fg_color="gray")
        header_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Fila 2: Columna 1 label, Columna 2 label, Columna 3 label
        label_2_1 = ctk.CTkLabel(self, text="Label 2.1", fg_color="lightgray")
        label_2_2 = ctk.CTkLabel(self, text="Label 2.2", fg_color="lightgray")
        label_2_3 = ctk.CTkLabel(self, text="Label 2.3", fg_color="lightgray")
        label_2_1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        label_2_2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        label_2_3.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        # Fila 3: Columna 1 y 2 expandida label, Columna 3 controles
        label_3_1_2 = ctk.CTkLabel(self, text="Label 3.1-2", fg_color="lightgray")
        controls_3_3 = ctk.CTkFrame(self, fg_color="lightgray")
        label_3_1_2.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        controls_3_3.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        # Fila 4: Columna 1 y 2 expandida label, Columna 3 label
        label_4_1_2 = ctk.CTkLabel(self, text="Label 4.1-2", fg_color="lightgray")
        label_4_3 = ctk.CTkLabel(self, text="Label 4.3", fg_color="lightgray")
        label_4_1_2.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        label_4_3.grid(row=3, column=2, sticky="nsew", padx=5, pady=5)

        # Fila 5: Columna 1 a 3 expandida label (footer)
        footer_label = ctk.CTkLabel(self, text="Footer", fg_color="gray")
        footer_label.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Configurar las columnas para que se expandan
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        # Configurar las filas para que se expandan y ajustar tamaño de filas 1 y 2
        self.grid_rowconfigure(0, weight=1)  # Fila 1 con peso 2
        self.grid_rowconfigure(1, weight=1)  # Fila 2 con peso 1
        self.grid_rowconfigure(2, weight=2)  # Fila 3
        self.grid_rowconfigure(3, weight=1)  # Fila 4
        self.grid_rowconfigure(4, weight=1)  # Fila 5

        # Empaquetar el frame principal para que ocupe todo el espacio disponible
        self.pack(fill="both", expand=True)

# Ejemplo de uso
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("600x400")

    inner_tab_content = InnerTab5Content(app)
    inner_tab_content.pack(fill="both", expand=True)

    app.mainloop()
