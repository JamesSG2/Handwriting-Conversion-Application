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

def low_confidence_rejection(pytesseract_list, threshold):
    # Finds low confidence words and their respective letters
    k = 0
    minimum_confidence_level = 55    # <<< feel free to adjust if necessary (CL: 0 to 100)
    unconfident_letters = []
    confident_pytesseract_list = []
    for n in pytesseract_list:
        confident_pytesseract_list.append(n)
    pytesseract_data = pytesseract.image_to_data(threshold, output_type='data.frame')
    for i in range(0, len(pytesseract_data)):
        if pytesseract_data.conf[i] == -1:
            continue
        for j in range(k, k + len(str(pytesseract_data.text[i]))):
            if pytesseract_data.conf[i] < minimum_confidence_level:
                unconfident_letters.append(pytesseract_list[j])
        k += len(str(pytesseract_data.text[i]))

    # Removes low confidence words and their respective letters
    for n in unconfident_letters:
        confident_pytesseract_list.remove(n)

    return confident_pytesseract_list

def multi_letter_finder(letter_img, avg_w, w_standard_deviation):
    ht, w = letter_img.shape
    letter_w = w
    z_score = (letter_w - avg_w) / w_standard_deviation
    if (z_score > 1.9):
        return True
    else:
        return False

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

    # get predictions from pytesseract and place bounding boxes in an array
    pytesseract_list = pytesseract.image_to_boxes(threshold).splitlines()

    #Shows what was originally found
    for b in pytesseract_list:
        text_string += b[0]
    print(text_string)

    # Finds the confidence level for each prediction, and removes words below the minimum confidence Level
    # returns confident letters and their bounding boxes after removing low confidence results
    confident_pytesseract_list = low_confidence_rejection(pytesseract_list, threshold)

    #Adds confident words to the uncorrected text
    text_string = ""
    for b in confident_pytesseract_list:
        # make each line into a list and place in the 2D list
        b = b.split(' ')
        text_array.append(b)
        text_string += b[0]

    # now run text correction and show before and after
    print("\nRemoved Low Confidence Results:")
    print(text_string)
    text_string = new_full_correction(text_string, text_contents)
    print("\nCorrected to:")
    print(text_string)

    # Calculates the average character-image width and the standard deviation of the widths (for the multi_letter_finder function)
    sum_w = 0
    w_list = []
    for i in range(len(text_array)):
        img = resized[h-int(text_array[i][4]):h-int(text_array[i][2]), \
            int(text_array[i][1]):int(text_array[i][3])]
        ht, w = img.shape
        sum_w += w
        w_list.append(w)
    avg_w = sum_w / len(text_array)
    w_standard_deviation = 0
    for i in range(len(text_array)):
        w_standard_deviation += ((w_list[i] - avg_w)**2) / len(text_array)
    w_standard_deviation = (w_standard_deviation)**(1/2)

    # store cropped images in list with their character
    image_list = []
    for i in range(len(text_array)):
        # crop the image based on tesseract bounding boxes
        cropped = resized[h-int(text_array[i][4]):h-int(text_array[i][2]), \
            int(text_array[i][1]):int(text_array[i][3])]
        # get the unicode number of the character and check if it is a letter
        char_num = ord(text_array[i][0])
        if(((char_num>=65) and (char_num<=90)) \
            or ((char_num>=97) and (char_num<=122))) and (multi_letter_finder(cropped, avg_w, w_standard_deviation) == False):  # doesn't save images that are suspect of being multi-letter
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
    print("\nExpect to find:")
    print(text_contents)

    print("\nFound:")

    # run correct analysis
    if("punctuation" in target):
        img, image_list = punctuation_analysis(original, text_contents)
    else:
        img, image_list = character_analysis(original, text_contents)

    # save images in image list avoiding duplicates by appending a number
    for i in image_list:
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
    blank = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    blank[:] = color
    return blank

def hconcat_whitespace(img1, img2):
    vert_diff = img1.shape[0]-img2.shape[0]
    if(vert_diff>0):
        pad = create_blank(img2.shape[1], vert_diff, (255,255,255))
        img2_padded = cv2.vconcat([pad, img2])
        return cv2.hconcat([img1, img2_padded])
    elif(vert_diff<0):
        pad = create_blank(img1.shape[1], abs(vert_diff), (255,255,255))
        img1_padded = cv2.vconcat([pad, img1])
        return cv2.hconcat([img1_padded, img2])
    else:
        return cv2.hconcat([img1, img2])

def vconcat_whitespace(img1, img2):
    horiz_diff = img1.shape[1]-img2.shape[1]
    if(horiz_diff>0):
        pad = create_blank(horiz_diff, img2.shape[0], (255,255,255))
        img2_padded = cv2.hconcat([img2, pad])
        return cv2.vconcat([img1, img2_padded])
    elif(horiz_diff<0):
        pad = create_blank(abs(horiz_diff), img1.shape[0], (255,255,255))
        img1_padded = cv2.hconcat([img1, pad])
        return cv2.vconcat([img1_padded, img2])
    else:
        return cv2.vconcat([img1, img2])

def save_writing_image(name, image_to_save):
    try:
        os.makedirs('output\\' + name + '\\writing_result')
    except OSError:
        pass
    # check how many images are already in folder
    result_count = len(os.listdir('output\\' + name + '\\writing_result'))
    # save the image with the number of images already in the folder
    # appended to avoid duplicates
    location = 'output\\' + name + '\\writing_result\\result' \
        + "_" + str(result_count) + '.png'
    cv2.imwrite(location, image_to_save)

    return True

def mark_char_as_bad(name, char, char_select):
    char_str = str(ord(char))
    path_to_file = 'output\\' + name + '\\' + char_str + '\\' + char_str + "_" + str(char_select)
    if(os.path.isfile(path_to_file + ".png")):
        os.rename((path_to_file + ".png"), (path_to_file+"_bad.png"))
    else:
        return False
    return True

def get_char_rand(name, char):
    # used to select a random character image
    char_num = ord(char)
    char_str = str(char_num)
    # if the character is not whitespace
    if(char_num>32):
        # check how many if any of the character exists
        try:
            char_count = len(os.listdir('output\\' + name + '\\' \
                + char_str))
        except FileNotFoundError:
            print("could not find letter:" + char)
            return create_blank(5,5, (255,255,255)), 0

        if (char_count == 0):
            print("could not find letter:" + char)
            return create_blank(5,5, (255,255,255)), 0
        # select a random character
        good_selection = False
        while(good_selection == False):
            char_select = random.randint(0, char_count-1)
            path_to_file = ('output\\' + name + '\\' + char_str \
                            + '\\' + char_str + "_" + str(char_select) + '.png')
            if(os.path.isfile(path_to_file)):
                char_img = cv2.imread(path_to_file)
                good_selection = True
            else:
                good_selection = False

    else:
        # if the character is whitespace use a white square
        char_img = create_blank(50,50, (255,255,255))
        char_select = 0

    return char_img, char_select

def get_char(name, char, char_select):
    # used to select predetermined character image
    # essentially the same as get_char_rand
    char_num = ord(char)
    char_str = str(char_num)

    if(char_num>32):
        try:
            char_count = len(os.listdir('output\\' + name + '\\' \
                + char_str))
        except FileNotFoundError:
            print("could not find letter:" + char)
            return create_blank(5,5, (255,255,255)), 0

        if (char_count == 0):
            print("could not find letter:" + char)
            return create_blank(5,5, (255,255,255)), 0
        good_selection = False
        while(good_selection == False):
            path_to_file = ('output\\' + name + '\\' + char_str \
                            + '\\' + char_str + "_" + str(char_select) + '.png')
            if(os.path.isfile(path_to_file)):
                char_img = cv2.imread(path_to_file)
                good_selection = True
            else:
                char_select = random.randint(0, char_count-1)
                good_selection = False

    elif(char_num==32):
        char_img = create_blank(50,50, (255,255,255))
        char_select = 0

    return char_img, char_select

def output_handwriting_sample(name, phrase):
    # this will be used when outputting a first draft sample of your handwriting
    output_image = create_blank(10,10, (255,255,255))
    selection_list = []

    for char in phrase:
        char_img, char_pos = get_char_rand(name, char)
        output_image = hconcat_whitespace(output_image, char_img)
        selection_list.append(char_pos)

    # save_line_image(name, output_image)
    print(selection_list)

    return output_image, selection_list

def output_handwriting_revision(name, phrase, previous_list, list_of_errors):

    output_image = create_blank(10,10, (255,255,255))
    selection_list = []

    for i in range(len(phrase)):
        # if a character was marked as needing correction get a random new image
        # otherwise use the same image as before
        if(list_of_errors[i]):
            mark_char_as_bad(name, phrase[i], previous_list[i])
            char_img, char_pos = get_char_rand(name, phrase[i])
        else:
            char_img, char_pos = get_char(name, phrase[i], previous_list[i])
        output_image = hconcat_whitespace(output_image, char_img)
        selection_list.append(char_pos)

    # save_line_image(name, output_image)
    print(selection_list)

    return output_image, selection_list

def join_lines(list_of_line_images):
    output_image = create_blank(10,10, (255,255,255))
    for image in list_of_line_images:
        output_image = vconcat_whitespace(output_image, image)
    # cv2.imshow("output", output_image)
    # cv2.waitKey(0)
    return output_image


def create_correction_list(list_of_positions, length):
    # returns list containing False if the character does not need correction
    list_of_corrections = [False] * length
    for position in list_of_positions:
        list_of_corrections[int(position)] = True
    return list_of_corrections

# These functions run the program
def main():

    #os.chdir("..")
    # hopefully this section can have it's functionality replaced by the GUI
    print("Analyze new samples? [Y/N]:")
    analysis = input().lower()

    if(analysis=="y"):
        print("Name: ")
        name = input()
        print("Image sample: ")
        target = input()

        img = analyze_sample(name, target)
        # cv2.imshow("full", img)
        # cv2.waitKey(0)

    elif(analysis=="n"):
        print("Name: ")
        name = input()
        print("What should be written:")
        phrase = input()
        if phrase: # skips empty strings
            phrase_lines = phrase.split(r"\n")
        line_images = []
        for line in phrase_lines:
            single_line, selection_list = output_handwriting_sample(name, line)
            cv2.imshow("output", single_line)
            cv2.waitKey(0)
            print("Is correction needed? [Y/N]:")
            needed = input().lower()
            while needed == "y":
                print("Correction locations?")
                corrections = input().split(',')
                list_of_corrections = create_correction_list(corrections, len(selection_list))
                single_line, selection_list = output_handwriting_revision(name, line, \
                    selection_list, list_of_corrections)
                cv2.imshow("output", single_line)
                cv2.waitKey(0)
                print("Is correction needed? [Y/N]:")
                needed = input().lower()
            line_images.append(single_line)
        final_image = join_lines(line_images)
        save_writing_image(name, final_image)
        cv2.imshow("output", final_image)
        cv2.waitKey(0)

    else:
        print("Error, did not select [Y/N]")

    print("Done")

if __name__ == '__main__':
    main()
