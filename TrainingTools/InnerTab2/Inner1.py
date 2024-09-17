
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import numpy as np
from CameraTools import Filters
from Global.GlobalV import Inherit, Img
import os
import threading

class InnerTab1Content(ctk.CTkFrame):
    def __init__(self, parent, filter_name, num_inspection_zones=2):
        super().__init__(parent, fg_color="white", bg_color="white")
        self.Camera = Img.Camera
        self.ImgWid = Img.ImgWidth
        self.ImgHei = Img.ImgHeidht

        self.filters = Filters()
        self.filter_name = Inherit.SelectionFilter
        self.save_path = Img.SaveImage
        os.makedirs(self.save_path, exist_ok=True)
        self.num_inspection_zones = num_inspection_zones
        self.create_save_folders()
        self.image_count = 0
        self.create_content()

        # Inicializar roi_images
        self.roi_images = {}
        self.selected_zones = {}  # Guardar estado de los toggles
        self.toggle_buttons = {}  # Guardar referencias a los toggles

        self.create_toggle_buttons()  # Crear toggle buttons
        self.update_toggle_buttons()  # Actualizar los toggle buttons según el estado de Enable_Inspection

        self.continuous_update()  # Iniciar la actualización continua

    def create_toggle_buttons(self):
        for i in range(1, self.num_inspection_zones + 1):
            zone_label = ctk.CTkLabel(self.right_frame, text=f"Zone {i}")
            zone_label.pack(pady=5)

            toggle_button = ctk.CTkSwitch(self.right_frame, text="OK",
                                          command=lambda z=f"Zone{i}": self.toggle_selection(z))
            toggle_button.select()  # Set default to OK
            toggle_button.pack(pady=2)
            self.toggle_buttons[f"Zone{i}"] = (zone_label, toggle_button)

            self.selected_zones[f"Zone{i}"] = "OK"  # Default selection

    def create_save_folders(self):
        self.inspection_paths = {}
        for i in range(1, self.num_inspection_zones + 1):
            ok_path = os.path.join(self.save_path, f"Inspection_Zone{i}", "OK")
            ng_path = os.path.join(self.save_path, f"Inspection_Zone{i}", "NG")
            os.makedirs(ok_path, exist_ok=True)
            os.makedirs(ng_path, exist_ok=True)
            self.inspection_paths[f"Zone{i}_OK"] = ok_path
            self.inspection_paths[f"Zone{i}_NG"] = ng_path

    def create_toggle_button(self, i):
        zone_label = ctk.CTkLabel(self.right_frame, text=f"Zone {i}")
        zone_label.pack(pady=5)

        toggle_button = ctk.CTkSwitch(self.right_frame, text="OK",
                                      command=lambda z=f"Zone{i}": self.toggle_selection(z))
        toggle_button.select()  # Set default to OK
        toggle_button.pack(pady=2)
        self.toggle_buttons[f"Zone{i}"] = (zone_label, toggle_button)

        self.selected_zones[f"Zone{i}"] = "OK"  # Default selection

    def create_content(self):
        # Frame izquierdo para la cámara
        self.left_frame = ctk.CTkFrame(self, fg_color="white", bg_color="white")
        self.left_frame.pack(side="left", padx=10, pady=10)

        # Frame derecho para controles y zona de información
        self.right_frame = ctk.CTkFrame(self, fg_color="white", bg_color="white")
        self.right_frame.pack(side="right", padx=10, pady=10)

        # Label para mostrar la imagen de la zona de inspección
        self.inspection_label = ctk.CTkLabel(self.left_frame, text="")
        self.inspection_label.pack()

        # Botón de trigger
        self.trigger_button = ctk.CTkButton(self.right_frame, text="Trigger", command=self.trigger_camera)
        self.trigger_button.pack(pady=5)

        # Frame para información
        self.info_frame = ctk.CTkFrame(self.right_frame, fg_color="white", bg_color="white")
        self.info_frame.pack(pady=10)

        # Labels para cada zona de inspección
        self.zone_info_labels = {}
        for i in range(1, self.num_inspection_zones + 1):
            zone_label = ctk.CTkLabel(self.info_frame, text=f"Zone {i}: OK: 0, NG: 0")
            zone_label.pack(pady=2)
            self.zone_info_labels[i] = zone_label

    def trigger_camera(self):


        self.trigger_button.configure(state="disabled")
        threading.Thread(target=self._capture_and_process_image).start()

    def _capture_and_process_image(self):
        # Inicializar la cámara
        self.camera = cv2.VideoCapture(self.Camera)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.ImgWid)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.ImgHei)

        ret, frame = self.camera.read()
        if ret:
            self.frame = frame.copy()
            self.update_inspection_zones()

            print(f"Filtro seleccionado: {Inherit.SelectionFilter}")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.ImgWid, self.ImgHei), interpolation=cv2.INTER_LINEAR)

            self.roi_images = {}  # Reset roi_images
            for i in range(1, self.num_inspection_zones + 1):
                if globals()[f"Enable_Inspection_{i}"] == 1 and globals()[f"rect{i}_width"] > 0 and globals()[
                    f"rect{i}_height"] > 0:
                    roi = frame[globals()[f"rect{i}_y"]:globals()[f"rect{i}_y"] + globals()[f"rect{i}_height"],
                          globals()[f"rect{i}_x"]:globals()[f"rect{i}_x"] + globals()[f"rect{i}_width"]]
                    roi_no_filter = roi.copy()
                    frame[globals()[f"rect{i}_y"]:globals()[f"rect{i}_y"] + globals()[f"rect{i}_height"],
                    globals()[f"rect{i}_x"]:globals()[f"rect{i}_x"] + globals()[f"rect{i}_width"]] = roi_no_filter

                    start_point = (globals()[f"rect{i}_x"], globals()[f"rect{i}_y"])
                    end_point = (globals()[f"rect{i}_x"] + globals()[f"rect{i}_width"],
                                 globals()[f"rect{i}_y"] + globals()[f"rect{i}_height"])
                    color = (255, 0, 0) if i == 1 else (0, 255, 0)
                    thickness = 2
                    frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
                    frame = cv2.putText(frame, f'Inspection {i}',
                                        (globals()[f"rect{i}_x"], globals()[f"rect{i}_y"] - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

                    self.roi_images[f"Zone{i}"] = roi_no_filter  # Guardar la imagen sin filtro

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.inspection_label.imgtk = imgtk
            self.inspection_label.configure(image=imgtk)

            if self.roi_images:  # Solo guardar si hay imágenes válidas
                self.save_image()  # Guardar automáticamente después de mostrar los toggle buttons
        self.camera.release()
        self.after(100, lambda: self.trigger_button.configure(state="normal"))

    def update_inspection_zones(self):
        for i in range(1, self.num_inspection_zones + 1):
            inspection_values = getattr(Inherit, f"Inspection{i}").split(',')
            globals()[f"Enable_Inspection_{i}"] = int(inspection_values[0])
            print(f"{inspection_values[0]}")
            globals()[f"rect{i}_x"] = int(inspection_values[1])
            globals()[f"rect{i}_y"] = int(inspection_values[2])
            globals()[f"rect{i}_width"] = int(inspection_values[3])
            globals()[f"rect{i}_height"] = int(inspection_values[4])

        self.update_toggle_buttons()  # Actualizar la visibilidad de los toggle buttons
    def show_popup(self, roi_images):
        self.popup = ctk.CTkFrame(self.right_frame, fg_color="white", bg_color="white")
        self.popup.pack(pady=10)

        self.selected_zones = {}
        self.toggle_buttons = {}

        for zone, image in roi_images.items():
            if self.is_zone_valid(zone):
                label = ctk.CTkLabel(self.popup, text=zone)
                label.pack(pady=5)

                toggle_button_ok = ctk.CTkSwitch(self.popup, text="OK",
                                                 command=lambda z=zone, s="OK": self.toggle_selection(z, s))
                toggle_button_ok.select()  # Set default to OK
                toggle_button_ok.pack(pady=2)
                self.toggle_buttons[(zone, "OK")] = toggle_button_ok

                toggle_button_ng = ctk.CTkSwitch(self.popup, text="NG",
                                                 command=lambda z=zone, s="NG": self.toggle_selection(z, s))
                toggle_button_ng.pack(pady=2)
                self.toggle_buttons[(zone, "NG")] = toggle_button_ng

                self.selected_zones[zone] = "OK"  # Default selection

    def toggle_selection(self, zone):
        # Cambiar estado basado en el estado del toggle button
        if self.toggle_buttons[zone][1].get() == 1:  # Toggle activado
            self.selected_zones[zone] = "OK"
        else:  # Toggle desactivado
            self.selected_zones[zone] = "NG"

    def save_image(self):
        for zone, status in self.selected_zones.items():
            if zone in self.roi_images:  # Asegurarse de que la zona sea válida
                image = self.roi_images[zone]
                image_filtered = self.filters.apply_filter(image,
                                                           Inherit.SelectionFilter)  # Aplicar el filtro al guardar
                self.image_count += 1
                save_path = self.inspection_paths[f"{zone}_{status}"]
                image_path = os.path.join(save_path, f"{zone}_{self.image_count}.png")
                image_bgr = cv2.cvtColor(image_filtered, cv2.COLOR_RGB2BGR)  # Guardar la imagen filtrada
                cv2.imwrite(image_path, image_bgr)
                print(f"Saved {zone} snapshot with filter to {image_path}")
                zone_num = int(zone.replace('Zone', ''))
                ok_count = len(os.listdir(self.inspection_paths[f"Zone{zone_num}_OK"]))
                ng_count = len(os.listdir(self.inspection_paths[f"Zone{zone_num}_NG"]))
                self.zone_info_labels[zone_num].configure(text=f"Zone {zone_num}: OK: {ok_count}, NG: {ng_count}")

        self.trigger_button.configure(state="normal")

    def update_toggle_buttons(self):
        for i in range(1, self.num_inspection_zones + 1):
            inspection_values = getattr(Inherit, f"Inspection{i}").split(',')
            globals()[f"Enable_Inspection_{i}"] = int(inspection_values[0])

            # Imprimir el valor de inspection_values[0]
            #print(f"Inspection {i} value: {inspection_values[0]}")

            if globals()[f"Enable_Inspection_{i}"] != 0:
                self.toggle_buttons[f"Zone{i}"][0].pack(pady=5)
                self.toggle_buttons[f"Zone{i}"][1].pack(pady=2)
            else:
                self.toggle_buttons[f"Zone{i}"][0].pack_forget()
                self.toggle_buttons[f"Zone{i}"][1].pack_forget()

    def check_inspection_zones(self):
        valid_zones = False
        for i in range(1, self.num_inspection_zones + 1):
            if globals()[f"rect{i}_width"] > 0 or globals()[f"rect{i}_height"] > 0:
                valid_zones = True
                break
        return valid_zones

    def continuous_update(self):
        self.update_toggle_buttons()
        self.after(1000, self.continuous_update)  # Llama a esta función cada 1000 ms (1 segundo)

    def is_zone_valid(self, zone):
        zone_num = int(zone.replace('Zone', ''))
        return globals()[f"rect{zone_num}_width"] > 0 and globals()[f"rect{zone_num}_height"] > 0

    def __del__(self):
        # Asegurarse de liberar la cámara si todavía está abierta
        try:
            if self.camera.isOpened():
                self.camera.release()
        except AttributeError:
            pass