"""

	Process an image and display result

"""

import argparse
import cv2
from detect.yolo_detect import detect_image 
from post_processing.post_processing import check_good
import numpy as np


def show_result(image: np.ndarray, isGood: bool):
	
	cv2.imshow('Predict image', image)
	if isGood:
		text = "OKE"
	else:
		text = "NOT GOOD"

	cv2.putText(image, text, org=(100, 100),fontFace=1, fontScale=1,color=(255, 0, 0), thickness=2)

	cv2.imshow('Result', image)

	cv2.waitKey(0)
	
	return 

def main(args):
	
	# Load image into program
	try:
		image = cv2.imread(args['image_path'])
	except:
		print("INVALID PATH !")
		exit(0)

	# Runing detection stage
	roi_image = detect_image(image)

	# Running post processing
	result, contours = check_good(roi_image, args['threshold'])

	# Display result 
	show_result(image=image, isGood=result)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process image and display result.')
	parser.add_argument('--image_path', '-path', type=str, default='./test/test1.png',
	                    help='The path of image.')
	parser.add_argument('--threshold', type=int, default=40,
	                    help='The path of image.')
	args = vars(parser.parse_args())
	main(args)