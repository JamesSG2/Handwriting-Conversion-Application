import cv2
import pytesseract
import os

# imports a test image I scaned of my handwriting
name = 'trevor'
target = 'pangram.png'
original = cv2.imread('data\\' + name + '\\' + target, cv2.IMREAD_GRAYSCALE)
try:
    os.makedirs('output\\' + name + '\\char')
except OSError:
    pass

# does some filtering to improve quality
# more research needed to find most efective filters for use case
resized = cv2.resize(original, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
img = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# get dimensions of image
h, w = img.shape

# get boundary boxes on each character identified
boxes = pytesseract.image_to_boxes(img)
# loop through boxes
i = [0] * 27
for b in boxes.splitlines():
    # break output into array
    b = b.split(' ')
    # add boxes to main image
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    # create and save a cropped image of each character
    cropped = resized[h-int(b[4]):h-int(b[2]),int(b[1]):int(b[3])]

    char_num = ord(b[0])-96
    if((char_num>0) and (char_num<27)):
        i[char_num] += 1
        try:
            os.makedirs('output\\' + name + '\\char\\' + b[0])
        except OSError:
            pass
        location = 'output\\' + name + '\\char\\' + b[0] + '\\' + str(i[char_num]) + '.png'
        cv2.imwrite(location, cropped)


# save text file
with open('output\\' + name + '\\pangram.txt', mode ='w') as file:
    file.write(boxes)
    file.close()
# show full image with boxes
cv2.imshow("full",img)
cv2.waitKey(0)
print("done")
