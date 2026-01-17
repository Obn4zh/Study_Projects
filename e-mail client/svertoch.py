import numpy as np
import binascii

def pause():
    pass

def encode(posled):
    global dvoinoySpisElemIndex, zakodir
    n=2


    def text_to_bits(posled, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int(binascii.hexlify(posled.encode(encoding, errors)), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))


    spisok_text_to_bit = text_to_bits(posled)
    spis_posled=[]
    for i in range(len(spisok_text_to_bit)):
        spis_posled.append(spisok_text_to_bit[i])


    # print("Важно",spisok_text_to_bit)
    #
    #
    # print("Введённая последовательность в бинарном представлении: ",spis_posled)


    poFactu=[]
    registr=np.zeros(3)

    dvoinoySpisElemIndex=[['0','1'],['1','2']]

    # print("Индексы слогаемых: ",dvoinoySpisElemIndex)
    # print("Состояния регистра:")
    # print(registr)

    poFactu=[]
    for i in range(len(spis_posled)):
        registr=np.delete(registr,2)
        registr=np.insert(registr,0,spis_posled[i])
        # print(registr)

        for j in range(len(dvoinoySpisElemIndex)):
            spisElemSlogaem=[]
            for k in dvoinoySpisElemIndex[j]:
                spisElemSlogaem.append(registr[int(k)])
            a=sum(spisElemSlogaem)
            poFactu.append(a%2)

    for i in range(len(poFactu)):
        poFactu[i]=int(poFactu[i])
        poFactu[i]=str(poFactu[i])

    zakodir=[]

    for i in range(0,len(poFactu),n):
        zakodir.append("".join(poFactu[i:i+n]))

    zakodirstr="".join(zakodir)
    # print(zakodir)
    print("Закодированная последовательность: ", zakodirstr)
    return zakodirstr


#ДЕКОДИРОВАНИЕ
def decode(zakodir):

    string_code="".join(zakodir)
    spisok_text_to_bit = string_code

    dvoinoySpisElemIndex = [['0', '1'], ['1', '2']]
    registrs = []
    kol_registrov = 0

    decodir_str = ''
    # находим кол-во регистров по максимальному элементу в сумматоре и обнуляем их
    for i in dvoinoySpisElemIndex:
        if kol_registrov < int(max(i)):
            kol_registrov = int(max(i))

    for i in range(kol_registrov + 1):
        registrs.append(0)

    def nolVregister():
        for i in reversed(range(len(registrs))):
            registrs[i] = registrs[i - 1]
        registrs[0] = 0
        return registrs

    def ProverochBits():
        # print("!!!!!!!!!!!!!!",registrs)
        global proverochnie_bits
        proverochnie_bits = ''
        for j in range(len(dvoinoySpisElemIndex)):
            c = 0
            for m in range(len(dvoinoySpisElemIndex[j])):
                c += registrs[int(dvoinoySpisElemIndex[j][m])]
            if c % 2 == 1:
                proverochnie_bits += ''.join('1')
            elif c % 2 == 0:
                proverochnie_bits += ''.join('0')
        return proverochnie_bits

    for i in range(len(zakodir)):
        nolVregister()
        ProverochBits()
        if proverochnie_bits != zakodir[i]:
            registrs[0] = 1
            decodir_str += ''.join('1')
        elif proverochnie_bits == zakodir[i]:
            decodir_str += ''.join('0')
    # print("Декодированная последовательность в бинарном представлении: ",decodir_str)

    if decodir_str != spisok_text_to_bit:
        dlina = len(decodir_str) - len(spisok_text_to_bit)
        decodir_str = decodir_str[:-dlina]


    def text_from_bits(binstring, encoding='utf-8', errors='surrogatepass'):
        n = int(binstring, 2)
        return int2bytes(n).decode(encoding, errors)


    def int2bytes(i):
        hex_string = '%x' % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

    decodir_poFactu = text_from_bits(decodir_str)

    # print("Декодированная последовательность: ",decodir_poFactu)
    return decodir_poFactu