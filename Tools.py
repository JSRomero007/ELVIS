from  Window_Tools.General import General
from  Window_Tools.IO import Io
from  Window_Tools.Ethernet import Ethernet

import customtkinter as ctk

class ToolsForm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg_color="white", fg_color="white")
        label = ctk.CTkLabel(self, text="Tools",font=("Consolas",20))
        label.pack(padx=10, pady=10)
        self.TabControl()

    def TabControl(self):
        # Crear un CTkTabview
        tabview = ctk.CTkTabview(self, width=400, height=300)
        tabview.pack(expand=True, fill="both")
        tabview.configure(fg_color="white",text_color="Black",segmented_button_fg_color="White", segmented_button_selected_color="lightgrey")
        tabview.add("General")
        tabview.add("IO")
        tabview.add("Ethernet")

        # Obtener los marcos de las pestañas para agregar contenido
        tab1_frame = tabview.tab("General")
        tab2_frame = tabview.tab("IO")
        tab3_frame = tabview.tab("Ethernet")
        
        # Configurar colores de los botones segmentados
        for tab in tabview._segmented_button._buttons_dict.values():
            tab.configure(text_color="black", font=("Arial", 12, "bold"))

        #Display Forms
        my_form = Ethernet(tabview.tab("General"))
        my_form.pack(expand=1, fill="both")


if __name__ == "__main__":
    app = ctk.CTk()  # Crea la ventana principal
    app.geometry("400x300")
    tools_form = ToolsForm(app)  # Crea una instancia de ToolsForm
    tools_form.pack(expand=True, fill='both')  # Agrega el ToolsForm a la ventana principal

    app.mainloop()  # Inicia el bucle principal de la aplicación