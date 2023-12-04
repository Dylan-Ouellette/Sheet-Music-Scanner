import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math

def checkDistance(coordinates, new_coordinate, min_distance):
    for existing_coordinate in coordinates:
        if math.dist(existing_coordinate, new_coordinate) < min_distance:
            return False
    return True

def checkCollision_List(pt, pt_w, pt_h, lst, list_element_w, list_element_h):
    for element_pt in lst:
        if (
            (pt[0] < (element_pt[0] + list_element_w))
            and ((pt[0] + pt_w) > element_pt[0])
            and (pt[1] < (element_pt[1] + list_element_h))
            and ((pt[1] + pt_h) > element_pt[1])
        ):
            return True
    return False

def match_template_and_store(output_list, image_path, templates, name, threshold):
    img_rgb = cv.imread(image_path)
    assert img_rgb is not None, f"File {image_path} could not be read, check with os.path.exists()"
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    for template_name in templates:
        template = cv.imread(template_name, cv.IMREAD_GRAYSCALE)
        assert template is not None, f"File {template_name} could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            # Check distance and collision before appending
            if (
                checkDistance([coord[0] for coord in output_list], pt, 10)
                and not checkCollision_List(
                    pt, w, h, [coord[0] for coord in output_list], w, h
                )
            ):
                output_list.append(((pt[0], pt[1]), name, None))
                cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    #cv.imwrite(f'{name}_matched.png', img_rgb)

    return output_list




def match_no_collision_check(output_list, image_path, template_names, name, threshold):
    img_rgb = cv.imread(image_path)
    assert img_rgb is not None, f"File {image_path} could not be read, check with os.path.exists()"
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    for template_name in template_names:
        template = cv.imread(template_name, cv.IMREAD_GRAYSCALE)
        assert template is not None, f"File {template_name} could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        found = set()  # To store unique matches

        for pt in zip(*loc[::-1]):
            x, y = pt[0], pt[1]
            # Check if the coordinate is part of a new match
            if all((x - x0) ** 2 + (y - y0) ** 2 > 100 for x0, y0 in found):
                output_list.append(((x, y), name, None))
                found.add((x, y))  # Store the first coordinate of the match

    return output_list

"""# time signatures"""

def time_signiture(input_image):# 'FinalImage.png'
  time_signiture_list = []
  match_template_and_store(time_signiture_list, input_image, ['44c.png'], '4/4c time', 0.95) #threshold = 0.9-0.95
  match_template_and_store(time_signiture_list, input_image, ['22.png'], '2/2c time', 0.95) #threshold = 0.8-0.9
  match_template_and_store(time_signiture_list, input_image, ['24.png'], '2/4 time', 0.95) #threshold = 0.9-0.95
  match_template_and_store(time_signiture_list, input_image, ['34.png'], '3/4 time', 0.95) #threshold = 0.9-0.95
  match_template_and_store(time_signiture_list, input_image, ['38.png'], '3/8 time', 0.95) #threshold = 0.9-0.95
  match_template_and_store(time_signiture_list, input_image, ['44.png'], '4/4 time', 0.9) #threshold = 0.8-0.95
  match_template_and_store(time_signiture_list, input_image, ['68.png'], '6/8 time', 0.9) #threshold = 0.8-0.95
  return time_signiture_list

"""# clefs"""

def clefs(input_image):# 'FinalImage.png'
  clef_list = []
  match_template_and_store(clef_list, input_image, ['treble.png'], 'treble', 0.7) #threshold = 0.5-0.9
  match_template_and_store(clef_list, input_image, ['bass.png'], 'bass', 0.7) #threshold = 0.5-0.9
  return clef_list

"""# accidentals"""

def accidentals(input_image):# 'FinalImage.png'
  accidental_list = []
  match_no_collision_check(accidental_list, input_image, ['sharp.png'], 'sharp', 0.7) #threshold = 0.6-0.7
  match_no_collision_check(accidental_list, input_image, ['flat.png'], 'flat', 0.7) #threshold = 0.6-0.7
  match_no_collision_check(accidental_list, input_image, ['natual.png'], 'natual', 0.7) #threshold = 0.7-0.8
  return accidental_list

"""#rests



"""

def rests(input_image):# 'FinalImage.png'
  rest_list = []
  match_template_and_store(rest_list, input_image, ['whole half rest.png'], 'whole half rest', 0.9) #threshold = 0.8-0.95
  match_template_and_store(rest_list, input_image, ['quarter rest.png'], 'quarter rest', 0.7) #threshold = 0.6-0.9
  match_template_and_store(rest_list, input_image, ['eighth rest.png'], 'eighth rest', 0.7) #threshold = 0.7-0.9
  match_no_collision_check(rest_list, input_image, ['sixteenth rest.png'], 'sixteenth rest', 0.7) #threshold = 0.7-0.9
  return rest_list

"""#notes"""

def notes(input_image):# 'FinalImage.png'
  note_list = []
  match_template_and_store(note_list, input_image, ['whole note.png'], 'whole note', 0.7) #threshold = 0.7-0.9
  match_template_and_store(note_list, input_image, ['half note.png'], 'half note', 0.8) #threshold = 0.8-0.85
  match_template_and_store(note_list, input_image, ['quarter note1.png', 'quarter note2.png'], 'quarter note', 0.9) #threshold = 0.9

  match_template_and_store(note_list, input_image, ['eighth note1l.png', 'eighth note1r.png', 'eighth note2l.png', 'eighth note2r.png','eighth note.png'], 'eighth note', 0.8) #threshold = 0.8
  match_template_and_store(note_list, input_image, ['sixteen note1l.png', 'sixteen note1r.png', 'sixteen note2l.png', 'sixteen note2r.png','sixteen note.png'], 'sixteen note', 0.7) #threshold = 0.7
  return note_list

"""#note_recognition output"""

def note_recognition(input_image):# 'FinalImage.png'
  note_recognition_result = []
  time_signiture_list = time_signiture(input_image)
  clef_list = clefs(input_image)
  accidental_list = accidentals(input_image)
  rest_list = rests(input_image)
  note_list = notes(input_image)

  note_recognition_result.extend(time_signiture_list)
  note_recognition_result.extend(clef_list)
  note_recognition_result.extend(accidental_list)
  note_recognition_result.extend(rest_list)
  note_recognition_result.extend(note_list)
  return note_recognition_result


list = note_recognition('FinalImage.png')
for result in list:
  print(result)
