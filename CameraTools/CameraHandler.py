import threading
import time
import cv2
from PIL import Image, ImageTk
from customtkinter import CTkCanvas
from Global.GlobalV import Img


class CameraHandler:
    def __init__(self):
        self.current_camera = Img.Camera1  # Inicializar con la primera cámara
        self.cap = cv2.VideoCapture(self.current_camera, cv2.CAP_DSHOW)  # Inicializar la captura de video
        self.is_running = False
        self.stop_event = threading.Event()

    def capture_single_image(self, canvas, retries=3):
        for attempt in range(retries):
            ret, frame = self.cap.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)

                canvas_width = canvas.winfo_width()
                canvas_height = canvas.winfo_height()
                img = img.resize((canvas_width, canvas_height))

                imgtk = ImageTk.PhotoImage(image=img)

                canvas.create_image(0, 0, anchor="nw", image=imgtk)
                canvas.image = imgtk  # Guardar una referencia de la imagen para evitar que se recoja como basura
                return
            else:
                print("Failed to capture image on attempt", attempt + 1)
                self._reconnect_camera()

    def start_cyclic_capture(self, canvas):
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self._run_cyclic_capture(canvas)

    def _run_cyclic_capture(self, canvas):
        if not self.is_running:
            return

        # Verificar si la cámara seleccionada ha cambiado
        if Img.Camera1 != self.current_camera:  # Verificar si la cámara activa es diferente
            self.current_camera = Img.Camera1
            self._switch_camera(self.current_camera)

        ret, frame = self.cap.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)

            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            img = img.resize((canvas_width, canvas_height))

            imgtk = ImageTk.PhotoImage(image=img)

            canvas.create_image(0, 0, anchor="nw", image=imgtk)
            canvas.image = imgtk
        else:
            print("Failed to capture image")
            self._reconnect_camera()

        # Continuar capturando imágenes en tiempo real
        if self.is_running:
            canvas.after(30, self._run_cyclic_capture, canvas)  # Esperar 30 ms entre capturas para tiempo real (~30 FPS)

    def _switch_camera(self, camera):
        print(f"Switching to camera {camera}")
        self.cap.release()
        self.cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)

    def _reconnect_camera(self):
        self.cap.release()
        self.cap = cv2.VideoCapture(self.current_camera, cv2.CAP_DSHOW)

    def stop_cyclic_capture(self):
        self.is_running = False
        self.stop_event.set()

    def get_current_frame(self):
        ret, frame = self.cap.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return Image.fromarray(img)
        else:
            print("Failed to capture image")
            return None

    def __del__(self):
        self.cap.release()
