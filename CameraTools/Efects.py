import cv2
import numpy as np

class Effects:
    def __init__(self):
        self.saturation_level = 1
        self.effects = []
        self.orb = cv2.ORB_create()
        self.sift = cv2.SIFT_create()
        # self.surf = cv2.xfeatures2d.SURF_create()  # Comentado debido a la limitación de OpenCV

    def apply_effects(self, frame):
        for effect in self.effects:
            if effect == "Original":
                continue
            if effect == "GrayScale":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

            elif effect== "RedVision":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            elif effect == "HighlightShadow":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            elif effect == "OnlyLines":
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

            elif effect == "FrontLines":
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

            elif effect=="Negative":
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        return frame

    def set_saturation_level(self, level):
        self.saturation_level = float(level)

    def add_effect(self, effect):
        if effect not in self.effects:
            self.effects.append(effect)

    def remove_effect(self, effect):
        if effect in self.effects:
            self.effects.remove(effect)

    def clear_effects(self):
        self.effects = []
