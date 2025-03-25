import cv2
import numpy as np

def embed_text(image_path, secret_data, output_path):
    image = cv2.imread(image_path)
    secret_data += "####"  # End delimiter
    binary_secret = ''.join(format(ord(i), '08b') for i in secret_data)

    data_index = 0
    for row in image:
        for pixel in row:
            for i in range(3):  # Modify R, G, B
                if data_index < len(binary_secret):
                    pixel[i] = pixel[i] & ~1 | int(binary_secret[data_index])
                    data_index += 1
    cv2.imwrite(output_path, image)
    return output_path
