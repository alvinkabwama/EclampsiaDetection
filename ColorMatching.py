# -*- coding: utf-8 -*-

import cv2
import numpy as np

def nothing(x):
    pass

#DISPLAYING IMAGES 
def image_show(header, image):
    '''
    cv2.imshow(header, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    
   
def colourIndex(testimage):    
    
    #testimage = cv2.imread('test_images/testcrop.jpg')
    #changing the incoming crop to hsv from rgb
    hsv = cv2.cvtColor(testimage, cv2.COLOR_BGR2HSV)
        
    #NEGATIVE PROTEIN TEST
    lowerneg = np.array([22, 60, 80])
    higherneg = np.array([30, 255, 255]) 
    
    #FIRST PROTEIN TEST
    lowerfirst = np.array([30, 60, 80])
    higherfirst = np.array([38, 255, 255]) 
    
    
    #SECOND PROTEIN TEST
    lowersecond = np.array([40, 60, 80])
    highersecond = np.array([58, 255, 255])
    
    #THIRD PROTEIN TEST
    lowerthird = np.array([80, 60, 80])
    higherthird = np.array([100, 255, 255])
    
    
    colorlist = []
    pixel_list = []
    colorlist.append(lowerneg)
    colorlist.append(higherneg)
    colorlist.append(lowerfirst)
    colorlist.append(higherfirst)
    colorlist.append(lowersecond)
    colorlist.append(highersecond)
    colorlist.append(lowerthird)
    colorlist.append(higherthird)
    
    for n in range(7):
        
        if (n%2 == 0):       
            mask = cv2.inRange(hsv, colorlist[n], colorlist[n+1])
            result = cv2.bitwise_and(testimage, testimage, mask = mask)        
            nonzero = cv2.countNonZero(mask)
            pixel_list.append(nonzero)
            
            
            print('Number of Nonzero Pixels: ', nonzero)
            cv2.imshow('Mask', mask)
            cv2.imshow('Original', testimage)
            cv2.imshow('Result', result)
            cv2.waitKey(0)  
            cv2.destroyAllWindows()
            
            
    highvalindex = pixel_list.index(max(pixel_list))
    
    #print(highvalindex)
    return highvalindex
 

