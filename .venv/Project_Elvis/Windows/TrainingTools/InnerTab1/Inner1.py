import customtkinter as ctk
from PIL import Image
from PIL import ImageGrab
from CameraTools import CameraHandler
from Global.GlobalV import Picture,Img



class InnerTab1Content(ctk.CTkFrame):
    def __init__(self, parent, saved_image_path, main_camera_class, update_grid_callback, inner_tab_control):
        super().__init__(parent)
        self.configure(fg_color="white", bg_color="white")
        self.Icons()
        self.saved_image_path = saved_image_path
        self.main_camera_class = main_camera_class
        self.update_grid_callback = update_grid_callback
        self.inner_tab_control = inner_tab_control
        self.main_camera = None  # Inicializar main_camera
        self.camera_handler = CameraHandler()  # Inicializar CameraHandler

        # Estados iniciales de los botones
        self.up_button_state = False
        self.left_button_state = False
        self.center_button_state = False
        self.right_button_state = False
        self.down_button_state = False

        self.top_button1_state = False
        self.top_button2_state = False
        self.top_button3_state = False

        self.UI()

    def UI(self):
        self.grid_rowconfigure(0, minsize=80,weight=0)
        self.grid_rowconfigure(1,minsize=80, weight=1)
        self.grid_rowconfigure(2, weight=4)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, minsize=500,weight=0)

        self.Header()

        text1 = ctk.CTkLabel(self, text="", text_color="black", font=('Consolas', 20))
        text1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        text2 = ctk.CTkLabel(self, text="", text_color="black", font=('Consolas', 20))
        text2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        text3 = ctk.CTkLabel(self, text="", text_color="black", font=('Consolas', 20))
        text3.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)


        self.CameraFrame()

        self.menu_frame = ctk.CTkFrame(self, width=50, fg_color="white", border_width=2, border_color="Gray", bg_color="white")
        self.menu_frame.grid(row=2, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)

        self.BackNextButtons = ctk.CTkFrame(self)
        self.BackNextButtons.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)



        footer = ctk.CTkLabel(self, text="", text_color="black", font=('Consolas', 25, 'bold'))
        footer.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.LightIntensity()
        self.LightDirection()
        self.CaptureOrCancel()

        self.start_button = ctk.CTkButton(self.menu_frame, text="Start Camera", command=self.toggle_camera_capture)
        self.start_button.grid(row=14, column=0, columnspan=3, pady=10)
    def Header(self):
        header = ctk.CTkLabel(self, text="- Preview camera inspection -", text_color="black", font=('Consolas', 20))
        header.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

    def CameraFrame(self):
        camera_frame = ctk.CTkFrame(self,fg_color="white",bg_color="white")
        camera_frame.grid(row=2, column=0, columnspan=2, rowspan=2, sticky="nsew", padx=10, pady=90)

        self.LiveFrame = ctk.CTkFrame(camera_frame, border_width=0, width=Img.ImgWidth, height=Img.ImgHeight)
        self.LiveFrame.pack( expand=False)

        self.canvas = ctk.CTkCanvas(self.LiveFrame, width=Img.ImgWidth, height=Img.ImgHeight)
        self.canvas.pack( expand=False)
    def CaptureOrCancel(self):

        self.ButtonCancel = ctk.CTkButton(self.BackNextButtons,
                                          fg_color="#a1a09f",
                                          text_color="black",
                                          text="Cancel",
                                          font=('Consolas', 20),
                                          command=self.Button_Cancel)


        self.capture_button = ctk.CTkButton(self.BackNextButtons,
                                       fg_color="#FE5202",
                                       text_color="white",
                                       text="Capture",
                                       font=('Consolas', 20),
                                       command=self.Button_Capture)

        self.ButtonCancel.pack(side="left", padx=5, pady=5)
        self.capture_button.pack(side="right", padx=5, pady=5)

    def toggle_camera_capture(self):
        if self.camera_handler.is_running:
            self.camera_handler.stop_cyclic_capture()
            self.start_button.configure(text="Start Camera")
        else:
            self.camera_handler.start_cyclic_capture(self.canvas)
            self.start_button.configure(text="Stop Camera")
    def start_camera_capture(self):
        self.camera_handler.start_cyclic_capture(self.LiveFrame)
    def Icons(self):
        self.LMaxOk = Picture.LightMaxOk
        self.LMaxNo = Picture.LightMaxNo
        self.LMidOk = Picture.LightMidOk
        self.LMidNo = Picture.LightMidNo
        self.LMinOk = Picture.LightMinOk
        self.LMinNo = Picture.LightMinNo

        self.LUpOk = Picture.LightUpOk
        self.LUpNo = Picture.LightUpNo
        self.LDowOk = Picture.LightDowOk
        self.LDowNo = Picture.LightDowNo
        self.LCenOk = Picture.LightCenOk
        self.LCenNo = Picture.LightCenNo
        self.LLefOk = Picture.LightLefOk
        self.LLefNo = Picture.LightLefNo
        self.LRigOk = Picture.LightRigOk
        self.LRigNo = Picture.LightRigNo

        self.CamPl = Picture.CameraPl
        self.CamMi = Picture.CameraMi
        self.CamRe = Picture.CameraRe

        self.RowUp = Picture.RowUP
        self.RowDo = Picture.RowDO
        self.RowLe = Picture.RowLE
        self.RowRi = Picture.RowRI

    def Live(self):
        LiveF = ctk.CTkFrame(self.LiveFrame, fg_color="white", bg_color="white")
        LiveF.pack(side="right")

        label = ctk.CTkLabel(LiveF,
                             text="Live Mode ",
                             font=('Consolas', 25),
                             text_color="black")
        label.grid(row=0, column=0)

        off = ctk.CTkLabel(LiveF, text="Off ",
                           font=('Consolas', 25),
                           text_color="black")
        off.grid(row=0, column=1)

    # Light Intensity 3 Component
    # -----| Min light | Mid Light | Max Light |-----
    def LightIntensity(self):
        Lbl = ctk.CTkLabel(self.menu_frame,
                           text="Select Intensity",
                           text_color="#000000",
                           font=('Consolas', 20))
        Lbl.grid(row=6, column=0, columnspan=3, pady=40, padx=(10, 5), sticky="w")

        size = (10, 10)

        self.top_button1 = ctk.CTkButton(self.menu_frame,
                                         text="",
                                         image=self.LMinNo,
                                         fg_color="white",
                                         width=size[0],
                                         height=size[1],
                                         command=self.Button_MinLight)
        self.top_button1.grid(row=7, column=1)

        self.top_button2 = ctk.CTkButton(self.menu_frame,
                                         text="",
                                         image=self.LMidNo,
                                         fg_color="white",
                                         width=size[0],
                                         height=size[1],
                                         command=self.Button_MidLight)
        self.top_button2.grid(row=7, column=2)

        self.top_button3 = ctk.CTkButton(self.menu_frame,
                                         text="",
                                         image=self.LMaxNo,
                                         fg_color="white",
                                         width=size[0],
                                         height=size[1],
                                         command=self.Button_MaxLight)
        self.top_button3.grid(row=7, column=3)

    # Light Direction 5 Component
    #            | ʌ |
    #        | < | ○ | > |
    #            | v |
    def LightDirection(self):
        size = (10, 10)

        # Agregar botones de control de dirección con imágenes
        self.up_button = ctk.CTkButton(self.menu_frame,
                                       text="",
                                       image=Picture.LightUpNo,
                                       fg_color="white",
                                       command=self.up_action,
                                       width=size[0],
                                       height=size[1])
        self.up_button.grid(row=9, column=2)

        self.left_button = ctk.CTkButton(self.menu_frame,
                                         text="",
                                         image=Picture.LightLefNo,
                                         fg_color="white",
                                         command=self.left_action,
                                         width=size[0],
                                         height=size[1])
        self.left_button.grid(row=10, column=1, sticky="e")

        self.center_button = ctk.CTkButton(self.menu_frame,
                                           text="",
                                           image=Picture.LightCenNo,
                                           fg_color="white",
                                           command=self.center_action,
                                           width=size[0],
                                           height=size[1])
        self.center_button.grid(row=10, column=2)

        self.right_button = ctk.CTkButton(self.menu_frame,
                                          text="",
                                          image=Picture.LightRigNo,
                                          fg_color="white",
                                          command=self.right_action,
                                          width=size[0],
                                          height=size[1])
        self.right_button.grid(row=10, column=3, sticky="w")

        self.down_button = ctk.CTkButton(self.menu_frame,
                                         text="",
                                         image=Picture.LightDowNo,
                                         fg_color="white",
                                         command=self.down_action,
                                         width=size[0],
                                         height=size[1])
        self.down_button.grid(row=11, column=2)

    # Capture or Cancel Option 2 Component
    # -----| Cancel | Capture |-----
    def Button_Capture(self):
        # Obtener el frame actual de la cámara
        frame = self.camera_handler.get_current_frame()

        if frame:
            # Guardar el frame en la ruta especificada
            frame.save(self.saved_image_path, format="JPEG")
            print(f"Imagen guardada en {self.saved_image_path}")

            self.toggle_camera_capture()

            # Cambiar a la siguiente pestaña
            self.inner_tab_control.set("Select inspection area")
        else:
            print("No se pudo capturar la imagen")

    def Button_Cancel(self):
        self.StartCamera()
        print("cancel")

    def StartCamera(self):
        if self.SwitchCamera.get():
            if self.main_camera:
                self.main_camera.start_camera()
        else:
            if self.main_camera:
                self.main_camera.stop_camera()

    def up_action(self):
        self.toggle_button("up")
        print("Up button pressed, current state:", self.up_button_state)

    def down_action(self):
        self.toggle_button("down")
        print("Down button pressed")

    def left_action(self):
        self.toggle_button("left")
        print("Left button pressed")

    def right_action(self):
        self.toggle_button("right")
        print("Right button pressed")

    def center_action(self):
        self.toggle_button("center")
        print("Center button pressed")

    def toggle_button(self, button_name):
        # Toggle the state of the button
        if button_name == "up":
            self.up_button_state = not self.up_button_state
            self.up_button.configure(image=Picture.LightUpOk if self.up_button_state else Picture.LightUpNo)
            print("Up button toggled, new state:", self.up_button_state)
        elif button_name == "down":
            self.down_button_state = not self.down_button_state
            self.down_button.configure(image=Picture.LightDowOk if self.down_button_state else Picture.LightDowNo)
        elif button_name == "left":
            self.left_button_state = not self.left_button_state
            self.left_button.configure(image=Picture.LightLefOk if self.left_button_state else Picture.LightLefNo)
        elif button_name == "right":
            self.right_button_state = not self.right_button_state
            self.right_button.configure(image=Picture.LightRigOk if self.right_button_state else Picture.LightRigNo)
        elif button_name == "center":
            self.center_button_state = not self.center_button_state
            self.center_button.configure(image=Picture.LightCenOk if self.center_button_state else Picture.LightCenNo)

        # Check if all buttons except center are selected
        if (self.up_button_state and self.left_button_state and
                self.right_button_state and self.down_button_state and
                not self.center_button_state):
            # Automatically select center and deselect others
            self.center_button_state = True
            self.center_button.configure(image=Picture.LightCenOk)
            self.up_button_state = self.left_button_state = self.right_button_state = self.down_button_state = False
            self.up_button.configure(image=Picture.LightUpNo)
            self.left_button.configure(image=Picture.LightLefNo)
            self.right_button.configure(image=Picture.LightRigNo)
            self.down_button.configure(image=Picture.LightDowNo)
        elif self.center_button_state:
            # If center is selected, deselect all other buttons
            self.up_button_state = self.left_button_state = self.right_button_state = self.down_button_state = False
            self.up_button.configure(image=Picture.LightUpNo)
            self.left_button.configure(image=Picture.LightLefNo)
            self.right_button.configure(image=Picture.LightRigNo)
            self.down_button.configure(image=Picture.LightDowNo)

    def deselect_other_buttons(self, selected_button):
        if selected_button != self.top_button1 and self.top_button1_state:
            self.top_button1.configure(image=self.LMinNo)
            self.top_button1_state = False
        if selected_button != self.top_button2 and self.top_button2_state:
            self.top_button2.configure(image=self.LMidNo)
            self.top_button2_state = False
        if selected_button != self.top_button3 and self.top_button3_state:
            self.top_button3.configure(image=selfe.LMaxNo)
            self.top_button3_state = False

    # -----|Min light | Mid Light | Max Light |-----
    def Button_MinLight(self):
        if self.top_button1_state:
            self.top_button1.configure(image=self.LMinNo)
            self.top_button1_state = False
            print("Minlight disable")
        else:
            self.deselect_other_buttons(self.top_button1)
            self.top_button1.configure(image=self.LMinOk)
            self.top_button1_state = True
            print("Minlight enabled")
    def Button_MidLight(self):
        if self.top_button2_state:
            self.top_button2.configure(image=self.LMidNo)
            self.top_button2_state = False
            print("Mid light disabled")
        else:
            self.deselect_other_buttons(self.top_button2)
            self.top_button2.configure(image=self.LMidOk)
            self.top_button2_state = True
            print("Mid light enabled")
    def Button_MaxLight(self):
        if self.top_button3_state:
            self.top_button3.configure(image=self.LMaxNo)
            self.top_button3_state = False
            print("Max light disabled")
        else:
            self.deselect_other_buttons(self.top_button3)
            self.top_button3.configure(image=self.LMaxOk)
            self.top_button3_state = True
            print("Max light enabled")
    def move_up(self):
        self.main_camera.move_up()
    def move_down(self):
        self.main_camera.move_down()
    def move_left(self):
        self.main_camera.move_left()
    def move_right(self):
        self.main_camera.move_right()