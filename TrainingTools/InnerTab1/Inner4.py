import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from Global.GlobalV import Img  # Asegúrate de que Img.CutOriginalPicture esté correctamente definido
import xml.etree.ElementTree as ET
from Global.GlobalV import Cam  # Suponiendo que Cam.id está definido aquí.
class InnerTab4Content(ctk.CTkFrame):
    def __init__(self, parent,inner_tab_control):
        super().__init__(parent)
        self.configure(fg_color="white", bg_color="white")
        self.inner_tab_control = inner_tab_control
        self.current_image_path = None  # Inicializar con None

        # Configurar las columnas para que se expandan
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)  # Para que se expanda también

        # Configurar las filas para que se expandan y establecer tamaños fijos
        self.grid_rowconfigure(0, minsize=50, weight=0)  # Header con tamaño fijo de 50 px
        self.grid_rowconfigure(1, minsize=120, weight=0)  # Fila 1 se expande
        self.grid_rowconfigure(2, weight=1)  # Fila 2 se expande
        self.grid_rowconfigure(3, minsize=80, weight=0)  # Fila 3 se expande
        self.grid_rowconfigure(4, minsize=50, weight=0)  # Footer con tamaño fijo de 50 px

        # Llamar a los métodos que configuran cada área
        self.Header()
        self.PictureFrame()  # Aquí se mostrará la imagen
        self.MenuFrame()  # Aquí se muestra el menú
        self.Footer()

        # Inicializar el valor anterior de Cam.id
        self.previous_cam_id = Cam.id

        # Llama a la función que carga la configuración inicial
        self.load_configuration_from_xml()

        # Iniciar el "watcher" que revisa cambios en Cam.id
        self.watch_cam_id()
    def watch_cam_id(self):
        """Función que observa cambios en Cam.id y actualiza la configuración si cambia."""
        if Cam.id != self.previous_cam_id:  # Si Cam.id ha cambiado
            print(f"Cam.id ha cambiado de {self.previous_cam_id} a {Cam.id}. Recargando configuración.")
            self.previous_cam_id = Cam.id  # Actualiza el valor anterior
            self.load_configuration_from_xml()  # Cargar la configuración de la nueva cámara

        # Revisa cada 1000 milisegundos (1 segundo)
        self.after(1000, self.watch_cam_id)
    def Header(self):
        # Fila 0: Header con título
        header = ctk.CTkLabel(self, text="- Preview camera inspection -", fg_color="white", font=('Consolas', 25),
                              text_color="black")
        header.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
    def PictureFrame(self):
        # Crear el frame para contener el canvas con un tamaño fijo
        camera_frame = ctk.CTkFrame(self, border_width=1, width=Img.ImgWidth + 10, height=Img.ImgHeight + 10,
                                    border_color="blue")  # Aumentar el tamaño del frame para que el borde sea visible
        camera_frame.grid(row=2, column=0, columnspan=2, rowspan=2, padx=90, pady=90, sticky="nsew")

        camera_frame.grid_propagate(False)  # Impide que el frame cambie su tamaño

        # Configurar las columnas y filas para permitir la expansión
        camera_frame.grid_columnconfigure(0, weight=1)
        camera_frame.grid_rowconfigure(0, weight=1)

        # Crear las barras de desplazamiento
        h_scrollbar = ctk.CTkScrollbar(camera_frame, orientation="horizontal",fg_color="#f5f5f5",bg_color="#d4d4d4")
        h_scrollbar.grid(row=1, column=0, padx=1,pady=1,sticky="ew")  # Barra en la parte inferior
        v_scrollbar = ctk.CTkScrollbar(camera_frame, orientation="vertical",fg_color="#f5f5f5",bg_color="#d4d4d4")
        v_scrollbar.grid(row=0, column=1,padx=1,pady=1, sticky="ns")  # Barra a la derecha

        # Crear el canvas dentro del frame
        self.canvas = ctk.CTkCanvas(camera_frame, bg="white", borderwidth=0,
                                    width=Img.ImgWidth, height=Img.ImgHeight,
                                    xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)

        # Configurar las scrollbars para controlar el canvas
        h_scrollbar.configure(command=self.canvas.xview)
        v_scrollbar.configure(command=self.canvas.yview)

        # Cargar la imagen desde Img.CutOriginalPicture
        self.image_path = Img.CutOriginalPicture
        self.original_image = Image.open(self.image_path)  # Mantener la imagen original sin modificaciones
        self.image_tk = ImageTk.PhotoImage(self.original_image)

        # Guardar el tamaño actual de la imagen
        self.current_image = self.original_image.copy()
        self.scale_factor_accum = 1  # Factor de escala acumulado

        # Colocar la imagen en el centro del canvas
        self.canvas.create_image(Img.ImgWidth // 2, Img.ImgHeight // 2, image=self.image_tk, anchor='center')

        # Guardar la referencia de la imagen
        self.canvas.image_tk = self.image_tk

        # Configurar el área desplazable del canvas
        self.canvas.configure(scrollregion=(0, 0, max(Img.ImgWidth, self.original_image.width),
                                            max(Img.ImgHeight, self.original_image.height)))

        # Asignar eventos del mouse para hacer zoom
        self.canvas.bind("<MouseWheel>", self.zoom)
    # Función para realizar el zoom sobre la imagen centrado con límites
    def zoom(self, event):
        # Obtener el tamaño actual del canvas y la imagen
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Obtener las coordenadas del centro del canvas
        center_x = canvas_width // 2
        center_y = canvas_height // 2

        # Escalar la imagen con control de límites
        if event.delta > 0 and self.scale_factor_accum < 5:  # Zoom in, máximo x5
            scale_factor = 1.1
            self.scale_factor_accum *= scale_factor  # Actualiza el factor de escala acumulado
        elif event.delta < 0 and self.scale_factor_accum > 0.5:  # Zoom out, mínimo -x2 (equivale a un factor de 0.5)
            scale_factor = 0.9
            self.scale_factor_accum *= scale_factor  # Actualiza el factor de escala acumulado
        else:
            return  # Si está fuera de los límites, no hacer nada

        # Redimensionar la imagen a partir de la imagen original para evitar pérdida de calidad
        new_width = int(self.original_image.width * self.scale_factor_accum)
        new_height = int(self.original_image.height * self.scale_factor_accum)

        # Redimensionar la imagen con PIL sin modificar la original
        resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(resized_image)

        # Limpiar el canvas y volver a dibujar la imagen en el centro
        self.canvas.delete("all")
        self.canvas.create_image(center_x, center_y, image=self.image_tk, anchor='center')

        # Actualizar la referencia a la imagen redimensionada
        self.canvas.image_tk = self.image_tk

        # Ajustar la región de desplazamiento del canvas
        self.canvas.configure(scrollregion=(0, 0, new_width, new_height))
    def MenuFrame(self):
        # Crear el menu frame con un tamaño fijo en la columna 2, junto a la PictureFrame
        self.menu_frame = ctk.CTkFrame(self, width=200, fg_color="white", border_width=2, border_color="Gray")
        self.menu_frame.grid(row=2, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")
        self.menu_frame.grid_propagate(False)  # Prevenir que el frame se expanda o contraiga
        self.menu_frame.grid_columnconfigure(0, weight=1)  # Columna para el slider
        self.menu_frame.grid_columnconfigure(1, weight=0)  # Columna para el numeric updown (derecha)

        # Configurar las filas del menú para agrupar mejor los elementos
        self.menu_frame.grid_rowconfigure(0, weight=1)  # Fila para el toggle Mode
        self.menu_frame.grid_rowconfigure(1, weight=1)  # Fila para Threshold slider
        self.menu_frame.grid_rowconfigure(2, weight=1)  # Fila para Contour slider
        self.menu_frame.grid_rowconfigure(3, weight=1)  # Fila para Closed Contours toggle
        self.menu_frame.grid_rowconfigure(4, weight=1)  # Fila para el Min Contour slider
        self.menu_frame.grid_rowconfigure(5, weight=1)  # Fila para el Max Contour slider
        self.menu_frame.grid_rowconfigure(6, weight=1)  # Fila para el Invert Threshold toggle
        self.menu_frame.grid_rowconfigure(7, weight=1)  # Espacio adicional
        self.menu_frame.grid_rowconfigure(8, weight=1)  # Fila para el primer botón
        self.menu_frame.grid_rowconfigure(9, weight=1)  # Fila para el segundo botón

        # Agregar el primer toggle (Mode)
        toggle_label = ctk.CTkLabel(self.menu_frame, text="Mode", anchor="center")
        toggle_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.toggle_mode = ctk.CTkSwitch(self.menu_frame, text="", onvalue="Normal", offvalue="Filter",
                                         command=self.toggle_changed)
        self.toggle_mode.grid(row=0, column=1, padx=5, pady=5, sticky="n")
        self.toggle_mode.select()  # Inicializar el toggle en "Normal"

        # Agregar el slider para Threshold y su numeric updown a la derecha
        slider_title = ctk.CTkLabel(self.menu_frame, text="Threshold", anchor="w")
        slider_title.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="ew")

        self.slider = ctk.CTkSlider(self.menu_frame, from_=0, to=255, number_of_steps=255,
                                    command=self.update_threshold)
        self.slider.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.slider.set(128)

        self.numeric_updown = ctk.CTkEntry(self.menu_frame, width=50, justify="center")
        self.numeric_updown.grid(row=1, column=1, padx=5, pady=5)
        self.numeric_updown.insert(0, "128")
        self.numeric_updown.bind("<Return>", self.update_slider)

        # Agregar el slider para Contours y su numeric updown a la derecha
        contour_slider_title = ctk.CTkLabel(self.menu_frame, text="Contours", anchor="w")
        contour_slider_title.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="ew")

        self.contour_slider = ctk.CTkSlider(self.menu_frame, from_=0, to=255, number_of_steps=255,
                                            command=self.update_contours)
        self.contour_slider.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.contour_slider.set(128)

        self.contour_numeric_updown = ctk.CTkEntry(self.menu_frame, width=50, justify="center")
        self.contour_numeric_updown.grid(row=2, column=1, padx=5, pady=5)
        self.contour_numeric_updown.insert(0, "128")
        self.contour_numeric_updown.bind("<Return>", self.update_contour_slider)

        # Agregar el toggle para seleccionar contornos cerrados
        contour_mode_label = ctk.CTkLabel(self.menu_frame, text="Closed Contours", anchor="w")
        contour_mode_label.grid(row=3, column=0, padx=5, pady=(5, 0), sticky="ew")

        self.contour_mode_toggle = ctk.CTkSwitch(self.menu_frame, text="", onvalue="Closed", offvalue="Normal",
                                                 command=self.toggle_contour_mode)
        self.contour_mode_toggle.grid(row=3, column=1, padx=5, pady=5, sticky="n")

        # Agregar el slider para el tamaño mínimo de contornos y su numeric updown a la derecha
        min_contour_label = ctk.CTkLabel(self.menu_frame, text="Min Contour Size", anchor="w")
        min_contour_label.grid(row=4, column=0, padx=5, pady=(5, 0), sticky="ew")

        self.min_contour_slider = ctk.CTkSlider(self.menu_frame, from_=0, to=9000, number_of_steps=100,
                                                command=self.update_min_contour_and_contours)
        self.min_contour_slider.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        self.min_contour_slider.set(0)

        self.min_contour_numeric_updown = ctk.CTkEntry(self.menu_frame, width=50, justify="center")
        self.min_contour_numeric_updown.grid(row=4, column=1, padx=5, pady=5)
        self.min_contour_numeric_updown.insert(0, "0")
        self.min_contour_numeric_updown.bind("<Return>", self.update_min_contour_slider)

        # Agregar el slider para el tamaño máximo de contornos y su numeric updown a la derecha
        max_contour_label = ctk.CTkLabel(self.menu_frame, text="Max Contour Size", anchor="w")
        max_contour_label.grid(row=5, column=0, padx=5, pady=(5, 0), sticky="ew")

        self.max_contour_slider = ctk.CTkSlider(self.menu_frame, from_=0, to=9000, number_of_steps=100,
                                                command=self.update_max_contour_and_contours)
        self.max_contour_slider.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        self.max_contour_slider.set(9000)

        self.max_contour_numeric_updown = ctk.CTkEntry(self.menu_frame, width=50, justify="center")
        self.max_contour_numeric_updown.grid(row=5, column=1, padx=5, pady=5)
        self.max_contour_numeric_updown.insert(0, "9000")
        self.max_contour_numeric_updown.bind("<Return>", self.update_max_contour_slider)

        # Agregar el toggle switch para invertir la umbralización
        invert_toggle_label = ctk.CTkLabel(self.menu_frame, text="Invert Threshold", anchor="w")
        invert_toggle_label.grid(row=6, column=0, padx=5, pady=(5, 0), sticky="ew")

        self.invert_toggle = ctk.CTkSwitch(self.menu_frame, text="", onvalue="On", offvalue="Off",
                                           command=self.toggle_invert_threshold)
        self.invert_toggle.grid(row=6, column=1, padx=5, pady=5, sticky="n")

        # Agregar el primer botón al final del menú
        apply_button = ctk.CTkButton(self.menu_frame, text="Apply Changes", command=self.apply_changes)
        apply_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Agregar el segundo botón debajo del primero
        save_button = ctk.CTkButton(self.menu_frame, text="Save Configuration", command=self.save_configuration)
        save_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    def save_configuration(self):
        self.save_configuration_to_xml()  # Guardar la configuración en XML
        self.inner_tab_control.set("Select inspection area")
    def apply_changes(self):
        self.inner_tab_control.set("Testing")
    def toggle_invert_threshold(self):
        # Verificar el estado del toggle
        if self.invert_toggle.get() == "On":
            # Leer la imagen umbralizada actual
            img = cv2.imread(Img.Contorns, cv2.IMREAD_GRAYSCALE)

            # Invertir los colores de la imagen
            inverted_img = cv2.bitwise_not(img)

            # Guardar la imagen invertida en el mismo archivo o en otro si prefieres mantener ambas versiones
            cv2.imwrite(Img.Contorns, inverted_img)

        else:
            # Si el toggle está en "Off", volver a cargar la imagen original sin invertir
            self.update_threshold(self.slider.get())  # Volver a aplicar el umbral actual sin invertir

        # Cargar y actualizar la imagen en el canvas
        self.load_image_with_zoom(Img.Contorns)
    def update_max_contour_and_contours(self, value):
        # Actualiza el campo numérico cuando el slider de tamaño máximo cambia
        self.update_max_contour_numeric(value)
        # Actualiza los contornos en tiempo real
        self.update_contours()
    def invert_threshold(self):
        # Leer la imagen umbralizada actual
        img = cv2.imread(Img.Contorns, cv2.IMREAD_GRAYSCALE)

        # Invertir los colores: lo que es blanco (255) pasa a negro (0) y lo que es negro (0) pasa a blanco (255)
        inverted_img = cv2.bitwise_not(img)

        # Guardar la imagen invertida en el mismo archivo o en otro si prefieres mantener ambas versiones
        cv2.imwrite(Img.Contorns, inverted_img)

        # Cargar y actualizar la imagen en el canvas
        self.load_image_with_zoom(Img.Contorns)
    def update_min_contour_and_contours(self, value):
        # Actualiza el campo numérico cuando el slider de tamaño mínimo cambia
        self.update_min_contour_numeric(value)
        # Actualiza los contornos en tiempo real
        self.update_contours()
    # Función para actualizar el numeric updown del tamaño mínimo cuando se mueve el slider
    def update_min_contour_numeric(self, value):
        self.min_contour_numeric_updown.delete(0, "end")
        self.min_contour_numeric_updown.insert(0, str(int(value)))
    def update_max_contour_numeric(self, value):
        self.max_contour_numeric_updown.delete(0, "end")
        self.max_contour_numeric_updown.insert(0, str(int(value)))
    def toggle_contour_mode(self):
        # Leer el estado del toggle para cambiar entre contornos cerrados o normales
        mode = self.contour_mode_toggle.get()

        if mode == "Closed":
            print("Modo: Contornos cerrados")
        else:
            print("Modo: Contornos normales")

        # Actualiza los contornos cada vez que se cambia el modo
        self.update_contours(self.contour_slider.get())
    def update_contour_slider(self, event):
        value = self.contour_numeric_updown.get()
        try:
            # Validar que el valor sea numérico y esté dentro del rango
            value = int(value)
            if 0 <= value <= 255:
                self.contour_slider.set(value)  # Actualizar el slider
        except ValueError:
            pass  # Ignorar si el valor no es válido
    # Función para actualizar el valor del slider de contornos
    def update_contours(self, value=None):
        # Leer la imagen original en escala de grises
        img = cv2.imread(Img.CutOriginalPicture, cv2.IMREAD_GRAYSCALE)

        # Obtener las dimensiones de la imagen
        img_height, img_width = img.shape

        # Obtener el valor actual del slider de umbralización (Threshold)
        threshold_value = int(self.slider.get())

        # Aplicar la umbralización antes de buscar contornos
        _, thresh_img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)

        # Verificar si el toggle de inversión está activado
        if self.invert_toggle.get() == "On":
            # Invertir los colores si está activado
            thresh_img = cv2.bitwise_not(thresh_img)

        # Aplicar cierre morfológico para cerrar pequeños huecos en los contornos
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # Tamaño del kernel ajustable
        closed_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)

        # Obtener el valor de los sliders de tamaño mínimo y máximo de contornos
        min_contour_size = int(self.min_contour_slider.get())
        max_contour_size = int(self.max_contour_slider.get())

        # Actualizar los numeric updown correspondientes
        self.min_contour_numeric_updown.delete(0, "end")
        self.min_contour_numeric_updown.insert(0, str(min_contour_size))

        self.max_contour_numeric_updown.delete(0, "end")
        self.max_contour_numeric_updown.insert(0, str(max_contour_size))

        # Verificar el modo seleccionado en el toggle (cerrados o normales)
        mode = self.contour_mode_toggle.get()

        # Crear una imagen en color con 3 canales (para dibujar los contornos en verde)
        contour_img = cv2.cvtColor(closed_img, cv2.COLOR_GRAY2BGR)

        if mode == "Closed":
            # Buscar solo contornos cerrados usando cv2.findContours
            contours, _ = cv2.findContours(closed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            # Aplicar filtro de detección de bordes (Canny) basado en el valor del slider de contornos
            edges = cv2.Canny(closed_img, int(self.contour_slider.get()), int(self.contour_slider.get()) * 2)

            # Encontrar contornos de las aristas detectadas por Canny
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filtrar los contornos que están en el borde de la imagen
        filtered_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)

            # Si el contorno cumple con el tamaño mínimo y máximo, lo procesamos
            if min_contour_size <= area <= max_contour_size:
                # Revisar si el contorno toca el borde de la imagen
                if not any((point[0][0] <= 1 or point[0][0] >= img_width - 1 or point[0][1] <= 1 or point[0][
                    1] >= img_height - 1) for point in cnt):
                    filtered_contours.append(cnt)

        # Dibujar los contornos filtrados en verde con grosor ajustable
        line_thickness = 3  # Ajusta este valor si es necesario
        cv2.drawContours(contour_img, filtered_contours, -1, (0, 255, 0), line_thickness)

        # Guardar la imagen procesada con contornos en Img.Contorns
        cv2.imwrite(Img.Contorns, contour_img)

        # Actualizar la imagen en tiempo real
        self.load_image_with_zoom(Img.Contorns)
    # Función para actualizar el slider del tamaño mínimo del contorno desde el numeric updown
    def update_min_contour_slider(self, event):
        value = self.min_contour_numeric_updown.get()
        try:
            # Validar que el valor sea numérico y esté dentro del rango
            value = int(value)
            if 0 <= value <= 9000:
                self.min_contour_slider.set(value)  # Actualizar el slider de tamaño mínimo
        except ValueError:
            pass  # Ignorar si el valor no es válido
    # Función para actualizar el slider de tamaño máximo de contorno desde el numeric updown
    def update_max_contour_slider(self, event):
        value = self.max_contour_numeric_updown.get()
        try:
            # Validar que el valor sea numérico y esté dentro del rango
            value = int(value)
            if 0 <= value <= 9000:
                self.max_contour_slider.set(value)  # Actualizar el slider de tamaño máximo
        except ValueError:
            pass  # Ignorar si el valor no es válido
    # Función para actualizar el numeric updown del tamaño mínimo cuando se mueve el slider
    def update_min_contour_numeric(self, value):
        self.min_contour_numeric_updown.delete(0, "end")
        self.min_contour_numeric_updown.insert(0, str(int(value)))
    # Función para actualizar el numeric updown del tamaño máximo cuando se mueve el slider
    def update_max_contour_numeric(self, value):
        self.max_contour_numeric_updown.delete(0, "end")
        self.max_contour_numeric_updown.insert(0, str(int(value)))
    def update_threshold(self, value):
        threshold_value = int(value)

        # Leer la imagen original en escala de grises
        img = cv2.imread(Img.CutOriginalPicture, cv2.IMREAD_GRAYSCALE)

        # Aplicar umbralización
        _, thresh_img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)

        # Verificar si el toggle de inversión está activado
        if self.invert_toggle.get() == "On":
            # Invertir los colores si está activado
            thresh_img = cv2.bitwise_not(thresh_img)

        # Guardar la imagen umbralizada (invertida o no) en Img.Contorns
        cv2.imwrite(Img.Contorns, thresh_img)

        # Actualizar la imagen umbralizada en tiempo real
        self.load_image_with_zoom(Img.Contorns)

        # Actualizar el numeric updown del umbral
        self.numeric_updown.delete(0, "end")
        self.numeric_updown.insert(0, str(threshold_value))
    def display_image(self, image_path):
        # Cargar y mostrar la imagen actualizada en el canvas
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)

        self.canvas.delete("all")
        self.canvas.create_image(Img.ImgWidth // 2, Img.ImgHeight // 2, image=image_tk, anchor='center')
        self.canvas.image_tk = image_tk  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
    # Función para manejar el cambio en el toggle
    def toggle_changed(self):
        mode = self.toggle_mode.get()

        # Cambiar la imagen dependiendo del estado del toggle
        if mode == "Normal":
            self.load_image_with_zoom(Img.CutOriginalPicture)  # Cargar la imagen normal
        else:
            self.load_image_with_zoom(Img.Contorns)  # Cargar la imagen con filtro

        print(f"Modo seleccionado: {mode}")
    # Función para cargar y actualizar la imagen si es necesario
    def load_image(self, image_path):
        # Si la nueva imagen es la misma que la actual, no hacer nada
        if self.current_image_path == image_path:
            return  # Mantener la imagen actual si es la misma

        # Cargar la nueva imagen y actualizar el path actual
        self.current_image_path = image_path
        self.original_image = Image.open(image_path)
        self.image_tk = ImageTk.PhotoImage(self.original_image)

        # Guardar el tamaño actual de la imagen
        self.current_image = self.original_image.copy()

        # Limpiar el canvas y volver a dibujar la imagen
        self.canvas.delete("all")
        self.canvas.create_image(Img.ImgWidth // 2, Img.ImgHeight // 2, image=self.image_tk, anchor='center')

        # Forzar la actualización del canvas
        self.canvas.update_idletasks()  # Forzar que el canvas se redibuje

        # Guardar la referencia de la imagen
        self.canvas.image_tk = self.image_tk

        # Ajustar la región de desplazamiento del canvas
        self.canvas.configure(scrollregion=(0, 0, max(Img.ImgWidth, self.original_image.width),
                                            max(Img.ImgHeight, self.original_image.height)))
    def load_image_with_zoom(self, image_path):
        # Cargar la nueva imagen
        self.original_image = Image.open(image_path)
        self.current_image_path = image_path

        # Redimensionar la imagen manteniendo el zoom actual
        new_width = int(self.original_image.width * self.scale_factor_accum)
        new_height = int(self.original_image.height * self.scale_factor_accum)

        # Redimensionar la imagen con PIL
        resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(resized_image)

        # Limpiar el canvas y volver a dibujar la imagen con el zoom aplicado
        self.canvas.delete("all")
        self.canvas.create_image(Img.ImgWidth // 2, Img.ImgHeight // 2, image=self.image_tk, anchor='center')

        # Guardar la referencia de la imagen redimensionada
        self.canvas.image_tk = self.image_tk

        # Ajustar la región de desplazamiento del canvas
        self.canvas.configure(scrollregion=(0, 0, new_width, new_height))

    # Función para actualizar el valor del numeric updown al mover el slider
    def update_numeric(self, value):
        # Actualiza el numeric updown con el valor del slider en formato de porcentaje
        self.numeric_updown.delete(0, "end")
        self.numeric_updown.insert(0, f"{int(value)}%")  # Actualizar en porcentaje
    def refresh_canvas(self, image_path):
        # Cargar y mostrar la imagen actualizada en el canvas
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)

        # Actualizar self.current_image para reflejar la imagen actual
        self.current_image = image  # Actualiza la imagen actual

        # Limpiar y actualizar el canvas
        self.canvas.delete("all")
        self.canvas.create_image(Img.ImgWidth // 2, Img.ImgHeight // 2, image=image_tk, anchor='center')

        # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
        self.canvas.image_tk = image_tk
        self.image_tk = image_tk  # Actualizar el atributo self.image_tk también
    # Función para actualizar el slider cuando se cambia el valor en el numeric updown
    def update_slider(self, event):
        value = self.numeric_updown.get()
        try:
            # Validar que el valor sea numérico y esté dentro del rango
            value = int(value)
            if 0 <= value <= 255:
                self.slider.set(value)  # Actualizar el slider
        except ValueError:
            pass  # Ignorar si el valor no es válido
    def Footer(self):
        # Fila 4: Footer vacío
        footer = ctk.CTkLabel(self, text="", text_color="black", font=('Consolas', 25, 'bold'))
        footer.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
    def save_configuration_to_xml(self):
        # Cargar el archivo XML
        xml_file = "C:\\ELVIS\\TmpDB\\003_Configuration\\TempConfiguration.xml"
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Encontrar el nodo de la cámara basado en Cam.id
        cam_id = f"Cam{Cam.id}"
        cam_node = root.find(cam_id)

        if cam_node is None:
            print(f"No se encontró la cámara {cam_id} en el archivo XML.")
            return

        # Función auxiliar para encontrar o crear nodos
        def find_or_create_node(parent, tag, default_value=""):
            node = parent.find(tag)
            if node is None:
                node = ET.SubElement(parent, tag)
                node.text = default_value
            return node

        # Actualizar los campos en el nodo de la cámara seleccionada
        umbral_value = str(int(self.slider.get()))  # Valor del umbral
        close_contourns_value = str(self.contour_mode_toggle.get())  # Contornos cerrados activado/desactivado
        value_contorn_value = str(int(self.contour_slider.get()))  # Valor del contorno
        min_contour_value = str(int(self.min_contour_slider.get()))  # Tamaño mínimo de contornos
        max_contour_value = str(int(self.max_contour_slider.get()))  # Tamaño máximo de contornos
        invert_value = "True" if self.invert_toggle.get() == "On" else "False"  # Invertir umbral activado/desactivado

        # Buscar o crear los nodos si no existen
        find_or_create_node(cam_node, "Umbral").text = umbral_value
        find_or_create_node(cam_node, "CloseContourns").text = close_contourns_value
        find_or_create_node(cam_node, "ValueContorn").text = value_contorn_value
        find_or_create_node(cam_node, "MinContourn").text = min_contour_value
        find_or_create_node(cam_node, "MaxContourn").text = max_contour_value
        find_or_create_node(cam_node, "Invert").text = invert_value

        # Guardar los cambios en el archivo XML
        tree.write(xml_file)

        print(f"Configuración guardada exitosamente para {cam_id}.")
    def load_configuration_from_xml(self):
        # Cargar el archivo XML
        xml_file = "C:\\ELVIS\\TmpDB\\003_Configuration\\TempConfiguration.xml"
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Encontrar el nodo de la cámara basado en Cam.id
        cam_id = f"Cam{Cam.id}"
        cam_node = root.find(cam_id)

        if cam_node is None:
            print(f"No se encontró la cámara {cam_id} en el archivo XML.")
            return

        # Función auxiliar para encontrar nodos y retornar un valor por defecto si no existe
        def find_node_value(parent, tag, default_value=""):
            node = parent.find(tag)
            return node.text if node is not None else default_value

        # Leer los valores del XML
        umbral_value = int(find_node_value(cam_node, "Umbral", "128"))  # Valor del umbral, por defecto 128
        close_contourns_value = find_node_value(cam_node, "CloseContourns",
                                                "False")  # Contornos cerrados, por defecto False
        value_contorn_value = int(
            find_node_value(cam_node, "ValueContorn", "128"))  # Valor del contorno, por defecto 128
        min_contour_value = int(
            find_node_value(cam_node, "MinContourn", "0"))  # Tamaño mínimo de contornos, por defecto 0
        max_contour_value = int(
            find_node_value(cam_node, "MaxContourn", "9000"))  # Tamaño máximo de contornos, por defecto 9000
        invert_value = find_node_value(cam_node, "Invert", "False")  # Invertir umbral, por defecto False

        # Actualizar los sliders, toggles y campos de la interfaz con los valores cargados
        self.slider.set(umbral_value)  # Actualiza el slider del umbral
        self.numeric_updown.delete(0, "end")
        self.numeric_updown.insert(0, str(umbral_value))  # Actualiza el numeric updown del umbral

        self.contour_slider.set(value_contorn_value)  # Actualiza el slider del contorno
        self.contour_numeric_updown.delete(0, "end")
        self.contour_numeric_updown.insert(0, str(value_contorn_value))  # Actualiza el numeric updown del contorno

        self.min_contour_slider.set(min_contour_value)  # Actualiza el slider de tamaño mínimo
        self.min_contour_numeric_updown.delete(0, "end")
        self.min_contour_numeric_updown.insert(0,
                                               str(min_contour_value))  # Actualiza el numeric updown de tamaño mínimo

        self.max_contour_slider.set(max_contour_value)  # Actualiza el slider de tamaño máximo
        self.max_contour_numeric_updown.delete(0, "end")
        self.max_contour_numeric_updown.insert(0,
                                               str(max_contour_value))  # Actualiza el numeric updown de tamaño máximo

        # Actualizar el toggle de contornos cerrados
        if close_contourns_value == "True":
            self.contour_mode_toggle.select()
        else:
            self.contour_mode_toggle.deselect()

        # Actualizar el toggle de inversión de umbral
        if invert_value == "True":
            self.invert_toggle.select()
        else:
            self.invert_toggle.deselect()

        print(f"Configuración cargada exitosamente para {cam_id}.")