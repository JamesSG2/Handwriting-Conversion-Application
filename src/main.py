import cv2
import pytesseract
import os
import re

def analyze_sample(name, target):

    # create output files
    os.chdir("..")
    original = cv2.imread('data\\' + name + '\\' + target + '.png', cv2.IMREAD_GRAYSCALE)
    try:
        with open('data\\' + name + '\\' + target + '.txt') as file:
            text_contents = file.read()
            text_contents = re.sub(r"\s", "", text_contents)
            # text_contents = text_contents + text_contents[0:4]
            file.close()
    except FileNotFoundError:
        print("Couldn't find text file. Will not spellcheck.")
        text_contents = ""

    try:
        os.makedirs('output\\' + name + '\\char')
    except OSError:
        pass

    # does some filtering to improve quality and gets dimensions
    resized = cv2.resize(original, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
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

    print(text_string)
    text_string = new_full_correction(text_string, text_contents)
    print(text_string)

    # save output string as text file
    with open('output\\' + name + '\\' + target + '.txt', mode ='w') as file:
        file.write(text_string)
        file.close()

    # save each character as a labled image
    box_counter = 0
    for b in text_array:
        # add boxes to main image
        # img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
        # use the corrected text
        b[0] = text_string[box_counter]
        box_counter += 1

        # create and save a cropped image of each character
        cropped = resized[h-int(b[4]):h-int(b[2]),int(b[1]):int(b[3])]

        # convert text to unicode and create folders for each letter
        char_num = ord(b[0])
        if(((char_num>=65) and (char_num<=90)) or ((char_num>=97) and (char_num<=122))):
            try:
                os.makedirs('output\\' + name + '\\char\\' + b[0])
            except OSError:
                pass

            # write image to output file and increment counter
            char_count = len(os.listdir('output\\' + name + '\\char\\' + b[0]))
            location = 'output\\' + name + '\\char\\' + b[0] + '\\' + b[0] + "_" + str(char_count) + '.png'
            cv2.imwrite(location, cropped)
    # cv2.imshow("full", img)
    # cv2.waitKey(0)
    return True

# imports a test image I scaned of my handwriting
print("Name: ")
name = input()
print("Image sample: ")
target = input()

analyze_sample(name, target)
