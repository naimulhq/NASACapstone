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

# Necessary Imports
import jetson.inference
import jetson.utils
import csv
import sys
import time
from datetime import datetime
import os
from instructionDatabase import instructionDatabase

# Ask user for names of parts and stages model. Only for testing purposes.
dirs = os.listdir('/home')
part_model_name = input("Enter part model name with extension: ")
stage_model_name = input("Enter stage model name with extension: ")
dirs = os.listdir('/home')
part_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/PartDetection/' + str(part_model_name)
stage_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/Stages/' + str(stage_model_name)


# Get instructionDatabase and modify instructions
# Create Database
instructionDB = instructionDatabase()
#instructionDB.deleteAllData() # Delete Instruction Info. Only run once.

# Get info from csv. Only run once. Comment out once .db is generated
with open(os.path.join(sys.path[0], "instructions.csv"),'r') as file:
    reader = csv.reader(file)
    data = list(reader)

# # Store information into instruction database
for i in data:
    instructionDB.insertDB(i[0],i[1])

# Get all contents of Database
endOfDB = False
instructions = []
while not endOfDB:
	endOfDB, instr = instructionDB.getInstruction()
	instructions.append(instr)
print(instructions)

# instructions has all the contents in the csv. instructions is the list of tuples where first element is instruction, second is stage.
# Make a dictionary where the key is the stage and the value will be a dictionary or list which holds the set of instructions
 
# Get parent directory. Necessary to load model correctly

# Open up labels file for part detection
f = open("labels_parts.txt","r")
labels = []
for i in f.readlines():
	labels.append(i.strip('\n'))
f.close()

# This net used with Part Detection.
# Change model directory depending on user. Stores labels in same directory as src

part_net = jetson.inference.detectNet(argv=['--model='+part_model_path,'--labels=./labels_parts.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8'])
stages_net = jetson.inference.detectNet(argv=['--model='+stage_model_path,'--labels=./labels_1.2+2.1.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8'])
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

# Add another net, camera, and display for Stage Detection
beginTime = time.time()
endTime = 0
currentInstr, stageCount = 0, 0

# Open up labels file for stage detection
f = open("labels_stages.txt","r")
labels_stages = []
for i in f.readlines():
	labels_stages.append(i.strip('\n'))
f.close()

while display.IsStreaming():
	# Keep Track of Time
	beginTime = time.time()
	img = camera.Capture()
	detections = part_net.Detect(img) # Holds all the valuable Information
	stages = stages_net.Detect(img)
	# if buttonPressed:	# user has pressed 'Stage Complete' button
	# 	if labels_stages[stages.ClassID] == instr[currentInstr][1]:
	#		stageCount += 1
	# 	else:
	#		stageCount = 0
	#		buttonPressed = False
	#	if stageCount == 48:
	#		currentInstr += 1
	#		buttonPressed = False
	#		# add timestamp of stage complete to datalog
	# If difference greater than log time desired in seconds, log the data. Currently, logging data every five seconds
	if(beginTime-endTime > 1):
		objects = []
		vertices = []
		for i in range(len(detections)):
			objects.append(labels[detections[i].ClassID])
			# Store box vertices in clockwise order
			bottomLeft = (detections[i].Left, detections[i].Bottom)
			bottomRight = (detections[i].Right, detections[i].Bottom)
			topLeft = (detections[i].Left, detections[i].Top)
			topRight = (detections[i].Right, detections[i].Top)
			vertices.append((topLeft,topRight,bottomRight,bottomLeft))
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		endTime = time.time()
	
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(part_net.GetNetworkFPS()))
