import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from Global.GlobalV import Inherit


class InnerTab2Content(ctk.CTkFrame):
    def __init__(self, parent, filters, inner_tab_control, main_camera_class):
        super().__init__(parent)
        self.filters = [f for f in filters if f not in ["RedVision", "HighlightShadow"]]  # Filtrar los filtros no deseados
        self.main_camera_class = main_camera_class
        self.grid_frame = None
        self.main_camera = None  # Inicializar main_camera
        self.inner_tab_control = inner_tab_control
        self.create_content()
    def StartCamera(self):
        if self.main_camera:
            self.main_camera.start_camera()
    def create_content(self):
        self.add_text_to_tab("Selection the best filter whit your aplication ", ("Consolas", 20, "bold"))
        self.create_grid()
    def add_text_to_tab(self, text, font):
        label = ctk.CTkLabel(self, text=text, font=font)
        label.pack(pady=10, padx=10)
    def create_grid(self):
        grid_frame = ctk.CTkFrame(self, bg_color="white", fg_color="white")
        grid_frame.pack(pady=10, padx=10, fill="both", expand=True)

        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                if index < 3:
                    pass
                elif index < len(self.filters) + 3:
                    filter_frame = ctk.CTkFrame(grid_frame,fg_color="white",bg_color="white",border_width=2,border_color="black")
                    filter_frame.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                    filter_button = ctk.CTkButton(filter_frame,
                                                  text=self.filters[index - 3],
                                                  font=("Consolas", 25, "bold"),
                                                  text_color="black",
                                                  fg_color="#CBCBCB",
                                                   width=10,
                                                  command=lambda
                                                  ft=self.filters[index - 3]:self.SeeFilter(ft))
                    filter_button.pack(fill="both", padx=5,pady=5)
                    image_label = ctk.CTkLabel(filter_frame, text="")
                    image_label.pack(fill="both", expand=True,pady=2,padx=2)
                    setattr(self, f"cell_{index}", image_label)
                else:
                    label = ctk.CTkLabel(grid_frame, text="")
                    label.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

        for i in range(3):
            grid_frame.grid_columnconfigure(i, weight=1)
            grid_frame.grid_rowconfigure(i, weight=1)

        self.grid_frame = grid_frame
    def SeeFilter(self, filter_type):

        Inherit.SelectionFilter=filter_type
        print(Inherit.SelectionFilter)
        self.StartCamera()
        self.inner_tab_control.set("Select inspection area")
    def update_grid(self, saved_image_path, main_camera):
        original_image = Image.open(saved_image_path)
        cell_width = self.grid_frame.winfo_width() // 3
        cell_height = self.grid_frame.winfo_height() // 3

        if cell_width <= 0 or cell_height <= 0:
            self.after(100, lambda: self.update_grid(saved_image_path, main_camera))
            return

        for i, filter_type in enumerate(self.filters, start=3):
            filtered_image = main_camera.apply_filter_to_image(original_image, filter_type)
            resized_image = filtered_image.resize((cell_width, cell_height), Image.NEAREST)
            img = CTkImage(light_image=resized_image, size=(cell_width, cell_height))
            label = getattr(self, f"cell_{i}")
            label.configure(image=img)
            label.image = img
