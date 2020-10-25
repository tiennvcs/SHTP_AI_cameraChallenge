import cv2
import numpy as np
import os
import argparse
import time
import datetime
from yolo_detect import detect_image
from google.colab.patches import cv2_imshow


def Check_Good(img):
  
  rawImage = img

  hsv = cv2.cvtColor(rawImage, cv2.COLOR_BGR2HS)

  hue ,saturation ,value = cv2.split(hsv)

  retval, thresholded = cv2.threshold(saturation, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

  medianFiltered = cv2.medianBlur(thresholded,5)

  kernel = np.ones((7,7),np.uint8)

  medianFiltered = cv2.morphologyEx(medianFiltered, cv2.MORPH_OPEN, kernel)
  medianFiltered = cv2.morphologyEx(medianFiltered, cv2.MORPH_CLOSE, kernel)

  cnts, hierarchy = cv2.findContours(medianFiltered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  # print("___Numbers contours: ", len(cnts) )
  s_len = 0
  for c in cnts:
    # print(c)
    s_len += len(c)
    #print(c)
  # compute the center of the contour
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])


    first = cv2.drawContours(rawImage, [c], -1, (0, 255, 0), 2)
    second =cv2.circle(rawImage, (cX, cY),1 , (255, 255, 255), -1)
  # print('sum point: ', s_len)
  
  # print('Objects Detected')
  # cv2_imshow(rawImage)
  result = check_number_contour(cnts,40,second.copy())
  return result

def check_number_contour(cnts,threshold,img):
  if len(cnts) >=2:
    return False
  y_max,y_min = np.max(cnts[0][:,0][:,1]),np.min(cnts[0][:,0][:,1])
  img =cv2.circle(img, (50, y_max),2 , (255, 0, 255), 2)
  img =cv2.circle(img, (50, y_min),2 , (255, 0, 255), 2)
  d = y_max - y_min
  #cv2.imshow(img)
  if d >= threshold:
    return True
  return False

def Show_Result(Text, image):

  image = cv2.putText(image, Text, (100, 100) , cv2.FONT_HERSHEY_SIMPLEX ,  
                    1,(255, 0, 0), 2, cv2.LINE_AA) 
  print(Text)

def main(args):
  start_time = datetime.datetime.now()
  # Đọc file
  Text = ""
  img = cv2.imread(args["path_image"],cv2.IMREAD_COLOR)

  # Detect cổ chai
  img_dec = detect_image(img)


  # Hậu xử lí
  result = Check_Good(img_dec)
  # Ghi ket qua

  if result == True:
    Text = Text + "Ok"
  else:
    Text = Text + "Not good"
  Text = Text + " " + str(start_time)

  # Show kết quả 
  # img_test = cv2.imread("E:\AI_Inspection\image_test\SNB-6004_20201014114132.jpeg",cv2.IMREAD_COLOR) 
  # Resize image
  scale_percent = 50

  #calculate the 50 percent of original dimensions
  width = int(img.shape[1] * scale_percent / 100)
  height = int(img.shape[0] * scale_percent / 100)

  # dsize
  dsize = (width, height)

# resize image
  img_result = cv2.resize(img, dsize)

  #Show_Result(Text,img)
  
  Show_Result(Text,img_result)
  # cv2.waitKey(0)
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process image')
  parser.add_argument('--path_image', type=str, required=True, help='The path of image need process')
  main(vars(parser.parse_args()))
