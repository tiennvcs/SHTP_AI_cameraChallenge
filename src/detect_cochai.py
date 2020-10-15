import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import imutils
from config import *
from bottle_cap import simple_process


# Bước 1: đọc ảnh
path = '../raw_data/AUQA/0001.jpeg'
if not os.path.exists(path):
	print("The invalid path")
	exit(0)

img = plt.imread(path, 0)

roi_img = cv2.rectangle(img, ROI_info['p1'], ROI_info['p4'], color=(0, 255, 255), thickness=2)
cv2.imwrite('ROI.png', roi_img[ROI_info['p1'][1]:ROI_info['p3'][1], 0:W,:])

roi_img = cv2.imread('ROI.png')

# Bước 3: tìm ra mask của nắp chai và vòng cổ chai
#simple_process(img=roi_img, output='.', lower=50, upper=200)
(lower, upper) = boundaries[-1]
#for (lower, upper) in boundaries:
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


# Bước 4: Template matching to find masks
path_template = '../template/AUQA_template.jpeg'
if not os.path.exists(path_template):
	print("The invalid template image path")
	exit(0)

# Read template image	
template = cv2.imread(path_template, 0)
cv2.imshow('Template image', template)
cv2.waitKey(0)

w, h = template.shape[0:2]

for meth in METHODS:

    img = output.copy()

    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img,top_left, bottom_right, 255, 2)
    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()

# Bước 4: Đo khoảng cách giữa nắp chai và vòng cổ chai
