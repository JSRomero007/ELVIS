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
        self.zoom_factor = 1.0
        self.start_x = 0
        self.start_y = 0
        self.offset_x = 0
        self.offset_y = 0

        self.circles = []

        self.init_ui()

    def init_ui(self):
        self.pack(fill="both", expand=True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, minsize=150)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        self.header_label = tk.Label(self, text="Encabezado", bg="white", font=("Arial", 16))
        self.header_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Add text labels in row 1
        self.original_text_label = tk.Label(self, text="Original Image", bg="#f0f0f0", font=("Arial", 12))
        self.original_text_label.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.filtered_text_label = tk.Label(self, text="Filtered Image", bg="#f0f0f0", font=("Arial", 12))
        self.filtered_text_label.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.contours_text_label = tk.Label(self, text="Contours Image", bg="#f0f0f0", font=("Arial", 12))
        self.contours_text_label.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

        self.contours_text_label = tk.Label(self, text="Configuration", bg="white", font=("Arial", 12))
        self.contours_text_label.grid(row=1, column=3, padx=10, pady=5, sticky="nsew")

        self.original_image_canvas = tk.Canvas(self, bg="white")
        self.original_image_canvas.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.filtered_image_canvas = tk.Canvas(self, bg="white")
        self.filtered_image_canvas.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.contours_image_canvas = tk.Canvas(self, bg="white")
        self.contours_image_canvas.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.slider_frame = tk.Frame(self, bg="white")
        self.slider_frame.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        self.low_threshold_slider = tk.Scale(self.slider_frame, from_=0, to=255, label="Low Threshold",
                                             orient=tk.HORIZONTAL, command=self.update_low_threshold)
        self.low_threshold_slider.set(self.low_threshold)
        self.low_threshold_slider.pack(padx=5, pady=5)

        self.high_threshold_slider = tk.Scale(self.slider_frame, from_=0, to=255, label="High Threshold",
                                              orient=tk.HORIZONTAL, command=self.update_high_threshold)
        self.high_threshold_slider.set(self.high_threshold)
        self.high_threshold_slider.pack(padx=5, pady=5)

        self.draw_button = tk.Button(self.slider_frame, text="Draw Circles", command=self.toggle_draw_mode)
        self.draw_button.pack(padx=5, pady=5)

        self.zoom_in_button = tk.Button(self.slider_frame, text="+ Zoom", command=self.zoom_in)
        self.zoom_in_button.pack(padx=5, pady=5)

        self.zoom_out_button = tk.Button(self.slider_frame, text="- Zoom", command=self.zoom_out)
        self.zoom_out_button.pack(padx=5, pady=5)

        self.lock_controls_var = tk.BooleanVar(value=False)
        self.lock_controls_checkbox = tk.Checkbutton(self.slider_frame, text="Lock Controls",
                                                     variable=self.lock_controls_var)
        self.lock_controls_checkbox.pack(padx=5, pady=5)

        self.text_label = tk.Label(self, text="Este es un texto en la fila 4, columnas 1 a 4", bg="white",
                                   font=("Arial", 14))
        self.text_label.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.contours_image_canvas.bind("<Button-2>", self.on_scroll_button_press)
        self.contours_image_canvas.bind("<B2-Motion>", self.on_scroll_mouse_drag)
        self.contours_image_canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self.check_images()

    def toggle_draw_mode(self):
        if not self.drawing:
            self.contours_image_canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.contours_image_canvas.bind("<B1-Motion>", self.on_mouse_drag)
            self.contours_image_canvas.bind("<ButtonRelease-1>", self.on_button_release)
            self.draw_button.config(text="Stop Drawing")
            self.drawing = True
        else:
            self.contours_image_canvas.unbind("<ButtonPress-1>")
            self.contours_image_canvas.unbind("<B1-Motion>")
            self.contours_image_canvas.unbind("<ButtonRelease-1>")
            self.draw_button.config(text="Draw Circles")
            self.drawing = False

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        self.draw_circle(event)

    def on_button_release(self, event):
        self.save_contours_image()

    def draw_circle(self, event):
        try:
            contours_image = Image.open(self.contours_image_path)
            draw = ImageDraw.Draw(contours_image)

            canvas_width = self.contours_image_canvas.winfo_width()
            canvas_height = self.contours_image_canvas.winfo_height()
            image_width = contours_image.width
            image_height = contours_image.height

            x = (self.start_x - (canvas_width - image_width * self.zoom_factor) // 2 - self.offset_x) / self.zoom_factor
            y = (self.start_y - (canvas_height - image_height * self.zoom_factor) // 2 - self.offset_y) / self.zoom_factor

            end_x = (event.x - (canvas_width - image_width * self.zoom_factor) // 2 - self.offset_x) / self.zoom_factor
            end_y = (event.y - (canvas_height - image_height * self.zoom_factor) // 2 - self.offset_y) / self.zoom_factor

            radius = int(((end_x - x) ** 2 + (end_y - y) ** 2) ** 0.5)

            if 0 <= x < image_width and 0 <= y < image_height:
                draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=(255, 0, 0), width=2)
                self.circles.append((x, y, radius))
                contours_image.save(self.contours_image_path)
                self.load_images()
        except Exception as e:
            print(f"Error drawing on image: {e}")

    def save_contours_image(self):
        try:
            contours_image = cv2.imread(self.contours_image_path)
            save_path = os.path.join(os.path.dirname(self.contours_image_path), "contornos_guardados.jpg")
            cv2.imwrite(save_path, contours_image)
            print(f"Contours image saved to {save_path}")
            for circle in self.circles:
                print(f"Circle at x: {circle[0]}, y: {circle[1]} with radius: {circle[2]}")
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

    def zoom_in(self):
        if self.zoom_factor < 9.0:
            self.zoom_factor *= 1.2
            self.load_images()

    def zoom_out(self):
        if self.zoom_factor > 0.5:
            self.zoom_factor /= 1.2
            self.load_images()

    def on_mouse_wheel(self, event):
        if self.lock_controls_var.get():
            return
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def on_scroll_button_press(self, event):
        if self.lock_controls_var.get():
            return
        self.start_x = event.x
        self.start_y = event.y

    def on_scroll_mouse_drag(self, event):
        if self.lock_controls_var.get():
            return
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.offset_x += dx
        self.offset_y += dy
        self.start_x = event.x
        self.start_y = event.y
        self.load_images()

    def resize_image(self, image):
        width, height = image.size
        new_size = (int(width * self.zoom_factor), int(height * self.zoom_factor))
        resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
        return resized_image

    def apply_offset(self, image):
        canvas = Image.new('RGB', (self.contours_image_canvas.winfo_width(), self.contours_image_canvas.winfo_height()), (255, 255, 255))
        paste_x = (self.contours_image_canvas.winfo_width() - image.width) // 2 + self.offset_x
        paste_y = (self.contours_image_canvas.winfo_height() - image.height) // 2 + self.offset_y
        canvas.paste(image, (paste_x, paste_y))
        return canvas

    def load_images(self):
        try:
            original_image = Image.open(self.original_image_path)
            filtered_image = Image.open(self.filtered_image_path)
            contours_image = Image.open(self.contours_image_path)

            original_imgtk = ImageTk.PhotoImage(self.apply_offset(self.resize_image(original_image)))
            filtered_imgtk = ImageTk.PhotoImage(self.apply_offset(self.resize_image(filtered_image)))
            contours_imgtk = ImageTk.PhotoImage(self.apply_offset(self.resize_image(contours_image)))

            self.original_image_canvas.create_image(0, 0, anchor="nw", image=original_imgtk)
            self.original_image_canvas.image = original_imgtk
            self.original_image_canvas.config(scrollregion=self.original_image_canvas.bbox("all"))

            self.filtered_image_canvas.create_image(0, 0, anchor="nw", image=filtered_imgtk)
            self.filtered_image_canvas.image = filtered_imgtk
            self.filtered_image_canvas.config(scrollregion=self.filtered_image_canvas.bbox("all"))

            self.contours_image_canvas.create_image(0, 0, anchor="nw", image=contours_imgtk)
            self.contours_image_canvas.image = contours_imgtk
            self.contours_image_canvas.config(scrollregion=self.contours_image_canvas.bbox("all"))

        except Exception as e:
            print(f"Error loading images: {e}")

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

        self.after(500, self.check_images)

    def process_contours_image(self):
        try:
            filtered_image = cv2.imread(self.filtered_image_path, cv2.IMREAD_GRAYSCALE)
            edges = cv2.Canny(filtered_image, self.low_threshold, self.high_threshold)

            # Encontrar los contornos
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Dibujar los contornos
            contours_image = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)
            cv2.drawContours(contours_image, contours, -1, (0, 255, 0), 2)

            # Guardar la imagen de contornos
            cv2.imwrite(self.contours_image_path, contours_image)

            # Guardar el contorno base para usarlo en comparaciones
            self.base_contour = contours[0] if contours else None
        except Exception as e:
            print(f"Error processing contours image: {e}")
