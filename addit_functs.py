import secrets
import string

from PIL import Image, ImageDraw
import numpy as np


def read_color(img_path, color_metod):
    """
    Функция извлекает цвета RGB из изображение
    :param img_path: путь к изображению
    :param color: извлекаемый цвет [red, green, blue],
                  pixels если извлечение идёт попиксильно
                  all если нужно извлечь массив всех цветов сначала красные, потом зелёные и потом синие
    :return: извлеченный массив цветов
    """

    img = Image.open(img_path)
    img_pix = img.load()

    width = img.size[0]
    height = img.size[1]

    red = []
    green = []
    blue = []
    for x in range(width):
        for y in range(height):
            r, g, b = img_pix[x, y]
            red.append(r)
            green.append(g)
            blue.append(b)

    img.close()

    if color_metod == 'red':
        return red
    elif color_metod == 'green':
        return green
    elif color_metod == 'blue':
        return blue
    elif color_metod == 'pixels':
        data = []
        for i in range(len(red)):
            data.append(red[i])
            data.append(green[i])
            data.append(blue[i])
        return data
    else:
        return red + green + blue


def save_color(img_old_path, img_new_path, img_pix_new, color_metod):
    """
    Сохранение изменённых пикселей в изображении
    :param img_path: пусть к изображению
    :param img_pix_new: новые пиксели в изображении
    :param color_metod: извлекаемый цвет [red, green, blue],
                        pixels если извлечение идёт попиксильно
                        all если нужно извлечь массив всех цветов сначала красные, потом зелёные и потом синие
    """

    img = Image.open(img_old_path)
    img_draw = ImageDraw.Draw(img)
    img_pix = img.load()

    width = img.size[0]
    height = img.size[1]

    index = 0
    for x in range(width):
        for y in range(height):
            r, g, b = img_pix[x, y]
            if color_metod == 'red':
                img_draw.point((x, y), (img_pix_new, g, b))
            elif color_metod == 'green':
                img_draw.point((x, y), (r, img_pix_new, b))
            elif color_metod == 'blue':
                img_draw.point((x, y), (r, g, img_pix_new))
            elif color_metod == 'pixels':
                red = img_pix_new[index]
                green = img_pix_new[index+1]
                blue = img_pix_new[index+2]
                img_draw.point((x, y), (red, green, blue))
                index += 3
            else:
                red = img_pix_new[0:len(r)]
                green = img_pix_new[len(r):len(g)]
                blue = img_pix_new[len(g):]
                img_draw.point((x, y), (red, green, blue))

    img.save(img_new_path, "BMP")
    img.close()


def get_size(img_path):
    """
    Получает размеры изображения
    :param img_path: пусть к изображению
    :return: ширина и высота
    """
    img = Image.open(img_path)
    width = img.size[0]
    height = img.size[1]
    img.close()

    return width, height


def text_to_binary(text):
    """
    Преобразует текст в массив байтов utf-8
    :param text: исходный текст
    :return: набор байтов []
    """

    text = text.encode("utf-8")
    data = []
    for c in text:
        data.append(c)
    return data


def binary_to_text(data):
    """
    Преобразует массив байт в текст utf-8
    :param data: массив байтов
    :return: текст
    """

    # text = ""
    # for byte in data:
    #     try:
    #         c = bytes([byte]).decode("utf-8")[0]
    #         text += c
    #     except:
    #         continue

    return bytes(data).decode("utf-8")


def number_to_bin_arr(data):
    """
    Переводит байт в массив длины 8 бит
    :param data: байт в виде числа 0 - 255
    :return: массив бит
    """

    return [1 if data & (1 << (7 - n)) else 0 for n in range(8)]


def bin_arr_to_number(data):
    """
    Обратное преобразование массива бит в байт
    :param data: массив из 8 бит
    :return: байт в виде числа 0 - 255
    """

    out = 0
    for bit in data:
        out = (out << 1) | bit
    return out


def set_bit(value, bit):
    """
    заменяет указанный бит в числе на еденицу
    :param value: число
    :param bit: позиция устанавливаемого бита
    :return: измененное число
    """

    return value | (1<<bit)


def clear_bit(value, bit):
    """
    заменяет указанный бит в числе на ноль
    :param value: число
    :param bit: позиция обнуляемого бита
    :return: измененное число
    """

    return value & ~(1<<bit)


def find_SubarrayStartIndex(array, subArray):
    """
    Поиск первого вхождения подмассива в массиве
    :param array: массив
    :param subArray: искомый подмассив
    :return: индекс вхождения подмассиива
    """

    index = -1
    for i in range(len(array) - len(subArray) + 1):
        index = i
        for j in range(len(subArray)):
            if array[i + j] != subArray[j]:
                index = -1
                break
        if index >= 0:
            return index
    return -1


def subarr_extract(bit_start, arr, bit_end):
    """
    Извлечение подмассива данных, окруженных двумя дургими подмассивами
    :param bit_start: левый подмассив
    :param arr: исходный массив
    :param bit_end: правый подмассив
    :return: подмассив между левым и правым подмассивом
    """

    index_bs = find_SubarrayStartIndex(arr, bit_start)
    index_be = find_SubarrayStartIndex(arr, bit_end)
    return arr[index_bs+len(bit_start):index_be]


def retn_bit(num, pos):
    """
    Получение бита числа на определённой позиции
    :param num: число
    :param pos: позиция бита
    :return: полученный бит
    """
    array_bit = number_to_bin_arr(num)
    return array_bit[pos]


def mod_on_2(vector):
    """
    Деление вектора по модулю 2
    :param vector: вектор
    :return: Поделённый по модулю 2 вектор
    """
    div_vector = vector.copy()
    div_vector.fill(2)
    return np.remainder(vector, div_vector)


def reverse_bit(vector, index):
    """
    Переворачивание бита в векторе
    :param vector: Вектор
    :param index: индекс переворачиваемого бита
    :return: получившийся вектор
    """
    if index == -1:
        return vector
    if vector[index] == 1:
        vector[index] = 0
    else:
        vector[index] = 1
    return vector


def generate_alphanum_crypt_string(length):
    letters_and_digits = string.ascii_letters + string.digits + string.punctuation
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(length))
    return crypt_rand_string