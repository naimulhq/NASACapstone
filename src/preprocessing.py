# Preprocess image data prior to training model
import os
import numpy as np
from sklearn.model_selection import train_test_split

def preprocessData():
    
    images = []
    annotations = []

  
    for _,_,filenames in os.walk("C:\\Users\\18186\\Downloads\\Image Dataset\\Testing"):
        for f in filenames:
            if(f.find('.jpg') == -1):
                annotations.append(f)
            else:
                images.append(f)

   
    
    trainImages, testImages, trainAnnotations, testAnnotations = train_test_split(images,annotations,test_size=0.20,random_state=10)

    path1 = "C:\\Users\\18186\\Downloads\\Image Dataset\\"+"train\\annotations\\"
    path2 = "C:\\Users\\18186\\Downloads\\Image Dataset\\"+"train\\images\\"
    path3 = "C:\\Users\\18186\\Downloads\\Image Dataset\\"+"validation\\annotations\\"
    path4 = "C:\\Users\\18186\\Downloads\\Image Dataset\\"+"validation\\images\\"

    os.makedirs(path1)
    os.makedirs(path2)
    os.makedirs(path3)
    os.makedirs(path4)

    ##### BE CAREFUL WHEN MOVING. MAKE SURE TO MAKE ANOTHER COPY OF EACH FOLDER PRIOR TO MOVING

    for i in trainImages:
        src = "C:\\Users\\18186\\Downloads\\Image Dataset\\Testing\\" + i
        dest = path2 + i
        os.rename(src,dest)

    for i in testImages:
        src = "C:\\Users\\18186\\Downloads\\Image Dataset\\Testing\\" + i
        dest = path4 + i
        os.rename(src,dest)

    for i in trainAnnotations:
        src = "C:\\Users\\18186\\Downloads\\Image Dataset\\Testing\\" + i
        dest = path1 + i
        os.rename(src,dest)

    for i in testAnnotations:
        src = "C:\\Users\\18186\\Downloads\\Image Dataset\\Testing\\" + i
        dest = path3 + i
        os.rename(src,dest)

