import os
from PIL import Image

# Параметры
input_image_path = "downloaded_images/a09k1putma.jpg"  # Укажите путь к вашему большому изображению
output_folder = "image_fragments"
fragment_width = 256
fragment_height = 256

# Создание папки, если она не существует
os.makedirs(output_folder, exist_ok=True)


def split_image(image_path, output_folder, fragment_width, fragment_height):
    try:
        img = Image.open(image_path)
        img_width, img_height = img.size

        # Рассчитываем количество фрагментов по горизонтали и вертикали
        num_fragments_x = img_width // fragment_width
        num_fragments_y = img_height // fragment_height

        fragment_number = 0

        for i in range(num_fragments_y):
            for j in range(num_fragments_x):
                left = j * fragment_width
                upper = i * fragment_height
                right = left + fragment_width
                lower = upper + fragment_height

                # Обрезаем фрагмент
                fragment = img.crop((left, upper, right, lower))

                # Генерируем имя файла для фрагмента
                fragment_filename = f"fragment_{fragment_number}.jpg"
                fragment_path = os.path.join(output_folder, fragment_filename)

                # Сохраняем фрагмент
                fragment.save(fragment_path)
                print(f"Fragment saved: {fragment_path}")

                fragment_number += 1

    except Exception as e:
        print(f"Failed to split image: {e}")


split_image(input_image_path, output_folder, fragment_width, fragment_height)
