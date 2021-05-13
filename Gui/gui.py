import os
os.system("sudo killall ibus-daemon")
os.system("./preSetup.sh")
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1214)	# DON'T CHANGE THIS
Config.set('graphics', 'height', 743)	# DON'T CHANGE THIS

import kivy
from kivy.app import App
from kivy.graphics import Color
from kivymd.app import MDApp
from kivy.uix.label import Label
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
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

from kivy.properties import ObjectProperty
from database import DataBase
from kivy.uix.popup import Popup
from kivy.lang import Builder

import face_recognition
import pickle
import time

class ProcedureScreen(Screen):
    def pressed_forward(self,cam,label):
        cam=app.camera
        if (cam.currentInstr < len(cam.instructions)-1):
            cam.currentInstr += 1
            label.text += "Forward:\n\n" + cam.instructions[cam.currentInstr][1] + ": " + cam.instructions[cam.currentInstr][0]
            label.text += "\n\nParts required: " + cam.instructions[cam.currentInstr][2][1:-1] + "\n\n"
            cam.missedValidations = 0
        elif (cam.currentInstr >= len(cam.instructions) - 1):
            #cam.currentInstr += 1
            label.text += "Procedure Complete!\n\nClose window or return to main menu.\n\n"

            # Create two csv files: one will hold information about parts and other will hold information about procedure
            label.text += "Writing Information into CSV Files... "

            with open('Stages.csv',mode='w') as stages_file:
                stages_file_writer = csv.writer(stages_file,delimiter=',')
                stages_file_writer.writerow(['Stage Completed', 'Time Completed', 'Missed Validations'])
                for i in range(len(cam.StageName)):
                    stages_file_writer.writerow([cam.StageName[i],cam.StageTimeStamps[i],cam.incorrectValidation[i]])

            with open('Parts.csv',mode='w') as parts_file:
                parts_file_writer = csv.writer(parts_file,delimiter=',')
                parts_file_writer.writerow(['Object Name', 'Top Left Coordinate', 'Top Right Coordinate', 'Bottom Right Coordinate', 'Bottom Left Coordinate', 'Time Stamped'])
                for i in range(len(cam.objects)):
                    parts_file_writer.writerow([cam.objects[i], cam.vertices[i][0],cam.vertices[i][1],cam.vertices[i][2],cam.vertices[i][3],cam.PartTimeStamps[i]])

            label.text += "Writing Complete.\n\n"
        else:
            label.text += "Cannot go forward. The procedure is complete.\n\nClose window or return to main menu.\n\n"


    def pressed_previous(self,cam,label):
        cam=app.camera
        if (cam.currentInstr > 0):
            cam.currentInstr -= 1
            label.text += "Previous:\n\n" + cam.instructions[cam.currentInstr][1] + ": " + cam.instructions[cam.currentInstr][0]
            label.text += "\n\nParts required: " + cam.instructions[cam.currentInstr][2][1:-1] + "\n\n"
            cam.missedValidations = 0
        else:
            label.text += "Currently on first instruction. Cannot go back a stage.\n\n"


    def beginValidation(self,cam,label):
        cam=app.camera
        if (cam.currentInstr < len(cam.instructions)):
            instructionString = cam.instructions[cam.currentInstr][1]
            if(instructionString == "Stage 6.1" or instructionString == "Stage 6.2" or instructionString == "Stage 6.3" ):
                cam.stageValidatePopup(instructionString,label)
            else:
                cam.isValidate = True
                label.text += "Begin Validation\n\n"
                cam.clock2 = Clock.schedule_interval(partial(cam.stageValidate, label), 1.0/20)
        else:
            label.text += "Procedure Complete! Can not validate!\n\nClose or return to main menu.\n\n"

    def updateChecklist(self,cam,label,fix):
        cam=app.camera
        temp = cam.currentInstr + fix
        if temp <= 0:
            label.text += cam.instructions[0][1] + " - Current\n\n"
            label.text += cam.instructions[1][1] + "\n\n"
            label.text += cam.instructions[2][1] + "\n\n"
            label.text += cam.instructions[3][1] + "\n\n"
            label.text += cam.instructions[4][1] + "\n\n"
        elif temp == 1:
            label.text += cam.instructions[0][1] + " - Done\n\n"
            label.text += cam.instructions[1][1] + " - Current\n\n"
            label.text += cam.instructions[2][1] + "\n\n"
            label.text += cam.instructions[3][1] + "\n\n"
            label.text += cam.instructions[4][1] + "\n\n"
        elif temp == len(cam.instructions)-1:
            label.text += cam.instructions[-5][1] + " - Done\n\n"
            label.text += cam.instructions[-4][1] + " - Done\n\n"
            label.text += cam.instructions[-3][1] + " - Done\n\n"
            label.text += cam.instructions[-2][1] + " - Done\n\n"
            label.text += cam.instructions[-1][1] + " - Current\n\n"
        elif temp == len(cam.instructions)-2:
            label.text += cam.instructions[-5][1] + " - Done\n\n"
            label.text += cam.instructions[-4][1] + " - Done\n\n"
            label.text += cam.instructions[-3][1] + " - Done\n\n"
            label.text += cam.instructions[-2][1] + " - Current\n\n"
            label.text += cam.instructions[-1][1] + "\n\n"
        elif temp >= len(cam.instructions):
            label.text += cam.instructions[-5][1] + " - Done\n\n"
            label.text += cam.instructions[-4][1] + " - Done\n\n"
            label.text += cam.instructions[-3][1] + " - Done\n\n"
            label.text += cam.instructions[-2][1] + " - Done\n\n"
            label.text += cam.instructions[-1][1] + " - Done\n\n"
        else:
            label.text += cam.instructions[temp-2][1] + " - Done\n\n"
            label.text += cam.instructions[temp-1][1] + " - Done\n\n"
            label.text += cam.instructions[temp][1] + " - Current\n\n"
            label.text += cam.instructions[temp+1][1] + "\n\n"
            label.text += cam.instructions[temp+2][1] + "\n\n"

    def openPreview(self,cam):
        cam=app.camera
        instructionStage = cam.instructions[cam.currentInstr][1]
        self.popup = Popup(title=instructionStage + " Preview",size_hint=(None, None), size=(400, 400))
        filename = instructionStage.replace(" ","")
        img = Image(source="StageImages/"+filename+".jpg")
        self.popup.content = img
        self.popup.open()

button_exist=False
class MainMenu(Screen):

    def add_button(self,grid):
        global button_exist

        if(button_exist==False):
            button = Button(text="Begin",size_hint_y=None,
                            height=100,size_hint_x=None,
                            width=400, pos=(810,3))
            button.bind(on_press=self.go_to_procedure)
            grid.add_widget(button)
            button_exist=True
        
    def go_to_procedure(self,instance):
        app.sm.current="procedureScreen"
        sc = app.sm.get_screen("procedureScreen")
        sc.ids.bottomleft.text = "Welcome to Project Argus! \n\n" + self.firstStage
        sc.ids.checklist.text += "Stage 1.2 - Current\n\n"
        sc.ids.checklist.text += "Stage 2.1\n\n"
        sc.ids.checklist.text += "Stage 2.2\n\n"
        sc.ids.checklist.text += "Stage 3.2\n\n"
        sc.ids.checklist.text += "Stage 4.1\n\n"

    def load_procedure(self,path,label):
        count = 0
        with open(path) as csvDataFile:
            csvReader = csv.reader(csvDataFile)            
            label.text = ''
            for row in csvReader:
                if count == 0:
                    self.firstStage = str(row[1]) + ": " + str(row[0]) + "\n\nParts required: " + str(row[2][1:-1]) + "\n\n"
                    count += 1
                label.text += "     - " + str(row[1]) + ": " + str(row[0]) + '\n'

class StartUp(Screen):
    def checkUser(self):
        if self.ids.userInput.text == "username" and self.ids.passwordInput.text == "password":
             app.sm.current = 'mainMenu'

class Project_Argus(MDApp):
    def build(self):
        # self.sm = ScreenManager()
        # self.sm.add_widget(StartUp(name='startUp'))
        # self.sm.add_widget(MainMenu(name='mainMenu'))
        # self.sm.add_widget(ProcedureScreen(name='procedureScreen'))
        # return self.sm
        # 0.77, 0.84
        self.camera = KivyCamera(allow_stretch=True,size_hint=(0.77, 0.84),pos_hint={"x":0.1, "y":0.15})
        self.camBool = True
        self.sm = ScreenManager()
        #self.sm.add_widget(StartUp(name='startUp'))
        self.sm.add_widget(LoginWindow(name='login'))
        self.sm.add_widget(CreateAccountWindow(name='create'))
        self.sm.add_widget(MainMenu(name='mainMenu'))
        self.sm.add_widget(ProcedureScreen(name='procedureScreen'))
        sc = app.sm.get_screen("login")
        sc.ids.FL.add_widget(self.camera)
        return self.sm

    

class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)

        self.camera=None
        self.font=cv2.FONT_HERSHEY_SIMPLEX
        self.Encodings=[]
        self.Names=[]
        self.fpsReport=0
        self.scaleFactor=.20
        self.timestamp = time.time()
        self.counter = 0
        with open('train2.pkl','rb') as f:
            self.Names=pickle.load(f)
            self.Encodings=pickle.load(f)

        dirs = os.listdir('/home')
        part_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/PartDetection/All_Parts.onnx'
        stage_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/Stages/All_Stages.onnx'

        # Lists will hold information for data collection of procedure
        self.objects = []
        self.vertices = []
        self.PartTimeStamps = []
        self.StageName = []
        self.StageTimeStamps = []
        self.incorrectValidation = []
        self.missedValidations = 0
        self.endTime = 0
       
	    #os.system("sudo modprobe v4l2loopback") for Rishit
	    #os.system("ffmpeg -thread_queue_size 512 -i rtsp://192.168.1.1/MJPG -vcodec rawvideo -vf scale=1920:1080 -f v4l2 -threads 0 -pix_fmt yuyv422 /dev/video1") for Rishit
	    #time.sleep(5)
        # This net used with Part Detection.
        # Change model directory depending on user. Stores labels in same directory as src

        self.part_net = jetson.inference.detectNet(argv=['--model='+part_model_path,'--labels=./labels_parts.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.9'])
        self.stages_net = jetson.inference.detectNet(argv=['--model='+stage_model_path,'--labels=./labels_stages.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.9'])
        #self.camera = jetson.utils.videoSource("csi://0") #csi://0 
        #self.camera = jetson.utils.videoSource("/dev/video0")# '/dev/video0'for Edwin '/dev/video1' for Rishit
        #self.display = jetson.utils.videoOutput() # 'my_video.mp4' for file
        self.camera=cv2.VideoCapture("/dev/video0")
        #self.camera=cv2.VideoCapture('udp://127.0.0.1:10000')
	#self.camera = cv2.VideoCapture("rtsp://192.168.1.1/MJPG")

        self.clock = Clock.schedule_interval(self.update, 1.0 / 20)
        self.clock2 = None
        self.isComplete = False
        self.isValidate = False

        with open(os.path.join(sys.path[0], "instructions.csv"),'r') as file:
            reader = csv.reader(file)
            self.instructions = list(reader)

        #print(self.instructions)

        f = open("labels_stages.txt","r")
        self.labels_stages = []
        for i in f.readlines():
            self.labels_stages.append(i.strip('\n'))
        f.close()

        f = open("labels_parts.txt","r")
        self.labels_parts = []
        for i in f.readlines():
            self.labels_parts.append(i.strip('\n'))
        f.close()

        self.timeout = 0
        self.currentInstr, self.stageCount = 0, 0

    def update(self, dt):
        self.beginTime = time.time()
        # self.img = self.camera.Capture()
        # if not self.isValidate:
        #     self.detections = self.part_net.Detect(self.img) # Holds all the valuable Information
        # else:
        #     self.stages = self.stages_net.Detect(self.img)
        # array = jetson.utils.cudaToNumpy(self.img)
        # buf1 = cv2.flip(array,0)
        # buf = buf1.tostring()
        # image_texture = Texture.create(size=(array.shape[1],array.shape[0]),colorfmt='rgb')
        # image_texture.blit_buffer(buf,colorfmt='rgb',bufferfmt='ubyte')
        # self.texture = image_texture
        #self.img = self.camera.Capture()
        _,self.img = self.camera.read()
        if app.camBool:

            #self.img = self.camera.Capture()
            #self.img = jetson.utils.cudaToNumpy(self.img)
            frame_small=cv2.resize(self.img,(0,0),fx=self.scaleFactor,fy=self.scaleFactor)
            frameRGB=cv2.cvtColor(frame_small,cv2.COLOR_BGR2RGB)
            facePositions=face_recognition.face_locations(frameRGB)#,model='cnn')
            allEncodings=face_recognition.face_encodings(frameRGB,facePositions)
            for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
                name='Unknown Person'
                matches=face_recognition.compare_faces(self.Encodings,face_encoding)
                if True in matches:
                    first_match_index=matches.index(True)
                    name=self.Names[first_match_index]
                    if name == "Edwin Varela" or name == "Naimul Hoque" or name == "Abel Semma" or name == "Rishit Arora" or name == "Oles Bober":
                        self.counter+=1
                        if self.counter>50:
                            self.counter=0
                            MainWindow.current = "edwin@gmail.com"
                            app.sm.current = "mainMenu"
                            app.camBool = False
                            sc = app.sm.get_screen("login")
                            sc.ids.FL.remove_widget(app.camera)
                            sc2 = app.sm.get_screen("procedureScreen")
                            sc2.ids.g2.add_widget(app.camera)

                            #self.camera.release()
                            #cv2.destroyAllWindows() 
                    else:
                        self.counter=0
                top=int(top/self.scaleFactor)
                right=int(right/self.scaleFactor)
                bottom=int(bottom/self.scaleFactor)
                left=int(left/self.scaleFactor)
                cv2.rectangle(self.img,(left,top),(right,bottom),(255,0,0),2)
                cv2.putText(self.img,name,(left,top-6),self.font,.75,(0,255,255),1)

            dt=time.time() - self.timestamp
            fps=1/dt
            self.fpsReport=.95*self.fpsReport + .05*fps
            cv2.rectangle(self.img,(0,0),(100,40),(255,0,0),-1)
            cv2.putText(self.img,str(round(self.fpsReport,1)) + ' fps ',(0,25),self.font,.75,(0,255,255),1)
            self.timestamp = time.time()

            buf1 = cv2.flip(self.img,0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(self.img.shape[1],self.img.shape[0]),colorfmt='rgb')
            image_texture.blit_buffer(buf,colorfmt='bgr',bufferfmt='ubyte')
            self.texture = image_texture
            cv2.destroyAllWindows()

        else:
            self.img = jetson.utils.cudaFromNumpy(self.img)
            if not self.isValidate:
                self.detections = self.part_net.Detect(self.img) # Holds all the valuable Information
            else:
                self.stages = self.stages_net.Detect(self.img)
            array = jetson.utils.cudaToNumpy(self.img)
            buf1 = cv2.flip(array,0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(array.shape[1],array.shape[0]),colorfmt='rgb')
            image_texture.blit_buffer(buf,colorfmt='bgr',bufferfmt='ubyte')
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
                self.StageName.append(self.instructions[self.currentInstr][1])
                self.incorrectValidation.append(self.missedValidations)
                self.missedValidations = 0
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                self.StageTimeStamps.append(current_time)
                self.isValidate = False
                self.currentInstr += 1
                self.stageCount = 0
                if(self.currentInstr < len(self.instructions)):
                    label.text += "Validation Successful\n\n" + self.instructions[self.currentInstr][1] + ": " + self.instructions[self.currentInstr][0]
                    label.text += "\n\nParts required: " + self.instructions[self.currentInstr][2][1:-1] + "\n\n"
                else:
                    label.text += "Procedure Complete"
                Clock.unschedule(self.clock2)
                sc = app.sm.get_screen("procedureScreen")
                if self.currentInstr <= 0:
                    sc.ids.checklist.text += self.instructions[0][1] + " - Current\n\n"
                    sc.ids.checklist.text += self.instructions[1][1] + "\n\n"
                    sc.ids.checklist.text += self.instructions[2][1] + "\n\n"
                    sc.ids.checklist.text += self.instructions[3][1] + "\n\n"
                    sc.ids.checklist.text += self.instructions[4][1] + "\n\n"
                elif self.currentInstr == 1:
                    sc.ids.checklist.text += self.instructions[0][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[1][1] + " - Current\n\n"
                    sc.ids.checklist.text += self.instructions[2][1] + "\n\n"
                    sc.ids.checklist.text += self.instructions[3][1] + "\n\n"
                    sc.ids.checklist.text += self.instructions[4][1] + "\n\n"
                elif self.currentInstr == len(self.instructions)-1:
                    sc.ids.checklist.text += self.instructions[-5][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-4][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-3][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-2][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-1][1] + " - Current\n\n"
                elif self.currentInstr == len(self.instructions)-2:
                    sc.ids.checklist.text += self.instructions[-5][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-4][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-3][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-2][1] + " - Current\n\n"
                    sc.ids.checklist.text += self.instructions[-1][1] + "\n\n"
                elif self.currentInstr >= len(self.instructions):
                    sc.ids.checklist.text += self.instructions[-5][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-4][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-3][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-2][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[-1][1] + " - Done\n\n"
                else:
                    sc.ids.checklist.text += self.instructions[self.currentInstr-2][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[self.currentInstr-1][1] + " - Done\n\n"
                    sc.ids.checklist.text += self.instructions[self.currentInstr][1] + " - Current\n\n"
                    sc.ids.checklist.text += self.instructions[self.currentInstr+1][1] + "\n\n"
                    sc.ids.checklist.text += self.instructions[self.currentInstr+2][1] + "\n\n"

            if(self.beginTime-self.endTime > 1):
                for i in range(len(self.detections)):
                    #if self.isValidate:
                    #self.objects.append(self.labels_stages[self.detections[i].ClassID-1])
                    #else:
                    self.objects.append(self.labels_parts[self.detections[i].ClassID])
                    # Store box vertices in clockwise order
                    bottomLeft = (self.detections[i].Left, self.detections[i].Bottom)
                    bottomRight = (self.detections[i].Right, self.detections[i].Bottom)
                    topLeft = (self.detections[i].Left, self.detections[i].Top)
                    topRight = (self.detections[i].Right, self.detections[i].Top)
                    self.vertices.append((topLeft,topRight,bottomRight,bottomLeft))
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                self.PartTimeStamps.append(current_time)
                self.endTime = time.time()

        if self.timeout == 400:
            self.isValidate = False
            label.text += "Validation Unsuccessful. Time expired!\n\n"
            self.missedValidations += 1
            Clock.unschedule(self.clock2)
            self.timeout = 0

    def stageValidatePopup(self,instructionStage,label):
        yesButton = Button(text="Yes")
        noButton = Button(text="No")
        yesButton.bind(on_press=partial(self.yesCallback, label))
        noButton.bind(on_press=partial(self.noCallback, label))

        if(instructionStage == "Stage 6.1"):
            self.popup = Popup(title=instructionStage+' Validation',size_hint=(None, None), size=(400, 400))
            grid1 = GridLayout(rows=2,cols=1)
            grid1.add_widget(Label(text="Does the Arbotix Board get detected by the computer?"))
            grid2 = GridLayout(rows=1,cols=2)
            grid2.add_widget(yesButton)
            grid2.add_widget(noButton)
            grid1.add_widget(grid2)
            self.popup.content = grid1
            self.popup.bind(on_open=partial(self.validationOptions, label))
            self.popup.open()


            
        elif(instructionStage == "Stage 6.2"):
            self.popup = Popup(title=instructionStage+' Validation',size_hint=(None, None), size=(400, 400))
            grid1 = GridLayout(rows=2,cols=1)
            grid1.add_widget(Label(text="Did the green led on the Arbotix board light up?"))
            grid2 = GridLayout(rows=1,cols=2)
            grid2.add_widget(yesButton)
            grid2.add_widget(noButton)
            grid1.add_widget(grid2)
            self.popup.content = grid1
            self.popup.open()
            
        elif(instructionStage == "Stage 6.3"):
            self.popup = Popup(title=instructionStage+' Validation',size_hint=(None, None), size=(400, 400))
            grid1 = GridLayout(rows=2,cols=1)
            grid1.add_widget(Label(text="Did you see the Robot Turret perform calibration movements?"))
            grid2 = GridLayout(rows=1,cols=2)
            grid2.add_widget(yesButton)
            grid2.add_widget(noButton)
            grid1.add_widget(grid2)
            self.popup.content = grid1
            #self.popup.bind(on_open=partial(self.validationOptions, label))
            self.popup.open()
        else:
            print("No stage exists.")
    
    def validationOptions(self,label,instance):
        pass
        
    def yesCallback(self,label,instance):
        self.StageName.append(self.instructions[self.currentInstr][1])
        self.incorrectValidation.append(self.missedValidations)
        self.missedValidations = 0
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.StageTimeStamps.append(current_time)
        self.isValidate = False
        self.currentInstr += 1
        app.sm.current="procedureScreen"
        sc = app.sm.get_screen("procedureScreen")
        if(self.currentInstr < len(self.instructions)):
            label.text += "Validation Successful\n\n" + self.instructions[self.currentInstr][1] + ": " + self.instructions[self.currentInstr][0]
            label.text += "\n\nParts required: " + self.instructions[self.currentInstr][2][1:-1] + "\n\n"
            if(self.currentInstr == 9):
                sc.ids.checklist.text += "Stage 5.2 - Done\n\n"
                sc.ids.checklist.text += "Stage 5.6 - Done\n\n"
                sc.ids.checklist.text += "Stage 6.1 - Current\n\n"
                sc.ids.checklist.text += "Stage 6.2\n\n"
                sc.ids.checklist.text += "Stage 6.3\n\n"
            elif(self.currentInstr == 10):
                sc.ids.checklist.text += "Stage 5.2 - Done\n\n"
                sc.ids.checklist.text += "Stage 5.6 - Done\n\n"
                sc.ids.checklist.text += "Stage 6.1 - Done\n\n"
                sc.ids.checklist.text += "Stage 6.2 - Current\n\n"
                sc.ids.checklist.text += "Stage 6.3\n\n"
            elif(self.currentInstr == 11):
                sc.ids.checklist.text += "Stage 5.2 - Done\n\n"
                sc.ids.checklist.text += "Stage 5.6 - Done\n\n"
                sc.ids.checklist.text += "Stage 6.1 - Done\n\n"
                sc.ids.checklist.text += "Stage 6.2 - Done\n\n"
                sc.ids.checklist.text += "Stage 6.3 - Current\n\n"
        else:
            #pass
            label.text += "Procedure Complete\n\n"
            sc.ids.checklist.text += "Stage 5.2 - Done\n\n"
            sc.ids.checklist.text += "Stage 5.6 - Done\n\n"
            sc.ids.checklist.text += "Stage 6.1 - Done\n\n"
            sc.ids.checklist.text += "Stage 6.2 - Done\n\n"
            sc.ids.checklist.text += "Stage 6.3 - Done\n\n"




        self.popup.dismiss()


    
    def noCallback(self,label,instance):
        self.popup.dismiss()
        self.missedValidations += 1
        label.text += "Validation Unsuccessful\n\n"
            
######################################
class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        app.sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            #MainWindow.current = self.email.text
            #self.reset()
            app.sm.current = "mainMenu"
            app.camBool = False
            sc = app.sm.get_screen("login")
            sc.ids.FL.remove_widget(app.camera)
            sc2 = app.sm.get_screen("procedureScreen")
            sc2.ids.g2.add_widget(app.camera)

        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        app.sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        app.sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()			
##################


if __name__ == "__main__":
    db = DataBase("users.txt")
    app=Project_Argus()
    app.run()
