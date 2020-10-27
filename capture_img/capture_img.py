import cv2
import snap7
import argparse

# CONSTANT 
DB_NUMBER = 100
START_ADDRESS = 0
SIZE = 259


def get_image(path_save):

    # Connect sensor
    PLC= snap7.client.Client()
    PLC.connect('192.168.1.55',0,1)

    while(True):

        # Read signal from sensor
        db = PLC.db_read(DB_NUMBER,START_ADDRESS,SIZE)
        productStatus = bool(db[258])
        print('productStatus ', productStatus)

        if productStatus == True:
            # Capture frame
            cap = cv2.VideoCapture('http://admin:SHTP_2020@192.168.1.52:8080/cgi-bin/video.cgi?msubmenu=jpg')
            ret, frame = cap.read()

            # Our operations on the frame come here
            #img = cv2.cvtColor(frame)

            # Display the resulting frame
            # cv2.imshow('frame',frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            if path_save != None:
                cv2.imwrite(path_save,frame)
            return frame 
    
def main(args):
    
    # Take image from Sensor
    img = get_image(args["path_save"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process image and display result.')
    parser.add_argument('-s','--path_save', type=str,default=None, help='The path to save the image.')
    main(vars(parser.parse_args()))

