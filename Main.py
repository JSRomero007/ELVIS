import os.path
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
from Default import  DefaultWindow
from CameraTools import MainCamera
from Training import TrainingModelForm
from Tools import ToolsForm
from Global.GlobalV import MenuConfig,Picture,PlayStopStatus

TextSize=MenuConfig.MenuTXTSize
X=MenuConfig.MenuPictureSize
Y=MenuConfig.MenuPictureSize
Icon=Picture.Icon
Home=Picture.Home
Training=Picture.Training
Tools=Picture.Tools
RunE=Picture.RunE
RunD=Picture.RunD
PauseE=Picture.PauseE
PauseD=Picture.PauseD
Status=PlayStopStatus.Status

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        icon_path = os.path.join("Img", "Icon", "Logo.ico")

        self.iconbitmap(icon_path)

        self.title("ELVIS | Live mode")
        self.configure(fg_color="white")
        self.geometry("1500x1000")
        self.minsize(1100,1000)
        # full screen, clear controls, Exit Button
        #self.attributes('-fullscreen', True)


        self.overrideredirect(False)
        self.bind('<Escape>', self.exit_fullscreen)

        self.selected_button = None

        # Crear el menú superior
        self.create_menu()

        # Crear el panel principal
        self.main_panel = ctk.CTkFrame(self,bg_color="white")
        self.main_panel.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Mostrar el formulario inicial
        self.show_child_form("DefWindow")

    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', True)
        self.overrideredirect(False)

    def create_menu(self):
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.configure(fg_color="white")
        self.menu_frame.pack(side="top", fill="x")


        self.image_label = ctk.CTkLabel(self.menu_frame, image=Icon,text="")
        self.image_label.pack(side="left", padx=(5,5), pady=5)

        # Botones del menú
        self.file_button = self.create_menu_button("Home",Home, self.HomeAction)

        # Combobox después del primer botón
        self.combobox = ctk.CTkComboBox(self.menu_frame,
                                        values=["Option 1", "Option 2", "Option 3"],
                                        font=('Consolas', TextSize),
                                        fg_color="white",
                                        border_width=1,
                                        border_color="orange",
                                        button_color="orange",
                                        text_color="black")
        self.combobox.pack(side="left")
        self.combobox.configure(width=300)

        self.edit_button = self.create_menu_button("Training", Training, self.TrainingAction)
        self.help_button = self.create_menu_button("Tools", Tools, self.ToolsAction)

        self.PlayStop()

        # Línea de selección
        self.selection_line = ctk.CTkFrame(self, height=2, fg_color="orange")
        self.selection_line.pack(side="top", fill="x")

    def PlayStop(self):
        buttons_frame = ctk.CTkFrame(self.menu_frame, fg_color="white")
        buttons_frame.pack(side="right")
        self.text = ctk.CTkLabel(self.menu_frame,
                                 text="Run Mode",
                                 font=('Consolas',TextSize),
                                 text_color="black")
        self.text.pack(side="right")

        # Button Pause
        self.pause_button = ctk.CTkButton(buttons_frame,
                                          text="",
                                          image=PauseE,
                                          fg_color="white",
                                          width=10,
                                          command=self.PauseButton)
        self.pause_button.pack(side="left", padx=(0, 5))
        # Button Play
        self.play_button = ctk.CTkButton(buttons_frame,
                                         text="",
                                         bg_color="white",
                                         image=RunD,
                                         fg_color="white",
                                         width=10,
                                         command=self.PlayButton)
        self.play_button.pack(side="left", padx=(0, 20))

        self.Runing = False

    def PlayButton(self):
        self.Runing = True
        self.Toggle_Play_Pause()

    def PauseButton(self):
        self.Runing = False
        self.Toggle_Play_Pause()

    def create_menu_button(self, text, icon, command):
        button = ctk.CTkButton(self.menu_frame,
                               text=text,
                               text_color="black",
                               image=icon,
                               compound="left",
                               command=command,
                               font=('Consolas', TextSize),
                               fg_color="white",
                               border_width=0,
                               border_color="black")
        button.bind("<Enter>", lambda e: self.on_enter(button))
        # button.bind("<Leave>", lambda e: self.on_leave(button))
        button.pack(side="left", padx=5, pady=5)
        return button

    def on_enter(self, button):
        button.configure(fg_color="white")

    def on_leave(self, button):
        if button != self.selected_button:
            button.configure(fg_color="#FE5202")

    def select_button(self, button):
        if self.selected_button:
            self.selected_button.configure()

        self.selected_button = button
        self.selected_button.configure(fg_color="white")

        self.update_selection_line()

    def update_selection_line(self):
        # Actualizar la posición y ancho de la línea de selección
        self.selection_line.place(x=self.selected_button.winfo_x(),
                                  y=self.selected_button.winfo_y() + self.selected_button.winfo_height() + 2)
        self.selection_line.configure(width=self.selected_button.winfo_width())

    def Toggle_Play_Pause(self):
        if self.Runing:
            self.play_button.configure(image=RunE,state="disabled")
            self.pause_button.configure(image=PauseD,state="normal")
            self.show_child_form("Play")
            Status="Enabled"
        else:
            self.play_button.configure(image=RunD,state="normal")
            self.pause_button.configure(image=PauseE,state="disabled")
            Status="Disabled"
        self.Runing = not self.Runing  # Toggle the state

    def HomeAction(self):
        self.Runing=False
        self.Toggle_Play_Pause()
        self.select_button(self.file_button)
        self.show_child_form("MainHome")

    def TrainingAction(self):
        self.Runing = False
        self.Toggle_Play_Pause()
        self.select_button(self.edit_button)
        self.show_child_form("TrainingModel")

    def ToolsAction(self):
        self.Runing = False
        self.Toggle_Play_Pause()
        self.select_button(self.help_button)
        self.show_child_form("Tools")

    # ----- Display Forms ------#
    def show_child_form(self, form_name):
        for widget in self.main_panel.winfo_children():
            widget.destroy()
       #if form_name == "Play":
            #form = RUNModel(self.main_panel)
            
        if form_name =="DefWindow":
            form = DefaultWindow(self.main_panel)

        elif form_name == "TrainingModel":
            form = TrainingModelForm(self.main_panel)

        elif form_name == "Tools":
            form = ToolsForm(self.main_panel)
        form.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()