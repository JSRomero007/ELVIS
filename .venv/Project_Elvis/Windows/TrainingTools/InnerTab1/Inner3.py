import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import os
import numpy as np
from Global.GlobalV import Inherit, Img


class InnerTab3Content(ctk.CTkFrame):
    def __init__(self, parent, TabView, inner_tab_control):
        super().__init__(parent, fg_color="white")
        self.parent = parent
        self.inner_tab_control = inner_tab_control
        self.NextMotherTabContro = TabView
        self.current_filter = "Negative"  # Siempre utilizar el filtro "Negative"
        self.Camera = Img.Camera
        self.ImgWid = Img.ImgWidth
        self.ImgHei = Img.ImgHeight
        self.shape = 'square'
        self.drawing = False
        self.start_x, self.start_y = 0, 0
        self.end_x, self.end_y = 0, 0
        self.threshold_value = 127
        # Image
        self.contours_image_path = Img.Contorns
        self.image_path = Img.Master
        self.Notfilter = Img.CutOriginalPicture
        self.last_modified = 0

        self.inspection_areas = [{'enabled': False, 'coords': (0, 0, 0, 0), 'width': 0, 'height': 0}]

        # Inicializar self.inspection_vars antes de llamar a InspectionControls
        self.inspection_vars = [
            {'enabled': ctk.IntVar(), 'start_x': ctk.StringVar(), 'start_y': ctk.StringVar(), 'size_x': ctk.StringVar(),
             'size_y': ctk.StringVar()}
        ]

        # Configurar el layout del grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(2,minsize=500)
        self.grid_rowconfigure(0, minsize=50, weight=0)  # Header con tamaño fijo de 50 px
        self.grid_rowconfigure(1, minsize=120, weight=0)  # Fila 1 se expande
        self.grid_rowconfigure(2, weight=1)  # Fila 2 con tamaño fijo de 120 px
        self.grid_rowconfigure(3, minsize=50, weight=0)  # Fila 3 se expande
        # Fila 0: Footer
        self.footer_label_top = ctk.CTkLabel(self, text="Footer (Top)", justify="center")
        self.footer_label_top.grid(row=0, column=0, columnspan=3, pady=5)

        # Fila 1: Labels en cada columna
        self.label1 = ctk.CTkLabel(self, text="Label 1", justify="center")
        self.label1.grid(row=1, column=0, pady=5)
        self.label2 = ctk.CTkLabel(self, text="Label 2", justify="center")
        self.label2.grid(row=1, column=1, pady=5)
        self.label3 = ctk.CTkLabel(self, text="Label 3", justify="center")
        self.label3.grid(row=1, column=2, pady=5)

        # Fila 2: Imagen en columna 0 y 1, Inspection controls en columna 2
        self.image_frame = ctk.CTkFrame(self, fg_color="white", border_width=0)
        self.image_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.canvas = ctk.CTkCanvas(self.image_frame, width=self.ImgWid, height=self.ImgHei)
        self.canvas.grid(row=0,column=0)



        self.button_panel = ctk.CTkFrame(self, fg_color="white", border_width=0)
        self.button_panel.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.InspectionControls()

        # Botón Continue
        self.continue_button = ctk.CTkButton(self.button_panel, text="Continue", text_color="black", command=self.NextStep)
        self.continue_button.pack(pady=10)

        # Fila 3: Footer
        self.footer_label_bottom = ctk.CTkLabel(self, text="Footer (Bottom)", justify="center")
        self.footer_label_bottom.grid(row=3, column=0, columnspan=3, pady=5)

        self.selected_area = ctk.StringVar(value="Inspection 1")

        self.ApplyFilter()

        self.canvas.bind("<Button-1>", self.MouseDown)
        self.canvas.bind("<B1-Motion>", self.MouseMove)
        self.canvas.bind("<ButtonRelease-1>", self.MouseUp)

        self.UpdateImage()


    def update_threshold(self, value):
        self.threshold_value = int(value)
        Img.ThresholdFilter = int(value)
        #print(f"Threshold value: {Img.ThresholdFilter}")  # Imprimir el valor del umbral
        self.threshold_label.configure(text=f"Threshold: {self.threshold_value}")
        self.ApplyFilter()

    # Get the coordinates Inspection 1 & Inspection 2 and save in GlobalV
    def SaveDataInspection(self):
        enabled = self.inspection_vars[0]['enabled'].get()
        start_x = self.inspection_vars[0]['start_x'].get()
        start_y = self.inspection_vars[0]['start_y'].get()
        size_x = self.inspection_vars[0]['size_x'].get()
        size_y = self.inspection_vars[0]['size_y'].get()

        data_string = ",".join([str(enabled), start_x, start_y, size_x, size_y])
        Inherit.Inspection1 = data_string

    def InspectionControls(self):
        for i in range(1):
            frame = ctk.CTkFrame(self.button_panel, fg_color="white", border_color="Gray", border_width=1)
            title_label = ctk.CTkLabel(frame, text=f"Inspection")
            title_label.pack(anchor="n", padx=10, pady=(5, 0))

            frame.pack(pady=10, fill="x", padx=10)
            control_frame = ctk.CTkFrame(frame, fg_color="white")
            control_frame.pack(fill="x", pady=5, padx=10)

            # Ajustar el empaquetado de los widgets dentro del frame
            self.inspection_vars[i]['enabled'].set(1)  # Set the switch to always be active

            ctk.CTkLabel(frame, text="Position", font=('Consolas', 14), text_color="black").pack()
            position_frame = ctk.CTkFrame(frame, fg_color="white")
            position_frame.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(position_frame, text="X", font=('Consolas', 14), text_color="black").pack(side=ctk.LEFT, padx=10)
            start_x_entry = ctk.CTkEntry(position_frame, textvariable=self.inspection_vars[i]['start_x'])
            start_x_entry.pack(side=ctk.LEFT, padx=5)
            start_x_entry.bind("<Return>", lambda event, i=i: self.update_position(i))
            ctk.CTkLabel(position_frame, text="Y", font=('Consolas', 14), text_color="black").pack(side=ctk.LEFT, padx=10)
            start_y_entry = ctk.CTkEntry(position_frame, textvariable=self.inspection_vars[i]['start_y'])
            start_y_entry.pack(side=ctk.LEFT, padx=5)
            start_y_entry.bind("<Return>", lambda event, i=i: self.update_position(i))

            ctk.CTkLabel(frame, text="Size", font=('Consolas', 14), text_color="black").pack(padx=10)
            size_frame = ctk.CTkFrame(frame, fg_color="white")
            size_frame.pack(fill="x", pady=5, padx=10)

            ctk.CTkLabel(size_frame, text="X", font=('Consolas', 14), text_color="black").pack(side=ctk.LEFT, padx=10)
            size_x_entry = ctk.CTkEntry(size_frame, textvariable=self.inspection_vars[i]['size_x'])
            size_x_entry.pack(side=ctk.LEFT, padx=5)
            size_x_entry.bind("<Return>", lambda event, i=i: self.update_size(i))

            ctk.CTkLabel(size_frame, text="Y", font=('Consolas', 14), text_color="black").pack(side=ctk.LEFT, padx=10)
            size_y_entry = ctk.CTkEntry(size_frame, textvariable=self.inspection_vars[i]['size_y'])
            size_y_entry.pack(side=ctk.LEFT, padx=5)
            size_y_entry.bind("<Return>", lambda event, i=i: self.update_size(i))

            ctk.CTkButton(frame, text="Delete Inspection", font=('Consolas', 14), text_color="black",
                          command=lambda i=i: self.DeleteInspection(i)).pack(pady=5, padx=10)
            ctk.CTkLabel(frame, text="Selecte Mode inspection").pack(pady=5, padx=10)
            self.inspection_vars[i]['start_x_entry'] = start_x_entry
            self.inspection_vars[i]['start_y_entry'] = start_y_entry
            self.inspection_vars[i]['size_x_entry'] = size_x_entry
            self.inspection_vars[i]['size_y_entry'] = size_y_entry



            # Crear y empaquetar el slider y la etiqueta dentro del frame de inspección
            self.threshold_slider = ctk.CTkSlider(frame, from_=0, to=255, number_of_steps=255, command=self.update_threshold)
            self.threshold_slider.set(self.threshold_value)
            self.threshold_slider.pack(pady=10)

            self.threshold_label = ctk.CTkLabel(frame, text=f"Threshold: {self.threshold_value}", justify="left")
            self.threshold_label.pack(pady=10)

    def SelectionMode(self):
        if self.Selector.get() == 1:
            print("Activate")
        else:
            print("Deactivate")

    def save_inspection_area(self):
        if self.shape == 'square':
            start_x, end_x = sorted([self.start_x, self.end_x])
            start_y, end_y = sorted([self.start_y, self.end_y])
            coords = (start_x, start_y, end_x, end_y)
            width = abs(end_x - start_x)
            height = abs(end_y - start_y)

            if width > 0 and height > 0:
                selected_index = int(self.selected_area.get()[-1]) - 1
                self.inspection_areas[selected_index] = {
                    'shape': self.shape,
                    'coords': coords,
                    'width': width,
                    'height': height,
                    'enabled': self.inspection_vars[selected_index]['enabled'].get()
                }

                # Capturar y guardar la imagen sin filtro
                self.capture_inspection_image(self.inspection_areas[selected_index], selected_index)

                self.UpdateInspectionVar()
                self.ApplyFilter()
            else:
                print("Error: Coordenadas no válidas para el área")

    # ------ Image ------
    # Filter
    def ApplyFilter(self, apply_only=False):
        # Cargar la imagen original para asegurarse de que los filtros anteriores no se apliquen
        self.frame = cv2.imread(self.image_path)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.frame = cv2.resize(self.frame, (self.ImgWid, self.ImgHei), interpolation=cv2.INTER_LINEAR)

        if self.inspection_areas:
            for area in self.inspection_areas:
                if area['enabled'] and area['coords'] != (0, 0, 0, 0):
                    x1, y1, x2, y2 = area['coords']
                    mask = self.frame[y1:y2, x1:x2].copy()
                    if mask.size != 0:
                        filtered_mask = self.ApplyFilterInImage(Image.fromarray(mask), self.current_filter,
                                                                self.threshold_value)
                        self.frame[y1:y2, x1:x2] = np.array(filtered_mask)
                        if not apply_only:
                            cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        self.update_frame()

    def ApplyFilterWithoutDrawing(self, frame, inspection_areas, filter_type):
        for area in inspection_areas:
            if area['enabled']:
                x1, y1, x2, y2 = area['coords']
                mask = frame[y1:y2, x1:x2].copy()
                if mask.size != 0:
                    filtered_mask = self.ApplyFilterInImage(Image.fromarray(mask), filter_type)
                    frame[y1:y2, x1:x2] = np.array(filtered_mask)
        return frame

    def ApplyFilterInImage(self, image, filter_type, threshold_value=127):
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        if filter_type == "GrayScale":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, frame = cv2.threshold(frame, threshold_value, 255, cv2.THRESH_BINARY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filter_type == "RedVision":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        elif filter_type == "HighlightShadow":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        elif filter_type == "OnlyLines":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.adaptiveThreshold(gray, threshold_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,
                                          2)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filter_type == "FrontLines":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, frame = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.adaptiveThreshold(gray, threshold_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,
                                          2)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filter_type == "Negative":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, frame = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def ShowImage(self):
        try:
            self.frame = cv2.imread(self.image_path)
            if self.frame is not None:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.frame = cv2.resize(self.frame, (self.ImgWid, self.ImgHei), interpolation=cv2.INTER_LINEAR)
                img = Image.fromarray(self.frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.config(width=self.ImgWid, height=self.ImgHei)
                self.canvas.update_idletasks()
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, anchor=ctk.NW, image=imgtk)
                self.canvas.image = imgtk
            else:
                print(f"Error: No se pudo cargar la imagen desde {self.image_path}")
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def UpdateImage(self):
        try:
            modified_time = os.path.getmtime(self.image_path)
            if modified_time != self.last_modified:
                self.last_modified = modified_time
                self.ShowImage()
        except Exception as e:
            print(f"Error al actualizar la imagen: {e}")

        self.after(500, self.UpdateImage)

    def DrawShapes(self):
        for i, area in enumerate(self.inspection_areas):
            if area['enabled']:
                self.DrawAndSaveShape(area, i + 1)

    def DrawShape(self):
        self.canvas.delete("shape")
        for i, area in enumerate(self.inspection_areas):
            if area['enabled']:
                self.DrawAndSaveShape(area, i + 1)
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='#FE5202', tag="shape")
        self.canvas.create_text((self.start_x + self.end_x) // 2, self.start_y - 10,
                                text="Inspection ".format(len(self.inspection_areas) + 1), fill="#FE5202",
                                tag="shape", font=('Consolas', 15))
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        self.canvas.create_text((self.start_x + self.end_x) // 2, (self.start_y + self.end_y) // 2,
                                text=f"{width}x{height}", fill="red", tag="shape")

    def DrawAndSaveShape(self, area, index):
        self.canvas.create_rectangle(area['coords'], outline='red')
        x1, y1, x2, y2 = area['coords']
        self.canvas.create_text((x1 + x2) // 2, y1 - 10, text="Inspection ".format(index), fill="#FE5202",
                                font=('Consolas', 15))
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=f"{width}x{height}", fill="#FE5202",
                                font=('Consolas', 15))

    # ----- Mouse ------
    def MouseDown(self, event):
        selected_index = int(self.selected_area.get()[-1]) - 1
        self.inspection_areas[selected_index]['enabled'] = True
        self.drawing = True
        self.start_x, self.start_y = event.x, event.y
        self.end_x, self.end_y = event.x, event.y  # Initialize end_x and end_y to avoid invalid coordinates

    def MouseMove(self, event):
        if self.drawing:
            self.end_x, self.end_y = event.x, event.y
            self.DrawShape()

    def MouseUp(self, event):
        self.drawing = False
        self.save_inspection_area()

    # ------ Controllers ------

    def toggle_area(self, index):
        self.inspection_areas[index]['enabled'] = True
        self.ApplyFilter()
        self.update_textbox_state()

    def update_textbox_state(self):
        enabled = self.inspection_vars[0]['enabled'].get() and (self.selected_area.get() == f"Inspection 1")
        state = ctk.NORMAL if enabled else ctk.DISABLED

        self.inspection_vars[0]['start_x_entry'].configure(state=state)
        self.inspection_vars[0]['start_y_entry'].configure(state=state)
        self.inspection_vars[0]['size_x_entry'].configure(state=state)
        self.inspection_vars[0]['size_y_entry'].configure(state=state)

    # ------ Controls ------

    # Update Zone
    def UpdateInspectionVar(self):
        area = self.inspection_areas[0]
        self.inspection_vars[0]['start_x'].set(area['coords'][0])
        self.inspection_vars[0]['start_y'].set(area['coords'][1])
        self.inspection_vars[0]['size_x'].set(area['width'])
        self.inspection_vars[0]['size_y'].set(area['height'])
        self.update_textbox_state()

    def update_position(self, index):
        try:
            start_x = int(self.inspection_vars[index]['start_x'].get())
            start_y = int(self.inspection_vars[index]['start_y'].get())
            size_x = self.inspection_areas[index]['width']
            size_y = self.inspection_areas[index]['height']

            end_x = start_x + size_x
            end_y = start_y + size_y

            self.inspection_areas[index]['coords'] = (start_x, start_y, end_x, end_y)

            self.ApplyFilter()

        except ValueError:
            print("Error: Valores de coordenadas inválidos")

    def update_size(self, index):
        try:
            size_x = int(self.inspection_vars[index]['size_x'].get())
            size_y = int(self.inspection_vars[index]['size_y'].get())
            start_x = self.inspection_areas[index]['coords'][0]
            start_y = self.inspection_areas[index]['coords'][1]

            end_x = start_x + size_x
            end_y = start_y + size_y

            self.inspection_areas[index]['coords'] = (start_x, start_y, end_x, end_y)
            self.inspection_areas[index]['width'] = size_x
            self.inspection_areas[index]['height'] = size_y

            self.ApplyFilter()

        except ValueError:
            print("Error: Valores de tamaño inválidos")

    def UpdateImage(self):
        try:
            modified_time = os.path.getmtime(self.image_path)
            if modified_time != self.last_modified:
                self.last_modified = modified_time
                self.ShowImage()
                self.DrawShapes()
        except Exception as e:
            print(f"Error al actualizar la imagen: {e}")

        self.after(500, self.UpdateImage)

    def UpdateFilter(self):
        if self.current_filter != Inherit.SelectionFilter:
            self.current_filter = Inherit.SelectionFilter
            self.ApplyFilter()

        self.after(500, self.UpdateFilter)

    def update_frame(self):
        self.SaveDataInspection()
        img = Image.fromarray(self.frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, anchor=ctk.NW, image=imgtk)
        self.canvas.image = imgtk
        self.DrawShapes()

    # Reset Zone
    def reset_image(self):
        self.ShowImage()
        self.DrawShapes()

    # Delete Zone
    def DeleteInspection(self, index):
        self.inspection_areas[index] = {'enabled': False, 'coords': (0, 0, 0, 0), 'width': 0, 'height': 0}
        self.UpdateInspectionVar()
        self.ApplyFilter()

    def save_inspection_images(self):
        for index, area in enumerate(self.inspection_areas):
            if area['enabled']:
                # Obtener la región de interés ya capturada previamente
                x1, y1, x2, y2 = area['coords']
                if x1 < x2 and y1 < y2:  # Verificar que las coordenadas sean válidas
                    original_roi = self.frame[y1:y2, x1:x2].copy()
                    if original_roi.size > 0:  # Verificar que la imagen no esté vacía

                        # Guardar imagen sin filtro


                        # Aplicar filtro sin dibujar el marco ni la zona de inspección
                        filtered_frame = self.ApplyFilterWithoutDrawing(self.frame.copy(), self.inspection_areas,
                                                                        Inherit.SelectionFilter)
                        filtered_roi = filtered_frame[y1:y2, x1:x2]

                        # Recortar 5 píxeles de cada borde
                        if filtered_roi.shape[0] > 10 and filtered_roi.shape[
                            1] > 10:  # Asegurarse de que el recorte no sea mayor que la imagen
                            cropped_filtered_roi = filtered_roi[2:-2, 2:-2]
                        else:
                            cropped_filtered_roi = filtered_roi  # No recortar si la imagen es demasiado pequeña

                        # Guardar imagen con filtro y recortada
                        filtered_image_path = Img.WithFilter
                        Image.fromarray(cropped_filtered_roi).save(filtered_image_path)

                        # Extraer y guardar contornos de la imagen con filtro
                        gray_filtered = cv2.cvtColor(cropped_filtered_roi, cv2.COLOR_BGR2GRAY)
                        _, thresh = cv2.threshold(gray_filtered, 127, 255, cv2.THRESH_BINARY)
                        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        contour_image = np.zeros_like(cropped_filtered_roi)
                        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 1)
                        Image.fromarray(contour_image).save(self.contours_image_path)

                    else:
                        print(f"Error: La región de interés original está vacía para el área {index + 1}")
                else:
                    print(f"Error: Coordenadas no válidas para el área {index + 1}")

    def capture_inspection_image(self, area, index):
        x1, y1, x2, y2 = area['coords']
        if x1 < x2 and y1 < y2:  # Verificar que las coordenadas sean válidas
            original_roi = self.frame[y1:y2, x1:x2].copy()
            if original_roi.size > 0:  # Verificar que la imagen no esté vacía
                # Guardar imagen sin filtro
                original_image_path = self.Notfilter
                Image.fromarray(original_roi).save(original_image_path)
                return original_roi
            else:
                print(f"Error: La región de interés original está vacía para el área {index + 1}")
        else:
            print(f"Error: Coordenadas no válidas para el área {index + 1}")
        return None

    def NextStep(self):
        self.save_inspection_images()
        self.inner_tab_control.set("Evaluation")

        # self.NextMotherTabContro.set(" Step 2 ")
