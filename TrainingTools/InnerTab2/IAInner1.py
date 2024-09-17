
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import numpy as np
from CameraTools import Filters
from Global.GlobalV import Inherit, Img
import os
import threading

class IAInnerTab1(ctk.CTkFrame):

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

