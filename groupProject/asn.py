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
       
    
def resize_image(input, output, size=(4500, 4500)):
    with Image.open(input) as img:
        resized_img = img.resize(size)
        resized_img.save(output)



# resize
resize_image('MozartTrio.png', 'ResizedExample03.png')  

# Read the resized image
resized_img = cv2.imread('ResizedExample03.png')

# remove function
removeLine(resized_img, 6, 'FinalImage.png')  
    
    
# detection

def detectionRest(png, template, thresholdVal, output):
    img_rgb = png
    assert img_rgb is not None, "file could not be read, check with os.path.exists()"
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    temp = template
    assert temp is not None, "file could not be read, check with os.path.exists()"
    w, h = temp.shape[::-1]
    res = cv2.matchTemplate(img_gray,temp,cv2.TM_CCOEFF_NORMED)
    threshold = thresholdVal
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imwrite(output,img_rgb)



img = cv2.imread('FinalImage.png')
template = cv2.imread('img/rest03.png', cv2.IMREAD_GRAYSCALE)
detectionRest(img, template, 0.52,'rest03.png'), 




    
