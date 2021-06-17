import pytesseract
from PIL import Image
from xml.etree import ElementTree
from xml.etree import ElementTree


def to_pdf(filepath):
    pdf = pytesseract.image_to_pdf_or_hocr(Image.open(filepath), extension="pdf")
    with open('test.pdf', 'w+b') as f:
        f.write(pdf)


def to_docx(filepath):
    # Get HOCR output
    hocr = pytesseract.image_to_alto_xml(filepath, lang="chi_sim")
    # with open('test.xml', 'w+b') as f:
    #     f.write(hocr)
    parse_hocr_xml(hocr=hocr)


def parse_hocr_xml(hocr, filepath):
    if hocr != "":
        root = ElementTree.fromstring(hocr)
        # root = tree.getroot()
        print_element(root)

    if filepath != "":
        tree = ElementTree.parse(filepath)
        root = tree.getroot()
        print_element(root)


def print_element(element: ElementTree.Element):
    ns = "http://www.loc.gov/standards/alto/ns-v3#"
    # print(element.find(path="{%s}Layout" % ns).find())
    # for child in element:
    #     print(f"{child.tag} {child.attrib}")
    # print(element.findall("Layout"))
    for block in element.find("{%s}Layout" % ns).find("{%s}Page" % ns).find("{%s}PrintSpace" % ns).findall(
            "{%s}ComposedBlock" % ns):
        print(block.tag, block.attrib)


if __name__ == '__main__':
    # to_docx("/Users/liuning/Desktop/image-ocr/g.png")
    parse_hocr_xml(filepath="test.xml", hocr="")
