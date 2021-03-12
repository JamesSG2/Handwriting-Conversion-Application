import cv2
import pytesseract

img = cv2.imread('quote.jpeg')

img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

result = pytesseract.image_to_string(img, lang="eng")
with open('result.txt', mode ='w') as file:
    file.write(result)
    print(result)

h, w = img.shape
boxes = pytesseract.image_to_boxes(img) 
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    
cv2.imshow('img', img)
cv2.waitKey(0)