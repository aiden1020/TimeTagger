import cv2
import os
import numpy as np


def process_images(input_directory, output_directory='output/', crop_coords=(10, 45, 1170, 1273), kernel_size=(3, 3), output=False):
    if not os.path.exists(output_directory) and output == True:
        os.makedirs(output_directory)
    filename_with_words = []
    for filename in os.listdir(input_directory):
        if filename.endswith('.jpg'):
            image_path = os.path.join(input_directory, filename)
            image = cv2.imread(image_path)

            cropped_image = image[crop_coords[0]:crop_coords[1], crop_coords[2]:crop_coords[3]]

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

            kernel = np.ones(kernel_size, np.uint8)
            eroded_image = cv2.erode(binary_image, kernel, iterations=1)
            if output == True:
                output_path = os.path.join(output_directory, filename)
                cv2.imwrite(output_path, eroded_image)
            else:
                total_pixels = eroded_image.size

                non_black_pixels = cv2.countNonZero(eroded_image)

                black_pixels = total_pixels - non_black_pixels
                if black_pixels > 800:  # it means image contains time
                    filename_with_words.append(filename)

    print("preprocess done...")
    return filename_with_words


if __name__ == "__main__":
    input_directory = 'dataset/0903-七賢路河東路口東北側挖除-3755'
    output_directory = 'output/'
    process_images(input_directory, output_directory, output=True)
