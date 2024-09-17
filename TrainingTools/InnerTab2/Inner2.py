import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk

class InnerTab2Content(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_content()

    def create_content(self):
        self.inner_tab_control = ctk.CTkLabel(self, text="Training", fg_color="white", text_color="black", corner_radius=10)
        self.inner_tab_control.pack(pady=10)

        # Botón para activar la cámara y realizar la comparación
        self.trigger_button = ctk.CTkButton(self, text="Trigger", command=self.trigger_comparison)
        self.trigger_button.pack(pady=10)

        # Canvas para mostrar la imagen
        self.image_canvas = ctk.CTkCanvas(self, width=600, height=600)
        self.image_canvas.pack()

        # Coordenadas y tamaño de la zona de inspección
        self.x = 100
        self.y = 100
        self.width = 50
        self.height = 50

        # Rutas de las imágenes buenas y malas
        self.good_image_path = 'path_to_good_images'
        self.bad_image_path = 'path_to_bad_images'

    def trigger_comparison(self):
        # Capturar imagen desde la cámara
        self.current_image = self.capture_image()

        # Convertir la imagen a un formato compatible con Tkinter
        self.display_image(self.current_image)

        # Comparar con imágenes buenas y malas
        good_result = self.compare_with_images(self.good_image_path)
        bad_result = self.compare_with_images(self.bad_image_path)

        # Mostrar resultado de la comparación
        if good_result < bad_result:
            print("La imagen es buena.")
        else:
            print("La imagen es mala.")

    def capture_image(self):
        # Capturar imagen desde la cámara (aquí puedes personalizar la captura según tu cámara)
        cap = cv2.VideoCapture(1)
        ret, frame = cap.read()
        cap.release()
        return frame

    def display_image(self, image):
        # Dibujar el rectángulo y la etiqueta en la imagen
        annotated_image = image.copy()
        cv2.rectangle(annotated_image, (self.x, self.y), (self.x + self.width, self.y + self.height), (0, 255, 0), 2)
        cv2.putText(annotated_image, "Inspection 1", (self.x, self.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convertir la imagen de OpenCV a PIL
        image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        tk_image = ImageTk.PhotoImage(pil_image)

        # Mostrar la imagen en el canvas
        self.image_canvas.create_image(0, 0, anchor="nw", image=tk_image)
        self.image_canvas.image = tk_image

    def compare_with_images(self, folder_path):
        # Extraer la zona de inspección de la imagen actual
        current_zone = self.get_inspection_zone(self.current_image, self.x, self.y, self.width, self.height)

        # Comparar con imágenes en la carpeta especificada
        similarity_sum = 0
        image_files = [f'{folder_path}/{i}.jpg' for i in range(1, 4)]  # Ajusta según tu estructura de archivos

        for path in image_files:
            registered_image = cv2.imread(path)
            if registered_image is not None:
                registered_zone = self.get_inspection_zone(registered_image, self.x, self.y, self.width, self.height)
                similarity = self.compare_using_fourier(current_zone, registered_zone)
                similarity_sum += similarity

        return similarity_sum

    def compare_using_fourier(self, img1, img2):
        # Convertir las imágenes a escala de grises
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Aplicar la Transformada de Fourier
        f1 = np.fft.fft2(gray1)
        f2 = np.fft.fft2(gray2)

        # Desplazar el componente de frecuencia cero al centro del espectro
        f1_shift = np.fft.fftshift(f1)
        f2_shift = np.fft.fftshift(f2)

        # Calcular la magnitud del espectro de Fourier
        magnitude_spectrum1 = 20 * np.log(np.abs(f1_shift))
        magnitude_spectrum2 = 20 * np.log(np.abs(f2_shift))

        # Calcular la diferencia entre los espectros de Fourier
        difference = np.abs(magnitude_spectrum1 - magnitude_spectrum2)
        similarity = np.sum(difference)

        return similarity

    def get_inspection_zone(self, image, x, y, width, height):
        return image[y:y+height, x:x+width]

