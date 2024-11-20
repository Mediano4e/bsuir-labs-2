import cv2
import numpy as np
import matplotlib.pyplot as plt

def create_stereo_image(left_image_path, right_image_path, shift=10):
    left_img = cv2.imread(left_image_path)
    right_img = cv2.imread(right_image_path)
    
    if left_img.shape != right_img.shape:
        height = min(left_img.shape[0], right_img.shape[0])
        width = min(left_img.shape[1], right_img.shape[1])
        left_img = cv2.resize(left_img, (width, height))
        right_img = cv2.resize(right_img, (width, height))
    
    right_img_shifted = np.roll(left_img, shift, axis=1)
    

    anaglyph = np.zeros_like(left_img)
    anaglyph[:,:,0] = left_img[:,:,0]
    anaglyph[:,:,1] = right_img_shifted[:,:,1]
    anaglyph[:,:,2] = right_img_shifted[:,:,2]
    
    return anaglyph

# Создаем стерео-изображение
anaglyph = create_stereo_image('3.jpg', '3.jpg', shift=10)

# Сохраняем результат
cv2.imwrite(f"stereo_anaglyph.jpg", anaglyph)
