# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import serial
import syslog
import time
import numpy as np

# define capturing size
width = 320
height = 240
tracking_width = 40
tracking_height = 40
auto_mode = 0

def check_for_direction(position_x):
    if position_x == 0 or position_x == width:
        print 'out of bound'
        arduino.write('s')
        arduino.write('f')
        arduino.write('m')
    if position_x <= ((width-tracking_width)/2 - tracking_width):
        print 'move right!'
        arduino.write('r')
    elif position_x >= ((width-tracking_width)/2 + tracking_width):
        print 'move left!'
        arduino.write('l')
    else:
        # print 'move front'
        arduino.write('f')

# initialize arduino port
port = '/dev/ttyACM0'
arduino = serial.Serial(port, 9600, timeout=5)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(width, height))
rawCapture2 = PiRGBArray(camera, size=(width, height))

# allow the camera to warmup
time.sleep(0.1)

# set the ROI (Region of Interest)
c,r,w,h = (width/2 - tracking_width/2), (height/2 - tracking_height/2), tracking_width, tracking_height
track_window = (c,r,w,h)

# capture single frame of tracking image
camera.capture(rawCapture2, format='bgr')

# create mask and normalized histogram
roi = rawCapture2.array[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array([0,30,32]), np.array([180,255,255]))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0,180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # filtering for tracking algorithm
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,180], 1)

    ret, track_window = cv2.meanShift(dst, track_window, term_crit)
    x,y,w,h = track_window
    cv2.rectangle(image, (x,y), (x+w,y+h), 255, 2)
    cv2.putText(image, 'Tracked', (x-25, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.CV_AA)

    # show the frame
    cv2.imshow("Raspberry Pi RC Car", image)
    key = cv2.waitKey(1) & 0xFF

    # check for direction of the car
    if auto_mode == 1:
        check_for_direction(x)
        time.sleep(0.1)

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # distinguish action command for rc car control
    if key == ord("q"):
	break

    if key == ord("g"):
	arduino.write("g")
        auto_mode = 0
        print "let's go"

    if key == ord("s"):
	arduino.write("s")
        auto_mode = 0
        print "let's stop"

    if key == ord("a"):
        arduino.write("a")
        auto_mode = 1
        print "auto mode"

    if key == ord("r"):
        arduino.write("r")
        auto_mode = 0
        print "turn right"

    if key == ord("l"):
        arduino.write("l")
        auto_mode = 0
        print "turn left"

    if key == ord("f"):
        arduino.write("f")
        auto_mode = 0
        print "go straight"

rawCapture2.truncate(0)
