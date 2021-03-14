import cv2
import pytesseract

#imports a test image I scaned of my handwriting
img = cv2.imread('test.png', cv2.IMREAD_GRAYSCALE)

#does some filtering to improve quality
#more research needed to find most efective filters for use case
img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
img = cv2.bilateralFilter(img,9,75,75)

# get dimensions of image
h, w = img.shape

#get boundary boxes on each character identified
boxes = pytesseract.image_to_boxes(img)
print(boxes)
#loop through boxes
for b in boxes.splitlines():
    #break output into array
    b = b.split(' ')
    #add boxes to main image
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    #create and show a cropped image of each character
    cropped = img[h-int(b[4]):h-int(b[2]),int(b[1]):int(b[3])]
    cv2.imshow(b[0], cropped)

#show full image with boxes
cv2.imshow("full",img)
cv2.waitKey(0)
