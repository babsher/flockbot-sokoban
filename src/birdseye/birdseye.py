from __future__ import division
import cv2
import numpy as np
from grid import Grid
import time
import csv
import zerorpc
import threading
import gevent
from gevent import Greenlet
from zerorpc import zmq

SERVER_ON = True

#resolution of the camera image
WIDTH = 640
HEIGHT = 480

#number of frames to discard when the camera first starts up
RAMP_FRAMES = 5

#lower & upper threshold for box color (hsv)
LOWER_THRESH_BOX = np.array([0,70,100])
UPPER_THRESH_BOX = np.array([25,150,255])
#the minimum area that a connected component can be to be considered a box
MIN_BOX_AREA = 300

#lower & upper threshold for goal points (hsv)
LOWER_THRESH_GOAL = np.array([35,100,120])
UPPER_THRESH_GOAL = np.array([85,160,255])
#the minimum area that a connected component can be to be considered a goal
MIN_GOAL_AREA = 300

#lower & upper threshold for obstacle points (hsv)
LOWER_THRESH_OBS = np.array([120,40,100])
UPPER_THRESH_OBS = np.array([180,140,255])
#the minimum area that a connected component can be to be considered a goal
MIN_OBS_AREA = 300

LOWER_THRESH_FLOCK1 = np.array([90,60,180])
UPPER_THRESH_FLOCK1 = np.array([135,190,255])

LOWER_THRESH_FLOCK2 = np.array([20,16,255])
UPPER_THRESH_FLOCK2 = np.array([46,70,255])

#the file containing the grid layout
GRID_LAYOUT_FILE = "grid_layout.csv"

#configuration for what to display
DISP_BOX_MASK = False
DISP_GOAL_MASK = False
DISP_OBS_MASK = False
DISP_COLOR = True
DISP_GRID = True
DISP_FLOCK = False

print "Starting up camera."
camera = cv2.VideoCapture(0)

def get_image():
    ''' retrieves an image from the camera'''
    retval, im = camera.read()
    return retval, im

def ramp():
    '''discards some frames immediately after the camera start up for warmup'''
    for i in range(RAMP_FRAMES):
        discard = get_image()

def blur(im):
    '''blurs the given image, returns the blurred image'''
    k = (7,7)
    blurred = cv2.GaussianBlur(im, k, 5)
    return blurred

def snapshot(im):
    '''saves the given image to disk with the timestamp as the name'''
    t = str(int(time.time()))
    cv2.imwrite("snapshots/"+t+".png",im)
    print "Saved a snapshot: " + t + ".png"


def center_mass(contour):
    '''given a contour (like those returned by cv2.findContours), calculates and returns the center of mass'''
    moments = cv2.moments(contour)
    com = (int(moments['m10'] / moments['m00']),int(moments['m01'] / moments['m00']))
    return com

def center_masses(contours):
    '''given a list of contours(like those returned by cv2.findCounters), calculates and returns a list of the coms'''
    
    coms = []

    #calculate the center of mass of each contour
    for contour in contours:
                
       #get center of mass
       com = center_mass(contour)
       coms.append(com)

    return coms

def threshold(img, lower_thresh, upper_thresh):
    '''returns the resulting mask when thresholding the given image by the given thresholds'''
    mask = cv2.inRange(img, lower_thresh, upper_thresh)
    return mask

def get_coms(img, lower_thresh, upper_thresh, min_area, display, name):
    '''gets the centers of mass of the objects it finds by thresholding'''

    #threshold color segmentation
    mask = threshold(img, lower_thresh, upper_thresh)

    #find contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #get the large contours
    large_contours = [contour for contour in contours if cv2.contourArea(contour) > min_area]

    #list to store the center of masses
    coms = center_masses(large_contours)

    if display:

        #create a new image of only the large contours
        maskimg = np.zeros((HEIGHT, WIDTH, 3))

        #draw the (filled) contours onto the image
        cv2.drawContours(maskimg, large_contours, -1, np.array([255,255,255]), -1)

        for com in coms:
          #draw a circle showing where the com is in the new image
          cv2.circle(maskimg,com,5,np.array([0,0,255]),-1)

        cv2.imshow(name,cv2.flip(maskimg,-1))

    return coms

def get_box_coms(img):
    '''finds the center of mass of boxes in the given image and returns them'''
    coms = get_coms(img,LOWER_THRESH_BOX,UPPER_THRESH_BOX,MIN_BOX_AREA,DISP_BOX_MASK,"Box Mask")
    return coms

def get_goal_coms(img):
    '''finds the center of mass of goal positions in the given image and returns them'''
    coms = get_coms(img,LOWER_THRESH_GOAL,UPPER_THRESH_GOAL,MIN_GOAL_AREA,DISP_GOAL_MASK,"Goal Mask")
    return coms

def get_obs_coms(img):
    '''finds the center of mass of obs positions in the given image and returns them'''
    coms = get_coms(img,LOWER_THRESH_OBS,UPPER_THRESH_OBS,MIN_OBS_AREA,DISP_OBS_MASK,"Obstacle Mask")
    return coms

def coms_in_grid(grid, coms):
    '''given a list of centers of masses, will check to see if those coms are in the grid
    and if so, will return a list of grid spaces those coms are occupying'''
    pts = []
    for com in coms:
        if grid.in_grid(com):
            grid_pt = grid.where_in_grid(com)
            if grid_pt != None:
                pts.append(grid_pt)
    return pts

def set_goal_locations(grid):
    '''grabs an image from the camera, processes it to find goal locations, 
    and updates the grid with those locations'''

    success, image = get_image()
    if success:
       
       #blur the image
       blurred = blur(image)

       #convert to hsv color space
       hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

       #get center of mass of goals
       goal_coms = get_goal_coms(hsv)

       #see if/where the boxes are in the grid
       goal_pts = coms_in_grid(grid,goal_coms)
      
       #update the grid to reflect the found boxes
       grid.set_goals(goal_pts)

def set_obstacle_locations(grid):
    '''grabs an image from camera, processes it to find obstacle locations, and updates
    the grid with those locations'''

    success, image = get_image()
    if success:

       #blur the image
       blurred = blur(image)

       #convert to hsv color space
       hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

       #get center of mass of obstacles
       obs_coms = get_obs_coms(hsv)

       #see if/where the obstacles are in the grid
       obs_pts = coms_in_grid(grid,obs_coms)

       #update the grid
       grid.set_obs(obs_pts)

def set_box_locations(grid, hsv = None):

    if hsv == None:
        success, image = get_image()

        #blur the image
        blurred = blur(image)

        #convert to hsv color space
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    #get center of mass of boxes -----------------
    box_coms = get_box_coms(hsv)

    #see if/where the boxes are in the grid
    box_pts = coms_in_grid(grid,box_coms)

    #update the grid to reflect the found boxes
    grid.set_boxes(box_pts)

def get_flock_location(grid, hsv, lower_thresh, upper_thresh,name):

    if hsv == None:
        success, image = get_image()

        #blur the image
        blurred = blur(image)

        #convert to hsv color space
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = threshold(hsv, lower_thresh, upper_thresh)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    if hierarchy != None:
        hierarchy = hierarchy[0]
        parent_child_pairs = []
        #figure out which is parent which is child
        for i,contour in enumerate(contours):
            if cv2.contourArea(contour) >  100:
                # no parent, and has child
                if hierarchy[i][3] < 0 and hierarchy[i][2] >= 0:
                    parent_child_pairs.append((contours[i],contours[hierarchy[i][2]]))

        p_c_coms = [(center_mass(parent),center_mass(child)) for parent,child in parent_child_pairs]

        flock_points = []

        if DISP_FLOCK:
            maskimg = np.zeros((HEIGHT, WIDTH, 3))
            cv2.drawContours(maskimg, contours, -1, np.array([255,255,255]), -1)

        for pcom, ccom in p_c_coms:
            if grid.in_grid(pcom):

                orientation = int(np.degrees(np.arctan2(ccom[1]-pcom[1],ccom[0]-pcom[0])))
                #print (grid.where_in_grid(pcom),orientation)
                flock_points.append((grid.where_in_grid(pcom),orientation))

                if DISP_FLOCK:
                    cv2.circle(maskimg,pcom,3,np.array([0,0,255]),-1)
                    cv2.circle(maskimg,ccom,3,np.array([0,0,255]),-1)

        if DISP_FLOCK:
            cv2.imshow(name, cv2.flip(maskimg,-1))

        return flock_points

def set_flock1_location(grid, hsv = None):

    flock1_locations = get_flock_location(grid, hsv, LOWER_THRESH_FLOCK1, UPPER_THRESH_FLOCK1, "Flock1")
    if flock1_locations == [] or flock1_locations == None:
        grid.set_flock1([])
    else:
        grid.set_flock1(flock1_locations[0])

def set_flock2_location(grid, hsv = None):

    flock2_locations = get_flock_location(grid, hsv, LOWER_THRESH_FLOCK2, UPPER_THRESH_FLOCK2, "Flock2")
    if flock2_locations == [] or flock2_locations == None:
        grid.set_flock2([])
    else:
        grid.set_flock2(flock2_locations[0])

def setup_server(grid):
    '''sets up the server for transmitting grid info'''

    class BIServ(zerorpc.Server):
        def get_box_pts(self):
            return grid.get_box_pts()

        def get_goal_pts(self):
            return grid.get_goal_pts()

        def get_obs_pts(self):
            return grid.get_obs_pts()

        def get_flock_pts(self):
            return grid.get_flock_pts()

        def get_flock1(self):
            return grid.get_flock1()

        def get_flock2(self):
            return grid.get_flock2()

    srv = BIServ()
    srv.bind("tcp://0.0.0.0:4242")
    g = Greenlet(srv.run)
    g.start()
    return srv

def main():

    #print "Resolution: {}x{}.".format(int(camera.get(3)), int(camera.get(4)))

    print "Ramping up."
    ramp()

    #set up the grid
    print "Initializing grid."
    grid = Grid(GRID_LAYOUT_FILE)

    #find & set the goal locations on the grid
    set_goal_locations(grid)
    print "Found goal locations: "
    print grid.get_goal_pts()

    #find & set obstacle locations on the grid
    set_obstacle_locations(grid)
    print "Found obstacle locations: "
    print grid.get_obs_pts()

    #set up the server
    if SERVER_ON:
       srv = setup_server(grid)

    #main loop for getting box positions
    while True:

        if SERVER_ON:
            gevent.sleep(.01)

        success, image = get_image()
        if success:

            #blur the image
            blurred = blur(image)

            #convert to hsv color space
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            set_box_locations(grid, hsv)

            #set_flock1_location(grid, hsv)
            # set_flock2_location(grid, hsv)

            #red_mask = threshold(hsv, LOWER_ORT_RIGHT, UPPER_ORT_RIGHT)
            #together = cv2.bitwise_or(blue_mask,red_mask)

            if DISP_COLOR:
                #display color image
                colorwgrid = grid.overlay_grid(image)
                colorwgrid = cv2.flip(colorwgrid,-1)            
                cv2.imshow("color", colorwgrid)

        #show the internal representation of the grid
        if DISP_GRID:
            grid_img = grid.display_grid()

        #take a snapshot of the color image
        if (cv2.waitKey(1) & 0xFF == ord('s')):
            snapshot(colorwgrid)

        #take a snapshot of the grid image
        if (cv2.waitKey(1) & 0xFF == ord('g')):
            snapshot(grid_img)

        #quit
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            print "Quitting..."
            if SERVER_ON:
                srv.close()
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

