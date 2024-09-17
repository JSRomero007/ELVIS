import cv2
import numpy as np

class Filters:
    def apply_filter(self, roi, filter_name):
        if filter_name == "RedVision":
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi_red = np.zeros((roi_gray.shape[0], roi_gray.shape[1], 3), dtype=np.uint8)
            roi_red[:, :, 0] = roi_gray
            return roi_red

        elif filter_name == "GrayScale":
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(roi_gray, cv2.COLOR_GRAY2BGR)

        elif filter_name == "HighlightShadow":
            return cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        elif filter_name == "OnlyLines":
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi_thresh = cv2.adaptiveThreshold(roi_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            return cv2.cvtColor(roi_thresh, cv2.COLOR_GRAY2BGR)

        elif filter_name == "FrontLines":
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, roi_thresh = cv2.threshold(roi_gray, 127, 255, cv2.THRESH_BINARY)
            roi_thresh = cv2.cvtColor(roi_thresh, cv2.COLOR_GRAY2BGR)
            roi_final = cv2.adaptiveThreshold(cv2.cvtColor(roi_thresh, cv2.COLOR_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            return cv2.cvtColor(roi_final, cv2.COLOR_GRAY2BGR)

        elif filter_name == "Negative":
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, roi_thresh = cv2.threshold(roi_gray, 127, 255, cv2.THRESH_BINARY)
            return cv2.cvtColor(roi_thresh, cv2.COLOR_GRAY2BGR)

        else:
            return roi
