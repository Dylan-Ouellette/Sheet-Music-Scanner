from find_scale import scaleImage
from Treble_Classification import Treble_Classification
from Bass_Classification import Bass_Classification
from BarLine_Classification import BarLine_Classification
from CreateBarBoxes import CreateBarBoxes
from node_recognition_output import note_recognition
from Structure_Data import Structure_Data
import cv2 as cv

def removeLine(image, value, output):
    img = image
    val = value
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bw_gray = cv.bitwise_not(gray)
    _, threshold_gray = cv.threshold(bw_gray, 100, 255, cv.THRESH_BINARY)
    vertical_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, val))
    vertical = cv.morphologyEx(threshold_gray, cv.MORPH_OPEN, vertical_kernel)
    vertical_inverted = cv.bitwise_not(vertical)
    cv.imwrite(output, vertical_inverted)

def main():
    testImage = "./data/images/TempTestSheet.png"
    
    scaleImage(testImage, "./data/images/rescaleOutput.png")
    
    removeLine(cv.imread('./data/images/rescaleOutput.png'), 10, './data/images/removeLineOutput.png')

    img_rgb = cv.imread('./data/images/removeLineOutput.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    treble_list = Treble_Classification(img_gray, img_rgb, './data/templates/treble.png', 0.5)
    bass_list = Bass_Classification(img_gray, img_rgb, './data/templates/bass.png', 0.5)
    barline_list = BarLine_Classification(img_gray, img_rgb, './data/templates/vertical_line.png', 0.8)
    
    barline_w, barline_h = (cv.imread('./data/templates/vertical_line.png', cv.IMREAD_GRAYSCALE)).shape[::-1]

    barbox_list = CreateBarBoxes(treble_list, bass_list, barline_list, barline_w, barline_h, img_gray, img_rgb)

    notation_list = note_recognition('./data/images/removeLineOutput.png')

    for element in notation_list:
        cv.rectangle(img_rgb, element[0], (element[0][0] + element[2][0], element[0][1] + element[2][1]), (100,100,100), 2)
        cv.putText(img_rgb, element[1], element[0], cv.FONT_HERSHEY_SIMPLEX, 0.8, (10,169,21), 2)

    cv.imwrite('./data/images/testOutput.png', img_rgb)

    structured_notation_list = Structure_Data((treble_list + bass_list + notation_list), barbox_list)

    print(structured_notation_list[6])

    return 0


if __name__ == '__main__':
    main()