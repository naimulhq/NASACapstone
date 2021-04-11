import os
os.system("sudo killall ibus-daemon")
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1214)	# DON'T CHANGE THIS
Config.set('graphics', 'height', 743)	# DON'T CHANGE THIS
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)

import kivy
from kivy.app import App
from kivy.graphics import Color
from kivymd.app import MDApp
from kivy.uix.label import Label
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
#from kivy.lang import Builder
#from kivy.uix.screenmanager import ScreenManager, Screen
#from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.camera import Camera
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.textfield import MDTextFieldRect
import cv2
import jetson.inference
import jetson.utils
import csv
import sys
import time
from datetime import datetime
from functools import partial


class ProcedureScreen(Screen):
    def pressed_forward(self,cam,label):
        if (cam.currentInstr < len(cam.instructions)-1) and not cam.isComplete :
            cam.currentInstr += 1
            label.text += "Forward:\n\n" + cam.instructions[cam.currentInstr][1] + ": " + cam.instructions[cam.currentInstr][0] +"\n\n"
        elif (cam.currentInstr == len(cam.instructions) - 1) and not cam.isComplete:
            label.text += "Procedure Complete!\n\nClose window or return to main menu.\n\n"
            cam.isComplete = True
        else:
            label.text += "Cannot go forward. The procedure is complete.\n\nClose window or return to main menu.\n\n"


    def pressed_previous(self,cam,label):
        if (cam.currentInstr > 0) and not cam.isComplete:
            cam.currentInstr -= 1
            label.text += "Previous:\n\n" + cam.instructions[cam.currentInstr][1] + ": " + cam.instructions[cam.currentInstr][0] +"\n\n"
        elif cam.currentInstr == 0:
            label.text += "Currently on first instruction. Cannot go back a stage.\n\n"
        else:
            label.text += "Cannot go backward. The procedure is complete.\n\nClose window or return to main menu.\n\n"

    def beginValidation(self,cam,label):
        if (cam.currentInstr < len(cam.instructions)) and not cam.isComplete:
            label.text += "Begin Validation\n\n"
            cam.clock2 = Clock.schedule_interval(partial(cam.stageValidate, label), 1.0/20)
        else:
            label.text += "Procedure Complete! Can not validate!\n\nClose or return to main menu.\n\n"
        

button_exist=False
class MainMenu(Screen):

    def add_button(self,grid):
        global button_exist

        if(button_exist==False):
            button = Button(text="Begin",size_hint_y=None,
                            height=100,size_hint_x=None,
                            width=400)
            button.bind(on_press=self.go_to_procedure)
            grid.add_widget(button)
            button_exist=True
        
    def go_to_procedure(self,instance):
        app.sm.current="procedureScreen"
        sc = app.sm.get_screen("procedureScreen")
        sc.ids.bottomleft.text = "Welcome to Project Argus! \n\n" + self.firstStage

    def load_procedure(self,path,label):
        count = 0
        with open(path) as csvDataFile:
            csvReader = csv.reader(csvDataFile)            
            label.text = ''
            for row in csvReader:
                if count == 0:
                    self.firstStage = str(row[1]) + ": " + str(row[0]) + '\n\n'
                    count += 1
                label.text += "         - " + str(row[1]) + ": " + str(row[0]) + '\n'
        

class Project_Argus(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainMenu(name='mainMenu'))
        self.sm.add_widget(ProcedureScreen(name='procedureScreen'))
        return self.sm


class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        # self.capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        # Ask user for names of parts and stages model. Only for testing purposes.
        dirs = os.listdir('/home')
        #part_model_name = input("Enter part model name with extension: ")
        #stage_model_name = input("Enter stage model name with extension: ")
        dirs = os.listdir('/home')
        #part_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/PartDetection/' + str(part_model_name)
        #stage_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/Stages/' + str(stage_model_name)
        part_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/PartDetection/All_Parts.onnx'
        stage_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/Stages/All_Stages_Test.onnx'

	#os.system("sudo modprobe v4l2loopback") for Rishit
	#os.system("ffmpeg -thread_queue_size 512 -i rtsp://192.168.1.1/MJPG -vcodec rawvideo -vf scale=1920:1080 -f v4l2 -threads 0 -pix_fmt yuyv422 /dev/video1") for Rishit
	#time.sleep(5)
        # This net used with Part Detection.
        # Change model directory depending on user. Stores labels in same directory as src

        self.part_net = jetson.inference.detectNet(argv=['--model='+part_model_path,'--labels=./labels_parts.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.9'])
        self.stages_net = jetson.inference.detectNet(argv=['--model='+stage_model_path,'--labels=./labels_stages.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.9'])
        self.camera = jetson.utils.videoSource("csi://0") #csi://0 
        #self.camera = jetson.utils.videoSource("/dev/video0")# '/dev/video0'for Edwin '/dev/video1' for Rishit
        #self.display = jetson.utils.videoOutput() # 'my_video.mp4' for file
        self.clock = Clock.schedule_interval(self.update, 1.0 / 20)
        self.clock2 = None
        self.isComplete = False

        with open(os.path.join(sys.path[0], "instructions.csv"),'r') as file:
            reader = csv.reader(file)
            self.instructions = list(reader)

        print(self.instructions)

        f = open("labels_stages.txt","r")
        self.labels_stages = []
        for i in f.readlines():
            self.labels_stages.append(i.strip('\n'))
        f.close()

        self.timeout = 0
        self.currentInstr, self.stageCount = 0, 0

    def update(self, dt):
        self.img = self.camera.Capture()
        self.detections = self.part_net.Detect(self.img) # Holds all the valuable Information
        self.stages = self.stages_net.Detect(self.img)
        array = jetson.utils.cudaToNumpy(self.img)
        buf1 = cv2.flip(array,0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(array.shape[1],array.shape[0]),colorfmt='rgb')
        image_texture.blit_buffer(buf,colorfmt='rgb',bufferfmt='ubyte')
        self.texture = image_texture

    def stageValidate(self,label,dt):
        self.timeout += 1
        if len(self.stages) == 0:
            pass
        else:
            if self.labels_stages[self.stages[0].ClassID] == self.instructions[self.currentInstr][1]:
                self.stageCount += 1
            else:
                self.stageCount = 0

            if self.stageCount == 48:
                self.currentInstr += 1
                self.stageCount = 0
                label.text += "Validation Successful\n\n\n" + self.instructions[self.currentInstr][1] + ": " + self.instructions[self.currentInstr][0] + "\n\n"
                Clock.unschedule(self.clock2)

        if self.timeout == 1200:
            label.text += "Validation Unsuccessful. Time expired!\n\n"
            Clock.unschedule(self.clock2)
            self.timeout = 0
            
			

if __name__ == "__main__":
    app=Project_Argus()
    app.run()


