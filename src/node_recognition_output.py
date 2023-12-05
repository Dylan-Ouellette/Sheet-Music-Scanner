import cv2 as cv
import numpy as np
from Classification_Functions import checkDistance, checkDistance_point, checkCollision_List
from remove_detect_line import detectionLine

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
                output_list.append(((pt[0], pt[1]), name, (w, h)))
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
                output_list.append(((x, y), name, (w, h)))
                found.add((x, y))  # Store the first coordinate of the match

    return output_list

"""# time signatures"""

def time_signiture(input_image):# 'FinalImage.png'
  time_signiture_list = []
  match_template_and_store(time_signiture_list, input_image, ['./data/templates/44c.png'], '4/4c time', 0.85) #threshold = 0.9-0.95
  match_template_and_store(time_signiture_list, input_image, ['./data/templates/22.png'], '2/2c time', 0.85) #threshold = 0.8-0.9
  match_template_and_store(time_signiture_list, input_image, ['./data/templates/24.png'], '2/4 time', 0.85) #threshold = 0.9-0.95
  match_template_and_store(time_signiture_list, input_image, ['./data/templates/34.png'], '3/4 time', 0.85) #threshold = 0.9-0.95
  match_template_and_store(time_signiture_list, input_image, ['./data/templates/38.png'], '3/8 time', 0.85) #threshold = 0.9-0.95
  match_template_and_store(time_signiture_list, input_image, ['./data/templates/44.png'], '4/4 time', 0.85) #threshold = 0.8-0.95
  match_template_and_store(time_signiture_list, input_image, ['./data/templates/68.png'], '6/8 time', 0.85) #threshold = 0.8-0.95
  return time_signiture_list

"""# clefs"""

def clefs(input_image):# 'FinalImage.png'
  clef_list = []
  match_template_and_store(clef_list, input_image, ['./data/templates/treble.png'], 'treble', 0.7) #threshold = 0.5-0.9
  match_template_and_store(clef_list, input_image, ['./data/templates/bass.png'], 'bass', 0.7) #threshold = 0.5-0.9
  return clef_list

"""# accidentals"""

def accidentals(input_image):# 'FinalImage.png'
  accidental_list = []
  match_no_collision_check(accidental_list, input_image, ['./data/templates/sharp.png'], 'sharp', 0.7) #threshold = 0.6-0.7
  match_no_collision_check(accidental_list, input_image, ['./data/templates/flat.png'], 'flat', 0.7) #threshold = 0.6-0.7
  match_no_collision_check(accidental_list, input_image, ['./data/templates/natual.png'], 'natual', 0.7) #threshold = 0.7-0.8
  return accidental_list

"""#rests"""

def rests(line_list, input_image):# 'FinalImage.png'

  rest_list = []
  match_template_and_store(rest_list, input_image, ['./data/templates/whole half rest.png'], 'whole half rest', 0.9) #threshold = 0.8-0.95

  #differentiate between whole rests and half rests
  newList = []
  for WholeHalf_rest in rest_list:
    WholeHalf_rest = list(WholeHalf_rest)
    for staff in line_list:
        #check if rest is in close proximity to line, add 20 to adjust for template
        if not checkDistance_point((WholeHalf_rest[0][0], staff[1][1]), (WholeHalf_rest[0][0], WholeHalf_rest[0][1] + 20), 50):
            #check if rest is touching line
            if not checkDistance_point((WholeHalf_rest[0][0], staff[1][1]), (WholeHalf_rest[0][0], WholeHalf_rest[0][1] + 20), 5):
              WholeHalf_rest[1] = "whole rest"
            else:
              WholeHalf_rest[1] = "half rest"
    newList.append(tuple(WholeHalf_rest))    
  rest_list = newList   

  match_template_and_store(rest_list, input_image, ['./data/templates/quarter rest.png'], 'quarter rest', 0.7) #threshold = 0.6-0.9
  match_template_and_store(rest_list, input_image, ['./data/templates/eighth rest.png'], 'eighth rest', 0.82) #threshold = 0.7-0.9
  match_no_collision_check(rest_list, input_image, ['./data/templates/sixteenth rest.png'], 'sixteenth rest', 0.7) #threshold = 0.7-0.9
  return rest_list

"""#notes"""

def notes(input_image):# 'FinalImage.png'
  note_list = []
  match_template_and_store(note_list, input_image, ['./data/templates/sixteen note.png'], 'sixteen note', 0.80)
  match_template_and_store(note_list, input_image, ['./data/templates/sixteen note1l.png', './data/templates/sixteen note1r.png', './data/templates/sixteen note2l.png', './data/templates/sixteen note2r.png'], 'sixteen note', 0.74) #threshold = 0.7
  match_template_and_store(note_list, input_image, ['./data/templates/eighth note.png'], 'eighth note', 0.80)
  match_template_and_store(note_list, input_image, ['./data/templates/eighth note1l.png', './data/templates/eighth note1r.png', './data/templates/eighth note2l.png', './data/templates/eighth note2r.png'], 'eighth note', 0.83) #threshold = 0.8

  match_template_and_store(note_list, input_image, ['./data/templates/whole note.png'], 'whole note', 0.7) #threshold = 0.7-0.9
  match_template_and_store(note_list, input_image, ['./data/templates/half note.png'], 'half note', 0.75) #threshold = 0.8-0.85
  match_template_and_store(note_list, input_image, ['./data/templates/quarter note1.png', './data/templates/quarter note2.png'], 'quarter note', 0.85) #threshold = 0.9

  return note_list

"""#note_recognition output"""

def note_recognition(line_list, input_image):# 'FinalImage.png'
  note_recognition_result = []
  time_signiture_list = time_signiture(input_image)
  #clef_list = clefs(input_image)
  accidental_list = accidentals(input_image)
  rest_list = rests(line_list, input_image)
  note_list = notes(input_image)

  note_recognition_result.extend(time_signiture_list)
  #note_recognition_result.extend(clef_list)
  note_recognition_result.extend(accidental_list)
  note_recognition_result.extend(rest_list)
  note_recognition_result.extend(note_list)
  return note_recognition_result

