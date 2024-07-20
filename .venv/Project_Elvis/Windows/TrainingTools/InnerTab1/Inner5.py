import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import cv2
import numpy as np

class InnerTab5Content(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.parent = parent