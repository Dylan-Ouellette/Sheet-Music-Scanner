import math

def checkDistance(coordinates, new_coordinate, min_distance):
    for existing_coordinate in coordinates:
        if math.dist(existing_coordinate, new_coordinate) < min_distance:
            return False
    return True

def checkCollision_List (pt, pt_w, pt_h, list, list_element_w, list_element_h):
    for element_pt in list:
        if ((pt[0] < (element_pt[0] + list_element_w)) and ((pt[0] + pt_w) > element_pt[0]) and (pt[1] < (element_pt[1] + list_element_h)) and ((pt[1] + pt_h) > element_pt[1])):
                return True
    return False

def checkCollision_Point (pt1, pt1_w, pt1_h, pt2, pt2_w, pt2_h):
    if ((pt1[0] < (pt2[0] + pt2_w)) and ((pt1[0] + pt1_w) > pt2[0]) and (pt1[1] < (pt2[1] + pt2_h)) and ((pt1[1] + pt1_h) > pt2[1])):
        return True
    return False