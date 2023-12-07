
import cv2
import numpy as np
from Classification_Functions import checkDistance

def removeLine(image, value, output):
    img = image
    val = value
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bw_gray = cv2.bitwise_not(gray)
    _, threshold_gray = cv2.threshold(bw_gray, 100, 255, cv2.THRESH_BINARY)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, val))
    vertical = cv2.morphologyEx(threshold_gray, cv2.MORPH_OPEN, vertical_kernel)
    vertical_inverted = cv2.bitwise_not(vertical)
    cv2.imwrite(output, vertical_inverted)

       
def detectionLine(img, template, threshold): 

    img_rgb = cv2.imread(img)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
    line_w, line_h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    line_pt_list = []

    page_length, page_width = img_gray.shape

    #removes 5/6 left part of the page to reduce noise
    for y in range(page_length):
            for x in range(page_width):
                if x > (page_width / 6):
                    # Set pixel color to white (255, 255, 255)
                    img_gray[y, x] = 255

    # draws rectangles
    for pt in zip(*loc[::-1]):
        if checkDistance(line_pt_list, pt, 10):
            line_pt_list.append(pt)
            cv2.rectangle(img_rgb, pt, (pt[0] + line_w, pt[1] + line_h), (255,0,0), 2)

    #adjust points to compensate for template
    newList = []
    for point in line_pt_list:
         newList.append((point[0] + 30, point[1] + 5))
    line_pt_list = newList

    #splits list in chunks of 5
    line_pt_list = [line_pt_list[i:i + 5] for i in range(0, len(line_pt_list), 5)]

    return line_pt_list


       














    
