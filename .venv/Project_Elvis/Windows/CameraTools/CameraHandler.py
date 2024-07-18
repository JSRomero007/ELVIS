import threading
import cv2
import time
from PIL import Image, ImageTk


class CameraHandler:
    def __init__(self):
        self.cap = cv2.VideoCapture(1)
        self.is_running = False
        self.thread = None
        self.stop_event = threading.Event()

    def capture_single_image(self, label):
        ret, frame = self.cap.read()
        if ret:
            # Convertir la imagen de OpenCV a PIL
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)

            # Mostrar la imagen en la etiqueta
            label.imgtk = imgtk
            label.configure(image=imgtk)
        else:
            print("Failed to capture image")

    def start_cyclic_capture(self, label):
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._run_cyclic_capture, args=(label,))
            self.thread.start()

    def _run_cyclic_capture(self, label):
        while not self.stop_event.is_set():
            ret, frame = self.cap.read()
            if ret:
                # Convertir la imagen de OpenCV a PIL
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)

                # Mostrar la imagen en la etiqueta
                label.imgtk = imgtk
                label.configure(image=imgtk)
            else:
                print("Failed to capture image")
            time.sleep(0.1)  # Esperar 100 ms entre capturas
        cv2.destroyAllWindows()

    def stop_cyclic_capture(self):
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            self.thread.join()

    def __del__(self):
        self.cap.release()
