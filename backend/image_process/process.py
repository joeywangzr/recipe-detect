import cv2
import numpy as np

def crop_flyer(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    copy = img.copy()
    for index, c in enumerate(contours[0]):
        (x,y,w,h) = cv2.boundingRect(c)
        min_x, max_x = x, x+w
        min_y, max_y = y, y+h
        cropped_flyer = img[min_y:max_y, min_x:max_x]
        # cv2.imwrite(f"./cropped-flyers/cropped_flyer.jpg", cropped_flyer)

    # img = cv2.imread('./cropped-flyers/cropped_flyer.jpg')
    img = cropped_flyer

    height, width, _ = cropped_flyer.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray,127,255,cv2.THRESH_TOZERO)

    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    copy = img.copy()
    min_area = 100000

    counter = 0
    for index, c in enumerate(contours[0]):
        area = cv2.contourArea(c)
        if area > min_area:
            approx = cv2.approxPolyDP(c,1,True)
            if len(approx) < 200:
                (x,y,w,h) = cv2.boundingRect(c)
                min_x, max_x = x, x+w
                min_y, max_y = y, y+h
                cropped_image = img[min_y:max_y, min_x:max_x]
                
                cv2.imwrite(f"./grocery/crop_{counter}.jpg", cropped_image)

                cv2.drawContours(copy, [c], -1, (0, 255, 0), thickness=cv2.FILLED)
                
                counter += 1

crop_flyer('./flyers/flyer8.png')
# cv2.imwrite("box_found.png", copy)
# cv2.waitKey(0)
