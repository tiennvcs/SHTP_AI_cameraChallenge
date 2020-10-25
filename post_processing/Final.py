import cv2
import numpy as np

def Check_Number_Contour(cnts,threshold):
  '''
  + Input: list contours
  '''
  if len(cnts) >=2:
    return False
  y_max,y_min = np.max(cnts[0][:,0][:,1]),np.min(cnts[0][:,0][:,1])
  d = y_max - y_min
  if d >= threshold:
    return True
  return False

def Check_Good(rawImage):

  """
  This function allow you to check whether bottle cap is close or open.  

  + Input: Image with region contain bottle neck 
  + Ouput: True if bottle cap is closed,
        False otherwise 
  """
  # Convert BGR to HSV
  hsv = cv2.cvtColor(rawImage, cv2.COLOR_BGR2HSV)


  hue ,saturation ,value = cv2.split(hsv)

  retval, thresholded = cv2.threshold(saturation, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
 
  medianFiltered = cv2.medianBlur(thresholded,5)

  kernel = np.one
  s((7,7),np.uint8)

  # Open annd closing 
  medianFiltered = cv2.morphologyEx(medianFiltered, cv2.MORPH_OPEN, kernel)
  medianFiltered = cv2.morphologyEx(medianFiltered, cv2.MORPH_CLOSE, kernel)

  # Take contours
  cnts, _= cv2.findContours(medianFiltered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  
  result = Check_Number_Contour(cnts,40)
  return result, cnts




