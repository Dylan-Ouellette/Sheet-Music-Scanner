import cv2 as cv
import numpy as np
from Classification_Functions import  checkDistance

def Treble_Classification(img_gray, img_rgb, template_file, threshold):

    template = cv.imread(template_file, cv.IMREAD_GRAYSCALE)
    treble_w, treble_h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    treble_pt_list = []

    #draws rectangles
    for pt in zip(*loc[::-1]):
        if checkDistance(treble_pt_list, pt, 50):
            treble_pt_list.append(pt)
            cv.rectangle(img_rgb, pt, (pt[0] + treble_w, pt[1] + treble_h), (0,255,0), 2)

    page_length, page_width = img_gray.shape

    #removes top part of page above the first treble clef to remove classification of title
    for y in range(page_length):
            for x in range(page_width):
                # Check if the pixel is above the specified y-coordinate
                if y < treble_pt_list[0][1] - 30:
                    # Set pixel color to white (255, 255, 255)
                    img_gray[y, x] = 255
    
    treble_list = []
    for treble_pt in treble_pt_list:
         treble_list.append([treble_pt, "treble", (treble_w, treble_h)])

    return treble_list