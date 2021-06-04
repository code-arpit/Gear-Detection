from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk
import time
from detect_GEAR import count_teeth
import os 
import glob
import numpy as np

#class for main app
class App:
    def __init__(self, Video_source=0):
        self.window = Tk()
        self.window.title("Gear detector")
        self.window.resizable=(0,0)
        self.window.configure(bg='#2a2a2e')
        self.Video_source = Video_source
        self.vid = Gear_capture(self.Video_source)
        self.label = Label(self.window, text= "Gear Detector", font=15)
        self.video_frame = LabelFrame(self.window, text = 'Gear Image', padx=5, pady=5, width=self.vid.width, height= self.vid.height)
        self.video_frame.grid(row=0, column=0,rowspan=16,padx=20,pady=20)
        #creating a canvas for video
        self.canvas= Canvas(self.video_frame, width=self.vid.width, height= self.vid.height)
        self.canvas.grid(row=0, column=0)

        Trigger_b= Button(self.video_frame, text="Trigger", width=40, padx=5, pady=10,command = self.snapshot)
        Trigger_b.grid(row=1, column=0, pady=10)

        # buttons beside frame...............
        Reset_b= Button(self.window, text="Reset", pady=5, width=10, padx=5, command= self.reset)
        Reset_b.grid(row=4, column=1)

        self.Indicator = Label(self.window, text='PASS/FAIL', width=12, height=3)        
        self.Indicator.grid(row=2 ,column=1) 
        
        self.teeth_frame = LabelFrame(self.window, padx=5, pady=5)
        self.teeth_frame.grid(row=6, column=1, padx=10)
        self.teeths_l = Label(self.teeth_frame, text="Teeths")
        self.teeths_l.grid(row=0, column=1)
        self.teeths_no = Label(self.teeth_frame, text='_', width=10)
        self.teeths_no.grid(row=1 ,column=1)
        
        
        pass_frame = LabelFrame(self.window, padx=5, pady=5)
        pass_frame.grid(row=8, column=1, padx=15)
        Pass_l= Label(pass_frame, text="Pass", padx=10)
        Pass_l.grid(row=0, column=1)
        Pass_b= Label(pass_frame, text="10",width=10)
        Pass_b.grid(row=1, column=1)

        fail_frame = LabelFrame(self.window, padx=5, pady=5)
        fail_frame.grid(row=10, column=1, padx=15)
        Fail_l= Label(fail_frame, text="Fail", padx=10)
        Fail_l.grid(row=0, column=1)
        Fail_b= Label(fail_frame, text="2",width=10)
        Fail_b.grid(row=1, column=1)

        total_frame = LabelFrame(self.window, padx=5, pady=5)
        total_frame.grid(row=12, column=1, padx=15)
        Total_l= Label(total_frame, text="Total", padx=10)
        Total_l.grid(row=0, column=1)
        Total_b= Label(total_frame, text="12",width=10)
        Total_b.grid(row=1, column=1)

        Exit_b = Button(self.window,text="EXIT", padx=5, pady=5,width=10, command = self.window.quit)
        Exit_b.grid(row=14, column=1, padx=5)
        
        self.update()

        self.window.mainloop()

    def update(self):
        #get frame from video source
        check, frame = self.vid.getFrame()
        if check:
            self.photo = ImageTk.PhotoImage(image= Image.fromarray(frame))
            self.canvas.create_image(0,0, image = self.photo, anchor = NW)

        self.window.after(1, self.update)

    def snapshot(self):
        #get frame from video source
        self.path = 'Images'
        self.file_type = '.jpg'
        if not os.path.exists(self.path):
            os.makedirs(path)
        check, frame = self.vid.getFrame()   
        if check:
            gear_name = "IMG-" + time.strftime("%m-%d-%H-%M-%S") + self.file_type
            frame_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            cv.imwrite(os.path.join(self.path, gear_name), frame_image)

        # destroying video and replacing it with clicked photo
        self.canvas.destroy()
        self.gear_photo_name = self.path + '/' + gear_name
        canvas = Canvas(self.video_frame, width=self.vid.width, height= self.vid.height)
        canvas.grid(row =0 , column =0)
        self.vid = ImageTk.PhotoImage(Image.open(f'{self.gear_photo_name}'))
        canvas.create_image(0,0, image=self.vid, anchor=NW)

        self.teeths = 0
        self.num_teeth = count_teeth(f'{self.gear_photo_name}', self.teeths)
        print(self.num_teeth)

        self.indicator_text = 'PASS/FAIL'
        if self.num_teeth < 40:
            self.indicator_bg = 'Red'
            self.indicator_text = 'FAIL'
        else :
            self.indicator_bg = 'Green'
            self.indicator_text = 'PASS'    

        self.Indicator = Label(self.window, text=self.indicator_text, width=12, height=3, background=self.indicator_bg)        
        self.Indicator.grid(row=2 ,column=1) 
        
        self.teeth_frame = LabelFrame(self.window, padx=5, pady=5)
        self.teeth_frame.grid(row=6, column=1, padx=10)
        self.teeths_l = Label(self.teeth_frame, text="Teeths")
        self.teeths_l.grid(row=0, column=1)
        self.teeths_no = Label(self.teeth_frame, text=f'{self.num_teeth}', width=10)
        self.teeths_no.grid(row=1 ,column=1) 
         #getting latest picture 
        
    def reset(self):        
        self.vid = Gear_capture(self.Video_source)
        self.label = Label(self.window, text= "Gear Detector", font=15)
        #creating a canvas for video
        self.canvas= Canvas(self.video_frame, width=self.vid.width, height= self.vid.height)
        self.canvas.grid(row=0, column=0)

        self.Indicator = Label(self.window, text='PASS/FAIL', width=12, height=3)        
        self.Indicator.grid(row=2 ,column=1) 
        
        self.teeth_frame = LabelFrame(self.window, padx=5, pady=5)
        self.teeth_frame.grid(row=6, column=1, padx=10)
        self.teeths_l = Label(self.teeth_frame, text="Teeths")
        self.teeths_l.grid(row=0, column=1)
        self.teeths_no = Label(self.teeth_frame, text='_', width=10)
        self.teeths_no.grid(row=1 ,column=1)


        self.update()
        
# Class for capturing video
class Gear_capture:
    def __init__(self, Video_source=0):
        #opening video
        self.vid = cv.VideoCapture(Video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open this camera \n Open another camera source")

        #getting video's width and height
        self.width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)

    def getFrame(self):
        if self.vid.isOpened():
            check, frame = self.vid.read()
            if check:
                #if check object is true then frame will be converted to rgb
                return (check, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            else:
                return (check, None)
        else:
            return (None)
                  
if __name__ == "__main__":
    App()


#doubts
# 1)refresh function ourside class
# 2)getting photo 
