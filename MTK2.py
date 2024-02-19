
ArrayBytesCodRule = ["11111", "00000", "11011", "00100", "00010", "01000"]

ArrayBytesCod = ["11000", "10011", "01110", "10010", "10000", "10110", "01011", "00101", "01100",
                 "11010", "11110", "01001", "00111", "00110", "00011", "01101", "11101", "01010",
                 "10100", "00001", "11100", "01111", "11001", "10111", "10101", "10001"]

ArrayLatinUp = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
ArrayLatinLow = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ArrayRussianUp = ['А', 'Б', 'Ц', 'Д', 'Е', 'Ф', 'Г', 'Х', 'И', 'Й', 'К', 'Л', 'М',
                  'Н', 'О', 'П', 'Я', 'Р', 'С', 'Т', 'У', 'Ж', 'В', 'Ь',  'Ы', 'З']
ArrayRussianLow = ['а', 'б', 'ц', 'д', 'е', 'ф', 'г', 'х', 'и', 'й', 'к', 'л', 'м',
                   'н', 'о', 'п', 'я', 'р', 'с', 'т', 'у', 'ж', 'в', 'ь',  'ы', 'з']

ArraySpecialUp = ['-', '?', ':', '', '3', 'Э', 'Ш', 'Щ', '8', 'Ю', '(', ')', '.', ',',
                  '9', '0', '1', '4', '\'', '5', '7', '=', '2', '/', '6', '+']
ArraySpecialLow = ['-', '?', ':', '', '3', 'э', 'ш', 'щ', '8', 'ю', '(', ')', '.', ',',
                   '9', '0', '1', '4', '\'', '5', '7', '=', '2', '/', '6', '+']


def MTK2_code(text):
    bytes_mass = ""
    flag = 0
    for i in range(len(text)):
        if text[i] == 'Ч' or text[i] =='ч':
            flag = 2
            bytes_mass += ArrayBytesCodRule[2]
            # Уникальный код для цифры 4 (без совпадения с символом "Ч")
            bytes_mass += ArrayBytesCod[17]
        elif (text[i] in ArrayLatinUp or text[i] in ArrayLatinLow) and flag != 0:
            flag = 0
            bytes_mass += ArrayBytesCodRule[0]
        elif (text[i] in ArrayRussianUp or text[i] in ArrayRussianLow) and flag != 1:
            flag = 1
            bytes_mass += ArrayBytesCodRule[1]
        elif (text[i] in ArraySpecialUp or text[i] in ArraySpecialLow) and flag != 2:
            flag = 2
            bytes_mass += ArrayBytesCodRule[2]
        elif text[i] == ' ':
            bytes_mass += ArrayBytesCodRule[3]
        elif text[i] == '\r':
            bytes_mass += ArrayBytesCodRule[4]
        elif text[i] == '\n':
            bytes_mass += ArrayBytesCodRule[5]

        if flag == 0:
            for j in range(len(ArrayLatinUp)):
                if text[i] == ArrayLatinUp[j] or text[i] == ArrayLatinLow[j]:
                    bytes_mass += ArrayBytesCod[j]
        elif flag == 1:
            for j in range(len(ArrayRussianUp)):
                if text[i] == ArrayRussianUp[j] or text[i] == ArrayRussianLow[j]:
                    bytes_mass += ArrayBytesCod[j]
        elif flag == 2 and text[i] != 'Ч' or text[i] != 'ч':
            for j in range(len(ArraySpecialUp)):
                if text[i] == ArraySpecialUp[j] or text[i] == ArraySpecialLow[j]:
                    bytes_mass += ArrayBytesCod[j]

    return bytes_mass

def MTK2_decode(bytes_mass):
    text = ""
    while len(bytes_mass) % 5 != 0:
        bytes_mass += ' '

    flag = 0
    for i in range(0, len(bytes_mass), 5):
        char_kod = bytes_mass[i:i+5]
        if char_kod == ArrayBytesCodRule[0]:
            flag = 0
        elif char_kod == ArrayBytesCodRule[1]:
            flag = 1
        elif char_kod == ArrayBytesCodRule[2]:
            flag = 2
        elif char_kod == ArrayBytesCodRule[3]:
            text += ' '
        elif char_kod == ArrayBytesCodRule[4]:
            text += '\r'
        elif char_kod == ArrayBytesCodRule[5]:
            text += '\n'
        elif char_kod == ArrayBytesCod[14]:  # код для символа "Ч"
            text += '4'
        else:
            for j in range(len(ArrayBytesCod)):
                if char_kod == ArrayBytesCod[j]:
                    if flag == 0:
                        text += ArrayLatinUp[j]
                    elif flag == 1:
                        text += ArrayRussianUp[j]
                    elif flag == 2:
                        text += ArraySpecialUp[j]

    return text


if __name__ == '__main__':
    text = "Тестовый текст for Проверка WORKING"
    print('открытый текст: ',text)
    MtK2 = MTK2_code(text)
    print(MtK2)
    text_new = MTK2_decode(MtK2)
    print('Полученный текст:',text_new)
    print(len(text_new))

