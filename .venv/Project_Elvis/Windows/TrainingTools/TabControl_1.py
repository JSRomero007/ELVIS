import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from .InnerTab1 import InnerTab1Content, InnerTab2Content, InnerTab3Content

class Tab1Content(ctk.CTkFrame):
    def __init__(self, parent, saved_image_path, main_camera_class, filters):
        super().__init__(parent)
        self.configure(fg_color="Gray", bg_color="white")
        self.saved_image_path = saved_image_path
        self.main_camera_class = main_camera_class
        self.filters = filters
        self.main_camera = None
        self.create_content()

    def create_content(self):
        self.inner_tab_control = ctk.CTkTabview(self, fg_color="white", text_color="white", corner_radius=10)
        self.inner_tab_control.pack(padx=10, pady=10, fill="both", expand=True)

        self.inner_tab1 = self.inner_tab_control.add("Adjust the camera")
        self.inner_tab2 = self.inner_tab_control.add("Select the filter")
        self.inner_tab3 = self.inner_tab_control.add("Select inspection area")

        inner_tab1_content = InnerTab1Content(self.inner_tab1, self.saved_image_path, self.main_camera_class, self.update_grid, self.inner_tab_control)
        inner_tab1_content.pack(fill="both", expand=True)
        self.main_camera = inner_tab1_content.main_camera

        self.inner_tab2_content = InnerTab2Content(self.inner_tab2, self.filters, self.inner_tab_control,self.main_camera_class)
        self.inner_tab2_content.pack(fill="both", expand=True)

        self.inner_tab3_content = InnerTab3Content(self.inner_tab3)
        self.inner_tab3_content.pack(fill="both", expand=True)

    def update_grid(self):
        self.inner_tab2_content.update_grid(self.saved_image_path, self.main_camera)
