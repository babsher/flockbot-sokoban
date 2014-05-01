import cv2
import numpy as np
import csv
import time


def save_to_csv(points):
	'''saves the list of points to a csv file'''

	t = str(int(time.time()))
	with open(t+'.csv', 'wb') as csvfile:

		spamwriter = csv.writer(csvfile, delimiter=',')
		for x,y in points:
			spamwriter.writerow([x,y])

# mouse callback function
def mouse_clicked(event,x,y,flags,(img,points)):
	'''This function handles mouseclick events by adding the x.y pos to the list of points'''
	if event == cv2.EVENT_LBUTTONUP:
		points.append((x,y))
		cv2.circle(img,(x,y),5,(0,0,255),-1)

def main():

	#read the image from disk
	name = "../snapshots/1398470596.png"
	img = cv2.imread(name)

	#list to store the points in
	points = []

	#set up window for display & clicking
	cv2.namedWindow('image')
	cv2.setMouseCallback('image',mouse_clicked,(img,points))

	while True:
		cv2.imshow('image',img)
		if cv2.waitKey(20) & 0xFF == ord('q'):
			break

	cv2.destroyAllWindows()

	#save the points to a csv file
	print "Saving points to csv file."
	save_to_csv(points)


if __name__ == '__main__':
	main()