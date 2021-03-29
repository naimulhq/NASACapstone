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

from kivymd.uix.textfield import MDTextField
from kivymd.uix.textfield import MDTextFieldRect
import cv2
import jetson.inference
import jetson.utils
import csv
import sys
import time
from datetime import datetime


#Using KV
class MyGrid(Widget):
	def print_button_text(self,label):
		label.text += "poop"
		#instance.text

	def pressed_validate(self,label):
		label.text += "Validate\n"


	def pressed_forward(self,label):
		label.text += "Forward\n"

	def pressed_previous(self,label):
		label.text += "Previous\n"

	

class Project_Argus(MDApp):
	def build(self):
		return MyGrid()

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


        # This net used with Part Detection.
        # Change model directory depending on user. Stores labels in same directory as src

        self.part_net = jetson.inference.detectNet(argv=['--model='+part_model_path,'--labels=./labels_parts.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.9'])
        self.stages_net = jetson.inference.detectNet(argv=['--model='+stage_model_path,'--labels=./labels_stages.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.9'])
        self.camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for Edwin
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


