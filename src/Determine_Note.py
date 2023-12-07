import cv2 as cv
import numpy as np
from Classification_Functions import checkDistance, checkDistance_point

def musical_note(body_loc, line_list, closeness):
    for staff in line_list:
        distance = staff[1][1] - staff[0][1]
        if not checkDistance_point(body_loc, (body_loc[0], (staff[0][1] - distance) ), closeness):
            return "G5"
        if not checkDistance_point(body_loc, (body_loc[0], (staff[0][1] - (distance / 2) )), closeness):
            return "F5"
        if not checkDistance_point(body_loc, (body_loc[0], staff[0][1]), closeness):
            return "E5"
        if not checkDistance_point(body_loc, (body_loc[0], (staff[0][1] + distance / 2) ), closeness):
            return "D5"
        if not checkDistance_point(body_loc, (body_loc[0], staff[1][1]), closeness):
            return "C5"
        distance = staff[2][1] - staff[1][1]
        if not checkDistance_point(body_loc, (body_loc[0], (staff[1][1] + distance / 2) ), closeness):
            return "B4"
        if not checkDistance_point(body_loc, (body_loc[0], staff[2][1]), closeness):
            return "A4"
        distance = staff[3][1] - staff[2][1]
        if not checkDistance_point(body_loc, (body_loc[0], (staff[2][1] + distance / 2) ), closeness):
            return "G4"
        if not checkDistance_point(body_loc, (body_loc[0], staff[3][1]), closeness):
            return "F4"
        distance = staff[4][1] - staff[3][1]
        if not checkDistance_point(body_loc, (body_loc[0], (staff[3][1] + distance / 2) ), closeness):
            return "E4"
        if not checkDistance_point(body_loc, (body_loc[0], staff[4][1]), closeness):
            return "D4"

def Determine_Note(line_list, structured_notation_list, image, threshold):

    newList = []

    for bar in structured_notation_list:
        newBar = []
        for notation in bar:
            
            notation = list(notation)

            if (notation[1] == "quarter note") or (notation[1] == "eighth note") or (notation[1] == "sixteen note"):
            
                #determine where body of note is using template matching
                template = cv.imread("./data/templates/Determine_Note_Template.png", cv.IMREAD_GRAYSCALE)
                template_w, template_h = template.shape[::-1]
                roi = image[(notation[0][1] - 5): (notation[0][1] + notation[2][1] + 5), (notation[0][0] - 5): (notation[0][0] + notation[2][0] + 5)]
                res = cv.matchTemplate(roi,template,cv.TM_CCOEFF_NORMED)
                loc = np.where( res >= threshold)

                pt_list = []
                for pt in zip(*loc[::-1]):
                    if checkDistance(pt_list, pt, 300):
                        pt_list.append(pt)

                #location of body_loc is on top left of body
                body_loc = ((notation[0][0] + pt_list[0][0]), (notation[0][1] + pt_list[0][1]))

                note = musical_note(body_loc, line_list, 7)
                notation.append(note)
                notation = tuple(notation)            

            
            elif (notation[1] == "whole note"):
                
                #location of body_loc is on top left of body
                body_loc = (notation[0][0], (notation[0][1] + 8))

                note = musical_note(body_loc, line_list, 7)
                notation.append(note)
                notation = tuple(notation)  
                 

            elif (notation[1] == "half note"):

                #location of body_loc is on top left of body
                body_loc = (notation[0][0], (notation[0][1] + 11))

                note = musical_note(body_loc, line_list, 7)
                notation.append(note)
                notation = tuple(notation)
                
            newBar.append(notation)
        
        newList.append(newBar)

    return newList           



