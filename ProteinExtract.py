 # -*- coding: utf-8 -*-
import cv2
import operator
import ColorMatching
import os

ytotal = 7.3

upper_ratio = 4.5/ytotal
lower_ratio = 5.1/ytotal

xtotal = 2.9
left_ratio = 0.9/xtotal
right_ratio = 2/xtotal


result_list = [0, 0.3, 1.0, 3.0, 10]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

directory = os.path.join(BASE_DIR, 'EclampsiaDetection')
#directory = BASE_DIR


#DISPLAYING IMAGES 
def image_show(header, image):
    '''
    cv2.imshow(header, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    

#DISPLAYING THE CORNER POINTS ON THE IMAGE 
def display_points(header, in_img, points, radius=40, colour=(0, 0, 255)):
	"""Draws circular points on an image."""
	imgee = in_img.copy()

	# Dynamically change to a colour image if necessary
	if len(colour) == 3:
		if len(imgee.shape) == 2:
			imgee = cv2.cvtColor(imgee, cv2.COLOR_GRAY2BGR)
		elif imgee.shape[2] == 1:
			imgee = cv2.cvtColor(imgee, cv2.COLOR_GRAY2BGR)

	for point in points:
		imgee = cv2.circle(imgee, tuple(int(x) for x in point), radius, colour, -1)
	image_show(header, imgee)
    


def imageExtract(directory):
    #READ IMAGE
    imagepath = os.path.join(directory,'images', 'testimage.jpg')
    
    img = cv2.imread(imagepath)
    
    #RESIZED IMAGE
    img = cv2.resize(img,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
    baseimage = img
    title = 'Resized_image'
    image_show(title, img)
    
    #CHANGING TO GRAYSCALE
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #baseimagegrayscale = img
    title = 'Grayscale_image'
    image_show(title, img)
        
        
    '''
      
    #APPLYING ADAPTIVE THRESHOLD
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 25)
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    title = 'Thresholded_image_image'
    image_show(title, img) 
        
    
    #INVERTING COLORS
    img = cv2.bitwise_not(img, img)
    title = 'Inverted_colours'
    image_show(title, img)
    contourimage = img
        
        
    #DILATE IMAGE TO RINCREASE SIZE OF GRID LINES
    kernel = np.ones((3,3),np.uint8)
    img = cv2.dilate(img, kernel, iterations = 1)
    title = 'Dilated_image'
    image_show(title, img)
    
    '''
        
    #FINDING CONTOURS TO ACQUIRE THE EDGE OF POLYGON
    new_img, ext_contours, hier = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    new_img, contours, hier = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    
    
    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    contourimage = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    
    # Draw all of the contours on the image in 2px red lines
    all_contours = cv2.drawContours(contourimage.copy(), contours, -1, (0, 0, 255), 2)
    title = 'All-Contours'
    image_show(title, all_contours)
    
    
    external_only = cv2.drawContours(contourimage.copy(), ext_contours, -1, (0, 0, 255), 2)
    title = 'External-Contours'
    image_show(title, external_only)
    
    
    
    #FINDING THE CORNERS OF THE BIGGEST CONTINUOUS POLYGON
    im2, contours, hierarchy = cv2.findContours(img.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)  # Sort by area, descending
    polygon = contours[0]  # Largest image
    
    # Use of `operator.itemgetter` with `max` and `min` allows us to get the index of the point
    # Each point is an array of 1 coordinate, hence the [0] getter, then [0] or [1] used to get x and y respectively.
    
    # Bottom-right point has the largest (x + y) value
    # Top-left has point smallest (x + y) value
    # Bottom-left point has smallest (x - y) value
    # Top-right point has largest (x - y) value
    
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    
    # Return an array of all 4 points using the indices
    # Each point is in its own array of one coordinate
    corners = [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]
    
    title = 'Points'
    display_points(title, contourimage, corners)
    
    '''
    print('Top_Left', polygon[top_left][0])
    print('Top_Right', polygon[top_right][0])
    print('Bottom_Left', polygon[bottom_left][0])
    print('Bottom_Right', polygon[bottom_right][0])
    '''
    
    
    y_cordinate0 = int(upper_ratio*polygon[bottom_left][0][1])
    y_cordinate1 = int(lower_ratio*polygon[bottom_left][0][1])
    x_cordinate0 = int(left_ratio*polygon[top_right][0][0])
    x_cordinate1 = int(right_ratio*polygon[top_right][0][0])
    
    '''
    print('y_cordinate0', y_cordinate0)
    print('y_cordinate1', y_cordinate1)
    print('x_cordinate0', x_cordinate0)
    print('x_cordinate1', x_cordinate1)
    '''
    
    proteinimage = baseimage[y_cordinate0:y_cordinate1, x_cordinate0:x_cordinate1]
    title = 'Protein test image)'
    proteinimage = cv2.resize(proteinimage,None,fx=2, fy=2, interpolation = cv2.INTER_LINEAR)
    image_show(title, proteinimage)
    
    position = ColorMatching.colourIndex(proteinimage)
    #print('Position ',position)
    
    #print('Protein_value ', result_list[position])
    
    return result_list[position]

    #imageExtract(directory)








