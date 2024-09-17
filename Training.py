from CameraTools import MainCamera
from TrainingTools import Tab1Content,Tab2Content
from PIL import Image, ImageTk
from Global.GlobalV import Img,Inherit
import customtkinter as ctk
import platform, os
import configparser
import ast
class TrainingModelForm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg_color="white", fg_color="white")
        self.saved_image_path = Img.Master
        self.MainPathS()
        self.filters = ["Original","GrayScale", "RedVision", "HighlightShadow", "OnlyLines", "FrontLines", "Negative"]
        self.main_camera = None  # Añadir una referencia para MainCamera
        self.MainTabview()
    def MainPathS(self):
        if platform.system() == "Windows":
            base_path = Img.TempDb  # Cambia esto a la ruta base en Windows
            print('its Windows')
        else:
            base_path = "/ELVIS/TmpDB"  # Cambia esto a la ruta base en Linux
            print('its Linux')

        if not os.path.exists(base_path):
            os.makedirs(base_path)
            print(f"Carpeta base '{base_path}' creada.")

        for folder_name in Img.InTempCreate:
            folder_path = os.path.join(base_path, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Carpeta '{folder_path}' creada.")
            else:
                print(f"Carpeta '{folder_path}' ya existe.")

    def LoadVariables(self):
        # Crear un objeto configparser
        config = configparser.ConfigParser()

        # Leer el archivo .ini
        config.read(Img.LoadAndSaveConfiguration)

        if 'Inspection' in config:
            if 'InspectionData' in config['Inspection']:
                try:
                    Img.InspectionData = ast.literal_eval(config['Inspection']['InspectionData'])
                except:
                    print("Failed to parse InspectionData")
            if 'Inspection' in config['Inspection']:
                inspection_items = config['Inspection']['Inspection'][1:-1].split('},{')
                try:
                    Img.Inspection = [ast.literal_eval(f"{{{item}}}") for item in inspection_items]
                except:
                    print("Failed to parse Inspection")
            if 'InspectionArea' in config['Inspection']:
                try:
                    Img.InspectionArea = ast.literal_eval(config['Inspection']['InspectionArea'])
                except:
                    print("Failed to parse InspectionArea")
            if 'ThresholdFilter' in config['Inspection']:
                try:
                    Img.ThresholdFilter = int(config['Inspection']['ThresholdFilter'])
                except ValueError:
                    print("Invalid integer for ThresholdFilter, keeping default value.")
            if 'Inspection1' in config['Inspection']:
                Img.Inspection1 = config['Inspection']['Inspection1']
            if 'SelectionFilter' in config['Inspection']:
                Img.SelectionFilter = config['Inspection']['SelectionFilter']
        print("Data loaded from ini file")
    def MainTabview(self):
        # Create the Tabview Control
        self.main_tab_control = ctk.CTkTabview(self, fg_color="white", bg_color="white", corner_radius=10)
        self.main_tab_control.pack(padx=10, pady=10, fill="both", expand=True)

        # Display 4 options
        self.tab1 = self.main_tab_control.add(" Step 1 ")
        self.tab2 = self.main_tab_control.add(" Step 2 ")
        self.tab3 = self.main_tab_control.add(" Step 3 ")
        self.tab4 = self.main_tab_control.add(" Step 4 ")

        # Agregar el contenido de la pestaña 1 desde el archivo tab1_content.py
        tab1_content = Tab1Content(self.tab1, self.saved_image_path, MainCamera, self.filters,self.main_tab_control)
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
