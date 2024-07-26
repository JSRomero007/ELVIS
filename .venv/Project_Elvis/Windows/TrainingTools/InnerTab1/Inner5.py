import customtkinter as ctk

class InnerTab5Content(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="white")

        self.Header()

        self.LblOkZone()
        self.LblNGZone()
        self.TitleMenu()
        self.MainArea()

        self.ButtonsArea()
        self.Footer()

        # Configurar las columnas para que se expandan
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  # Columna 2 no se expande
        self.grid_columnconfigure(2, weight=0)  # Columna 3 no se expande

        # Establecer el ancho fijo para las columnas 2 y 3
        self.grid_columnconfigure(2, minsize=500)

        # Configurar las filas para que se expandan y establecer tamaños fijos
        self.grid_rowconfigure(0, minsize=50, weight=0)  # Header con tamaño fijo de 50 px
        self.grid_rowconfigure(1, minsize=120, weight=0)  # Fila 1 se expande
        self.grid_rowconfigure(2, weight=1)  # Fila 2 con tamaño fijo de 120 px
        self.grid_rowconfigure(3, weight=1)  # Fila 3 se expande
        self.grid_rowconfigure(4, minsize=50, weight=0)  # Footer con tamaño fijo de 50 px

        # Empaquetar el frame principal para que ocupe todo el espacio disponible
        self.pack(fill="both", expand=True)

    def Header(self):
        # Fila 1: Columna 1 a 3 expandida label (header)
        header_label = ctk.CTkLabel(self, text="- Clasification -", fg_color="white", font=('Consolas', 20), text_color="black")
        header_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
    def LblOkZone(self):
        label_2_1 = ctk.CTkLabel(self, text="Label 2.1", fg_color="lightgray")
        label_2_1.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=5, pady=5)
    def LblNGZone(self):
        label_2_2 = ctk.CTkLabel(self, text="Label 2.2", fg_color="lightgray")
        label_2_2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    def MainArea(self):
        label_3_1_2 = ctk.CTkLabel(self, text="Label 3.1-2", fg_color="lightgray")
        label_3_1_2.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    def TitleMenu(self):
        label_2_3 = ctk.CTkLabel(self, text="Label 2.3", fg_color="lightgray")
        label_2_3.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
    def ButtonsArea(self):

        controls_3_3 = ctk.CTkFrame(self, fg_color="lightgray")
        controls_3_3.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
        button_frame = ctk.CTkFrame(self, fg_color="lightgray")
        button_frame.grid(row=3, column=2, sticky="nsew", padx=5, pady=5)

        # Crear los botones dentro del frame
        button_1 = ctk.CTkButton(button_frame, text="Back")
        button_2 = ctk.CTkButton(button_frame, text="Next step")

        # Colocar los botones en el frame
        button_1.pack(side="left", padx=5, pady=5)
        button_2.pack(side="right", padx=5, pady=5)
    def Footer(self):
        footer_label = ctk.CTkLabel(self, text="Footer", fg_color="gray")
        footer_label.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)




# Ejemplo de uso
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("600x400")

    inner_tab_content = InnerTab5Content(app)
    inner_tab_content.pack(fill="both", expand=True)

    app.mainloop()
