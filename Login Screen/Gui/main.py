# main.py
import os
os.system("sudo killall ibus-daemon")
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1214)	# DON'T CHANGE THIS
Config.set('graphics', 'height', 743)	
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase

from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.camera import Camera
import cv2
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
import jetson.utils

import face_recognition
import pickle
import time

import threading


class KivyCameraLogin(Image):
   
    def __init__(self, **kwargs):
        super(KivyCameraLogin, self).__init__(**kwargs)
        self.font=cv2.FONT_HERSHEY_SIMPLEX
        self.Encodings=[]
        self.Names=[]
        self.fpsReport=0
        self.scaleFactor=.25
        self.timestamp = time.time()
        self.counter = 0
        with open('/home/edwin/FR/train.pkl','rb') as f:
            self.Names=pickle.load(f)
            self.Encodings=pickle.load(f)
        self.camera = jetson.utils.videoSource("/dev/video0")# '/dev/video0'for Edwin '/dev/video1' for Rishit
        #self.camera=cv2.VideoCapture('/dev/video0')
        #cv2.namedWindow("Picture")
        #self.display = jetson.utils.videoOutput() # 'my_video.mp4' for file
        self.clock = Clock.schedule_interval(self.update, 1.0 / 20)
        self.clock2 = None

        self.timeout = 0

    def update(self, dt):
        self.img = self.camera.Capture()

        #_,self.img = self.camera.read()
        self.img = jetson.utils.cudaToNumpy(self.img)
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
            if name == "Unknown Person":
                self.counter+=1
                if self.counter>30:
                    self.counter=0
                    MainWindow.current = "edwin@gmail.com"
                    sm.current = "main"
                    #self.camera.release()
                    #cv2.destroyAllWindows() 

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
        image_texture.blit_buffer(buf,colorfmt='rgb',bufferfmt='ubyte')
        self.texture = image_texture
        cv2.destroyAllWindows()

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
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

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





kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

class MyMainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()
