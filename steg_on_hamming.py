import collections

import numpy as np
from addit_functs import mod_on_2, reverse_bit
from addit_functs import read_color, text_to_binary, subarr_extract, \
    number_to_bin_arr, bin_arr_to_number, binary_to_text, save_color

# Матрица проверки четности для кода Хэмминга
H = np.matrix([
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
], dtype=int)
n = 15  # Количество бит на пиксель

# Функция кодирования сообщения с использованием кода Хэмминга и добавления его к вектору кодовых слов
def encode(vector_c, vector_m):
    cod = np.matrix(vector_c, dtype=int)
    m = np.matrix(vector_m, dtype=int)
    s = mod_on_2(H * cod.T)  # Вычисление синдрома
    s = mod_on_2(s + m.T).T.tolist()[0]  # Добавление вектора сообщения к синдрому

    # Вычисление позиции ошибки
    i = (8 * s[3] + 4 * s[2] + 2 * s[1] + s[0]) - 1
    if i >= 0:
        vector_c = reverse_bit(vector_c, i)  # Инвертирование бита, если обнаружена ошибка

    return vector_c

# Функция декодирования полученного кодового слова с использованием кода Хэмминга
def decode(vector_c):
    vector_m = mod_on_2(H * np.matrix(vector_c, dtype=int).T)
    vector_m = vector_m.T.tolist()[0]
    return vector_m

# Функция скрытия текста в изображении с использованием метода стеганографии с кодами Хэмминга (SoH)
def SoH_enc(img, text, start, end, sdvig):
    # Преобразование текста в бинарный формат
    binary_text = text_to_binary(start) + text_to_binary(text) + text_to_binary(end)
    img_LSB_bit = []

    # Извлечение младшего значащего бита (LSB) из каждого пикселя в изображении
    for byte in img:
        bit_array = number_to_bin_arr(byte)
        img_LSB_bit.append(bit_array[7])

    index = sdvig * n  # Начальный индекс для скрытия текста
    # Итерация по бинарному тексту и кодирование его в LSB последовательных пикселей
    for byte in binary_text:
        arr_bit_text = number_to_bin_arr(byte)
        for i in range(0, len(arr_bit_text), 4):
            vector_m = arr_bit_text[i:i + 4]
            vector_c = img_LSB_bit[index:index + n]
            vector_c = encode(vector_c, vector_m)
            img_LSB_bit[index:index + n] = vector_c
            index += n

    # Восстановление измененного изображения с скрытым текстом
    new_img = []
    for i in range(len(img_LSB_bit)):
        if i >= len(img):
            break
        bit_array = number_to_bin_arr(img[i])
        bit_array[7] = img_LSB_bit[i]
        byte = bin_arr_to_number(bit_array)
        new_img.append(byte)

    return new_img

# Функция извлечения скрытого текста из изображения с использованием метода стеганографии с кодами Хэмминга (SoH)
def SoH_dec(img, start, end):
    img_LSB_bit = []

    bit_start = []
    for e in text_to_binary(start):
        bit_start = bit_start + number_to_bin_arr(e)

    bit_end = []
    for e in text_to_binary(end):
        bit_end = bit_end + number_to_bin_arr(e)

    # Извлечение LSB каждого пикселя изображения
    for byte in img:
        bit_array = number_to_bin_arr(byte)
        img_LSB_bit.append(bit_array[7])

    text_bit = []
    # Декодирование скрытых битов сообщения из LSB последовательных пикселей
    for i in range(0, len(img_LSB_bit), n):
        vector_c = img_LSB_bit[i:i + n]
        if len(vector_c) < n:
            break
        vector_m = decode(vector_c)
        for bit in vector_m:
            text_bit.append(bit)

    # Извлечение битов текста между маркерами начала и конца
    text_bit = subarr_extract(bit_start, text_bit, bit_end)

    # Преобразование бинарного текста обратно в символы
    text_byte = []
    for i in range(0, len(text_bit), 8):
        byte = bin_arr_to_number(text_bit[i:i + 8])
        text_byte.append(byte)

    return binary_to_text(text_byte)

if __name__ == '__main__':
    path_to_image = "flag.jpg"
    image = read_color(path_to_image, 'pixels')
    text = "Hello world! Как дела? Привет мир!!!"
    m_start = "#d*&63ls"
    m_end = "&2KJH349"

    # Скрытие текста в изображении
    image = SoH_enc(image, text, m_start, m_end, 15)
    # Извлечение скрытого текста из изображения
    orig_text = SoH_dec(image, m_start, m_end)
    # Сохранение измененного изображения с скрытым текстом
    save_color(path_to_image, image, 'pixels')

    print(orig_text)


    # total = 0
    # count = 0
    # for i in range(32768):
    #     c = [1 if i & (1 << (14 - n)) else 0 for n in range(15)]
    #     for j in range(16):
    #         m = [1 if i & (1 << (3 - n)) else 0 for n in range(4)]
    #         cod = np.matrix(c, dtype=int)
    #         m = np.matrix(m, dtype=int)
    #         s = mod_on_2(H * cod.T)
    #         s = mod_on_2(s + m.T).T.tolist()[0]
    #
    #         i = (8 * s[3] + 4 * s[2] + 2 * s[1] + s[0]) - 1
    #         if i >= 0:
    #             c = reverse_bit(c, i)
    #
    #         m_new = mod_on_2(H * np.matrix(c, dtype=int).T)
    #         m_new = m_new.T.tolist()[0]
    #
    #         m = collections.Counter(m.tolist()[0])
    #         m_new = collections.Counter(m_new)
    #
    #         total += 1
    #         if m != m_new:
    #             count += 1
    #
    # print(total)
    # print(count)
    # print(total - count)