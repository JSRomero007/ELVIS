import customtkinter as ctk
from customtkinter import CTkCanvas
from CameraTools import CameraHandler
from Global.GlobalV import Img

class InnerTab5Content(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="white")
        self.camera_handler = CameraHandler()
        #Frame
        self.Header()
        self.LblOkZone()
        self.LblNGZone()
        self.Trigger()
        self.MainArea()
        self.ButtonsArea()
        self.BackNextButtos()
        self.Footer()
        self.previous_length = len(Img.InspectionData)  # Store the initial length
        self.states = {}
        self.check_for_updates()

        # Configurar las columnas para que se expandan
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  # Columna 2 no se expande
        self.grid_columnconfigure(2, weight=0)  # Columna 3 no se expande

        # Establecer el ancho fijo para las columnas 2 y 3
        self.grid_columnconfigure(2, minsize=500)

        # Configurar las filas para que se expandan y establecer tamaños fijos
        self.grid_rowconfigure(0, minsize=50, weight=0)  # Header con tamaño fijo de 50 px
        self.grid_rowconfigure(1, minsize=120, weight=0)  # Fila 1 se expande
        self.grid_rowconfigure(2, weight=1)  # Fila 2 con tamaño fijo de 120 px
        self.grid_rowconfigure(3,minsize=80, weight=0)  # Fila 3 se expande
        self.grid_rowconfigure(4, minsize=50, weight=0)  # Footer con tamaño fijo de 50 px

        # Empaquetar el frame principal para que ocupe todo el espacio disponible
        self.pack(fill="both", expand=True)

    def Header(self):
        # Fila 1: Columna 1 a 3 expandida label (header)
        header_label = ctk.CTkLabel(self, text="- Clasification -", fg_color="white", font=('Consolas', 20), text_color="black")
        header_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
    def LblOkZone(self):
        OkZone = ctk.CTkFrame(self, fg_color="lightgray")
        OkZone.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=5, pady=5)
        OkZone.grid_rowconfigure(0, weight=1)
        OkZone.grid_rowconfigure(1, weight=1)

        OkZone.grid_columnconfigure(0,minsize=80, weight=0)
        OkZone.grid_columnconfigure(1, weight=1)


        Oklabel = ctk.CTkLabel(OkZone, text="OK",fg_color="white",font=('Consolas',30,"bold"),text_color="Green")
        Oklabel.grid(row=0,rowspan=2, column=0, sticky="nsew", padx=5, pady=5)

        label = ctk.CTkLabel(OkZone, text="OK",fg_color="white",font=('Consolas',20,"bold"),text_color="Gray")
        label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        #Frame to count and view
        CountAndView = ctk.CTkFrame(OkZone,fg_color="white")
        CountAndView.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        CountAndView.grid_columnconfigure(0,weight=1)
        Count = ctk.CTkLabel(CountAndView, text="Do you have 10 Good pictures ",fg_color="white",font=('Consolas',15),text_color="black")
        Count.grid(row=0,rowspan=2, column=0, sticky="nsew", padx=5, pady=5)

        View = ctk.CTkButton(CountAndView, text="View",fg_color="white",font=('Consolas',20,"bold"),text_color="black")
        View.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    def LblNGZone(self):
        OkZone = ctk.CTkFrame(self, fg_color="lightgray")
        OkZone.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        OkZone.grid_rowconfigure(0, weight=1)
        OkZone.grid_rowconfigure(1, weight=1)

        OkZone.grid_columnconfigure(0,minsize=80, weight=0)
        OkZone.grid_columnconfigure(1, weight=1)


        Oklabel = ctk.CTkLabel(OkZone, text="NG",fg_color="white",font=('Consolas',30,"bold"),text_color="Red")
        Oklabel.grid(row=0,rowspan=2, column=0, sticky="nsew", padx=5, pady=5)

        label = ctk.CTkLabel(OkZone, text="OK",fg_color="white",font=('Consolas',20,"bold"),text_color="Gray")
        label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        #Frame to count and view
        CountAndView = ctk.CTkFrame(OkZone,fg_color="white")
        CountAndView.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        CountAndView.grid_columnconfigure(0,weight=1)
        Count = ctk.CTkLabel(CountAndView, text="Do you have 10 Good pictures ",fg_color="white",font=('Consolas',15),text_color="black")
        Count.grid(row=0,rowspan=2, column=0, sticky="nsew", padx=5, pady=5)

        View = ctk.CTkButton(CountAndView, text="View",fg_color="white",font=('Consolas',20,"bold"),text_color="black")
        View.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def MainArea(self):
        MainFrame = ctk.CTkFrame(self, fg_color="white")
        MainFrame.grid(row=2, rowspan=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Configurar el grid dentro del Frame para que también se expanda
        MainFrame.grid_rowconfigure(0, weight=1)
        MainFrame.grid_columnconfigure(0, weight=1)

        self.MainPic = CTkCanvas(MainFrame, width=Img.ImgWidth, height=Img.ImgHeight)  # Ajusta el tamaño del canvas aquí
        self.MainPic.grid(row=0, column=0)

    def Trigger(self):
        TriggerFrame = ctk.CTkLabel(self, text="Label 2.3", fg_color="lightgray")
        TriggerFrame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        TriggerFrame.grid_columnconfigure(0,weight=1)
        TriggerFrame.grid_columnconfigure(0,weight=1)

        TriggerButton =ctk.CTkButton(TriggerFrame,text="Trigger", command=self.capture_single_image)
        TriggerButton.grid(row=0, column=0)
    def capture_single_image(self):
        self.camera_handler.capture_single_image(self.MainPic)

    def ButtonsArea(self):
        self.ButtonFrame = ctk.CTkFrame(self, fg_color="White")
        self.ButtonFrame.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        self.ButtonFrame.grid_columnconfigure(0, weight=1)
        self.ButtonFrame.grid_columnconfigure(1, weight=1)
        self.ButtonFrame.grid_rowconfigure(0, minsize=80, weight=0)
        self.ButtonFrame.grid_rowconfigure(1, weight=1)

        # -- OK Area
       #oklabel = ctk.CTkButton(self.ButtonFrame, text="Ok", fg_color="white", font=('Consolas', 15),text_color="black")
        #oklabel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # -- NG Area
        #NGlabel = ctk.CTkButton(self.ButtonFrame, text="NG", fg_color="white", font=('Consolas', 15))
        #NGlabel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Frame for list elements
        self.ListFrame = ctk.CTkScrollableFrame(self.ButtonFrame, bg_color="white",fg_color="white", height=300)  # Scrollable frame
        self.ListFrame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.ListFrame.grid_columnconfigure(0, weight=1)  # Adjust weight to control spacing
        self.ListFrame.grid_columnconfigure(1, weight=1)
        self.ListFrame.grid_columnconfigure(2, weight=1)
        self.ListFrame.grid_columnconfigure(3, weight=1)
        self.update_list_elements()

    def add_list_elements(self, frame, start_row, data):
        # Agregar encabezados
        headers = ["View", "ID", "Treshold", "NG  |  OK"]
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(frame, text=header, fg_color="white", bg_color="white",
                                        font=('Consolas', 15, 'bold'), text_color="black")
            header_label.grid(row=start_row, column=col, sticky="ew", padx=2, pady=2)

        # Agregar elementos de la lista
        for i, item in enumerate(data):
            row = start_row + 1 + i
            bg_color = "white" if i % 2 == 0 else "lightgray"  # Alternar colores

            item_id = item['ID']

            # Agregar checkbox siempre activo
            checkbox_var = ctk.BooleanVar(value=True)
            checkbox = ctk.CTkCheckBox(frame, text="", variable=checkbox_var)
            checkbox.grid(row=row, column=0, sticky="ew", padx=2, pady=2)
            checkbox_var.trace_add("write", lambda *args, item_id=item_id, var=checkbox_var: self.update_state(item_id,
                                                                                                               'checkbox',
                                                                                                               var.get()))

            # Agregar label1 lo más cerca posible del lado izquierdo
            label1 = ctk.CTkLabel(frame, text=f"ID: {item_id}", fg_color=bg_color, bg_color=bg_color,
                                  text_color="black", font=('Consolas', 15))
            label1.grid(row=row, column=1, sticky="ew", padx=2, pady=2)

            # Agregar label2
            label2 = ctk.CTkLabel(frame, text=f"NInspection: {item['NInspection']}", fg_color=bg_color,
                                  bg_color=bg_color, text_color="black", font=('Consolas', 15))
            label2.grid(row=row, column=2, sticky="ew", padx=2, pady=2)

            # Agregar toggle switch
            toggle_var = ctk.BooleanVar(value=True)
            toggle = ctk.CTkSwitch(frame, text="", variable=toggle_var)
            toggle.select()
            toggle.grid(row=row, column=3, sticky="ew", padx=2, pady=2)
            toggle_var.trace_add("write",
                                 lambda *args, item_id=item_id, var=toggle_var: self.update_state(item_id, 'toggle',
                                                                                                  var.get()))

            # Inicializar estado en el diccionario
            self.states[item_id] = {
                'checkbox': checkbox_var.get(),
                'toggle': toggle_var.get()
            }

    def clean_unused_states(self, current_ids):
        keys_to_remove = [key for key in self.states.keys() if key not in current_ids]
        for key in keys_to_remove:
            del self.states[key]

    def update_state(self, item_id, widget_type, value):
        if item_id in self.states:
            self.states[item_id][widget_type] = value
            print(f"Updated {widget_type} state for ID {item_id}: {value}")

    def update_list_elements(self):
        # Clear current elements
        for widget in self.ListFrame.winfo_children():
            widget.destroy()

        current_ids = [item['ID'] for item in Img.InspectionData]

        # Limpia los estados no utilizados
        self.clean_unused_states(current_ids)

        if len(Img.InspectionData) > 0:
            self.add_list_elements(self.ListFrame, 0, Img.InspectionData)  # List in a single column

    def check_for_updates(self):
        current_length = len(Img.InspectionData)
        if current_length != self.previous_length:
            self.previous_length = current_length
            self.update_list_elements()
        self.after(1000, self.check_for_updates)  # Check for updates every second

    def BackNextButtos(self):
        button_frame = ctk.CTkFrame(self, fg_color="lightgray")
        button_frame.grid(row=3, column=2, sticky="nsew", padx=5, pady=5)

        # Crear los botones dentro del frame
        button_1 = ctk.CTkButton(button_frame, text="Back",command=self.testData)
        button_2 = ctk.CTkButton(button_frame, text="Next step",command=self.test)

        # Colocar los botones en el frame
        button_1.pack(side="left", padx=5, pady=5)
        button_2.pack(side="right", padx=5, pady=5)
    def Footer(self):
        footer_label = ctk.CTkLabel(self, text="Footer", fg_color="gray")
        footer_label.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

    def test(self):
        print(self.states)
    def testData(self):
        print(Img.InspectionData)




# Ejemplo de uso
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("600x400")

    inner_tab_content = InnerTab5Content(app)
    inner_tab_content.pack(fill="both", expand=True)

    app.mainloop()
