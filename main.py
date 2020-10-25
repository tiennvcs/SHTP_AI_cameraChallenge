"""

	Process an image and display result

"""

import argparse
import cv2
from detect.yolo.yolo_detect import detect_image
from post_processing. import check_good


def main(args):
	
	# Load image into program
	try:
		image = cv2.imread(args['path'])
	except:
		print("INVALID PATHT !")
		exit(0)

	cv2.imshow('The origin image', image)
	cv2.waitKey(0)

	# Runing detection stage
	detected_image = detect_image(image)

	# Running post processing
	result, contours = check_good(detected_image)

	# Display result 
	print(result)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process image and display result.')
	parser.add_argument('--image_path', '-path', type=str, default='./test/test1.png'
	                    help='The path of image.')
	parser.add_argument('--model_weights', '-weights', type=str, default='./detect/yolo/ABC_weights.pkt',
	                    help='The path of image.')
	args = parser.parse_args()
