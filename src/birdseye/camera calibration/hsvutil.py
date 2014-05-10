import cv2
import numpy as np
import time

def nothing(x):
    pass


camera = cv2.VideoCapture(0)

# Make a window for the video feed  
cv2.namedWindow('frame',cv2.CV_WINDOW_AUTOSIZE | cv2.WINDOW_OPENGL)

# Make trackbars for thresholding  
cv2.createTrackbar('LowerH','frame',0,180,nothing)
cv2.createTrackbar('UpperH','frame',0,180,nothing)
cv2.createTrackbar('LowerS','frame',100,255,nothing)
cv2.createTrackbar('UpperS','frame',255,255,nothing)
cv2.createTrackbar('LowerV','frame',100,255,nothing)
cv2.createTrackbar('UpperV','frame',255,255,nothing)

while True:

    # Capture frame-by-frame
    ret, frame = camera.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Name the variable used for mask bounds
    lower_h = cv2.getTrackbarPos('LowerH','frame')
    upper_h = cv2.getTrackbarPos('UpperH','frame')

    lower_s = cv2.getTrackbarPos('LowerS','frame')
    upper_s = cv2.getTrackbarPos('UpperS','frame')

    lower_v = cv2.getTrackbarPos('LowerV','frame')
    upper_v = cv2.getTrackbarPos('UpperV','frame')

    # define range of color in HSV
    lower = np.array([lower_h,lower_s,lower_v])
    upper = np.array([upper_h,upper_s,upper_v])

    # Threshold the HSV image to get only selected color
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask the original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Display the resulting frame
    cv2.imshow('frame',cv2.flip(mask,-1))

    # Press q to quit
    if cv2.waitKey(3) & 0xFF == ord('q'):
        break

    elif cv2.waitKey(3) & 0xFF == ord('p'):
    	print "Lower H: " + str(lower_h)
    	print "Upper H: " + str(upper_h) 

    	print "Lower S: " + str(lower_s)
    	print "Upper S: " + str(upper_s)

    	print "Lower V: " + str(lower_v)
    	print "Upper V: " + str(upper_v)  


# When everything is done, release the capture
camera.release()
cv2.destroyAllWindows()