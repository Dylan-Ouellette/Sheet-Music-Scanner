
import numpy as np
import cv2 as cv


def findScale(fileName):
    img = cv.imread(fileName, 0)
    hSum = getHorizontalSum(img)
    scale = 0
    factor = 0 # Used to increase a threshold if a staff is't detected

    while scale == 0 and factor < 0.8:
        scale = getStaffScale(hSum, factor)
        factor += 0.1

    return scale


def getHorizontalSum(img):
    rightMargen = getRightMargen(img)

    # Takes a small vertical slice of the image starting at the right hand
    # margen and 1% of total width to the left of that.
    img = img[:, (rightMargen - int(len(img[0]) * 1/100)):rightMargen]

    return img.sum(axis=1, dtype='int')/len(img)


def getRightMargen(img):
    vSum = img.sum(axis=0, dtype='int')
    
    # Finds the location where staff starts by checking the change in
    # brightness from right to left.
    i = len(vSum) - 1
    while i > 0:
        if vSum[i] - vSum[i - 1] > 0.05 * np.max(vSum):
            return i
        i = i - 1

    # Default return
    return len(vSum) - 1


def getStaffScale(hSum, lineFactor):
    # Checks if the space between lines one and two, is the same as two and three.
    def sameSpace(one, two, three):
        if one - two == two - three:
            return True
        if -2 < (one - two) - (two - three) < 2:
            return True
        return False
    

    cutoff = np.average(hSum) - lineFactor * np.max(hSum)
    lineCount = 0
    lineLocation = [0, 0, 0, 0, 0]
    whiteSpace = True

    # Finds the first set of five lines that are equildistant to each other.
    for i in range(0, len(hSum)):
        if hSum[i] < cutoff:
            if not whiteSpace:
                pass
            elif lineCount < 2:
                lineLocation[lineCount] = i
                lineCount += 1
            elif sameSpace(i, lineLocation[lineCount - 1], lineLocation[lineCount - 2]):
                lineLocation[lineCount] = i
                lineCount += 1
            else:
                lineLocation[0] = lineLocation[lineCount - 1]
                lineLocation[1] = i
                lineCount = 2

            if lineCount == 5:
                return lineLocation[4] - lineLocation[0]
            
            whiteSpace = False
        else:
            whiteSpace = True

    # Default return
    return 0


def main():
    print(findScale("./data/images/Scan1.jpg"))
    print(findScale("./data/images/example01.png"))
    print(findScale("./data/images/TempTestSheet.png"))

    return 0


if __name__ == '__main__':
    main()