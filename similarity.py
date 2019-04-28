# -*- coding: utf-8 -*-

import cv2
import numpy as np

def nothing(x):
    pass

#DISPLAYING IMAGES 
def image_show(header, image):
    
    cv2.imshow(header, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        print('Q')
        break
    
    
import csv
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

directory = os.path.join(BASE_DIR, 'Test_Strip')
#directory = BASE_DIR

print(directory)

csvpath = os.path.join(directory,'Data.csv')


name = 'Alvin'
high_pressure = '70'
low_pressure = '34'
pregnancy_age = '12'
protein_value = 3.0

hpress_float = float(high_pressure)
lpress_float = float(low_pressure)
preg_float = float(pregnancy_age)
prot_float = float(protein_value)

param_list = [name, hpress_float, lpress_float, preg_float, prot_float]
title_list = ['Name','High Blood Pressure', 'Low Blood Pressure', 'Preg Age', 'Protein Value']     

exists = os.path.isfile('Data')
if exists:
    with open('Data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(param_list)
else:
    with open('Data.csv', 'a') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(title_list)
        writer.writerow(param_list)
    

    
    # Store configuration file values
    


'''
croptest = cv2.imread('test_images/testcrop.jpg')
sample = cv2.imread('test_images/image_0.jpg')

sample = cv2.resize(sample,None,fx=3, fy=3, interpolation = cv2.INTER_LINEAR)
title = 'Sample_image'
image_show(title, sample)

croptest = cv2.resize(croptest,None,fx=2, fy=2, interpolation = cv2.INTER_LINEAR)
title = 'Crop_image'
image_show(title, croptest)
'''


'''
cv2.namedWindow('TrackBars')

cv2.createTrackbar("L - H", 'Trackbars', 0, 179, nothing)
cv2.createTrackbar("L - S", 'Trackbars', 0, 255, nothing)
cv2.createTrackbar("L - V", 'Trackbars', 0, 255, nothing)
cv2.createTrackbar("U - H", 'Trackbars', 179, 179, nothing)
cv2.createTrackbar("L - S", 'Trackbars', 255, 255, nothing)
cv2.createTrackbar("L - V", 'Trackbars', 255, 255, nothing)
'''


combined = cv2.imread('test_images/main_combined.jpg')
hsv = cv2.cvtColor(combined, cv2.COLOR_BGR2HSV)

'''
l_h = cv2.getTrackbarPos("L - H", 'Trackbars')
l_s = cv2.getTrackbarPos("L - S", 'Trackbars')
l_v = cv2.getTrackbarPos("L - V", 'Trackbars')
u_h = cv2.getTrackbarPos("U - H", 'Trackbars')
u_s = cv2.getTrackbarPos("U - S", 'Trackbars')
u_v = cv2.getTrackbarPos("U - V", 'Trackbars')
    

lowertest = np.array([l_v, l_s, l_v])
highertest = np.array([u_v, u_s, u_v]) 
'''

lowertest = np.array([80, 60, 80])
highertest = np.array([100, 255, 255]) 

mask = cv2.inRange(hsv, lowertest, highertest)
result = cv2.bitwise_and(combined, combined, mask = mask)

cv2.imshow('Mask', mask)
cv2.imshow('Original', combined)
cv2.imshow('Result', result)
cv2.waitKey(0)  
cv2.destroyAllWindows()






#NEGATIVE PROTEIN
lowerneg = np.array([22, 60, 80])
higherneg = np.array([30, 255, 255]) 

#FIRST POTEIN TEST
lowerfirst = np.array([30, 60, 80])
higherfirst = np.array([38, 255, 255]) 


#SECOND PROTEIN TEST
lowersecond = np.array([40, 60, 80])
highersecond = np.array([58, 255, 255])

#THIRD PROTEIN TEST
lowerthird = np.array([80, 60, 80])
higherthird = np.array([100, 255, 255])


















'''

croptest_grey = cv2.cvtColor(croptest, cv2.COLOR_BGR2GRAY)
sample_grey = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)

w,h = sample_grey.shape[::-1]

res = cv2.matchTemplate(croptest_grey, sample_grey, cv2.TM_CCOEFF_NORMED)

threshold = 0.6
loc = np.where(res >= threshold)
count = 0
for pt in zip(*loc[::-1]):
    count = count+1
    cv2.rectangle(croptest, pt, (pt[0]+w, pt[0]+h), (0,255,255), 2)

print('Count: ', count)
title = 'Detected'
image_show(title, croptest)
'''







'''

title = 'Crop_image'
image_show(title, croptest)

title = 'Sample_image'
image_show(title, sample)

sift = cv2.xfeatures2d.SIFT_create()

kp_1, desc_1 = sift.detectAndCompute(sample, None)
kp_2, desc_2 = sift.detectAndCompute(croptest, None)


index_params = dict(algorithm = 0, trees = 50)
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(desc_1, desc_2,k = 100)
print(len(matches))

'''

