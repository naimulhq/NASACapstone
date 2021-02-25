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

# Ask user for names of parts and stages model. Only for testing purposes.
dirs = os.listdir('/home')
#part_model_name = input("Enter part model name with extension: ")
#stage_model_name = input("Enter stage model name with extension: ")
dirs = os.listdir('/home')
#part_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/PartDetection/' + str(part_model_name)
#stage_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/Stages/' + str(stage_model_name)
part_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/PartDetection/ssd-mobilenet-2.03.onnx'
stage_model_path = list()
stage_model_path.append('/home/'+ str(dirs[0]) + '/Capstone/models/Stages/Stage_1.2.onnx')
stage_model_path.append('/home/'+ str(dirs[0]) + '/Capstone/models/Stages/Stage_2.1.onnx')
stage_model_path.append('/home/'+ str(dirs[0]) + '/Capstone/models/Stages/Stage_2.2.onnx')
stage_model_path.append('/home/'+ str(dirs[0]) + '/Capstone/models/Stages/Stage_3.2.onnx')
stage_model_path.append('/home/'+ str(dirs[0]) + '/Capstone/models/Stages/Stage_4.1.onnx')
stage_model_path.append('/home/'+ str(dirs[0]) + '/Capstone/models/Stages/Stage_4.3.onnx')
stage_model_path.append('/home/'+ str(dirs[0]) + '/Capstone/models/Stages/Stage_5.1.onnx')
stage_model_path.append('/home/'+ str(dirs[0]) + '/Capstone/models/Stages/Stage_5.2.onnx')
print("edWhine")


# Get info from csv. Only run once. Comment out once .db is generated
with open(os.path.join(sys.path[0], "instructions.csv"),'r') as file:
    reader = csv.reader(file)
    instructions = list(reader)

print(instructions)

# Open up labels file for part detection
f = open("labels_parts.txt","r")
labels = []
for i in f.readlines():
	labels.append(i.strip('\n'))
f.close()

# This net used with Part Detection.
# Change model directory depending on user. Stores labels in same directory as src

part_net = jetson.inference.detectNet(argv=['--model='+part_model_path,'--labels=./labels_parts.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8'])
stages_net = []
stages_net.append(jetson.inference.detectNet(argv=['--model='+stage_model_path[0],'--labels=./labels_1.2.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8']))
stages_net.append(jetson.inference.detectNet(argv=['--model='+stage_model_path[1],'--labels=./labels_2.1.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8']))
stages_net.append(jetson.inference.detectNet(argv=['--model='+stage_model_path[2],'--labels=./labels_2.2.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8']))
stages_net.append(jetson.inference.detectNet(argv=['--model='+stage_model_path[3],'--labels=./labels_3.2.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8']))
stages_net.append(jetson.inference.detectNet(argv=['--model='+stage_model_path[4],'--labels=./labels_4.1.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8']))
stages_net.append(jetson.inference.detectNet(argv=['--model='+stage_model_path[5],'--labels=./labels_4.3.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8']))
stages_net.append(jetson.inference.detectNet(argv=['--model='+stage_model_path[6],'--labels=./labels_5.1.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8']))
stages_net.append(jetson.inference.detectNet(argv=['--model='+stage_model_path[7],'--labels=./labels_5.2.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8']))
print("edWINE")
#exit()
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
#camera = jetson.utils.videoSource("/dev/video0")      # For EDWHINE YESSSS DATS MEE'/dev/video0' for V4L2
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

buttonPressed = True

print(instructions[0][0], instructions[0][1])

# Lists will hold information for duration of procedure
objects = []
vertices = []
PartTimeStamps = []
StageName = []
StageTimeStamps = []

while display.IsStreaming():
	# Keep Track of Time
	beginTime = time.time()
	img = camera.Capture()
	detections = part_net.Detect(img) # Holds all the valuable Information
	stages = stages_net[currentInstr].Detect(img)
	#if len(stages) != 0:
	#	print(instructions[currentInstr][0])
	#	print(instructions[currentInstr][1])
	if buttonPressed and len(stages) != 0:	# user has pressed 'Stage Complete' button
		if labels_stages[stages[0].ClassID] == instructions[currentInstr][1]:
			#print("stageCount increased")
			stageCount += 1
		else:
			#print("stageCount = 0")
			stageCount = 0
	#		buttonPressed = False
		if stageCount == 48:
			StageName.append(instructions[currentInstr][1])
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			StageTimeStamps.append(current_time)
			currentInstr += 1
			print(instructions[currentInstr][0], instructions[currentInstr][1])
			#userInput = input("Next stage?")
			#if userInput == "y":
			#	currentInstr += 1
			#	print(instructions[currentInstr][0], instructions[currentInstr][1])
			#buttonPressed = False
	#		# add timestamp of stage complete to datalog
	# If difference greater than log time desired in seconds, log the data. Currently, logging data every five seconds
	if(beginTime-endTime > 1):
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
		PartTimeStamps.append(current_time)
		endTime = time.time()
	
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(part_net.GetNetworkFPS()))


# Create two csv files: one will hold information about parts and other will hold information about procedure
print("Success: Procedure Complete!")

print("Writing Information into CSV Files ...")

with open('Stages.csv',mode='w') as stages_file:
	stages_file_writer = csv.writer(stages_file,delimiter=',')

	stages_file_writer.writerow(['Stage Completed', 'Time Completed'])

	for i in range(len(StageName)):
		stages_file_writer.writerow([StageName[i],StageTimeStamps[i]])

with open('Parts.csv',mode='w') as parts_file:
	parts_file_writer = csv.writer(parts_file,delimiter=',')

	parts_file_writer.writerow(['Object Name', 'Top Left Coordinate', 'Top Right Coordinate', 'Bottom Right Coordinate', 'Bottom Left Coordinate', 'Time Stamped'])

	for i in range(len(objects)):
		parts_file_writer.writerow([objects[i], vertices[i][0],vertices[i][1],vertices[i][2],vertices[i][3], PartTimeStamps[i]])

print("Writing Complete")
