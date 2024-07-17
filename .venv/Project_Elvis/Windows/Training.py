from CameraTools import MainCamera
from TrainingTools import Tab1Content,Tab2Content
import customtkinter as ctk
from PIL import Image, ImageTk
from Global.GlobalV import Img

class TrainingModelForm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg_color="white", fg_color="white")
        self.saved_image_path = Img.Master

        self.filters = ["GrayScale", "RedVision", "HighlightShadow", "OnlyLines", "FrontLines", "Negative"]
        self.main_camera = None  # Añadir una referencia para MainCamera
        self.MainTabview()

    def MainTabview(self):
        # Create the Tabview Control
        main_tab_control = ctk.CTkTabview(self, fg_color="white", bg_color="white", corner_radius=10)
        main_tab_control.pack(padx=10, pady=10, fill="both", expand=True)

        # Display 4 options
        self.tab1 = main_tab_control.add(" Step 1 ")
        self.tab2 = main_tab_control.add(" Step 2 ")
        self.tab3 = main_tab_control.add(" Step 3 ")
        self.tab4 = main_tab_control.add(" Step 4 ")

        # Agregar el contenido de la pestaña 1 desde el archivo tab1_content.py
        tab1_content = Tab1Content(self.tab1, self.saved_image_path, MainCamera, self.filters)
        tab1_content.pack(fill="both", expand=True)

        # Guardar referencia de MainCamera
        self.main_camera = tab1_content.main_camera

        # Agregar texto a cada pestaña principal
        tab2_content = Tab2Content(self.tab2)
        tab2_content.pack(fill="both",expand=True)

        self.add_text_to_tab(self.tab3, "Content of Tab 3")
        self.add_text_to_tab(self.tab4, "Content of Tab 4")

    def add_text_to_tab(self, tab, text):
        label = ctk.CTkLabel(tab, text=text)
        label.pack(pady=10, padx=10)

    def start_camera(self):
        if self.main_camera:
            self.main_camera.start_camera()

    def stop_camera(self):
        if self.main_camera:
            self.main_camera.stop_camera()

if __name__ == "__main__":
    root = ctk.CTk()
    frame = TrainingModelForm(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()