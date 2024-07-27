import threading
import time
import cv2
from PIL import Image, ImageTk
from customtkinter import CTkCanvas
from Global.GlobalV import Img

class CameraHandler:
    def __init__(self):
        self.cap = cv2.VideoCapture(Img.Camera)
        self.is_running = False
        self.thread = None
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
                self.cap = cv2.VideoCapture(1)  # Intentar reconectar la cámara

    def start_cyclic_capture(self, canvas):
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._run_cyclic_capture, args=(canvas,))
            self.thread.start()

    def _run_cyclic_capture(self, canvas):
        while not self.stop_event.is_set():
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
            else:
                print("Failed to capture image")
                self.cap.release()  # Liberar la cámara
                self.cap = cv2.VideoCapture(Img.Camera)  # Intentar reconectar la cámara
            time.sleep(0.1)  # Esperar 100 ms entre capturas
        cv2.destroyAllWindows()

    def stop_cyclic_capture(self):
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            self.thread.join()

    def __del__(self):
        self.cap.release()