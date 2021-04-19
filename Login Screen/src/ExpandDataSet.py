import cv2
import glob
import os
import numpy as np

path = 'Images/'

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

for file in glob.glob(path + '*.jpg'):
    img = cv2.imread(file)
    b,g,r = cv2.split(img)

    filename, file_extension = os.path.splitext(file)

    gauss = np.random.normal(0,1,img.size)
    gauss = gauss.reshape(img.shape[0],img.shape[1],img.shape[2]).astype('uint8')
    img_gauss = cv2.add(img,gauss)
    cv2.imwrite(filename + '_Gauss.jpg',img_gauss)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(filename + '_Gray.jpg',gray)

    imgdc = 0.5*img
    imgdcr = rotate_image(imgdc,270)
    cv2.imwrite(filename + '_Dark.jpg',imgdcr)

    imgbc = 1.5*img
    imgbc = rotate_image(imgbc,315)
    cv2.imwrite(filename + '_Bright.jpg',imgbc)

    img = cv2.merge((b,r,g))
    img = rotate_image(img,45)
    cv2.imwrite(filename + '_BRG.jpg',img)
    
    img = cv2.merge((r,g,b))
    img = rotate_image(img,90)
    cv2.imwrite(filename + '_RGB.jpg',img)
    
    img = cv2.merge((r,b,g))
    img = rotate_image(img,135)
    cv2.imwrite(filename + '_RBG.jpg',img)
    
    img = cv2.merge((g,r,b))
    img = rotate_image(img,180)
    cv2.imwrite(filename + '_GRB.jpg',img)
    
    img = cv2.merge((g,b,r))
    img = rotate_image(img,225)
    cv2.imwrite(filename + '_GBR.jpg',img)
