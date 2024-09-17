import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import hashlib
import numpy as np
import cv2
import os
from Global.GlobalV import Img
def calculate_image_hash(image):
    image_bytes = image.tobytes()
    return hashlib.md5(image_bytes).hexdigest()


class InnerTab4Content(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.parent = parent

        self.EctractGlobalV()
        self.inspection_areas_data = Img.InspectionData
        self.drawing = False
        self.start_x, self.start_y = None, None
        self.shape_id = None
        self.shape_type = tk.StringVar(value="rectangle")  # Variable para los radiobuttons
        self.inspection_areas = Img.Inspection
        self.current_area_index = tk.IntVar(value=-1)
        self.show_all_shapes = tk.BooleanVar(value=True)

        self.setup_grid()
        self.update_image_periodically()  # Llamar a la función periódica
    def EctractGlobalV(self):
        self.image_path = Img.Contorns
        self.second_image_path = Img.CutOriginalPicture
        self.TempDB= Img.TempDb
    def print_inspection_areas_data(self):
        print("hola")
        for area_data in self.inspection_areas_data:
            print(area_data)

    def on_mouse_wheel(self, event):
        if event.delta > 0 or event.num == 4:
            self.zoom_in()
        elif event.delta < 0 or event.num == 5:
            self.zoom_out()

    def update_image(self, new_image_path, is_second_image=False):
        try:
            new_image = Image.open(new_image_path)
            new_image_hash = calculate_image_hash(new_image)

            if is_second_image:
                image_attr = 'second_image'
                original_image_attr = 'second_original_image'
                photo_attr = 'second_photo'
                current_image_hash_attr = 'current_second_image_hash'
                canvas_attr = 'second_canvas'
            else:
                image_attr = 'image'
                original_image_attr = 'original_image'
                photo_attr = 'photo'
                current_image_hash_attr = 'current_image_hash'
                canvas_attr = 'canvas'

            canvas = getattr(self, canvas_attr, None)

            if canvas is None:
                self.create_canvas_image(new_image_path, 2, 2 if not is_second_image else 1)
                canvas = getattr(self, canvas_attr)

            # Si la imagen es diferente, actualizar la interfaz
            if not hasattr(self, current_image_hash_attr) or getattr(self, current_image_hash_attr) != new_image_hash:
                setattr(self, image_attr, new_image)
                setattr(self, original_image_attr, new_image.copy())  # Guardar la imagen original
                setattr(self, photo_attr, ImageTk.PhotoImage(new_image))
                setattr(self, current_image_hash_attr, new_image_hash)  # Guardar el hash de la imagen actual

                width, height = new_image.size
                canvas.create_image(0, 0, image=getattr(self, photo_attr), anchor="nw")
                canvas.config(scrollregion=canvas.bbox(tk.ALL))

                self.update_radio_buttons()
                self.redraw_image()
        except FileNotFoundError:
            print("Image not found:", new_image_path)

    def setup_grid(self):
        # Configure grid
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.grid_columnconfigure(j, weight=1)

        # Fila 1, Columnas 1 a 4
        header_label = tk.Label(self, text="- Evaluation of inspection zone -",justify="center", bg="white", font=("Consolas", 20))
        header_label.grid(row=0, column=0, columnspan=4)

        # Fila 2, Cada columna con un texto
        for j in range(4):
            if j>1:
                label = tk.Label(self, text=" ", bg="white", font=("Arial", 12))
                label.grid(row=1, column=j, sticky="nsew")


        # Fila 3, Imágenes y Controles
        self.create_canvas_image(self.image_path, 2, 2)
        self.create_canvas_image(self.second_image_path, 2, 1)  # Añadir la segunda imagen

        controls_frame = tk.Frame(self, bg="white")
        controls_frame.grid(row=2, column=3, sticky="nsew")
        self.create_controls(controls_frame)

        # Fila 4, Pie de página
        footer_label = tk.Label(self, text="", bg="white", font=("Arial", 14))
        footer_label.grid(row=3, column=0, columnspan=4, sticky="nsew")

    def create_canvas_image(self, image_path, row, col):
        # Eliminar cualquier frame existente
        for widget in self.grid_slaves(row=row, column=col):
            widget.destroy()

        frame = tk.Frame(self, bg="white")
        frame.grid(row=row, column=col, sticky="nsew", padx=10)

        # Crear un frame para contener el canvas y las barras de desplazamiento
        canvas_frame = tk.Frame(frame, bg="white")
        canvas_frame.pack(side="top", fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        # Añadir scrollbars al canvas
        v_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical",
                                   command=lambda *args: self.sync_scroll_y(*args, from_canvas=canvas))
        v_scrollbar.pack(side="right", fill="y")

        h_scrollbar = tk.Scrollbar(frame, orient="horizontal",
                                   command=lambda *args: self.sync_scroll_x(*args, from_canvas=canvas))
        h_scrollbar.pack(side="bottom", fill="x")

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        try:
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)

            width, height = image.size
            canvas.create_image(0, 0, image=photo, anchor="nw")
            canvas.config(scrollregion=canvas.bbox(tk.ALL))

            canvas.bind("<Button-1>", self.on_button_press)
            canvas.bind("<B1-Motion>", self.on_move_press)
            canvas.bind("<ButtonRelease-1>", self.on_button_release)

            # Vincular eventos de desplazamiento del mouse
            canvas.bind("<MouseWheel>", self.on_mouse_wheel)
            canvas.bind("<Button-4>", self.on_mouse_wheel)  # Para otros sistemas
            canvas.bind("<Button-5>", self.on_mouse_wheel)  # Para otros sistemas

            # Guardar referencia de la imagen y el canvas en el objeto
            if col == 2:
                self.canvas = canvas
                self.photo = photo
                self.image = image
                self.original_image = image.copy()
            else:
                self.second_canvas = canvas
                self.second_photo = photo
                self.second_image = image
                self.second_original_image = image.copy()

        except FileNotFoundError:
            error_label = tk.Label(frame, text="Image not found", bg="white", font=("Arial", 12), fg="red")
            error_label.pack(side="top", fill="both", expand=True)

    def sync_scroll_y(self, *args, from_canvas=None):
        if args[0] == "moveto":
            fraction = float(args[1])
            if from_canvas == self.canvas:
                self.second_canvas.yview_moveto(fraction)
            elif from_canvas == self.second_canvas:
                self.canvas.yview_moveto(fraction)
        elif args[0] == "scroll":
            units = int(args[1])
            what = args[2]
            if from_canvas == self.canvas:
                self.second_canvas.yview_scroll(units, what)
            elif from_canvas == self.second_canvas:
                self.canvas.yview_scroll(units, what)
        self.canvas.yview(*args)
        self.second_canvas.yview(*args)

    def update_max_zones_label(self):
        current_zones = len(self.inspection_areas)
        self.MaxZones.configure(text=f"{current_zones} to 20 zones")

    def sync_scroll_x(self, *args, from_canvas=None):
        if args[0] == "moveto":
            fraction = float(args[1])
            if from_canvas == self.canvas:
                self.second_canvas.xview_moveto(fraction)
            elif from_canvas == self.second_canvas:
                self.canvas.xview_moveto(fraction)
        elif args[0] == "scroll":
            units = int(args[1])
            what = args[2]
            if from_canvas == self.canvas:
                self.second_canvas.xview_scroll(units, what)
            elif from_canvas == self.second_canvas:
                self.canvas.xview_scroll(units, what)
        self.canvas.xview(*args)
        self.second_canvas.xview(*args)

    def create_controls(self, frame):
        controls_frame = ctk.CTkFrame(frame, fg_color="white", bg_color="white", border_color="gray", border_width=1)
        controls_frame.pack(side="top", fill="both", expand=True)

        # Configurar la cuadrícula en controls_frame
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        controls_frame.grid_columnconfigure(2, weight=1)


        titl = ctk.CTkLabel(controls_frame, text="- Inspections -", font=('Consolas', 20, "bold"), text_color="Gray",
                            fg_color="white")
        titl.grid(row=0, column=0, columnspan=4, pady=(30,10), padx=5)

        self.MaxZones = ctk.CTkLabel(controls_frame, text="0 to 20 zones", text_color="black", font=('Consolas', 20))
        self.MaxZones.grid(row=1, column=1, pady=5, sticky="ew")

        add_button = ctk.CTkButton(controls_frame, text="Add zone +", fg_color="white", bg_color="white",
                                   text_color="black",
                                   command=self.add_inspection_area)
        add_button.grid(row=1, column=2, padx=5)

        titl = ctk.CTkLabel(controls_frame, text="Select Shape", font=("Consolas", 20), text_color="black")
        titl.grid(row=2, column=0, columnspan=4, pady=(30,10), padx=5)

        rectangle_rb = tk.Radiobutton(controls_frame, text="Rectangle", variable=self.shape_type, value="rectangle",
                                      bg="white", font=("Arial", 12))
        rectangle_rb.grid(row=3, column=0, pady=5, padx=5, sticky="ew")

        circle_rb = tk.Radiobutton(controls_frame, text="Circle", variable=self.shape_type, value="circle", bg="white",
                                   font=("Arial", 12))
        circle_rb.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        oval_rb = tk.Radiobutton(controls_frame, text="Oval", variable=self.shape_type, value="oval", bg="white",
                                 font=("Arial", 12))
        oval_rb.grid(row=3, column=2, pady=5, padx=5, sticky="ew")

        # View mode
        titl = ctk.CTkLabel(controls_frame, text="View mode", font=("Consolas", 20), text_color="black")
        titl.grid(row=4, column=0, columnspan=4, pady=(30,10), padx=5)

        # Crear un Frame para combinar celdas en la fila 5
        combined_frame = ctk.CTkFrame(controls_frame, bg_color="white", fg_color="white")
        combined_frame.grid(row=5, column=0, columnspan=4, pady=3, padx=5)

        # Crear un Frame interno para centrar los elementos
        inner_frame = ctk.CTkFrame(combined_frame, bg_color="white", fg_color="white")
        inner_frame.pack(padx=5, pady=(10,30))

        # Agregar elementos dentro del Frame interno
        label_only_shape_1 = ctk.CTkLabel(inner_frame, text="Only shape", font=("Consolas", 20), text_color="black")
        label_only_shape_1.pack(side="left", padx=3, pady=3)  # Alinear a la izquierda

        switch_only_shape = ctk.CTkSwitch(inner_frame, text="All shapes", font=("Consolas", 20), text_color="black",
                                          variable=self.show_all_shapes, command=self.toggle_all_shapes)
        switch_only_shape.pack(side="left", padx=3, pady=3)  # Alinear a la izquierda

        # Add and edit zones
        listbox_frame = tk.Frame(controls_frame, width=20)
        listbox_frame.grid(row=6, rowspan=3, column=0, pady=5, sticky="nsew")  # Ajusta el rowspan y sticky

        self.text_widget = tk.Text(listbox_frame, height=2, wrap="none",
                                   width=20)  # Ajusta el tamaño a aproximadamente 40px de altura
        self.text_widget.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.text_widget.yview)
        scrollbar.pack(side="right", fill="y")

        self.text_widget.config(yscrollcommand=scrollbar.set)

        txt = ctk.CTkLabel(controls_frame, text="Configure Zone")
        txt.grid(row=6, column=1, columnspan=2, pady=5,padx=5)  # Ajusta el sticky

        #Delete Zone
        txt = ctk.CTkLabel(controls_frame, text="Delete zone:",text_color="black",font=('Consolas',15))
        txt.grid(row=7, column=1, padx=5,pady=5)  # Ajusta el sticky

        DeleteButton = ctk.CTkButton(controls_frame, text="-", fg_color="white", bg_color="white", text_color="black",
                                      command=self.delete_inspection_area)
        DeleteButton.grid(row=7, column=2, pady=5, padx=5, sticky="ew")

        #Rename Zone
        txt = ctk.CTkLabel(controls_frame, text="Rename:",text_color="black",font=('Consolas',15))
        txt.grid(row=8, column=1, padx=5,pady=5)  # Ajusta el sticky

        self.entry_var = tk.StringVar()
        self.entry = ctk.CTkEntry(controls_frame, textvariable=self.entry_var)
        self.entry.grid(row=8, column=2, pady=5, padx=5, sticky="ew")  # Ajusta el columnspan y sticky
        self.entry_var.trace_add("write", lambda *args: self.save_radiobutton_name())


        # Frame adicional para los botones en la parte inferior
        button_frame = ctk.CTkFrame(controls_frame, fg_color="white", bg_color="white")
        button_frame.grid(row=10, column=0, columnspan=4, pady=30, padx=5, sticky="ew")

        print_button = ctk.CTkButton(button_frame, text="BACK")
        print_button.pack(side="left", padx=5)

        next_button = ctk.CTkButton(button_frame, text="Next step")
        next_button.pack(side="right", padx=5)

    def add_inspection_area(self):
        if len(self.inspection_areas) < 20:  # Permitir hasta 20 zonas
            shape = self.shape_type.get()

            new_area = {
                'shape': shape,
                'coords': (0, 0, 0, 0),
                'width': 0,
                'height': 0,
                'enabled': False,  # Initially not enabled until drawn
                'canvas_id': None  # Store the canvas ID of the shape
            }
            self.inspection_areas.append(new_area)

            self.update_radio_buttons()
            self.current_area_index.set(len(self.inspection_areas) - 1)
            self.update_max_zones_label()  # Actualizar la etiqueta
        else:
            print("No se pueden añadir más zonas. Límite alcanzado.")

    def toggle_all_shapes(self):
        self.redraw_image()  # Redraw the image and shapes based on the switch state

    def zoom_in(self):
        current_width, current_height = self.image.size
        original_width, original_height = self.original_image.size

        if current_width < original_width * 5 and current_height < original_height * 5:
            self.zoom(1.2)  # Increase the size by 20%

    def zoom_out(self):
        current_width, current_height = self.image.size
        original_width, original_height = self.original_image.size
        if current_width > original_width // 2 and current_height > original_height // 2:
            self.zoom(0.8)  # Decrease the size by 20%

    def zoom(self, scale):
        for canvas, image_attr, original_image_attr, photo_attr in [
            (self.canvas, 'image', 'original_image', 'photo'),
            (self.second_canvas, 'second_image', 'second_original_image', 'second_photo')
        ]:
            current_image = getattr(self, image_attr)
            original_image = getattr(self, original_image_attr)

            current_width, current_height = current_image.size
            original_width, original_height = original_image.size

            # Resize the image
            new_width = int(current_width * scale)
            new_height = int(current_height * scale)

            if scale > 1 and (new_width > original_width or new_height > original_height):
                # If scaling up beyond original size, use original image as base
                new_image = original_image.resize((new_width, new_height))
            else:
                new_image = current_image.resize((new_width, new_height))

            setattr(self, image_attr, new_image)
            setattr(self, photo_attr, ImageTk.PhotoImage(new_image))

            # Clear and redraw the canvas
            canvas.delete("all")
            canvas.create_image(0, 0, image=getattr(self, photo_attr), anchor="nw")
            canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Update scrollregion

            # Redraw the shapes
            self.draw_shapes()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for index, area in enumerate(self.inspection_areas):
            display_name = f"ID: {index + 1}, Name: {area.get('name', 'NA')}, Type: {area['shape']}"
            self.listbox.insert(tk.END, display_name)

    def save_radiobutton_name(self, *args):
        index = self.current_area_index.get()
        if 0 <= index < len(self.inspection_areas):
            new_name = self.entry_var.get()
            self.inspection_areas[index]['name'] = new_name
            self.update_radio_buttons()  # Actualizar radiobuttons en el Text widget
            self.redraw_image()
            self.update_inspection_areas_data(index, new_name)  # Actualizar datos de inspección

    def update_inspection_areas_data(self, index, new_name):
        if 0 <= index < len(self.inspection_areas):
            area = self.inspection_areas[index]
            inspection_area_data = {
                'ID': index + 1,
                'NInspection': new_name,
                'Type': area['shape'],
                'PositionX': area['coords'][0],
                'PositionY': area['coords'][1],
                'SizeX': area['width'] if area['shape'] in ["rectangle", "oval"] else 'NA',
                'SizeY': area['height'] if area['shape'] in ["rectangle", "oval"] else 'NA',
                'Radio': area['width'] / 2 if area['shape'] == "circle" else 'NA'
            }

            # Si el ID ya existe en el array, actualizarlo, si no, añadirlo
            for i, data in enumerate(self.inspection_areas_data):
                if data['ID'] == inspection_area_data['ID']:
                    self.inspection_areas_data[i] = inspection_area_data
                    break
            else:
                self.inspection_areas_data.append(inspection_area_data)

    def update_radio_buttons(self):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)  # Clear the Text widget first

        for index, area in enumerate(self.inspection_areas):
            name = area.get('name', f"Zona {index + 1}")
            shape = "círculo" if area['shape'] == "circle" else "rectángulo"
            display_name = f"{name} ({shape})"

            # Create a Radiobutton and insert it in the Text widget
            rb = tk.Radiobutton(self.text_widget, text=display_name,
                                variable=self.current_area_index, value=index, bg="white", font=("Arial", 12),
                                command=self.on_radio_select)

            self.text_widget.window_create(tk.END, window=rb)
            self.text_widget.insert(tk.END, "\n")  # Add a newline for spacing

        self.text_widget.config(state=tk.DISABLED)

    def delete_inspection_area(self):
        index = self.current_area_index.get()
        if 0 <= index < len(self.inspection_areas):
            area = self.inspection_areas[index]
            if area['canvas_id'] is not None:
                self.canvas.delete(area['canvas_id'])  # Remove the shape from the canvas
                self.second_canvas.delete(area['canvas_id'])  # Remove the shape from the second canvas
            del self.inspection_areas[index]
            self.current_area_index.set(-1)

            # Eliminar el área de inspection_areas_data
            for i, data in enumerate(self.inspection_areas_data):
                if data['ID'] == index + 1:
                    del self.inspection_areas_data[i]
                    break

            # Actualizar los IDs en inspection_areas_data
            for i, data in enumerate(self.inspection_areas_data):
                data['ID'] = i + 1

            self.update_radio_buttons()
            self.redraw_image()
            self.update_max_zones_label()  # Actualizar la etiqueta

    def update_radio_buttons(self):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)  # Clear the Text widget first

        for index, area in enumerate(self.inspection_areas):
            name = area.get('name', f"Zona {index + 1}")
            shape = "círculo" if area['shape'] == "circle" else "rectángulo"
            display_name = f"{name} ({shape})"

            # Create a Radiobutton and insert it in the Text widget
            rb = tk.Radiobutton(self.text_widget, text=display_name,
                                variable=self.current_area_index, value=index, bg="white", font=("Arial", 12),
                                command=self.on_radio_select)

            self.text_widget.window_create(tk.END, window=rb)
            self.text_widget.insert(tk.END, "\n")  # Add a newline for spacing

        self.text_widget.config(state=tk.DISABLED)

    def on_radio_select(self):
        index = self.current_area_index.get()
        if 0 <= index < len(self.inspection_areas):
            area = self.inspection_areas[index]
            self.entry_var.set(area.get('name', f"Zona {index + 1}"))
            self.shape_type.set(area['shape'])

    def enable_drawing(self):
        self.drawing = True

    def on_button_press(self, event):
        if self.current_area_index.get() != -1:
            area = self.inspection_areas[self.current_area_index.get()]
            if area['canvas_id'] is not None:
                # Eliminar el rectángulo existente antes de dibujar uno nuevo
                self.canvas.delete(area['canvas_id'])
                self.second_canvas.delete(area['canvas_id'])
                area['canvas_id'] = None  # Restablecer el ID del canvas

            # Ajustar coordenadas con el desplazamiento del scrollbar y límites de la imagen
            self.start_x = max(0, min(self.canvas.canvasx(event.x), self.image.width))
            self.start_y = max(0, min(self.canvas.canvasy(event.y), self.image.height))

            shape = self.shape_type.get()
            if shape == "rectangle":
                self.shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                             outline="red")
                self.second_shape_id = self.second_canvas.create_rectangle(self.start_x, self.start_y, self.start_x,
                                                                           self.start_y, outline="red")
            elif shape == "circle":
                self.shape_id = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y,
                                                        outline="red")
                self.second_shape_id = self.second_canvas.create_oval(self.start_x, self.start_y, self.start_x,
                                                                      self.start_y, outline="red")
            elif shape == "oval":
                self.shape_id = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y,
                                                        outline="red")
                self.second_shape_id = self.second_canvas.create_oval(self.start_x, self.start_y, self.start_x,
                                                                      self.start_y, outline="red")

    def on_move_press(self, event):
        if self.shape_id and self.current_area_index.get() != -1:
            # Ajustar coordenadas con el desplazamiento del scrollbar y límites de la imagen
            cur_x = max(0, min(self.canvas.canvasx(event.x), self.image.width))
            cur_y = max(0, min(self.canvas.canvasy(event.y), self.image.height))

            shape = self.shape_type.get()
            if shape == "rectangle":
                self.canvas.coords(self.shape_id, self.start_x, self.start_y, cur_x, cur_y)
                self.second_canvas.coords(self.second_shape_id, self.start_x, self.start_y, cur_x, cur_y)
            elif shape == "circle":
                # Calcular el radio como la distancia desde el punto de inicio
                radius = min(abs(cur_x - self.start_x), abs(cur_y - self.start_y))
                self.canvas.coords(self.shape_id, self.start_x - radius, self.start_y - radius, self.start_x + radius,
                                   self.start_y + radius)
                self.second_canvas.coords(self.second_shape_id, self.start_x - radius, self.start_y - radius,
                                          self.start_x + radius, self.start_y + radius)
            elif shape == "oval":
                # Calcular el centro del óvalo
                center_x = self.start_x
                center_y = self.start_y
                width = abs(cur_x - center_x)
                height = abs(cur_y - center_y)
                self.canvas.coords(self.shape_id, center_x - width, center_y - height, center_x + width,
                                   center_y + height)
                self.second_canvas.coords(self.second_shape_id, center_x - width, center_y - height, center_x + width,
                                          center_y + height)

    def save_inspection_area_image(self):
        def save_area(area, index):
            current_width, current_height = self.image.size
            original_width, original_height = self.original_image.size

            if area['enabled']:
                x1_real, y1_real, x2_real, y2_real = area['coords_real']

                # Convertir las coordenadas a enteros
                x1_real = int(x1_real)
                y1_real = int(y1_real)
                x2_real = int(x2_real)
                y2_real = int(y2_real)

                # Crear una copia de la imagen original
                result_image = self.original_image.copy()
                result_image_np = np.array(result_image)

                # Crear una máscara
                mask = np.zeros((original_height, original_width), dtype=np.uint8)

                if area['shape'] == 'rectangle':
                    cv2.rectangle(mask, (x1_real, y1_real), (x2_real, y2_real), (255), thickness=cv2.FILLED)
                elif area['shape'] == 'circle':
                    radius_real = int(abs(x2_real - x1_real) / 2)
                    center_real = (int((x1_real + x2_real) / 2), int((y1_real + y2_real) / 2))
                    cv2.circle(mask, center_real, radius_real, (255), thickness=cv2.FILLED)
                elif area['shape'] == 'oval':
                    center_real = (int((x1_real + x2_real) / 2), int((y1_real + y2_real) / 2))
                    axes = (int(abs(x2_real - x1_real) / 2), int(abs(y2_real - y1_real) / 2))
                    cv2.ellipse(mask, center_real, axes, 0, 0, 360, (255), thickness=cv2.FILLED)

                # Colorear el área fuera de la inspección en negro
                blue_background = np.full_like(result_image_np, (0, 0, 0))  # Black en BGR
                result_image_np[mask == 0] = blue_background[mask == 0]

                # Convertir de nuevo a imagen PIL y guardar
                result_image = Image.fromarray(result_image_np)

                # Crear carpeta y guardar imagen
                dir_path = os.path.join(self.TempDB, f"Inspection_{index + 1}")
                os.makedirs(dir_path, exist_ok=True)
                image_path = os.path.join(dir_path, f"Inspection_{index + 1}.png")
                result_image.save(image_path)

                print(f"Zona de inspección {index + 1} guardada como 'Inspection_{index + 1}.png'")

        for index, area in enumerate(self.inspection_areas):
            if area['enabled']:
                threading.Thread(target=save_area, args=(area, index)).start()


    def on_button_release(self, event):
        if self.shape_id and self.current_area_index.get() != -1:
            self.save_inspection_area()  # Guardar automáticamente al soltar el botón
            self.shape_id = None  # Reset shape_id to prevent drawing multiple shapes
            self.second_shape_id = None  # Reset second_shape_id to prevent drawing multiple shapes

    def save_inspection_area(self):
        if self.shape_id and self.current_area_index.get() != -1:
            x1, y1, x2, y2 = self.canvas.coords(self.shape_id)
            current_width, current_height = self.image.size
            original_width, original_height = self.original_image.size

            # Escalar las coordenadas al tamaño original de la imagen
            x1_real = x1 * original_width / current_width
            y1_real = y1 * original_height / current_height
            x2_real = x2 * original_width / current_width
            y2_real = y2 * original_height / current_height

            width_real = abs(x2_real - x1_real)
            height_real = abs(y2_real - y1_real)

            area = self.inspection_areas[self.current_area_index.get()]
            area.update({
                'shape': self.shape_type.get(),
                'coords': (x1, y1, x2, y2),  # Coordenadas escaladas para visualización
                'coords_real': (x1_real, y1_real, x2_real, y2_real),  # Coordenadas reales para guardar
                'width': width_real,
                'height': height_real,
                'enabled': True,
                'canvas_id': self.shape_id  # Store the canvas ID of the shape
            })

            # Actualizar el arreglo global
            inspection_area_data = {
                'ID': self.current_area_index.get() + 1,
                'NInspection': area.get('name', f"Zona {self.current_area_index.get() + 1}"),
                'Type': self.shape_type.get(),
                'PositionX': x1_real,
                'PositionY': y1_real,
                'SizeX': width_real if self.shape_type.get() in ["rectangle", "oval"] else 'NA',
                'SizeY': height_real if self.shape_type.get() in ["rectangle", "oval"] else 'NA',
                'Radio': width_real / 2 if self.shape_type.get() == "circle" else 'NA'
            }

            # Si el ID ya existe en el arreglo, actualizarlo, si no, añadirlo
            for i, data in enumerate(self.inspection_areas_data):
                if data['ID'] == inspection_area_data['ID']:
                    self.inspection_areas_data[i] = inspection_area_data
                    break
            else:
                self.inspection_areas_data.append(inspection_area_data)

            # Imprimir coordenadas y dimensiones en la consola
            shape = self.shape_type.get()
            if shape == "rectangle":
                print(
                    f"Rectángulo - Posición: ({x1_real:.2f}, {y1_real:.2f}), Tamaño: ({width_real:.2f}x{height_real:.2f})")
            elif shape == "circle":
                radius_real = width_real / 2  # Suponiendo que los círculos sean perfectos
                center_x_real = (x1_real + x2_real) / 2
                center_y_real = (y1_real + y2_real) / 2
                print(f"Círculo - Centro: ({center_x_real:.2f}, {center_y_real:.2f}), Radio: {radius_real:.2f}")
            elif shape == "oval":
                print(f"Óvalo - Posición: ({x1_real:.2f}, {y1_real:.2f}), Tamaño: ({width_real:.2f}x{height_real:.2f})")

            self.redraw_image()  # Redraw image and shapes
            self.shape_id = None  # Reset shape_id to prevent drawing multiple shapes
            self.second_shape_id = None  # Reset second_shape_id to prevent drawing multiple shapes
            self.save_inspection_area_image()  # Save inspection area image and configuration

    def update_image_periodically(self):
        self.update_image(self.image_path)
        self.update_image(self.second_image_path, is_second_image=True)
        self.after(500, self.update_image_periodically)

    def redraw_image(self):
        if hasattr(self, 'canvas') and hasattr(self, 'second_canvas'):
            for canvas, photo_attr in [
                (self.canvas, 'photo'),
                (self.second_canvas, 'second_photo')
            ]:
                canvas.delete("all")  # Clear the canvas
                canvas.create_image(0, 0, image=getattr(self, photo_attr), anchor="nw")  # Redraw the image
                canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Update scrollregion
                self.draw_shapes()
        else:
            print("Canvas not initialized.")

    def draw_shapes(self):
        for canvas, image_attr in [
            (self.canvas, 'image'),
            (self.second_canvas, 'second_image')
        ]:
            current_image = getattr(self, image_attr)
            current_width, current_height = current_image.size
            original_width, original_height = self.original_image.size

            width_ratio = current_width / original_width
            height_ratio = current_height / original_height

            if self.show_all_shapes.get():
                areas_to_draw = self.inspection_areas
            else:
                index = self.current_area_index.get()
                if 0 <= index < len(self.inspection_areas):
                    areas_to_draw = [self.inspection_areas[index]]
                else:
                    areas_to_draw = []

            for area in areas_to_draw:
                if area['enabled']:
                    name = area.get('name', f"Zona {self.inspection_areas.index(area) + 1}")
                    x1, y1, x2, y2 = area['coords_real']  # Usar las coordenadas reales para dibujar
                    x1, y1, x2, y2 = x1 * width_ratio, y1 * height_ratio, x2 * width_ratio, y2 * height_ratio
                    if area['shape'] == 'rectangle':
                        canvas.create_rectangle(x1, y1, x2, y2, outline='red', tag="shape")
                    elif area['shape'] == 'circle':
                        radius = (x2 - x1) / 2
                        center_x = x1 + radius
                        center_y = y1 + radius
                        canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                                           outline='red', tag="shape")
                    elif area['shape'] == 'oval':
                        canvas.create_oval(x1, y1, x2, y2, outline='red', tag="shape")
                    canvas.create_text((x1 + x2) / 2, y1 - 10, text=name, fill="white", tag="shape")
                    canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(self.inspection_areas.index(area) + 1),
                                       fill="white", tag="shape")
