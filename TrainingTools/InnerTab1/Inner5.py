import customtkinter as ctk
from customtkinter import CTkCanvas
from CameraTools import CameraHandler
# Importa la función de entrenamiento desde el módulo local

from Global.GlobalV import Img,Inherit,Calibration

import os  # Importar el módulo os
import shutil  # Importar el módulo shutil
from PIL import ImageGrab
from PIL import Image, ImageDraw  # Asegúrate de tener PILLOW instalado: pip install pillow
import io  # Importar el módulo io para manejar los flujos de entrada/salida
import cv2  # Importar OpenCV
import numpy as np
import configparser


class InnerTab5Content(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="white")
        self.camera_handler = CameraHandler()
        self.states = {}  # Inicializar states aquí
        self.drawn_items = {}  # Inicializar drawn_items aquí
        self.image_counters = {}
        self.Header()
        self.LblOkZone()
        self.LblNGZone()
        self.Trigger()
        self.MainArea()
        self.ButtonsArea()
        self.BackNextButtos()
        self.Footer()
        self.previous_length = len(Img.InspectionData)  # Store the initial length
        self.check_for_updates()

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
        self.grid_rowconfigure(4, minsize=50, weight=0)  # Footer con tamaño fijo de 50 px

        # Empaquetar el frame principal para que ocupe todo el espacio disponible
        self.pack(fill="both", expand=True)
    def Header(self):
        # Fila 1: Columna 1 a 3 expandida label (header)
        header_label = ctk.CTkLabel(self, text="- Clasification -", fg_color="white", font=('Consolas', 25), text_color="black")
        header_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
    def LblOkZone(self):
        OkZone = ctk.CTkFrame(self, fg_color="lightgray")
        OkZone.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=5, pady=5)
        OkZone.grid_rowconfigure(0, weight=1)
        OkZone.grid_rowconfigure(1, weight=1)

        OkZone.grid_columnconfigure(0, minsize=80, weight=0)
        OkZone.grid_columnconfigure(1, weight=1)

        Oklabel = ctk.CTkLabel(OkZone, text="OK", fg_color="white", font=('Consolas', 30, "bold"), text_color="Green")
        Oklabel.grid(row=0, rowspan=2, column=0, sticky="nsew", padx=5, pady=5)

        label = ctk.CTkLabel(OkZone, text="OK", fg_color="white", font=('Consolas', 20, "bold"), text_color="Gray")
        label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Frame to count and view
        CountAndView = ctk.CTkFrame(OkZone, fg_color="white")
        CountAndView.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        CountAndView.grid_columnconfigure(0, weight=1)
        Count = ctk.CTkLabel(CountAndView, text="Do you have 10 Good pictures", fg_color="white", font=('Consolas', 15), text_color="black")
        Count.grid(row=0, rowspan=2, column=0, sticky="nsew", padx=5, pady=5)

        View = ctk.CTkButton(CountAndView, text="View", fg_color="white", font=('Consolas', 20, "bold"), text_color="black")
        View.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    def LblNGZone(self):
        OkZone = ctk.CTkFrame(self, fg_color="lightgray")
        OkZone.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        OkZone.grid_rowconfigure(0, weight=1)
        OkZone.grid_rowconfigure(1, weight=1)

        OkZone.grid_columnconfigure(0, minsize=80, weight=0)
        OkZone.grid_columnconfigure(1, weight=1)

        Oklabel = ctk.CTkLabel(OkZone, text="NG", fg_color="white", font=('Consolas', 30, "bold"), text_color="Red")
        Oklabel.grid(row=0, rowspan=2, column=0, sticky="nsew", padx=5, pady=5)

        label = ctk.CTkLabel(OkZone, text="OK", fg_color="white", font=('Consolas', 20, "bold"), text_color="Gray")
        label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Frame to count and view
        CountAndView = ctk.CTkFrame(OkZone, fg_color="white")
        CountAndView.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        CountAndView.grid_columnconfigure(0, weight=1)
        Count = ctk.CTkLabel(CountAndView, text="Do you have 10 Good pictures", fg_color="white", font=('Consolas', 15), text_color="black")
        Count.grid(row=0, rowspan=2, column=0, sticky="nsew", padx=5, pady=5)

        View = ctk.CTkButton(CountAndView, text="View", fg_color="white", font=('Consolas', 20, "bold"), text_color="black")
        View.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    def MainArea(self):
        MainFrame = ctk.CTkFrame(self, fg_color="white")
        MainFrame.grid(row=2, rowspan=2, column=0, columnspan=2, padx=5, pady=5)

        # Configurar el grid dentro del Frame para que también se expanda
        MainFrame.grid_rowconfigure(0, weight=1)
        MainFrame.grid_columnconfigure(0, weight=1)

        self.MainPic = CTkCanvas(MainFrame, width=Img.ImgWidth, height=Img.ImgHeight)  # Ajusta el tamaño del canvas aquí
        self.MainPic.grid(row=0, column=0)
    def Trigger(self):
        TriggerFrame = ctk.CTkLabel(self, text="Label 2.3", fg_color="lightgray")
        TriggerFrame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        TriggerFrame.grid_columnconfigure(0, weight=1)
        TriggerFrame.grid_columnconfigure(0, weight=1)

        TriggerButton = ctk.CTkButton(TriggerFrame, text="Trigger", command=self.capture_single_image)
        TriggerButton.grid(row=0, column=0)
    def capture_single_image(self):
        self.camera_handler.capture_single_image(self.MainPic)
        # Obtener y procesar la cadena de Inherit.Inspection1
        data = Inherit.Inspection1.split(',')
        rect_x = int(data[1])+Calibration.CalibrationX
        rect_y = int(data[2])+Calibration.CalibrationY
        rect_width = int(data[3])
        rect_height = int(data[4])

        # Dibujar el rectángulo en el canvas
        self.MainPic.create_rectangle(rect_x, rect_y, rect_x + rect_width, rect_y + rect_height, outline='red', width=2)

        # Dibujar las formas de InspectionData dentro del rectángulo
        for item in Img.InspectionData:
            self.draw_shape(item, rect_x, rect_y)
    def show_image_on_canvas(self, img):
        self.MainPic.delete("all")  # Limpiar el canvas antes de mostrar la nueva imagen
        self.image_on_canvas = ImageTk.PhotoImage(img)  # Asegúrate de usar ImageTk.PhotoImage aquí
        self.MainPic.create_image(0, 0, anchor='nw', image=self.image_on_canvas)
    def draw_shape(self, item, rect_x, rect_y):
        shape_x = (item['PositionX'])
        shape_y = (item['PositionY'])
        shape_type = item['Type']
        item_id = item['ID']

        if shape_type == 'oval':
            size_x = item['SizeX']
            size_y = item['SizeY']
            shape_x += size_x / 2
            shape_y += size_y / 2
            shape = self.MainPic.create_oval(rect_x + shape_x - size_x / 2, rect_y + shape_y - size_y / 2,
                                             rect_x + shape_x + size_x / 2, rect_y + shape_y + size_y / 2,
                                             outline='red', width=2)
        elif shape_type == 'rectangle':
            size_x = item['SizeX']
            size_y = item['SizeY']
            shape_x += size_x / 2
            shape_y += size_y / 2
            shape = self.MainPic.create_rectangle(rect_x + shape_x - size_x / 2, rect_y + shape_y - size_y / 2,
                                                  rect_x + shape_x + size_x / 2, rect_y + shape_y + size_y / 2,
                                                  outline='red', width=2)
        elif shape_type == 'circle':
            radius = item['Radio']
            shape_x += radius
            shape_y += radius
            shape = self.MainPic.create_oval(rect_x + shape_x - radius, rect_y + shape_y - radius,
                                             rect_x + shape_x + radius, rect_y + shape_y + radius,
                                             outline='red', width=2)

        if item_id not in self.drawn_items:
            self.drawn_items[item_id] = []
        self.drawn_items[item_id].append(shape)
    def ButtonsArea(self):
        self.ButtonFrame = ctk.CTkFrame(self, fg_color="White")
        self.ButtonFrame.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        self.ButtonFrame.grid_columnconfigure(0, weight=1)
        self.ButtonFrame.grid_columnconfigure(1, weight=1)
        self.ButtonFrame.grid_rowconfigure(0, minsize=80, weight=0)
        self.ButtonFrame.grid_rowconfigure(1, weight=1)

        # Botón para guardar la inspección
        self.SaveButton = ctk.CTkButton(self.ButtonFrame, text="Save Inspection", command=self.save_inspection)
        self.SaveButton.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Frame para elementos de la lista
        self.ListFrame = ctk.CTkScrollableFrame(self.ButtonFrame, bg_color="white", fg_color="white",
                                                height=300)  # Scrollable frame
        self.ListFrame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.ListFrame.grid_columnconfigure(0, weight=1)  # Ajustar peso para controlar el espaciado
        self.ListFrame.grid_columnconfigure(1, weight=1)
        self.ListFrame.grid_columnconfigure(2, weight=1)
        self.ListFrame.grid_columnconfigure(3, weight=1)
        self.update_list_elements()
    def add_list_elements(self, frame, start_row, data):
        # Agregar encabezados
        headers = ["View", "ID", "Treshold", "NG  |  OK"]
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(frame, text=header, fg_color="white", bg_color="white",
                                        font=('Consolas', 15, 'bold'), text_color="black")
            header_label.grid(row=start_row, column=col, sticky="ew", padx=2, pady=2)

        # Agregar elementos de la lista
        for i, item in enumerate(data):
            row = start_row + 1 + i
            bg_color = "white" if i % 2 == 0 else "lightgray"  # Alternar colores

            item_id = item['ID']

            # Agregar checkbox siempre activo
            checkbox_var = ctk.BooleanVar(value=True)
            checkbox = ctk.CTkCheckBox(frame, text="", variable=checkbox_var)
            checkbox.grid(row=row, column=0, sticky="ew", padx=2, pady=2)
            checkbox_var.trace_add("write", lambda *args, item_id=item_id, var=checkbox_var: self.update_state(item_id,
                                                                                                               'checkbox',
                                                                                                               var.get()))

            # Agregar label1 lo más cerca posible del lado izquierdo
            label1 = ctk.CTkLabel(frame, text=f"ID: {item_id}", fg_color=bg_color, bg_color=bg_color,
                                  text_color="black", font=('Consolas', 15))
            label1.grid(row=row, column=1, sticky="ew", padx=2, pady=2)

            # Agregar label2
            label2 = ctk.CTkLabel(frame, text=f"NInspection: {item['NInspection']}", fg_color=bg_color,
                                  bg_color=bg_color, text_color="black", font=('Consolas', 15))
            label2.grid(row=row, column=2, sticky="ew", padx=2, pady=2)

            # Agregar toggle switch
            toggle_var = ctk.BooleanVar(value=True)
            toggle = ctk.CTkSwitch(frame, text="", variable=toggle_var)
            toggle.select()
            toggle.grid(row=row, column=3, sticky="ew", padx=2, pady=2)
            toggle_var.trace_add("write",
                                 lambda *args, item_id=item_id, var=toggle_var: self.update_state(item_id, 'toggle',
                                                                                                  var.get()))

            # Inicializar estado en el diccionario
            self.states[item_id] = {
                'checkbox': checkbox_var.get(),
                'toggle': toggle_var.get()
            }
    def clean_unused_states(self, current_ids):
        keys_to_remove = [key for key in self.states.keys() if key not in current_ids]
        for key in keys_to_remove:
            del self.states[key]
    def update_state(self, item_id, widget_type, value):
        if item_id in self.states:
            self.states[item_id][widget_type] = value
            if widget_type == 'checkbox':
                if value:  # Si se selecciona el checkbox
                    # Dibujar nuevamente las formas
                    for item in Img.InspectionData:
                        if item['ID'] == item_id:
                            self.draw_shape(item, int(Inherit.Inspection1.split(',')[1]),
                                            int(Inherit.Inspection1.split(',')[2]))
                else:  # Si se deselecciona el checkbox
                    # Eliminar las formas del canvas
                    if item_id in self.drawn_items:
                        for shape in self.drawn_items[item_id]:
                            self.MainPic.delete(shape)
                        del self.drawn_items[item_id]
    def update_list_elements(self):
        # Clear current elements
        for widget in self.ListFrame.winfo_children():
            widget.destroy()

        current_ids = [item['ID'] for item in Img.InspectionData]

        # Crear y eliminar las carpetas automáticamente
        self.manage_inspection_folders(current_ids)

        # Limpia los estados no utilizados
        self.clean_unused_states(current_ids)

        if len(Img.InspectionData) > 0:
            self.add_list_elements(self.ListFrame, 0, Img.InspectionData)  # List in a single column
    def save_inspection(self):
        # Desactivar la actualización de la interfaz
        self.update_idletasks()
        self.grid_propagate(False)

        data = Inherit.Inspection1.split(',')
        rect_x = int(data[1])+Calibration.CalibrationX
        rect_y = int(data[2])+Calibration.CalibrationY
        rect_width = int(data[3])
        rect_height = int(data[4])

        for item in Img.InspectionData:
            item_id = item['ID']
            if not self.states[item_id]['checkbox']:
                continue

            shape_x = (int(item['PositionX']))
            shape_y = (int(item['PositionY']))
            print(shape_x,shape_y)
            shape_type = item['Type']

            self.hide_all_shapes()
            self.draw_shape(item, rect_x, rect_y)
            self.update_idletasks()

            # Capturar la imagen del área del canvas después de dibujar la forma
            x1 = self.MainPic.winfo_rootx()
            y1 = self.MainPic.winfo_rooty()
            x2 = x1 + self.MainPic.winfo_width()
            y2 = y1 + self.MainPic.winfo_height()
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            img_np = np.array(img)

            # Convertir la imagen a escala de grises
            gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

            # Aplicar umbral
            threshold_value = Img.ThresholdFilter
            _, img_threshold = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

            # Detectar contornos usando Canny
            img_contours = cv2.Canny(img_threshold, 50, 150)

            # Crear una imagen en color a partir de los contornos detectados
            img_contours_colored = np.zeros_like(img_np)
            img_contours_colored[:, :, 1] = img_contours  # Colocar los contornos en el canal verde

            if self.states[item_id]['toggle']:
                folder = os.path.join(Img.TempDb, f"Inspection_{item_id}", "OK")
                status = "OK"
            else:
                folder = os.path.join(Img.TempDb, f"Inspection_{item_id}", "NG")
                status = "NG"

            if not os.path.exists(folder):
                os.makedirs(folder)

            if item_id not in self.image_counters:
                self.image_counters[item_id] = {"OK": 0, "NG": 0}
            self.image_counters[item_id][status] += 1

            file_name = f"Inspection_{item_id}_{status}_{self.image_counters[item_id][status]:03d}.png"

            img_cropped = img_contours_colored[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width]

            mask = np.zeros_like(img_cropped[:, :, 0], dtype=np.uint8)  # Crear máscara de un solo canal
            mask[:] = 255  # Máscara blanca

            # Dibujar la forma en la máscara y eliminar un borde de 5 píxeles
            # Dibujar la forma en la máscara y eliminar un borde de 5 píxeles

            if shape_type == 'oval':
                shape_x += (int(item['SizeX']) // 2)
                shape_y += (int(item['SizeY']) // 2)
                cv2.ellipse(mask, (shape_x, shape_y), ((int(item['SizeX']) // 2)-2, (int(item['SizeY']) // 2) - 2), 0, 0,
                            360, 0, -1)
            elif shape_type == 'rectangle':
                cv2.rectangle(mask, (shape_x + 2, shape_y + 2),
                              (shape_x + int(item['SizeX']) - 2, shape_y + int(item['SizeY']) - 2), 0, -1 )
            elif shape_type == 'circle':
                shape_x += (int(item['Radio']))
                shape_y += (int(item['Radio']))
                cv2.circle(mask, (shape_x, shape_y), int(item['Radio'])-2 , 0, -1)

            img_result = img_cropped.copy()
            img_result[mask == 255] = (0, 0, 0)  # Color the area outside the inspection in black

            # Convertir de nuevo a imagen PIL y guardar
            img_result_pil = Image.fromarray(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB))
            img_result_pil.save(os.path.join(folder, file_name))

            self.hide_shape(item_id)

        # Mostrar todas las formas al finalizar
        self.show_all_shapes()

        # Reactivar la actualización de la interfaz
        self.grid_propagate(True)
        self.update_idletasks()
    def hide_all_shapes(self):
        for item_id in self.drawn_items:
            for shape in self.drawn_items[item_id]:
                self.MainPic.itemconfig(shape, state='hidden')
    def hide_shape(self, item_id):
        if item_id in self.drawn_items:
            for shape in self.drawn_items[item_id]:
                self.MainPic.itemconfig(shape, state='hidden')
    def show_all_shapes(self):
        for item_id in self.drawn_items:
            for shape in self.drawn_items[item_id]:
                self.MainPic.itemconfig(shape, state='normal')
    def manage_inspection_folders(self, current_ids):
        base_path = Img.TempDb
        # Crear carpetas para los IDs actuales
        for item_id in current_ids:
            inspection_folder = os.path.join(base_path, f"Inspection_{item_id}")
            ng_folder = os.path.join(inspection_folder, "NG")
            ok_folder = os.path.join(inspection_folder, "OK")

            if not os.path.exists(inspection_folder):
                os.makedirs(inspection_folder)
            if not os.path.exists(ng_folder):
                os.makedirs(ng_folder)
            if not os.path.exists(ok_folder):
                os.makedirs(ok_folder)

        # Eliminar carpetas para IDs que ya no están presentes
        all_inspection_folders = [f for f in os.listdir(base_path) if f.startswith("Inspection_")]
        for folder in all_inspection_folders:
            folder_id = int(folder.split("_")[1])
            if folder_id not in current_ids:
                inspection_folder = os.path.join(base_path, folder)
                if os.path.exists(inspection_folder):
                    shutil.rmtree(inspection_folder)  # Eliminar el directorio y todo su contenido
    def check_for_updates(self):
        current_length = len(Img.InspectionData)
        if current_length != self.previous_length:
            self.previous_length = current_length
            self.update_list_elements()
        self.after(1000, self.check_for_updates)  # Check for updates every second
    def BackNextButtos(self):
        button_frame = ctk.CTkFrame(self, fg_color="lightgray")
        button_frame.grid(row=3, column=2, sticky="nsew", padx=5, pady=5)

        # Crear los botones dentro del frame
        button_1 = ctk.CTkButton(button_frame, text="Back", command=self.testData)
        button_2 = ctk.CTkButton(button_frame, text="Training", command=self.run_training)
        button_3 = ctk.CTkButton(button_frame, text="Testing", command=self.test)

        # Colocar los botones en el frame
        button_1.pack(side="left", padx=5, pady=5)
        button_2.pack(side="left", padx=30, pady=5)
        button_3.pack(side="right", padx=5, pady=5)
    def run_training(self):
        # Llama a la función de entrenamiento aquí
        base_path = "C:\\ELVIS\\TmP"
        for inspection_folder in os.listdir(base_path):
            inspection_path = os.path.join(base_path, inspection_folder)
            if os.path.isdir(inspection_path):
                train_model_on_inspection_folder(inspection_path)
    def save_data_to_ini(self):
        # Crear un objeto configparser
        config = configparser.ConfigParser()
        # Convertir todos los elementos a cadenas de texto
        inspection_data_str = ','.join([str(item) for item in Img.InspectionData])
        inspection_str = ','.join([str(item) for item in Img.Inspection])
        inspection_area_str = ','.join([str(item) for item in Img.InspectionArea])


        # Agregar secciones y datos al archivo .ini
        config['Inspection'] = {
            'InspectionData': inspection_data_str,
            'Inspection': inspection_str,
            'InspectionArea': inspection_area_str,
            'ThresholdFilter': str(Img.ThresholdFilter),
            'Inspection1': Inherit.Inspection1,
            'SelectionFilter': Inherit.SelectionFilter
        }

        # Guardar el archivo .ini en la ruta especificada
        with open(Img.LoadAndSaveConfiguration, 'w') as configfile:
            config.write(configfile)

        print("Data saved to inspection_data.ini")
    def Footer(self):
        footer_label = ctk.CTkLabel(self, text="Footer", fg_color="white")
        footer_label.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
    def test(self):
        print(self.states)
    def testData(self):
        print(Img.InspectionData)
        print("--------------")
        print(Img.InspectionArea)
        print("--------------")
        print(Inherit.Inspection1)