from funcs import get_prime,EXP,inverse

# функция для преобразования текста в биты
def text_to_bits(text, encoding='Windows-1251', errors='ignore'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

# функция для преобразования битов в текст
def text_from_bits(bits, encoding='Windows-1251', errors='ignore'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

# получаем два простых числа p и q
p,q = get_prime()
print(f'p: {p}\nq: {q}')

# вычисляем модуль N и функцию Эйлера Ф(N)
n=p*q 
fn=(p-1)*(q-1) 
print("Модуль N: ",n) 
print("Ф(N): ",fn)

# генерируем открытый ключ e
e= EXP(fn)
print("e: ",e)

# вычисляем секретный ключ d
d=inverse(fn,e) 
print("d: ",d)

# выводим открытый и секретный ключи
print(f'Открытый ключ{e,n}\nСекретный ключ{d,n}')

# запрашиваем у пользователя текст для шифрования
ot=input("Введите текст: ") 

# шифруем каждый символ текста
shifr = [bin((int(text_to_bits(i), 2) ** e) % n)[2:] for i in ot]

# объединяем биты в одну строку и преобразуем ее в текст
shifr_text="".join(shifr)
shifr_text=text_from_bits(shifr_text)

# преобразуем каждый бит в шестнадцатеричную систему
shifr_hex=[hex(int(i))[2:] for i in shifr]

# выводим зашифрованный текст и шифр в шестнадцатеричной системе
print(f' Зашифрованный текст:\n{shifr_text}\n\n Шифр в шестнадцатиричной:\n{shifr_hex}')

# расшифровываем каждый символ
decrypt = [text_from_bits(bin((int(i, 2) ** d) % n)[2:]) for i in shifr]

# выводим расшифрованный текст
print(f'\n Расшифрованое сообщение:\n{("".join(decrypt))}')
