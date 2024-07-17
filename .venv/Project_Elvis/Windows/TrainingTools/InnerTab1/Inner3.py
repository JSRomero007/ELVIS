import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import os
import numpy as np
from Global.GlobalV import Inherit,Img


class InnerTab3Content(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")
        self.parent = parent
        self.current_filter = Inherit.SelectionFilter
        self.Camera=Img.Camera
        self.ImgWid=Img.ImgWidth
        self.ImgHei=Img.ImgHeidht
        self.shape = 'square'
        self.drawing = False
        self.start_x, self.start_y = 0, 0
        self.end_x, self.end_y = 0, 0

        self.image_path = "C:\\Users\\y80txk\\Pictures\\ELVIS\\captured_image.jpg"
        self.last_modified = 0

        self.inspection_areas = [{'enabled': False, 'coords': (0, 0, 0, 0), 'width': 0, 'height': 0}] * 2

        self.image_frame = ctk.CTkFrame(self, fg_color="white", border_width=0)
        self.image_frame.pack(side=ctk.LEFT, padx=0, pady=0)

        self.button_panel = ctk.CTkFrame(self, fg_color="white", border_width=0)
        self.button_panel.pack(side=ctk.RIGHT, padx=10, pady=10, fill="y")

        self.canvas = ctk.CTkCanvas(self.image_frame, width=1280, height=720, highlightthickness=0, bg="white")
        self.canvas.pack()

        self.table_label = ctk.CTkLabel(self.button_panel, text="", justify="left")
        self.table_label.pack(pady=10)

        self.ShowImage()
        self.UpdateImage()
        self.UpdateFilter()

        self.canvas.bind("<Button-1>", self.MouseDown)
        self.canvas.bind("<B1-Motion>", self.MouseMove)
        self.canvas.bind("<ButtonRelease-1>", self.MouseUp)

        self.selected_area = ctk.StringVar(value="Inspection 1")
        self.inspection_vars = [
            {'enabled': ctk.IntVar(), 'start_x': ctk.StringVar(), 'start_y': ctk.StringVar(), 'size_x': ctk.StringVar(),
             'size_y': ctk.StringVar()},
            {'enabled': ctk.IntVar(), 'start_x': ctk.StringVar(), 'start_y': ctk.StringVar(), 'size_x': ctk.StringVar(),
             'size_y': ctk.StringVar()}
        ]
        self.InspectionControls()

    #Get the coordinates Inspection 1 & Inspection 2 and save in GlobalV
    def SaveDataInspection(self):
        for i, inspection in enumerate(self.inspection_vars):
            enabled = inspection['enabled'].get()
            start_x = inspection['start_x'].get()
            start_y = inspection['start_y'].get()
            size_x = inspection['size_x'].get()
            size_y = inspection['size_y'].get()

            data_string = ",".join([str(enabled), start_x, start_y, size_x, size_y])

            if i == 0:
                Inherit.Inspection1 = data_string
            elif i == 1:
                Inherit.Inspection2 = data_string
    def InspectionControls(self):
        for i in range(2):
            frame = ctk.CTkFrame(self.button_panel,fg_color="white",border_color="Gray",border_width=1)
            title_label = ctk.CTkLabel(self.button_panel, text=f"Inspection {i+1}")
            title_label.pack(anchor="n", padx=10, pady=(5, 0))

            frame.pack(pady=10, fill="x",padx=10)
            control_frame = ctk.CTkFrame(frame,fg_color="white")
            control_frame.pack(fill="x", pady=5,padx=10)

            ctk.CTkRadioButton(control_frame, text=f"Inspection {i + 1}",font=('Consolas',14),text_color="black", variable=self.selected_area,
                               value=f"Inspection {i + 1}", command=self.update_textbox_state).pack(side=ctk.LEFT,padx=10)
            ctk.CTkSwitch(control_frame, text="Enable",font=('Consolas',14), variable=self.inspection_vars[i]['enabled'],
                          command=lambda i=i: [self.toggle_area(i), self.update_textbox_state()]).pack(side=ctk.RIGHT,padx=10)

            ctk.CTkLabel(frame, text="Position",font=('Consolas',14),text_color="black").pack()
            position_frame = ctk.CTkFrame(frame,fg_color="white")
            position_frame.pack(fill="x", pady=5,padx=10)
            ctk.CTkLabel(position_frame, text="X",font=('Consolas',14),text_color="black").pack(side=ctk.LEFT, padx=10)
            start_x_entry = ctk.CTkEntry(position_frame, textvariable=self.inspection_vars[i]['start_x'])
            start_x_entry.pack(side=ctk.LEFT, padx=5)
            start_x_entry.bind("<Return>", lambda event, i=i: self.update_position(i))
            ctk.CTkLabel(position_frame, text="Y",font=('Consolas',14),text_color="black").pack(side=ctk.LEFT, padx=10)
            start_y_entry = ctk.CTkEntry(position_frame, textvariable=self.inspection_vars[i]['start_y'])
            start_y_entry.pack(side=ctk.LEFT, padx=5)
            start_y_entry.bind("<Return>", lambda event, i=i: self.update_position(i))

            ctk.CTkLabel(frame, text="Size",font=('Consolas',14),text_color="black").pack(padx=10)
            size_frame = ctk.CTkFrame(frame,fg_color="white")
            size_frame.pack(fill="x", pady=5,padx=10)

            ctk.CTkLabel(size_frame, text="X",font=('Consolas',14),text_color="black").pack(side=ctk.LEFT, padx=10)
            size_x_entry = ctk.CTkEntry(size_frame, textvariable=self.inspection_vars[i]['size_x'])
            size_x_entry.pack(side=ctk.LEFT, padx=5)
            size_x_entry.bind("<Return>", lambda event, i=i: self.update_size(i))

            ctk.CTkLabel(size_frame, text="Y",font=('Consolas',14),text_color="black").pack(side=ctk.LEFT, padx=10)
            size_y_entry = ctk.CTkEntry(size_frame, textvariable=self.inspection_vars[i]['size_y'])
            size_y_entry.pack(side=ctk.LEFT, padx=5)
            size_y_entry.bind("<Return>", lambda event, i=i: self.update_size(i))

            ctk.CTkButton(frame, text="Delete Inspection",font=('Consolas',14),text_color="black", command=lambda i=i: self.DeleteInspection(i)).pack(pady=5,padx=10)
            ctk.CTkLabel(frame,text="Selecte Mode inspection").pack(pady=5,padx=10)
            self.inspection_vars[i]['start_x_entry'] = start_x_entry
            self.inspection_vars[i]['start_y_entry'] = start_y_entry
            self.inspection_vars[i]['size_x_entry'] = size_x_entry
            self.inspection_vars[i]['size_y_entry'] = size_y_entry

        self.UpdateInspectionVar()

        ctk.CTkLabel(self.button_panel, text="Countorn", font=('Consolas', 14), text_color="black").pack(side=ctk.LEFT, padx=5)
        ctk.CTkSwitch(self.button_panel, text="", font=('Consolas', 14), command=lambda i=i: self.nueva_funcion_switch(i)).pack(side=ctk.LEFT, padx=5)
        ctk.CTkLabel(self.button_panel, text="IA", font=('Consolas', 14), text_color="black").pack(side=ctk.LEFT)
    def save_inspection_area(self):
        if self.shape == 'square':
            start_x, end_x = sorted([self.start_x, self.end_x])
            start_y, end_y = sorted([self.start_y, self.end_y])
            coords = (start_x, start_y, end_x, end_y)
            width = abs(end_x - start_x)
            height = abs(end_y - start_y)

            selected_index = int(self.selected_area.get()[-1]) - 1

            self.inspection_areas[selected_index] = {'shape': self.shape, 'coords': coords, 'width': width, 'height': height,'enabled': self.inspection_vars[selected_index]['enabled'].get()}
            self.UpdateInspectionVar()
            self.ApplyFilter()

    # ------ Image ------
        #Filter
    def ApplyFilter(self):
        self.reset_image()
        if self.inspection_areas:
            for area in self.inspection_areas:
                if area['enabled']:
                    x1, y1, x2, y2 = area['coords']
                    mask = self.frame[y1:y2, x1:x2].copy()
                    if mask.size != 0:
                        filtered_mask = self.ApplyFilterInImage(Image.fromarray(mask), Inherit.SelectionFilter)
                        self.frame[y1:y2, x1:x2] = np.array(filtered_mask)
                        cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        self.update_frame()
    def ApplyFilterInImage(self, image, filter_type):
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        if filter_type == "GrayScale": #complete
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filter_type == "RedVision":#complete
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        elif filter_type == "HighlightShadow":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        elif filter_type == "OnlyLines":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filter_type == "FrontLines":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filter_type == "Negative":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def ShowImage(self):
        try:
            self.frame = cv2.imread(self.image_path)
            if self.frame is not None:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                # Redimensionar la imagen a 1280x720
                new_width, new_height = self.ImgWid, self.ImgHei
                self.frame = cv2.resize(self.frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

                img = Image.fromarray(self.frame)
                imgtk = ImageTk.PhotoImage(image=img)

                self.canvas.config(width=new_width, height=new_height)
                self.canvas.create_image(0, 0, anchor=ctk.NW, image=imgtk)
                self.canvas.image = imgtk
            else:
                print(f"Error: No se pudo cargar la imagen desde {self.image_path}")
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def DrawShapes(self):
        for i, area in enumerate(self.inspection_areas):
            if area['enabled']:
                self.DrawAndSaveShape(area, i + 1)
    def DrawShape(self):
        self.canvas.delete("shape")
        for i, area in enumerate(self.inspection_areas):
            if area['enabled']:
                self.DrawAndSaveShape(area, i + 1)
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='#FE5202', tag="shape")
        self.canvas.create_text((self.start_x + self.end_x) // 2, self.start_y - 10,
                                text="Inspection {}".format(len(self.inspection_areas) + 1), fill="#FE5202",
                                tag="shape", font=('Consolas', 15))
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        self.canvas.create_text((self.start_x + self.end_x) // 2, (self.start_y + self.end_y) // 2,
                                text=f"{width}x{height}", fill="red", tag="shape")
    def DrawAndSaveShape(self, area, index):
        self.canvas.create_rectangle(area['coords'], outline='red')
        x1, y1, x2, y2 = area['coords']
        self.canvas.create_text((x1 + x2) // 2, y1 - 10, text="Inspection {}".format(index), fill="#FE5202",
                                font=('Consolas', 15))
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=f"{width}x{height}", fill="#FE5202",
                                font=('Consolas', 15))

    #----- Mouse ------
    def MouseDown(self, event):
        if self.inspection_areas[int(self.selected_area.get()[-1]) - 1]['enabled']:
            self.drawing = True
            self.start_x, self.start_y = event.x, event.y
    def MouseMove(self, event):
        if self.drawing:
            self.end_x, self.end_y = event.x, event.y
            self.DrawShape()
    def MouseUp(self, event):
        self.drawing = False
        self.save_inspection_area()


    # ------ Controllers ------

    def toggle_area(self, index):
        self.inspection_areas[index]['enabled'] = bool(self.inspection_vars[index]['enabled'].get())
        self.ApplyFilter()

        self.update_textbox_state()
    def update_textbox_state(self):
        for i in range(2):
            enabled = self.inspection_vars[i]['enabled'].get() and (self.selected_area.get() == f"Inspection {i + 1}")
            state = ctk.NORMAL if enabled else ctk.DISABLED

            self.inspection_vars[i]['start_x_entry'].configure(state=state)
            self.inspection_vars[i]['start_y_entry'].configure(state=state)
            self.inspection_vars[i]['size_x_entry'].configure(state=state)
            self.inspection_vars[i]['size_y_entry'].configure(state=state)

    # ------ Controls ------

        #Update Zone
    def UpdateInspectionVar(self):
        for i, area in enumerate(self.inspection_areas):
            self.inspection_vars[i]['start_x'].set(area['coords'][0])
            self.inspection_vars[i]['start_y'].set(area['coords'][1])
            self.inspection_vars[i]['size_x'].set(area['width'])
            self.inspection_vars[i]['size_y'].set(area['height'])
        self.update_textbox_state()
    def update_position(self, index):
        try:
            start_x = int(self.inspection_vars[index]['start_x'].get())
            start_y = int(self.inspection_vars[index]['start_y'].get())
            size_x = self.inspection_areas[index]['width']
            size_y = self.inspection_areas[index]['height']

            end_x = start_x + size_x
            end_y = start_y + size_y

            self.inspection_areas[index]['coords'] = (start_x, start_y, end_x, end_y)

            self.ApplyFilter()

        except ValueError:
            print("Error: Valores de coordenadas inválidos")
    def update_size(self, index):
        try:
            size_x = int(self.inspection_vars[index]['size_x'].get())
            size_y = int(self.inspection_vars[index]['size_y'].get())
            start_x = self.inspection_areas[index]['coords'][0]
            start_y = self.inspection_areas[index]['coords'][1]

            end_x = start_x + size_x
            end_y = start_y + size_y

            self.inspection_areas[index]['coords'] = (start_x, start_y, end_x, end_y)
            self.inspection_areas[index]['width'] = size_x
            self.inspection_areas[index]['height'] = size_y

            self.ApplyFilter()


        except ValueError:
            print("Error: Valores de tamaño inválidos")
    def UpdateImage(self):
        try:
            modified_time = os.path.getmtime(self.image_path)
            if modified_time != self.last_modified:
                self.last_modified = modified_time
                self.ShowImage()
                self.DrawShapes()
        except Exception as e:
            print(f"Error al actualizar la imagen: {e}")

        self.after(500, self.UpdateImage)
    def UpdateFilter(self):
        if self.current_filter != Inherit.SelectionFilter:
            self.current_filter = Inherit.SelectionFilter
            self.ApplyFilter()

        self.after(500, self.UpdateFilter)
    def update_frame(self):
        self.SaveDataInspection()
        img = Image.fromarray(self.frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, anchor=ctk.NW, image=imgtk)
        self.canvas.image = imgtk
        self.DrawShapes()
        #Reset Zone
    def reset_image(self):
        self.ShowImage()
        self.DrawShapes()

        #Delete Zone
    def DeleteInspection(self, index):
        self.inspection_areas[index] = {'enabled': False, 'coords': (0, 0, 0, 0), 'width': 0, 'height': 0}
        self.UpdateInspectionVar()
        self.ApplyFilter()



