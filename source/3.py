import cv2
import numpy as np

img = cv2.imread(r'../resource/sc.png')
template = cv2.imread(r'../resource/123.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
res = cv2.matchTemplate(mask, template, cv2.TM_SQDIFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = min_loc
h, w = template.shape[:2]
bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
cv2.imshow('result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
