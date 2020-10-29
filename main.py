"""

	Process an image and display result

"""

import argparse
import cv2
from detect.tensorflow-yolov4-tflite import preprocess_image, model_output 
from post_processing. import check_good


def main(args):
	
	# Load image into program
	try:
		image = cv2.imread(args['path'])
		img_datas_stack, img = preprocess_image(img=image)
	except:
		print("INVALID PATHT !")
		exit(0)

	cv2.imshow('The origin image', image)
	cv2.waitKey(0)


	# Create model 
	model = model(img_datas_stack)

	# Runing detection stage
	detected_image = model_output(img)

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
