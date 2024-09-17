import customtkinter as ctk

class Io(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg_color="white", fg_color="white")
        label = ctk.CTkLabel(self, text="Run")
        label.pack(padx=10, pady=10)
