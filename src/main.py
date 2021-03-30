import cv2
import pytesseract
import os
import re

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



def analyze_sample(name, target):
    # create output files
    os.chdir("..")
    original = cv2.imread('data\\' + name + '\\' + target + '.png')
    try:
        with open('data\\' + name + '\\' + target + '.txt') as file:
            text_contents = file.read()
            text_contents = re.sub(r"\s", "", text_contents)
            file.close()
    except FileNotFoundError:
        print("Couldn't find text file. Will not spellcheck.")
        text_contents = ""

    try:
        os.makedirs('output\\' + name + '\\char')
    except OSError:
        pass

    # does some filtering to improve quality and gets dimensions
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    h, w = img.shape

    # create 2D list and string for storing characters and bounding boxes
    text_array = []
    text_string = ""
    for b in pytesseract.image_to_boxes(img).splitlines():
        # make each line into a list and place in the 2D list
        b = b.split(' ')
        text_array.append(b)
        text_string += b[0]

    # run text correction and show before and after
    print(text_string)
    text_string = new_full_correction(text_string, text_contents)
    print(text_string)

    # save output string as text file
    with open('output\\' + name + '\\' + target + '.txt', mode ='w') as file:
        file.write(text_string)
        file.close()

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

    # save images in image list avoiding duplicates by appending a number
    for i in image_list:
        # try to create output folder
        try:
            os.makedirs('output\\' + name + '\\char\\' + i[1])
        except OSError:
            pass
        # check how many images are already in folder
        char_count = len(os.listdir('output\\' + name + '\\char\\' + i[1]))
        # save the image with the number of images already in the folder appended to avoid duplicates
        location = 'output\\' + name + '\\char\\' + i[1] + '\\' + i[1] + "_" + str(char_count) + '.png'
        cv2.imwrite(location, i[0])


    # cv2.imshow("full", img)
    # cv2.waitKey(0)
    return True

# imports a test image I scaned of my handwriting
print("Name: ")
name = input()
print("Image sample: ")
target = input()

analyze_sample(name, target)
