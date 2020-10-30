# Usage:
"""
    python run.py test
            or 
    python run.py device
"""

from tkinter import *
from tkinter.ttk import *
import tkinter.font as font
import tkinter
from datetime import datetime
import sys, os

import snap7
import cv2
import PIL.Image, PIL.ImageTk
from detect.yolo_detect import detect_image 
from post_processing.post_processing import check_good, show_result
from config import DB_NUMBER, START_ADDRESS, WINDOW_HEIGHT, WINDOW_WIDTH, X_POSITION, CAPTURE_VIDEO_URL, SIZE, FONT_FACE, FONT_SCALE, COLOR, THICKNESS, CAMERA_IP_ADDRESS,\
                    IMAGE_HEIGHT, IMAGE_WIDTH
from utils import next_image, simulation


# Global variables
number_of_good_bottles = 0
number_of_not_good_bottles = 0
number_of_bottles = 0
denta = 30


log_file = os.path.join('logs', datetime.now().strftime("%Y_%m_%d_%Hh_%Mm_%Ss")+'.txt')


def draw_info(img, captered_time, save, check):

    global number_of_good_bottles, number_of_not_good_bottles, number_of_bottles
    info = "{:<10s} {:<10s} {:<10s} {:<40s}\n".format(str(number_of_bottles), str(number_of_good_bottles), str(number_of_not_good_bottles), str(captered_time))
    with open(log_file, 'a+') as f:
        f.writelines(info)
    
    if check:
        status = "OKE"
        color_status = (0, 255, 0)
    else:
        status = "NOT GOOD"
        color_status = (0, 0, 255)
    status_puttext                      = "STATUS           {:<10s}".format(str(status))
    number_puttext                      = "NUMBER          {:<10s}".format(str(number_of_bottles))
    number_of_good_bottles_puttext      = "OKE              {:<10s}".format(str(number_of_good_bottles))
    number_of_not_good_bottles_puttext  = "NOT_GOOD        {:<10s}".format(str(number_of_not_good_bottles))
    time_puttext                        = "TIME              {:<10s}".format(str(captered_time))
    
    # Write status
    img = cv2.putText(img, text=status_puttext, org=(X_POSITION, 450+denta*0), fontFace=FONT_FACE, 
                    fontScale=FONT_SCALE, color=color_status, thickness=THICKNESS, lineType=cv2.LINE_AA)
    # Write number of bottles
    img = cv2.putText(img=img, text=number_puttext, org=(X_POSITION, 450+denta*1), fontFace=FONT_FACE,  
                    fontScale=FONT_SCALE, color=(255, 0, 0), thickness=THICKNESS, lineType=cv2.LINE_AA)
    # Write number of good bottles    
    img = cv2.putText(img=img, text=number_of_good_bottles_puttext, org=(X_POSITION, 450+denta*2), fontFace=FONT_FACE,  
                    fontScale=FONT_SCALE, color=(0, 255, 0), thickness=THICKNESS, lineType=cv2.LINE_AA)
    # Write number of not good bottles
    img = cv2.putText(img=img, text=number_of_not_good_bottles_puttext, org=(X_POSITION, 450+denta*3), fontFace=FONT_FACE,  
                    fontScale=FONT_SCALE, color=(0, 0, 255), thickness=THICKNESS, lineType=cv2.LINE_AA)
    # Write time
    img = cv2.putText(img=img, text=time_puttext, org=(X_POSITION, 450+denta*4), fontFace=FONT_FACE,  
                    fontScale=FONT_SCALE, color=(0, 0, 0), thickness=THICKNESS, lineType=cv2.LINE_AA)

    if save:
        folder = "NOT_GOOD"
        if check:
            folder = "OKE"
        cv2.imwrite(os.path.join('detected_images', folder, str(number_of_bottles).zfill(5))+'.png', img)
    return img


def update_frame(test=True):

    global canvas, photo, Cont, number_of_good_bottles, number_of_not_good_bottles, number_of_bottles

    if not test:
        PLC= snap7.client.Client()
        PLC.connect(CAMERA_IP_ADDRESS, 0, 1)
        db = PLC.db_read(DB_NUMBER,START_ADDRESS, SIZE)
        productStatus = bool(db[258])
        print('productStatus ', productStatus) 
        is_show = productStatus
    else:
        is_show = simulation()
    
    if Cont == 1:
        os.system('cls')
        print("| Number of checked bottles: {:10} | Number of OKE bottles: {:10} | Number of NOT GOOD bottles: {:10}".format(number_of_bottles, number_of_good_bottles, number_of_not_good_bottles))
        if is_show:
            if test:
                ori_img = cv2.imread("./test_images/009.jpeg")
            else:
                cap = cv2.VideoCapture(CAPTURE_VIDEO_URL)
                _, ori_img = cap.read()

            now = datetime.now().strftime("%d %b %Y %Hh:%Mm:%Ss")
            capture_time =str(now)

            copied_image = ori_img.copy()

            roi_image = detect_image(copied_image)
            
            result, _ = check_good(roi_image, show=False)

            result_image = show_result(image=ori_img, isGood=result, show=False)
            
            if result:
                number_of_good_bottles += 1
            else:
                number_of_not_good_bottles += 1

            number_of_bottles += 1

            img = draw_info(img=result_image, captered_time=capture_time, save=True, check=result)

            img = cv2.resize(src=img, dsize=(WINDOW_WIDTH, WINDOW_HEIGHT), fx=1, fy=1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
            status.pack_forget()
            button.pack()
            Cont = 0
        else:
            photo = None
            button.forget()
            button.pack_forget()
            status.pack()


    canvas.create_image(0,0, image=photo, anchor=tkinter.NW)
    window.after(15, update_frame)


title = "{:<10s} {:<10s} {:<10s} {:<40s}\n".format("#NUMBERS", "#OKE", "#NOT GOOD", "TIME")
with open(log_file, 'w') as f:
    f.write(title)

try:
    mode = sys.argv[1]
except:
    print("! GIVE THE MODE FOR RUNNING (TEST or CONNECT DEVICE)")
    exit(0)

if mode == 'test':
    mode = True
elif mode == 'device':
    mode = False
else:
    print("! INVALID MODE FOR RUNNING.")
    exit(0)


window = Tk()
window.title("SHTP - AI CAMERA CHALLENGER 2020")

canvas = Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT , bg="white")
canvas.pack()

Cont = 1

button = Button(window, text="CONTINUE", command=next_image)
button.place(relx=0.5, rely=0.5, anchor=S)

status = Label(window, text="WAITING SIGNAL FROM SENSOR", font=("Arial", 20))
status.place(relx=0.5, rely=0.5, anchor=CENTER)

photo = None
update_frame(test=mode)
window.mainloop()