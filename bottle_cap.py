import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import imageio

path = "/home/thuyentd/2019-2020/AI_Camera_Inspection/Data/1/data1_182.jpg"
img = cv2.imread(path)

img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


# (thresh, blackAndWhiteImage) = cv2.threshold(img_grey, 127, 255, cv2.THRESH_BINARY)
# (thresh, blackAndWhiteImage_) = cv2.threshold(img_grey, 100, 240, cv2.THRESH_BINARY)
# (thresh, blackAndWhiteImage_2) = cv2.threshold(img_grey, 100, 200, cv2.THRESH_BINARY)

images = []
for upBound in range(200,255,20):
    for lowBound in range(100,140,10):
        plt.clf()
        (thresh, blackAndWhiteImage) = cv2.threshold(img_grey, upBound, lowBound, cv2.THRESH_BINARY)
        imgplot = plt.imshow(blackAndWhiteImage,cmap='Greys')
        plt.title('Image upbound {} lowerbound {}.png'.format(upBound,lowBound))
        plt.savefig('./plot/Image_upbound_{}_lowerbound_{}.png'.format(upBound,lowBound))
        img = cv2.imread('./plot/Image_upbound_{}_lowerbound_{}.png'.format(upBound,lowBound))
        images.append(img)

imageio.mimsave("/home/thuyentd/2019-2020/AI_Camera_Inspection/movie.gif", images,duration = 1)

# cv2.imwrite("test.jpg",blackAndWhiteImage)
# cv2.imwrite("test_.jpg",blackAndWhiteImage_)
# cv2.imwrite("test_2.jpg",blackAndWhiteImage_2)