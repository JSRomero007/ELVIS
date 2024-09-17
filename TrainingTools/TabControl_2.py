import customtkinter as ctk
from  .InnerTab2 import (ContorInnerTab1,
                         IAInner1,
                         InnerTab1Content,
                         InnerTab2Content)
from Global.GlobalV import Inherit
'''

        enabled_2, start_x_2, start_y_2, size_x_2, size_y_2 = self.process_data_string(Inherit.Inspection2)
        self.label2.configure(
            text=f"Datos de Inspección 2: Enabled: {enabled_2}, Start X: {start_x_2}, Start Y: {start_y_2}, Size X: {size_x_2}, Size Y: {size_y_2}")
    def process_data_string(self, data_string):
        parts = data_string.split(',')
        enabled = parts[0]
        start_x = parts[1]
        start_y = parts[2]
        size_x = parts[3]
        size_y = parts[4]
        return enabled, start_x, start_y, size_x, size_y
'''
class Tab2Content(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.Filter=filter
        self.create_content()

    def create_content(self):
        self.inner_tab_control = ctk.CTkTabview(self, fg_color="white", text_color="white", corner_radius=10)
        self.inner_tab_control.pack(padx=10, pady=10, fill="both", expand=True)

        self.inner_tab1 = self.inner_tab_control.add("Image history")
        self.inner_tab2 = self.inner_tab_control.add("Training")

        inner_tab1_content = ContorInnerTab1(self.inner_tab1, self.Filter)
        inner_tab1_content.pack(fill="both", expand=True)

        #inner_tab1_content = InnerTab2Content(self.inner_tab2)
        #inner_tab1_content.pack(fill="both", expand=True)