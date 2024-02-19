import docx
import MTK2
from docx.shared import RGBColor
from docx.enum.text import WD_COLOR_INDEX

def run_get_spacing(text_block):
    rPr = text_block._r.get_or_add_rPr()
    spacings = rPr.xpath("./w:spacing")
    return spacings


def run_get_scale(text_block):
    rPr = text_block._r.get_or_add_rPr()
    scale = rPr.xpath("./w:w")
    return scale


def main(doc):
    collect_color,collect_font_size,collect_highlight,collect_scale,collect_spacing=[],[],[],[],[]
    kod = ''
    for String in doc.paragraphs:
        for text_block in String.runs:

            font_color = text_block.font.color.rgb
            collect_color.append(font_color)
          
            font_size = text_block.font.size
            collect_font_size.append(font_size)

            font_highlight_color = text_block.font.highlight_color
            collect_highlight.append(font_highlight_color)
          
            font_scale = run_get_scale(text_block)
            collect_scale.append(font_scale)
            
            font_spacing = run_get_spacing(text_block)
            collect_spacing.append(font_spacing)

            if font_color != RGBColor(0, 0, 0):
                for i in range(len(text_block.text)):
                    kod += '1'
            else:
                for i in range(len(text_block.text)):
                    kod += '0'
    
    while len(kod)%8!=0:
        kod += "0"
    print(f'Код- {kod}\n')
    # print(len(kod))

    if len(set(collect_color))!=1:
        print('Стеганографическое преобразование - изменение спектра цвета шрифта\n')
    else: pass 

    if len(set(collect_font_size))!=1:
        print('Стеганографическое преобразование - изменение размера шрифта\n')
    else: pass 

    if len(set(collect_highlight))!=1:
        print('Стеганографическое преобразование - изменение цвета фона шрифта\n')
    else: pass

    if not all(not sublist for sublist in collect_scale):
        print('Стеганографическое преобразование - изменение масштаба шрифта\n')
    else: pass

    if not all(not sublist for sublist in collect_spacing):
        print('Стеганографическое преобразование - изменение межстрочного интервала\n')
    else: pass

    dec_text = MTK2.MTK2_decode(kod)
    print('MTK-2: ')
    print(dec_text)
    dec_text = bytes.fromhex(hex(int(kod, 2))[2:]).decode(encoding="koi8_r")
    print('koi8 - ',dec_text)
    dec_text = bytes.fromhex(hex(int(kod, 2))[2:]).decode(encoding="cp866")
    print('cp866 - ',dec_text)
    dec_text = bytes.fromhex(hex(int(kod, 2))[2:]).decode(encoding="Windows-1251")
    print('Windows-1251 - ',dec_text)

if __name__ == '__main__':
    doc = docx.Document('C:/D/5 курс/progs/2 семестр/Сафарьян/2/01variant.docx')
    main(doc)