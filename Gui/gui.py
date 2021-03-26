import os
os.system("sudo killall ibus-daemon")
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1214)
Config.set('graphics', 'height', 743)

import kivy
from kivy.app import App
from kivy.uix.label import Label
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
#from kivy.lang import Builder
#from kivy.uix.screenmanager import ScreenManager, Screen
#from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

#Using KV
class MyGrid(Widget):
	def pressed_validate(self):
		print("Validate")

	def pressed_forward(self):
		print("Forward")

	def pressed_previous(self):
		print("Previous")
	

class Project_Argus(App):
	def build(self):
		return MyGrid()



if __name__ == "__main__":
	Project_Argus().run()


