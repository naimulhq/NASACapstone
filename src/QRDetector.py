from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

vs = VideoStream(src="nvarguscamerasrc ! video/x-raw(memory:NVMM), " \
	"width=(int)1920, height=(int)1080,format=(string)NV12, " \
	"framerate=(fraction)20/1 ! nvvidconv flip-method=2 ! video/x-raw, " \
	"format=(string)BGRx ! videoconvert ! video/x-raw, " \
	"format=(string)BGR ! appsink").start()

time.sleep(2.0)

Green = (36,255,12)
Red = (0,0,255)
keywords = ['M2 Hex Nut', 'M3X30 Standoff']

while True:
	frame = vs.read()	
	frame = imutils.resize(frame, width=600, height=400)

	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame)

	for barcode in barcodes:
		barcodeData = barcode.data.decode("utf-8")
		if barcodeData in keywords:
			col = Green
		else:
			col = Red
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h),col, 2)
		text = "{}".format(barcodeData)
		cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,col, 2)

		# show the output frame
	cv2.imshow("Barcode Scanner", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

vs.stop()
cv2.destroyAllWindows()