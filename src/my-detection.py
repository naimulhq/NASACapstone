#!/usr/bin/python3
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import jetson.inference
import jetson.utils
import time
from datetime import datetime
import os
# Might need to change paths for --model and --labels.
# If no boxes appear, lower threshold.

# Get parent directory. Necessary to load model correctly


# Open up labels file for part detection
f = open("labels.txt","r")
labels = []
for i in f.readlines():
	labels.append(i.strip('\n'))
f.close()

# This net used with Part Detection.
# Change model directory depending on user. Stores labels in same directory as src
net = jetson.inference.detectNet(argv=['--model=/home/naimulhq/Capstone/models/PartDetection/ssd-mobilenet-2.03.onnx','--labels=./labels.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8'])
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

# Add another net, camera, and display for Stage Detection
beginTime = time.time()
endTime = 0

while display.IsStreaming():
	# Keep Track of Time
	beginTime = time.time()
	img = camera.Capture()
	detections = net.Detect(img) # Holds all the valuable Information
	
	# If difference greater than log time desired in seconds, log the data. Currently, logging data every five seconds
	if(beginTime-endTime > 1):
		objects = []
		for i in range(len(detections)):
			objects.append(labels[detections[i].ClassID])
		print(objects)
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		print(current_time)
		endTime = time.time()
		
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
