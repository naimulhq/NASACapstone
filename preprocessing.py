# Preprocess image data prior to training model
import os
from sklearn.model_selection import train_test_split

def preprocessData():
    folderNames = ["Bottom Plate","Motor","Mounting Plate"]

    images = []
    annotations = []

    for label in folderNames:
        for _,_,filenames in os.walk("C:\\Users\\18186\\Downloads\\Image Dataset\\" + str(label)):
            images.append(filenames)
    
    for label in folderNames:
        for _,_,filenames in os.walk("C:\\Users\\18186\\Downloads\\Image Dataset\\" + str(label) + " Annotations"):
            annotations.append(filenames)

    
    
preprocessData()
