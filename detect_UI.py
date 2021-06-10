from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk
import time
from detect_GEAR import detect_teeth
import os 
import numpy as np
from Config import *

#class for main app
class App:
    def __init__(self, Video_source):
        self.window = Tk()
        self.window.title(getApplication_Name())
        self.window.resizable=(0,0)
        self.Video_source = Video_source
        self.vid = Gear_capture(self.Video_source)
        self.label = Label(self.window, text= "Gear Detector", font=25)
        self.video_frame = LabelFrame(self.window, text = 'Gear Image', padx=5, pady=5, width=self.vid.width, height= self.vid.height)
        self.video_frame.grid(row=0, column=0,rowspan=16,padx=20,pady=20)
        #creating a canvas for video
        self.canvas= Canvas(self.video_frame, width=self.vid.width, height= self.vid.height)
        self.canvas.grid(row=0, column=0)

        Trigger_b= Button(self.video_frame, text="Trigger", width=30, padx=5, pady=10,command = self.snapshot)
        Trigger_b.grid(row=1, column=0, pady=10)

        # buttons beside frame...............
        Reset_b= Button(self.window, text="Reset", width=10, padx=5, command= self.reset)
        Reset_b.grid(row=4, column=1)

        self.Indicator = Label(self.window, text='PASS/FAIL', width=12, height=3 ,relief="raised")        
        self.Indicator.grid(row=2 ,column=1) 
        
        self.teeth_frame = LabelFrame(self.window, padx=5, pady=5)
        self.teeth_frame.grid(row=6, column=1, padx=10)
        self.teeths_l = Label(self.teeth_frame, text="Teeths")
        self.teeths_l.grid(row=0, column=1)
        self.teeths_no = Label(self.teeth_frame, text='_', width=10)
        self.teeths_no.grid(row=1 ,column=1)
                
        self.Pass_frame = LabelFrame(self.window, padx=5, pady=5)
        self.Pass_frame.grid(row=8, column=1, padx=15)
        self.Pass_l= Label(self.Pass_frame, text="Pass", padx=10)
        self.Pass_l.grid(row=0, column=1)
        self.Pass_b= Label(self.Pass_frame, text='_', width=10)
        self.Pass_b.grid(row=1, column=1)

        self.Fail_frame = LabelFrame(self.window, padx=5, pady=5)
        self.Fail_frame.grid(row=10, column=1, padx=15)
        self.Fail_l= Label(self.Fail_frame, text="Fail", padx=10)
        self.Fail_l.grid(row=0, column=1)
        self.Fail_b= Label(self.Fail_frame, text='_', width=10)
        self.Fail_b.grid(row=1, column=1)

        self.Total_frame = LabelFrame(self.window, padx=5, pady=5)
        self.Total_frame.grid(row=12, column=1, padx=15)
        self.Total_l= Label(self.Total_frame, text="Total", padx=10)
        self.Total_l.grid(row=0, column=1)
        self.Total_b= Label(self.Total_frame, text="_",width=10)
        self.Total_b.grid(row=1, column=1)

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
        self.path = getStorage_Path()
        self.file_type = getFile_Type()
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        check, frame = self.vid.getFrame()   
        if check:
            # self.gear_name = "Images/IMG-06-05-11-00-07.jpg"
            self.gear_name = self.path + '/IMG-' + time.strftime("%m-%d-%H-%M-%S") + self.file_type
            self.frame_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            cv.imwrite(os.path.join(self.gear_name), self.frame_image)

        self.detect(self.gear_name)
        # self.detect('gear.jpg')
        
    def detect(self, gear_photo):
        self.teeths = 0
        self.gear_photo = gear_photo
        self.return_teeth = detect_teeth(self.gear_photo, self.teeths)
        self.photo_teeth = self.return_teeth.teeth()[0]
        self.num_teeth = self.return_teeth.teeths
        self.num_pass = 0 
        self.num_fail = 0
        self.num_total = self.num_pass + self.num_fail
        #Indicator for pass and fail
        self.indicator_text = 'PASS/FAIL'
        if self.num_teeth < 40:
            self.indicator_bg = 'Red'
            self.indicator_text = 'FAIL'
        else :
            self.indicator_bg = 'Green'
            self.indicator_text = 'PASS'    

        self.Indicator = Label(self.window, text=self.indicator_text, width=12, height=3, background=self.indicator_bg,relief="raised")        
        self.Indicator.grid(row=2 ,column=1)

        self.new_gear_name = self.path + "/IMG-" + time.strftime("%m-%d-%H-%M-%S-") + self.indicator_text + self.file_type 
        cv.imwrite(os.path.join(self.new_gear_name), self.photo_teeth) 
        self.gear_photo_name = self.new_gear_name

        for root, dirs, files in os.walk(self.path):
                for file in files: 
                    if file.endswith('PASS.jpg'):
                        self.num_pass += 1
                    elif file.endswith('FAIL.jpg'):
                        self.num_fail += 1         
        
        self.teeths_no = Label(self.teeth_frame, text=f'{self.num_teeth}', width=10)
        self.teeths_no.grid(row=1 ,column=1)

        self.Pass_b= Label(self.Pass_frame, text=f'{self.num_pass}', width=10)
        self.Pass_b.grid(row=1, column=1)

        self.Fail_b= Label(self.Fail_frame, text=f'{self.num_fail}',width=10)
        self.Fail_b.grid(row=1, column=1)

        self.num_total = self.num_pass + self.num_fail
        self.Total_b= Label(self.Total_frame, text=f'{self.num_total}',width=10)
        self.Total_b.grid(row=1, column=1)

        # destroying video and replacing it with clicked photo
        self.canvas.destroy()
        canvas = Canvas(self.video_frame, width=self.vid.width, height= self.vid.height)
        canvas.grid(row =0 , column =0)
        self.vid = ImageTk.PhotoImage(Image.open(f'{self.gear_photo_name}'))
        canvas.create_image(0,0, image=self.vid, anchor=NW) 

    def reset(self):        
        self.vid = Gear_capture(self.Video_source)
        self.label = Label(self.window, text= "Gear Detector", font=15)
        #creating a canvas for video
        self.canvas= Canvas(self.video_frame, width=self.vid.width, height= self.vid.height)
        self.canvas.grid(row=0, column=0)

        self.Indicator = Label(self.window, text='PASS/FAIL', width=12, height=3 ,relief="raised")        
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
    App(getVideo_Source())
