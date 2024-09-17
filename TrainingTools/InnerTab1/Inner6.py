import customtkinter as ctk
from Global.GlobalV import Img, Calibration
from CameraTools import CameraHandler

class InnerTab6Content(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg_color="white", fg_color="white")

        # Inicializar CameraHandler
        self.camera_handler = CameraHandler()

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
        self.grid_rowconfigure(3, minsize=80, weight=0)  # Fila 3 se expande

        self.Header()
        self.Trigger()
        self.MainArea()
        self.Data()
        self.BackNext()
        self.Footer()
    def Header(self):
        # Header (Fila 0, Columna 0 a 2)
        header_label = ctk.CTkLabel(self, text="- Testing -", fg_color="white", font=('Consolas', 25), text_color="black")
        header_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
    def MainArea(self):
        MainFrame = ctk.CTkFrame(self, fg_color="white")
        MainFrame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Configurar el grid dentro del Frame para que también se expanda
        MainFrame.grid_rowconfigure(0, weight=1)
        MainFrame.grid_columnconfigure(0, weight=1)

        self.MainPic = ctk.CTkCanvas(MainFrame, width=Img.ImgWidth, height=Img.ImgHeight, bg="red", bd=7, highlightthickness=0)
        self.MainPic.grid(row=0, column=0)
    def Trigger(self):
        # Fila 1 (Columnas 0 a 2)
        label1 = ctk.CTkLabel(self, text="")
        label1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        label2 = ctk.CTkLabel(self, text="")
        label2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        capture_button = ctk.CTkButton(self, text="Capture Image", command=self.capture_image)
        capture_button.grid(row=3, column=2, padx=10, pady=10)  # Mover el botón a {buttons}
    def capture_image(self):
        self.camera_handler.capture_single_image(self.MainPic)
    def Data(self):
        # Fila 2 (Column 2 Labels)
        data_frame = ctk.CTkFrame(self, fg_color="white")
        data_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        zone1_label = ctk.CTkLabel(data_frame, text="Zona 1: Similitud",text_color="black")
        zone1_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Barra de progreso para Zona 1 con color personalizado
        self.similarity_bar1 = ctk.CTkProgressBar(data_frame, orientation="horizontal", width=200, height=20,border_width=1)
        self.similarity_bar1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.similarity_bar1.set(0.86)  # Valor preestablecido al 75% de la barra (0.75 de un rango de 0 a 1)

        # Etiqueta para mostrar el valor numérico de la similitud
        self.similarity_value1 = ctk.CTkLabel(data_frame, text="86%",text_color="black")
        self.similarity_value1.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        zone2_label = ctk.CTkLabel(data_frame, text="Zona 2: Similitud",text_color="black")
        zone2_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        # Barra de progreso para Zona 2 con color personalizado
        self.similarity_bar2 = ctk.CTkProgressBar(data_frame, orientation="horizontal", width=200, height=20,border_width=1)
        self.similarity_bar2.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.similarity_bar2.set(0.20)  # Valor preestablecido al 50% de la barra (0.50 de un rango de 0 a 1)

        # Etiqueta para mostrar el valor numérico de la similitud
        self.similarity_value2 = ctk.CTkLabel(data_frame, text="20%",text_color="black")
        self.similarity_value2.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
    def BackNext(self):
        # Fila 3 (Columnas 0 a 2)
        label5 = ctk.CTkLabel(self, text="")
        label5.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        label6 = ctk.CTkLabel(self, text="")
        label6.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

        # Mover el botón a la celda correcta
        capture_button = ctk.CTkButton(self, text="Capture Image", command=self.capture_image)
        capture_button.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
    def Footer(self):
        # Footer (Fila 4, Columna 0 a 2)
        footer_label = ctk.CTkLabel(self, text="Footer")
        footer_label.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
