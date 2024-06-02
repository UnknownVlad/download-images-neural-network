import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pywt


def load_image(image_path):
    """
    Загрузка изображения.
    """
    return Image.open(image_path)


def compute_detail_level(block):
    """
    Вычисление меры детализации блока с помощью вейвлет-преобразования.
    """
    block_array = np.array(block)
    coeffs = pywt.dwt2(block_array, 'haar')
    LL, (LH, HL, HH) = coeffs
    return np.sum(np.abs(HH))


def embed_watermark_text(image, watermark_text, block_size):
    """
    Внедрение текстового водяного знака в блок.
    """
    font_path = "arial.ttf"
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(image)

    # Размер изображения
    image_width, image_height = image.size

    # Вычисление количества блоков в строке и столбце
    blocks_per_row = image_width // block_size
    blocks_per_column = image_height // block_size

    # Выбор блока с наибольшей детализацией
    detail_levels = []
    for y in range(0, image_height, block_size):
        for x in range(0, image_width, block_size):
            block = image.crop((x, y, x + block_size, y + block_size))
            detail_levels.append((compute_detail_level(block), (x, y)))

    max_detail_block = max(detail_levels, key=lambda x: x[0])[1]

    # Внедрение водяного знака
    draw.text((max_detail_block[0], max_detail_block[1]), watermark_text, fill=(255, 255, 255), font=font)

    return image
if __name__ == "__main__":
    # Путь к изображению и текстовому водяному знаку
    image_path = "dataset/cyberpunk.jpg"
    watermark_text = "Watermark"

    original_image = load_image(image_path)

    # Размер блока
    block_size = 100  # Измените размер блока по вашему выбору

    # Внедрение водяного знака
    watermarked_image = embed_watermark_text(original_image, watermark_text, block_size)

    # Сохранение стеганографированного блока (для демонстрации)
    watermarked_image.save("dataset/watermarked_image.jpg")