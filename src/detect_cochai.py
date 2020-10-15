import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import imutils
from config import ROI_info, H, W, boundaries
from bottle_cap import simple_process


# Bước 1: đọc ảnh
path = '../raw_data/DASANI/SNB-6004_20201014114137.jpeg'
if not os.path.exists(path):
	print("The invalid path")
	exit(0)

img = plt.imread(path)

roi_img = cv2.rectangle(img, ROI_info['p1'], ROI_info['p4'], color=(0, 255, 255), thickness=2)
cv2.imwrite('ROI.png', roi_img[ROI_info['p1'][1]:ROI_info['p3'][1], 0:W,:])

roi_img = cv2.imread('ROI.png')

# Bước 3: tìm ra mask của nắp chai và vòng cổ chai
#simple_process(img=roi_img, output='.', lower=50, upper=200)
for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(roi_img, lower, upper)
	output = cv2.bitwise_and(roi_img, roi_img, mask=mask)
	# show the images
	cv2.imshow("ROI image detect nap chai",  output)
	cv2.waitKey(0)

# Bước 4: Đo khoảng cách giữa nắp chai và vòng cổ chai
