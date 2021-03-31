import jetson.inference
import jetson.utils
import time

height = 720
width =1280

net=jetson.inference.imageNet('googlenet')
cam=jetson.utils.gstCamera(width,height,'/dev/video0')
disp=jetson.utils.glDisplay()
font=jetson.utils.cudaFont()
timeMark=time.time()
fpsFilter=0

while disp.IsOpen():
    frame,width,height = cam.CaptureRGBA()
    classID,condifent=net.Classify(frame,width,height)
    item=net.GetClassDesc(classID)
    dt = time.time() - timeMark
    fps = 1/dt
    fpsFilter = .95*fpsFilter + .05*fps
    timeMark=time.time()
    font.OverlayText(frame,width,height, str(round(fpsFilter,1))+' fps'+item, 5,5, font.Magenta,font.Blue)
    disp.RenderOnce(frame,width,height)