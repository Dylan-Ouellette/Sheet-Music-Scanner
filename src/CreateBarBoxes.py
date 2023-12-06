import cv2 as cv

def CreateBarBoxes (treble_list, bass_list, BarLine_list, BarLine_w, BarLine_h, img_gray, img_rgb):

    page_length, page_width = img_gray.shape

    treble_pt_list = []
    for treble in treble_list:
        treble_pt_list.append(treble[0])

    bass_pt_list = []
    for bass in bass_list:
        bass_pt_list.append(bass[0])

    barline_pt_list = []
    for barline in BarLine_list:
        barline_pt_list.append(barline[0])

    clef_lines_list = []

    #sort the clefs in order by y
    clef_pt_list = sorted(treble_pt_list + bass_pt_list, key = lambda k: [k[1]])

    #creates list of lists where each list represents a staff and in the list are the coresponding clef and vertical line points
    for clef_pt in clef_pt_list:
        staff_clef_lines = []
        staff_clef_lines.append(clef_pt)
        for line_pt in barline_pt_list:
            if abs(clef_pt[1] - line_pt[1]) < 200:
                staff_clef_lines.append(line_pt)
        
        clef_lines_list.append(staff_clef_lines)

    #sorts each list in order by x
    newList = []
    for staff_dividers in clef_lines_list:
        newList.append(sorted(staff_dividers, key = lambda k: [k[0]]))
    clef_lines_list = newList

    #creates a list of lists where each list represents a staff and holds the boxes to represent each bar
    barBox_list = []
    for staff_dividers in clef_lines_list:
        
        staff_barBoxes = []
        for i in range(0, len(staff_dividers) - 1):
            
            staff_barBoxes.append(((staff_dividers[i][0] + BarLine_w, staff_dividers[i][1] - 100),
                                   (staff_dividers[i + 1][0], staff_dividers[i + 1][1] + BarLine_h + 100))) #also stretches the boxes vertically by 100 pixels

            if i == (len(staff_dividers) - 2):
                staff_barBoxes.append(((staff_dividers[i + 1][0] + BarLine_w, staff_dividers[i + 1][1] - 20),
                                       (page_width, staff_dividers[i + 1][1] + BarLine_h + 20)))

        barBox_list.append(staff_barBoxes)    

    #draws rectangles
    for staff in barBox_list:
        for barBox in staff:
            cv.rectangle(img_rgb, barBox[0], barBox[1], (0,0,0), 2)

    return barBox_list