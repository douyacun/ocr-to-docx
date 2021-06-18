import json
import logging
import easyocr
import math
import click
from word.word import NewDefaultPage
from word.word import Word

DIFF = 20
BASE_FONT_SIZE = 12
FONT_DIFF = 2


@click.group()
def handle():
    pass


@click.command("ocr_to_docx")
@click.argument("filepath")
@click.argument("outfile")
def ocr_to_docx(filepath, outfile):
    logging.basicConfig(level="ERROR")
    reader = easyocr.Reader(lang_list=['ch_sim', 'en'], gpu=False)
    result = reader.readtext(filepath)

    data = merge_line(result)
    click.echo(json.dumps(data))

    data["outfile"] = outfile

    Word(data).write_docx().save()


@click.command()
@click.argument("filepath")
# 1. 统一字体，判断字体大小？
# 2. 行间距
# 3. 横间距缩进
# 4. 标点符号，转中文
def debug(filepath):
    logging.basicConfig(level="DEBUG")
    # print(easyocr.__version__)

    # reader = easyocr.Reader(lang_list=['ch_sim', 'en'], gpu=False)
    # result = reader.readtext(filepath)
    # logging.debug(json.dumps(merge_line(result)))


def merge_line(res):
    """
    合并同一行
    1. 判断是否位同一行, 同一行：topY <= preBottomY
    2. 判断是否需要换行，本行最后一个字没有达到最右侧边界
    3. 首行缩进？居中？
    """
    page = NewDefaultPage()
    lineList = list()
    border = parse_border(res)
    logging.debug(f"border: {border}")
    fontList = parse_fontsize(res)
    logging.debug(f"font: {fontList}")

    line = {"text": "", "first_line_indent": False, "font_size": BASE_FONT_SIZE, "line_count": 0, "is_center": False}

    for i in range(len(res)):
        (bbox, text, prob) = res[i]
        pos = parse_pos(bbox)
        logging.debug(f"text {text} pos: {pos}")
        prePos = parse_pos(res[i - 1][0])
        if i == 0:
            line["text"] = text
            line["font_size"] = get_fontsize(fontList, pos["height"])
            line["line_count"] += 1
            if pos["leftX"] > border["left"]:
                line["first_line_indent"] = True
        else:
            # 在图片中可以确认是统一行
            if pos["topY"] <= prePos["topY"] + 2 or pos["bottomY"] <= prePos["bottomY"] + 2:
                line["text"] += text
            else:
                # 确定是否需要换行
                if prePos["rightX"] >= border["right"] and pos["leftX"] <= border["left"]:
                    line["line_count"] += 1
                    line["text"] += text
                else:
                    # 前一行入库
                    if line["line_count"] == 1:
                        line["font_size"] = get_fontsize(fontList, prePos["height"])
                        if math.fabs(prePos["leftX"] - border["left"]) > 200 and \
                                math.fabs(prePos["rightX"] - border["right"]) > 200:
                            line["is_center"] = True
                            line["first_line_indent"] = False
                    page["paragraph"].append(line)
                    # 开头
                    line = {"text": text, "first_line_indent": False, "font_size": BASE_FONT_SIZE, "line_count": 1,
                            "is_center": False}
                    if pos["leftX"] > border["left"]:
                        line["first_line_indent"] = True

    if line["text"] != "":
        page["paragraph"].append(line)

    # logging.debug(lineList)
    return page


def get_fontsize(fontList: list, height: int):
    for v in fontList:
        if v["minHeight"] <= height <= v["maxHeight"]:
            return v["fontSize"]
    return BASE_FONT_SIZE


# 预估字体大小
def parse_fontsize(res) -> list:
    fontList = []
    heightDict = {}
    for i in range(len(res)):
        (bbox, text, prob) = res[i]
        pos = parse_pos(bbox)
        if pos["height"] in heightDict:
            heightDict[pos["height"]] += 1
        else:
            heightDict[pos["height"]] = 1

    c = 0
    midHeight = 0  # 中分位高度
    for k in sorted(heightDict.keys()):
        if heightDict[k] > c:
            c = heightDict[k]
            midHeight = k

    font = {"minHeight": 0, "maxHeight": midHeight, "fontSize": BASE_FONT_SIZE}
    fontList.append(font)
    for k in sorted(heightDict.keys()):
        # 初始值
        if k > font["maxHeight"]:
            font = {"minHeight": k, "maxHeight": k + FONT_DIFF,
                    "fontSize": math.floor(k / midHeight * BASE_FONT_SIZE)}
            fontList.append(font)
    return fontList


def parse_pos(bbox) -> dict:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    res = {
        "topY": min(bottom_left[1], top_left[1]),
        "bottomY": min(bottom_left[1], bottom_right[1]),
        "leftX": min(top_left[0], bottom_left[0]),
        "rightX": min(top_right[0], bottom_right[0]),
    }
    res["width"] = res["rightX"] - res["leftX"]
    res["height"] = res["bottomY"] - res["topY"]
    return res


# 左右边界
def parse_border(res):
    border = dict()
    if len(res) == 0:
        return border

    right = 0
    left = 0
    for i in range(len(res)):
        (bbox, text, prob) = res[i]
        (top_left, top_right, bottom_right, bottom_left) = bbox
        if i == 0:
            left = top_left[0]
        right = max(right, top_right[0], bottom_right[0])
        left = min(left, top_left[0], bottom_left[0])

    border["left"] = left + DIFF
    border["right"] = right - DIFF
    return border


handle.add_command(ocr_to_docx)
# handle.add_command(debug)

if __name__ == '__main__':
    handle()
