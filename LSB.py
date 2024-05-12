from addit_functs import *
import random

TB_old = []
TB_new = []


def LSB_R_enc(img, text, start, end, sdvig, raid=0.25):
    # Преобразование текстовых маркеров в бинарное представление
    binary_text = text_to_binary(start) + text_to_binary(text) + text_to_binary(end)
    
    # Вычисление нового значения raid (частоты изменения пикселей)
    raid = round(3 / raid)
    print(raid)
    
    # Вычисление начального индекса для скрытия битов
    index = round(sdvig * raid)

    # Инициализация списка для хранения младших битов
    array_LSB = []
    
    # Цикл по каждому символу в бинарном тексте
    for ch in binary_text:
        # Конвертация символа в массив битов
        arr_bit_ch = number_to_bin_arr(ch)
        
        # Цикл по каждому биту в символе
        for bit in arr_bit_ch:
            # Установка младшего бита в пикселе изображения в зависимости от значения бита
            if bit == 0:
                img[index] = clear_bit(img[index], 0)
            else:
                img[index] = set_bit(img[index], 0)
            
            # Получение младшего бита из обновленного пикселя и добавление его в список
            bits = number_to_bin_arr(img[index])
            array_LSB.append(bits[7])
            
            # Обновление индекса с учетом raid
            index += raid

    # Формирование байтов из младших битов и добавление их в список TB_old
    TB_old = []
    for i in range(0, len(array_LSB), 8):
        byte = bin_arr_to_number(array_LSB[i:i + 8])
        TB_old.append(byte)

    # Возвращение измененного изображения
    return img


import random

def LSB_M_enc(img, text, start, end, sdvig, raid=0.25):
    # Преобразуем текст в бинарное представление и объединяем с маркерами начала и конца
    binary_text = text_to_binary(start) + text_to_binary(text) + text_to_binary(end)
    # Вычисляем значение шага для изменения пикселей в изображении
    raid = round(3 / raid)

    # Инициализируем индекс для отслеживания текущего положения в изображении
    index = round(sdvig * raid)
    
    # Перебираем каждый бит скрытого текста
    for ch in binary_text:
        # Преобразуем символ (бит) в массив битов
        arr_bit_ch = number_to_bin_arr(ch)
        # Перебираем каждый бит в массиве битов символа
        for bit in arr_bit_ch:
            # Получаем текущий младший бит пикселя изображения
            bit_img = retn_bit(img[index], 7)
            # Если бит текста и младший бит пикселя равны 0
            if bit == 0 and bit_img == 0:
                # Ничего не делаем и смещаемся к следующему пикселю
                index += raid
                continue
            # Если бит текста 0, а младший бит пикселя 1
            elif bit == 0 and bit_img == 1:
                # Изменяем младший бит пикселя на случайное значение, чтобы сделать изменения менее заметными
                if img[index] == 255:
                    img[index] = img[index] - 1
                else:
                    rand_bit = random.randrange(-1, 2, 2)
                    img[index] = img[index] + rand_bit
            # Если бит текста 1, а младший бит пикселя 0
            elif bit == 1 and bit_img == 0:
                # Изменяем младший бит пикселя на случайное значение
                if img[index] == 0:
                    img[index] = img[index] + 1
                else:
                    rand_bit = random.randrange(-1, 2, 2)
                    img[index] = img[index] + rand_bit
            # Если бит текста и младший бит пикселя равны 1
            elif bit == 1 and bit_img == 1:
                # Ничего не делаем и смещаемся к следующему пикселю
                index += raid
                continue

            # Смещаемся к следующему пикселю
            index += raid

    # Возвращаем измененное изображение
    return img


def LSB_dec(img, start, end, raid=0.25):
    # Округляем 3 / raid и присваиваем результат переменной raid
    raid = round(3 / raid)

    # Создаем пустой список для хранения LSB каждого байта изображения
    array_LSB = []
    # Перебираем каждый байт в изображении с шагом, определенным переменной raid
    for i in range(0, len(img), raid):
        # Получаем текущий байт изображения
        byte = img[i]
        # Преобразуем текущий байт в массив битов
        bits = number_to_bin_arr(byte)
        # Добавляем последний (младший) бит текущего байта в список array_LSB
        array_LSB.append(bits[7])

    # Создаем пустые списки для хранения битов начальной и конечной строки
    bit_start = []
    bit_end = []
    # Преобразуем начальную строку в бинарный формат и добавляем ее биты в bit_start
    for e in text_to_binary(start):
        bit_start = bit_start + number_to_bin_arr(e)
    # Преобразуем конечную строку в бинарный формат и добавляем ее биты в bit_end
    for e in text_to_binary(end):
        bit_end = bit_end + number_to_bin_arr(e)

    # Извлекаем массив битов, соответствующий скрытому тексту, используя биты начальной и конечной строки
    text_bit = subarr_extract(bit_start, array_LSB, bit_end)

    # Создаем пустой список для хранения байтов скрытого текста
    text_byte = []
    # Преобразуем массив битов скрытого текста обратно в байты
    for i in range(0, len(text_bit), 8):
        byte = bin_arr_to_number(text_bit[i:i + 8])
        text_byte.append(byte)

    print(TB_old)
    # Выводим извлеченный скрытый текст в виде байтов
    print(text_byte)

    # Преобразуем байты скрытого текста в строку и возвращаем результат
    return binary_to_text(text_byte)



def main():
    path_to_image = "flag.jpg"
    image = read_color(path_to_image, 'pixels')
    text = "Hello world! Как дела? Привет мир!!!"
    m_start = "1"
    m_end = "2"

    text = "HW"

    image = LSB_R_enc(image, text, m_start, m_end, 5, 0.25)
    orig_text = LSB_dec(image, m_start, m_end, 0.25)



    # save_color(path_to_image, image, 'pixels')

    print(orig_text)


if __name__ == '__main__':
    main()
