from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from word import word


def NewDefaultParagraph():
    return {
        "is_center": False,
        "first_line_indent": False,
        "text": "",
        "font_size": 0
    }


class Paragraph:
    def __init__(self, word: word, doc: Document, data):
        """
        :param doc:
        :param data:
        """
        self.word = word
        self.doc = doc
        self.data = data

    def get_paragraph_value(self, field):
        """
        段落取值，0值填充默认值
        :param field: 字段名
        :return:
        """
        default = {
            "is_center": False,
            "first_line_indent": False,
            "text": "",
            "font_size": self.word.get_page_value("font_size")
        }
        if field in self.data:
            return self.data[field]
        else:
            return default[field]

    def write_docx(self):
        p = self.doc.add_paragraph()
        if self.get_paragraph_value("is_center"):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif self.get_paragraph_value("first_line_indent"):
            p.paragraph_format.first_line_indent = Pt(self.word.get_page_value("font_size"))

        p.add_run(self.get_paragraph_value("text")).font.size = Pt(self.get_paragraph_value("font_size"))
