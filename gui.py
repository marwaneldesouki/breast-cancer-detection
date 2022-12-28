import os
import tkinter
import tkinter.messagebox
import customtkinter
from PIL import ImageGrab,ImageOps,Image
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import BreastCancer_Classifier as classify
from threading import *
from main import dilate,erode
import random

import concurrent.futures

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("BreastCancer Detection")
        self.geometry(f"{920}x{580}")
        self.resizable(0,0)
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Pages", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton( self.sidebar_frame,text="Classifier", command=lambda : self.sidebar_button_event(page=self.page_0))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text="Image Processing", command=lambda : self.sidebar_button_event(page=self.page_1))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        #########
    def page_0(self):
        self.title_frame = customtkinter.CTkFrame(self)
        self.title_frame.grid(row=0, column=1, padx=(20, 20),sticky="nwe")
        self.title_lable = customtkinter.CTkLabel(self.title_frame,anchor='center',text="Classifier",font=("Comic Sans MS", 40, "bold"),)
        self.title_lable.grid(row=0, column=0,padx=250 ,pady=(10, 0))
        #########
        self.main_frame = customtkinter.CTkFrame(self,)
        self.main_frame.grid(row=0, column=1,pady=90, rowspan=5, sticky="n")
        self.main_frame.grid_rowconfigure(5, weight=1)
        self.bg_image_0 = customtkinter.CTkImage(Image.open(".\others\place_holder.jpg"),
                                               size=(500, 300))
        self.bg_image_label = customtkinter.CTkLabel(self.main_frame, image=self.bg_image_0,text="",)
        self.bg_image_label.grid(row=0, column=0)
        self.prediction_lable = customtkinter.CTkLabel(self.main_frame,text="Prediction:",font=("Comic Sans MS", 20),anchor=tkinter.CENTER,)
        self.prediction_lable.grid(row=1,)
        #########
        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=3, column=1,  padx=0, pady=0, sticky="nwe")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=5, sticky="nsew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # set default values
        
        self.progressbar_1.configure(mode="determinate")
        self.progressbar_1.set(1)
        self.seg_button_1.configure(values=["Browse Image", "get random cancer img", "get random non-cancer img"],command=self.segmented_button_callback)
    
    eroded_times=0
    dilated_times=0
    def page_1(self):
        self.title_frame = customtkinter.CTkFrame(self)
        self.title_frame.grid(row=0, column=1, padx=(20, 20),sticky="nwe")
        self.title_lable = customtkinter.CTkLabel(self.title_frame,anchor='center',text="Image processing",font=("Comic Sans MS", 40, "bold"),)
        self.title_lable.grid(row=0, column=0,padx=200 ,pady=(10, 0))
        #########
        self.main_frame = customtkinter.CTkFrame(self,)
        self.main_frame.grid(row=0, column=1,pady=90, rowspan=5, sticky="n")
        self.main_frame.grid_rowconfigure(5, weight=1)
        self.bg_image = customtkinter.CTkImage(dark_image=Image.open(".\others\place_holder.jpg"),
                                               size=(500, 300))
        self.bg_image_label = customtkinter.CTkLabel(self.main_frame, image=self.bg_image,text="",)
        self.bg_image_label.grid(row=0, column=0)
        self.eroded_lable = customtkinter.CTkLabel(self.main_frame,text="Eroded:"+str(self.eroded_times),font=("Comic Sans MS", 20),)
        self.eroded_lable.grid(row=1,column=0)
        self.dilate_lable = customtkinter.CTkLabel(self.main_frame,text="Dilated:"+str(self.dilated_times),font=("Comic Sans MS", 20),)
        self.dilate_lable.place(x=20,y=299)
        #########
        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=3, column=1,  padx=0, pady=0, sticky="nwe")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=5, sticky="nsew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # set default values
        
        self.progressbar_1.configure(mode="determinate")
        self.progressbar_1.set(1)
        self.seg_button_1.configure(values=["Open Image", "Save Image","Erode", "Dilate"],command=self.segmented_button_callback)
    def erode(self):
        self.bg_image = customtkinter.CTkImage(dark_image=erode(self.bg_image.cget('dark_image')),
                                                    size=(500, 300))
        self.bg_image_label.configure(image=self.bg_image)
        self.bg_image_label._image = self.bg_image
        self.eroded_times +=1
        self.seg_button_1.set(0)
        self.progressbar_1.set(1)
        self.seg_button_1.configure(values=["Open Image", "Save Image","Erode", "Dilate"],command=self.segmented_button_callback)
    def dilate(self):
        self.bg_image = customtkinter.CTkImage(dark_image=dilate(self.bg_image.cget('dark_image')),
                                                    size=(500, 300))
        self.bg_image_label.configure(image=self.bg_image)
        self.bg_image_label._image = self.bg_image
        self.dilated_times +=1
        self.seg_button_1.set(0)
        self.progressbar_1.set(1)
        self.seg_button_1.configure(values=["Open Image", "Save Image","Erode", "Dilate"],command=self.segmented_button_callback)
    def get_random_cancer(self):
        all_cancer=[]
        for path, subdirs, files in os.walk("./Dataset/1_test"):
            for name in files:
                try:
                    print(name)
                    all_cancer.append(name)
        
                except Exception as ex:
                    print(ex)
        random.shuffle(all_cancer)
        Thread(target=self.start_process()).start()
        filepath = os.path.join(path, all_cancer[0])
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(classify.classifiy, filepath)
            return_value = future.result()
        self.bg_image = customtkinter.CTkImage(Image.open(filepath),
                                           size=(500, 300))
        self.bg_image_label.configure(image=self.bg_image)
        self.bg_image_label._image = self.bg_image
        self.seg_button_1.set(0)
        self.progressbar_1.configure(mode="determinate")
        self.progressbar_1.stop()
        self.progressbar_1.set(1)
        return_value= return_value.split(" ")[0]
        if(return_value == '1'):
            self.prediction_lable.configure(self.main_frame,text="Prediction: Has Cancer",font=("Comic Sans MS", 20),text_color=("#ff0000"),)
        else:
            self.prediction_lable.configure(self.main_frame,text="Prediction: Has NOT Cancer",font=("Comic Sans MS", 20),text_color=("#00ff00"),)
        self.seg_button_1.set(0)
        self.progressbar_1.configure(mode="determinate")
        self.progressbar_1.stop()
        self.progressbar_1.set(1)
    def get_random_noncancer(self):
        all_cancer=[]
        for path, subdirs, files in os.walk("./Dataset/0_test"):
            for name in files:
                try:
                    print(name)
                    all_cancer.append(name)
        
                except Exception as ex:
                    print(ex)
        random.shuffle(all_cancer)
        Thread(target=self.start_process()).start()
        filepath = os.path.join(path, all_cancer[0])
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(classify.classifiy, filepath)
            return_value = future.result()
        self.bg_image = customtkinter.CTkImage(Image.open(filepath),
                                           size=(500, 300))
        self.bg_image_label.configure(image=self.bg_image)
        self.bg_image_label._image = self.bg_image
        self.seg_button_1.set(0)
        self.progressbar_1.configure(mode="determinate")
        self.progressbar_1.stop()
        self.progressbar_1.set(1)
        return_value= return_value.split(" ")[0]
        if(return_value == '1'):
            self.prediction_lable.configure(self.main_frame,text="Prediction: Has Cancer",font=("Comic Sans MS", 20),text_color=("#ff0000"),)
        else:
            self.prediction_lable.configure(self.main_frame,text="Prediction: Has NOT Cancer",font=("Comic Sans MS", 20),text_color=("#00ff00"),)
        self.seg_button_1.set(0)
        self.progressbar_1.configure(mode="determinate")
        self.progressbar_1.stop()
        self.progressbar_1.set(1)
    def segmented_button_callback(self,selected_segment :str):
        if(selected_segment=="Browse Image"):
            self.browse_image()
        elif(selected_segment=="Open Image"):
            self.open_image()
        elif(selected_segment=="Save Image"):
            self.save_file(self.bg_image.cget('dark_image'))
        elif(selected_segment=="Erode"):
            self.erode()
            self.eroded_lable.configure(text="Eroded:"+str(self.eroded_times))
        elif(selected_segment=="Dilate"):
            self.dilate()
            self.dilate_lable.configure(text="Dilated:"+str(self.dilated_times))
        elif(selected_segment=="get random cancer img"):
            self.get_random_cancer()
        elif(selected_segment=="get random non-cancer img"):
            self.get_random_noncancer()

        print(selected_segment)
    def start_process(self):
        self.progressbar_1.configure(mode="indeterminate")
        self.progressbar_1.start()

    def browse_image(self):
        Thread(target=self.start_process()).start()
        file = filedialog.askopenfile(mode='r', filetypes=[('Image', ('*.jpg','*.png'))])
        if file:
            filepath = os.path.abspath(file.name)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(classify.classifiy, filepath)
                return_value = future.result()
            self.bg_image = customtkinter.CTkImage(Image.open(filepath),
                                               size=(500, 300))
            self.bg_image_label.configure(image=self.bg_image)
            self.bg_image_label._image = self.bg_image
            self.seg_button_1.set(0)
            self.progressbar_1.configure(mode="determinate")
            self.progressbar_1.stop()
            self.progressbar_1.set(1)
            return_value= return_value.split(" ")[0]
            if(return_value == '1'):
                self.prediction_lable.configure(self.main_frame,text="Prediction: Has Cancer",font=("Comic Sans MS", 20),text_color=("#ff0000"),)
            else:
                self.prediction_lable.configure(self.main_frame,text="Prediction: Has NOT Cancer",font=("Comic Sans MS", 20),text_color=("#00ff00"),)
            print(return_value)
        else:
            self.seg_button_1.set(0)
            self.progressbar_1.configure(mode="determinate")
            self.progressbar_1.stop()
            self.progressbar_1.set(1)
    def open_image(self):
        Thread(target=self.start_process()).start()
        file = filedialog.askopenfile(mode='r', filetypes=[('Image', ('*.jpg','*.png'))])
        if file:
            filepath = os.path.abspath(file.name)
            self.bg_image= customtkinter.CTkImage(dark_image=Image.open(filepath),size=(500, 300))
            self.bg_image_label.configure(image=self.bg_image)
            self.bg_image_label._image = self.bg_image
            self.seg_button_1.set(0)
            self.progressbar_1.configure(mode="determinate")
            self.progressbar_1.stop()
            self.progressbar_1.set(1)
        else:
            self.seg_button_1.set(0)
            self.progressbar_1.configure(mode="determinate")
            self.progressbar_1.stop()
            self.progressbar_1.set(1)
    def save_file(self,image):
        Thread(target=self.start_process()).start()

        file = filedialog.asksaveasfile(mode='w', filetypes=(
                    ("Image", "*.jpg"),
                ),defaultextension='.jpg',)
                
        if file:
            image.save(file) # saves the image to the input file name. 
            self.seg_button_1.set(0)
            self.progressbar_1.configure(mode="determinate")
            self.progressbar_1.stop()
            self.progressbar_1.set(1)
        else:
            self.seg_button_1.set(0)
            self.progressbar_1.configure(mode="determinate")
            self.progressbar_1.stop()
            self.progressbar_1.set(1)
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self,page):
        page()


if __name__ == "__main__":
    app = App()
    app.page_0()
    app.mainloop()