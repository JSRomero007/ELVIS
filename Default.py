import customtkinter as ctk
from PIL import Image, ImageTk
import os


class DefaultWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg_color="white",fg_color="white")
        # Especifica las dimensiones deseadas
        target_width = 300
        target_height = 200

        image_path = os.path.join("Img","Logo", "FullLogo.png")  # Asegúrate de que esta ruta sea correcta
        image = Image.open(image_path)
        resized_image = image.resize((target_width, target_height))  # Redimensionar sin ANTIALIAS
        photo = ImageTk.PhotoImage(resized_image)

        # Crea un widget de etiqueta y añade la imagen
        label = ctk.CTkLabel(self, image=photo, text="")
        label.image = photo  # Necesario para evitar que la imagen sea recolectada por el recolector de basura

        # Centra la etiqueta en el formulario
        label.place(relx=0.5, rely=0.5, anchor="center")

# Ejemplo de cómo utilizar la clase DefaultWindow en una aplicación customtkinter
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(bg="blue")

        self.default_window = DefaultWindow(self)
        self.default_window.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()