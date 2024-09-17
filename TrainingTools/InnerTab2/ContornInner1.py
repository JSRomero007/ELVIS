import customtkinter as ctk
from PIL import Image, ImageTk
from CameraTools import CameraHandler

class ContorInnerTab1(ctk.CTkFrame):
    def __init__(self, parent, filter_name, num_inspection_zones=2):
        super().__init__(parent, fg_color="white", bg_color="white")
        self.camera_handler = CameraHandler()

        self.lbl = ctk.CTkLabel(self, text="hh")
        self.lbl.pack()

        self.image_label = ctk.CTkLabel(self,text="")
        self.image_label.pack(pady=20)

        self.single_capture_button = ctk.CTkButton(self, text="Capture Single Image", command=self.capture_single_image)
        self.single_capture_button.pack(pady=20)

        self.start_cyclic_button = ctk.CTkButton(self, text="Start Cyclic Capture", command=self.start_cyclic_capture)
        self.start_cyclic_button.pack(pady=20)

        self.stop_cyclic_button = ctk.CTkButton(self, text="Stop Cyclic Capture", command=self.stop_cyclic_capture)
        self.stop_cyclic_button.pack(pady=20)

    def capture_single_image(self):
        self.camera_handler.capture_single_image(self.image_label)

    def start_cyclic_capture(self):
        self.camera_handler.start_cyclic_capture(self.image_label)

    def stop_cyclic_capture(self):
        self.camera_handler.stop_cyclic_capture()
