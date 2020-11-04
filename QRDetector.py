# QR Detector which uses OpenCV to capture live feed and pyzbar to detect QR Codes
import cv2
from pyzbar.pyzbar import decode

# Create a video capture object. Necessary to capture video from webcam. 0 = front camera. 1 for back camera
cap = cv2.VideoCapture(1)

Green = (36,255,12)
Red = (0,0,255)

keywords = ['M2 Hex Nut', 'M3X30 Standoff']

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Get all QR Codes in frame
    QRCodes = decode(frame)
    
    # If length is not 0, put a bounding box on each code
    if(len(QRCodes) != 0):
        # Iterate through each Decoded Object in QRCodes List
        for i in range(len(QRCodes)):
            x,y,w,h = QRCodes[i].rect.left, QRCodes[i].rect.top, QRCodes[i].rect.width, QRCodes[i].rect.height # Get coordinates
            string = (QRCodes[i].data).decode('ASCII') # Get Text Data

            if string in keywords:
                col = Green
            else:
                col = Red

            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),col, 1) # Create a rectangle on the frame
            cv2.putText(frame, string, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,col, 2) # Add text with decoded QR Code text.

        cv2.imshow('frame',frame) # Output image
    else:
        cv2.imshow('frame',frame) # Output image.

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


