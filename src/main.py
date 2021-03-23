import cv2
import pytesseract
import os
import re

# imports a test image I scaned of my handwriting
print("Name: ")
name = input()
print("Image sample: ")
target = input()

# if we already know the contents we can use it for text correction
if(target == "pangram"):
    text_contents = "Aquickbrownfoxjumpsoverthelazydog.Aqui"
else:
    text_contents = ""

# create output files
os.chdir("..")
original = cv2.imread('data\\' + name + '\\' + target + '.png', cv2.IMREAD_GRAYSCALE)
try:
    os.makedirs('output\\' + name + '\\char')
except OSError:
    pass

# does some filtering to improve quality and get dimensions
resized = cv2.resize(original, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
img = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
h, w = img.shape


# create 2D list and string for storing characters and bounding boxes
text_array = []
text_string = ""
readable_string = ""
for b in pytesseract.image_to_boxes(img).splitlines():
    # make each line into a list and place in the 2D list
    b = b.split(' ')
    text_array.append(b)
    text_string += b[0]

# corrects errors in tesseract data using regex
def full_correction(text_to_correct, correct_text):
    if(correct_text == ""):
        return text_to_correct
    for k in range(1, 5):
        for i in range((2*k)+4, (2*k)+2, -1):
            for j in range(k, i-((2*k)-1)):
                patterns = []
                for h in range(len(correct_text)-i):
                    replacement = r"\w" * k
                    segment = correct_text[h:h+i]
                    search = segment[0:j] + replacement + segment[j+k: ]
                    patterns.append(search)
                    patterns.append(segment)
                for p in range(0, len(patterns), 2):
                    text_to_correct = re.sub(patterns[p], patterns[p+1], text_to_correct)
                #print(str(i) + ":" + str(j) + ":str(k) " + corrected)
    return text_to_correct

text_string = full_correction(text_string, text_contents)

# adds line breaks when a return is detected
length = len(text_array)
m = 0
while m < length-1:
    current_list = text_array[m]
    next_list = text_array[m+1]
    if((int(next_list[1])-int(current_list[1]))>=0):
        readable_string += current_list[0]
    else:
        readable_string += current_list[0] + "\n"
    m += 1

# save output string as text file
with open('output\\' + name + '\\' + target + '.txt', mode ='w') as file:
    file.write(text_string + "\n\n" + readable_string)
    file.close()

# save each character as a labled image
char_counter = [0]*27
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
    char_num = ord(b[0])-96
    if((char_num>0) and (char_num<27)):
        try:
            os.makedirs('output\\' + name + '\\char\\' + b[0])
        except OSError:
            pass
        # write image to output file and increment counter
        location = 'output\\' + name + '\\char\\' + b[0] + '\\' + str(char_counter[char_num]) + '.png'
        cv2.imwrite(location, cropped)
        char_counter[char_num] += 1
