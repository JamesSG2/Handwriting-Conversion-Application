#import pillow
import cv2
import pytesseract


img = cv2.imread('quote.jpeg')

#file_name = os.path.basename(img_path).split('.')[0]
#file_name = file_name.split()[0]

#output_path os.path.join(output_dir, file_name)
#if not os.path.exists(output_path):
#    os.makedirs(output_path)
    
img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#kernel = np.ones((1, 1), np.uint8)
#img = cv2.dilate(img, kernel, iterations=1)
#img = cv2.erode(img, kernel, iterations=1)

img = cv2.GaussianBlur(img, (5, 5), 0)

#img = cv2.threshold(img,  0, 255, cv2.THRES_BINARY + cv2.THRES_OTSU)[1]

cv2.imwrite('processed_test.png', img)

result = pytesseract.image_to_string(img, lang="eng")

with open('result.txt', mode ='w') as file:
    file.write(result)
    print(result)