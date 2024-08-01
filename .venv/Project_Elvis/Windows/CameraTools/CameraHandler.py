import threading
import time
import cv2
from PIL import Image, ImageTk
from customtkinter import CTkCanvas
from Global.GlobalV import Img


class CameraHandler:
    def __init__(self):
        self.cap = cv2.VideoCapture(Img.Camera, cv2.CAP_DSHOW)  # Cambiar el backend a DirectShow
        self.is_running = False
        self.stop_event = threading.Event()

    def capture_single_image(self, canvas, retries=3):
        for attempt in range(retries):
            ret, frame = self.cap.read()
            if ret:
                # Convertir la imagen de OpenCV a PIL
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)

                # Redimensionar la imagen al tamaño del canvas sin usar ANTIALIAS
                canvas_width = canvas.winfo_width()
                canvas_height = canvas.winfo_height()
                img = img.resize((canvas_width, canvas_height))

                imgtk = ImageTk.PhotoImage(image=img)

                # Mostrar la imagen en el canvas
                canvas.create_image(0, 0, anchor="nw", image=imgtk)
                canvas.image = imgtk  # Guardar una referencia de la imagen para evitar que se recoja como basura
                return
            else:
                print("Failed to capture image on attempt", attempt + 1)
                self.cap.release()  # Liberar la cámara
                self.cap = cv2.VideoCapture(Img.Camera, cv2.CAP_DSHOW)  # Intentar reconectar la cámara con DirectShow

    def start_cyclic_capture(self, canvas):
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self._run_cyclic_capture(canvas)

    def _run_cyclic_capture(self, canvas):
        if not self.is_running:
            return
        ret, frame = self.cap.read()
        if ret:
            # Convertir la imagen de OpenCV a PIL
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)

            # Redimensionar la imagen al tamaño del canvas sin usar ANTIALIAS
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            img = img.resize((canvas_width, canvas_height))

            imgtk = ImageTk.PhotoImage(image=img)

            # Mostrar la imagen en el canvas usando el método after para asegurar que se ejecute en el hilo principal
            canvas.create_image(0, 0, anchor="nw", image=imgtk)
            canvas.image = imgtk  # Guardar una referencia de la imagen para evitar que se recoja como basura
        else:
            print("Failed to capture image")
            self.cap.release()  # Liberar la cámara
            self.cap = cv2.VideoCapture(Img.Camera, cv2.CAP_DSHOW)  # Intentar reconectar la cámara con DirectShow

        # Continuar capturando imágenes si no se ha solicitado detener
        if self.is_running:
            canvas.after(100, self._run_cyclic_capture, canvas)  # Esperar 100 ms entre capturas

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
