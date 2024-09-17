import threading
import cv2

class CameraHandler:
    def __init__(self):
        self.cap = None
        self.is_running = False
        self.thread = None

    def start_camera(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_camera)
            self.thread.start()

    def _run_camera(self):
        self.cap = cv2.VideoCapture(1)
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                # Aquí puedes agregar el código para mostrar la imagen en tu GUI
                cv2.imshow('Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def stop_camera(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()

    def is_camera_running(self):
        return self.is_running
