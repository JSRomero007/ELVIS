import cv2

class Camera:
    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)

    def read_frame(self):
        ret, frame = self.cap.read()
        return ret, frame

    def set_focus(self, value):
        self.cap.set(cv2.CAP_PROP_FOCUS, int(value))

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
