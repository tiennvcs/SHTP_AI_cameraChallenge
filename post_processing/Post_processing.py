# Usage
"""
  python post_processing.py --image_path ./test/NOTGOOD_detected_test.jpeg --show 0

"""
import cv2
import numpy as np
import argparse
import time


def check_number_contour(cnts:list, threshold: int):

  if len(cnts) >=2 or len(cnts) == 0:
    return False
  y_max, y_min = np.max(cnts[0][:,0][:,1]), np.min(cnts[0][:,0][:,1])
  distance = y_max - y_min
  if distance >= threshold:
    return True
  return False


def show_result(image: np.ndarray, isGood: bool, show=True):
	try:
		image = cv2.resize(image, dsize=(800, 600), interpolation=cv2.INTER_AREA)
	except:
		print("CAN'T RESIZE !")
		exit(0)

	if isGood:
		text = "OKE"
	else:
		text = "NOT GOOD"
  
	if show:
		cv2.putText(image, text, org=(100, 100),fontFace=1, fontScale=2,color=(255, 0, 0), thickness=2)
		cv2.imshow('Result', image)
		cv2.waitKey(0)
	
	return image


def check_good(rawImage, threshold=40, show=True):

  """
  This function allow you to check whether bottle cap is close or open.  

  + Input: Image with region contain bottle neck 
  + Ouput: True if bottle cap is closed,
        False otherwise 
  """
  # Convert BGR to HSV
  hsv = cv2.cvtColor(rawImage, cv2.COLOR_BGR2HSV)

  hue, saturation, value = cv2.split(hsv)

  retval, thresholded = cv2.threshold(saturation, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
  
  medianFiltered = cv2.medianBlur(thresholded,5)

  kernel = np.ones((7,7),np.uint8)

  # Open annd closing 
  medianFiltered = cv2.morphologyEx(medianFiltered, cv2.MORPH_OPEN, kernel)
  medianFiltered = cv2.morphologyEx(medianFiltered, cv2.MORPH_CLOSE, kernel)

  if show:
    cv2.imshow('meadian filtered image', medianFiltered)
    cv2.waitKey(0)

  # Take contours
  contours, _= cv2.findContours(medianFiltered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  #if len(contours) == 1:
  result = check_number_contour(contours, threshold)
  
  return result, contours
  

def main(args):
  
  # Load image into program
  try:
    img = cv2.imread(args['image_path'])
    if args['show']:
      cv2.imshow('The croped image', img)
      cv2.waitKey(0)
  except:
    print("The invalid path!")
    exit(0)

  # Post process stage
  isGood, contours = check_good(rawImage=img, threshold=args['threshold'], show=args['show'])

  # Show result
  if isGood:
    print("OKE")
  else:
    print("NOT GOOD")

  cv2.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Process a croped image and produce GOOD or NOT GOOD result.')
  parser.add_argument('--image_path', '-path', required=True, 
                      type=str, help='the path of croped image.')
  parser.add_argument('--threshold', default=40, 
                      type=int, help='the threshold value.')
  parser.add_argument('--show', default=0, choices=[0, 1],
                      type=int, help='Show visualizatoin result.')
  args = vars(parser.parse_args())

  start_time = time.time()
  main(args)
  print("The execution time of post-processing is {}s".format(time.time()-start_time))