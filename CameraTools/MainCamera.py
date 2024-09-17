import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import numpy as np
from CameraTools import Camera
from Global.GlobalV import Img
import threading


class MainCamera(ctk.CTkFrame):
    def __init__(self, parent, save_path, update_callback, filter_type=None):
        super().__init__(parent)
        self.Camera=Img.Camera
        self.ImgWid=Img.ImgWidth
        self.ImgHei=Img.ImgHeight
        self.filter_type = filter_type
        self.save_path = save_path
        self.update_callback = update_callback
        self.configure(bg_color="white", fg_color="white")

        self.camera = None
        self.thread = None
        self.stop_event = threading.Event()
        self.frame = None

        # Frame for camera display
        self.panel = ctk.CTkLabel(self, text="")  # Initialize the panel
        self.panel.pack(fill="both", expand=True)

        self.update_frame()

        # Variables for zoom and pan
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.dragging = False

        # Bind mouse events
        self.panel.bind("<ButtonPress-1>", self.start_drag)
        self.panel.bind("<B1-Motion>", self.do_drag)
        self.panel.bind("<ButtonRelease-1>", self.stop_drag)

    def get_frame(self):
        return self.frame

    def start_camera(self):
        self.stop_event.clear()
        #Change the Camera whit (self.Camera)
        self.camera = Camera(index=self.Camera)
        self.thread = threading.Thread(target=self.read_frame)
        self.thread.start()

    def stop_camera(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        if self.camera:
            self.camera.release()
        self.camera = None

    def apply_filter(self, frame):
        if self.filter_type == "GrayScale":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif self.filter_type == "RedVision":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        elif self.filter_type == "HighlightShadow":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        elif self.filter_type == "OnlyLines":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif self.filter_type == "FrontLines":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif self.filter_type == "Negative":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        return frame

    def read_frame(self):
        while not self.stop_event.is_set():
            ret, frame = self.camera.read_frame()
            if ret:
                frame = self.apply_filter(frame)
                self.frame = frame

    def update_frame(self):
        if self.frame is not None:
            # Aplica el zoom y el desplazamiento
            zoomed_frame = self.apply_zoom_and_pan(self.frame)
            # Ajusta la imagen al panel manteniendo la relación de aspecto
            img = Image.fromarray(cv2.cvtColor(zoomed_frame, cv2.COLOR_BGR2RGB))
            ctk_img = ctk.CTkImage(light_image=img, size=(self.ImgWid, self.ImgHei))
            self.panel.imgtk = ctk_img
            self.panel.configure(image=ctk_img)

        self.after(10, self.update_frame)

    def fit_to_panel(self, frame, size):
        h, w, _ = frame.shape
        panel_width, panel_height = size

        # Calcula el factor de escala para mantener la relación de aspecto
        scale_width = panel_width / w
        scale_height = panel_height / h
        scale = min(scale_width, scale_height)

        # Redimensiona la imagen
        new_width = int(w * scale)
        new_height = int(h * scale)
        resized_image = cv2.resize(frame, (new_width, new_height))

        # Crea una nueva imagen en blanco del tamaño del panel
        result = np.zeros((panel_height, panel_width, 3), dtype=np.uint8)

        # Centra la imagen redimensionada en la imagen en blanco
        x_offset = (panel_width - new_width) // 2
        y_offset = (panel_height - new_height) // 2
        result[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_image

        return result

    def capture_image(self):
        if self.frame is not None:
            zoomed_frame = self.apply_zoom_and_pan(self.frame)
            desired_resolution = (self.ImgWid, self.ImgHei)  # Cambia esto a la resolución deseada
            resized_frame = cv2.resize(zoomed_frame, desired_resolution)
            cv2.imwrite(self.save_path, resized_frame)
            self.update_callback()

    def apply_filter_to_image(self, image, filter_type):
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        if filter_type == "GrayScale":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filter_type == "RedVision":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        elif filter_type == "HighlightShadow":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        elif filter_type == "OnlyLines":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filter_type == "FrontLines":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filter_type == "Negative":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def apply_zoom_and_pan(self, frame):
        h, w, _ = frame.shape
        center_x, center_y = w // 2, h // 2

        # Calcula las nuevas dimensiones basadas en el nivel de zoom
        new_w, new_h = int(w / self.zoom_level), int(h / self.zoom_level)

        # Calcula el área de recorte
        left = int(max(center_x - new_w // 2 + self.pan_x, 0))
        right = int(min(center_x + new_w // 2 + self.pan_x, w))
        top = int(max(center_y - new_h // 2 + self.pan_y, 0))
        bottom = int(min(center_y + new_h // 2 + self.pan_y, h))

        # Limita el desplazamiento para no salir de los bordes de la imagen
        self.pan_x = min(max(self.pan_x, -(center_x - new_w // 2)), center_x - new_w // 2)
        self.pan_y = min(max(self.pan_y, -(center_y - new_h // 2)), center_y - new_h // 2)

        # Recorta la imagen
        cropped_frame = frame[top:bottom, left:right]

        # Redimensiona el marco recortado para que coincida con la resolución del panel
        return cv2.resize(cropped_frame, (self.ImgWid, self.ImgHei))

    def zoom_in(self):
        self.zoom_level = min(self.zoom_level * 1.1, 3.0)

    def zoom_out(self):
        self.zoom_level = max(self.zoom_level / 1.1, 1.0)

    def set_zoom(self, zoom_level):
        self.zoom_level = zoom_level

    def zoom_2x(self):
        self.set_zoom(1.2)

    def zoom_4x(self):
        self.set_zoom(2)

    def zoom_6x(self):
        self.set_zoom(3)

    def zoom_8x(self):
        self.set_zoom(5)

    def move_up(self):
        self.pan_y -= 10 / self.zoom_level
        self.limit_pan()

    def move_down(self):
        self.pan_y += 10 / self.zoom_level
        self.limit_pan()

    def move_left(self):
        self.pan_x -= 10 / self.zoom_level
        self.limit_pan()

    def move_right(self):
        self.pan_x += 10 / self.zoom_level
        self.limit_pan()

    def limit_pan(self):
        if self.frame is not None:
            h, w, _ = self.frame.shape
            zoomed_width = int(w / self.zoom_level)
            zoomed_height = int(h / self.zoom_level)

            # Limita el desplazamiento para que no salga de la imagen
            self.pan_x = min(max(self.pan_x, -(w // 2 - zoomed_width // 2)), w // 2 - zoomed_width // 2)
            self.pan_y = min(max(self.pan_y, -(h // 2 - zoomed_height // 2)), h // 2 - zoomed_height // 2)

    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.dragging = True

    def do_drag(self, event):
        if self.dragging:
            delta_x = event.x - self.drag_start_x
            delta_y = event.y - self.drag_start_y
            self.pan_x += delta_x
            self.pan_y += delta_y
            self.limit_pan()
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            print(f"Dragging: pan_x={self.pan_x}, pan_y={self.pan_y}")

    def stop_drag(self, event):
        self.dragging = False

    def reset_zoom_pan(self):
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        print("Reset zoom and pan")

    def __del__(self):
        self.stop_camera()
