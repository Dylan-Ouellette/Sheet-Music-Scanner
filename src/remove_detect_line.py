import cv2
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np




def removeLine(image, value, output):
    
    img = image
    val = value
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bw_gray = cv2.bitwise_not(gray)
    
    #only remove line 
    binary_src = cv2.adaptiveThreshold(bw_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    hline = cv2.getStructuringElement(cv2.MORPH_RECT, (int(img.shape[1] / 16), 1), (-1, -1))
    dst = cv2.morphologyEx(binary_src, cv2.MORPH_OPEN, hline)
    dst = cv2.bitwise_not(dst)    
    cv2.imshow("RemoveLine", dst)
    cv2.imwrite("removeLine.png", dst)
    
    _, threshold_gray = cv2.threshold(bw_gray, 100, 255, cv2.THRESH_BINARY)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, val))
    vertical = cv2.morphologyEx(threshold_gray, cv2.MORPH_OPEN, vertical_kernel)
    vertical_inverted = cv2.bitwise_not(vertical)
    plt.imshow(vertical_inverted, cmap='gray')
    plt.title('final image')
    plt.show()
    cv2.imwrite(output, vertical_inverted)
       
def detectionLine(img): 
    image = cv2.imread(img)
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Binary threshold
    _, binary_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detected_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    #Second, process edge detection use Canny.
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(detected_lines, low_threshold, high_threshold)
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 1000  # minimum number of pixels making up a line
    max_line_gap = 250  # maximum gap in pixels between connectable line segments
    line_image = np.copy(image) * 0  # creating a blank to draw lines on
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
    newtup = ()
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image,(x1,y1),(x2,y2 ),(255,0,0),5)
            newtup+=('Coordinates of line:', 'Start point',(x1, y1), 'End point',(x2, y2))
    for i in newtup:
        print(i)

       














    
