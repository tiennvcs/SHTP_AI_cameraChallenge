from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from time import sleep
from threading import Thread
import random
from detect.yolo_detect import detect_image 
from post_processing.post_processing import check_good, show_result


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

n_oke = 0
n_not_oke = 0
n = 0


def conti():
    global Cont
    Cont = 1


def gia_lap():
    a = random.randrange(100)
    if a == 2:
        return 1
    return 0

def update_frame():
    global canvas, photo, Cont
    # Gia lap sensor 
    is_show = gia_lap()
    
    print("im_show {} Cont {}".format(is_show,Cont))
    #
    if Cont == 1:
        if is_show == 1:
            # Doc tu camera
            try:
                img = cv2.imread("./test_images/009.jpeg")
                # cv2.imshow('Origin image', img)
                # cv2.waitKey(0)
                copied_image = img.copy()
            except: 
                print("PATH IS INVALID")
                exit(0)
            
            roi_image = detect_image(copied_image)
            # cv2.imshow('ROI', roi_image)
            # cv2.waitKey(0)

            # Running post processing
            result, contours = check_good(roi_image, show=True)

            # Display result 
            
            result_image = show_result(image=img, isGood=result, show=True)
            # cv2.imshow('Result', result_image)
            # cv2.waitKey(0)

            # Ressize
            img = cv2.resize(img,(WINDOW_WIDTH,WINDOW_HEIGHT), interpolation=cv2.INTER_AREA)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(result_image))
            status.configure(text = "Processing",font = ("Arial",20 ))
            Cont = 0

        else:
            photo = None
            status.configure(text = "Waiting",font = ("Arial",20))
            print("Waiting")
        
        
    # Show
    canvas.create_image(0,0, image = photo, anchor=tkinter.NW)
    window.after(15, update_frame)


window = Tk()
window.title("SHTP Camera Inspection")

video = cv2.VideoCapture(0)
canvas = Canvas(window, width = WINDOW_WIDTH, height= WINDOW_HEIGHT , bg= "white")
canvas.pack()

Cont = 1
button = Button(window,text = "Continue", command=conti)
button.pack()


status = Label(window,text = "Waiting",font = ("Arial",20))
status.pack()
status.place(x=300,y=300)
photo = None
update_frame()

window.mainloop()