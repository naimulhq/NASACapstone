import os
os.system("sudo killall ibus-daemon")
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1214)
Config.set('graphics', 'height', 743)
from kivy.logger import Logger
import logging
Logger.setLevel(logging.TRACE)

import kivy
from kivy.app import App
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



class ProcedureScreen(Screen):
    pass

class ValidateScreen(Screen):
    pass
	

class Project_Argus(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ProcedureScreen(name='procedureScreen'))
        sm.add_widget(ValidateScreen(name='validateScreen'))
        return sm


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
        stage_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/Stages/All_Stages.onnx'

	#os.system("sudo modprobe v4l2loopback") for Rishit
	#os.system("ffmpeg -thread_queue_size 512 -i rtsp://192.168.1.1/MJPG -vcodec rawvideo -vf scale=1920:1080 -f v4l2 -threads 0 -pix_fmt yuyv422 /dev/video1") for Rishit
	time.sleep(5)
        # This net used with Part Detection.
        # Change model directory depending on user. Stores labels in same directory as src

        self.part_net = jetson.inference.detectNet(argv=['--model='+part_model_path,'--labels=./labels_parts.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.9'])
        self.stages_net = jetson.inference.detectNet(argv=['--model='+stage_model_path,'--labels=./labels_stages.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.9'])
        self.camera = jetson.utils.videoSource("csi://0") 
	#self.camera = jetson.utils.videoSource("/dev/video1")# '/dev/video0'for Edwin '/dev/video1' for Rishit
        #self.display = jetson.utils.videoOutput() # 'my_video.mp4' for file
        self.clock = Clock.schedule_interval(self.update, 1.0 / 20)

    def update(self, dt):
        img = self.camera.Capture()
        detections = self.part_net.Detect(img) # Holds all the valuable Information
        stages = self.stages_net.Detect(img)
        array = jetson.utils.cudaToNumpy(img)
        buf1 = cv2.flip(array,0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(array.shape[1],array.shape[0]),colorfmt='bgr')
        image_texture.blit_buffer(buf,colorfmt='bgr',bufferfmt='ubyte')
        self.texture = image_texture

if __name__ == "__main__":
	Project_Argus().run()


