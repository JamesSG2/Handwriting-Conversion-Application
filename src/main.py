import cv2
import pytesseract
import os
import re
import numpy as np

#remove this comment later
# corrects errors in tesseract data using regex
def new_full_correction(text_to_correct, correct_text):
    correct_text = correct_text*2
    if(correct_text.islower()):
        text_to_correct = text_to_correct.lower()
    elif(correct_text.isupper()):
        text_to_correct = text_to_correct.upper()

    for k in range(2,5):
        patterns = []
        for h in range(int(float(len(correct_text))/2)):
            replacement = r"\w" * k
            segment = correct_text[h:h+(3*k)]
            search = segment[0:k] + replacement + segment[(2*k): ]
            patterns.append(search)
            patterns.append(segment)
        for p in range(0, len(patterns), 2):
            text_to_correct = re.sub(patterns[p], patterns[p+1], text_to_correct)
        # print(str(k) + ":" + text_to_correct)
    return text_to_correct

def punctuation_analysis(img, text_contents):
    print(text_contents)
    # use hsv colorspace
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([20,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([160,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    mask = mask0 + mask1

    # expand mask
    final_kernel = np.ones((4,4), np.uint8)
    dialated = cv2.dilate(mask,final_kernel,iterations=1)

    # remove red
    newmask = cv2.cvtColor(dialated, cv2.COLOR_GRAY2BGR)
    cleaned = cv2.add(img, newmask)

    # find contours
    contours_full, hierarchy = cv2.findContours(dialated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = contours_full[::2]

    # place a bounding box around each contour
    boundRect = [None]*len(contours)
    for i, c in enumerate(contours):
        boundRect[i] = cv2.boundingRect(contours[i])
    boundRect.sort()

    # crop boxes and save
    image_list = []
    for i in range(len(contours)):
        cropped = cleaned[int(boundRect[i][1]):int(boundRect[i][1]+boundRect[i][3]),int(boundRect[i][0]):int(boundRect[i][0]+boundRect[i][2])]
        ordinal = "ord_" + str(ord(text_contents[i]))
        storage_list = [cropped, ordinal]
        image_list.append(storage_list)

    # add bounding boxes to img
    for i in range(len(contours)):
        color = (0, 0, 0)
        cv2.rectangle(cleaned, (int(boundRect[i][0]), int(boundRect[i][1])), \
            (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)

    return cleaned, image_list

def character_analysis(img, text_contents):
    # make image binary and scale up
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    threshold = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    h, w, = threshold.shape

    # create 2D list and string for storing characters and bounding boxes
    text_array = []
    text_string = ""
    pytesseract_list = pytesseract.image_to_boxes(threshold).splitlines()
    for b in pytesseract_list:
        # make each line into a list and place in the 2D list
        b = b.split(' ')
        text_array.append(b)
        text_string += b[0]

    # run text correction and show before and after
    print(text_string)
    text_string = new_full_correction(text_string, text_contents)
    print("Corrected to:")
    print(text_string)

    # store cropped images in list with their character
    image_list = []
    for i in range(len(text_array)):
        # crop the image based on tesseract bounding boxes
        cropped = resized[h-int(text_array[i][4]):h-int(text_array[i][2]),int(text_array[i][1]):int(text_array[i][3])]
        # get the unicode number of the character and check if it is a letter
        char_num = ord(text_array[i][0])
        if(((char_num>=65) and (char_num<=90)) or ((char_num>=97) and (char_num<=122))):
            # store cropped image and it's character in a nested list
            storage_list = [cropped, text_string[i]]
            image_list.append(storage_list)

    return resized, image_list

def analyze_sample(name, target):
    # open image
    os.chdir("..")
    original = cv2.imread('data\\' + name + '\\' + target + '.png')

    # open text
    try:
        with open('data\\' + name + '\\' + target + '.txt') as file:
            text_contents = file.read()
            text_contents = re.sub(r"\s", "", text_contents)
            file.close()
    except FileNotFoundError:
        print("Couldn't find text file. Will not spellcheck.")
        text_contents = ""

    print("Analyzing: " + target + " from " + name)
    print("Expect to find:")
    print(text_contents)
    print("Found:")

    # run correct analysis
    if("punctuation" in target):
        img, image_list = punctuation_analysis(original, text_contents)
    else:
        img, image_list = character_analysis(original, text_contents)

    # save images in image list avoiding duplicates by appending a number
    for i in image_list:
        # try to create output folder
        try:
            os.makedirs('output\\' + name + '\\' + i[1])
        except OSError:
            pass
        # check how many images are already in folder
        char_count = len(os.listdir('output\\' + name + '\\' + i[1]))
        # save the image with the number of images already in the folder appended to avoid duplicates
        location = 'output\\' + name + '\\' + i[1] + '\\' + i[1] + "_" + str(char_count) + '.png'
        cv2.imwrite(location, i[0])

    print("Saved")
    return img

# imports a test image I scaned of my handwriting
print("Name: ")
name = input()
print("Image sample: ")
target = input()

img = analyze_sample(name, target)
cv2.imshow("full", img)
cv2.waitKey(0)
print("Done")
