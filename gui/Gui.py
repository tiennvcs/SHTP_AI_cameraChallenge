from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from time import sleep
from threading import Thread
import random
import snap7
from datetime import datetime
from detect.yolo_detect import detect_image 
from post_processing.post_processing import check_good, show_result


# CONSTANT 
DB_NUMBER = 100
START_ADDRESS = 0
SIZE = 259

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
        return True
    return False

def put_text(img,time):

    global n_oke, n_not_oke, n
    font = cv2.FONT_HERSHEY_SIMPLEX   
    # org 
    org = (200, 500) 

    # fontScale 
    fontScale = 1

    # Blue color in BGR 
    color = (0, 0, 255) 

    # Line thickness of 2 px 
    thickness = 2

    # Using cv2.putText() method 
    img = cv2.putText(img, time, org, font,  
                    fontScale, color, thickness, cv2.LINE_AA) 
    # Infor
    Info = "SL: " + str(n) + " N_Oke: " + str(n_oke) + " N_not_good " + str(n_not_oke)
    org_info = (200, 550) 
    img = cv2.putText(img,Info, org_info, font,  
                    fontScale, color, thickness, cv2.LINE_AA) 
    return img

def update_frame():
    global canvas, photo, Cont
    # Gia lap sensor 
    # Connect sensor

    # PLC= snap7.client.Client()
    # PLC.connect('192.168.1.55',0,1)
    # db = PLC.db_read(DB_NUMBER,START_ADDRESS,SIZE)
    # productStatus = bool(db[258])
    # print('productStatus ', productStatus) 
    # is_show = productStatus

    is_show = gia_lap()
    
    print("im_show {} Cont {}".format(is_show,Cont))
    #
    if Cont == 1:
        if is_show == True :
            # Doc tu camera
            
            # cap = cv2.VideoCapture('http://admin:SHTP_2020@192.168.1.52:8080/cgi-bin/video.cgi?msubmenu=jpg')
            
            now = datetime.now()
            capture_time =str(now)

            # ret, ori_img = cap.read()
            # Detect 
            ori_img = cv2.imread("./test/002.jpeg")
            copied_image = ori_img.copy()

            roi_image = detect_image(copied_image)
            # cv2.imshow('ROI', roi_image)
            # cv2.waitKey(0)

            # Running post processing
            result, contours = check_good(roi_image, show=True)

            # Display result 
            
            result_image = show_result(image=ori_img, isGood=result, show=True)
            
            #             
            # PutText
            if result == True:
                n_oke += 1
            else:
                n_not_oke += 1
            n += 1
            
            img = cv2.putText( result_image, capture_time)
            # Resize
            img = cv2.resize(img, ( WINDOW_WIDTH,WINDOW_HEIGHT ))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
            status.configure(text = "Processing",font = ("Arial",20))
            Cont = 0

        else:
            photo = None
            status.configure(text = "Waiting",font = ("Arial",20))
            print("Waiting")
        
        
    # Show
    canvas.create_image(0,0, image = photo, anchor=tkinter.NW)
    window.after(15, update_frame)


window = Tk()
window.title("SHTP Camera Inspection ")


# Canvas
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