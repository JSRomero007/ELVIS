import customtkinter as ctk
from PIL import Image
from Global.GlobalV import Picture

LMaxOk = Picture.LightMaxOk
LMaxNo = Picture.LightMaxNo
LMidOk = Picture.LightMidOk
LMidNo = Picture.LightMidNo
LMinOk = Picture.LightMinOk
LMinNo = Picture.LightMinNo

LUpOk = Picture.LightUpOk
LUpNo = Picture.LightUpNo
LDowOk = Picture.LightDowOk
LDowNo = Picture.LightDowNo
LCenOk = Picture.LightCenOk
LCenNo = Picture.LightCenNo
LLefOk = Picture.LightLefOk
LLefNo = Picture.LightLefNo
LRigOk = Picture.LightRigOk
LRigNo = Picture.LightRigNo

CamPl = Picture.CameraPl
CamMi = Picture.CameraMi
CamRe = Picture.CameraRe

RowUp = Picture.RowUP
RowDo = Picture.RowDO
RowLe = Picture.RowLE
RowRi = Picture.RowRI

class InnerTab1Content(ctk.CTkFrame):
    def __init__(self, parent, saved_image_path, main_camera_class, update_grid_callback, inner_tab_control):
        super().__init__(parent)
        self.configure(fg_color="white", bg_color="white")
        self.saved_image_path = saved_image_path
        self.main_camera_class = main_camera_class
        self.update_grid_callback = update_grid_callback
        self.inner_tab_control = inner_tab_control
        self.main_camera = None  # Inicializar main_camera

        # Estados iniciales de los botones
        self.up_button_state = False
        self.left_button_state = False
        self.center_button_state = False
        self.right_button_state = False
        self.down_button_state = False

        self.top_button1_state = False
        self.top_button2_state = False
        self.top_button3_state = False

        self.create_inner1_layout()
    def create_inner1_layout(self):
        # Crear un frame para la cámara y el menú
        inner1_frame = ctk.CTkFrame(self)
        inner1_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.size=(5,5)

        camera_frame = ctk.CTkFrame(inner1_frame)
        camera_frame.pack(side="left", fill="both", expand=True)

        self.LiveFrame = ctk.CTkFrame(camera_frame, fg_color="white",bg_color="white",border_width=0)
        self.LiveFrame.pack(side="top", fill="x")

        self.menu_frame = ctk.CTkFrame(inner1_frame,
                                       width=50,
                                       fg_color="white",
                                       border_width=2,
                                       border_color="Gray",
                                       bg_color="white")
        self.menu_frame.pack(side="right", fill="both", expand=False)


        self.main_camera = self.main_camera_class(camera_frame, self.saved_image_path, self.update_grid_callback)
        self.main_camera.pack(fill="both", expand=True)

        # first position
        self.Live()

        self.MenuTitle()
        self.ZoomButtons()
        self.ZoomOrientacion()
        self.LightIntensity()
        self.LightDirection()
        self.CapturetureOrCacel()

    def MenuTitle(self):


        container = ctk.CTkFrame(self.menu_frame,fg_color="white")
        container.grid(row=0, column=1, columnspan=4, pady=20)
        Lbl = ctk.CTkLabel(container,
                           text="Lighting setup",
                           text_color="#7d7d7d",
                           font=('Consolas', 25, 'bold'))
        Lbl.pack()
        lbl = ctk.CTkLabel(container,
                           text="_____________________",
                           font=('Arial', 10),
                           text_color="Gray")
        lbl.pack()



    def Live(self):

        LiveF = ctk.CTkFrame(self.LiveFrame,fg_color="white",bg_color="white")
        LiveF.pack(side="right")


        label= ctk.CTkLabel(LiveF,
                            text="Live Mode ",
                            font=('Consolas',25),
                            text_color="black")
        label.grid(row=0,column=0)


        off=ctk.CTkLabel(LiveF,text="Off ",
                         font=('Consolas',25),
                         text_color="black")
        off.grid(row=0, column=1)
        self.SwitchCamera = ctk.CTkSwitch(
                         LiveF,text="On",
                         font=('Consolas',25),text_color="black",
                         command=self.StartCamera)
        self.SwitchCamera.grid(row=0, column=2)

    # Zoom 3 Component
    # -----| X2 | X4 | X6 | X8 | R |-----

    def ZoomButtons(self):

        container_zoom = ctk.CTkFrame(self.menu_frame,fg_color="white")
        container_zoom.grid(row=1, column=0, columnspan=6, pady=30, padx=(10,5), sticky="w")

        ZoomLabel = ctk.CTkLabel(container_zoom,
                                 text="Zoom options\n",
                                 font=('Consolas', 20),
                                 text_color="black")
        ZoomLabel.pack(side="left")



        zoom_in_button = ctk.CTkButton(self.menu_frame,
                                       text="X2",
                                       font=('Consolas',20,"bold"),
                                       text_color="black",
                                       fg_color="white",
                                       width=self.size[0],
                                       height=self.size[1],
                                       command=self.Zoom_X2,
                                       hover_color="gray")
        zoom_in_button.grid(row=2,column=0,padx=(0,5),sticky="e")
        zoom_out_button = ctk.CTkButton(self.menu_frame,
                                        text="X4",
                                        font=('Consolas', 20, "bold"),
                                        text_color="black",
                                        fg_color="white",
                                        width=self.size[0],
                                        height=self.size[1],
                                        command=self.Zoom_X4)
        zoom_out_button.grid(row=2,column=1)
        Zoom_X6 = ctk.CTkButton(self.menu_frame,
                                        text="X6",
                                        font=('Consolas', 20, "bold"),
                                        text_color="black",
                                        fg_color="white",
                                        width=self.size[0],
                                        height=self.size[1],
                                        command=self.Zoom_X6)
        Zoom_X6.grid(row=2,column=2)
        Zoom_X8 = ctk.CTkButton(self.menu_frame,
                                        text="X8",
                                        font=('Consolas', 20, "bold"),
                                        text_color="black",
                                        fg_color="white",
                                        width=self.size[0],
                                        height=self.size[1],
                                        command=self.Zoom_X8)
        Zoom_X8.grid(row=2,column=3)
        reset_button = ctk.CTkButton(self.menu_frame,
                                     text="",
                                     fg_color="white",
                                     image=CamRe,
                                     width=self.size[0],
                                     height=self.size[1],
                                     command=self.reset_zoom_pan)
        reset_button.grid(row=2,column=4,padx=(5,0),sticky="w")

    # Zoom orientacion 4 Component
    #            | ʌ |
    #        | < |   | > |
    #            | v |
    def ZoomOrientacion(self):

        # Agregar botones de desplazamiento
        move_up_button = ctk.CTkButton(self.menu_frame,
                                       text="",
                                       image=RowUp,
                                       fg_color="white",
                                       width=self.size[0]-4,
                                       height=self.size[1]-4,
                                       command=self.move_up)
        move_up_button.grid(row=3, column=2,pady=(20,0))

        move_right_button = ctk.CTkButton(self.menu_frame,
                                       text="",
                                       image=RowDo,
                                       fg_color="white",
                                       width=self.size[0]-4,
                                       height=self.size[1]-4,
                                       command=self.move_down)
        move_right_button.grid(row=5, column=2)

        move_down_button = ctk.CTkButton(self.menu_frame,
                                       text="",
                                       image=RowLe,
                                       fg_color="white",
                                       width=self.size[0]-4,
                                       height=self.size[1]-4,
                                       command=self.move_left)
        move_down_button.grid(row=4, column=1,sticky="e")

        move_left_button = ctk.CTkButton(self.menu_frame,
                                       text="",
                                       image=RowRi,
                                       fg_color="white",
                                       width=self.size[0]-4,
                                       height=self.size[1]-4,
                                       command=self.move_right)
        move_left_button.grid(row=4, column=3,sticky="w")



    # Light Intensity 3 Component
    # -----| Min light | Mid Light | Max Light |-----
    def LightIntensity(self):
        Lbl = ctk.CTkLabel(self.menu_frame,
                           text="Select Intensity",
                           text_color="#000000",
                           font=('Consolas',20))
        Lbl.grid(row=6,column=0,columnspan=3,pady=40,padx=(10,5),sticky="w")

        size = (10, 10)

        self.top_button1 = ctk.CTkButton(self.menu_frame,
                                         text="",
                                         image=LMinNo,
                                         fg_color="white",
                                         width=size[0],
                                         height=size[1],
                                         command=self.Button_MinLight)
        self.top_button1.grid(row=7, column=1)

        self.top_button2 = ctk.CTkButton(self.menu_frame,
                                         text="",
                                         image=LMidNo,
                                         fg_color="white",
                                         width=size[0],
                                         height=size[1],
                                         command=self.Button_MidLight)
        self.top_button2.grid(row=7, column=2 )

        self.top_button3 = ctk.CTkButton(self.menu_frame,
                                         text="",
                                         image=LMaxNo,
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
        self.left_button.grid(row=10, column=1,sticky="e")

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
        self.right_button.grid(row=10, column=3,sticky="w")

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
    def CapturetureOrCacel(self):

        Lbl = ctk.CTkLabel(self.menu_frame,
                           text="Select option",
                           font=('Consolas',20),
                           text_color="black")
        Lbl.grid(row=12,column=0,columnspan=4,pady=30,padx=(10,5),sticky="w")

        self.ButtonCancel = ctk.CTkButton(self.menu_frame,
                                          fg_color="#a1a09f",
                                          text_color="black",
                                          text="Cancel",
                                          font=('Consolas', 20),
                                          command=self.Button_Cancel)
        self.ButtonCancel.grid(row=13, column=0, columnspan=2,sticky="w",padx=(5,0))

        capture_button = ctk.CTkButton(self.menu_frame,
                                       fg_color="#FE5202",
                                       text_color="white",
                                       text="Capture",
                                       font=('Consolas', 20),
                                       command=self.Button_Capture)
        capture_button.grid(row=13, column=3,columnspan=4,  sticky="w",padx=(0,5))

    def Button_Capture(self):
        self.SwitchCamera.deselect()
        self.main_camera.capture_image()
        if self.main_camera:
            self.main_camera.stop_camera()
        self.inner_tab_control.set("Select inspection area")

    def Button_Cancel(self):
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
            self.top_button1.configure(image=LMinNo)
            self.top_button1_state = False
        if selected_button != self.top_button2 and self.top_button2_state:
            self.top_button2.configure(image=LMidNo)
            self.top_button2_state = False
        if selected_button != self.top_button3 and self.top_button3_state:
            self.top_button3.configure(image=LMaxNo)
            self.top_button3_state = False


    # -----|Min light | Mid Light | Max Light |-----
    def Button_MinLight(self):
        if self.top_button1_state:
            self.top_button1.configure(image=LMinNo)
            self.top_button1_state = False
            print("Minlight disable")
        else:
            self.deselect_other_buttons(self.top_button1)
            self.top_button1.configure(image=LMinOk)
            self.top_button1_state = True
            print("Minlight enabled")
    def Button_MidLight(self):
        if self.top_button2_state:
            self.top_button2.configure(image=LMidNo)
            self.top_button2_state = False
            print("Mid light disabled")
        else:
            self.deselect_other_buttons(self.top_button2)
            self.top_button2.configure(image=LMidOk)
            self.top_button2_state = True
            print("Mid light enabled")
    def Button_MaxLight(self):
        if self.top_button3_state:
            self.top_button3.configure(image=LMaxNo)
            self.top_button3_state = False
            print("Max light disabled")
        else:
            self.deselect_other_buttons(self.top_button3)
            self.top_button3.configure(image=LMaxOk)
            self.top_button3_state = True
            print("Max light enabled")



    def Zoom_X2(self):
        self.main_camera.zoom_2x()
    def Zoom_X4(self):
        self.main_camera.zoom_4x()
    def Zoom_X6(self):
        self.main_camera.zoom_6x()
    def Zoom_X8(self):
        self.main_camera.zoom_8x()
    def reset_zoom_pan(self):
        self.main_camera.reset_zoom_pan()
    def move_up(self):
        self.main_camera.move_up()
    def move_down(self):
        self.main_camera.move_down()
    def move_left(self):
        self.main_camera.move_left()
    def move_right(self):
        self.main_camera.move_right()