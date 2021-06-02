import easyocr
from docx import Document
from docx.shared import Pt
from docx.enum.style import WD_STYLE_TYPE


def print_hi():
    doc = Document()

    parag = doc.add_paragraph("Hello!")

    font_styles = doc.styles
    font_charstyle = font_styles.add_style('CommentsStyle', WD_STYLE_TYPE.CHARACTER)
    font_object = font_charstyle.font
    font_object.size = Pt(12)
    font_object.name = '宋体'

    parag.add_run("this word document, was created using Times New Roman", style='CommentsStyle').bold = True
    parag.add_run("Python", style='CommentsStyle').italic = True
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
    parag = doc.add_paragraph()

    font_styles = doc.styles
    font_charstyle = font_styles.add_style('CommentsStyle', WD_STYLE_TYPE.CHARACTER)
    font_object = font_charstyle.font
    font_object.size = Pt(12)
    font_object.name = '宋体'

    for i in range(len(result)):
        (bbox, text, prob) = result[i]
        (topY, bottomY) = parse_pos(bbox)
        print(f'Detected text: {text}')
        if i == 0:
            parag.add_run(text, style='CommentsStyle')
        else:
            (preBbox, preText, preProb) = result[i - 1]
            (preTopY, preBottomY) = parse_pos(preBbox)
            # print(f'topY: {topY} bottomY:{bottomY}" preTopY: {preTopY} preBottomY: {preBottomY}')
            if topY > preBottomY:
                parag.add_run().add_break()
            parag.add_run(str(text), style="CommentsStyle")

    doc.save("demo.docx")


def parse_pos(bbox):
    (top_left, top_right, bottom_right, bottom_left) = bbox
    topY = min(top_left[1], top_right[1])
    bottomY = max(bottom_left[1], bottom_right[1])
    return topY, bottomY


def font_size(bbox):
    (top_left, top_right, bottom_right, bottom_left) = bbox
    print(bottom_left[1] - top_left[1])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi()
    debug("/Users/admin/Desktop/b.png")
    # font_size(([30, 29], [521, 29], [521, 107], [30, 107]))
