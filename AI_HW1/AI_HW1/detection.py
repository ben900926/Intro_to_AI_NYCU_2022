import os
import cv2
import adaboost
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    """
    explanation:
    open the txt file, get the filename of image and the coordinates of face images
    then read the image, crop out the face image, then convert it to 19X19 grayscale
    use the strong classifier to classify the modified face image,
    draw the rectangle according to classification result and show the result
    """
    # read detectData.txt
    with open(dataPath) as f:
      while True:
        # for each image
        line = f.readline()
        if not line: # reach EOF
          break
        line_lst = line.split(' ')
        imName = line_lst[0] 
        # get folder
        i = 0
        for w in range(len(dataPath)):
          if dataPath[w] == '/':
            i = w
        dataPath = dataPath[0:i+1]
        #read image
        image = cv2.imread(dataPath+imName)
        # read coordinates for face images
        line_num =int( line_lst[1][0:-1] )#remove last char
        for i in range(line_num):
          line = f.readline()
          if not line:
            break
          coors = line.split(' ') #coordinates
          # coordinates for face images
          x = int(coors[0])  
          y = int(coors[1])
          w = int(coors[2])
          h = int(coors[3][0:-1])
          # resize and change to grayscale
          face_image = image.copy()[y:y+h,x:x+w]
          face_image = cv2.cvtColor(face_image,cv2.COLOR_BGR2GRAY) # change to gray
          face_image = cv2.resize(face_image,(19,19)) # resize to 19X19
          # classify the face image
          isFace = adaboost.Adaboost.classify(clf,face_image)
          # if it's face draw a green rectangle,else draw a red one
          if isFace: 
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
          else : 
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),3)
        #display result
        cv2.imshow('result',image)
        cv2.waitKey()
        cv2.destroyAllWindows()
    # End your code (Part 4)
