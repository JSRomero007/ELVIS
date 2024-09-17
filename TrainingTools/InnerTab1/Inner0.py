import customtkinter as ctk
from Global.GlobalV import Img, Cam
from CameraTools import CameraHandler
import xml.etree.ElementTree as ET
import os

class InnerTab0Content(ctk.CTkFrame):
    def __init__(self, parent,inner_tab_control):
        super().__init__(parent)
        self.inner_tab_control = inner_tab_control
        self.configure(bg_color="white", fg_color="white")

        # Configurar las columnas y filas para que se expandan
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, minsize=50, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, minsize=50, weight=0)

        # Crear la interfaz primero
        self.create_layout()

        # Cargar la configuración desde el XML después de crear la interfaz
        self.load_configuration()

    def create_layout(self):
        self.Header()
        self.Data()
        self.BackNext()
        self.MainArea()
        self.Footer()

    def Header(self):
        header_label = ctk.CTkLabel(self, text="- Setup -", fg_color="white", font=('Consolas', 25), text_color="black")
        header_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    def MainArea(self):
        # Crear un frame principal para MainArea en el lado derecho
        MainFrame = ctk.CTkFrame(self, fg_color="white")
        MainFrame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Lista para almacenar las referencias a los botones "View", etiquetas de Configuration y Light
        self.view_buttons = []
        self.status_checkboxes = []
        self.config_labels = []  # Lista para almacenar las etiquetas de Configuration
        self.light_labels = []  # Lista para almacenar las etiquetas de Light

        # Configurar el grid dentro del MainFrame para que también se expanda
        MainFrame.grid_rowconfigure(0, weight=0)
        MainFrame.grid_rowconfigure(1, weight=0)
        for i in range(2, 6):
            MainFrame.grid_rowconfigure(i, weight=1, minsize=50)  # Tamaño mínimo de las filas

        for j in range(5):
            MainFrame.grid_columnconfigure(j, weight=1, minsize=120)  # Tamaño mínimo de las columnas

        # Título
        title_label = ctk.CTkLabel(MainFrame, text="Configuration Cameras", font=('Consolas', 20), text_color="black")
        title_label.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

        # Encabezados de las columnas
        headers = ["Camera", "Status", "Configuration", "Light", "View"]
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(MainFrame, text=header, fg_color="gray", text_color="black",
                                        font=('Consolas', 15, 'bold'))
            header_label.grid(row=1, column=col, sticky="nsew", padx=5, pady=5)

        # Crear la tabla de 4 filas y 5 columnas
        for row in range(2, 6):
            camera_label = ctk.CTkLabel(MainFrame, text=str(row - 1), fg_color="white", text_color="black")
            camera_label.grid(row=row, column=0, sticky="nsew", padx=5, pady=5)

            status_var = ctk.IntVar()
            status_checkbox = ctk.CTkCheckBox(MainFrame, variable=status_var, text="",
                                              command=lambda r=row, v=status_var: self.checkbox_status(r, v))
            status_checkbox.grid(row=row, column=1, sticky="nsew", padx=5, pady=5)

            # Etiqueta de Configuration
            config_label = ctk.CTkLabel(MainFrame, text="Config", fg_color="lightgray", text_color="black")
            config_label.grid(row=row, column=2, sticky="nsew", padx=5, pady=5)
            self.config_labels.append(config_label)  # Guardar la referencia

            # Etiqueta de Light
            light_label = ctk.CTkLabel(MainFrame, text="Light Info", fg_color="lightgray", text_color="black")
            light_label.grid(row=row, column=3, sticky="nsew", padx=5, pady=5)
            self.light_labels.append(light_label)  # Guardar la referencia

            view_button = ctk.CTkButton(MainFrame, text="View", width=80, height=30,
                                        command=lambda r=row: self.show_button_location(r),
                                        fg_color="gray", hover_color="gray")
            view_button.grid(row=row, column=4, sticky="nsew", padx=5, pady=5)
            view_button.configure(state="disabled")  # Deshabilitar por defecto

            # Almacenar el botón y el checkbox para poder habilitar/deshabilitar más tarde
            self.view_buttons.append(view_button)
            self.status_checkboxes.append(status_checkbox)

    def checkbox_status(self, row, status_var):
        status = "Enabled" if status_var.get() else "Disabled"
        print(f"Checkbox in row {row} is {status}")

        # Actualizar el estado del checkbox
        if status_var.get():
            self.view_buttons[row - 2].configure(state="normal", fg_color="#FE5200", hover_color="#FE5202")
            self.status_checkboxes[row - 2].configure(fg_color="#FE5202")
        else:
            self.view_buttons[row - 2].configure(state="disabled", fg_color="gray", hover_color="gray")
            self.status_checkboxes[row - 2].configure(fg_color="gray")

        # Guardar el estado en el archivo XML
        self.save_configuration(row)

    def show_button_location(self, row):
        print(f"Button pressed in row {row-1}")
        Img.Camera1=row-1
        Cam.id=Img.Camera1

        # Cargar datos del XML para la cámara seleccionada
        self.load_cam_configuration(row - 1)

        #row-1 save this info
        self.inner_tab_control.set("Adjust the camera")
        print(Cam.id)
        #print(Cam.id)

    def load_cam_configuration(self, cam_id):
        xml_path = "C:\\ELVIS\\TmpDB\\003_Configuration\\TempConfiguration.xml"  # Ruta del archivo XML
        if os.path.exists(xml_path):
            tree = ET.parse(xml_path)
            root = tree.getroot()

            cam_element = root.find(f'Cam{cam_id}')  # Ajustar al índice de la cámara

            if cam_element is not None:
                # Asignar valores a las variables de Cam
                Cam.StatusLight = True if cam_element.find('Light').text == 'True' else False
                Cam.LightConfiguration = cam_element.find('LightConfig').text
                Cam.Tool = cam_element.find('Tool').text if cam_element.find('Tool').text is not None else ""
                Cam.InspectionArea = cam_element.find('InspectionArea').text
                Cam.CloseContourns = True if cam_element.find('CloseContourns').text == 'True' else False
                Cam.Umbral = int(cam_element.find('Umbral').text)
                Cam.MinContourn = int(cam_element.find('MinContourn').text)
                Cam.MaxContourn = int(cam_element.find('MaxContourn').text)
                Cam.ValueContorn = int(cam_element.find('ValueContorn').text)
                Cam.Invert = True if cam_element.find('Invert').text == 'True' else False

                # Imprimir los valores para verificar
                print(f"Light Status: {Cam.StatusLight}")
                print(f"Light Configuration: {Cam.LightConfiguration}")
                print(f"Tool: {Cam.Tool}")
                print(f"Inspection Area: {Cam.InspectionArea}")
                print(f"Close Contourns: {Cam.CloseContourns}")
                print(f"Umbral: {Cam.Umbral}")
                print(f"Min Contourn: {Cam.MinContourn}")
                print(f"Max Contourn: {Cam.MaxContourn}")
                print(f"Value Contorn: {Cam.ValueContorn}")
                print(f"Invert: {Cam.Invert}")
            else:
                print(f"Error: No se encontró la configuración para la cámara {cam_id + 1}")
        else:
            print(f"Error: No se encuentra el archivo XML en {xml_path}")
    def Data(self):
        data_frame = ctk.CTkFrame(self, fg_color="white")
        data_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        data_frame.grid_rowconfigure(0, weight=0)
        data_frame.grid_rowconfigure(1, weight=0)
        data_frame.grid_rowconfigure(2, weight=0)
        data_frame.grid_rowconfigure(3, weight=0)
        data_frame.grid_rowconfigure(4, weight=0)
        data_frame.grid_rowconfigure(5, weight=0)
        data_frame.grid_rowconfigure(6, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)

        # Título
        title_label = ctk.CTkLabel(data_frame, text="Data Entry", font=('Consolas', 20), text_color="black")
        title_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Input Textbox 1
        input_label = ctk.CTkLabel(data_frame, text="Input:", text_color="black")
        input_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.input_textbox = ctk.CTkEntry(data_frame, width=200)
        self.input_textbox.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        # Evento para guardar cuando se cambie el valor del textbox
        self.input_textbox.bind("<KeyRelease>", lambda event: self.save_data_to_xml())

        # Checkboxes con variables para Opt1, Opt2, Opt3
        self.checkbox1_var = ctk.IntVar()
        self.checkbox1 = ctk.CTkCheckBox(data_frame, text="Option 1", variable=self.checkbox1_var,
                                         command=self.save_data_to_xml)
        self.checkbox1.grid(row=2, column=0, sticky="n", padx=5, pady=(5, 0))

        self.checkbox2_var = ctk.IntVar()
        self.checkbox2 = ctk.CTkCheckBox(data_frame, text="Option 2", variable=self.checkbox2_var,
                                         command=self.save_data_to_xml)
        self.checkbox2.grid(row=3, column=0, sticky="n", padx=5, pady=(5, 0))

        self.checkbox3_var = ctk.IntVar()
        self.checkbox3 = ctk.CTkCheckBox(data_frame, text="Option 3", variable=self.checkbox3_var,
                                         command=self.save_data_to_xml)
        self.checkbox3.grid(row=4, column=0, sticky="n", padx=5, pady=(5, 0))

        # Segundo Input Textbox
        second_input_label = ctk.CTkLabel(data_frame, text="Second Input:", text_color="black")
        second_input_label.grid(row=5, column=0, sticky="n", padx=5, pady=(15, 0))

        self.another_textbox = ctk.CTkEntry(data_frame, width=200)
        self.another_textbox.grid(row=5, column=0, sticky="s", padx=5, pady=(35, 10))

        # Evento para guardar cuando se cambie el valor del segundo textbox
        self.another_textbox.bind("<KeyRelease>", lambda event: self.save_data_to_xml())

    def submit_data(self):
        print("Data submitted")

    def BackNext(self):
        # Configuración de botones de navegación también en el lado izquierdo
        back_next_frame = ctk.CTkFrame(self, fg_color="white")
        back_next_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Agregar contenido a BackNext (por ejemplo, botones de navegación)

    def Footer(self):
        footer_label = ctk.CTkLabel(self, text="Footer")
        footer_label.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    def load_configuration(self):
        xml_path = "C:\\ELVIS\\TmpDB\\003_Configuration\\TempConfiguration.xml"  # Ruta del archivo XML
        if os.path.exists(xml_path):
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Cargar valores del XML a la interfaz
            self.input_textbox.delete(0, 'end')
            self.input_textbox.insert(0, root.find('Code').text)

            self.checkbox1_var.set(True if root.find('Opt1').text == 'True' else False)
            self.checkbox2_var.set(True if root.find('Opt2').text == 'True' else False)
            self.checkbox3_var.set(True if root.find('Opt3').text == 'True' else False)

            self.another_textbox.delete(0, 'end')
            self.another_textbox.insert(0, root.find('Input2').text)

            # Cargar configuración para las cámaras (Cam1, Cam2, etc.)
            for i in range(1, 5):
                cam = root.find(f'Cam{i}')
                if cam is not None:
                    # Estado del checkbox
                    status = True if cam.find('Status').text == 'True' else False
                    self.status_checkboxes[i - 1].select() if status else self.status_checkboxes[i - 1].deselect()

                    # Actualizar colores y el botón correspondiente
                    if status:
                        self.view_buttons[i - 1].configure(state="normal", fg_color="#FE5200", hover_color="#FE5202")
                        self.status_checkboxes[i - 1].configure(fg_color="#FE5202")
                    else:
                        self.view_buttons[i - 1].configure(state="disabled", fg_color="gray", hover_color="gray")
                        self.status_checkboxes[i - 1].configure(fg_color="gray")

                    # Actualizar las etiquetas de 'Configuration' y 'Light'
                    self.config_labels[i - 1].configure(text=cam.find('Configuration').text)
                    self.light_labels[i - 1].configure(text=cam.find('Light').text)

    def save_configuration(self, row):
        xml_path = "C:\\ELVIS\\TmpDB\\003_Configuration\\TempConfiguration.xml"

        # Asegúrate de que el archivo XML exista
        if os.path.exists(xml_path):
            # Cargar el archivo XML
            tree = ET.parse(xml_path)  # Definir 'tree' cargando el archivo XML
            root = tree.getroot()  # Obtener la raíz del árbol

            # Buscar la cámara correspondiente en el archivo XML
            cam = root.find(f'Cam{row - 1}')
            if cam is not None:
                # Actualizar el valor de 'Status' en el archivo XML
                cam.find('Status').text = "True" if self.status_checkboxes[row - 2].get() else "False"
                cam.find('Configuration').text = self.config_labels[row - 2].cget("text")
                cam.find('Light').text = self.light_labels[row - 2].cget("text")

            # Guardar los cambios en el archivo XML
            tree.write(xml_path)
        else:
            print(f"Error: No se encuentra el archivo XML en {xml_path}")

    def save_data_to_xml(self):
        xml_path = "C:\\ELVIS\\TmpDB\\003_Configuration\\TempConfiguration.xml"

        # Verificar que el archivo XML exista
        if os.path.exists(xml_path):
            tree = ET.parse(xml_path)  # Cargar el archivo XML
            root = tree.getroot()  # Obtener la raíz del árbol

            # Actualizar los valores de los elementos del XML
            root.find('Code').text = self.input_textbox.get()
            root.find('Opt1').text = "True" if self.checkbox1_var.get() else "False"
            root.find('Opt2').text = "True" if self.checkbox2_var.get() else "False"
            root.find('Opt3').text = "True" if self.checkbox3_var.get() else "False"
            root.find('Input2').text = self.another_textbox.get()

            # Guardar los cambios en el archivo XML
            tree.write(xml_path)
        else:
            print(f"Error: No se encuentra el archivo XML en {xml_path}")

