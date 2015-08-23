# Raspi-RC-Car
Raspberry Pi Remote Control Car with Tracking System

## camera.py
> camera.py is the basic raspberry pi camera python script that allows users to see how the PiCamera works. Also it contains a little bit arduino control commands in order to manage RC car.

## camera_alpha.py
> camera_alpha.py contains all the things in camera.py. It also contains barcode tracking module in it. With series of open-cv filters, it distinguishes barcode and keep track of it with contours.

## camera_cv2.py
> camera_cv2.py contains all the things in camera.py. It also contains object tracking module in it. Not like barcode tracking, first it need to capture single frame and decide an object to follow. After the object had decided, it will keep track of it. Size of the object and camera resolution can be changed by changing defined values.

### Update info
#### 2015.08.22
+ Update some of algorithm

#### 2015.08.21
+ Update some of algorithm of tracking
+ Refactorized some of codes
+ Test actual running of RC car

#### 2015.08.20
+ Decision make for RC car to move left or right
+ Arduino update for left / right movement
+ Removal of temp folder
