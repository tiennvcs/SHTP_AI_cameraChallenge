import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import imageio
import os
import numpy as np
import argparse


def process_image(img: np.ndarray, output:str, lower, upper):


	img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	images = []

	for upBound in range(upper,255,20):

	    for lowBound in range(lower,140,10):

	        plt.clf()
	        
	        (thresh, blackAndWhiteImage) = cv2.threshold(img_grey, upBound, lowBound, cv2.THRESH_BINARY)
	        
	        imgplot = plt.imshow(blackAndWhiteImage, cmap='Greys')
	        
	        plt.title('Image upbound {} lowerbound {}.png'.format(upBound,lowBound))
	       	        
	        file_save = os.path.join(output, 'Image_upbound_{}_lowerbound_{}.png'.format(upBound, lowBound))
	       
	        plt.savefig(file_save)

	        img = cv2.imread(file_save)

	        images.append(img)

	return images



def simple_process(img, output, lower, upper):
	img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	
	plt.clf()
	
	(thresh, blackAndWhiteImage) = cv2.threshold(img_grey, upper, lower, cv2.THRESH_BINARY)

	imgplot = plt.imshow(blackAndWhiteImage, cmap='Greys')


	plt.title('Image upbound {} lowerbound {}.png'.format(upper,lower))
	        
	file_save = os.path.join(output, 'Image_upbound_{}_lowerbound_{}.png'.format(upper, lower))

	plt.savefig(file_save)


def main(args):

	# Check the path file
	if not os.path.exists(args['path_image']):
		print("The invalid path")
		exit(0)
	
	# Read image by path
	img = cv2.imread(args['path_image'])
	
	# Create output directory
	output_directory = os.path.join("../output", os.path.split(args['path_image'])[1].split(".")[0])
	if not os.path.exists(output_directory):
		os.mkdir(output_directory)


	images = simple_process(img, output=output_directory, lower=args['lower_bound'], upper=args['upper_bound'])


	# Create gif from images
	# imageio.mimsave(os.path.join(output_directory, 'animation.gif'), images, duration=1)



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Process image')
	parser.add_argument('--path_image', type=str, required=True, help='The path of image need process')
	parser.add_argument('--lower_bound', '-lower', type=int, required=True, help='The lower bound')
	parser.add_argument('--upper_bound', '-upper', type=int, required=True, help='The upper bound')

	main(vars(parser.parse_args()))