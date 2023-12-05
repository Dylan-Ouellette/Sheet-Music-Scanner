from Classification_Functions import checkCollision_Point

def Structure_Data(full_notation_list, Barbox_list):

    #restructures Barbox_list so it's no longer seperated by staffs
    newList = []
    for i in range (0, len(Barbox_list)):
        newList.extend(Barbox_list[i])
    Barbox_list = newList

    final_notation_list = []

    for Barbox in Barbox_list:

        BarNotations = []

        for notation in full_notation_list:
            if checkCollision_Point(notation[0], notation[2][0], notation[2][1], Barbox[0], (Barbox[1][0] - Barbox[0][0]), (Barbox[1][1] - Barbox[0][1])):
                BarNotations.append(notation)
        
        if BarNotations:
            final_notation_list.append(sorted(BarNotations, key = lambda k: [k[0][0]]))

    return final_notation_list
