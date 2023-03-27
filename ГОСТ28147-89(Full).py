import re
import binascii

    # Функция для перевода текстовой строки в битовую последовательность
def text_to_bits(posled, encoding='Windows-1251', errors='surrogatepass'): 
    bits = bin(int(binascii.hexlify(posled.encode(encoding, errors)), 16))[2:] 
    return bits.zfill(8 * ((len(bits) + 7) // 8)) 

     # Функция для перевода битовой последовательности в текстовую строку
def text_from_bits(binstring, encoding='Windows-1251', errors='surrogatepass'): 
    n = int(binstring, 2) 
    return int2bytes(n).decode(encoding, errors) 

 
def int2bytes(i): 
    # Вспомогательная функция для преобразования целого числа в байтовую строку
    hex_string = '%x' % i 
    n = len(hex_string) 
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def func_preobr(R,X):
    # Функция для выполнения операции преобразования R с помощью X
    sum_mod=(int(R,2)+int(X,2))%4294967296
    sum_mod=bin(sum_mod)[2:].zfill(32)
    
    return sum_mod

def table_perestanovok(table,vhod):
    # Функция для выполнения таблицы перестановок над битовой строкой
    vhod=(re.findall('.{%s}' % 4, vhod)) # разбиваем входную строку на блоки по 4 символа (бита) каждый
    for k in range(len(vhod)):
        vhod[k]=int(vhod[k],2) # переводим каждый блок из двоичной строки в целое число
        
    zamen=[]

    for j in range(len(vhod)):
        zamen.append(bin(table[j][vhod[j]])[2:]) # заменяем каждый блок входной строки согласно таблице перестановок
        
    for i in range(len(zamen)):
        if len(zamen[i])<4:
            prefix = '0'
            n=4-len(zamen[i])
            zamen[i] = f'{prefix * n}{zamen[i]}' # добавляем ведущие нули для каждого блока, чтобы их длина была равна 4
        else:
            pass
    zamen="".join(zamen)
    zamen=zamen[11:]+zamen[0:11] # циклически сдвигаем полученную строку на 11 символов влево
    return zamen                             
    


def new_R(L,F):
    # Функция для получения нового значения правой половины блока шифрования
    Rn=int(L,2)^int(F,2) # применяем операцию XOR между левой половиной блока и значением функции F
    Rn=bin(Rn)[2:].zfill(32) # преобразуем результат в двоичную строку длиной 32 символа (бита)
    return Rn



def one(Ot,key,N1,N2):
    # Ot - список сообщений для шифрования
    # key - ключ шифрования
    # N1 - список для хранения шифрованных сообщений
    # N2 - список для хранения расшифрованных сообщений
    
    for i in range(len(Ot)):
        
        # Преобразуем ключ в ASCII и делим на блоки по 32 бита
        key_ascii=text_to_bits(key)
        n = 32
        split_key=(re.findall('.{%s}' % n, key_ascii))
        
        # Добавляем в массив split_key ещё 96 бит, повторив ключ и его реверс
        cop1=split_key
        cop2=split_key
        cop3=split_key[::-1]
        split_key=split_key+cop1+cop2+cop3

        # Делим сообщение на две части LR
        LR=(text_to_bits(Ot[i]))
        L=[]
        R=[]
        l = len(LR) + 1 
        L.append(LR[0:l//2])
        R.append(LR[l//2:])

        # Цикл шифрования
        for p in range(32):
            # Выполняем преобразование над правой частью блока и ключом
            vhod=func_preobr(R[p],split_key[p])

            # Выполняем перестановку
            F=table_perestanovok(Sblock,vhod)
            
            # Сохраняем левую часть и вычисляем новую правую
            L.append(R[p])
            Rn=new_R(L[p],F)
            R.append(Rn)

        # Объединяем получившиеся части
        last_l=L[32]
        kon=last_l+Rn
    
        # Сохраняем зашифрованную часть в массив N1
        N1.append(text_from_bits(last_l))

        # Расшифровываем
        Lo=[]
        Ro=[]
        lo = len(kon) + 1 
        Lo.append(kon[0:l//2])
        Ro.append(kon[l//2:])

        split_key2=split_key[::-1]
        for p in range(32):
            # Преобразуем левую часть и ключ
            vhod1=func_preobr(Lo[p],split_key2[p])

            # Выполняем перестановку
            Fo=table_perestanovok(Sblock,vhod1)

            # Сохраняем правую часть и вычисляем новую левую
            Ro.append(Lo[p]) 
            Lno=new_R(Ro[p],Fo)
            Lo.append(Lno)

        # Объединяем получившиеся части и сохраняем результат в N2
        ogo1=Ro[32]
        kon1=Lno+ogo1
        
        N2.append(text_from_bits(kon1))

    # Выводим результат
    print("Полное шифрованное сообщение: \n","".join(N1))
    print("Полное дешифрованное сообщение: \n","".join(N2))



def two(Ot,key,N1,N2):
    # Переводим ключ в двоичный вид
    key_ascii=text_to_bits(key)
    # Делим ключ на блоки по 32 бита
    n = 32
    split_key=(re.findall('.{%s}' % n, key_ascii))
    # Создаем копии ключа
    cop1=split_key
    cop2=split_key
    cop3=split_key[::-1]
    # Объединяем все три копии вместе с оригинальным ключом для получения нужной пооследовательности(0-7,0-7,0-7,7-0)
    split_key=split_key+cop1+cop2+cop3

    # Переводим текст в двоичный вид
    LR=(text_to_bits(Ot))

    L=[]
    R=[]
    l = len(LR) + 1 
    # Делим текст на левую и правую половины
    L.append(LR[0:l//2])
    R.append(LR[l//2:])

    # Производим 32 раунда шифрования
    for p in range(32):
        vhod=func_preobr(R[p],split_key[p])
        F=table_perestanovok(Sblock,vhod)
        L.append(R[p]) 
        Rn=new_R(L[p],F)
        R.append(Rn)

    # Получаем последнюю левую часть и правую часть
    last_l=L[32]
    kon=last_l+Rn

    # Выводим зашифрованное сообщение
    print("Шифрованное сообщение:\n",text_from_bits(last_l))

    Lo=[]
    Ro=[]
    lo = len(kon) + 1 
    # Делим зашифрованное сообщение на левую и правую половины
    Lo.append(kon[0:l//2])
    Ro.append(kon[l//2:])
    
    # Создаем обратный порядок ключа
    split_key2=split_key[::-1]
    # Производим 32 раунда расшифрования
    for p in range(32):
        vhod1=func_preobr(Lo[p],split_key2[p])
        Fo=table_perestanovok(Sblock,vhod1)
        Ro.append(Lo[p]) 
        Lno=new_R(Ro[p],Fo)
        Lo.append(Lno)

    # Получаем последнюю правую часть и дешифрованное сообщение
    last_R=Ro[32]
    kon1=Lno+last_R

    # Выводим дешифрованное сообщение
    print("Дешифрованное сообщение:\n",text_from_bits(last_R))



# S-блоки
Sblock = [
    [1,15,13,0,5,7,10,4,9,2,3,14,6,11,8,12],
    [13,11,4,1,3,15,5,9,0,10,14,7,6,8,2,12],
    [4,11,10,0,7,2,1,13,3,6,8,5,9,12,15,14],
    [6,12,7,1,5,15,13,8,4,10,9,14,0,3,11,2],
    [7,13,10,1,0,8,9,15,14,4,6,12,11,2,5,3],
    [5,8,1,13,10,3,4,2,14,15,12,7,6,0,9,11],
    [14,11,4,12,6,13,15,10,2,3,8,1,0,7,5,9],
    [4,10,9,2,13,8,0,14,6,11,1,12,7,15,5,3]
]

# Открытый текст
Ot = "Че хочешь"
Ot_list = list(Ot)

# Замена буквы "й" на "и" так как с "й" могут возникать проблемы
for i in range(len(Ot_list)):
    if Ot_list[i] == "й":
        Ot_list[i] = "и"
Ot = "".join(Ot_list)

print("Открытый текст:\n", Ot)

# Дополнение открытого текста пробелами, чтобы его длина была кратна 8
while len(Ot) % 8 != 0:
    Ot = Ot + " "

# Разбиение открытого текста на блоки по 8 символов
if len(Ot) > 8:
    pom = (re.findall('.{%s}' % 8, Ot))

# Ключ
key = "Пошла алина в лес собирать грибы"

# Списки для хранения преобразованных блоков
N1 = []
N2 = []

# Выбор функции шифрования в зависимости от длины открытого текста
if len(Ot) != 8:
    # Если открытый текст состоит из нескольких блоков
    # вызываем функцию one(), которая применяет шифрование к каждому блоку отдельно
    Ot = pom
    one(Ot, key, N1, N2)
else:
    # Если открытый текст состоит из одного блока
    # вызываем функцию two(), которая применяет шифрование к этому блоку
    two(Ot, key, N1, N2)
