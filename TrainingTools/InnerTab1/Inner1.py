import customtkinter as ctk
import configparser
from PIL import Image
from PIL import ImageGrab
from CameraTools import CameraHandler
from Global.GlobalV import Picture,Img,Cam
import xml.etree.ElementTree as ET
import os


class InnerTab1Content(ctk.CTkFrame):
    def __init__(self, parent, saved_image_path, main_camera_class, update_grid_callback, inner_tab_control):
        super().__init__(parent)
        self.configure(fg_color="white", bg_color="white")
        self.Icons()
        self.light_intensity_state = None
        self.light_direction_state = []
        self.saved_image_path = saved_image_path
        self.main_camera_class = main_camera_class
        self.update_grid_callback = update_grid_callback
        self.inner_tab_control = inner_tab_control
        self.main_camera = None
        self.camera_handler = CameraHandler()

        # Inicializar listas vacías para almacenar los botones y checkboxes
        self.camera_buttons = []
        self.checkboxes = []


        # Estados iniciales de los botones
        self.up_button_state = False
        self.left_button_state = False
        self.center_button_state = False
        self.right_button_state = False
        self.down_button_state = False

        self.top_button1_state = False
        self.top_button2_state = False
        self.top_button3_state = False

        # Inicialización del diccionario para almacenar los estados de LightIntensity y LightDirection de cada cámara
        self.camera_states = {i: {'light_intensity': None, 'light_direction': None} for i in range(1, 5)}

        # Configurar la interfaz de usuario
        self.UI()
    def update_light_direction_xml(self):
        xml_path = "C:\\ELVIS\\TmpDB\\003_Configuration\\TempConfiguration.xml"

        if not os.path.exists(xml_path):
            print(f"Error: El archivo XML no existe en la ruta {xml_path}")
            return

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            cam_tag = f"Cam{Cam.id}"
            cam_element = root.find(cam_tag)

            if cam_element is not None:
                # Verificar y actualizar el elemento LightDirection
                light_direction_element = cam_element.find('LightConfig')
                if light_direction_element is not None:
                    # Construimos el texto para LightDirection con la intensidad de luz y las direcciones seleccionadas
                    light_direction_text = f"{self.light_intensity_state}: {','.join(self.light_direction_state)}"
                    light_direction_element.text = light_direction_text
                    print(f"Actualizando LightDirection a: {light_direction_text}")
                else:
                    print(f"Error: No se encontró el elemento 'LightDirection' en {cam_tag}")

                # Verificar y actualizar el elemento Light
                light_config_element = cam_element.find('LightConfig')
                light_element = cam_element.find('Light')

                if light_config_element is not None and light_element is not None:
                    # Si LightConfig contiene 'None' o está vacía, poner False en Light
                    light_config_text = light_config_element.text
                    if light_config_text is None or light_config_text.strip() == "" or "None" in light_config_text:
                        light_element.text = "False"
                        print(f"Actualizando <Light> a False porque <LightConfig> es '{light_config_text}'")
                    else:
                        light_element.text = "True"
                        print(f"Actualizando <Light> a True porque <LightConfig> contiene '{light_config_text}'")
                else:
                    print(f"Error: No se encontraron los elementos 'LightConfig' o 'Light' en {cam_tag}")

            else:
                print(f"Error: No se encontró el elemento {cam_tag} en el XML")

            # Guardamos el XML actualizado
            tree.write(xml_path)
            print("XML actualizado correctamente")

        except ET.ParseError as e:
            print(f"Error al leer el archivo XML: {e}")
        except Exception as e:
            print(f"Error desconocido: {e}")
    def update_light_direction(self, direction):
        if direction not in self.light_direction_state:
            self.light_direction_state.append(direction)
        else:
            self.light_direction_state.remove(direction)
        self.update_light_direction_xml()
    def UI(self):
        # Configurar las columnas para que se expandan
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)  # Cambiado a 1 para que también se expanda

        # Configurar las filas para que se expandan y establecer tamaños fijos
        self.grid_rowconfigure(0, minsize=50, weight=0)  # Header con tamaño fijo de 50 px
        self.grid_rowconfigure(1, minsize=120, weight=0)  # Fila 1 se expande
        self.grid_rowconfigure(2, weight=1)  # Fila 2 con tamaño fijo de 120 px
        self.grid_rowconfigure(3, minsize=80, weight=0)  # Fila 3 se expande
        self.grid_rowconfigure(4, minsize=50, weight=0)  # Footer con tamaño fijo de 50 px

        self.Header()

        text1 = ctk.CTkLabel(self, text="", text_color="black", font=('Consolas', 20))
        text1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        text2 = ctk.CTkLabel(self, text="", text_color="black", font=('Consolas', 20))
        text2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        text3 = ctk.CTkLabel(self, text="", text_color="black", font=('Consolas', 20))
        text3.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        self.CameraFrame()

        # Crear el menu frame con un tamaño fijo
        self.menu_frame = ctk.CTkFrame(self, width=200, fg_color="white", border_width=2, border_color="Gray",
                                       bg_color="white")
        self.menu_frame.grid(row=2, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.menu_frame.grid_propagate(False)  # Prevenir que el frame se expanda o contraiga
        self.menu_frame.grid_columnconfigure(0, weight=1)  # Asegurar que se expanda en horizontal

        # Configurar sub-grid para menu_frame
        self.menu_frame.grid_rowconfigure(0, weight=1)  # Fila para botones adicionales
        self.menu_frame.grid_rowconfigure(1, weight=1)  # Fila para LightIntensity
        self.menu_frame.grid_rowconfigure(2, weight=1)  # Fila para LightDirection
        self.menu_frame.grid_rowconfigure(3, weight=1)  # Fila para start_button

        self.BackNextButtons = ctk.CTkFrame(self)
        self.BackNextButtons.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)

        footer = ctk.CTkLabel(self, text="", text_color="black", font=('Consolas', 25, 'bold'))
        footer.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.LightIntensity()  # Asegurarse de que LightIntensity esté en la fila correcta
        self.LightDirection()  # Asegurarse de que LightDirection esté en la fila correcta
        self.CaptureOrCancel()
    def AdditionalButtons(self):
        # Mover el botón start_button dentro de menu_frame, justo debajo de LightIntensity y LightDirection
        self.start_button = ctk.CTkButton(self.menu_frame, text="Start Camera",
                                          command=self.toggle_camera_capture)
        self.start_button.grid(row=3, column=0, pady=(10, 0), padx=10, sticky="ew")  # Expandir en "x" y centrar
    def toggle_inspection(self, index):
        # Cambiar el texto del checkbox entre "Enable" y "Disabled"
        checkbox = self.checkboxes[index]
        if checkbox.get() == 1:  # Si el checkbox está seleccionado
            checkbox.configure(text="Enable", text_color="#A6A6A6")
            checkbox.label_status.configure(text="Enabled", text_color="green")  # Actualizar la etiqueta a Enabled
        else:  # Si el checkbox no está seleccionado
            checkbox.configure(text="Disabled", text_color="#A6A6A6")
            checkbox.label_status.configure(text="Disabled", text_color="red")  # Actualizar la etiqueta a Disabled

        # Guardar configuración después de cambiar el estado del checkbox
        self.save_configuration(index + 1)
    def update_light_config_label(self, camera_number):
        # Actualiza el texto del label para mostrar la cámara seleccionada
        self.light_config_label.configure(text=f"Light config for Camera-{camera_number}")
    def Header(self):
        header = ctk.CTkLabel(self, text="- Preview camera inspection -",fg_color="white", font=('Consolas', 25), text_color="black")
        header.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
    def CameraFrame(self):
        camera_frame = ctk.CTkFrame(self,fg_color="white",bg_color="white")
        camera_frame.grid(row=2, column=0, columnspan=2, rowspan=2,  padx=10, pady=90)

        self.LiveFrame = ctk.CTkFrame(camera_frame, border_width=0, width=Img.ImgWidth, height=Img.ImgHeight)
        self.LiveFrame.pack( expand=False)

        self.canvas = ctk.CTkCanvas(self.LiveFrame, width=Img.ImgWidth, height=Img.ImgHeight)
        self.canvas.pack( expand=False)
    def CaptureOrCancel(self):

        self.ButtonCancel = ctk.CTkButton(self.BackNextButtons,
                                          fg_color="#a1a09f",
                                          text_color="black",
                                          text="Back",
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
            if self.start_button:  # Verifica si el botón existe antes de intentar configurarlo
                self.start_button.configure(text="Start Camera")
        else:
            self.camera_handler.start_cyclic_capture(self.canvas)
            if self.start_button:  # Verifica si el botón existe antes de intentar configurarlo
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
        # Crear un frame dentro de menu_frame para los controles de intensidad de luz
        light_intensity_frame = ctk.CTkFrame(self.menu_frame, fg_color="white", bg_color="white")
        light_intensity_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")  # Configuración para expandirse

        # Configurar las columnas del frame para centrar los botones
        light_intensity_frame.grid_columnconfigure(0, weight=1)
        light_intensity_frame.grid_columnconfigure(1, weight=1)
        light_intensity_frame.grid_columnconfigure(2, weight=1)

        # Título centrado
        self.light_config_label = ctk.CTkLabel(light_intensity_frame,
                                               text="Light config for Camera-",
                                               text_color="#000000",
                                               font=('Consolas', 20))
        self.light_config_label.grid(row=0, column=0, columnspan=3, pady=5, padx=(10, 5),
                                     sticky="ew")  # Expandir horizontalmente

        size = (10, 10)

        # Botones de intensidad de luz con padx específico
        self.top_button1 = ctk.CTkButton(light_intensity_frame,
                                         text="",
                                         image=self.LMinNo,
                                         fg_color="white",
                                         width=size[0],
                                         height=size[1],
                                         command=self.Button_MinLight)
        self.top_button1.grid(row=1, column=0, padx=(20, 0), pady=5, sticky="ew")  # Margen izquierdo de 20 px

        self.top_button2 = ctk.CTkButton(light_intensity_frame,
                                         text="",
                                         image=self.LMidNo,
                                         fg_color="white",
                                         width=size[0],
                                         height=size[1],
                                         command=self.Button_MidLight)
        self.top_button2.grid(row=1, column=1, padx=(20, 0), pady=5, sticky="ew")  # Margen izquierdo de 20 px

        self.top_button3 = ctk.CTkButton(light_intensity_frame,
                                         text="",
                                         image=self.LMaxNo,
                                         fg_color="white",
                                         width=size[0],
                                         height=size[1],
                                         command=self.Button_MaxLight)
        self.top_button3.grid(row=1, column=2, padx=(20, 0), pady=5, sticky="ew")  # Margen izquierdo de 20 px
    # Light Direction 5 Component
    #            | ʌ |
    #        | < | ○ | > |
    #            | v |
    def LightDirection(self):
        # Crear un frame dentro de menu_frame para los controles de dirección de luz
        light_direction_frame = ctk.CTkFrame(self.menu_frame, fg_color="white", bg_color="white")
        light_direction_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")  # Reducir pady

        # Configurar las columnas del frame para centrar los botones
        light_direction_frame.grid_columnconfigure(0, weight=1)  # Columna izquierda
        light_direction_frame.grid_columnconfigure(1, weight=1)  # Columna central
        light_direction_frame.grid_columnconfigure(2, weight=1)  # Columna derecha

        size = (10, 10)

        # Agregar botones de control de dirección con imágenes
        self.up_button = ctk.CTkButton(light_direction_frame,
                                       text="",
                                       image=Picture.LightUpNo,
                                       fg_color="white",
                                       command=self.up_action,
                                       width=size[0],
                                       height=size[1])
        self.up_button.grid(row=0, column=1)  # Posicionar en la columna central para centrar

        self.left_button = ctk.CTkButton(light_direction_frame,
                                         text="",
                                         image=Picture.LightLefNo,
                                         fg_color="white",
                                         command=self.left_action,
                                         width=size[0],
                                         height=size[1])
        self.left_button.grid(row=1, column=0, sticky="e")

        self.center_button = ctk.CTkButton(light_direction_frame,
                                           text="",
                                           #image=Picture.LightCenNo,
                                           fg_color="white",
                                           #command=self.center_action,
                                           width=size[0],
                                           height=size[1])
        self.center_button.grid(row=1, column=1)

        self.right_button = ctk.CTkButton(light_direction_frame,
                                          text="",
                                          image=Picture.LightRigNo,
                                          fg_color="white",
                                          command=self.right_action,
                                          width=size[0],
                                          height=size[1])
        self.right_button.grid(row=1, column=2, sticky="w")

        self.down_button = ctk.CTkButton(light_direction_frame,
                                         text="",
                                         image=Picture.LightDowNo,
                                         fg_color="white",
                                         command=self.down_action,
                                         width=size[0],
                                         height=size[1])
        self.down_button.grid(row=2, column=1)  # Posicionar en la columna central para centrar

        # Colocar el botón start_button debajo de los controles de dirección
        self.start_button = ctk.CTkButton(light_direction_frame, text="Start Camera",
                                          command=self.toggle_camera_capture)
        self.start_button.grid(row=3, column=0, columnspan=3, pady=(10, 0), padx=10,
                               sticky="ew")  # Expandir en "x" y centrar
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
        #self.StartCamera()
        self.inner_tab_control.set("Setup")
        print("Back")
    def StartCamera(self):
        if self.SwitchCamera.get():
            if self.main_camera:
                self.main_camera.start_camera()
        else:
            if self.main_camera:
                self.main_camera.stop_camera()
    def up_action(self):
        self.toggle_button("up")
        self.update_light_direction("Up")
    def down_action(self):
        self.toggle_button("down")
        self.update_light_direction("Down")
    def left_action(self):
        self.toggle_button("left")
        self.update_light_direction("Left")
    def right_action(self):
        self.toggle_button("right")
        self.update_light_direction("Right")
    def center_action(self):
        self.toggle_button("center")
        self.update_light_direction("Center")
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
    # -----|Min light | Mid Light | Max Light |-----
    def Button_MinLight(self):
        if self.top_button1_state:
            self.top_button1.configure(image=self.LMinNo)
            self.top_button1_state = False
            self.light_intensity_state = None
        else:
            self.deselect_other_buttons(self.top_button1)
            self.top_button1.configure(image=self.LMinOk)
            self.top_button1_state = True
            self.light_intensity_state = "Min Light"
        self.update_light_direction_xml()
    def Button_MidLight(self):
        if self.top_button2_state:
            self.top_button2.configure(image=self.LMidNo)
            self.top_button2_state = False
            self.light_intensity_state = None
        else:
            self.deselect_other_buttons(self.top_button2)
            self.top_button2.configure(image=self.LMidOk)
            self.top_button2_state = True
            self.light_intensity_state = "Mid Light"
        self.update_light_direction_xml()
    def Button_MaxLight(self):
        if self.top_button3_state:
            self.top_button3.configure(image=self.LMaxNo)
            self.top_button3_state = False
            self.light_intensity_state = None
        else:
            self.deselect_other_buttons(self.top_button3)
            self.top_button3.configure(image=self.LMaxOk)
            self.top_button3_state = True
            self.light_intensity_state = "Max Light"
        self.update_light_direction_xml()
    def deselect_other_buttons(self, selected_button):
        # Desactivar los otros botones excepto el seleccionado
        if selected_button != self.top_button1:
            self.top_button1.configure(image=self.LMinNo)
            self.top_button1_state = False
        if selected_button != self.top_button2:
            self.top_button2.configure(image=self.LMidNo)
            self.top_button2_state = False
        if selected_button != self.top_button3:
            self.top_button3.configure(image=self.LMaxNo)
            self.top_button3_state = False
    def move_up(self):
        self.main_camera.move_up()
    def move_down(self):
        self.main_camera.move_down()
    def move_left(self):
        self.main_camera.move_left()
    def move_right(self):
        self.main_camera.move_right()