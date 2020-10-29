"""

	Process an image and display result

"""

import argparse
import cv2
from detect.yolo_detect import detect_image 
from post_processing.post_processing import check_good, show_result
import numpy as np
from config import SIZE_DISPLAY
import os



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

	# Save image
	if args['save']:
		saving_path = os.path.join('output/', os.path.split(args['image_path'])[1])
		print(saving_path)
		input()



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process image and display result.')
	parser.add_argument('--image_path', '-path', type=str, default='./test/test1.png',
	                    help='The path of image.')
	parser.add_argument('--threshold', type=int, default=40,
	                    help='The path of image.')
	parser.add_argument('--save', type=int, choices=[0, 1], help='Save image or not')
	args = vars(parser.parse_args())
	main(args)