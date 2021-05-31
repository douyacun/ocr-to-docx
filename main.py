import easyocr
from docx import Document
import cv2
import matplotlib.pyplot as plt


def print_hi():
    document = Document()
    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True
    document.save('test.docx')


def read_image(filepath: str):
    reader = easyocr.Reader(lang_list=['ch_sim', 'en'], gpu=False)
    res = reader.readtext(filepath)
    for v in res:
        print(v)


def debug(filepath: str):
    reader = easyocr.Reader(lang_list=['ch_sim', 'en'], gpu=False)
    result = reader.readtext(filepath)

    for (bbox, text, prob) in result:
        if prob >= 0.5:
            # display
            print(f'Detected text: {text} (Probability: {prob:.2f})')
            # get top-left and bottom-right bbox vertices
            # (top_left, top_right, bottom_right, bottom_left) = bbox
            print(bbox)


def font_size(bbox):
    (top_left, top_right, bottom_right, bottom_left) = bbox
    print(bottom_left[1] - top_left[1])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi()
    # debug("/Users/liuning/Desktop/a.png")
    font_size(([30, 29], [521, 29], [521, 107], [30, 107]))
