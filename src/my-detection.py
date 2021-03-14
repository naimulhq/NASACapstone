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
part_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/PartDetection/All_Parts.onnx'
stage_model_path = '/home/'+ str(dirs[0]) + '/Capstone/models/Stages/All_Stages.onnx'


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
stages_net = jetson.inference.detectNet(argv=['--model='+stage_model_path,'--labels=./labels_stages.txt','--input_blob=input_0','--output-cvg=scores','--output-bbox=boxes','--threshold=.8'])
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

# Add another net, camera, and display for Stage Detection
beginTime = time.time()
procedureTime = time.time()
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
incorrectValidation = []
missedValidations = 0


while display.IsStreaming():
	if currentInstr >= len(instructions):	# end program if all instructions have been passed through
		break
	# Keep Track of Time
	beginTime = time.time()
	img = camera.Capture()
	detections = part_net.Detect(img) # Holds all the valuable Information
	stages = stages_net.Detect(img)
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
			missedValidations += 1
	#		buttonPressed = False
		if stageCount == 48:
			StageName.append(instructions[currentInstr][1])
			incorrectValidation.append(missedValidations)
			missedValidations = 0
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			StageTimeStamps.append(current_time)
			currentInstr += 1
			print(instructions[currentInstr][0], instructions[currentInstr][1])
			userInput = int(input("Skip how many stages? (0-7) "))
			currentInstr += userInput
			if userInput != 0:
				print(instructions[currentInstr][0], instructions[currentInstr][1])
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

	stages_file_writer.writerow(['Stage Completed', 'Time Completed', 'Missed Validations'])

	for i in range(len(StageName)):
		stages_file_writer.writerow([StageName[i],StageTimeStamps[i],incorrectValidation[i]])

with open('Parts.csv',mode='w') as parts_file:
	parts_file_writer = csv.writer(parts_file,delimiter=',')

	parts_file_writer.writerow(['Object Name', 'Top Left Coordinate', 'Top Right Coordinate', 'Bottom Right Coordinate', 'Bottom Left Coordinate', 'Time Stamped'])

	for i in range(len(objects)):
		parts_file_writer.writerow([objects[i], vertices[i][0],vertices[i][1],vertices[i][2],vertices[i][3], PartTimeStamps[i]])

print("Writing Complete")
