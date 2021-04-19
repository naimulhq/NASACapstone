from xml.dom import minidom
import os
import time

## Enter directory where all xml files are in.

directory = "/home/oles/Capstone/TrainingTools/ssd/Annotations/";

for _,_,files in os.walk(directory):
    pass

incorrectFiles = []
labels = ['Motor','Top Plate', 'Board', 'Bottom Plate', 'F2 Bracket', 'F3 Bracket', 'M3X15 Standoff', 'M3X30 Standoff', 'Mounting Plate', 'Stage 1.2', 'Stage 2.1', 'Stage 2.2', 'Stage 3.2', 'Stage 4.1', 'Stage 4.3', 'Stage 5.1', 'Stage 5.2', 'Stage 5.6 (No FTDI)']

for f in files:
    print(f)
    my_xml = minidom.parse(directory+f)
    objects = my_xml.getElementsByTagName('object')
    for obj in objects:
        name = obj.getElementsByTagName('name')
        if name[0].firstChild.data not in labels:
            custom_str = "\nIncorrect File: " + str(f)  + "--------- Supposed Label: " + str(name[0].firstChild.data)
            incorrectFiles.append(custom_str)
            
f = open('IncorrectFiles.txt','w')
f.writelines(incorrectFiles)
f.close()

