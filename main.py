"""

	Process an image and display result

"""

import argparse
import cv2
from detect.yolo_detect import detect_image 
from post_processing.post_processing import check_good


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
	print(result)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process image and display result.')
	parser.add_argument('--image_path', '-path', type=str, default='./test/test1.png',
	                    help='The path of image.')
	parser.add_argument('--threshold', type=int, default=40,
	                    help='The path of image.')
	args = vars(parser.parse_args())
	main(args)