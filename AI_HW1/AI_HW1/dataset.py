import os
import cv2
from cv2 import IMREAD_GRAYSCALE
 

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    """
    explanation:
    read all the pmg file in the face and non-face folder with os.listdir and cv2.imread respectively,
    then append the tuples including the numpy array and label of each data, to a list
    finally return the list
    """
    dataset = []        
    #read all images in folder
    #face
    face_path = dataPath+"/face"
    for filename in os.listdir(face_path):
        img = cv2.imread(os.path.join(face_path,filename),IMREAD_GRAYSCALE)
        if img is not None:
           dataset.append( tuple((img,1)) )
    #non-face
    nonface_path = dataPath+"/non-face"
    for filename in os.listdir(nonface_path):
        img = cv2.imread(os.path.join(nonface_path,filename),IMREAD_GRAYSCALE)
        if img is not None:
            dataset.append( tuple((img,0)) )
    # End your code (Part 1)
    return dataset

