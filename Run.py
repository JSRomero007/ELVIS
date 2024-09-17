import customtkinter as ctk
from RunTools import Simple


# Define el RUNModel como el formulario principal
class RUNModel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(bg_color="white", fg_color="white")

        self.child_form = Simple(self)
        self.child_form.pack(padx=20, pady=20, fill="both", expand=True)

'''
if __name__ == "__main__":
    app = RUNModel()
    app.mainloop()'''