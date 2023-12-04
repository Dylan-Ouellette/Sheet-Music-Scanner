import cv2 as cv
import numpy as np
from Classification_Functions import  checkDistance

def Bass_Classification(img_gray, img_rgb, template_file, threshold):

    template = cv.imread(template_file, cv.IMREAD_GRAYSCALE)
    bass_w, bass_h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    bass_pt_list = []

    #draws rectangles
    for pt in zip(*loc[::-1]):
        if checkDistance(bass_pt_list, pt, 50):
            bass_pt_list.append(pt)
            cv.rectangle(img_rgb, pt, (pt[0] + bass_w, pt[1] + bass_h), (255,0,0), 2)

    bass_list = []
    for bass_pt in bass_pt_list:
         bass_list.append([bass_pt, "bass"])

    return bass_list




