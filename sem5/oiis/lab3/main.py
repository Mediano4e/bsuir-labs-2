import cv2
import numpy as np
import matplotlib.pyplot as plt


image1 = cv2.imread("image1.jpeg")
image2 = cv2.imread("image2.jpg")

gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

brightness1 = np.mean(gray1)
brightness2 = np.mean(gray2)

adjustment_factor_1 = brightness2 / brightness1
adjustment_factor_2 = brightness1 / brightness2

image1_adjusted = np.clip(image1 * adjustment_factor_1, 0, 255).astype(np.uint8)
image2_adjusted = np.clip(image2 * adjustment_factor_2, 0, 255).astype(np.uint8)


fig, axes = plt.subplots(1, 4, figsize=(20, 5))

axes[0].imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
axes[0].set_title("Исходное изображение 1")
axes[0].axis('off')

axes[1].imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
axes[1].set_title("Исходное изображение 2")
axes[1].axis('off')

axes[2].imshow(cv2.cvtColor(image1_adjusted, cv2.COLOR_BGR2RGB))
axes[2].set_title("Откорректированное изображение 1")
axes[2].axis('off')

axes[3].imshow(cv2.cvtColor(image2_adjusted, cv2.COLOR_BGR2RGB))
axes[3].set_title("Откорректированное изображение 2")
axes[3].axis('off')


plt.tight_layout()
plt.show()

