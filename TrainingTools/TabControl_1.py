import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from .InnerTab1 import (InnerTab0Content,
                        InnerTab1Content,
                        InnerTab2Content,
                        InnerTab3Content,
                        InnerTab4Content,
                        InnerTab5Content,
                        InnerTab6Content)

class Tab1Content(ctk.CTkFrame):
    def __init__(self, parent, saved_image_path, main_camera_class, filters,MotherTab):
        super().__init__(parent)
        self.configure(fg_color="Gray", bg_color="white")
        self.saved_image_path = saved_image_path
        self.main_camera_class = main_camera_class
        self.filters = filters
        self.TabControl=MotherTab
        self.main_camera = None
        self.create_content()

    def create_content(self):
        self.inner_tab_control = ctk.CTkTabview(self, fg_color="white", text_color="white", corner_radius=10)
        self.inner_tab_control.pack(padx=10, pady=10, fill="both", expand=True)

        self.inner_tab0 = self.inner_tab_control.add("Setup")
        self.inner_tab2_1 = self.inner_tab_control.add(" | ")
        self.inner_tab1 = self.inner_tab_control.add("Adjust the camera")
        self.inner_tab2_2 = self.inner_tab_control.add(" |  ")
        self.inner_tab3 = self.inner_tab_control.add("Select inspection area")
        self.inner_tab2_3 = self.inner_tab_control.add(" |   ")
        self.inner_tab4 = self.inner_tab_control.add("Evaluation")
        self.inner_tab2_4 = self.inner_tab_control.add(" |    ")
        self.inner_tab5 = self.inner_tab_control.add("Testing")
        #self.inner_tab2_5 = self.inner_tab_control.add(" |     ")
        #self.inner_tab6 = self.inner_tab_control.add("Testing ")


        self.inner_tab0_content = InnerTab0Content(self.inner_tab0,self.inner_tab_control)
        self.inner_tab0_content.pack(fill="both", expand=True)

        inner_tab1_content = InnerTab1Content(self.inner_tab1, self.saved_image_path, self.main_camera_class, self.update_grid, self.inner_tab_control)
        inner_tab1_content.pack(fill="both", expand=True)
        self.main_camera = inner_tab1_content.main_camera

        self.inner_tab2_content = InnerTab2Content(self.inner_tab2_1, self.filters, self.inner_tab_control,self.main_camera_class)
        self.inner_tab2_content.pack(fill="both", expand=True)

        self.inner_tab3_content = InnerTab3Content(self.inner_tab3,self.TabControl, self.inner_tab_control)
        self.inner_tab3_content.pack(fill="both", expand=True)

        self.inner_tab4_content = InnerTab4Content(self.inner_tab4,self.inner_tab_control)
        self.inner_tab4_content.pack(fill="both", expand=True)

        self.inner_tab5_content = InnerTab5Content(self.inner_tab5)
        self.inner_tab5_content.pack(fill="both", expand=True)

        #self.inner_tab6_content = InnerTab6Content(self.inner_tab6)
        #self.inner_tab6_content.pack(fill="both", expand=True)



    def update_grid(self):
        self.inner_tab2_content.update_grid(self.saved_image_path, self.main_camera)
