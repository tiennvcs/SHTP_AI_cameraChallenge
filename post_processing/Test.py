import cv2
# from google.colab.patches import cv2_imshow
import numpy as np
import os

import Post_processing
import time 

start  = time.time()
path = "E:\AI_Inspection\image_test\SNB-6004_20201014114217.jpeg"

img = cv2.imread(path,cv2.IMREAD_COLOR)
# cv2.imshow("Origin Image: ",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
result, cnts = Post_processing.Check_Good(img)

end = time.time()
print("Result: ", result)
print("Time post processing: ", end -start)