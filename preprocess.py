import cv2
import os
import numpy as np

input_directory = 'dataset/'
output_directory = 'output/'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for filename in os.listdir(input_directory):
    if filename.endswith('.jpg'):
        image_path = os.path.join(input_directory, filename)
        image = cv2.imread(image_path)

        cropped_image = image[10:45, 1178:1273]

        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        blurred_image1 = cv2.GaussianBlur(gray_image, (5, 5), 0)
        blurred_image2 = cv2.GaussianBlur(gray_image, (9, 9), 0)

        dog_image = cv2.subtract(blurred_image1, blurred_image2)

        _, mask = cv2.threshold(dog_image, 7, 15, cv2.THRESH_BINARY)

        masked_result = cv2.bitwise_and(
            cropped_image, cropped_image, mask=mask)

        result_gray_image = cv2.cvtColor(masked_result, cv2.COLOR_BGR2GRAY)

        _, binary_image = cv2.threshold(
            result_gray_image, 245, 255, cv2.THRESH_BINARY_INV)

        kernel = np.ones((3, 3), np.uint8)
        eroded_image = cv2.erode(binary_image, kernel, iterations=1)

        output_path = os.path.join(output_directory, filename)
        cv2.imwrite(output_path, eroded_image)


print("done")
