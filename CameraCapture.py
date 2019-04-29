# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os
import sys
 
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

directory = os.path.join(BASE_DIR, 'EclampsiaDetection')
#directory = BASE_DIR

print(directory)

# initialize the camera and grab a reference to the raw camera capture

height = 400
width = 80
print(width)
camera = PiCamera()
#camera.resolution = (640, 480)
camera.resolution = (width, height)
camera.framerate = 32
#rawCapture = PiRGBArray(camera, size=(640, 480))
rawCapture = PiRGBArray(camera, size=(width, height))

 
# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    rectimage = image

    x = int( width/3 )
    y = 0
    w = int( width/3 )
    h = height
    cv2.rectangle(rectimage, (x, y), (x+w, y+h), (00, 00, 255), 1)
    
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
     
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
 
	 # if the `q` key was pressed, break from the loop
    if key == ord("c"):
        image = frame.array
        imagepath = os.path.join(directory,'images', 'testimage.jpg')
        cv2.imwrite(imagepath, image)
        cv2.destroyAllWindows()
        os.system('sudo python3 Eclampsia.py')

    if key == ord("q"):
        cv2.destroyAllWindows()
        sys.exit()
        break
        
        
        
