from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

class RaspberryPiCam:

    def __init__(self):
        self.vs = VideoStream(src=RaspberryPiCam.gstreamer_pipeline()).start()
        self.width = 600
        self.height = 400
        time.sleep(2.0)

    def run_camera(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=self.width, height=self.height)
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
            
    def QRDetector(self,frame):
        # find the barcodes in the frame and decode each of the barcodes
        Green = (36,255,12)
        Red = (0,0,255)
        keywords = ['M2 Hex Nut', 'M3X30 Standoff']
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            print(barcode)
            barcodeData = barcode.data.decode("utf-8")
            if barcodeData in keywords:
                col = Green
            else:
                col = Red
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h),col, 2)
            text = "{}".format(barcodeData)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,col, 2)
        return frame

    @staticmethod
    def gstreamer_pipeline(capture_width=1920, capture_height=1080, framerate=20, flip_method=2):
        return (
            "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
            % (capture_width,capture_height,framerate,flip_method)
        )
