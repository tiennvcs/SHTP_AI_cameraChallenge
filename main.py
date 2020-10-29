"""

	Process an image and display result

"""

import argparse
import cv2
from detect.yolo_detect import detect_image 
from post_processing.post_processing import check_good
import numpy as np
from config import SIZE_DISPLAY

def show_result(image: np.ndarray, isGood: bool, show=True):
	
	try:
		image = cv2.resize(image, dsize=SIZE_DISPLAY, interpolation=cv2.INTER_AREA)
	except:
		print("CAN'T RESIZE !")
		exit(0)

	if isGood:
		text = "OKE"
	else:
		text = "NOT GOOD"

	cv2.putText(image, text, org=(100, 100),fontFace=1, fontScale=1,color=(255, 0, 0), thickness=2)

	if show:
		cv2.imshow('Result', image)
		cv2.waitKey(0)
	
	return image

def main(args):
	
	# Load image into program
	try:
		image = cv2.imread(args['image_path'])
	except:
		print("INVALID PATH !")
		exit(0)

	copied_image = image.copy()
	# Runing detection stage
	roi_image = detect_image(copied_image)

	# Running post processing
	result, contours = check_good(roi_image, args['threshold'], show=False)

	# Display result 
	show_result(image=image, isGood=result, show=True)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process image and display result.')
	parser.add_argument('--image_path', '-path', type=str, default='./test/test1.png',
	                    help='The path of image.')
	parser.add_argument('--threshold', type=int, default=40,
	                    help='The path of image.')
	args = vars(parser.parse_args())
	main(args)