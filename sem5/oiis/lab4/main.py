import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


image = cv2.imread("image.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

reshaped_image = image_rgb.reshape((-1, 3))

kmeans = KMeans(n_clusters=9, random_state=0)
kmeans.fit(reshaped_image)

labels = kmeans.labels_

segmented_image = labels.reshape(image_rgb.shape[:2])

fig, axes = plt.subplots(1, 2, figsize=(15, 7))

axes[0].imshow(image_rgb)
axes[0].set_title("Исходное изображение")
axes[0].axis('off')

axes[1].imshow(segmented_image, cmap='tab20b')
axes[1].set_title("Сегментированное изображение (k-средние)")
axes[1].axis('off')

plt.tight_layout()
plt.show()
