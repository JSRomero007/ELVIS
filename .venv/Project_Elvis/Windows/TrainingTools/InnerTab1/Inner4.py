import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import cv2
import numpy as np


class InnerTab4Content(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.parent = parent

        self.original_image_path = "C:\\ELVIS\\sin_filtro_inspeccion_1.jpg"
        self.filtered_image_path = "C:\\ELVIS\\con_filtro_inspeccion_1.jpg"
        self.contours_image_path = "C:\\ELVIS\\contornos_inspeccion.jpg"
        self.last_modified_original = 0
        self.last_modified_filtered = 0

        self.low_threshold = 100
        self.high_threshold = 200
        self.drawing = False

        self.init_ui()

    def init_ui(self):
        self.image_frame = tk.Frame(self, bg="white")
        self.image_frame.pack(side=tk.LEFT, padx=0, pady=0)

        self.original_image_label = tk.Label(self.image_frame)
        self.original_image_label.grid(row=0, column=0, padx=10, pady=10)

        self.filtered_image_label = tk.Label(self.image_frame)
        self.filtered_image_label.grid(row=0, column=1, padx=10, pady=10)

        self.contours_image_label = tk.Label(self.image_frame)
        self.contours_image_label.grid(row=0, column=2, padx=10, pady=10)

        self.slider_frame = tk.Frame(self, bg="white")
        self.slider_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.low_threshold_slider = tk.Scale(self.slider_frame, from_=0, to=255, label="Low Threshold",
                                             orient=tk.HORIZONTAL, command=self.update_low_threshold)
        self.low_threshold_slider.set(self.low_threshold)
        self.low_threshold_slider.pack(padx=5, pady=5)

        self.high_threshold_slider = tk.Scale(self.slider_frame, from_=0, to=255, label="High Threshold",
                                              orient=tk.HORIZONTAL, command=self.update_high_threshold)
        self.high_threshold_slider.set(self.high_threshold)
        self.high_threshold_slider.pack(padx=5, pady=5)

        self.erase_button = tk.Button(self.slider_frame, text="Erase", command=self.toggle_erase_mode)
        self.erase_button.pack(padx=5, pady=5)

        self.check_images()

    def toggle_erase_mode(self):
        if not self.drawing:
            self.contours_image_label.bind("<ButtonPress-1>", self.on_button_press)
            self.contours_image_label.bind("<B1-Motion>", self.on_mouse_drag)
            self.contours_image_label.bind("<ButtonRelease-1>", self.on_button_release)
            self.erase_button.config(text="Stop Erase")
            self.drawing = True
        else:
            self.contours_image_label.unbind("<ButtonPress-1>")
            self.contours_image_label.unbind("<B1-Motion>")
            self.contours_image_label.unbind("<ButtonRelease-1>")
            self.erase_button.config(text="Erase")
            self.drawing = False

    def on_button_press(self, event):
        self.draw_on_image(event.x, event.y)

    def on_mouse_drag(self, event):
        self.draw_on_image(event.x, event.y)

    def on_button_release(self, event):
        self.save_contours_image()

    def draw_on_image(self, x, y):
        try:
            contours_image = Image.open(self.contours_image_path)
            draw = ImageDraw.Draw(contours_image)
            scale = 2  # Assuming the image is scaled by a factor of 2
            draw.ellipse((x // scale - 5, y // scale - 5, x // scale + 5, y // scale + 5), fill=(0, 0, 0))
            contours_image.save(self.contours_image_path)
            self.load_images()
        except Exception as e:
            print(f"Error drawing on image: {e}")

    def save_contours_image(self):
        try:
            contours_image = Image.open(self.contours_image_path)
            contours_image.save(self.contours_image_path)
        except Exception as e:
            print(f"Error saving contours image: {e}")

    def update_low_threshold(self, value):
        self.low_threshold = int(value)
        self.process_contours_image()
        self.load_images()

    def update_high_threshold(self, value):
        self.high_threshold = int(value)
        self.process_contours_image()
        self.load_images()

    def load_images(self):
        try:
            original_image = Image.open(self.original_image_path)
            filtered_image = Image.open(self.filtered_image_path)
            contours_image = Image.open(self.contours_image_path)

            original_imgtk = ImageTk.PhotoImage(self.resize_image(original_image))
            filtered_imgtk = ImageTk.PhotoImage(self.resize_image(filtered_image))
            contours_imgtk = ImageTk.PhotoImage(self.resize_image(contours_image))

            self.original_image_label.config(image=original_imgtk)
            self.original_image_label.image = original_imgtk

            self.filtered_image_label.config(image=filtered_imgtk)
            self.filtered_image_label.image = filtered_imgtk

            self.contours_image_label.config(image=contours_imgtk)
            self.contours_image_label.image = contours_imgtk

        except Exception as e:
            print(f"Error loading images: {e}")

    def resize_image(self, image, scale=2):
        width, height = image.size
        new_size = (width * scale, height * scale)
        return image.resize(new_size, Image.NEAREST)  # Resize using NEAREST to avoid anti-aliasing

    def check_images(self):
        try:
            original_modified = os.path.getmtime(self.original_image_path)
            filtered_modified = os.path.getmtime(self.filtered_image_path)

            if original_modified != self.last_modified_original or filtered_modified != self.last_modified_filtered:
                self.last_modified_original = original_modified
                self.last_modified_filtered = filtered_modified
                self.process_contours_image()
                self.load_images()

        except FileNotFoundError:
            print("Image not found, waiting for images to be saved...")

        self.after(500, self.check_images)  # Revisa cada 500 milisegundos

    def process_contours_image(self):
        try:
            filtered_image = cv2.imread(self.filtered_image_path, cv2.IMREAD_GRAYSCALE)
            edges = cv2.Canny(filtered_image, self.low_threshold, self.high_threshold)

            # Create an image with green contours on a black background
            contours_image = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)
            contours_image[edges != 0] = [0, 255, 0]

            cv2.imwrite(self.contours_image_path, contours_image)
        except Exception as e:
            print(f"Error processing contours image: {e}")


