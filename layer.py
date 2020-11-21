#use python3 layer.py to run app
#project argus

import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import tkinter as tk
  
class App:
     def __init__(self, window, window_title, video_source=0):
         self.window = window
         self.window.title(window_title)
         self.video_source = video_source
 
        
         self.vid = MyVideoCapture(self.video_source)
         
    
         # Create a canvas that can fit the above video source size
         self.canvas = tkinter.Canvas(window, width = 2*self.vid.width, height = self.vid.height)
         self.canvas = tkinter.Canvas(window, width = 2*self.vid.width, height = self.vid.height)
         self.canvas.pack()
        
         root = window
         T = tk.Text(root, height=2, width=60)
         T.pack()
         T.insert(tk.END, "The procedure can be displayed in this format when the button is pressed ---currently button just takes a screenshot\n")
         #tk.mainloop()   
 
         self.btn_snapshot=tkinter.Button(window, text="Capture Step", width=50, command=self.snapshot)
         self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
         self.btn_snapshot=tkinter.Button(window, text="Procedure Script", width=50, command=self.snapshot)
         self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
 
         # After it is called once, the update method will be automatically called every delay milliseconds
         self.delay = 15
         self.update()
 
         self.window.mainloop()
 
     def snapshot(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()
 
         if ret:
             cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
 
     def update(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()
 
         if ret:
             self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
             self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
         self.window.after(self.delay, self.update)
 
 
class MyVideoCapture:
     def __init__(self, video_source=0):
         # this line opens the computer video source which will be changed once we have the cameras
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (ret, None)
 
     # Releases the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()


App(tkinter.Tk(), "Project Argus: The Future of Procedural Tracking")