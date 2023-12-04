import cv2 as cv
import numpy as np
from Classification_Functions import  checkDistance

def BarLine_Classifcation(img_gray, img_rgb, template_file, threshold):

    template = cv.imread(template_file, cv.IMREAD_GRAYSCALE)
    barline_w, barline_h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    barline_pt_list = []

    for pt in zip(*loc[::-1]):
        if checkDistance(barline_pt_list, pt, 50):
            barline_pt_list.append(pt)
            cv.rectangle(img_rgb, pt, (pt[0] + barline_w, pt[1] + barline_h), (100,100,100), 2)
    
    barline_list = []
    for barline_pt in barline_pt_list:
         barline_list.append([barline_pt, "bass"])

    return barline_list

    