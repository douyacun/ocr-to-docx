import json

from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from word.paragraph import Paragraph


def NewDefaultPage():
    return {
        "font": u"宋体",
        "font_size": 12,
        "paragraph": [],
        "outfile": "temp/test.docx"
    }


class Word:
    def __init__(self, data):
        """
        :param data: 页面数据
        """
        if isinstance(data, str):
            self.data = json.load(data)
        elif isinstance(data, object):
            self.data = data
        self.doc = None
        self.new_docx()

    def new_docx(self):
        self.doc = Document()
        # self.doc.styles['Normal'].font.name = self.get_page_value("font")
        self.doc.styles['Normal'].font.name = u"宋体"
        # self.doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), self.get_page_value("font"))
        self.doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u"宋体")

        self.doc.styles['Normal'].font.size = Pt(self.get_page_value("font_size"))

    def get_page_value(self, field: str):
        """
        页面取值，0值填充默认值
        :param field:
        :return:
        """
        default = {
            "font": u"宋体",
            "font_size": 12,
            "paragraph": [],
            "outfile": "temp/test.docx"
        }
        if field in self.data:
            return self.data[field]
        else:
            return default[field]

    def write_docx(self):
        for p in self.get_page_value("paragraph"):
            pl = Paragraph(word=self, doc=self.doc, data=p)
            pl.write_docx()

        return self

    def save(self):
        self.doc.save(self.get_page_value("outfile"))
