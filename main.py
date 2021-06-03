import easyocr
from docx import Document
from docx.shared import Pt
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn


def print_hi():
    doc = Document()

    doc.styles['Normal'].font.name = u'宋体'
    doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    doc.styles['Normal'].font.size = Pt(12)
    parag = doc.add_paragraph("")

    # font_styles = doc.styles
    # font_charstyle = font_styles.add_style('CommentsStyle', WD_STYLE_TYPE.CHARACTER)
    # font_object = font_charstyle.font
    # font_object.size = Pt(12)
    # font_object.name = u'宋体'

    # print(font_object.name)

    parag.add_run("this word document, was created using Times New Roman").bold = True
    run = parag.add_run("Python")
    # print(run._element.rPr)

    doc.save("test.docx")


def read_image(filepath: str):
    reader = easyocr.Reader(lang_list=['ch_sim', 'en'], gpu=False)
    res = reader.readtext(filepath)
    for v in res:
        print(v)


# 1. 统一字体，判断字体大小？
# 2. 行间距
# 3. 横间距缩进
# 4. 标点符号，转中文
def debug(filepath: str):
    reader = easyocr.Reader(lang_list=['ch_sim', 'en'], gpu=False)
    result = reader.readtext(filepath)

    doc = Document()

    doc.styles['Normal'].font.name = u'宋体'
    doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    doc.styles['Normal'].font.size = Pt(12)

    parag = doc.add_paragraph()

    # font_styles = doc.styles
    # font_charstyle = font_styles.add_style('CommentsStyle', WD_STYLE_TYPE.CHARACTER)
    # font_object = font_charstyle.font
    # font_object.size = Pt(12)
    # font_object.name = u'宋体'
    # lineSpace = 0
    # paragraphSpace = 0

    for i in range(len(result)):
        (bbox, text, prob) = result[i]
        (topY, bottomY) = parse_pos(bbox)
        (preBbox, preText, preProb) = result[i - 1]
        (preTopY, preBottomY) = parse_pos(preBbox)
        print(f'text: {text} topY: {topY} bottomY:{bottomY}" preTopY: {preTopY} preBottomY: {preBottomY}')

        if i == 0:
            run = parag.add_run(text)
            run.font.size = Pt(20)
        else:
            if topY > preBottomY:
                parag.add_run().add_break()
                parag.add_run(str(text))

    doc.save("demo.docx")


def parse_pos(bbox) -> dict:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    res = dict()
    res["topY"] = min(bottom_left[1], top_left[1])
    res["bottomY"] = min(bottom_left[1], bottom_right[1])
    res["leftX"] = min(top_left[0], bottom_left[0])
    res["rightX"] = min(top_right[0], bottom_right[0])
    res["width"] = res["rightX"] - res["leftX"]
    res["height"] = res["bottomY"] - res["topY"]
    return res


def page_border(res):


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi()
    # debug("/Users/admin/Desktop/c.png")
    debug("/Users/liuning/Desktop/d.png")
    # font_size(([30, 29], [521, 29], [521, 107], [30, 107]))
