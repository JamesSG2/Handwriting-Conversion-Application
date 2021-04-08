import cv2
import pytesseract
import os
import re
import numpy as np
import random

# These functions handle the initial processing of the handwriting images
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
            text_to_correct = re.sub(patterns[p], patterns[p+1], \
            text_to_correct)
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
    contours_full, hierarchy = cv2.findContours(dialated,cv2.RETR_TREE, \
                                                cv2.CHAIN_APPROX_SIMPLE)
    contours = contours_full[::2]

    # place a bounding box around each contour
    boundRect = [None]*len(contours)
    for i, c in enumerate(contours):
        boundRect[i] = cv2.boundingRect(contours[i])
    boundRect.sort()

    # crop boxes and save
    image_list = []
    for i in range(len(contours)):
        cropped = cleaned[int(boundRect[i][1]):int(boundRect[i][1] \
            +boundRect[i][3]), \
            int(boundRect[i][0]):int(boundRect[i][0]+boundRect[i][2])]
        storage_list = [cropped, text_contents[i]]
        image_list.append(storage_list)

    return cleaned, image_list

def character_analysis(img, text_contents):
    # make image binary and scale up
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    threshold = cv2.threshold(resized, 0, 255, \
        cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
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
        cropped = resized[h-int(text_array[i][4]):h-int(text_array[i][2]), \
            int(text_array[i][1]):int(text_array[i][3])]
        # get the unicode number of the character and check if it is a letter
        char_num = ord(text_array[i][0])
        if(((char_num>=65) and (char_num<=90)) \
            or ((char_num>=97) and (char_num<=122))):
            # store cropped image and it's character in a nested list
            storage_list = [cropped, text_string[i]]
            image_list.append(storage_list)

    return resized, image_list

def analyze_sample(name, target):
    # open image
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
        # check case
        # case = ""
        # if i[1].isupper():
        #     case = "u"
        # elif i[1].islower():
        #     case = "l"
        # else:
        #     case = "p"
        character_id = str(ord(i[1]))

        # try to create output folder
        try:
            os.makedirs('output\\' + name + '\\' + character_id)
        except OSError:
            pass
        # check how many images are already in folder
        char_count = len(os.listdir('output\\' + name + '\\' + character_id))
        # save the image with the number of images already in the folder
        # appended to avoid duplicates
        location = 'output\\' + name + '\\' + character_id + '\\' + \
            character_id + "_" + str(char_count) + '.png'
        cv2.imwrite(location, i[0])

    print("Saved")
    return img

# These functions handle the reproduction of the handwriting
def create_blank(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image

def hconcat_whitespace(img1, img2):
    vert_diff = img1.shape[0]-img2.shape[0]
    if(vert_diff>0):
        pad = create_blank(img2.shape[1], vert_diff, (255,255,255))
        img2_padded = cv2.vconcat([pad, img2])
        return cv2.hconcat([img1, img2_padded])
    elif(vert_diff<0):
        pad = create_blank(img1.shape[1], abs(vert_diff), (255,255,255))
        img1_padded = cv2.vconcat([pad, img1])
        return cv2.hconcat([img1_padded, img1_padded])
    else:
        return cv2.hconcat([img1, img2])

def hconcat_resize(img_list, interpolation = cv2.INTER_CUBIC):
    # take minimum hights
    h_size = min(img.shape[0] for img in img_list)

    # image resizing
    im_list_resize = [cv2.resize(img, (int(img.shape[1]*h_size/img.shape[0]), \
        h_size), interpolation = interpolation) for img in img_list]

    # return final image
    return cv2.hconcat(im_list_resize)

def add_char(original_img, char_img):
    output = hconcat_resize([original_img, char_img])
    return output

def output_handwriting(name, phrase):
    # this will be used when outputting the reproduction of your handwriting

    output_image = create_blank(10,50, (255,255,255))

    for char in phrase:
        # check case
        # case = ""
        # if char.isupper():
        #     case = "u"
        # elif char.islower():
        #     case = "l"
        # else:
        #     case = "p"
        # character_id = char + "_" + case
        char_num = ord(char)
        char_str = str(char_num)

        if(char_num>32):
            try:
                char_count = len(os.listdir('output\\' + name + '\\' \
                    + char_str))
            except FileNotFoundError:
                print("could not find letter:" + char)
                continue
            if (char_count == 0):
                print("could not find letter:" + char)
                continue

            char_select = random.randint(0, char_count-1)
            char_img = cv2.imread('output\\' + name + '\\' + char_str \
                + '\\' + char_str + "_" + str(char_select) + '.png')
            output_image = hconcat_whitespace(output_image, char_img)

        elif(char_num==32):
            char_img = create_blank(50,50, (255,255,255))
            output_image = hconcat_whitespace(output_image, char_img)

    return output_image

# These functions run the program
def main():

    os.chdir("..")
    # hopefully this section can have it's functionality replaced by the GUI
    print("Analyze new samples? [Y/N]:")
    analysis = input()

    if(analysis=="Y"):
        print("Name: ")
        name = input()
        print("Image sample: ")
        target = input()

        img = analyze_sample(name, target)
        # cv2.imshow("full", img)
        # cv2.waitKey(0)

    elif(analysis=="N"):
        print("Name: ")
        name = input()
        print("What should be written:")
        phrase = input()
        img = output_handwriting(name, phrase)
        cv2.imshow("output", img)
        cv2.waitKey(0)

    else:
        print("Error, did not select [Y/N]")

    print("Done")

if __name__ == '__main__':
    main()
