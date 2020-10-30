import cv2


SIZE_WINDOW_GUI = {
	'WIDTH': 800,
	'HEIGHT': 500,
}

SIZE_DISPLAY = (800, 700)

FONT = 'Arial Bold'

TEXTS = {
	'camera_window_title': 'Tien Nguyen UIT - KHMT',
	'':'',
}

TEXT_POSITIONS = {
	'camera_window_title': (SIZE_WINDOW_GUI['WIDTH']//2, 20),
	
}

# PARAMETERS FOR GRAPHIC USE INTERFACE
DB_NUMBER = 100
START_ADDRESS = 0
SIZE = 259

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
X_POSITION = 10
IMAGE_WIDTH = int(WINDOW_WIDTH*0.8)
IMAGE_HEIGHT = int(WINDOW_HEIGHT*0.9)


CAPTURE_VIDEO_URL = 'http://admin:SHTP_2020@192.168.1.190:80/cgi-bin/video.cgi?msubmenu=jpg'
SIZE = 259
CAMERA_IP_ADDRESS = '192.168.1.100'

# Parameter for display required information
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX   
FONT_SCALE = 0.5
COLOR = (0, 0, 255) 
THICKNESS = 1

