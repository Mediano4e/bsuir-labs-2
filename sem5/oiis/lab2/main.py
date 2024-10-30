import cv2
import numpy as np
from matplotlib import pyplot as plt

def show_images(images, titles):
    plt.figure(figsize=(15, 8))
    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(2, 3, i+1)
        if len(img.shape) == 2:  # Для одноканальных изображений
            plt.imshow(img, cmap='gray')
        else:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()
    plt.show()

def apply_filters(image):
    # Преобразуем в оттенки серого для фильтров Собеля и Лапласа
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 1. Медианный фильтр
    median = cv2.medianBlur(image, 5)
    
    # 2. Гауссовский фильтр
    gaussian = cv2.GaussianBlur(image, (5,5), 0)
    
    # 3. Обычный блюр
    blur = cv2.blur(image, (5,5))
    
    # 4. Фильтр Собеля
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = np.sqrt(sobelx**2 + sobely**2)
    sobel = np.uint8(sobel)
    
    # 5. Фильтр Лапласа
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian = np.uint8(np.absolute(laplacian))
    
    return [image, median, gaussian, blur, sobel, laplacian]

def main():
    # Загрузка изображения
    image = cv2.imread('image.jpg')  # Замените на путь к вашему изображению
    
    if image is None:
        print("Ошибка: Не удалось загрузить изображение")
        return
    
    # Применяем фильтры
    filtered_images = apply_filters(image)
    
    # Названия для отображения
    titles = ['Оригинал', 
             'Медианный фильтр',
             'Гауссовский фильтр',
             'Размытие',
             'Фильтр Собеля',
             'Фильтр Лапласа']
    
    # Показываем результаты
    show_images(filtered_images, titles)
    
    # Сохранение результатов
    for img, title in zip(filtered_images[1:], titles[1:]):
        filename = f"{title}.jpg"
        cv2.imwrite(filename, img)
        print(f"Сохранено: {filename}")

if __name__ == "__main__":
    main()